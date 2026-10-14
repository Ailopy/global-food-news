#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日跟踪 — 配置模块
─────────────────────────────────────────────
· 数据源：用户指定 7 个网站（按国家/地区归类）
· 保留窗口：最近 30 天（超过自动清理）
· 抓取频率：北京时间每日 09:00 / 15:00
· 分类：10 类（新产品/新包装/新技术/新原料/新营销/企业动态/财报/政策法规/人事/其他）
· S级：含"全球首创/首款/爆品/卖爆/热卖"等明显创新性或爆品属性
"""

# ── 保留与容量 ──────────────────────────────────────────────
RETENTION_DAYS = 30      # 只保留最近 1 个月
MAX_PER_SOURCE = 80      # 每个源最多解析条数（防止无限翻页）
ABSTRACT_MAX = 220       # 摘要最大显示长度

# ── 市场（国家/地区）与旗帜 ─────────────────────────────────
MARKETS = {
    "日本": "🇯🇵",
    "北美": "🇺🇸",
    "韩国": "🇰🇷",
    "欧洲": "🇪🇺",
}

# ── 分类标签（10 类）定义顺序即展示顺序 ─────────────────────
CATEGORIES = [
    "新产品", "新包装", "新技术", "新原料", "新营销",
    "企业动态", "财报", "政策法规", "人事", "其他",
]

# ── 数据源配置 ──────────────────────────────────────────────
# type: rss  → 用 feedparser 解析
# type: html → 抓列表页，正则/选择器提取条目
# fetch: default / cffi_safari(绕 Cloudflare) / playwright(JS挑战)
SOURCES = [
    {
        "key": "nissyoku", "name": "日本食粮新闻", "market": "日本",
        "lang": "ja", "type": "rss",
        "url": "https://news.nissyoku.co.jp/archives/news-cat/001/feed",
        "enabled": True,
    },
    {
        "key": "prtimes", "name": "PRTIMES", "market": "日本",
        "lang": "ja", "type": "html", "url": "https://prtimes.jp/gourmet/",
        "link_re": r"https://prtimes\.jp/main/html/rd/p/\d+\.\d+\.html",
        "title_selector": "[class*=title]",
        "date_from_url": False, "enabled": True,
    },
    {
        "key": "cnbc", "name": "CNBC Food & Beverage", "market": "北美",
        "lang": "en", "type": "html", "url": "https://www.cnbc.com/food-and-beverage/",
        "link_re": r"https://www\.cnbc\.com/20\d{2}/\d{2}/\d{2}/[a-z0-9-]+\.html",
        "container_class": "Card-titleContainer",
        "date_from_url": True, "enabled": True,
    },
    {
        "key": "beveragedaily", "name": "BeverageDaily", "market": "北美",
        "lang": "en", "type": "html", "url": "https://www.beveragedaily.com/News/",
        "link_re": r"https://www\.beveragedaily\.com/Article/20\d{2}/\d{2}/\d{2}/[a-z0-9-]+/",
        "date_from_url": True, "enabled": True,
    },
    {
        "key": "foodtoday", "name": "food today", "market": "韩国",
        "lang": "ko", "type": "html", "url": "https://www.foodtoday.or.kr/news/section.html?sec_no=80",
        "link_re": r"https://www\.foodtoday\.or\.kr/news/article\.html\?no=\d+",
        "title_selector": "h2",
        "date_from_url": False, "enabled": True,
    },
    {
        "key": "justfood", "name": "Just Food", "market": "欧洲",
        "lang": "en", "type": "html", "fetch": "cffi_safari",
        "url": "https://www.just-food.com/news/",
        "link_re": r"https://www\.just-food\.com/news/[a-z0-9-]+/",
        "date_from_url": False, "enabled": True,
    },
    {
        "key": "dairyreporter", "name": "Dairy Reporter", "market": "北美",
        "lang": "en", "type": "html", "url": "https://www.dairyreporter.com/",
        "link_re": r"https://www\.dairyreporter\.com/Article/20\d{2}/\d{2}/\d{2}/[a-z0-9-]+/",
        "date_from_url": True, "enabled": True,
    },
    {
        "key": "dairyfoods", "name": "Dairy Foods", "market": "北美",
        "lang": "en", "type": "html", "fetch": "playwright",
        "url": "https://www.dairyfoods.com/",
        "link_re": r"https://www\.dairyfoods\.com/articles/\d+/[a-z0-9-]+",
        "date_from_url": False,
        "enabled": False,   # Cloudflare JS挑战：HTTP(含15种指纹)与Playwright无头浏览器均无法通过，实测0条
    },
]

# ── 分类关键词（多语言），顺序即优先级：靠前优先命中 ─────────
CATEGORY_RULES = [
    # 更具体、更少误判的放前面
    ("政策法规", [
        "規制", "規制緩和", "法改正", "食品衛生法", "JAS", "許可", "禁止", "基準", "指針",
        "政策", "条例", "規格", "標準", "認証", "表示義務", "義務化",
        "regulation", "regulatory", "policy", "legislation", "compliance", "ban", "recall", "fda", "efsa",
        "규제", "법규", "정책", "기준", "인증", "고시",
        "监管", "法规", "政策", "标准", "认证", "召回", "禁令", "规范",
    ]),
    ("人事", [
        "人事", "社長就任", "CEO就任", "代表取締役", "執行役員", "役員人事", "就任",
        "appoints", "appointment", "names new", "steps down", "resigns", "new ceo", "new cfo", "hires",
        "임원", "인사", "선임", "취임", "대표이사",
        "上任", "任命", "离任", "换帅", "出任",
    ]),
    ("财报", [
        "決算", "業績", "売上高", "営業利益", "増収", "減収", "純利益", "見通し",
        "earnings", "revenue", "profit", "sales", "q1", "q2", "q3", "q4", "fiscal", "guidance", "results",
        "실적", "매출", "영업이익", "순이익",
        "财报", "营收", "净利", "业绩", "亏损", "增长",
    ]),
    ("新包装", [
        "パッケージ", "容器", "ボトル", "缶", "デザイン一新", "リニューアル", "包装",
        "packaging", "pack", "bottle", "can design", "new look", "redesign", "label",
        "포장", "패키지", "용기", "리뉴얼",
        "包装", "瓶身", "外包装", "新包装",
    ]),
    ("新原料", [
        "原料", "素材", "成分", "甘味料", "たんぱく", "タンパク", "エキス", "配合",
        "ingredient", "sweetener", "protein", "extract", "formulation", "additive", "fiber", "probiotic",
        "원료", "소재", "성분", "감미료", "단백질",
        "原料", "配料", "成分", "甜味剂", "蛋白", "提取物", "添加剂",
    ]),
    ("新技术", [
        "技術", "開発", "特許", "発酵", "製造法", "AI", "ロボット", "自動化", "研究",
        "technology", "tech", "patent", "innovation", "ai ", "robotics", "automation", "r&d", "process",
        "기술", "개발", "특허", "공정", "자동화",
        "技术", "研发", "专利", "工艺", "自动化", "发酵",
    ]),
    ("新营销", [
        "キャンペーン", "コラボ", "タイアップ", "販促", "限定", "PR", "CM", "広告", "ブランド",
        "campaign", "collaboration", "collab", "partnership", "promotion", "marketing", "tie-up", "limited edition", "brand",
        "캠페인", "협업", "콜라보", "프로모션", "마케팅", "광고",
        "营销", "联名", "跨界", "代言", "合作", "直播", "种草",
    ]),
    ("企业动态", [
        "買収", "合併", "統合", "提携", "業務提携", "出資", "投資", "進出", "子会社", "譲渡", "株式",
        "acqui", "merger", "merges", "invest", "expansion", "alliance", "stake", "takeover", "partnership",
        "인수", "합병", "투자", "제휴", "진출", "지분",
        "收购", "并购", "合并", "投资", "扩张", "合作", "融资", "上市",
    ]),
    ("新产品", [
        "新商品", "新製品", "発売", "登場", "リリース", "投入", "ラインアップ", "新ブランド",
        "launch", "launches", "new product", "unveils", "debuts", "introduces", "rolls out", "releases", "new range", "new line",
        "출시", "신제품", "선보", "론칭",
        "上市", "推出", "新品", "发布", "首发",
    ]),
]

# ── S级关键词（全球首创/首款/爆品/卖爆/热卖）────────────────
S_LEVEL_KWS = [
    # 首创/首款（日中英韩）
    "世界初", "世界最初", "業界初", "国内初", "日本初", "世界最高", "初の試み", "業界初の",
    "首个", "首款", "首例", "首推", "全球首创", "世界首创", "首开", "首度", "第一次",
    "world's first", "world first", "first-ever", "first ever", "first of its kind",
    "industry's first", "industry first", "world's only", "only one",
    "세계 최초", "국내 최초", "업계 최초", "최초",
    # 爆品/卖爆/热卖
    "爆売れ", "大ヒット", "ヒット商品", "売上No.1", "売れ筋", "話題沸騰", "完売", "品切れ",
    "爆品", "卖爆", "热卖", "爆火", "热销", "抢购", "断货", "脱销", "销量第一", "销量翻",
    "best-selling", "bestseller", "best seller", "sells out", "sold out", "viral", "hit product",
    "blockbuster", "record-breaking", "top-selling",
    "완판", "매진", "판매 1위", "대박", "히트",
]

# ── 食品安全/相关领域排除（避免明显非食品内容）────────────────
EXCLUDE_KWS = [
    "不動産", "住宅", "株価", "株式市場", "仮想通貨", "暗号資産",
    "real estate", "stock market", "crypto", "mortgage", "reit",
    "부동산", "주식", "가상화폐",
    "房地产", "股市", "加密货币", "房贷",
]


def classify(text: str) -> str:
    """按关键词把资讯归入 10 类之一（顺序即优先级）"""
    t = (text or "").lower()
    for cat, kws in CATEGORY_RULES:
        for kw in kws:
            if kw.lower() in t:
                return cat
    return "其他"


def is_s_level(text: str) -> bool:
    """是否命中 S级（明显创新性或爆品属性）"""
    t = (text or "").lower()
    return any(kw.lower() in t for kw in S_LEVEL_KWS)


def s_reason(text: str):
    """返回命中的 S级关键词（用于展示标注理由）"""
    t = (text or "").lower()
    for kw in S_LEVEL_KWS:
        if kw.lower() in t:
            return kw
    return ""


def is_excluded(text: str) -> bool:
    """明显非食品领域内容剔除"""
    t = (text or "").lower()
    return any(kw.lower() in t for kw in EXCLUDE_KWS)
