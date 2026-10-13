# -*- coding: utf-8 -*-
"""
policy_scraper.py — 食品政策监控爬虫
数据源：食品伙伴网（食品行业权威政策/标准聚合站）
策略：抓列表页 → 近7天过滤 → 详情页取摘要/来源 → S+/S/A/B 分级
输出：web/data/news_policy.json（纯数组，前端直接消费）
运行：每日北京时间 09:00（GitHub Actions）
"""

import json, re, sys, time, logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from policy_config import (
    POLICY_SOURCES, RETENTION_DAYS, MAX_ITEMS,
    ABSTRACT_MAX, doc_level, should_keep,
)

# ── 常量 ───────────────────────────────────────────────────
ROOT_DIR    = Path(__file__).resolve().parent.parent
OUTPUT_FILE = ROOT_DIR / "web" / "data" / "news_policy.json"
REQUEST_TIMEOUT = 25
DELAY = 1.2  # 秒，礼貌抓取
CANDIDATE_CAP = 60  # 每源最多抓取候选数（列表按时间倒序）

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

CST = timezone(timedelta(hours=8))
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("policy")

# 列表页文章链接模式
ARTICLE_HREF_RE = re.compile(r"(?:draft/)?show-\d+\.html|info/sort/\d+/\d+\.html")
DATE_RE = re.compile(r"(20\d{2})[-/.](\d{1,2})[-/.](\d{1,2})")


def now_cst():
    return datetime.now(CST)


def fetch(url):
    resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
    resp.raise_for_status()
    if not resp.encoding or resp.encoding.lower() == "iso-8859-1":
        resp.encoding = resp.apparent_encoding or "utf-8"
    return resp.text


def parse_date(text):
    m = DATE_RE.search(text or "")
    if not m:
        return None
    try:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


# ── 列表页解析 ─────────────────────────────────────────────
def parse_list_page(url):
    """返回 [{'url','title','date':datetime}]"""
    items = []
    try:
        html = fetch(url)
    except Exception as e:
        log.warning(f"列表页获取失败 [{url}]: {e}")
        return items

    soup = BeautifulSoup(html, "lxml")
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not ARTICLE_HREF_RE.search(href):
            continue
        full = urljoin(url, href)
        if full in seen:
            continue
        title = (a.get("title") or a.get_text(" ", strip=True) or "").strip()
        if len(title) < 8:
            continue
        seen.add(full)

        # 日期：优先看所在容器文本
        container = a.find_parent(["li", "div", "td", "tr", "p"]) or a.parent
        ctext = container.get_text(" ", strip=True) if container else ""
        dt = parse_date(ctext[:120]) or parse_date(a.get_text(" ", strip=True))
        items.append({"url": full, "title": title, "date": dt})
    log.info(f"  列表 [{url}] 解析到 {len(items)} 条")
    return items


# ── 详情页解析 ─────────────────────────────────────────────
def parse_detail(url, fallback_title="", fallback_date=None):
    """抓详情页，返回 (title, abstract, source, date)
    权威来源：详情页 <div class="info">（发布时间 + 来源），列表日期仅兜底。"""
    title, abstract, source = fallback_title, "", ""
    ddate = fallback_date
    try:
        html = fetch(url)
        soup = BeautifulSoup(html, "lxml")
        h1 = soup.find(["h1"])
        if h1 and h1.get_text(strip=True):
            title = h1.get_text(" ", strip=True)
        # 摘要：meta description
        for m in soup.find_all("meta"):
            key = (m.get("name") or m.get("property") or "").lower()
            if key in ("description", "og:description") and not abstract:
                abstract = (m.get("content") or "").strip()
        # 发布时间 + 来源：优先解析 <div class="info">
        info = soup.find("div", class_="info")
        if info:
            it = info.get_text(" ", strip=True)
            dm = re.match(r"\s*(20\d{2}[-/.]\d{1,2}[-/.]\d{1,2})", it)
            if dm:
                ddate = parse_date(dm.group(1))
            sm = re.search(r"来源[：:]\s*(.+?)(?:\s*浏览次数|\s*编辑|\s*$)", it)
            if sm:
                source = sm.group(1).strip()
        text = soup.get_text(" ", strip=True)
        # 兜底：正文中的“发布日期/发布时间”
        if not ddate:
            dm = re.search(r"(?:发布日期|发布时间|公布日期|发文日期)[：:]\s*(20\d{2}[-/年.]\d{1,2}[-/月.]\d{1,2})", text)
            if dm:
                ddate = parse_date(dm.group(1))
        if not source:
            sm = re.search(r"来源[：:]\s*(.+?)(?:\s*浏览次数|\s*编辑|\s*$)", text)
            if sm:
                source = sm.group(1).strip()
        # 清洗来源中的页面回显文案
        source = re.sub(r"\s*(复制网址|复制|浏览次数.*|编辑.*|下载.*)$", "", source).strip()
        source = source.strip("、,，")
    except Exception as e:
        log.warning(f"  详情页失败 [{url}]: {e}")
    return title, abstract, source, ddate


# ── 已有数据 ───────────────────────────────────────────────
def load_existing():
    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else data.get("articles", [])
        except Exception:
            pass
    return []


# ── 主流程 ─────────────────────────────────────────────────
def main(dry=False):
    log.info("=" * 60)
    log.info("食品政策监控爬虫启动")

    cutoff = now_cst().replace(tzinfo=None) - timedelta(days=RETENTION_DAYS)
    collected = {}  # url -> item

    for src in POLICY_SOURCES:
        log.info(f"抓取源：{src['name']} → {src['url']}")
        cnt = 0
        for it in parse_list_page(src["url"]):
            if not should_keep(it["title"]):
                continue
            if it["url"] in collected:
                continue
            collected[it["url"]] = it
            cnt += 1
            if cnt >= CANDIDATE_CAP:   # 列表按时间倒序，取前 N 条足够覆盖近7天
                break
        time.sleep(DELAY)

    log.info(f"候选政策：{len(collected)} 条，开始抓详情…")

    articles = []
    for it in collected.values():
        title, abstract, source, ddate = parse_detail(it["url"], it["title"], it["date"])
        if not should_keep(title):
            continue
        pub = ddate or it.get("date") or now_cst()   # 详情页日期优先
        if pub < cutoff:                               # 用可靠日期过滤近7天
            continue
        level, reason = doc_level(title, abstract)
        articles.append({
            "title": f"【{level}级】{title}",
            "source": source or "食品伙伴网",
            "publish_time": pub.strftime("%Y-%m-%d"),
            "url": it["url"],
            "abstract": abstract[:ABSTRACT_MAX],
            "level": level,
            "reason": reason,
        })
        time.sleep(DELAY)

    # 合并已有（按 url 去重，保留新版本）
    existing = [a for a in load_existing() if a.get("url")]
    for old in existing:
        if old["url"] not in collected:
            articles.append(old)

    # 统一重过滤：剔除不符食品语境/已过期的条目（含旧数据）
    cleaned = []
    for a in articles:
        clean_title = re.sub(r"^【[^】]*】\s*", "", a.get("title", ""))
        if not should_keep(clean_title):
            continue
        d = parse_date(a.get("publish_time", ""))
        if d and d < cutoff:
            continue
        cleaned.append(a)
    articles = cleaned

    # 去重（url）
    uniq = {}
    for a in articles:
        uniq[a["url"]] = a
    articles = list(uniq.values())

    # 仅保留近 N 天
    def in_window(a):
        d = parse_date(a.get("publish_time", ""))
        return (d is None) or (d >= cutoff)
    articles = [a for a in articles if in_window(a)]

    # 排序：级别优先，其次时间倒序
    order = {"S+": 0, "S": 1, "A": 2, "B": 3}
    articles.sort(key=lambda a: (order.get(a.get("level"), 9), _neg_time(a.get("publish_time", ""))))
    articles = articles[:MAX_ITEMS]

    counts = {lv: sum(1 for a in articles if a["level"] == lv) for lv in ["S+", "S", "A", "B"]}
    log.info(f"最终：{len(articles)} 条 | S+ {counts['S+']} / S {counts['S']} / A {counts['A']} / B {counts['B']}")

    if dry:
        print(json.dumps(articles, ensure_ascii=False, indent=2)[:4000])
        return

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    log.info(f"已写入：{OUTPUT_FILE}")
    log.info("=" * 60)


def _neg_time(s):
    """把日期字符串转成可比较的负数时间戳（越新越靠前）"""
    d = parse_date(s or "")
    return -(d.timestamp() if d else 0)


if __name__ == "__main__":
    main(dry="--dry" in sys.argv)
