#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日跟踪 — 抓取脚本
─────────────────────────────────────────────
流程：抓取7个源(近1月) → 提取标题/链接/日期/摘要 → 标题译中文
      → 10类分析 → S级判定 → 按时间倒序输出 news_daily_track.json
用法：
  python daily_track_scraper.py            # 正式写入
  python daily_track_scraper.py --dry      # 只打印不写文件
"""
import argparse
import json
import logging
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from urllib.parse import urljoin

import feedparser
import requests
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from daily_track_config import (  # noqa: E402
    SOURCES, MARKETS, RETENTION_DAYS, MAX_PER_SOURCE, ABSTRACT_MAX,
    classify, is_s_level, s_reason, is_excluded,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%H:%M:%S")
log = logging.getLogger("daily_track")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "web", "data", "news_daily_track.json")
CACHE = os.path.join(ROOT, ".workbuddy", "daily_track_tr_cache.json")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
HEADERS = {"User-Agent": UA, "Accept-Language": "ja,en;q=0.9,ko;q=0.8,zh;q=0.7"}
REQUEST_TIMEOUT = 30
DELAY = 0.8
CST = timezone(timedelta(hours=8))

DATE_PATS = [
    r"(20\d{2})[-/.](\d{1,2})[-/.](\d{1,2})",
    r"(20\d{2})年(\d{1,2})月(\d{1,2})日",
]


def now_cst():
    return datetime.now(CST)


def parse_date_any(text):
    if not text:
        return None
    for pat in DATE_PATS:
        m = re.search(pat, text)
        if m:
            try:
                y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
                if 1 <= mo <= 12 and 1 <= d <= 31:
                    return datetime(y, mo, d)
            except ValueError:
                continue
    return None


def clean_title(t):
    """清洗标题杂质：前导序号、日期串、相对时间、多余空白"""
    if not t:
        return ""
    t = re.sub(r"^\s*\d{1,3}\s+", "", t)                       # 前导序号
    t = re.sub(r"\d{4}[-/年]\d{1,2}[-/月]\d{1,2}日?(\s*\d{1,2}:\d{2})?", "", t)
    t = re.sub(r"\d{1,2}:\d{2}(:\d{2})?", "", t)
    t = re.sub(r"\d+\s*(?:分|時間|小時|小时|日|週間|周|ヶ月|个月|か月)前", "", t)
    t = re.sub(r"\s+\d{1,2}-[A-Za-z]{3,}-\d{4}.*$", "", t)   # 尾部 "12-Oct-2026 By 作者"
    t = re.sub(r"\s+\d{1,2}\s+[A-Z][a-z]{2}\s+\d{4}\s+By\s+.*$", "", t)
    t = re.sub(r"\s+\[[^\]]{0,140}\]\s*$", "", t)             # 尾部 "[来源 = 记者]"
    t = re.sub(r"\s+", " ", t).strip(" 　·・|,-—–")
    return t.strip()


# ── 网络抓取 ────────────────────────────────────────────────
def fetch(url, mode="default"):
    """按模式抓取页面，返回 HTML 文本或 None"""
    try:
        if mode == "cffi_safari":
            from curl_cffi import requests as cr
            for imp in ("safari17_2_1", "safari17_0", "safari15_5", "safari15_3"):
                try:
                    r = cr.get(url, impersonate=imp, timeout=REQUEST_TIMEOUT)
                    if r.status_code == 200 and "just a moment" not in (r.text or "").lower():
                        return r.text
                except Exception:
                    continue
            log.warning(f"  [cffi] 失败: {url}")
            return None
        if mode == "playwright":
            return fetch_playwright(url)
        r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        if r.status_code == 200:
            r.encoding = r.apparent_encoding or r.encoding
            return r.text
        log.warning(f"  [http {r.status_code}] {url}")
        return None
    except Exception as e:
        log.warning(f"  [fetch err] {url}: {type(e).__name__} {e}")
        return None


def fetch_playwright(url):
    """无头浏览器抓取（用于绕过 Cloudflare JS 挑战的站点）"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        log.warning("  [playwright] 未安装，跳过")
        return None
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True,
                                  args=["--disable-blink-features=AutomationControlled",
                                        "--no-sandbox"])
            ctx = b.new_context(user_agent=UA, locale="en-US",
                                viewport={"width": 1366, "height": 900})
            page = ctx.new_page()
            page.goto(url, timeout=60000, wait_until="domcontentloaded")
            for _ in range(12):
                page.wait_for_timeout(2500)
                if "just a moment" not in page.title().lower():
                    break
            html = page.content()
            b.close()
            return html
    except Exception as e:
        log.warning(f"  [playwright err] {url}: {type(e).__name__} {e}")
        return None


# ── 解析：RSS ───────────────────────────────────────────────
def fetch_rss(src):
    items = []
    raw = fetch(src["url"])
    if not raw:
        return items
    feed = feedparser.parse(raw)
    for e in feed.entries[:MAX_PER_SOURCE]:
        title = clean_title((e.get("title") or "").strip())
        link = (e.get("link") or "").strip()
        if not title or not link:
            continue
        dt = None
        for k in ("published_parsed", "updated_parsed"):
            if e.get(k):
                try:
                    dt = datetime(*e[k][:6])
                    break
                except Exception:
                    pass
        summary = BeautifulSoup(e.get("summary", "") or "", "lxml").get_text(" ", strip=True)
        items.append({"title": title, "url": link, "date": dt, "abstract": summary})
    return items


# ── 解析：HTML 列表 ─────────────────────────────────────────
def _in_container(a, cls_re, depth=6):
    """判断锚点是否位于指定 class 的容器内（用于限定主列表，排除推荐位）"""
    p = a
    for _ in range(depth):
        p = p.parent
        if p is None:
            return False
        cls = " ".join(p.get("class") or [])
        if cls and cls_re.search(cls):
            return True
    return False


def fetch_html(src):
    items = []
    raw = fetch(src["url"], src.get("fetch", "default"))
    if not raw:
        return items
    soup = BeautifulSoup(raw, "lxml")
    link_re = re.compile(src["link_re"])
    container_re = re.compile(src["container_class"]) if src.get("container_class") else None
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        full = urljoin(src["url"], href)
        if not link_re.search(full) or full in seen:
            continue
        if container_re and not _in_container(a, container_re):
            continue
        title = ""
        if src.get("title_selector"):
            te = a.select_one(src["title_selector"])
            if te:
                title = te.get_text(" ", strip=True)
        if not title:
            title = a.get_text(" ", strip=True)
        if not title or len(title) < 8:
            # 尝试从父级找标题（有些站点标题不在 <a> 文本里）
            parent = a.find_parent(["h2", "h3", "h4", "li", "article"])
            if parent:
                title = parent.get_text(" ", strip=True)
        title = re.sub(r"\s+", " ", title).strip()
        title = clean_title(title)
        if not title or len(title) < 8:
            continue
        seen.add(full)
        items.append({"title": title, "url": full, "date": None, "abstract": ""})
        if len(items) >= MAX_PER_SOURCE:
            break
    # 日期：URL 中优先
    if src.get("date_from_url"):
        for it in items:
            it["date"] = parse_date_any(it["url"])
    # 无日期的条目 → 尝试从列表上下文补齐（带位置匹配）
    for it in items:
        if it["date"]:
            continue
        pos = raw.find(it["url"].split("?")[0])
        if pos > 0:
            ctx = raw[max(0, pos - 500): pos + 500]
            it["date"] = parse_date_any(ctx)
    return items


# ── 详情页补齐（摘要 / 日期）─────────────────────────────────
def enrich_detail(items, src):
    """对缺少日期的条目抓详情页补齐（限量，控制请求数）"""
    need = [it for it in items if not it["date"]]
    for it in need[:25]:
        html = fetch(it["url"], src.get("fetch", "default"))
        if not html:
            continue
        try:
            soup = BeautifulSoup(html, "lxml")
            if not it["abstract"]:
                m = soup.find("meta", attrs={"name": "description"}) or \
                    soup.find("meta", attrs={"property": "og:description"})
                if m and m.get("content"):
                    it["abstract"] = m["content"].strip()
            if not it["date"]:
                m = soup.find("meta", attrs={"property": "article:published_time"}) or \
                    soup.find("meta", attrs={"name": "date"}) or \
                    soup.find("time")
                if m:
                    it["date"] = parse_date_any(m.get("content", "") or m.get("datetime", "") or m.get_text())
                if not it["date"]:
                    it["date"] = parse_date_any(soup.get_text(" ", strip=True)[:2000])
        except Exception:
            pass
        time.sleep(DELAY)


# ── 标题翻译（MyMemory 免费接口 → Google 备用 → 原文兜底）─────
class Translator:
    def __init__(self):
        self.cache = {}
        self.google_ok = True   # 熔断：Google 一旦失败即禁用（本机被墙/网络受限）
        self.mm_ok = True
        self._load()

    def _load(self):
        try:
            with open(CACHE, encoding="utf-8") as f:
                self.cache = json.load(f)
        except Exception:
            self.cache = {}

    def save(self):
        try:
            os.makedirs(os.path.dirname(CACHE), exist_ok=True)
            with open(CACHE, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, ensure_ascii=False)
        except Exception:
            pass

    @staticmethod
    def _is_cjk(text):
        """已是中文才跳过翻译：含假名(日)或谚文(韩)则必须翻译"""
        if re.search(r"[\u3040-\u30ff\uac00-\ud7af]", text):
            return False
        cjk = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
        return cjk >= max(4, len(text) * 0.4)

    def tr(self, text, src_lang):
        if not text or self._is_cjk(text):
            return text
        key = f"{src_lang}::{text}"
        if key in self.cache:
            return self.cache[key]
        out = ""
        if self.google_ok:
            out = self._google(text, src_lang)
        if not out and self.mm_ok:
            out = self._mymemory(text, src_lang)
        out = out or text
        self.cache[key] = out
        return out

    def _mymemory(self, text, src_lang):
        if not self.mm_ok:
            return ""
        try:
            r = requests.get("https://api.mymemory.translated.net/get",
                             params={"q": text[:480], "langpair": f"{src_lang}|zh-CN"},
                             timeout=12, headers={"User-Agent": UA})
            j = r.json()
            t = (j.get("responseData") or {}).get("translatedText") or ""
            if t and "MYMEMORY WARNING" not in t.upper():
                return t.strip()
            if "MYMEMORY WARNING" in (t or "").upper():
                self.mm_ok = False   # 配额用尽，熔断
        except Exception:
            pass
        return ""

    def _google(self, text, src_lang):
        if not self.google_ok:
            return ""
        try:
            r = requests.get("https://translate.googleapis.com/translate_a/single",
                             params={"client": "gtx", "sl": src_lang, "tl": "zh-CN",
                                     "dt": "t", "q": text[:480]},
                             timeout=6, headers={"User-Agent": UA})
            j = r.json()
            return "".join(seg[0] for seg in j[0] if seg and seg[0]).strip()
        except Exception:
            self.google_ok = False   # 熔断，后续不再尝试
            return ""


# ── 主流程 ──────────────────────────────────────────────────
def load_existing():
    try:
        with open(OUT, encoding="utf-8") as f:
            d = json.load(f)
            return d.get("articles", []) if isinstance(d, dict) else d
    except Exception:
        return []


def run(dry=False, only=None):
    tr = Translator()
    cutoff = now_cst().replace(tzinfo=None) - timedelta(days=RETENTION_DAYS)
    articles, source_stats = [], []

    for src in SOURCES:
        if only and src["key"] not in only:
            continue
        if not src.get("enabled"):
            source_stats.append({"key": src["key"], "name": src["name"],
                                 "market": src["market"], "count": 0, "status": "disabled"})
            continue
        log.info(f"抓取：{src['name']} ({src['market']}) → {src['url']}")
        items = fetch_rss(src) if src["type"] == "rss" else fetch_html(src)
        # 详情补齐（仅对缺日期/摘要的，限量）
        enrich_detail(items, src)

        kept = 0
        for it in items:
            title = it["title"]
            if is_excluded(title):
                continue
            dt = it["date"]
            if dt and dt < cutoff:
                continue
            cat = classify(title + " " + (it.get("abstract") or ""))
            sflag = is_s_level(title)
            articles.append({
                "title": tr.tr(title, src["lang"]),
                "title_original": title,
                "url": it["url"],
                "source": src["name"],
                "market": src["market"],
                "lang": src["lang"],
                "published_at": dt.strftime("%Y-%m-%d") if dt else now_cst().strftime("%Y-%m-%d"),
                "category": cat,
                "s_level": sflag,
                "s_reason": s_reason(title) if sflag else "",
                "abstract": (it.get("abstract") or "")[:ABSTRACT_MAX],
            })
            kept += 1
        source_stats.append({"key": src["key"], "name": src["name"], "market": src["market"],
                             "count": kept, "status": "ok" if kept else "empty"})
        log.info(f"  → 保留 {kept} 条")
        time.sleep(DELAY)

    # 合并历史（按 url 去重，保留新版本），并再次按窗口清理
    by_url = {a["url"]: a for a in articles}
    for old in load_existing():
        u = old.get("url")
        if u and u not in by_url:
            d = parse_date_any(old.get("published_at", ""))
            if not d or d >= cutoff:
                by_url[u] = old

    final = list(by_url.values())
    # 时间倒序（第一优先级）；同级按 S级 优先
    final.sort(key=lambda a: (a.get("published_at", ""), a.get("s_level", False)), reverse=True)

    result = {
        "last_updated": now_cst().strftime("%Y-%m-%d %H:%M"),
        "total": len(final),
        "s_count": sum(1 for a in final if a.get("s_level")),
        "retention_days": RETENTION_DAYS,
        "markets": MARKETS,
        "sources": source_stats,
        "articles": final,
    }

    tr.save()
    log.info(f"合计 {len(final)} 条（S级 {result['s_count']}）")

    if dry:
        for a in final[:25]:
            flag = "🔴S" if a["s_level"] else "  "
            print(f"  {flag} [{a['market']}|{a['category']}] {a['published_at']} {a['title'][:46]}")
        return result

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    log.info(f"已写入 {OUT}")
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--only", default="", help="只跑指定源key，逗号分隔（测试用）")
    args = ap.parse_args()
    run(dry=args.dry, only=set(x for x in args.only.split(",") if x) or None)
