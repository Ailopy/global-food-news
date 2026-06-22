/**
 * app.js — 全球食品资讯聚合前端逻辑 v4
 * 新增：地区筛选、品类筛选、数据统计面板、推荐选题Tab（视频栏目选题体系）
 */

// ── 视频栏目选题配置（对应 Foodaily 视频选题计划）─────────────
// maxItems: 该方向展示的最多条数（权重越高展示越多）
// priorityKeywords: 高权重词，命中 +10 分；keywords: 普通词，命中 +1 分
const TOPIC_CONFIGS = [
  // ══════════════════════════════════════════════════════════
  // 栏目一：全球创新品鉴（占比 80%）—— 展示 5 条
  // 子方向：①巨头新品爆品 ②国内新品渠道爆品 ③品牌潮趣营销 ④宝藏食材
  // ══════════════════════════════════════════════════════════
  {
    id: "global-innovation",
    icon: "🌟",
    title: "全球创新品鉴",
    badge: "每日必看 · 占比 80%",
    desc: "新产品 · 新技术 · 新原料 · 新包装 · 新营销 ｜ 巨头爆品 / 国内爆品 / 品牌潮趣 / 宝藏食材",
    color: "#c7521a",
    bgColor: "#fff5ef",
    maxItems: 5,
    // ── ①巨头新品 & 爆品（日韩/北美/欧洲/澳洲/东南亚）
    priorityKeywords: [
      "new product", "new flavor", "new launch", "launches", "new range",
      "limited edition", "limited-edition", "bestseller", "best seller",
      "top selling", "record sales", "sold out",
      "new formula", "reformulation", "new recipe",
      // 巨头品牌
      "nestle", "nestlé", "unilever", "pepsico", "pepsi", "coca-cola", "coca cola",
      "mondelez", "kellogg", "kellanova", "general mills", "mars", "danone",
      "campbell", "kraft heinz", "conagra", "tyson", "jbs",
      "meiji", "morinaga", "glico", "calbee", "nissin", "kirin", "suntory",
      "lotte", "orion", "ottogi", "nong shim", "nongshim", "cj cheiljedang",
      "ferrero", "lindt", "haribo", "ritter sport", "bahlsen",
      "arnotts", "fonterra", "sanitarium",
      // 营销爆款
      "collab", "collaboration", "limited", "co-branding", "联名",
      "viral", "trending", "gone viral", "social media", "tiktok",
      "brand campaign", "罪恶营销", "guilty", "indulgence",
      // 宝藏食材 / 社媒爆品
      "superfood", "trending ingredient", "exotic ingredient",
      "yuzu", "柚子", "matcha", "抹茶", "miso", "味噌",
      "butter mochi", "黄油年糕", "tahini", "芝麻酱", "ube", "紫薯",
      "adaptogen", "mushroom coffee", "lion's mane", "chaga",
      "moringa", "ashwagandha", "sea moss", "spirulina",
      "trending food", "food trend", "hot product"
    ],
    keywords: [
      // 通用新品词
      "launch", "introduce", "debut", "unveil", "release", "rollout",
      "product innovation", "innovation", "ingredient innovation",
      "new packaging", "new design", "rebrand", "relaunch",
      // 国内渠道爆品
      "sam's club", "sams club", "山姆", "costco", "盒马", "hema",
      "aldi", "奥乐齐", "trader joe", "target", "walmart",
      "抖音", "douyin", "小红书", "xiaohongshu", "直播带货",
      // 包装 / 设计
      "packaging", "package design", "new packaging", "packaging innovation",
      "sustainable packaging", "eco-friendly", "biodegradable",
      "refill", "recyclable", "clean label",
      // 区域市场
      "japan", "japanese", "korea", "korean", "australia", "australian",
      "europe", "european", "uk", "southeast asia", "southeast asian",
      // 产品形态
      "snack", "beverage", "drink", "chocolate", "candy", "confectionery",
      "dairy", "yogurt", "ice cream", "frozen", "bakery", "biscuit",
      "noodle", "sauce", "condiment", "seasoning", "protein bar",
      "energy drink", "functional drink", "health food", "organic",
      // 技术 / 原料
      "fermentation", "precision fermentation", "biotech",
      "plant-based", "plant based", "alternative protein",
      "probiotic", "prebiotic", "postbiotic", "gut health",
      "collagen", "protein", "fiber", "omega", "vitamin",
      "zero sugar", "no sugar", "low calorie", "natural flavor",
      "non-gmo", "gluten-free", "vegan", "keto", "paleo"
    ]
  },

  // ══════════════════════════════════════════════════════════
  // 栏目二：新XIU — 增长解构（占比 10%）—— 展示 2 条
  // 企业/品牌商战 + 出海策略增长拆解
  // ══════════════════════════════════════════════════════════
  {
    id: "growth-decode",
    icon: "📈",
    title: "新XIU · 增长解构",
    badge: "品牌增长拆解 · 占比 10%",
    desc: "企业商战 · 出海策略 · 增长关键点拆解 · 国内市场可复制性分析",
    color: "#1a6b8a",
    bgColor: "#e0f4fb",
    maxItems: 2,
    priorityKeywords: [
      // 商战 / 增长
      "market share", "record revenue", "record sales", "fastest growing",
      "overtake", "surpass", "number one", "market leader",
      "turnaround", "comeback", "revival", "reinvention",
      "brand strategy", "growth strategy", "success story",
      // 出海
      "export", "global expansion", "international", "overseas",
      "enter market", "market entry", "cross-border", "go global",
      "lotus biscoff", "lotus", "biscoff",
      // 案例型词
      "how", "why", "key to", "secret", "case study", "analysis",
      "brand story", "behind the brand"
    ],
    keywords: [
      "growth", "revenue", "profit", "sales", "performance", "earnings",
      "expansion", "scale", "category", "penetration",
      "rebranding", "repositioning", "pivot", "innovation strategy",
      "consumer insight", "consumer behavior", "market trend",
      "disruption", "disruptor", "challenger brand",
      "partnership", "distribution", "retail expansion",
      "japan expansion", "korea market", "china market",
      "premium", "premiumization", "trading up", "value",
      "subscription", "loyalty", "community", "brand equity"
    ]
  },

  // ══════════════════════════════════════════════════════════
  // 栏目三：赛道新物种（占比 5%）—— 展示 2 条
  // 行业新品类、新赛道、新机遇
  // ══════════════════════════════════════════════════════════
  {
    id: "new-category",
    icon: "🔬",
    title: "赛道新物种",
    badge: "新品类 · 新赛道 · 占比 5%",
    desc: "行业潜力赛道 · 新品类机遇 · 清洁标签 / 康普茶 / 功能性食品等前沿方向",
    color: "#7c3aed",
    bgColor: "#f0edfb",
    maxItems: 2,
    priorityKeywords: [
      // 功能性 / 健康
      "clean label", "clean-label", "kombucha", "kefir",
      "functional food", "functional beverage", "nutraceutical",
      "nootropic", "cognitive", "stress relief", "mood",
      "sleep aid", "beauty from within", "skin health",
      "immunity", "immune support", "longevity", "anti-aging",
      "personalized nutrition", "precision nutrition",
      // 新品类
      "emerging category", "new category", "rising category",
      "trending category", "white space", "niche market",
      "category creator", "category disruptor",
      // 植物基 / 替代蛋白
      "cultivated meat", "lab-grown", "cell-based", "mycoprotein",
      "insect protein", "single-cell protein"
    ],
    keywords: [
      "probiotic", "prebiotic", "postbiotic", "gut health",
      "plant-based", "plant based", "vegan", "vegetarian",
      "fermented", "fermentation", "live cultures",
      "adaptogen", "ashwagandha", "rhodiola", "lion's mane",
      "collagen", "peptide", "amino acid", "electrolyte",
      "hydration", "sports nutrition", "performance",
      "RTD", "ready to drink", "grab and go",
      "organic", "natural", "non-gmo", "regenerative",
      "sustainable", "carbon neutral", "zero waste",
      "upcycled", "circular economy",
      "trend report", "market report", "forecast", "future of food"
    ]
  },

  // ══════════════════════════════════════════════════════════
  // 栏目四：商业新知（占比 5%）—— 展示 2 条
  // 政策、投融资、渠道变革、食品安全
  // ══════════════════════════════════════════════════════════
  {
    id: "biz-news",
    icon: "📰",
    title: "商业新知",
    badge: "行业动态 · 占比 5%",
    desc: "重磅政策 · 投融资 · 全球巨头并购 · 渠道变革 · 食品安全快讯",
    color: "#374151",
    bgColor: "#f3f4f6",
    maxItems: 2,
    priorityKeywords: [
      // 并购 / 融资
      "acquisition", "acquires", "acquired", "merger", "m&a",
      "funding", "investment", "series a", "series b", "series c",
      "ipo", "goes public", "listing", "valuation",
      "raises", "secures funding", "venture capital", "private equity",
      // 政策 / 监管
      "regulation", "regulatory", "fda", "efsa", "food safety authority",
      "ban", "recall", "warning", "violation", "penalty",
      "new regulation", "policy", "legislation", "standard",
      "approved", "approval", "authorized", "certified",
      // 渠道变革
      "don quijote", "donki", "唐吉坷德",
      "trader joe", "缺德舅", "costco", "aldi", "lidl",
      "convenience store", "drug store", "pharmacy",
      "e-commerce", "online grocery", "delivery", "quick commerce",
      // 食品安全
      "food safety", "contamination", "outbreak", "listeria",
      "salmonella", "recall notice", "allergen", "undeclared"
    ],
    keywords: [
      "invest", "deal", "transaction", "stake", "shares",
      "revenue", "profit", "loss", "quarterly", "annual",
      "ceo", "executive", "appoint", "resign", "leadership",
      "partnership", "joint venture", "license", "franchise",
      "export", "import", "tariff", "trade",
      "supply chain", "shortage", "inflation", "cost",
      "retail", "channel", "distribution", "wholesale",
      "market", "industry", "sector", "category",
      "report", "survey", "data", "statistics", "forecast",
      "sustainability", "ESG", "carbon", "emission"
    ]
  }
];

// ── 计算文章与选题方向的匹配分 ────────────────────────────────
function topicMatchScore(art, config) {
  const text = ((art.title || "") + " " + (art.summary || "")).toLowerCase();
  let score = 0;
  for (const kw of (config.priorityKeywords || [])) {
    if (text.includes(kw.toLowerCase())) score += 10;
  }
  for (const kw of (config.keywords || [])) {
    if (text.includes(kw.toLowerCase())) score += 1;
  }
  return score;
}

const DATA_URL        = "./data/news_latest.json";
const GIANTS_DATA_URL = "./data/news_giant_brands.json";
const STOPICS_DATA_URL = "./data/news_s_topics.json";
const PAGE_SIZE  = 24;
const DEBOUNCE_MS = 220;

const LANG_LABEL = { en: "EN", zh: "中文", ja: "日本語", ko: "한국어", fr: "Français" };

// 地区 emoji 映射
const REGION_ICON = {
  "北美": "🇺🇸", "欧洲": "🇪🇺", "日本": "🇯🇵", "亚太": "🌏",
  "全球": "🌐", "欧美": "🌍", "意大利": "🇮🇹", "美国": "🇺🇸"
};

// 品类颜色
const CATEGORY_COLOR = {
  "综合": "#2d7d46", "功能性食品": "#7c3aed", "饮料": "#1a6b8a",
  "乳制品": "#d97706", "烘焙&零食": "#b45309", "糕点糖巧": "#9d174d",
  "糖巧&零食": "#9d174d", "原辅料": "#065f46"
};

// 来源颜色哈希
const SOURCE_COLORS = [
  "#2d7d46","#1a6b8a","#7c3aed","#b45309",
  "#1d4ed8","#9d174d","#065f46","#7f1d1d",
  "#0f766e","#92400e","#1e40af","#6b21a8"
];
function sourceColor(name) {
  let h = 0;
  for (let i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) | 0;
  return SOURCE_COLORS[Math.abs(h) % SOURCE_COLORS.length];
}

// ── 状态 ──────────────────────────────────────────────────────
let allArticles      = [];
let filteredArts     = [];
let activeSourcesSet = new Set();
let activeRegions    = new Set();
let activeCategories = new Set();
let searchKeyword    = "";
let currentPage      = 1;
let isListView       = false;
let allRegions       = [];
let allCategories    = [];
let activeTab        = "all";   // "all" | "topics" | "giants" | "stopics"
let allGiantArticles = [];
let giantBrandsActive = new Set();
let giantRegionsActive = new Set();
let allSTopicsArticles = [];
let sTopicsSitesActive = new Set();
let sTopicsRegionsActive = new Set();

// ── DOM ───────────────────────────────────────────────────────
const grid           = document.getElementById("articlesGrid");
const emptyState     = document.getElementById("emptyState");
const loadingState   = document.getElementById("loadingState");
const loadMoreWrap   = document.getElementById("loadMoreWrap");
const loadMoreBtn    = document.getElementById("loadMoreBtn");
const sourceFilters  = document.getElementById("sourceFilters");
const searchInput    = document.getElementById("searchInput");
const clearSearchBtn = document.getElementById("clearSearch");
const updateTimeText = document.getElementById("updateTimeText");
const statsText      = document.getElementById("statsText");
const backToTop      = document.getElementById("backToTop");
const selectAllBtn   = document.getElementById("selectAll");
const clearAllBtn    = document.getElementById("clearAll");
const viewGridBtn    = document.getElementById("viewGrid");
const viewListBtn    = document.getElementById("viewList");
// 新增 DOM（地区/品类）
const regionFilters  = document.getElementById("regionFilters");
const categoryFilters= document.getElementById("categoryFilters");

// Tab DOM
const tabBar         = document.getElementById("tabBar");
const tabAllBtn      = document.getElementById("tabAll");
const tabTopicsBtn   = document.getElementById("tabTopics");
const tabGiantsBtn   = document.getElementById("tabGiants");
const tabSTopicsBtn  = document.getElementById("tabSTopics");
const mainContent  = document.getElementById("main");

// ── 时间格式化 ─────────────────────────────────────────────────
function formatTime(isoStr) {
  if (!isoStr) return "时间未知";
  try {
    const diff = Math.floor((Date.now() - new Date(isoStr).getTime()) / 1000);
    if (diff < 0)       return formatDate(isoStr);
    if (diff < 60)      return `${diff}秒前`;
    if (diff < 3600)    return `${Math.floor(diff / 60)}分钟前`;
    if (diff < 86400)   return `${Math.floor(diff / 3600)}小时前`;
    if (diff < 172800)  return "昨天";
    return formatDate(isoStr);
  } catch { return ""; }
}
function formatDate(isoStr) {
  const d = new Date(isoStr);
  return `${String(d.getMonth()+1).padStart(2,"0")}-${String(d.getDate()).padStart(2,"0")}`;
}

// ── 高亮关键词 ─────────────────────────────────────────────────
function highlight(text, kw) {
  if (!kw || !text) return text || "";
  const escaped = kw.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return text.replace(new RegExp(escaped, "gi"), m => `<mark>${m}</mark>`);
}
function truncate(text, len) {
  return !text ? "" : text.length > len ? text.slice(0, len) + "…" : text;
}

// ── 渲染卡片 ───────────────────────────────────────────────────
function renderCard(art, kw, idx) {
  const title   = highlight(art.title   || "（无标题）", kw);
  const summary = highlight(truncate(art.summary || "", 180), kw);
  const timeStr = formatTime(art.published_at);
  const color   = sourceColor(art.source);
  const regionIcon = REGION_ICON[art.region] || "🌐";
  const catColor   = CATEGORY_COLOR[art.category] || "#2d7d46";
  const langLabel  = LANG_LABEL[art.language] || (art.language || "").toUpperCase();
  const animDelay  = `animation-delay:${(idx % PAGE_SIZE) * 30}ms`;

  return `
  <article class="card" style="${animDelay}" data-id="${art.id}">
    <div class="card-header">
      <span class="source-tag" style="background:${color}20;color:${color};border-color:${color}40">${art.source}</span>
      <div class="card-meta-right">
        <span class="region-tag">${regionIcon} ${art.region || ""}</span>
        ${art.category ? `<span class="cat-tag" style="color:${catColor}">${art.category}</span>` : ""}
        <span class="lang-tag">${langLabel}</span>
      </div>
    </div>
    <h2 class="card-title">
      <a href="${art.url}" target="_blank" rel="noopener noreferrer">${title}</a>
    </h2>
    ${summary ? `<p class="card-summary">${summary}</p>` : ""}
    <div class="card-footer">
      <span class="time-badge" title="${art.published_at}">
        <svg viewBox="0 0 16 16" fill="currentColor" width="12" height="12"><path d="M8 1a7 7 0 100 14A7 7 0 008 1zM0 8a8 8 0 1116 0A8 8 0 010 8zm8-3.5a.5.5 0 01.5.5v3.25l2.25 1.3a.5.5 0 01-.5.866L7.5 8.866V5a.5.5 0 01.5-.5z"/></svg>
        ${timeStr}
      </span>
      <a href="${art.url}" target="_blank" rel="noopener noreferrer" class="read-btn">
        阅读原文
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="13" height="13">
          <path d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
      </a>
    </div>
  </article>`;
}

// ── 渲染分页 ───────────────────────────────────────────────────
function renderPage() {
  const end = currentPage * PAGE_SIZE;
  const visible = filteredArts.slice(0, end);

  if (visible.length === 0) {
    grid.innerHTML = "";
    emptyState.classList.remove("hidden");
    loadMoreWrap.classList.add("hidden");
    updateStats(0);
    return;
  }

  emptyState.classList.add("hidden");
  grid.innerHTML = visible.map((art, i) => renderCard(art, searchKeyword, i)).join("");

  if (filteredArts.length > end) {
    loadMoreWrap.classList.remove("hidden");
    loadMoreBtn.textContent = `加载更多（剩余 ${filteredArts.length - end} 条）`;
  } else {
    loadMoreWrap.classList.add("hidden");
  }
  updateStats(filteredArts.length);
}

function updateStats(count) {
  const total = allArticles.length;
  const isFiltered = searchKeyword || activeSourcesSet.size < allArticles.length
    || activeRegions.size < allRegions.length || activeCategories.size < allCategories.length;
  statsText.textContent = isFiltered
    ? `筛选结果：${count} 条 / 共 ${total} 条`
    : `共 ${total} 条资讯，近 7 天`;
}

// ── 筛选逻辑 ───────────────────────────────────────────────────
function applyFilters() {
  const kw = searchKeyword.toLowerCase();
  filteredArts = allArticles.filter(art => {
    if (!activeSourcesSet.has(art.source)) return false;
    if (art.region    && activeRegions.size    > 0 && !activeRegions.has(art.region))    return false;
    if (art.category  && activeCategories.size > 0 && !activeCategories.has(art.category)) return false;
    if (kw) {
      const inTitle   = (art.title   || "").toLowerCase().includes(kw);
      const inSummary = (art.summary || "").toLowerCase().includes(kw);
      if (!inTitle && !inSummary) return false;
    }
    return true;
  });
  currentPage = 1;
  renderPage();
}

// ── 构建筛选 Chips ─────────────────────────────────────────────
function buildSourceChips(sources) {
  activeSourcesSet = new Set(sources);
  sourceFilters.innerHTML = "";
  sources.forEach(src => {
    const chip = document.createElement("button");
    chip.className = "chip active";
    chip.dataset.source = src;
    chip.innerHTML = `<span class="chip-dot" style="background:${sourceColor(src)}"></span>${src}`;
    chip.addEventListener("click", () => {
      const active = activeSourcesSet.has(src);
      active ? activeSourcesSet.delete(src) : activeSourcesSet.add(src);
      chip.classList.toggle("active", !active);
      applyFilters();
    });
    sourceFilters.appendChild(chip);
  });
}

function buildRegionChips(regions) {
  allRegions = regions;
  activeRegions = new Set(regions);
  if (!regionFilters) return;
  regionFilters.innerHTML = "";
  regions.forEach(r => {
    const chip = document.createElement("button");
    chip.className = "chip active chip-region";
    chip.dataset.region = r;
    const icon = REGION_ICON[r] || "🌐";
    chip.innerHTML = `${icon} ${r}`;
    chip.addEventListener("click", () => {
      const active = activeRegions.has(r);
      active ? activeRegions.delete(r) : activeRegions.add(r);
      chip.classList.toggle("active", !active);
      applyFilters();
    });
    regionFilters.appendChild(chip);
  });
}

function buildCategoryChips(categories) {
  allCategories = categories;
  activeCategories = new Set(categories);
  if (!categoryFilters) return;
  categoryFilters.innerHTML = "";
  categories.forEach(cat => {
    const chip = document.createElement("button");
    chip.className = "chip active chip-category";
    chip.dataset.category = cat;
    const color = CATEGORY_COLOR[cat] || "#2d7d46";
    chip.style.setProperty("--cat-color", color);
    chip.innerHTML = cat;
    chip.addEventListener("click", () => {
      const active = activeCategories.has(cat);
      active ? activeCategories.delete(cat) : activeCategories.add(cat);
      chip.classList.toggle("active", !active);
      applyFilters();
    });
    categoryFilters.appendChild(chip);
  });
}

// ── 数据加载 ───────────────────────────────────────────────────
async function loadData() {
  loadingState.classList.remove("hidden");
  grid.innerHTML = "";

  try {
    const resp = await fetch(`${DATA_URL}?t=${Date.now()}`);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const data = await resp.json();

    allArticles = data.articles || [];

    // 更新时间
    if (data.last_updated) {
      const d = new Date(data.last_updated);
      updateTimeText.textContent = `最后更新：${String(d.getMonth()+1).padStart(2,"0")}-${String(d.getDate()).padStart(2,"0")} ${String(d.getHours()).padStart(2,"0")}:${String(d.getMinutes()).padStart(2,"0")}`;
    }

    // 来源
    const sources = data.sources || [...new Set(allArticles.map(a => a.source))];
    buildSourceChips(sources);

    // 地区（从文章数据中提取）
    const regions = [...new Set(allArticles.map(a => a.region).filter(Boolean))].sort();
    buildRegionChips(regions);

    // 品类
    const categories = [...new Set(allArticles.map(a => a.category).filter(Boolean))].sort();
    buildCategoryChips(categories);

    // 统计面板更新
    updateSummaryPanel(allArticles, sources, regions);

    loadingState.classList.add("hidden");
    applyFilters();

  } catch (err) {
    console.error("加载数据失败:", err);
    loadingState.classList.add("hidden");
    grid.innerHTML = `
      <div style="grid-column:1/-1;text-align:center;padding:60px 24px;color:#7a9478;">
        <div style="font-size:3rem;margin-bottom:16px;">⚠️</div>
        <p style="font-weight:600;font-size:1rem;">资讯数据加载失败</p>
        <p style="font-size:.875rem;margin-top:8px;opacity:.8;">${err.message || "网络错误，请稍后刷新"}</p>
        <button onclick="loadData()" style="margin-top:20px;padding:8px 20px;background:#2d7d46;color:#fff;border:none;border-radius:20px;cursor:pointer;font-weight:600;">重新加载</button>
      </div>`;
  }
}

// ── 顶部统计面板 ──────────────────────────────────────────────
function updateSummaryPanel(articles, sources, regions) {
  const panel = document.getElementById("summaryPanel");
  if (!panel) return;
  panel.innerHTML = `
    <div class="summary-item">
      <span class="summary-num">${articles.length}</span>
      <span class="summary-label">近7天资讯</span>
    </div>
    <div class="summary-item">
      <span class="summary-num">${sources.length}</span>
      <span class="summary-label">活跃来源</span>
    </div>
    <div class="summary-item">
      <span class="summary-num">${regions.length}</span>
      <span class="summary-label">覆盖地区</span>
    </div>
    <div class="summary-item">
      <span class="summary-num">${countToday(articles)}</span>
      <span class="summary-label">今日更新</span>
    </div>
  `;
}

function countToday(articles) {
  const today = new Date();
  today.setHours(0,0,0,0);
  return articles.filter(a => {
    try { return new Date(a.published_at) >= today; } catch { return false; }
  }).length;
}

// ── 选题推荐渲染 ─────────────────────────────────────────────
function renderTopicsView() {
  const statsBar    = document.getElementById("statsBar");
  const articlesGrid = document.getElementById("articlesGrid");
  const emptyState  = document.getElementById("emptyState");
  const loadMoreWrap = document.getElementById("loadMoreWrap");
  if (statsBar) statsBar.style.display = "none";
  articlesGrid.innerHTML = "";
  emptyState.classList.add("hidden");
  loadMoreWrap.classList.add("hidden");

  if (allArticles.length === 0) {
    articlesGrid.innerHTML = `
      <div style="grid-column:1/-1;text-align:center;padding:60px 24px;color:#7a9478;">
        <div style="font-size:3rem;margin-bottom:16px;">📋</div>
        <p style="font-weight:600;font-size:1rem;">资讯加载中…</p>
        <p style="font-size:.875rem;margin-top:8px;opacity:.7;">数据加载完成后将显示选题推荐</p>
      </div>`;
    return;
  }

  // 今日资讯判断（用于加「今日」角标）
  const todayStart = new Date(); todayStart.setHours(0,0,0,0);
  function isToday(art) {
    try { return new Date(art.published_at) >= todayStart; } catch { return false; }
  }

  // 更新时间展示
  let lastUpdatedStr = "";
  if (allArticles.length > 0) {
    const times = allArticles.map(a => { try { return new Date(a.published_at).getTime(); } catch { return 0; }});
    const maxTs = Math.max(...times);
    if (maxTs > 0) {
      const d = new Date(maxTs);
      lastUpdatedStr = `${String(d.getMonth()+1).padStart(2,"0")}-${String(d.getDate()).padStart(2,"0")} ${String(d.getHours()).padStart(2,"0")}:${String(d.getMinutes()).padStart(2,"0")}`;
    }
  }

  let topicsHTML = `
  <div class="topics-intro">
    <div class="topics-heading-row">
      <h2 class="topics-heading">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
        </svg>
        视频选题推荐
      </h2>
      ${lastUpdatedStr ? `<span class="topics-update-time">资讯截至 ${lastUpdatedStr} · 每日 17:00 自动更新</span>` : ""}
    </div>
    <p class="topics-sub">基于当天抓取资讯自动匹配 Foodaily 视频栏目选题方向 · 每个方向取匹配分最高的内容，供选题参考</p>
  </div>
  <div class="topics-grid">`;

  TOPIC_CONFIGS.forEach((config, cardIdx) => {
    const maxItems = config.maxItems || 2;
    const scored = allArticles
      .map(art => ({ art, score: topicMatchScore(art, config), today: isToday(art) }))
      .filter(x => x.score > 0)
      .sort((a, b) => {
        // 今日资讯加权：同分时今日优先
        const todayBonus = (b.today ? 3 : 0) - (a.today ? 3 : 0);
        return (b.score - a.score) + todayBonus;
      })
      .slice(0, maxItems);

    const count = scored.length;

    const articlesHTML = scored.map(({ art, today }, i) => {
      const timeStr = formatTime(art.published_at);
      const regionIcon = REGION_ICON[art.region] || "🌐";
      return `
      <a href="${art.url}" target="_blank" rel="noopener noreferrer" class="topic-art-item${today ? " topic-art-today" : ""}" style="animation-delay:${i * 50}ms">
        <div class="topic-art-header">
          <div class="topic-art-meta">
            <span class="source-tag" style="background:${sourceColor(art.source)}20;color:${sourceColor(art.source)};border-color:${sourceColor(art.source)}40">${art.source}</span>
            <span class="region-tag">${regionIcon} ${art.region || ""}</span>
            ${today ? `<span class="today-badge">今日</span>` : ""}
          </div>
          <span class="topic-art-time">${timeStr}</span>
        </div>
        <h3 class="topic-art-title">${truncate(art.title || "（无标题）", 90)}</h3>
        ${art.summary ? `<p class="topic-art-summary">${truncate(art.summary, 130)}</p>` : ""}
        <div class="topic-art-readmore">阅读原文 →</div>
      </a>`;
    }).join("");

    const emptyMsg = `
      <div class="topic-empty">
        <span>📭 今日暂未匹配到相关资讯</span>
        <small>17:00 抓取后将自动呈现，或调整关键词覆盖</small>
      </div>`;

    topicsHTML += `
    <div class="topic-card topic-card-${config.id}" style="--topic-color:${config.color};--topic-bg:${config.bgColor};animation-delay:${cardIdx * 80}ms">
      <div class="topic-card-header">
        <div class="topic-card-title-row">
          <span class="topic-icon">${config.icon}</span>
          <div class="topic-card-titles">
            <h3 class="topic-title">${config.title}</h3>
            ${config.badge ? `<span class="topic-badge">${config.badge}</span>` : ""}
          </div>
        </div>
        <p class="topic-desc">${config.desc}</p>
      </div>
      <div class="topic-arts">
        ${count > 0 ? articlesHTML : emptyMsg}
      </div>
      <div class="topic-footer">
        <span class="topic-count">${count > 0 ? `匹配到 ${count} 条相关资讯` : "暂无匹配"}</span>
        <span class="topic-maxhint">最多展示 ${maxItems} 条</span>
      </div>
    </div>`;
  });

  topicsHTML += `</div>
  <div class="topics-note">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
      <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
    </svg>
    以上内容由关键词算法自动匹配生成（每日 17:00 抓取后自动刷新），仅供选题参考，具体方向以团队判断为准。如需全量浏览，请切换「全部资讯」标签。
  </div>`;

  articlesGrid.innerHTML = topicsHTML;
  articlesGrid.classList.add("topics-view");
}

// ══════════════════════════════════════════════════════════
// ── 巨头官网资讯视图 ──────────────────────────────────────
// ══════════════════════════════════════════════════════════

// 巨头品牌 emoji 映射
const BRAND_ICON = {
  "PepsiCo": "🥤", "Nestlé": "🐦", "Coca-Cola": "🥤", "Unilever": "🧴",
  "AB InBev": "🍺", "Mars": "🍫", "Mondelez": "🥨", "Kraft Heinz": "🧀",
  "General Mills": "🥣", "Danone": "🥛", "Ferrero": "🌰", "Suntory": "🍶",
  "Asahi": "🍺", "Nissin": "🍜", "Kirin": "🍺", "Ajinomoto": "🧂",
  "Meiji": "🍫", "Megmilk": "🧈", "Morinaga": "🍪", "Yakult": "🦠",
  "Ito En": "🍵", "CJ": "🌽", "Lotte Chilsung": "🥤",
  "Nestlé HS": "💊",
};

// S级原因中文映射
const LEVEL_REASON_LABEL = {
  "并购": "🔥 并购大动作", "新原料": "🧪 新原料", "新技术": "⚡ 新技术",
  "新产品": "🆕 新产品", "营销创新": "🎯 营销创新", "重磅新政": "📋 重磅新政",
  "常规新品/营销": "新品/营销", "企业动态": "企业动态",
};

async function loadGiantBrandsData() {
  try {
    const resp = await fetch(`${GIANTS_DATA_URL}?t=${Date.now()}`);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const data = await resp.json();
    allGiantArticles = data.articles || [];
    // 初始化筛选
    if (data.brands) {
      giantBrandsActive = new Set(data.brands);
    } else {
      giantBrandsActive = new Set(allGiantArticles.map(a => a.brand_cn));
    }
    if (data.regions) {
      giantRegionsActive = new Set(data.regions);
    } else {
      giantRegionsActive = new Set(allGiantArticles.map(a => a.region));
    }
    return data;
  } catch (err) {
    console.error("巨头资讯加载失败:", err);
    return null;
  }
}

function renderGiantsView() {
  const articlesGrid = document.getElementById("articlesGrid");
  const emptyState   = document.getElementById("emptyState");
  const loadMoreWrap = document.getElementById("loadMoreWrap");
  const statsBar     = document.getElementById("statsBar");
  if (statsBar) statsBar.style.display = "none";
  emptyState.classList.add("hidden");
  loadMoreWrap.classList.add("hidden");

  if (allGiantArticles.length === 0) {
    articlesGrid.innerHTML = `
      <div style="grid-column:1/-1;text-align:center;padding:60px 24px;color:#7a9478;">
        <div style="font-size:3rem;margin-bottom:16px;">🏢</div>
        <p style="font-weight:600;font-size:1rem;">巨头资讯加载中…</p>
        <p style="font-size:.875rem;margin-top:8px;opacity:.7;">数据加载完成后将显示巨头官网最新资讯</p>
      </div>`;
    articlesGrid.classList.add("giants-view");
    return;
  }

  // 筛选
  const filtered = allGiantArticles.filter(a =>
    giantBrandsActive.has(a.brand_cn) && giantRegionsActive.has(a.region)
  );

  // 按级别分组
  const sArts = filtered.filter(a => a.level === "S");
  const aArts = filtered.filter(a => a.level === "A");
  const bArts = filtered.filter(a => a.level === "B");

  // 品牌筛选 chips
  const allBrands = [...new Set(allGiantArticles.map(a => a.brand_cn))];
  const allRegions = [...new Set(allGiantArticles.map(a => a.region))];

  const brandChipsHTML = allBrands.map(b => {
    const icon = Object.entries(BRAND_ICON).find(([k]) =>
      allGiantArticles.some(a => a.brand_cn === b && a.brand.startsWith(k))
    );
    const isActive = giantBrandsActive.has(b);
    return `<button class="giant-chip${isActive ? " active" : ""}" data-giant-brand="${b}" onclick="toggleGiantBrand(this,'${b}')">${icon ? icon[1] : ""} ${b}</button>`;
  }).join("");

  const regionChipsHTML = allRegions.map(r => {
    const icon = REGION_ICON[r] || "🌐";
    const isActive = giantRegionsActive.has(r);
    return `<button class="giant-chip${isActive ? " active" : ""}" data-giant-region="${r}" onclick="toggleGiantRegion(this,'${r}')">${icon} ${r}</button>`;
  }).join("");

  // S 级卡片
  function renderGiantCard(art) {
    const icon = Object.entries(BRAND_ICON).find(([k]) => art.brand.startsWith(k));
    const regionIcon = REGION_ICON[art.region] || "🌐";
    const levelClass = art.level === "S" ? "giant-card-s" : art.level === "A" ? "giant-card-a" : "giant-card-b";
    const levelBadge = art.level === "S"
      ? `<span class="giant-level-badge giant-level-s">S级 · ${(LEVEL_REASON_LABEL[art.level_reason] || art.level_reason)}</span>`
      : art.level === "A"
        ? `<span class="giant-level-badge giant-level-a">A级</span>`
        : `<span class="giant-level-badge giant-level-b">B级</span>`;
    const timeStr = formatTime(art.published_at);
    return `
    <a href="${art.url}" target="_blank" rel="noopener noreferrer" class="giant-card ${levelClass}">
      <div class="giant-card-header">
        <div class="giant-card-brand">
          <span class="giant-brand-icon">${icon ? icon[1] : "🏢"}</span>
          <span class="giant-brand-name">${art.brand_cn}</span>
          <span class="giant-region-tag">${regionIcon} ${art.region}</span>
        </div>
        ${levelBadge}
      </div>
      <h3 class="giant-card-title">${truncate(art.title || "（无标题）", 120)}</h3>
      ${art.summary ? `<p class="giant-card-summary">${truncate(art.summary, 160)}</p>` : ""}
      <div class="giant-card-footer">
        <span class="giant-card-time">${timeStr}</span>
        <span class="giant-card-readmore">阅读原文 →</span>
      </div>
    </a>`;
  }

  // 构建完整 HTML
  let html = `
  <div class="giants-intro">
    <div class="giants-heading-row">
      <h2 class="giants-heading">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
          <path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>
        </svg>
        全球巨头官网资讯
      </h2>
      <span class="giants-update-time">每日 09:00 自动更新 · S/A/B 分级</span>
    </div>
    <p class="giants-sub">直连全球 ${allBrands.length} 大巨头官方新闻源 · 投融资/新品类/新原料/新技术/营销创新 → S级重点</p>
  </div>

  <!-- 品牌筛选 -->
  <div class="giants-filter-bar">
    <span class="giants-filter-label">品牌</span>
    <div class="giants-filter-chips">
      <button class="giant-chip${giantBrandsActive.size === allBrands.length ? " active" : ""}" onclick="toggleAllGiantBrands()">全选</button>
      ${brandChipsHTML}
    </div>
  </div>
  <!-- 地区筛选 -->
  <div class="giants-filter-bar">
    <span class="giants-filter-label">地区</span>
    <div class="giants-filter-chips">
      <button class="giant-chip${giantRegionsActive.size === allRegions.length ? " active" : ""}" onclick="toggleAllGiantRegions()">全选</button>
      ${regionChipsHTML}
    </div>
  </div>

  <!-- 统计 -->
  <div class="giants-stats">
    <span class="giants-stat-s">🔥 S级 ${sArts.length}</span>
    <span class="giants-stat-a">📦 A级 ${aArts.length}</span>
    <span class="giants-stat-b">📋 B级 ${bArts.length}</span>
    <span class="giants-stat-total">共 ${filtered.length} 条</span>
  </div>`;

  // S 级区域
  if (sArts.length > 0) {
    html += `<div class="giants-section"><h3 class="giants-section-title giants-section-s">🔥 S级 · 重大资讯</h3><div class="giants-grid giants-grid-s">`;
    sArts.forEach(a => { html += renderGiantCard(a); });
    html += `</div></div>`;
  }

  // A 级区域
  if (aArts.length > 0) {
    html += `<div class="giants-section"><h3 class="giants-section-title giants-section-a">📦 A级 · 常规新品/营销</h3><div class="giants-grid giants-grid-ab">`;
    aArts.forEach(a => { html += renderGiantCard(a); });
    html += `</div></div>`;
  }

  // B 级区域
  if (bArts.length > 0) {
    html += `<div class="giants-section"><h3 class="giants-section-title giants-section-b">📋 B级 · 企业动态</h3><div class="giants-grid giants-grid-ab">`;
    bArts.forEach(a => { html += renderGiantCard(a); });
    html += `</div></div>`;
  }

  if (filtered.length === 0) {
    html += `<div class="giants-empty"><span>📭 当前筛选条件下没有资讯</span></div>`;
  }

  html += `
  <div class="giants-note">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
      <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
    </svg>
    S级定义：行业巨头大动作（并购/合并）· 新原料/新技术 · 新产品（非新口味）· 创新营销联名 · 食品行业重磅新政。每日 09:00 自动抓取，保留近 10 天数据。
  </div>`;

  articlesGrid.innerHTML = html;
  articlesGrid.classList.add("giants-view");
}

// 巨头品牌/地区筛选
function toggleGiantBrand(btn, brand) {
  if (giantBrandsActive.has(brand)) {
    giantBrandsActive.delete(brand);
    btn.classList.remove("active");
  } else {
    giantBrandsActive.add(brand);
    btn.classList.add("active");
  }
  renderGiantsView();
}

function toggleGiantRegion(btn, region) {
  if (giantRegionsActive.has(region)) {
    giantRegionsActive.delete(region);
    btn.classList.remove("active");
  } else {
    giantRegionsActive.add(region);
    btn.classList.add("active");
  }
  renderGiantsView();
}

function toggleAllGiantBrands() {
  const allBrands = [...new Set(allGiantArticles.map(a => a.brand_cn))];
  if (giantBrandsActive.size === allBrands.length) {
    giantBrandsActive.clear();
  } else {
    giantBrandsActive = new Set(allBrands);
  }
  renderGiantsView();
}

function toggleAllGiantRegions() {
  const allRegions = [...new Set(allGiantArticles.map(a => a.region))];
  if (giantRegionsActive.size === allRegions.length) {
    giantRegionsActive.clear();
  } else {
    giantRegionsActive = new Set(allRegions);
  }
  renderGiantsView();
}

function switchTab(tab) {
  activeTab = tab;
  tabAllBtn.classList.toggle("active", tab === "all");
  tabTopicsBtn.classList.toggle("active", tab === "topics");
  tabGiantsBtn.classList.toggle("active", tab === "giants");
  tabSTopicsBtn.classList.toggle("active", tab === "stopics");

  const statsBar = document.getElementById("statsBar");
  const filterBars = [
    document.getElementById("filterBar"),
    document.getElementById("filterBarRegion"),
    document.getElementById("filterBarCat")
  ];

  const articlesGrid = document.getElementById("articlesGrid");

  if (tab === "topics") {
    filterBars.forEach(el => { if (el) el.style.display = "none"; });
    if (statsBar) statsBar.style.display = "none";
    articlesGrid.classList.remove("giants-view");
    articlesGrid.classList.remove("stopics-view");
    renderTopicsView();
  } else if (tab === "giants") {
    filterBars.forEach(el => { if (el) el.style.display = "none"; });
    if (statsBar) statsBar.style.display = "none";
    articlesGrid.classList.remove("topics-view");
    articlesGrid.classList.remove("stopics-view");
    if (allGiantArticles.length === 0) {
      loadGiantBrandsData().then(() => renderGiantsView());
    } else {
      renderGiantsView();
    }
  } else if (tab === "stopics") {
    filterBars.forEach(el => { if (el) el.style.display = "none"; });
    if (statsBar) statsBar.style.display = "none";
    articlesGrid.classList.remove("topics-view");
    articlesGrid.classList.remove("giants-view");
    if (allSTopicsArticles.length === 0) {
      loadSTopicsData().then(() => renderSTopicsView());
    } else {
      renderSTopicsView();
    }
  } else {
    filterBars.forEach(el => { if (el) el.style.display = ""; });
    if (statsBar) statsBar.style.display = "";
    articlesGrid.classList.remove("topics-view");
    articlesGrid.classList.remove("giants-view");
    articlesGrid.classList.remove("stopics-view");
    applyFilters();
  }
}

// ── Tab 事件 ───────────────────────────────────────────────────
tabAllBtn.addEventListener("click",    () => switchTab("all"));
tabTopicsBtn.addEventListener("click", () => switchTab("topics"));
tabGiantsBtn.addEventListener("click", () => switchTab("giants"));
tabSTopicsBtn.addEventListener("click", () => switchTab("stopics"));

// ── 搜索防抖 ───────────────────────────────────────────────────
let searchTimer = null;
searchInput.addEventListener("input", () => {
  searchKeyword = searchInput.value.trim();
  clearSearchBtn.classList.toggle("visible", searchKeyword.length > 0);
  clearTimeout(searchTimer);
  searchTimer = setTimeout(applyFilters, DEBOUNCE_MS);
});

clearSearchBtn.addEventListener("click", () => {
  searchInput.value = "";
  searchKeyword = "";
  clearSearchBtn.classList.remove("visible");
  applyFilters();
});

selectAllBtn.addEventListener("click", () => {
  document.querySelectorAll(".chip[data-source]").forEach(c => {
    c.classList.add("active");
    activeSourcesSet.add(c.dataset.source);
  });
  applyFilters();
});

clearAllBtn.addEventListener("click", () => {
  document.querySelectorAll(".chip[data-source]").forEach(c => {
    c.classList.remove("active");
    activeSourcesSet.delete(c.dataset.source);
  });
  applyFilters();
});

loadMoreBtn.addEventListener("click", () => {
  currentPage++;
  renderPage();
  setTimeout(() => {
    const cards = grid.querySelectorAll(".card");
    const targetIdx = (currentPage - 1) * PAGE_SIZE;
    if (cards[targetIdx]) cards[targetIdx].scrollIntoView({ behavior:"smooth", block:"start" });
  }, 60);
});

viewGridBtn.addEventListener("click", () => {
  isListView = false;
  grid.classList.remove("list-view");
  viewGridBtn.classList.add("active");
  viewListBtn.classList.remove("active");
});
viewListBtn.addEventListener("click", () => {
  isListView = true;
  grid.classList.add("list-view");
  viewListBtn.classList.add("active");
  viewGridBtn.classList.remove("active");
});

window.addEventListener("scroll", () => {
  backToTop.classList.toggle("hidden", window.scrollY < 400);
});
backToTop.addEventListener("click", () => window.scrollTo({ top:0, behavior:"smooth" }));

window.resetFilters = function() {
  searchInput.value = "";
  searchKeyword = "";
  clearSearchBtn.classList.remove("visible");
  document.querySelectorAll(".chip").forEach(c => {
    c.classList.add("active");
    if (c.dataset.source)   activeSourcesSet.add(c.dataset.source);
    if (c.dataset.region)   activeRegions.add(c.dataset.region);
    if (c.dataset.category) activeCategories.add(c.dataset.category);
  });
  applyFilters();
};

// ── 启动 ──────────────────────────────────────────────────────
loadData();

// ════════════════════════════════════════════════════════════
// S级选题网站 — 数据加载 + 渲染
// ════════════════════════════════════════════════════════════

const SITE_REGION_ICON = {
  "日本": "🇯🇵", "北美": "🇺🇸", "北美&欧洲": "🌍", "欧洲": "🇪🇺",
  "全球": "🌐", "中国": "🇨🇳",
};

const POSITIONING_BADGE = {
  "综合&分析": { color: "#2563eb", bg: "#eff6ff" },
  "新品&新闻": { color: "#059669", bg: "#f0fdf4" },
  "新闻&新品": { color: "#059669", bg: "#f0fdf4" },
  "新品发布":  { color: "#c2410c", bg: "#fff7ed" },
  "行业分析":  { color: "#7c3aed", bg: "#faf5ff" },
  "包装&设计": { color: "#9333ea", bg: "#fdf4ff" },
};

async function loadSTopicsData() {
  try {
    const resp = await fetch(`${STOPICS_DATA_URL}?t=${Date.now()}`);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const data = await resp.json();
    allSTopicsArticles = data.articles || [];
    if (data.sites) sTopicsSitesActive = new Set(data.sites);
    else sTopicsSitesActive = new Set(allSTopicsArticles.map(a => a.site_name));
    if (data.regions) sTopicsRegionsActive = new Set(data.regions);
    else sTopicsRegionsActive = new Set(allSTopicsArticles.map(a => a.region));
    return data;
  } catch (err) {
    console.error("S级选题数据加载失败:", err);
    return null;
  }
}

function renderSTopicsView() {
  const articlesGrid = document.getElementById("articlesGrid");
  const emptyState   = document.getElementById("emptyState");
  const loadMoreWrap = document.getElementById("loadMoreWrap");
  const statsBar     = document.getElementById("statsBar");
  if (statsBar) statsBar.style.display = "none";
  emptyState.classList.add("hidden");
  loadMoreWrap.classList.add("hidden");

  if (allSTopicsArticles.length === 0) {
    articlesGrid.innerHTML = `
      <div style="grid-column:1/-1;text-align:center;padding:60px 24px;color:#7a9478;">
        <div style="font-size:3rem;margin-bottom:16px;">⭐</div>
        <p style="font-weight:600;font-size:1rem;">S级选题数据加载中…</p>
        <p style="font-size:.875rem;margin-top:8px;opacity:.7;">每日 09:00 自动抓取，保留最近30天资讯</p>
      </div>`;
    articlesGrid.classList.add("stopics-view");
    return;
  }

  // 筛选
  const filtered = allSTopicsArticles.filter(a =>
    sTopicsSitesActive.has(a.site_name) && sTopicsRegionsActive.has(a.region)
  );

  const allSites = [...new Set(allSTopicsArticles.map(a => a.site_name))];
  const allRegionsList = [...new Set(allSTopicsArticles.map(a => a.region))];

  // S+ 和普通分组
  const sPlusArts = filtered.filter(a => a.is_s_plus);
  const normalArts = filtered.filter(a => !a.is_s_plus);

  // 品类统计
  const catStats = {};
  filtered.forEach(a => {
    const cat = (a.categories && a.categories[0]) ? a.categories[0].name : "其他";
    catStats[cat] = (catStats[cat] || 0) + 1;
  });
  const catStatHTML = Object.entries(catStats)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 6)
    .map(([k, v]) => `<span class="stopics-cat-stat">${k} <em>${v}</em></span>`)
    .join("");

  // 网站 chips
  const siteChipsHTML = allSites.map(s => {
    const isActive = sTopicsSitesActive.has(s);
    return `<button class="giant-chip${isActive ? " active" : ""}" onclick="toggleSTopicsSite(this,'${s.replace(/'/g, "\\'")}')">${s}</button>`;
  }).join("");

  const regionChipsHTML = allRegionsList.map(r => {
    const icon = SITE_REGION_ICON[r] || "🌐";
    const isActive = sTopicsRegionsActive.has(r);
    return `<button class="giant-chip${isActive ? " active" : ""}" onclick="toggleSTopicsRegion(this,'${r}')">${icon} ${r}</button>`;
  }).join("");

  // 卡片渲染函数
  function renderSTopicCard(art) {
    const regionIcon = SITE_REGION_ICON[art.region] || "🌐";
    const posStyle   = POSITIONING_BADGE[art.positioning] || { color: "#6b7280", bg: "#f9fafb" };
    const timeStr    = art.published_at
      ? formatTime(art.published_at)
      : (art.scraped_at ? "已抓取" : "");

    // 品类标签 (最多2个)
    const cats = art.categories || [];
    const catTagsHTML = cats.slice(0, 2).map(c =>
      `<span class="stopics-cat-tag" style="color:${c.color};background:${c.color}18;border-color:${c.color}33">${c.icon} ${c.name}</span>`
    ).join("");

    const sPlusBadge = art.is_s_plus
      ? `<span class="stopics-splus-badge">⭐ S+选题</span>`
      : "";

    const cardClass = art.is_s_plus ? "stopics-card stopics-card-splus" : "stopics-card";

    return `
    <a href="${art.url}" target="_blank" rel="noopener noreferrer" class="${cardClass}">
      ${art.is_s_plus ? '<div class="stopics-splus-glow"></div>' : ''}
      <div class="stopics-card-header">
        <div class="stopics-card-site">
          <span class="stopics-site-name">${art.site_name}</span>
          <span class="stopics-region-tag">${regionIcon} ${art.region}</span>
          <span class="stopics-pos-tag" style="color:${posStyle.color};background:${posStyle.bg}">${art.positioning}</span>
        </div>
        <div class="stopics-badge-row">
          ${sPlusBadge}
        </div>
      </div>
      <h3 class="stopics-card-title">${art.title}</h3>
      ${art.summary ? `<p class="stopics-card-summary">${art.summary}</p>` : ""}
      <div class="stopics-card-footer">
        <div class="stopics-cat-tags">${catTagsHTML}</div>
        <div class="stopics-card-meta">
          <span class="stopics-time">${timeStr}</span>
          <span class="stopics-readmore">阅读原文 →</span>
        </div>
      </div>
    </a>`;
  }

  let html = `
  <div class="stopics-intro">
    <div class="stopics-heading-row">
      <h2 class="stopics-heading">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="22" height="22">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
        </svg>
        S级选题网站
      </h2>
      <span class="stopics-update-badge">每日 09:00 · 近30天 · 自动品类分析</span>
    </div>
    <p class="stopics-sub">跟踪 ${allSites.length} 个精选选题网站 · <strong style="color:#b45309">⭐ S+选题</strong> = 全球首创 / 首款 / 爆品 / 卖爆 等明显创新或爆品属性</p>
  </div>

  <!-- 网站筛选 -->
  <div class="giants-filter-bar">
    <span class="giants-filter-label">网站</span>
    <div class="giants-filter-chips">
      <button class="giant-chip${sTopicsSitesActive.size === allSites.length ? " active" : ""}" onclick="toggleAllSTopicsSites()">全选</button>
      ${siteChipsHTML}
    </div>
  </div>
  <!-- 地区筛选 -->
  <div class="giants-filter-bar">
    <span class="giants-filter-label">地区</span>
    <div class="giants-filter-chips">
      <button class="giant-chip${sTopicsRegionsActive.size === allRegionsList.length ? " active" : ""}" onclick="toggleAllSTopicsRegions()">全选</button>
      ${regionChipsHTML}
    </div>
  </div>

  <!-- 统计 -->
  <div class="stopics-stats-bar">
    <span class="stopics-stat-splus">⭐ S+选题 ${sPlusArts.length}</span>
    <span class="stopics-stat-normal">📰 普通 ${normalArts.length}</span>
    <span class="stopics-stat-total">共 ${filtered.length} 条</span>
    <div class="stopics-cat-stats">${catStatHTML}</div>
  </div>`;

  // S+ 区域
  if (sPlusArts.length > 0) {
    html += `<div class="stopics-section"><h3 class="stopics-section-title stopics-section-splus">⭐ S+选题 · 全球首创 / 爆品</h3><div class="stopics-grid stopics-grid-splus">`;
    sPlusArts.forEach(a => { html += renderSTopicCard(a); });
    html += `</div></div>`;
  }

  // 普通资讯区域（按品类分组）
  if (normalArts.length > 0) {
    // 按主品类分组
    const catGroups = {};
    normalArts.forEach(a => {
      const cat = (a.categories && a.categories[0]) ? a.categories[0].name : "其他";
      if (!catGroups[cat]) catGroups[cat] = [];
      catGroups[cat].push(a);
    });
    // 合并为统一列表（保持按时间排序）
    html += `<div class="stopics-section"><h3 class="stopics-section-title stopics-section-normal">📰 全部资讯 · 已自动分类</h3><div class="stopics-grid stopics-grid-normal">`;
    normalArts.forEach(a => { html += renderSTopicCard(a); });
    html += `</div></div>`;
  }

  if (filtered.length === 0) {
    html += `<div class="giants-empty"><span>📭 当前筛选条件下没有资讯</span></div>`;
  }

  html += `
  <div class="giants-note" style="margin:4px 24px 24px;">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
      <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
    </svg>
    <strong>⭐ S+选题</strong>定义：命中"全球首创/首款/世界初/大ヒット/sold out/viral/爆品"等关键词。品类由AI自动分析，仅供参考。每日09:00抓取，保留近30天数据。
  </div>`;

  articlesGrid.innerHTML = html;
  articlesGrid.classList.add("stopics-view");
}

// S级选题筛选函数
function toggleSTopicsSite(btn, site) {
  if (sTopicsSitesActive.has(site)) { sTopicsSitesActive.delete(site); btn.classList.remove("active"); }
  else { sTopicsSitesActive.add(site); btn.classList.add("active"); }
  renderSTopicsView();
}
function toggleSTopicsRegion(btn, region) {
  if (sTopicsRegionsActive.has(region)) { sTopicsRegionsActive.delete(region); btn.classList.remove("active"); }
  else { sTopicsRegionsActive.add(region); btn.classList.add("active"); }
  renderSTopicsView();
}
function toggleAllSTopicsSites() {
  const all = [...new Set(allSTopicsArticles.map(a => a.site_name))];
  if (sTopicsSitesActive.size === all.length) sTopicsSitesActive.clear();
  else sTopicsSitesActive = new Set(all);
  renderSTopicsView();
}
function toggleAllSTopicsRegions() {
  const all = [...new Set(allSTopicsArticles.map(a => a.region))];
  if (sTopicsRegionsActive.size === all.length) sTopicsRegionsActive.clear();
  else sTopicsRegionsActive = new Set(all);
  renderSTopicsView();
}
