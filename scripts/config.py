"""
config.py — 配置加载器
读取 sources.yaml 并提供全局配置对象
"""
import os
import yaml

# 项目根目录（此文件在 scripts/ 下，根目录为上级）
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(ROOT_DIR, "sources.yaml")


def load_config() -> dict:
    """加载并返回 sources.yaml 配置"""
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg


def get_sources(cfg: dict) -> list:
    """返回所有 enabled=true 的来源列表，按优先级倒序排列（A+ > A > B > C）"""
    sources = [s for s in cfg.get("sources", []) if s.get("enabled", True)]
    level_order = {"A+": 0, "A": 1, "B": 2, "C": 3, "D": 4}
    def sort_key(s):
        lvl = s.get("level", "B")
        # 未定义 level 排在 B 之后
        return (level_order.get(lvl, 2), s.get("name", ""))
    sources.sort(key=sort_key)
    return sources


def get_settings(cfg: dict) -> dict:
    """返回 settings 配置项，并补充默认值（兼容新旧字段名）"""
    s = cfg.get("settings", {})
    return {
        "retention_days": s.get("keep_days", s.get("retention_days", 7)),
        "summary_max_length": s.get("summary_max_length", 200),
        "request_timeout": s.get("fetch_timeout", s.get("request_timeout", 15)),
        "max_workers": s.get("max_workers", 6),
        "data_dir": s.get("output_dir", s.get("data_dir", "web/data")),
        "web_dir": s.get("web_dir", "web"),
    }
