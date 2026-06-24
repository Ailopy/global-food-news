# -*- coding: utf-8 -*-
"""
s_topics_scraper.py — S级选题跟踪网站爬虫
每日北京时间 09:00 运行
策略：① 优先 RSS/Atom ② 回退 HTML 解析
过滤：只保留最近 30 天资讯
分析：10个品类自动打标 + S+特殊标注（全球首创/爆品等）
输出：web/data/news_s_topics.json
"""

import json, re, os, sys, time, logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedparser
import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateparser

from s_topics_config import S_TOPIC_SITES, S_PLUS_KEYWORDS, CATEGORY_KEYWORDS, PRODUCT_WATCH_LIST

# ── 常量 ────────────────────────────────────────────────────────
OUTPUT_DIR   = Path(__file__).resolve().parent.parent / "web" / "data"
OUTPUT_FILE  = OUTPUT_DIR / "news_s_topics.json"
RETENTION_DAYS   = 30   # 只保留30天
REQUEST_TIMEOUT  = 25
DELAY_BETWEEN    = 1.5  # 请求间隔秒

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,ja;q=0.8,zh-CN;q=0.7",
}

# YouTube RSS 需要更简洁的请求头（避免触发 YouTube 反爬）
YOUTUBE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "application/rss+xml,application/xml;q=0.9,text/xml;q=0.7",
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

CST = timezone(timedelta(hours=8))


# ── 工具函数 ────────────────────────────────────────────────────
def now_cst():
    return datetime.now(CST)


def parse_date_fuzzy(s):
    if not s:
        return None
    s = s.strip()
    s = re.sub(r"^(Published|Posted|Date|Updated|発行|発表)[：:]\s*", "", s, flags=re.I)
    try:
        return dateparser.parse(s)
    except (ValueError, TypeError, OverflowError):
        pass
    # 日语日期
    m = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日?", s)
    if m:
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)),
                            tzinfo=timezone.utc)
        except ValueError:
            pass
    return None


def is_within_days(dt, days=30):
    if not dt:
        return False
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return (now - dt).days <= days


def clean_text(s):
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()[:400]


# ── 品类分析 ────────────────────────────────────────────────────
def analyze_category(title, summary=""):
    """
    分析新闻属于哪个品类，返回 (category_name, icon, score)
    同时返回所有命中品类的列表（可能命中多个）
    """
    text = (title + " " + summary).lower()
    results = []
    for cat_name, cat_info in CATEGORY_KEYWORDS.items():
        score = 0
        hit_kws = []
        for kw in cat_info["keywords"]:
            if kw.lower() in text:
                score += 1
                hit_kws.append(kw)
        # 负向词减分
        if cat_info.get("negative"):
            for neg in cat_info["negative"]:
                if neg.lower() in text:
                    score -= 1
        if score > 0:
            results.append({
                "name": cat_name,
                "icon": cat_info["icon"],
                "color": cat_info["color"],
                "score": score,
            })
    # 按分数排序，取前3个
    results.sort(key=lambda x: x["score"], reverse=True)
    top_cats = results[:3] if results else [{"name": "其他", "icon": "📰", "color": "#6b7280", "score": 0}]
    return top_cats


# ── S+ 判断 ─────────────────────────────────────────────────────
def is_s_plus(title, summary=""):
    """判断是否为 S+ 级（全球首创/爆品/卖爆等），返回 (bool, reason)"""
    text = (title + " " + summary).lower()
    for kw in S_PLUS_KEYWORDS:
        if kw.lower() in text:
            return True, kw
    return False, ""


# ── 重点产品盯梢检测 ─────────────────────────────────────────────
def check_product_watch(title, summary=""):
    """
    检查是否命中重点产品盯梢清单。
    返回 (watched: bool, product_info: dict or None)
    """
    text = (title + " " + summary).lower()
    for pw in PRODUCT_WATCH_LIST:
        for kw in pw["keywords"]:
            if kw.lower() in text:
                return True, pw
    return False, None


# ── RSS 抓取 ────────────────────────────────────────────────────
def extract_real_url(url):
    """
    处理 Google News 中转链接。
    Google News RSS 的链接是中转链接，点击会跳转到真实文章，直接保留即可。
    """
    if not url:
        return url
    # 如有 ?url= 参数（某些 Google News 旧格式），直接提取
    if "news.google.com" in url and "?url=" in url:
        import urllib.parse
        parsed = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(parsed.query)
        if "url" in qs:
            return qs["url"][0]
    return url


def clean_google_news_title(title):
    """清理 Google News 标题后缀（如 '- 日本経済新聞'）"""
    if " - " in title:
        parts = title.rsplit(" - ", 1)
        if len(parts) == 2 and len(parts[1]) < 30:
            return parts[0].strip()
    return title


def try_rss(site):
    """尝试 RSS 抓取，成功则返回文章列表，失败返回 None"""
    for rss_url in site.get("rss_candidates", []):
        try:
            # YouTube RSS 使用专属请求头（减少反爬触发）
            req_headers = YOUTUBE_HEADERS if site.get("type") == "youtube" else HEADERS
            resp = requests.get(rss_url, headers=req_headers, timeout=REQUEST_TIMEOUT)
            if resp.status_code != 200:
                continue
            feed = feedparser.parse(resp.content)
            if not feed.entries:
                continue
            log.info(f"  [RSS OK] {site['name']} → {rss_url} ({len(feed.entries)} entries)")
            articles = []
            is_google_news = "news.google.com" in rss_url
            is_youtube = site.get("type") == "youtube"
            for entry in feed.entries:
                raw_title = clean_text(getattr(entry, "title", ""))
                title = clean_google_news_title(raw_title) if is_google_news else raw_title
                # 处理链接
                raw_url = getattr(entry, "link", "")
                url = extract_real_url(raw_url)
                # Google News RSS 的 source 字段包含真实来源名
                source_name = ""
                if hasattr(entry, "source") and hasattr(entry.source, "title"):
                    source_name = entry.source.title
                # YouTube 特殊处理：提取视频描述和缩略图
                summary = ""
                video_thumbnail = ""
                if is_youtube:
                    # YouTube RSS 使用 media:group 结构
                    media_group = getattr(entry, "media_group", None)
                    if media_group:
                        media_desc = getattr(media_group, "media_description", "")
                        if media_desc:
                            summary = clean_text(str(media_desc))
                        media_thumbnails = getattr(media_group, "media_thumbnail", [])
                        if media_thumbnails:
                            video_thumbnail = media_thumbnails[0].get("url", "")
                    # feedparser 也可能把 media:description 放在 entry 级别
                    if not summary:
                        media_desc = getattr(entry, "media_description", "")
                        if media_desc:
                            summary = clean_text(str(media_desc))
                    # 从 entry.summary 提取
                    if not summary:
                        entry_summary = getattr(entry, "summary", "")
                        if entry_summary:
                            summary = clean_text(entry_summary)
                    # 从 entry.content 提取
                    if not summary and hasattr(entry, "content"):
                        for content_item in entry.content:
                            val = content_item.get("value", "")
                            if val:
                                summary = clean_text(val)
                                break
                    # 缩略图：feedparser 的 media_thumbnail
                    if not video_thumbnail:
                        media_thumbnails = getattr(entry, "media_thumbnail", [])
                        if media_thumbnails:
                            video_thumbnail = media_thumbnails[0].get("url", "")
                    # YouTube 视频链接规范化
                    if "watch?v=" not in url and url:
                        # 某些YouTube RSS可能只返回 channel URL
                        video_id = ""
                        if hasattr(entry, "yt_videoid"):
                            video_id = entry.yt_videoid
                        elif "youtube.com/watch" in raw_url:
                            import re as _re
                            m = _re.search(r"v=([a-zA-Z0-9_-]+)", raw_url)
                            if m:
                                video_id = m.group(1)
                        if video_id:
                            url = f"https://www.youtube.com/watch?v={video_id}"
                else:
                    summary = clean_text(getattr(entry, "summary", ""))
                # 解析发布时间
                pub_dt = None
                if hasattr(entry, "published"):
                    pub_dt = parse_date_fuzzy(entry.published)
                if pub_dt is None and hasattr(entry, "updated'):
                    pub_dt = parse_date_fuzzy(entry.updated)
                # 过滤30天
                if not is_within_days(pub_dt, RETENTION_DAYS):
                    continue
                if not title or not url:
                    continue
                published_at = pub_dt.strftime("%Y-%m-%dT%H:%M:%SZ") if pub_dt else ""
                article = {
                    "title": title,
                    "url": url,
                    "summary": summary,
                    "published_at": published_at,
                    "source_name": source_name,
                }
                # YouTube 视频附加字段
                if is_youtube:
                    article["is_video"] = True
                    article["video_thumbnail"] = video_thumbnail
                    article["channel_name"] = site["name"]
                articles.append(article)
            return articles if articles else None
        except Exception as e:
            log.debug(f"  RSS fail {rss_url}: {e}")
    return None


# ── HTML 解析回退 ────────────────────────────────────────────────
def parse_html_generic(site):
    """通用 HTML 解析，提取链接+标题，按网站定制选择器"""
    url = site["url"]
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        # 按网站定制解析策略
        name = site["name"]
        articles = []

        if "nikkei" in url or "xtrend" in url:
            # 日経 xTrend：文章列表
            for item in soup.select("li.article-list__item, .m-articleList__item, article"):
                a_tag = item.find("a", href=True)
                title_el = item.find(["h2", "h3", "h4", ".title", ".headline"])
                if not a_tag:
                    continue
                title = clean_text(title_el.get_text() if title_el else a_tag.get_text())
                href = a_tag.get("href", "")
                if not href.startswith("http"):
                    href = "https://xtrend.nikkei.com" + href
                if title and href:
                    articles.append({"title": title, "url": href, "summary": "", "published_at": ""})

        elif "prtimes" in url:
            # PR Times
            for item in soup.select(".arc-item, .list-article-item, article.ArticleCard"):
                a_tag = item.find("a", href=True)
                title_el = item.find(["h2", "h3", ".title", ".arc-item-title"])
                if not a_tag:
                    continue
                title = clean_text(title_el.get_text() if title_el else a_tag.get_text())
                href = a_tag.get("href", "")
                if not href.startswith("http"):
                    href = "https://prtimes.jp" + href
                if title and href:
                    articles.append({"title": title, "url": href, "summary": "", "published_at": ""})

        elif "nissyoku" in url:
            # 日本食粮新闻
            for item in soup.select("article, .post, .entry-item, li.news-item"):
                a_tag = item.find("a", href=True)
                title_el = item.find(["h2", "h3", "h4"])
                if not a_tag:
                    continue
                title = clean_text(title_el.get_text() if title_el else a_tag.get_text())
                href = a_tag.get("href", "")
                if not href.startswith("http"):
                    href = "https://news.nissyoku.co.jp" + href
                if title and href:
                    articles.append({"title": title, "url": href, "summary": "", "published_at": ""})

        elif "trendhunter" in url:
            # Trend Hunter
            for item in soup.select(".item, .trend-card, article.trend"):
                a_tag = item.find("a", href=True)
                title_el = item.find(["h2", "h3", ".title"])
                img = item.find("img")
                if not a_tag:
                    continue
                title = clean_text(title_el.get_text() if title_el else a_tag.get_text())
                href = a_tag.get("href", "")
                if not href.startswith("http"):
                    href = "https://www.trendhunter.com" + href
                summary = img.get("alt", "") if img else ""
                if title and href and len(title) > 5:
                    articles.append({"title": title, "url": href, "summary": clean_text(summary), "published_at": ""})

        elif "fooddive" in url:
            # Food Dive
            for item in soup.select("article, .feed__item, .article-item"):
                a_tag = item.find("a", href=True)
                title_el = item.find(["h2", "h3", "h4"])
                summary_el = item.find(["p", ".article-deck", ".deck"])
                if not a_tag:
                    continue
                title = clean_text(title_el.get_text() if title_el else a_tag.get_text())
                href = a_tag.get("href", "")
                if not href.startswith("http"):
                    href = "https://www.fooddive.com" + href
                summary = clean_text(summary_el.get_text() if summary_el else "")
                if title and href and len(title) > 5:
                    articles.append({"title": title, "url": href, "summary": summary, "published_at": ""})

        elif "packagingdigest" in url:
            # Packaging Digest
            for item in soup.select("article, .view-content .views-row, .node-teaser"):
                a_tag = item.find("a", href=True)
                title_el = item.find(["h2", "h3", "h4"])
                summary_el = item.find(["p", ".field-summary"])
                if not a_tag:
                    continue
                title = clean_text(title_el.get_text() if title_el else a_tag.get_text())
                href = a_tag.get("href", "")
                if not href.startswith("http"):
                    href = "https://www.packagingdigest.com" + href
                summary = clean_text(summary_el.get_text() if summary_el else "")
                if title and href and len(title) > 5:
                    articles.append({"title": title, "url": href, "summary": summary, "published_at": ""})

        else:
            # 通用回退：提取所有 <article> 或有标题的链接
            for item in soup.select("article, .post, .news-item"):
                a_tag = item.find("a", href=True)
                title_el = item.find(["h2", "h3"])
                if not a_tag:
                    continue
                title = clean_text(title_el.get_text() if title_el else a_tag.get_text())
                href = a_tag.get("href", "")
                if title and href and len(title) > 5:
                    articles.append({"title": title, "url": href, "summary": "", "published_at": ""})

        log.info(f"  [HTML OK] {site['name']} → {url} ({len(articles)} items)")
        return articles[:50] if articles else None

    except Exception as e:
        log.warning(f"  [HTML FAIL] {site['name']}: {e}")
        return None


# ── 主爬取逻辑 ──────────────────────────────────────────────────
def scrape_site(site):
    """抓取单个网站，返回处理后的文章列表"""
    log.info(f"[START] {site['name']} ({site['region']}) ...")

    # ① 优先 RSS
    raw_articles = try_rss(site)

    # ② 回退 HTML
    if not raw_articles:
        raw_articles = parse_html_generic(site)

    if not raw_articles:
        log.warning(f"  [SKIP] {site['name']}: 没有获取到数据")
        return []

    # ③ 品类分析 + S+ 判断 + 产品盯梢检测
    result = []
    for art in raw_articles:
        title   = art.get("title", "")
        summary = art.get("summary", "")

        # 品类分析
        categories = analyze_category(title, summary)

        # S+ 判断
        is_sp, sp_reason = is_s_plus(title, summary)

        # 重点产品盯梢检测
        watched, product_info = check_product_watch(title, summary)

        entry = {
            "site_name": site["name"],
            "site_name_en": site["name_en"],
            "region": site["region"],
            "positioning": site["positioning"],
            "title": title,
            "url": art.get("url", ""),
            "summary": summary,
            "published_at": art.get("published_at", ""),
            "is_s_plus": is_sp,
            "s_plus_reason": sp_reason,
            "categories": categories,          # [{"name","icon","color","score"}]
            "primary_category": categories[0]["name"],  # 主品类
            "scraped_at": now_cst().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        }

        # 产品盯梢标记
        if watched:
            entry["watched_product"] = True
            entry["watched_product_name"] = product_info["product_name"]
            entry["watched_priority"] = product_info["priority"]
            log.info(f"  🔔 产品盯梢命中: {title} → {product_info['product_name']}")

        # YouTube 视频附加字段
        if art.get("is_video"):
            entry["is_video"] = True
            entry["video_thumbnail"] = art.get("video_thumbnail", "")
            entry["channel_name"] = art.get("channel_name", site["name"])

        result.append(entry)

    return result


# ── 加载旧数据（去重/保留30天）─────────────────────────────────
def load_existing():
    if not OUTPUT_FILE.exists():
        return []
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        arts = data.get("articles", [])
        # 过滤掉超过30天的旧数据
        cutoff = datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)
        kept = []
        for a in arts:
            pub = a.get("published_at", "")
            if pub:
                try:
                    dt = datetime.fromisoformat(pub.replace("Z", "+00:00"))
                    if dt >= cutoff:
                        kept.append(a)
                        continue
                except Exception:
                    pass
            # published_at 为空的（HTML抓取没时间戳），按抓取时间判断
            scraped = a.get("scraped_at", "")
            if scraped:
                try:
                    dt = datetime.fromisoformat(scraped)
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    if (datetime.now(timezone.utc) - dt).days <= RETENTION_DAYS:
                        kept.append(a)
                except Exception:
                    pass
        return kept
    except Exception:
        return []


# ── 主入口 ──────────────────────────────────────────────────────
def main():
    log.info(f"=== S级选题网站爬虫启动 ({now_cst().strftime('%Y-%m-%d %H:%M')} CST) ===")
    log.info(f"共 {len(S_TOPIC_SITES)} 个网站待抓取")

    all_new = []
    for i, site in enumerate(S_TOPIC_SITES):
        arts = scrape_site(site)
        all_new.extend(arts)
        if i < len(S_TOPIC_SITES) - 1:
            time.sleep(DELAY_BETWEEN)

    log.info(f"本次新抓取：{len(all_new)} 条")

    # 合并旧数据（去重）
    existing = load_existing()
    existing_urls = {a["url"] for a in existing if a.get("url")}
    merged = list(existing)
    added = 0
    for art in all_new:
        if art["url"] and art["url"] not in existing_urls:
            merged.append(art)
            existing_urls.add(art["url"])
            added += 1

    log.info(f"新增：{added} 条 | 保留旧数据：{len(existing)} 条 | 合计：{len(merged)} 条")

    # 按发布时间排序（有时间戳的优先，无时间戳放后面）
    def sort_key(a):
        pub = a.get("published_at", "")
        if pub:
            try:
                return datetime.fromisoformat(pub.replace("Z", "+00:00")).timestamp()
            except Exception:
                pass
        return 0
    merged.sort(key=sort_key, reverse=True)

    # 统计
    s_plus_count = sum(1 for a in merged if a.get("is_s_plus"))
    watched_count = sum(1 for a in merged if a.get("watched_product"))
    sites_active = list({a["site_name"] for a in merged})
    regions_active = list({a["region"] for a in merged})
    cat_stats = {}
    for a in merged:
        cat = a.get("primary_category", "其他")
        cat_stats[cat] = cat_stats.get(cat, 0) + 1

    output = {
        "total": len(merged),
        "s_plus_count": s_plus_count,
        "watched_product_count": watched_count,
        "sites": sites_active,
        "regions": regions_active,
        "category_stats": cat_stats,
        "last_updated": now_cst().strftime("%Y-%m-%d %H:%M"),
        "last_updated_iso": now_cst().isoformat(),
        "articles": merged,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    log.info(f"✅ 写入 {OUTPUT_FILE}")
    log.info(f"   S+级: {s_plus_count} | 产品盯梢: {watched_count} | 活跃站点: {len(sites_active)} | 地区: {len(regions_active)}")
    log.info(f"   品类分布: {cat_stats}")


if __name__ == "__main__":
    main()
