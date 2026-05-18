# 🌿 全球食品资讯·每日速览

> 个人每日食品行业资讯聚合站，自动抓取多个英文/中文权威来源，集中展示，告别逐网站翻查。

**在线访问：** `https://Ailopy.github.io/global-food-news/`

---

## 功能特性

- 📡 **多源 RSS 聚合**：支持英/中/日/法等多语言网站
- 🔄 **每日自动更新**：GitHub Actions 北京时间 08:00 / 20:00 各抓取一次
- 🔍 **实时搜索**：标题 + 摘要全文检索，关键词高亮
- 🏷️ **来源多选筛选**：顶部 Chip 按钮，随时切换感兴趣的来源
- 📱 **响应式布局**：网格 / 列表双视图，手机和桌面均适配
- 🕐 **7天资讯窗口**：只展示最近一周，保持页面轻量
- ⚡ **纯静态部署**：无服务器，GitHub Pages 免费托管

---

## 项目结构

```
food-news-aggregator/
├── .github/
│   └── workflows/
│       └── update.yml        # GitHub Actions 自动化任务
├── scripts/
│   ├── __init__.py
│   ├── config.py             # 配置加载器
│   ├── rss_fetcher.py        # RSS 抓取 + 解析模块
│   └── main.py               # 主入口脚本
├── web/                      # 前端静态文件（部署目录）
│   ├── index.html            # 主页面
│   ├── styles.css            # 样式表
│   ├── app.js                # 前端逻辑
│   └── data/
│       ├── news_latest.json  # 最新7天资讯（自动生成）
│       └── news_archive.json # 历史存档（自动生成）
├── sources.yaml              # ⭐ 资讯源配置（主配置文件）
├── requirements.txt          # Python 依赖
├── .gitignore
└── README.md
```

---

## 🚀 首次部署指南（从零开始）

### 第一步：注册 GitHub 账号

1. 打开 [https://github.com](https://github.com)
2. 点击右上角 **Sign up** 按钮
3. 填写邮箱、用户名、密码（用户名会出现在你的网站链接中，建议取简洁易记的名字）
4. 验证邮箱，完成注册

### 第二步：安装 Git（Windows）

1. 打开 [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. 下载并安装（全部默认选项即可）
3. 安装完成后，在 PowerShell 中运行 `git --version` 确认安装成功

### 第三步：在 GitHub 创建仓库

1. 登录 GitHub，点击右上角 **+** → **New repository**
2. 填写：
   - Repository name: `global-food-news`
   - 选择 **Public**（GitHub Pages 免费套餐需要公开仓库）
   - **不要**勾选 "Add a README file"（我们本地已有文件）
3. 点击 **Create repository**

### 第四步：推送本地代码

在 PowerShell 中，进入项目目录（`C:\Users\Administrator\WorkBuddy\Claw`），运行：

```powershell
# 配置 Git 用户信息（替换为你的信息）
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"

# 初始化并推送
git init
git add .
git commit -m "feat: 初始化食品资讯聚合站"

# 替换 YOUR_USERNAME 为你的 GitHub 用户名
git remote add origin https://github.com/YOUR_USERNAME/food-news-aggregator.git
git branch -M main
git push -u origin main
```

> 推送时会弹出 GitHub 登录窗口，输入账号密码或使用浏览器授权即可。

### 第五步：开启 GitHub Pages

1. 打开你的仓库页面 → 点击顶部 **Settings** 标签
2. 左侧菜单找到 **Pages**
3. Source 选择 **Deploy from a branch**
4. Branch 选择 **gh-pages**，目录选择 `/ (root)`
5. 点击 **Save**

### 第六步：触发首次数据抓取

1. 在仓库页面，点击顶部 **Actions** 标签
2. 左侧找到 **每日资讯更新**
3. 点击右侧 **Run workflow** → **Run workflow**（绿色按钮）
4. 等待约 2-5 分钟，完成后 Actions 显示绿色勾号 ✅

### 第七步：访问你的网站

几分钟后，访问：

```
https://YOUR_USERNAME.github.io/food-news-aggregator/
```

🎉 **大功告成！** 之后每天北京时间 08:00 和 20:00，网站会自动更新。

---

## 📰 如何添加新闻来源

编辑 `sources.yaml` 文件，在 `sources:` 列表中添加新条目：

```yaml
- name: "来源显示名称"          # 在网站上显示的名称
  url: "https://example.com"    # 来源网站主页（用于参考）
  rss: "https://example.com/feed.xml"  # RSS/Atom Feed 地址（必填）
  type: "rss"
  language: "en"                # en/zh/ja/ko/fr
  enabled: true
```

**如何找到 RSS 地址？**
- 在网站页面搜索 RSS / Feed 图标
- 尝试常见路径：`/feed`、`/rss`、`/rss.xml`、`/feed.xml`
- 使用 RSS 发现工具：[https://rss.app/find-rss](https://rss.app/find-rss)

修改后提交并推送：
```powershell
git add sources.yaml
git commit -m "feat: 添加新来源 XXX"
git push
```

## 🔕 如何临时停用某个来源

将对应条目的 `enabled` 改为 `false`：

```yaml
- name: "某来源"
  ...
  enabled: false    # ← 改为 false
```

## ❌ 如何删除来源

直接删除 `sources.yaml` 中对应的整个条目块（从 `- name:` 到下一个 `- name:` 之间的内容）。

---

## ⚙️ 如何修改自动更新时间

编辑 `.github/workflows/update.yml`，找到 `cron:` 行：

```yaml
schedule:
  - cron: "0 0 * * *"    # UTC 00:00 = 北京 08:00
  - cron: "0 12 * * *"   # UTC 12:00 = 北京 20:00
```

Cron 格式：`分 时 日 月 星期`（UTC 时间）。

北京时间与 UTC 换算：**北京时间 = UTC + 8**，所以北京 8:00 = UTC 0:00

常用示例：
| 需求 | cron 表达式 |
|------|------------|
| 每天北京 08:00 | `0 0 * * *` |
| 每天北京 20:00 | `0 12 * * *` |
| 每天北京 06:00 | `0 22 * * *`（前一天 UTC 22:00） |
| 每小时 | `0 * * * *` |

---

## 🖥️ 如何手动在本地运行一次更新

```powershell
# 进入项目目录
cd C:\Users\Administrator\WorkBuddy\Claw

# 激活虚拟环境
.venv\Scripts\Activate.ps1

# 运行抓取脚本
python scripts/main.py
```

数据将更新到 `web/data/news_latest.json`，刷新浏览器即可看到最新内容。

---

## 🔧 如何修改资讯保留天数

编辑 `sources.yaml` 末尾的 `settings:` 部分：

```yaml
settings:
  retention_days: 7    # 改为你想要的天数，如 14
  summary_max_length: 200   # 摘要最大字符数
```

---

## RSS 源验证结果

| 来源 | RSS 状态 | 备注 |
|------|---------|------|
| Just Food | ✅ 可用 | 正常抓取 |
| Food Dive | ✅ 可用 | 正常抓取 |
| The Food Institute | ✅ 可用 | 正常抓取 |
| Food Safety News | ✅ 可用 | 正常抓取 |
| FoodNavigator | ⚠️ 待确认 | 官网 RSS 路径需确认 |
| FoodNavigator Asia | ⚠️ 待确认 | 官网 RSS 路径需确认 |
| Food Business News | ⚠️ 待确认 | RSS 路径需确认 |
| Beverage Daily | ⚠️ 待确认 | RSS 路径需确认 |
| 食品伙伴网 | ⚠️ 待确认 | Feed 结构异常，需人工确认 |
| 中国食品报网 | ⚠️ 待确认 | 需确认 |

> ℹ️ 标注 "待确认" 的来源，等你发来 Excel 网站列表后，我会帮你逐一找到正确的 RSS 地址并更新配置。

---

## 常见问题

**Q: Actions 运行失败怎么办？**
A: 进入 Actions 页面，点击失败的运行记录，查看日志。常见原因：
- 某个网站临时不可访问（自动跳过，不影响其他来源）
- 权限问题：确保仓库 Settings → Actions → General → Workflow permissions 设为 "Read and write"

**Q: 网站一直显示"加载资讯中"？**
A: 检查是否已运行过 Actions 并生成了 `web/data/news_latest.json`。

**Q: 如何绑定自己的域名？**
A: 在 GitHub Pages 设置中填写 Custom domain，并在域名 DNS 添加 CNAME 记录指向 `YOUR_USERNAME.github.io`。

---

*本项目使用 GitHub Pages 免费托管，数据来自各网站公开 RSS 源，仅供个人阅读使用。*
