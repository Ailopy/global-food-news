# 工作记忆 MEMORY.md

## 项目：全球食品资讯聚合网站

- **项目位置**：`C:\Users\Administrator\WorkBuddy\Claw`
- **创建时间**：2026-04-25
- **最后更新**：2026-05-17
- **项目状态**：本地开发完成（v2），待用户注册 GitHub 并部署
- **技术栈**：Python 3.13 + feedparser + 纯静态 HTML/CSS/JS + GitHub Actions + GitHub Pages
- **数据来源**：用户 Excel《新素材矩阵》，共 46 个网站，覆盖日本/北美/欧洲/全球
- **RSS 验证结果（2026-05-17）**：
  - ✅ 16个源可抓取：Mognavi、日本食粮新聞、食品産業新聞社、食品新聞（日本）、Food Dive、NOSH、BevNET、Food Safety News、The Food Institute（北美）、Just Food、Fab News、Sweets & Snacks World、Confectionery Production、Nutraceutical Business Review（欧洲）、The Spoon（欧美）、Italian Food Net（意大利）
  - ❌ 30个源暂无RSS：FoodNavigator三站（连接被阻）、Food Business News（404）、Prepared Foods/Dairy Foods/Snack Food/Beverage Industry（403）等
  - 近7天实际数据量：**249条**，14个活跃来源
- **前端新功能（v2）**：地区筛选（北美/欧洲/日本/亚太等）、品类筛选（综合/功能性食品/饮料等）、顶部统计面板（总数/来源数/地区数/今日更新）
- **用户待办**：
  1. 注册 GitHub 账号
  2. 推送代码到仓库 `food-news-aggregator`
  3. 开启 GitHub Pages（gh-pages 分支）
  4. 手动触发 Actions 完成首次数据抓取
- **用户偏好**：中文界面，多语言源（英/中/日/韩/法），绿色食品主题设计
