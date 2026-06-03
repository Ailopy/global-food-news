@echo off
chcp 65001 > nul
cd /d "C:\Users\Administrator\WorkBuddy\Claw"
"C:\Program Files\Git\cmd\git.exe" add web/app.js web/styles.css
"C:\Program Files\Git\cmd\git.exe" commit -m "feat: 视频栏目选题体系重构 v4 - 全球创新品鉴/新XIU/赛道新物种/商业新知"
"C:\Program Files\Git\cmd\git.exe" pull --rebase origin master
"C:\Program Files\Git\cmd\git.exe" push
echo.
echo ✅ 推送完成！稍等 1-2 分钟 GitHub Pages 自动部署
pause
