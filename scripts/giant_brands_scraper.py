# -*- coding: utf-8 -*-
"""
giant_brands_scraper.py — 全球巨头官网资讯爬虫
每日北京时间 09:00 / 12:00 / 15:00 运行
策略：① 优先 RSS/Atom ② 回退 HTML 解析 ③ S/A/B 分级
输出：web/data/news_giant_brands.json
"""

import json, re, os, sys, time, logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedparser
import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateparser

from giant_brands_config import GIANT_BRANDS, S_LEVEL_KEYWORDS, A_LEVEL_KEYWORDS

# ── 常量 ───────────────────────────────────────────────────
OUTPUT_DIR  = Path(__file__).resolve().parent.parent / "web" / "data"
OUTPUT_FILE = OUTPUT_DIR / "news_giant_brands.json"
RETENTION_DAYS = 7
REQUEST_TIMEOUT = 30
DELAY_BETWEEN_REQUESTS = 1.5  # 秒，避免频繁请求

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,ja;q=0.8,zh-CN;q=0.7",
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# ── 时区 ───────────────────────────────────────────────────
CST = timezone(timedelta(hours=8))  # 北京时间


# ── 工具函数 ───────────────────────────────────────────────
def now_cst():
    return datetime.now(CST)


def parse_date_fuzzy(s):
    """尝试多种方式解析日期字符串"""
    if not s:
        return None
    s = s.strip()
    # 去掉常见前缀
    s = re.sub(r"^(Published|Posted|Date|发布时间)[：:]\s*", "", s, flags=re.I)
    try:
        return dateparser.parse(s)
    except (ValueError, TypeError, OverflowError):
        pass
    # 日语日期：2024年1月15日
    m = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日?", s)
    if m:
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass
    # 韩语日期
    m = re.search(r"(\d{4})\.(\d{2})\.(\d{2})", s)
    if m:
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass
    return None


def extract_date_from_url(url):
    """从 URL 路径中提取日期"""
    m = re.search(r"/(\d{4})/(\d{2})/(\d{2})/", url)
    if m:
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass
    m = re.search(r"/(\d{4})(\d{2})(\d{2})[^/]*$", url)
    if m:
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass
    return None


def normalize_url(href, base_url):
    """将相对 URL 转为绝对 URL"""
    if not href:
        return ""
    if href.startswith("http"):
        return href.split("?")[0]  # 去掉查询参数中的追踪码
    if href.startswith("/"):
        from urllib.parse import urlparse
        parsed = urlparse(base_url)
        return f"{parsed.scheme}://{parsed.netloc}{href}"
    return href


def classify_article(title, summary=""):
    """S/A/B 分级"""
    text = f"{title} {summary}".lower()
    # S 级匹配
    for kw, reason in S_LEVEL_KEYWORDS.items():
        if kw.lower() in text:
            return "S", reason
    # A 级匹配
    for kw in A_LEVEL_KEYWORDS:
        if kw.lower() in text:
            return "A", "常规新品/营销"
    # 默认 B 级
    return "B", "企业动态"


# ── RSS 发现与解析 ─────────────────────────────────────────
def discover_rss_urls(soup, base_url):
    """从 HTML <head> 和 <body> 中发现 RSS/Atom 链接"""
    feeds = []
    # <link rel="alternate" type="application/rss+xml" ...>
    for link in soup.find_all("link", rel=True):
        rel = " ".join(link.get("rel", []))
        href = link.get("href", "")
        if ("alternate" in rel or "feed" in rel) and href:
            t = link.get("type", "")
            if "rss" in t or "atom" in t or "xml" in t or "feed" in href.lower():
                feeds.append(normalize_url(href, base_url))
    # 页面中的 /feed /rss 链接
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        if any(x in href for x in ["/feed", "/rss", "/atom", "feed.xml", "rss.xml"]):
            feeds.append(normalize_url(a["href"], base_url))
    return list(set(feeds))


def parse_rss_feed(feed_url, brand_info):
    """解析 RSS/Atom feed"""
    articles = []
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:15]:
            title = entry.get("title", "").strip()
            if not title:
                continue
            url = entry.get("link", "")
            # 日期
            dt = None
            for field in ["published_parsed", "updated_parsed"]:
                tp = entry.get(field)
                if tp:
                    try:
                        dt = datetime(*tp[:6])
                    except:
                        pass
                    break
            if not dt:
                for field in ["published", "updated"]:
                    raw = entry.get(field, "")
                    if raw:
                        dt = parse_date_fuzzy(raw)
                        if dt:
                            break
            summary = ""
            if entry.get("summary"):
                soup = BeautifulSoup(entry.summary, "lxml")
                summary = soup.get_text(" ", strip=True)[:300]
            level, reason = classify_article(title, summary)
            articles.append({
                "brand": brand_info["brand"],
                "brand_cn": brand_info["brand_cn"],
                "region": brand_info["region"],
                "title": title,
                "url": normalize_url(url, feed_url),
                "published_at": dt.strftime("%Y-%m-%dT%H:%M:%S") if dt else "",
                "summary": summary[:200],
                "level": level,
                "level_reason": reason,
            })
    except Exception as e:
        log.warning(f"RSS 解析失败 [{feed_url}]: {e}")
    return articles


# ── HTML 通用解析 ─────────────────────────────────────────
def parse_html_page(url, brand_info):
    """通用 HTML 新闻列表解析"""
    articles = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        resp.raise_for_status()
        # 处理编码
        if not resp.encoding or resp.encoding.lower() == "iso-8859-1":
            resp.encoding = resp.apparent_encoding or "utf-8"
        soup = BeautifulSoup(resp.text, "lxml")
    except Exception as e:
        log.warning(f"页面获取失败 [{url}]: {e}")
        return articles

    # ── 尝试发现 RSS ──
    rss_feeds = discover_rss_urls(soup, url)
    if rss_feeds:
        log.info(f"发现 RSS [{brand_info['brand_cn']}]: {rss_feeds[0]}")
        for feed_url in rss_feeds[:2]:
            rss_articles = parse_rss_feed(feed_url, brand_info)
            if rss_articles:
                return rss_articles

    # ── HTML 解析：寻找新闻条目 ──
    # 策略1: <article> 标签
    # 策略2: 含 news/press/article 类名的容器
    # 策略3: 含日期的链接
    items = []

    # 找所有可能的新闻条目容器
    candidates = []
    for tag in soup.find_all(["article", "li", "div", "section"]):
        classes = " ".join(tag.get("class", []))
        if any(kw in classes.lower() for kw in [
            "news", "press", "article", "release", "story",
            "post", "item", "entry", "content-list", "card",
            "media", "pressreleases"
        ]):
            candidates.append(tag)

    # 如果没找到带类的，找 <article> 或 <li>
    if not candidates:
        candidates = soup.find_all("article") or soup.find_all("li")

    for tag in candidates[:30]:
        # 找标题链接
        links = tag.find_all("a", href=True)
        if not links:
            continue

        main_link = None
        for a in links:
            href = a.get("href", "")
            text = a.get_text(strip=True)
            # 跳过导航/面包屑链接
            if len(text) < 8:
                continue
            # 跳过明显不是文章的链接
            if any(skip in href.lower() for skip in ["mailto:", "tel:", "javascript:", "#", "login", "signup", "privacy", "cookie", "terms"]):
                continue
            main_link = a
            break

        if not main_link:
            continue

        title = main_link.get_text(strip=True)
        if len(title) < 8:
            continue

        href = normalize_url(main_link["href"], url)

        # 找日期
        dt = None
        # 方式1: <time> 标签
        time_tag = tag.find("time")
        if time_tag:
            dt_str = time_tag.get("datetime") or time_tag.get_text(strip=True)
            dt = parse_date_fuzzy(dt_str)
        # 方式2: 含 date/time 的 class
        if not dt:
            for el in tag.find_all(["span", "div", "p", "time"]):
                classes = " ".join(el.get("class", []))
                if any(kw in classes.lower() for kw in ["date", "time", "published", "meta"]):
                    dt = parse_date_fuzzy(el.get_text(strip=True))
                    if dt:
                        break
        # 方式3: 文本中的日期模式
        if not dt:
            text_content = tag.get_text(" ")
            # 匹配常见日期格式
            for pattern in [
                r"(\w+ \d{1,2}, \d{4})",           # January 15, 2024
                r"(\d{1,2} \w+ \d{4})",             # 15 January 2024
                r"(\d{4}-\d{2}-\d{2})",             # 2024-01-15
                r"(\d{4}\.\d{2}\.\d{2})",           # 2024.01.15
                r"(\d{4}年\d{1,2}月\d{1,2}日)",      # 2024年1月15日
                r"(\d{4}\.\s*\d{1,2}\.\s*\d{1,2})", # 2024. 1. 15
            ]:
                m = re.search(pattern, text_content)
                if m:
                    dt = parse_date_fuzzy(m.group(1))
                    if dt:
                        break
        # 方式4: 从 URL 提取日期
        if not dt:
            dt = extract_date_from_url(href)

        # 摘要
        summary = ""
        for p in tag.find_all("p"):
            txt = p.get_text(strip=True)
            if len(txt) > 20 and txt != title:
                summary = txt[:300]
                break

        level, reason = classify_article(title, summary)
        articles.append({
            "brand": brand_info["brand"],
            "brand_cn": brand_info["brand_cn"],
            "region": brand_info["region"],
            "title": title,
            "url": href,
            "published_at": dt.strftime("%Y-%m-%dT%H:%M:%S") if dt else "",
            "summary": summary[:200],
            "level": level,
            "level_reason": reason,
        })

    return articles


# ── 去重 ───────────────────────────────────────────────────
def deduplicate(articles):
    """按 URL 去重，保留最新的"""
    seen = {}
    for art in articles:
        url = art.get("url", "")
        if not url:
            continue
        if url not in seen:
            seen[url] = art
        else:
            # 保留日期更近的
            existing = seen[url]
            if art.get("published_at", "") > existing.get("published_at", ""):
                seen[url] = art
    return list(seen.values())


# ── 数据保留策略（7 天）──────────────────────────────
def prune_old_articles(articles, retention_days=RETENTION_DAYS):
    """只保留最近 N 天的资讯"""
    cutoff = now_cst() - timedelta(days=retention_days)
    kept = []
    for art in articles:
        dt_str = art.get("published_at", "")
        if not dt_str:
            kept.append(art)  # 无日期的保留
            continue
        try:
            dt = dateparser.parse(dt_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            if dt >= cutoff.replace(tzinfo=None):
                kept.append(art)
        except:
            kept.append(art)  # 日期解析失败的保留
    return kept


# ── 合并已有数据 ───────────────────────────────────────────
def load_existing():
    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return None


def merge_with_existing(new_articles, existing_data):
    """将新抓取的与已有数据合并去重"""
    if not existing_data or "articles" not in existing_data:
        return new_articles
    old_articles = existing_data.get("articles", [])
    combined = old_articles + new_articles
    return deduplicate(combined)


# ── 主流程 ─────────────────────────────────────────────────
def main():
    log.info("=" * 60)
    log.info("巨头官网资讯爬虫启动")
    log.info(f"共 {len(GIANT_BRANDS)} 个抓取源")
    log.info("=" * 60)

    all_articles = []
    success_count = 0
    fail_count = 0

    for i, brand_info in enumerate(GIANT_BRANDS):
        url = brand_info["url"]
        log.info(f"[{i+1}/{len(GIANT_BRANDS)}] {brand_info['brand_cn']}({brand_info['region']}) → {url}")

        try:
            articles = parse_html_page(url, brand_info)
            if articles:
                all_articles.extend(articles)
                success_count += 1
                log.info(f"  ✅ 获取 {len(articles)} 条")
            else:
                fail_count += 1
                log.warning(f"  ⚠️ 未获取到内容（可能需要 JS 渲染）")
        except Exception as e:
            fail_count += 1
            log.error(f"  ❌ 异常: {e}")

        time.sleep(DELAY_BETWEEN_REQUESTS)

    # 去重
    all_articles = deduplicate(all_articles)

    # 合并已有数据
    existing = load_existing()
    all_articles = merge_with_existing(all_articles, existing)

    # 保留最近 7 天
    all_articles = prune_old_articles(all_articles)

    # 按发布时间倒序排列（最新在前）
    all_articles.sort(key=lambda a: a.get("published_at", "") or "", reverse=True)

    # 提取品牌和地区列表
    brands = sorted(set(a["brand_cn"] for a in all_articles))
    regions = sorted(set(a["region"] for a in all_articles))

    # 统计
    s_count = sum(1 for a in all_articles if a.get("level") == "S")
    a_count = sum(1 for a in all_articles if a.get("level") == "A")
    b_count = sum(1 for a in all_articles if a.get("level") == "B")

    output = {
        "last_updated": now_cst().strftime("%Y-%m-%dT%H:%M:%S"),
        "retention_days": RETENTION_DAYS,
        "total": len(all_articles),
        "s_count": s_count,
        "a_count": a_count,
        "b_count": b_count,
        "brands": brands,
        "regions": regions,
        "articles": all_articles,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    log.info("=" * 60)
    log.info(f"爬取完成！成功 {success_count} / 失败 {fail_count} 个源")
    log.info(f"总条数: {len(all_articles)} | S级: {s_count} | A级: {a_count} | B级: {b_count}")
    log.info(f"输出: {OUTPUT_FILE}")
    log.info("=" * 60)


if __name__ == "__main__":
    main()
