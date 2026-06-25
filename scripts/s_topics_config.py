# -*- coding: utf-8 -*-
"""
s_topics_config.py — S级选题跟踪网站配置
来源：用户Excel表（S级选题跟踪网站.xlsx）
共 8 个网站：日本(4) / 北美(2) / 北美&欧洲(1) / YouTube(1)
新增：日経新聞主站（www.nikkei.com）via Google News RSS
新增：朝日グループ公式YouTubeチャンネル（产品广告监控）
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
    {
        "name": "朝日グループYouTube",
        "name_en": "Asahi Group YouTube",
        "region": "日本",
        "positioning": "产品广告&视频",
        "desc": "朝日集团官方YouTube频道，监控新产品广告/CM视频发布，特别关注「未来のレモンサワー」系列产品",
        "url": "https://www.youtube.com/@AsahiGroupHoldings/videos",
        "type": "youtube",
        "channel_id": "UCsqyXuphJN_Msxuik8QOW5Q",
        "rss_candidates": [
            "https://www.youtube.com/feeds/videos.xml?channel_id=UCsqyXuphJN_Msxuik8QOW5Q",
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

# ── 重点产品盯梢清单 ────────────────────────────────────────────
# 命中任意关键词 → 标记为 watched_product（前端高亮+特殊标注）
# 第一时间发现新产品广告/CM视频
PRODUCT_WATCH_LIST = [
    {
        "product_name": "未来のレモンサワー 檸檬（レモン）コーラサワー",
        "brand": "アサヒ",
        "keywords": [
            "レモンサワー", "檸檬コーラ", "コーラサワー",
            "未来のレモン", "レモンコーラ", "檸檬サワー",
            "ミライレモン", "レモンサワーCM", "レモンサワー広告",
            "lemon sour", "cola sour", "mirai lemon",
            "柠檬可乐", "柠檬沙瓦",
        ],
        "priority": "URGENT",   # 紧急盯梢 — 发现后第一时间通知
    },
]

# ── 食品饮料行业企业名称列表 ──────────────────────────────────────
# 文章标题或摘要命中这些企业名称 → 直接判定为食品饮料行业相关
# （即使不包含食品饮料品类关键词，只要提到食品饮料公司也保留）
FOOD_BEV_COMPANY_NAMES = [
    # ── 全球巨头 ──
    # 百事 PepsiCo
    "pepsico", "pepsi", "百事", "ペプシ",
    # 可口可乐 Coca-Cola
    "coca-cola", "cocacola", "コカ・コーラ", "可口可乐", "コカコーラ",
    # 雀巢 Nestlé
    "nestle", "nestlé", "雀巢", "ネスレ",
    # 联合利华 Unilever
    "unilever", "联合利华", "ユニリーバ",
    # 亿滋 Mondelez
    "mondelez", "亿滋", "モンデリーズ",
    # 玛氏 Mars
    "mars inc", "mars incorporated", "玛氏", "マース",
    # 卡夫亨氏 Kraft Heinz
    "kraft heinz", "kraft", "heinz", "卡夫亨氏", "亨氏", "クラフト", "ハインツ",
    # 百威英博 AB InBev
    "ab inbev", "anheuser-busch", "百威英博", "アンハイザー・ブッシュ",
    "budweiser", "百威", "バドワイザー",
    # 达能 Danone
    "danone", "达能", "ダノン",
    # 通用磨坊 General Mills
    "general mills", "通用磨坊", "ゼネラルミルズ",
    # 费列罗 Ferrero
    "ferrero", "费列罗", "フェレロ",
    # 嘉吉 Cargill
    "cargill", "嘉吉", "カーギル",
    # ADM
    "adm", "archer daniels", "アーチャー・ダニエルズ",
    # DSM (帝斯曼-芬美意)
    "dsm", "dsm-firmenich", "帝斯曼", "芬美意",
    # 恒天然 Fonterra
    "fonterra", "恒天然", "フォンテラ",
    # Ingredion
    "ingredion", "宜瑞安",
    # JBS
    "jbs", "jbs usa",
    # 泰森 Tyson
    "tyson foods", "tyson", "泰森", "タイソン",
    # 凯洛格 Kellanova (原Kellogg's)
    "kellanova", "kellogg", "kelloggs", "家乐氏", "ケロッグ",
    # ── 日本巨头 ──
    # 朝日 Asahi
    "asahi", "アサヒ", "朝日", "asahi group",
    # 麒麟 Kirin
    "kirin", "キリン", "麒麟",
    # 三得利 Suntory
    "suntory", "サントリー", "三得利",
    # 日清食品 Nissin
    "nissin", "日清食品", "日清", "ニッスイ", "ニッシン",
    # 味之素 Ajinomoto
    "ajinomoto", "味之素", "アジノモト",
    # 明治 Meiji
    "meiji", "明治", "meiji holdings",
    # 雪印 Megmilk
    "megmilk", "雪印", "メグミルク", "雪印メグミルク",
    # 森永 Morinaga
    "morinaga", "森永", "モリナガ", "森永乳業", "morinaga milk",
    # 养乐多 Yakult
    "yakult", "养乐多", "ヤクルト",
    # 伊藤园 Ito En
    "ito en", "伊藤园", "伊藤園",
    # 江崎グリコ Ezaki Glico
    "glico", "グリコ", "江崎グリコ",
    # 卡乐比 Calbee
    "calbee", "カールビー", "カルビー",
    # 不二家 Fujiya
    "fujiya", "不二家", "フジヤ",
    # 永旺 Aeon
    "aeon", "イオン", "永旺",
    # 龟田 Kameda
    "kameda", "龟田", "亀田", "亀田製菓",
    # ロッテ Lotte (日本)
    "lotte", "ロッテ",
    # ── 韩国巨头 ──
    # 希杰 CJ
    "cj cheiljedang", "cj group", "希杰", "cj제일제당",
    # 乐天七星 Lotte Chilsung
    "lotte chilsung", "乐天七星", "롯데칠성",
    # 农心 Nongshim
    "nongshim", "农心", "농심",
    # ── 中国巨头 ──
    # 康师傅
    "康师傅", "master kong", "ティンイー",
    # 统一
    "统一企业", "uni-president",
    # 伊利
    "伊利", "yili",
    # 蒙牛
    "蒙牛", "mengniu",
    # 光明
    "光明乳业", "bright dairy",
    # 华润啤酒
    "华润啤酒", "china resources beer",
    # 青岛啤酒
    "青岛啤酒", "tsingtao", "チンタオ",
    # 农夫山泉
    "农夫山泉", "nongfu spring",
    # 娃哈哈
    "娃哈哈", "wahaha",
    # 飞鹤
    "飞鹤", "feihe",
    # 益海嘉里
    "益海嘉里", "wilmar", "丰益国际",
    # 双汇
    "双汇", "shineway",
    # ── 欧美其他 ──
    # 喜力 Heineken
    "heineken", "喜力", "ハイネケン",
    # 嘉士伯 Carlsberg
    "carlsberg", "嘉士伯", "カールスバーグ",
    # 星巴克 Starbucks
    "starbucks", "星巴克", "スターバックス",
    # 麦当劳 McDonald's
    "mcdonald", "麦当劳", "マクドナルド",
    # 肯德基 KFC
    "kfc", "肯德基", "ケンタッキー",
    # 汉堡王 Burger King
    "burger king", "汉堡王", "バーガーキング",
    # 红牛 Red Bull
    "red bull", "红牛", "レッドブル",
    # 怪兽 Monster
    "monster beverage", "monster energy", "モンスター",
    # 汉高 Henkel（部分食品业务）
    # 金宝汤 Campbell's
    "campbell", "campbell soup", "金宝汤", "キャンベル",
    # 家乐 Home/Knorr (Unilever旗下)
    "knorr", "家乐",
    # 好时 Hershey
    "hershey", "好时", "ハーシー",
    # 王子饼干 Yamazaki
    "yamazaki", "王子", "ヤマザキ", "山崎製パン",
    # 乐事 Lay's (PepsiCo旗下) — 注意必须带引号避免子串误匹配
    "lay's", "乐事",
    # 多芬 Dove (Unilever旗下食品)
    # 宝洁 P&G（部分食品业务已出售）
    # 惠氏 Wyeth (Nestlé旗下)
    # 雅培 Abbott（营养品业务）
    "abbott", "雅培", "アボット",
    # GSK 营养品
    # 美赞臣 Mead Johnson (Reckitt旗下)
    # 惠灵顿 Wellington
    # ── 食品配料/原料巨头 ──
    # Chr. Hansen (现在属于Novonesis)
    "chr. hansen", "chr hansen", "科汉森", "novonesis",
    # Givaudan 奇华顿
    "givaudan", "奇华顿", "ジヴァダン",
    # IFF 国际香精香料
    "iff", "international flavors", "国际香精香料",
    # Tate & Lyle 泰特莱尔
    "tate & lyle", "泰特莱尔",
    # Puratos 焙乐道
    "puratos", "焙乐道",
    # Kerry 凯瑞
    "kerry group", "kerry", "凯瑞",
    # Lesaffre 乐斯福
    "lesaffre", "乐斯福",
    # ── 餐饮连锁 ──
    # 味千拉面 Ajisen
    "ajisen", "味千",
    # 吉野家 Yoshinoya
    "yoshinoya", "吉野家", "よしのや",
    # 松屋 Matsuya
    "matsuya", "松屋", "マツヤ",
    # 鼎泰丰 Din Tai Fung
    "din tai fung", "鼎泰丰",
    # 海底捞 Haidilao
    "haidilao", "海底捞", "ハイディラオ",
    # 喜茶 Heytea
    "heytea", "喜茶",
    # 奈雪的茶 Nayuki
    "nayuki", "奈雪",
    # 蜜雪冰城 Mixue
    "mixue", "蜜雪冰城",
    # 瑞幸 Luckin
    "luckin", "瑞幸", "ラッキン",
    # ── 超市/渠道（食品零售巨头）──
    # 沃尔玛 Walmart
    "walmart", "沃尔玛", "ウォルマート",
    # 7-Eleven
    "7-eleven", "7-11", "セブン-イレブン",
    # 全家 FamilyMart
    "familymart", "全家", "ファミリーマート",
    # LAWSON 罗森
    "lawson", "罗森", "ローソン",
    # Amazon Fresh
    "amazon fresh",
    # Aldi
    "aldi",
    # Lidl
    "lidl",
    # Costco
    "costco", "好市多",
    # Trader Joe's
    "trader joe",
    # Carrefour 家乐福
    "carrefour", "家乐福", "カルフール",
    # 永旺 Aeon（已在日本列表）
    # 伊藤洋华堂 Ito-Yokado
    "ito-yokado", "イトーヨーカドー",
]

# ── 食品饮料行业过滤关键词 ──────────────────────────────────────
# 判断文章是否属于食品饮料行业：标题或摘要命中任意关键词 → 保留
# 或者命中食品饮料企业名称 → 保留
# 未命中任何关键词或企业名称 → 过滤掉（非食品饮料资讯不收录）
FOOD_BEV_RELEVANCE_KEYWORDS = [
    # ── 英文：食品饮料品类 ──
    "food", "beverage", "drink", "snack", "meal", "dining", "restaurant",
    "cuisine", "cooking", "bakery", "bread", "chocolate", "candy",
    "confectionery", "meat", "poultry", "seafood", "vegetable", "fruit",
    "grain", "rice", "wheat", "cereal", "pasta", "noodle", "soup", "sauce",
    "condiment", "seasoning", "flavor", "flavour", "taste", "texture",
    "aroma", "recipe",
    # ── 英文：饮料品类 ──
    "soda", "juice", "water", "beer", "wine", "spirits", "coffee", "tea",
    "milk", "dairy", "cocktail", "smoothie", "energy drink", "soft drink",
    "brewery", "brewing", "distillery", "alcohol", "alcoholic",
    "carbonated", "sparkling water", "mineral water", "fermented",
    # ── 英文：食品行业术语 ──
    "food industry", "beverage industry", "food tech", "food innovation",
    "food safety", "food regulation", "food processing", "food manufacturing",
    "food packaging", "ingredient", "ingredients", "nutrition", "nutritional",
    "functional food", "health food", "organic food", "plant-based",
    "vegan", "vegetarian", "alternative protein", "lab-grown",
    "cultivated meat", "cell-based", "fmcg", "cpg", "supply chain",
    "sustainable packaging", "e-commerce", "dtc", "retail", "grocery",
    "supermarket", "convenience store", "vending",
    # ── 英文：食品饮料品牌名（行业新闻高频提及）──
    "asahi", "suntory", "kirin", "coca-cola", "pepsi", "nestle", "nestlé",
    "mondelez", "kraft", "unilever", "mars", "danone", "ab inbev",
    "heineken", "carlsberg", "mcdonald", "starbucks", "kfc",
    "cargill", "adm", "dsm", "fonterra", "ingredion",
    # ── 日文：食品核心词 ──
    "食品", "飲料", "飲食", "お菓子", "菓子", "和菓子", "洋菓子",
    "チョコレート", "キャンディ", "パン", "調味料", "スープ", "カレー",
    "米", "麺", "麦", "肉", "魚", "野菜", "果物", "豆", "乳",
    "缶詰", "冷凍食品", "レトルト", "弁当",
    # ── 日文：饮料品类 ──
    "清涼飲料", "ビール", "サワー", "ワイン", "カクテル",
    "コーヒー", "紅茶", "緑茶", "牛乳", "乳製品",
    "ソフトドリンク", "アルコール", "酒", "日本酒", "焼酎",
    "ハイボール", "缶コーヒー", "炭酸", "発泡",
    "スポーツドリンク", "ミネラルウォーター",
    # ── 日文：食品行业高频词 ──
    "食品業界", "食品産業", "飲料業界", "食品安全", "食品規制",
    "食品加工", "食品製造", "食材", "栄養", "健康食品",
    "有機", "オーガニック", "プラントベース", "ヴィーガン",
    "代替肉", "大豆肉", "食感", "外食", "中食", "コンビニ",
    "フードテック", "新商品", "新製品", "新飲料", "新フレーバー",
    "発売", "コラボ", "限定", "キャンペーン", "パッケージ",
    "機能性表示", "特定保健用食品",
    # ── 中文：食品饮料核心词 ──
    "食品行业", "饮料行业", "餐饮", "零食", "甜品", "糕点",
    "面包", "巧克力", "糖果", "调味料", "方便食品", "冷冻食品",
    "啤酒", "白酒", "红酒", "茶饮", "咖啡", "牛奶", "酒类",
    "果汁", "碳酸饮料", "乳制品", "饮品", "原料", "营养",
    "健康食品", "有机食品", "植物基", "代餐", "外卖",
    "便利店", "新品", "联名", "限定", "包装", "配方",
    # ── 食品饮料品类大词 ──
    "sour", "cola", "lemon", "orange", "apple", "berry", "mango",
    "strawberry", "peach", "grape", "vanilla", "caramel", "matcha",
    "抹茶", "レモン", "オレンジ", "マンゴー", "イチゴ", "もも",
    "葡萄", "バニラ", "キャラメル", "コーラ",
]

# ── 食品饮料行业排除关键词 ──────────────────────────────────────
# 即使命中食品关键词，如果同时命中排除关键词 → 过滤掉
# （避免把"药品含食品添加剂"这类非食品文章收录）
FOOD_BEV_EXCLUDE_KEYWORDS = [
    # 药品/医疗（除非是功能性食品/保健品）
    "医薬品", "医薬", "処方", "診療", "病院", "患者", "治療",
    "clinical", "prescription", "pharmaceutical", "drug", "medicine",
    "hospital", "patient", "treatment", "diagnosis",
    # IT/科技（非食品领域）
    "software", "app store", "ai model", "cloud computing",
    "semiconductor", "chip design", "blockchain", "crypto",
    "半導体", "ブロックチェーン", "暗号資産",
    "iphone", "ipad", "macbook", "ios", "mac os", "apple watch",
    # 汽车/交通
    "automotive", "car model", "vehicle", "electric vehicle", "ev",
    "自動車", "車種", "電気自動車", "ev車",
    # 房产/建筑
    "real estate", "property market", "housing", "construction",
    "不動産", "住宅", "建設", "マンション",
    # 金融/投资（纯金融不涉及食品企业）
    "stock market", "interest rate", "bond", "currency",
    "株式市場", "金利", "債券", "為替",
    # 体育/娱乐
    "olympic", "world cup", "football", "soccer", "baseball",
    "オリンピック", "ワールドカップ", "サッカー", "野球",
    "映画", "ドラマ", "アニメ", "music", "concert",
    # 服装/时尚
    "fashion", "apparel", "clothing", "luxury brand",
    "ファッション", "アパレル", "服", "ハイブランド",
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
