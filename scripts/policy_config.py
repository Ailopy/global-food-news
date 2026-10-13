# -*- coding: utf-8 -*-
"""
policy_config.py — 食品政策监控配置
数据源：食品伙伴网（law.foodmate.net / down.foodmate.net）
分级标准：S+ > S > A > B（与前端 policy_levels 对应）
"""
import re

# ── 数据源（列表页）────────────────────────────────────────
POLICY_SOURCES = [
    {"name": "法规中心·最新",  "url": "https://law.foodmate.net/",                 "type": "law"},
    {"name": "法规中心·草案",  "url": "https://law.foodmate.net/draft/",           "type": "draft"},
    {"name": "标准中心·动态",  "url": "https://down.foodmate.net/info/sort/1/",     "type": "std"},
    {"name": "标准中心·公告",  "url": "https://down.foodmate.net/info/sort/2/",     "type": "std"},
]

RETENTION_DAYS = 7      # 保留窗口（天）
MAX_ITEMS = 30          # 单次输出上限
ABSTRACT_MAX = 200      # 摘要截断长度

# ── 国家级发文机构 ─────────────────────────────────────────
NATIONAL_AUTHORITIES = [
    "市场监管总局", "国家市场监督管理总局", "市场监管总局办公厅",
    "国家卫生健康委", "国家卫生健康委员会", "卫健委", "国务院",
    "国家发展改革委", "国家发展和改革委员会", "发改委",
    "工业和信息化部", "工信部", "海关总署", "商务部",
    "国家标准化管理委员会", "国标委", "国务院食品安全办", "国务院食安办",
    "国家粮食和物资储备局", "国家食品安全风险评估中心", "农业农村部",
    "国家药监局", "教育部", "财政部",
]

# 食品监管核心部委（其发文默认视为食品相关政策）
FOOD_AUTHORITIES = [
    "市场监管总局", "国家市场监督管理总局", "市场监管总局办公厅",
    "国家卫生健康委", "国家卫生健康委员会", "卫健委",
    "农业农村部", "国家标准化管理委员会", "国标委",
    "国家食品安全风险评估中心", "国家粮食和物资储备局",
    "国务院食品安全办", "国务院食安办", "商务部",
]

# ── 食品语境关键词（强相关，命中即收录）──────────────────
FOOD_CONTEXT_KWS = [
    "食品", "食用", "农产", "畜牧", "兽医", "渔业", "水产", "肉", "蛋",
    "奶", "乳", "粮", "油", "调味", "饮料", "酒", "茶", "罐头", "烘焙",
    "餐饮", "添加剂", "营养", "保健", "婴幼", "特殊医学", "零食", "预制",
    "冷链", "屠宰", "生猪", "禽", "食品安全", "食物",
]

# ── 弱语境（农业/粮食/标准/计量等，需叠加食品关联词）──────
WEAK_CONTEXT_KWS = [
    "农业", "粮食", "国家计量", "计量器具", "标准化", "国家标准",
    "农产品", "植物新品种", "作物", "种植", "农村",
]

# ── 食品关联词（与弱语境叠加判定）──────────────────────────
FOOD_TIE_KWS = [
    "食品", "食用", "粮", "油", "肉", "蛋", "奶", "乳", "水产", "屠宰",
    "烹", "配料", "添加剂", "饮", "酒", "茶", "调味", "禽", "农产",
    "营养", "餐", "包装", "保鲜", "冷藏", "贮藏",
]

# ── S+ 信号 ────────────────────────────────────────────────
S_PLUS_PATTERNS = [
    r"十五五",                                                        # 现行五年规划
    r"(首个|首部|首份|第一部).{0,14}(强制性|国家标准|国标|规划|条例|管理办法|规范)",
    r"(联合印发|联合发布|联合公告|三部委|多部门联合)",
]

# ── S 级：国家级正式文件用语 ───────────────────────────────
S_DOC_KWS = [
    "令", "规章", "公告", "强制性国家标准", "GB", "国家标准", "国标",
    "办法", "条例", "规划", "细则", "规定", "标准立项", "立项计划",
    "风险管控清单", "注册", "监督管理", "管理规定", "实施意见",
    "通知", "指引", "通则", "复函", "审查细则",
]

# ── A 级：地方/行业文件用语 ────────────────────────────────
LOCAL_KWS = [
    "省", "市", "自治区", "地方", "地方标准", "团体标准", "行业标准",
    "解读", "问答", "释义", "答复", "协会",
]
A_DOC_KWS = [
    "条例", "办法", "规定", "指引", "方案", "规划", "标准", "意见",
    "通知", "指南", "措施", "管理", "草案", "征求意见", "试行",
]

# ── 排除（非政策正文）──────────────────────────────────────
EXCLUDE_TITLE_KWS = [
    "培训", "研修", "会议", "论坛", "峰会", "展会", "展览", "招聘",
    "报名", "课程", "沙龙", "研讨", "竞赛", "征稿", "招商", "展位",
    "参观", "考察", "直播", "答谢", "促销", "优惠", "邀请函",
    "动态回顾", "周报", "周刊", "月报", "速览", "盘点", "合集", "汇总",
    "抽奖", "问卷", "满意度",
]

# ── 非食品饮料领域排除 ─────────────────────────────────────
EXCLUDE_DOMAIN_KWS = [
    "化妆品", "饲料", "兽药", "宠物食品", "农业机械", "烟草",
]


def doc_authority(title: str) -> str:
    for a in NATIONAL_AUTHORITIES:
        if a in title:
            return a
    return ""


def is_food_context(title: str) -> bool:
    return any(k in title for k in FOOD_CONTEXT_KWS)


def should_keep(title: str) -> bool:
    """是否纳入食品政策板块（必须食品强相关）"""
    if not title or len(title) < 8:
        return False
    if any(k in title for k in EXCLUDE_TITLE_KWS):
        return False
    if any(k in title for k in EXCLUDE_DOMAIN_KWS):
        return False
    # 食品强语境：与民生/产业强相关
    if is_food_context(title):
        return True
    # 弱语境（农业/粮食/标准）需叠加食品关联词
    if any(k in title for k in WEAK_CONTEXT_KWS) and any(k in title for k in FOOD_TIE_KWS):
        return True
    return False


def is_national(title: str) -> bool:
    """是否国家级发文（非地方）"""
    return bool(doc_authority(title))


def doc_level(title: str, abstract: str = ""):
    """判定政策级别，返回 (level, reason)"""
    t = title
    food = is_food_context(t)
    national = is_national(t)

    # 1) S+：国家级五年规划（限食品）/ 首创重大政策 / 多部委联合
    if re.search(r"十五五", t) and food and national:
        return "S+", "食品行业‘十五五’规划信号，行业顶层风向标"
    if re.search(r"(首个|首部|首份|第一部).{0,14}(强制性|国家标准|国标|规划|条例|管理办法|规范)", t) and food:
        return "S+", "国家级‘首个/首部’重大政策，具行业里程碑意义"
    if re.search(r"(联合印发|联合发布|联合公告|三部委|多部门联合)", t) and food:
        return "S+", "多部委联合发文，行业重大政策信号"

    # 2) S：国家级部委正式文件（须与食品相关；弱语境需叠加食品关联词）
    food_related = food or any(k in t for k in FOOD_TIE_KWS)
    if national and food_related:
        if any(k in t for k in S_DOC_KWS):
            return "S", f"国家级主管部门（{doc_authority(t)}）发布正式规章/标准/公告，全行业适用"
        return "A", f"国家级主管部门（{doc_authority(t)}）发布政策动态，具全国指引意义"

    # 3) 团体标准（协会级）→ B
    if "团体标准" in t:
        return "B", "行业协会团体标准发布/立项，常规参考"

    # 4) A：地方条例/地方标准/权威解读
    if any(k in t for k in LOCAL_KWS) and any(k in t for k in A_DOC_KWS):
        return "A", "地方/行业层重要政策动态，具区域或行业参考价值"

    # 5) B：常规动态
    return "B", "常规性政策动态/配套通知"
