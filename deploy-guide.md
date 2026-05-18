# 📤 部署指南 — 全球食品资讯聚合站

> 本文档指导你将 `C:\Users\Administrator\WorkBuddy\Claw` 项目完整部署到 GitHub Pages。
> **目标网站：** `https://Ailopy.github.io/global-food-news/`

---

## 准备工作

### ✅ 确认已完成
- [x] 代码已就绪（Python 抓取脚本、前端页面、GitHub Actions 均完整）
- [x] GitHub 账号已注册并登录
- [ ] Git for Windows 已安装（**下一步**）
- [ ] GitHub 仓库已创建
- [ ] 代码已推送到 GitHub
- [ ] GitHub Pages 已开启

---

## Step 1：安装 Git for Windows

Git 是连接本地电脑和 GitHub 仓库的桥梁，必须先安装。

### 下载

打开浏览器访问：

```
https://git-scm.com/download/win
```

页面会自动检测你的系统（64位 Windows），直接点击 **64-bit Git for Windows Setup** 下载（约 58MB）。

### 安装（全部选默认即可）

运行下载的 `.exe` 安装程序，**每一步都点「Next」**，保持默认选项不变，直到「Install」。

> 💡 如果安装向导询问是否添加到 PATH，选择 **「Use Git from the Windows Command Prompt」**（推荐）。

### 验证安装成功

安装完成后，**重新打开一个新的 PowerShell 窗口**（重要！），运行：

```powershell
git --version
```

看到类似以下输出即为成功：

```
git version 2.49.0.windows.1
```

---

## Step 2：在 GitHub 创建仓库

### 登录 GitHub

访问 **https://github.com** 并确认已登录（右上角显示你的头像）。

### 创建新仓库

1. 点击右上角 **+** 图标 → **New repository**
2. 填写如下：

| 字段 | 值 |
|------|-----|
| **Owner** | `Ailopy`（你的用户名） |
| **Repository name** | `global-food-news` |
| **Description** | `全球食品饮料行业资讯聚合，每日自动更新` |
| **Visibility** | ✅ **Public**（必须选公开，GitHub Pages 免费版仅支持公开仓库） |
| **Add a README file** | ⬜ **不要勾选**（本地已有文件） |
| **Add .gitignore** | 不需要选择 |
| **Choose a license** | 不需要选择 |

3. 点击 **Create repository**

### 重要：记录仓库地址

创建成功后，你会看到一个空仓库页面。**找到绿色按钮 `<> Code`** 下方的仓库 URL，类似：

```
https://github.com/Ailopy/global-food-news
```

这个地址后面推送代码时会用到。

---

## Step 3：推送代码到 GitHub

回到本地电脑，在 PowerShell 中按顺序运行以下命令。

### 3.1 进入项目目录

```powershell
cd C:\Users\Administrator\WorkBuddy\Claw
```

### 3.2 初始化 Git 并配置用户信息

```powershell
git init
git config --global user.name "Ailopy"
git config --global user.email "你的注册邮箱@example.com"
```

> ⚠️ 将 `你的注册邮箱@example.com` 替换为你注册 GitHub 时使用的邮箱地址。

### 3.3 添加远程仓库

```powershell
git remote add origin https://github.com/Ailopy/global-food-news.git
```

### 3.4 添加所有文件并提交

```powershell
git add .
git commit -m "feat: 初始化全球食品资讯聚合站 v1.0"
```

### 3.5 推送到 GitHub

```powershell
git branch -M main
git push -u origin main
```

**第一次推送时**会弹出 GitHub 登录窗口（浏览器弹窗），按提示授权即可。

成功后会看到类似输出：

```
Enumerating objects: 20, done.
Counting objects: 100% (20/20), done.
Delta compression using up to 8 threads
To https://github.com/Ailopy/global-food-news.git
   1a2b3c4..d5e6f7  main -> main
```

> 💡 如果提示权限问题，用浏览器打开 https://github.com/Ailopy/global-food-news 确认仓库已创建成功，然后重试推送。

---

## Step 4：开启 GitHub Pages

### 4.1 进入仓库设置

在 GitHub 仓库页面，点击顶部 **Settings**（设置）标签。

### 4.2 找到 Pages 配置

左侧菜单找到 **Pages**（在 Pages 下面有一行灰色字"GitHub Pages">

### 4.3 配置 Source

1. **Source** 选择：**Deploy from a branch**
2. **Branch** 选择：`gh-pages` 分支，目录选 `/ (root)`
3. 点击 **Save**（保存按钮）

> 💡 第一次配置 Pages 时，`gh-pages` 分支可能还不存在——没关系，等 Actions 首次运行后会自动创建。

### 4.4 等待部署

保存后，页面顶部会出现一条紫色提示：

```
Your site is live at https://Ailopy.github.io/global-food-news/
```

> ⚠️ 第一次配置后可能需要等 **1-3 分钟**才会显示可用链接，因为 GitHub 需要初始化环境。

---

## Step 5：手动触发首次数据抓取

### 5.1 进入 Actions 页面

在仓库页面，点击顶部 **Actions** 标签。

### 5.2 运行工作流

左侧找到 **「每日资讯更新」** 工作流（橙色图标）。

点击右侧 **Run workflow** → **Run workflow**（绿色按钮）。

### 5.3 等待完成

- 运行时间：约 2-5 分钟
- 成功标志：左侧出现绿色勾号 ✅
- 如果出现红色 ❌，点击进入查看日志，常见原因：
  - 某个 RSS 源临时不可访问（会自动跳过，不影响其他来源）
  - 网络问题（重试即可）

---

## Step 6：访问你的网站

所有步骤完成后，访问：

```
https://Ailopy.github.io/global-food-news/
```

🎉 **恭喜！你的全球食品资讯站已上线！**

---

## 日常维护

### 自动更新
网站每天会自动更新两次：
- 北京时间 **08:00**（UTC 00:00）
- 北京时间 **20:00**（UTC 12:00）

无需任何操作，GitHub Actions 会自动运行。

### 手动更新数据
如果想立即刷新数据，进入仓库 → **Actions** → **每日资讯更新** → **Run workflow** 即可。

### 修改资讯来源
编辑项目中的 `sources.yaml` 文件，添加或修改 RSS 源，然后：

```powershell
git add sources.yaml
git commit -m "feat: 更新资讯来源"
git push
```

GitHub Actions 会自动检测到更新并重新抓取数据。

---

## 故障排除

| 问题 | 解决方法 |
|------|---------|
| `git --version` 提示找不到 | Git 未安装成功，重新安装并重启 PowerShell |
| 推送时被拒绝（403） | GitHub 授权过期，在 PowerShell 运行 `git push` 后重新授权 |
| Pages 页面没有 Source 选项 | 确认仓库是 **Public**（公开），Private 仓库需要付费套餐 |
| Actions 运行失败 | 点击红色失败的运行记录，展开日志查看具体原因 |
| 网站显示"加载中" | 等 Actions 首次运行完成后再访问 |

---

## 快速参考

| 项目 | 值 |
|------|-----|
| 仓库地址 | `https://github.com/Ailopy/global-food-news` |
| 网站地址 | `https://Ailopy.github.io/global-food-news/` |
| 本地项目目录 | `C:\Users\Administrator\WorkBuddy\Claw` |
| 仓库名 | `global-food-news` |
