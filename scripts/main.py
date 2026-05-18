"""
main.py — 主入口脚本
功能：并发抓取所有 RSS 源 → 去重 → 过滤 → 写入 JSON
"""
import json
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta

# 将 scripts 目录父级加入路径，确保 config/rss_fetcher 可正常导入
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.config import load_config, get_sources, get_settings
from scripts.rss_fetcher import fetch_rss

# ── 日志配置 ────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

TZ_CST = timezone(timedelta(hours=8))


def load_existing_data(filepath: str) -> dict:
    """加载已有 JSON 数据（用于合并历史）"""
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"无法加载已有数据: {e}")
    return {"articles": []}


def deduplicate(articles: list) -> list:
    """基于 id 字段去重，保留最新出现的版本"""
    seen = {}
    for art in articles:
        seen[art["id"]] = art
    return list(seen.values())


def filter_by_days(articles: list, retention_days: int) -> list:
    """只保留 retention_days 天内的文章"""
    cutoff = datetime.now(TZ_CST) - timedelta(days=retention_days)
    result = []
    for art in articles:
        try:
            pub = datetime.fromisoformat(art["published_at"])
            if pub.tzinfo is None:
                pub = pub.replace(tzinfo=TZ_CST)
            if pub >= cutoff:
                result.append(art)
        except Exception:
            # 时间解析失败，保留文章
            result.append(art)
    return result


def sort_by_time(articles: list) -> list:
    """按发布时间倒序排列"""
    def parse_time(art):
        try:
            return datetime.fromisoformat(art["published_at"])
        except Exception:
            return datetime.min.replace(tzinfo=TZ_CST)

    return sorted(articles, key=parse_time, reverse=True)


def save_json(data: dict, filepath: str):
    """保存 JSON 到文件"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"已保存: {filepath} ({len(data.get('articles', []))} 条)")


def main():
    logger.info("=" * 50)
    logger.info("全球食品资讯聚合 — 开始抓取")
    logger.info("=" * 50)

    # 加载配置
    cfg = load_config()
    sources = get_sources(cfg)
    settings = get_settings(cfg)

    timeout = settings["request_timeout"]
    max_workers = settings["max_workers"]
    retention_days = settings["retention_days"]
    summary_max_len = settings["summary_max_length"]
    data_dir = settings["data_dir"]

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir_abs = os.path.join(root_dir, data_dir)
    latest_path = os.path.join(data_dir_abs, "news_latest.json")
    archive_path = os.path.join(data_dir_abs, "news_archive.json")

    logger.info(f"已配置来源: {len(sources)} 个，保留天数: {retention_days}")

    # ── 并发抓取 ────────────────────────────────────────────
    all_new_articles = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(fetch_rss, src, timeout, summary_max_len): src["name"]
            for src in sources
        }
        for future in as_completed(futures):
            name = futures[future]
            try:
                articles = future.result()
                all_new_articles.extend(articles)
                logger.info(f"  [{name}] 完成，新增 {len(articles)} 条")
            except Exception as e:
                logger.error(f"  [{name}] 抓取失败: {e}")

    logger.info(f"本次抓取合计: {len(all_new_articles)} 条（含重复）")

    # ── 加载历史存档并合并 ──────────────────────────────────
    archive_data = load_existing_data(archive_path)
    historical = archive_data.get("articles", [])

    # 合并：新数据优先（去重以 id 为键，新数据覆盖旧数据）
    combined = all_new_articles + historical
    deduped = deduplicate(combined)
    logger.info(f"合并去重后: {len(deduped)} 条")

    # ── 保存历史存档（所有数据）────────────────────────────
    archive_out = {
        "last_updated": datetime.now(TZ_CST).isoformat(),
        "total": len(deduped),
        "articles": sort_by_time(deduped),
    }
    save_json(archive_out, archive_path)

    # ── 过滤最近 N 天，保存最新数据 ────────────────────────
    recent = filter_by_days(deduped, retention_days)
    recent_sorted = sort_by_time(recent)
    logger.info(f"近 {retention_days} 天内: {len(recent_sorted)} 条")

    # 收集来源列表
    source_names = sorted(set(a["source"] for a in recent_sorted))

    latest_out = {
        "last_updated": datetime.now(TZ_CST).isoformat(),
        "retention_days": retention_days,
        "total": len(recent_sorted),
        "sources": source_names,
        "articles": recent_sorted,
    }
    save_json(latest_out, latest_path)

    logger.info("=" * 50)
    logger.info(f"抓取完成！最新数据: {len(recent_sorted)} 条，来源: {len(source_names)} 个")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
