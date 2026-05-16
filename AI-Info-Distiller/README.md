# 🌟 AI Info Distiller (AI 信息蒸馏器)

> 天下苦信息过载久矣！这是一个为你量身定制的**全自动 AI 知识助理**。它能帮你24小时盯紧感兴趣的资讯源，用 AI 榨干水分，每周一早晨把最核心的洞察送到你的微信里。

## 💡 为什么做这个项目？

在海量公众号、科技博客和新闻源中，90% 的内容是噪音、软文或情绪宣泄。
本项目旨在通过 **RSS + LLM (大语言模型)** 构建一条纯净的“知识流水线”，让你告别信息焦虑，只看真正有密度的思考。

## 🚀 核心特性

- 🤖 **AI 深度提炼**：接入 DeepSeek 大模型，自动过滤无效水文，将万字长文浓缩为 **“核心事实 + 深度洞察 + 行动启发”**。
- 📡 **全领域 RSS 兼容**：支持任意 RSS 订阅源（科技博客、财经智库、甚至是你自己部署的 WeRSS 微信公众号节点）。
- ⚡ **零成本自动化**：依托 GitHub Actions 定时任务，无需自己购买服务器即可实现 7x24 小时云端运行。
- 📱 **微信无缝推送**：打通 PushPlus 接口，每周定时将排版精美的 Markdown 周报推送到你的微信。

---

## 🛠️ 架构说明

`RSS 源 (信息采集)` ➡️ `Python 脚本 (过滤近期文章)` ➡️ `DeepSeek API (AI 深度研判)` ➡️ `PushPlus (微信投递)`

---

## 🏃‍♂️ 快速开始 (小白也能 5 分钟用上)

如果你想拥有一个完全属于自己的 AI 知识助理，只需按以下步骤操作：

### 1. Fork 本仓库
点击右上角的 `Fork` 按钮，将本项目复制到你自己的 GitHub 账号下。

### 2. 准备必需的 API 密钥
你需要去以下两个平台免费注册并获取秘钥：
- **[DeepSeek](https://platform.deepseek.com/)**：获取 `API Key`（用于 AI 分析，目前注册赠送免费额度）。
- **[PushPlus](https://www.pushplus.plus/)**：扫码登录，在“发送消息”中获取你的 `Token`（用于微信推送）。

### 3. 配置 GitHub Secrets (安全存储密钥)
在你 Fork 后的仓库页面，进入 `Settings` -> `Secrets and variables` -> `Actions`，点击 `New repository secret`，添加以下两个变量：
- `DEEPSEEK_API_KEY`：填入你的 DeepSeek API 秘钥。
- `PUSHPLUS_TOKEN`：填入你的 PushPlus Token。

### 4. 定制你的专属信息源
打开仓库中的 `main.py` 文件，找到 `# 📢 [用户自定义区]`：
- 修改 `DOMESTIC_FEEDS` 和 `INTL_FEEDS` 列表，填入你想看的 RSS 链接。
- 修改 `REPORT_TITLE` 换成你喜欢的周报名字。

### 5. 坐等收信 (或手动触发)
- **自动触发**：系统已设定北京时间**每周一早晨 7:00** 自动运行。
- **手动测试**：进入仓库的 `Actions` 标签页，点击左侧的 `AI Weekly Info Distiller`，然后点击右侧的 `Run workflow` 按钮进行首次测试。

---

## 🧩 进阶玩法：抓取微信公众号 (WeRSS 联动)

如果你极其依赖微信公众号生态，但又不想手动刷手机，可以结合 [WeRSS](https://github.com/We-mp-RSS/we-mp-rss) 项目使用：
1. 在本地或轻量云服务器上部署 WeRSS。
2. 将 WeRSS 生成的私有 RSS 链接填入 `main.py` 的 `DOMESTIC_FEEDS` 中。
3. **注意**：如果 WeRSS 部署在云服务器，请确保防火墙已放行相应端口，且 GitHub Actions 能够访问该公网 IP。

---

## 🤝 贡献与感谢

欢迎提交 PR 或 Issue 来完善这个工具！如果这个项目帮你在信息洪流中找回了专注力，欢迎点个 ⭐️ **Star** 支持一下！

**License:** MIT License