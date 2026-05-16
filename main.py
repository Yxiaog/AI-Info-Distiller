import os
import requests
import feedparser
from openai import OpenAI
from datetime import datetime, timedelta
import time
from email.utils import parsedate_to_datetime

# ==========================================
# 1. 核心环境配置 (API 密钥)
# ==========================================
# 📢 [用户自定义区]：请确保你的运行环境或 GitHub Actions 中配置了这两个环境变量
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
PUSHPLUS_TOKEN = os.environ.get("PUSHPLUS_TOKEN")

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

# ==========================================
# 2. 终极信息源矩阵 (RSS 订阅源)
# ==========================================
# 📢 [用户自定义区]：在这里填入你感兴趣的国内源（比如你本地部署的 WeRSS 链接，或独立博客 RSS）
DOMESTIC_FEEDS = [
    "http://124.223.40.126:8001/feed/all.rss" # 示例：本地微信公众号聚合源
]

# 📢 [用户自定义区]：在这里填入你感兴趣的国际源（如科技、财经、AI、设计等领域的 RSS）
INTL_FEEDS = [
    "https://www.theverge.com/rss/index.xml",           # 示例：科技资讯 The Verge
    "https://hnrss.org/frontpage",                      # 示例：极客论坛 Hacker News
    "https://www.economist.com/finance-and-economics/rss.xml" # 示例：经济学人
]

# 📢 [用户自定义区]：自定义你的周报名称和你的专属身份/格言
REPORT_TITLE = "🌍 专属【AI 洞察周报】"
REPORT_SUBTITLE = "由 DeepSeek 强力驱动，为您过滤信息噪音，提炼高维认知。"

# ==========================================
# 3. 抓取近期更新的 RSS 文章
# ==========================================
def fetch_recent_rss(feed_urls, days_limit=7):
    # 📢 [用户自定义区]：默认抓取过去 7 天的内容，可修改 days_limit 参数
    print(f"📡 正在扫描订阅源，严格筛选过去 {days_limit} 天内的文章...")
    recent_items = []
    limit_date = datetime.now() - timedelta(days=days_limit)
    
    for url in feed_urls:
        try:
            feed = feedparser.parse(url)
            source_name = feed.feed.title if hasattr(feed.feed, 'title') else "精选智库"
            
            for entry in feed.entries:
                try:
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'published'):
                        pub_date = parsedate_to_datetime(entry.published).replace(tzinfo=None)
                    else:
                        continue
                        
                    if pub_date >= limit_date:
                        recent_items.append({
                            "title": entry.title,
                            "url": entry.link,
                            "summary": entry.get("summary", ""),
                            "source": source_name,
                            "pub_date": pub_date
                        })
                except Exception:
                    pass
        except Exception as e:
            print(f"解析 {url} 失败: {e}")
            
    recent_items.sort(key=lambda x: x['pub_date'], reverse=True)
    print(f"✅ 扫描完毕，共发现 {len(recent_items)} 篇新鲜文章。")
    return recent_items

# ==========================================
# 4. Jina 穿透抓取正文 (用于非微信的外部网页)
# ==========================================
def extract_full_text(url):
    jina_url = f"https://r.jina.ai/{url}"
    try:
        response = requests.get(jina_url, timeout=15)
        if response.status_code == 200:
            text = response.text
            if len(text) > 200 and "Access Denied" not in text:
                return text[:3800] 
    except Exception:
        pass
    return "抓取正文受限，请基于标题和摘要进行研判。"

# ==========================================
# 5. DeepSeek 深度剖析 (核心 AI 引擎)
# ==========================================
def analyze_with_deepseek(title, content, source_name):
    # 📢 [用户自定义区]：这是决定 AI 输出质量的灵魂 Prompt。你可以根据自己的需求调整语气和结构！
    prompt = f"""
    你是一位资深的行业分析师与知识提炼专家，擅长从繁杂的资讯中过滤噪音，提取核心价值。
    请审读这篇来自【{source_name}】的最新资讯：
    【标题】：{title}
    【正文/摘要】：{content}
    
    【判定准则】
    1. 如果该内容完全是无营养的广告、纯软文、毫无逻辑的碎片信息，请仅回复“无效资讯”。
    2. 如果内容具备一定的信息增量或阅读价值，请发挥你的专长，按以下结构输出结构化简报。

    【深度洞察产出】
    📰 **1. 核心提要**：用 1-2 句话极简概括这篇资讯的核心事实（谁做了什么，发布了什么，或探讨了什么）。
    🧠 **2. 深度洞察**：分析该事件或观点背后的底层逻辑、潜在影响或行业趋势（这件事为什么重要？说明了什么问题？）。
    🎯 **3. 行动启发**：结合这篇资讯，给读者提供一个具体的思考角度或可以直接落地的行动建议。
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个能提供高信噪比信息摘要的顶级 AI 知识助理。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "无效资讯"

# ==========================================
# 6. 流水线核心逻辑
# ==========================================
def process_news_pipeline(news_list, section_title, limit=None):
    report_text = f"## {section_title}\n\n"
    valid_count = 0
    
    for item in news_list:
        # 📢 [用户自定义区]：控制每个版块最多输出多少篇文章，防止推送超载
        if limit is not None and valid_count >= limit:
            print(f"🛑 {section_title} 已达到 {limit} 篇上限，停止分析。")
            break
            
        print(f"🧐 评估文章: {item['title'][:30]}... (发布于 {item['pub_date'].strftime('%m-%d')})")
        full_text = extract_full_text(item['url'])
        time.sleep(1.5) # 防止请求过频被封
        
        analysis = analyze_with_deepseek(item['title'], full_text, item['source'])
        
        if "无效资讯" not in analysis:
            valid_count += 1
            report_text += f"### {valid_count}. {item['title']}\n"
            report_text += f"🔗 **原文直达**：[点击阅读全文]({item['url']})\n\n"
            report_text += f"{analysis}\n\n---\n\n"
            
    if valid_count == 0:
        report_text += "> 🛡️ *本周期内暂无符合价值研判标准的新鲜动态。*\n\n---\n\n"
    return report_text

# ==========================================
# 7. 执行与微信推送
# ==========================================
if __name__ == "__main__":
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    raw_domestic = fetch_recent_rss(DOMESTIC_FEEDS)
    raw_intl = fetch_recent_rss(INTL_FEEDS)
    
    # 构建报告头部
    final_report = f"# {REPORT_TITLE}\n\n"
    final_report += f"> 📅 **生成日期**：{today_str}\n"
    final_report += f"> 💡 **订阅说明**：{REPORT_SUBTITLE}\n\n---\n\n"
    
    # 📢 [用户自定义区]：组装报告。这里设置国内最多 15 篇，国际最多 8 篇，可自行修改 limit。
    final_report += process_news_pipeline(raw_domestic, "📌 第一部分：国内精选动态", limit=15)
    final_report += process_news_pipeline(raw_intl, "🌐 第二部分：海外视野观察", limit=8)
    
    # 推送至微信 (使用 HTTPS 防止被拦截)
    try:
        requests.post("https://www.pushplus.plus/send", json={
            "token": PUSHPLUS_TOKEN,
            "title": f"【本周推送】{REPORT_TITLE} - {today_str}",
            "content": final_report,
            "template": "markdown"
        }, timeout=15)
        print("✅ 任务完成，周报已成功发送至微信！")
    except Exception as e:
        print(f"❌ 推送失败，请检查网络或 Token 配置: {e}")