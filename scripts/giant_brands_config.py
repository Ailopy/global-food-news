# -*- coding: utf-8 -*-
"""
giant_brands_config.py — 全球头部巨头官网配置
数据来源：全球头部巨头网站.xlsx（品牌/地区/网址）
"""

GIANT_BRANDS = [
    # ── 百事 ──────────────────────────────────────────────
    {"brand": "PepsiCo",     "brand_cn": "百事",     "region": "北美", "url": "https://www.pepsico.com/newsroom/press-releases-category"},
    {"brand": "PepsiCo",     "brand_cn": "百事",     "region": "中国", "url": "https://www.pepsico.com.cn/media-center"},
    # ── 联合利华 ──────────────────────────────────────────
    {"brand": "Unilever",    "brand_cn": "联合利华",  "region": "欧洲", "url": "https://www.unilever.com/news/"},
    # ── 百威英博 ──────────────────────────────────────────
    {"brand": "AB InBev",    "brand_cn": "百威英博",  "region": "欧洲", "url": "https://www.ab-inbev.com/news-media"},
    # ── 雀巢 ──────────────────────────────────────────────
    {"brand": "Nestlé",      "brand_cn": "雀巢",     "region": "欧洲", "url": "https://www.nestle.com/media/news"},
    {"brand": "Nestlé",      "brand_cn": "雀巢",     "region": "日本", "url": "https://www.nestle.co.jp/media/pressreleases"},
    {"brand": "Nestlé",      "brand_cn": "雀巢",     "region": "中国", "url": "https://www.nestle.com.cn/media"},
    {"brand": "Nestlé HS",   "brand_cn": "雀巢",     "region": "欧洲", "url": "https://www.nestlehealthscience.com/newsroom"},
    # ── 玛氏 ──────────────────────────────────────────────
    {"brand": "Mars",        "brand_cn": "玛氏",     "region": "北美", "url": "https://www.mars.com/news-and-stories/all-news-and-stories"},
    {"brand": "Mars",        "brand_cn": "玛氏",     "region": "日本", "url": "https://www.mars.com/ja-jp/news-and-stories/all-news-and-stories"},
    # ── 可口可乐 ──────────────────────────────────────────
    {"brand": "Coca-Cola",   "brand_cn": "可口可乐",  "region": "北美", "url": "https://www.coca-colacompany.com/media-center"},
    {"brand": "Coca-Cola",   "brand_cn": "可口可乐",  "region": "日本", "url": "https://www.coca-cola.com/jp/ja/media-center"},
    {"brand": "Coca-Cola",   "brand_cn": "可口可乐",  "region": "中国", "url": "https://www.coca-cola.com/cn/zh/media-center"},
    # ── 亿滋 ──────────────────────────────────────────────
    {"brand": "Mondelez",    "brand_cn": "亿滋",     "region": "北美", "url": "https://www.mondelezinternational.com/news/"},
    {"brand": "Mondelez",    "brand_cn": "亿滋",     "region": "北美", "url": "https://www.mondelezinternational.com/media/press-releases/"},
    # ── 卡夫亨氏 ──────────────────────────────────────────
    {"brand": "Kraft Heinz", "brand_cn": "卡夫亨氏",  "region": "北美", "url": "https://news.kraftheinzcompany.com/press-releases/default.aspx"},
    # ── 通用磨坊 ──────────────────────────────────────────
    {"brand": "General Mills","brand_cn": "通用磨坊", "region": "北美", "url": "https://www.generalmills.com/news/press-releases"},
    # ── 达能 ──────────────────────────────────────────────
    {"brand": "Danone",      "brand_cn": "达能",     "region": "欧洲", "url": "https://www.danone.com/newsroom/press-releases.html"},
    {"brand": "Danone",      "brand_cn": "达能",     "region": "欧洲", "url": "https://www.danoneresearch.com/"},
    # ── 费列罗 ──────────────────────────────────────────────
    {"brand": "Ferrero",     "brand_cn": "费列罗",    "region": "欧洲", "url": "https://www.ferrero.com/int/en/news-stories/news"},
    # ── 三得利 ──────────────────────────────────────────────
    {"brand": "Suntory",     "brand_cn": "三得利",    "region": "日本", "url": "https://www.suntory.com/news/?ke=mn"},
    {"brand": "Suntory",     "brand_cn": "三得利",    "region": "日本", "url": "https://www.suntory.co.jp/news/?fromid=top"},
    {"brand": "Suntory",     "brand_cn": "三得利",    "region": "日本", "url": "https://www.suntory.co.jp/sic/whatsnew/"},
    # ── 朝日 ──────────────────────────────────────────────
    {"brand": "Asahi",       "brand_cn": "朝日",     "region": "日本", "url": "https://www.asahigroup-holdings.com/newsroom/"},
    {"brand": "Asahi",       "brand_cn": "朝日",     "region": "日本", "url": "https://www.asahiinryo.co.jp/company/newsrelease/"},
    {"brand": "Asahi",       "brand_cn": "朝日",     "region": "日本", "url": "https://www.asahibeer.co.jp/news/2025/"},
    # ── 日清食品 ──────────────────────────────────────────
    {"brand": "Nissin",      "brand_cn": "日清食品",  "region": "日本", "url": "https://www.nissin.com/jp/company/news/"},
    # ── 麒麟 ──────────────────────────────────────────────
    {"brand": "Kirin",       "brand_cn": "麒麟",     "region": "日本", "url": "https://www.kirinholdings.com/jp/newsroom/"},
    # ── 味之素 ──────────────────────────────────────────
    {"brand": "Ajinomoto",   "brand_cn": "味之素",    "region": "日本", "url": "https://news.ajinomoto.co.jp/"},
    # ── 明治 ──────────────────────────────────────────────
    {"brand": "Meiji",       "brand_cn": "明治",     "region": "日本", "url": "https://www.meiji.co.jp/corporate/pressrelease/"},
    {"brand": "Meiji",       "brand_cn": "明治",     "region": "日本", "url": "https://www.meiji.co.jp/quality/r_d/topics/"},
    # ── 雪印 ──────────────────────────────────────────────
    {"brand": "Megmilk",     "brand_cn": "雪印",     "region": "日本", "url": "https://www.meg-snow.com/news/"},
    # ── 森永 ──────────────────────────────────────────────
    {"brand": "Morinaga",    "brand_cn": "森永",     "region": "日本", "url": "https://www.morinagamilk.co.jp/release/"},
    # ── 养乐多 ──────────────────────────────────────────
    {"brand": "Yakult",      "brand_cn": "养乐多",    "region": "日本", "url": "https://www.yakult.co.jp/information/"},
    # ── 伊藤园 ──────────────────────────────────────────
    {"brand": "Ito En",      "brand_cn": "伊藤园",    "region": "日本", "url": "https://www.itoen.co.jp/news/release/"},
    # ── 希杰 ──────────────────────────────────────────────
    {"brand": "CJ",          "brand_cn": "希杰",     "region": "韩国", "url": "https://www.cj.co.kr/kr/newsroom/overview"},
    # ── 乐天七星 ──────────────────────────────────────────
    {"brand": "Lotte Chilsung","brand_cn":"乐天七星", "region": "韩国", "url": "https://company.lottechilsung.co.kr/kor/company/news/list.do"},
]

# S级关键词 — 行业巨头大动作 / 新原料 / 新技术 / 新产品 / 营销创新 / 重磅新政
S_LEVEL_KEYWORDS = {
    # ── 并购/合并/重大商业动作 ──
    "acquisition": "并购", "merger": "并购", "acquire": "并购", "merge": "并购",
    "buyout": "并购", "takeover": "并购", "buy out": "并购",
    "收购": "并购", "并购": "并购", "合并": "并购",
    # ── 新原料/原料创新 ──
    "allulose": "新原料", "阿洛酮糖": "新原料", "rare sugar": "新原料",
    "new ingredient": "新原料", "novel ingredient": "新原料",
    "alternative protein": "新原料", "precision fermentation": "新原料",
    "cell-based": "新原料", "cultivated meat": "新原料",
    "new sweetener": "新原料", "stevia": "新原料",
    "adaptogen": "新原料", "功能性原料": "新原料",
    # ── 新技术/突破 ──
    "breakthrough": "新技术", "new technology": "新技术",
    "innovation": "新技术", "patent": "新技术",
    "新技术": "新技术", "技术突破": "新技术",
    # ── 新产品（非新口味）/首发 ──
    "first-ever": "新产品", "world first": "新产品", "全球首款": "新产品",
    "global first": "新产品", "first of its kind": "新产品",
    "全新产品": "新产品", "新品类": "新产品",
    "launch": "新产品", "debut": "新产品", "unveil": "新产品",
    "introduc": "新产品", "新品": "新产品",
    # ── 巨头联名/创新营销 ──
    "collaboration": "营销创新", "collab": "营销创新",
    "co-branding": "营销创新", "cross-brand": "营销创新",
    "联名": "营销创新", "limited edition": "营销创新",
    "限定": "营销创新", "viral": "营销创新",
    # ── 重磅政策/法规/安全 ──
    "regulation": "重磅新政", "FDA": "重磅新政", "ban": "重磅新政",
    "carcinogen": "重磅新政", "aspartame": "重磅新政", "食品安全": "重磅新政",
    "批准": "重磅新政", "法规": "重磅新政",
}

# A级关键词 — 普通新品/扩展/可持续
A_LEVEL_KEYWORDS = [
    "new flavor", "new variant", "new taste", "expansion",
    "sustainability", "sustainable", "campaign", "partnership",
    "新口味", "新装", "扩展", "可持续",
]

# 地区 emoji 映射
REGION_ICON = {
    "北美": "🇺🇸", "欧洲": "🇪🇺", "日本": "🇯🇵",
    "中国": "🇨🇳", "韩国": "🇰🇷",
}
