---
name: food-news-aggregator
overview: 构建一个全球食品饮料行业资讯聚合网站，包含 Python RSS 抓取脚本、纯静态前端、GitHub Actions 自动化调度，并指导用户完成 GitHub 账号创建和 GitHub Pages 部署。
design:
  architecture:
    framework: html
---

## 用户需求概要

构建一个全球食品饮料行业资讯聚合网站，用于个人每天集中查看来自固定来源的最新资讯。

### 核心功能要求

**1. 资讯来源**

- 用户将提供 Excel 形式的网站列表（待发），先用示例网站完成框架
- 网站语言：多语言混合（英文为主，混有中日韩法等）
- 优先使用 RSS 源，无法获取则尝试页面抓取

**2. 信息提取字段**

- 标题
- 摘要（200字以内，无摘要取正文前几句）
- 原文链接
- 发布时间（统一转为北京时间 UTC+8）
- 来源站点名称

**3. 聚合规则**

- 所有来源合并，按发布时间倒序排列
- 根据标题+链接去重
- 只展示最近7天资讯（数据文件保留历史）

**4. 前端展示**

- 纯静态页面（HTML+CSS+JS）
- 中文界面
- 页面标题：「全球食品资讯·每日速览」
- 卡片式布局，浅色背景，响应式（适配手机和桌面）
- 顶部固定筛选栏（按来源多选过滤）
- 关键词搜索框（实时搜索标题和摘要）
- 点击标题或「阅读原文」在新标签页打开原文

**5. 自动化更新**

- Python 抓取脚本，每天自动运行
- GitHub Actions 调度：北京时间 08:00 和 20:00 各一次（即 UTC 00:00 和 12:00）
- 失败自动重试
- 输出数据为 JSON 文件

**6. 部署与访问**

- 用户无 GitHub 账号，需指导创建
- 部署到 GitHub Pages（免费静态托管）
- 最终提供可直接访问的网址

**7. 可维护性**

- 所有配置集中在单一配置文件（sources.yaml 或 config.json）
- 完整 README 说明如何增减新闻源、手动运行更新、修改定时

### 工作环境

- 工作空间：`c:/Users/Administrator/WorkBuddy/Claw`（空目录）
- 系统：Windows（PowerShell）
- Python：`C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe`

## 技术方案

### 技术栈选择

| 层次 | 技术选型 | 说明 |
| --- | --- | --- |
| 前端 | 纯 HTML5 + CSS3 + Vanilla JS | 无需构建工具，纯静态部署 |
| 数据抓取 | Python 3.13 + feedparser + requests + BeautifulSoup4 | 多语言 RSS 解析 + 页面抓取备选 |
| 数据格式 | JSON | 前端直接读取，供 GitHub Actions 生成 |
| 持续集成 | GitHub Actions | 定时任务 + 自动部署 |
| 托管服务 | GitHub Pages | 免费静态托管，绑定自定义域名可选 |


### 项目架构

```
food-news-aggregator/
├── .github/
│   └── workflows/
│       └── update.yml          # GitHub Actions 调度配置
├── data/
│   ├── news_latest.json        # 生成的最新资讯数据（7天内）
│   └── news_archive.json       # 历史数据存档
├── scripts/
│   ├── config.py               # 配置加载器
│   ├── fetcher.py              # 抓取器基类
│   ├── rss_fetcher.py          # RSS 抓取实现
│   ├── scraper.py              # 页面抓取备选实现
│   └── main.py                 # 主入口脚本
├── web/
│   ├── index.html               # 主页面
│   ├── styles.css              # 样式表
│   └── app.js                  # 前端逻辑
├── sources.yaml                # 资讯源配置文件
├── README.md                    # 项目说明文档
├── requirements.txt             # Python 依赖
└── .gitignore                   # Git 忽略文件
```

### 核心模块设计

#### 1. 配置管理（sources.yaml）

```
sources:
  - name: "FoodNavigator"
    url: "https://www.foodnavigator.com"
    rss: "https://www.foodnavigator.com/rss"
    enabled: true
    
  - name: "Just Food"
    url: "https://www.just-food.com"
    rss: "https://www.just-food.com/rss"
    enabled: true
    
  - name: "食品伙伴网"
    url: "https://news.foodmate.net"
    rss: "https://www.foodmate.net/rss"
    enabled: true

settings:
  retention_days: 7
  summary_max_length: 200
  update_schedule: "0,12 * * *"
```

#### 2. 数据模型

```
{
  "last_updated": "2026-04-25T08:00:00+08:00",
  "sources": ["FoodNavigator", "Just Food", ...],
  "articles": [
    {
      "id": "uuid-hash",
      "title": "文章标题",
      "summary": "摘要内容...",
      "url": "https://...",
      "published_at": "2026-04-25T06:30:00+08:00",
      "source": "FoodNavigator",
      "language": "en"
    }
  ]
}
```

#### 3. GitHub Actions 工作流

- 触发时间：UTC 00:00 和 12:00（对应北京 08:00 和 20:00）
- 执行步骤：安装依赖 → 运行抓取脚本 → 提交 JSON → 触发 Pages 部署
- 重试机制：`on: workflow_dispatch` + `retries: 2`

### 关键实现决策

1. **多语言处理**：使用 `feedparser` 解析 RSS，编码自动检测；摘要提取支持 Unicode 多语言
2. **去重策略**：基于 `url` 字段的 SHA256 哈希生成唯一 ID，避免重复
3. **时区处理**：所有时间统一转为北京时间（UTC+8）存储和展示
4. **前端搜索**：使用 JavaScript 原生 `filter()` 实现实时搜索，无外部依赖
5. **部署策略**：JSON 数据提交到 `gh-pages` 分支，GitHub Pages 自动托管

### 性能考量

- 前端加载：JSON 文件预计 < 500KB，包含约 200-500 条7天内资讯
- 搜索性能：前端过滤 O(n) 遍历，实测 < 50ms
- GitHub Actions：每次执行约 2-5 分钟（取决于网站响应速度）