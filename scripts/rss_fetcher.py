"""
rss_fetcher.py — RSS/Atom Feed 抓取器
支持多语言、时区转换、摘要提取
"""
import hashlib
import logging
import re
from datetime import datetime, timezone, timedelta
from typing import Optional

import feedparser
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# 北京时间 UTC+8
TZ_CST = timezone(timedelta(hours=8))

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


def make_article_id(url: str, title: str) -> str:
    """基于 URL + 标题生成唯一 ID"""
    raw = f"{url.strip()}{title.strip()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def to_beijing_time(t) -> Optional[str]:
    """
    将 feedparser 的 time_struct 或 datetime 转为北京时间 ISO 字符串
    返回格式: "2026-04-25T08:00:00+08:00"
    """
    if t is None:
        return None
    try:
        if hasattr(t, "timetuple"):
            # 已经是 datetime 对象
            dt = t
        else:
            # feedparser time_struct (UTC)
            import time as time_mod
            ts = time_mod.mktime(t)
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)

        # 确保有时区信息
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        # 转为北京时间
        dt_cst = dt.astimezone(TZ_CST)
        return dt_cst.isoformat()
    except Exception as e:
        logger.debug(f"时间转换失败: {e}")
        return None


def clean_html(html_text: str) -> str:
    """清除 HTML 标签，返回纯文本"""
    if not html_text:
        return ""
    soup = BeautifulSoup(html_text, "lxml")
    return soup.get_text(separator=" ", strip=True)


def truncate_summary(text: str, max_len: int = 200) -> str:
    """截取摘要到指定长度，在词边界处截断"""
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_len:
        return text
    # 在最后一个完整词/句处截断
    truncated = text[:max_len]
    last_space = max(truncated.rfind(" "), truncated.rfind("。"), truncated.rfind("，"))
    if last_space > max_len * 0.7:
        truncated = truncated[:last_space]
    return truncated.strip() + "…"


def extract_summary(entry, max_len: int = 200) -> str:
    """从 RSS 条目提取摘要"""
    # 优先使用 summary 字段
    for field in ("summary", "description", "content"):
        raw = getattr(entry, field, None)
        if raw:
            if isinstance(raw, list):
                raw = raw[0].get("value", "") if raw else ""
            text = clean_html(raw)
            if len(text) > 20:
                return truncate_summary(text, max_len)
    return ""


def fetch_rss(source: dict, timeout: int = 20, summary_max_len: int = 200) -> list:
    """
    抓取单个 RSS 源，返回文章列表
    
    Args:
        source: sources.yaml 中的单条配置
        timeout: HTTP 请求超时秒数
        summary_max_len: 摘要最大长度
    
    Returns:
        list of article dicts
    """
    rss_url = source.get("rss", "")
    source_name = source.get("name", "未知来源")
    language = source.get("language", "en")

    if not rss_url:
        logger.warning(f"[{source_name}] 无 RSS 地址，跳过")
        return []

    articles = []
    try:
        resp = requests.get(rss_url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()

        feed = feedparser.parse(resp.content)

        if feed.bozo and not feed.entries:
            logger.warning(f"[{source_name}] Feed 解析异常: {feed.bozo_exception}")
            return []

        logger.info(f"[{source_name}] 获取到 {len(feed.entries)} 条资讯")

        for entry in feed.entries:
            title = getattr(entry, "title", "").strip()
            link = getattr(entry, "link", "").strip()

            if not title or not link:
                continue

            # 发布时间
            published_at = to_beijing_time(
                getattr(entry, "published_parsed", None)
                or getattr(entry, "updated_parsed", None)
            )
            if published_at is None:
                # 无时间则用当前时间
                published_at = datetime.now(TZ_CST).isoformat()

            # 摘要
            summary = extract_summary(entry, summary_max_len)

            article = {
                "id": make_article_id(link, title),
                "title": title,
                "summary": summary,
                "url": link,
                "published_at": published_at,
                "source": source_name,
                "region": source.get("region", ""),
                "category": source.get("category", "综合"),
                "level": source.get("level", ""),
                "language": language,
            }
            articles.append(article)

    except requests.exceptions.RequestException as e:
        logger.error(f"[{source_name}] 请求失败: {e}")
    except Exception as e:
        logger.error(f"[{source_name}] 未知错误: {e}", exc_info=True)

    return articles
