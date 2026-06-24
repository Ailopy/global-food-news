# -*- coding: utf-8 -*-
"""
s_topics_config.py — S级选题跟踪网站配置
来源：用户Excel表（S级选题跟踪网站.xlsx）
共 7 个网站：日本(4) / 北美(2) / 北美&欧洲(1)
新增：日経新聞主站（www.nikkei.com）via Google News RSS
"""

# ── S级选题跟踪网站列表 ────────────────────────────────────────
S_TOPIC_SITES = [
    {
        "name": "日経新聞",
        "name_en": "Nikkei News",
        "region": "日本",
        "positioning": "新品&产业",
        "desc": "日本经济新闻主站，食品饮料新品发布/产业动态，通过Google News RSS抓取",
        "url": "https://www.nikkei.com/",
        "rss_candidates": [
            # Google News RSS 是抓取 nikkei.com 食品新闻最稳定的方式
            "https://news.google.com/rss/search?q=site:nikkei.com+%E9%A3%9F%E5%93%81+%E6%96%B0%E5%95%86%E5%93%81&hl=ja&gl=JP&ceid=JP:ja",
            "https://news.google.com/rss/search?q=site:nikkei.com+%E9%A3%9F%E5%93%81&hl=ja&gl=JP&ceid=JP:ja",
        ],
    },
    {
        "name": "日経xTrend",
        "name_en": "Nikkei xTrend",
        "region": "日本",
        "positioning": "综合&分析",
        "desc": "日本行业分析网站，产品开发/趋势/营销案例",
        "url": "https://xtrend.nikkei.com/atcl/contents/new/?i_cid=nbpnxr_top_new_list",
        "rss_candidates": [
            "https://xtrend.nikkei.com/rss/index.rdf",
            "https://xtrend.nikkei.com/rss/",
        ],
    },
    {
        "name": "PR Times",
        "name_en": "PR Times",
        "region": "日本",
        "positioning": "新品&新闻",
        "desc": "日本新品预发布信息，品牌营销活动，按时间顺序检索",
        "url": "https://prtimes.jp/main/html/searchbiscate/busi_cate_id/013/lv2/41",
        "rss_candidates": [
            "https://prtimes.jp/rss/category/013.rss",
            "https://prtimes.jp/rss/",
        ],
    },
    {
        "name": "日本食粮新闻",
        "name_en": "Nissyoku News",
        "region": "日本",
        "positioning": "新闻&新品",
        "desc": "食品行业新动向，新战略，包括食品行业和餐饮业企业动向，新产品栏目",
        "url": "https://news.nissyoku.co.jp/archives/news-cat/08",
        "rss_candidates": [
            "https://news.nissyoku.co.jp/feed",
            "https://news.nissyoku.co.jp/rss",
        ],
    },
    {
        "name": "Trend Hunter",
        "name_en": "Trend Hunter",
        "region": "北美&欧洲",
        "positioning": "新品发布",
        "desc": "欧美新品汇集，包装颜值高，符合流行热点，食品饮料新品板块",
        "url": "https://www.trendhunter.com/ideas/food",
        "rss_candidates": [
            "https://www.trendhunter.com/rss/food",
            "https://www.trendhunter.com/feed",
        ],
    },
    {
        "name": "Food Dive",
        "name_en": "Food Dive",
        "region": "北美",
        "positioning": "行业分析",
        "desc": "产品、品牌、商业综合信息，更新频率高，分析角度深入，新品跟踪",
        "url": "https://www.fooddive.com",
        "rss_candidates": [
            "https://www.fooddive.com/feeds/news.rss",
            "https://www.fooddive.com/rss/",
        ],
    },
    {
        "name": "Packaging Digest",
        "name_en": "Packaging Digest",
        "region": "北美",
        "positioning": "包装&设计",
        "desc": "聚焦包装趋势、包材、包装设计，偏行业与专业",
        "url": "https://www.packagingdigest.com/food-beverage",
        "rss_candidates": [
            "https://www.packagingdigest.com/rss.xml",
            "https://www.packagingdigest.com/feed",
        ],
    },
]

# ── S+ 级判断关键词（命中任意一个 → S+）────────────────────────
# 含义：全球/日本/亚洲首创、首款、爆品、卖爆、热卖等明显创新或爆品属性
S_PLUS_KEYWORDS = [
    # 首创/首款
    "world first", "world's first", "global first", "industry first",
    "first in the world", "first ever", "first time", "first-ever",
    "pioneering", "unprecedented", "groundbreaking",
    # 日语首创
    "世界初", "業界初", "日本初", "初登場", "初披露", "史上初",
    "世界で初", "国内初", "アジア初", "初の試み", "初めて",
    # 爆品/热卖
    "viral", "gone viral", "sold out", "sell out", "instant sellout",
    "best seller", "bestseller", "record sales", "record-breaking",
    "top seller", "most popular", "highly anticipated",
    "million units", "billion units", "huge success",
    "飞速售罄", "卖断货", "卖爆", "热销", "爆品", "爆款",
    "大卖", "销售额破", "热卖", "超预期",
    # 日语爆品
    "大ヒット", "品切れ", "即完売", "完売", "爆発的", "売上記録",
    "話題", "大人気", "バズ", "インスタ映え", "話題沸騰",
    "累計販売", "億本", "万本突破", "売れ筋",
    # 创新性
    "revolutionary", "breakthrough", "disruptive", "innovative",
    "game-changer", "game changer", "next generation", "next-gen",
    "cutting-edge", "state-of-the-art",
    # 日语创新性
    "ユニーク", "画期的", "革新的", "新感覚", "独自技術",
    "新たな体験", "新しい飲み方", "新しい食べ方", "体験価値",
    # 特殊联名/合作
    "collab", "collaboration", "limited edition", "limited-edition",
    "co-branded", "co-creation",
    # 日语联名（常见缩写和表达）
    "コラボ", "コラボレーション", "タイアップ", "限定コラボ",
    # 特殊视觉/感官创新（如开盖浮起柠檬片这类）
    "食感", "浮き上がる", "見た目", "映える", "インパクト",
    "ビジュアル", "演出", "仕掛け", "仕様",
]

# ── 品类分析关键词映射（10个品类）──────────────────────────────
# 每个品类有主关键词和辅助关键词，命中得分最高的品类胜出
CATEGORY_KEYWORDS = {
    "新产品": {
        "icon": "🆕",
        "color": "#2563eb",
        "keywords": [
            "new product", "new launch", "launches", "new item", "new range",
            "new offering", "product debut", "new arrival", "just launched",
            "released", "new release", "unveil", "unveiled",
            "新商品", "新製品", "発売", "新発売", "発表", "リリース",
            "debut", "introduce", "introducing", "rollout",
        ],
        "negative": ["flavor", "variety", "size", "color", "colour"],  # 新口味/规格不算
    },
    "新包装": {
        "icon": "📦",
        "color": "#7c3aed",
        "keywords": [
            "new packaging", "packaging redesign", "redesigned packaging",
            "new design", "new look", "rebrand", "rebranding", "refresh",
            "label redesign", "bottle design", "can design", "wrapper",
            "sustainable packaging", "eco packaging", "recyclable packaging",
            "packaging innovation", "pack design", "新パッケージ", "パッケージ",
            "リデザイン", "リブランディング",
        ],
        "negative": [],
    },
    "新技术": {
        "icon": "⚡",
        "color": "#0891b2",
        "keywords": [
            "new technology", "new tech", "technology breakthrough",
            "patent", "patented", "proprietary technology",
            "ai ", "artificial intelligence", "machine learning",
            "3d printing", "fermentation technology", "precision fermentation",
            "biotechnology", "biotech", "nano", "nanotechnology",
            "production technology", "manufacturing process",
            "新技術", "テクノロジー", "特許", "革新技術",
        ],
        "negative": [],
    },
    "新原料": {
        "icon": "🧪",
        "color": "#059669",
        "keywords": [
            "new ingredient", "novel ingredient", "ingredients",
            "functional ingredient", "superfood", "allulose", "allulose",
            "precision fermentation", "alternative protein", "plant-based protein",
            "insect protein", "cultivated meat", "cell-based", "lab-grown",
            "prebiotic", "probiotic", "postbiotic", "adaptogens",
            "hemp", "cbd", "collagen", "nootropic",
            "新原材料", "新成分", "新素材", "機能性素材",
        ],
        "negative": [],
    },
    "联名营销": {
        "icon": "🤝",
        "color": "#c2410c",
        "keywords": [
            "collab", "collaboration", "co-brand", "co-branded",
            "partnership", "team up", "join forces",
            "x ", "×", "crossover", "co-creation",
            "コラボ", "コラボレーション", "タイアップ",
        ],
        "negative": [],
    },
    "营销创新": {
        "icon": "🎯",
        "color": "#9333ea",
        "keywords": [
            "marketing campaign", "viral campaign", "ad campaign",
            "brand campaign", "social media campaign", "influencer",
            "tiktok", "instagram", "youtube", "viral", "trending",
            "stunt", "experiential", "pop-up", "activation",
            "limited edition drop", "flash sale", "guerrilla",
            "マーケティング", "キャンペーン", "広告",
        ],
        "negative": [],
    },
    "并购融资": {
        "icon": "💼",
        "color": "#b45309",
        "keywords": [
            "acquisition", "acquire", "merger", "merge", "takeover",
            "investment", "funding", "raises", "series a", "series b",
            "ipo", "listing", "valuation", "billion deal",
            "partnership agreement", "joint venture",
            "買収", "合併", "出資", "投資", "上場", "資金調達",
        ],
        "negative": [],
    },
    "行业政策": {
        "icon": "📋",
        "color": "#374151",
        "keywords": [
            "regulation", "regulatory", "fda", "eu regulation", "policy",
            "ban", "banned", "approved", "approval", "recall",
            "food safety", "safety concern", "health warning",
            "legislation", "law", "act", "standard",
            "规制", "規制", "法律", "政策", "食品安全",
        ],
        "negative": [],
    },
    "渠道新物种": {
        "icon": "🏪",
        "color": "#0f766e",
        "keywords": [
            "new store", "pop-up store", "flagship store", "concept store",
            "vending machine", "direct to consumer", "dtc",
            "subscription", "e-commerce", "omnichannel",
            "convenience store", "retailer", "distribution",
            "新業態", "新チャンネル", "コンビニ", "通販",
        ],
        "negative": [],
    },
    "品牌故事": {
        "icon": "✨",
        "color": "#6b7280",
        "keywords": [
            "brand story", "founder", "heritage", "history",
            "sustainability", "purpose", "mission", "vision",
            "social responsibility", "csr", "community",
            "brand values", "authenticity",
            "ブランド", "ストーリー", "創業", "歴史",
        ],
        "negative": [],
    },
}
