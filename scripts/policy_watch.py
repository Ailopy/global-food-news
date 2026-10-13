# -*- coding: utf-8 -*-
"""
policy_watch.py — 政策更新提醒
对比线上 news_policy.json 与本地快照，输出新增政策条目。
用于"有新闻及时更新提醒"：定时运行 → 有新增则列出。
"""

import json, sys, os, logging
from pathlib import Path
from datetime import datetime, timedelta, timezone

import requests

ROOT_DIR    = Path(__file__).resolve().parent.parent
LOCAL_FILE  = ROOT_DIR / "web" / "data" / "news_policy.json"
STATE_FILE  = ROOT_DIR / ".workbuddy" / "policy_seen.json"
ONLINE_URL  = "https://ailopy.github.io/global-food-news/data/news_policy.json"
TIMEOUT     = 25
CST = timezone(timedelta(hours=8))

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("policy-watch")


def load_json(p):
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def fetch_online():
    try:
        r = requests.get(f"{ONLINE_URL}?t={int(datetime.now().timestamp())}",
                         timeout=TIMEOUT, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        return r.json()
    except Exception as e:
        log.warning(f"线上数据获取失败: {e}")
        return None


def main():
    # --sync：先抓取最新政策写入本地（供自动化"抓取+提醒"一体化调用）
    if "--sync" in sys.argv:
        import subprocess
        scraper = Path(__file__).resolve().parent / "policy_scraper.py"
        if scraper.exists():
            print("⏳ 正在抓取最新政策…")
            subprocess.run([sys.executable, str(scraper)], cwd=str(scraper.parent))

    articles = None
    src = ""
    online = fetch_online()
    if online:
        articles, src = online, "线上"
    else:
        local = load_json(LOCAL_FILE)
        if local:
            articles, src = local, "本地"

    if not articles:
        print("⚠️ 无法获取政策数据（线上与本地均不可用）")
        return

    seen = load_json(STATE_FILE) or {"urls": []}
    seen_urls = set(seen.get("urls", []))

    new_items = [a for a in articles if a.get("url") and a["url"] not in seen_urls]

    print(f"📋 数据源：{src} | 当前 {len(articles)} 条 | 新增 {len(new_items)} 条")
    print(f"🕐 检查时间：{datetime.now(CST).strftime('%Y-%m-%d %H:%M')}")
    print("-" * 60)

    if not new_items:
        print("✅ 暂无新增食品政策")
        return

    order = {"S+": 0, "S": 1, "A": 2, "B": 3}
    new_items.sort(key=lambda a: (order.get(a.get("level"), 9), a.get("publish_time", "")), reverse=False)

    for a in new_items:
        print(f"[{a.get('level','?')}] {a.get('publish_time','')} | {a.get('source','')}")
        print(f"  {a.get('title','')}")
        print(f"  {a.get('url','')}")
        print()

    # 更新已见快照
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    all_urls = list({a["url"] for a in articles if a.get("url")})
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"urls": all_urls, "updated": datetime.now(CST).isoformat()}, f, ensure_ascii=False, indent=2)
    print(f"（已记录 {len(all_urls)} 条至快照）")


if __name__ == "__main__":
    main()
