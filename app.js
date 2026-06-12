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

const DATA_URL   = "./data/news_latest.json";
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
let activeTab        = "all";   // "all" | "topics"

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
const tabBar       = document.getElementById("tabBar");
const tabAllBtn    = document.getElementById("tabAll");
const tabTopicsBtn = document.getElementById("tabTopics");
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

function switchTab(tab) {
  activeTab = tab;
  tabAllBtn.classList.toggle("active", tab === "all");
  tabTopicsBtn.classList.toggle("active", tab === "topics");

  const statsBar = document.getElementById("statsBar");
  const filterBars = [
    document.getElementById("filterBar"),
    document.getElementById("filterBarRegion"),
    document.getElementById("filterBarCat")
  ];

  if (tab === "topics") {
    // 隐藏筛选栏，显示选题视图
    filterBars.forEach(el => { if (el) el.style.display = "none"; });
    renderTopicsView();
  } else {
    // 显示筛选栏，显示资讯列表
    filterBars.forEach(el => { if (el) el.style.display = ""; });
    if (statsBar) statsBar.style.display = "";
    const articlesGrid = document.getElementById("articlesGrid");
    articlesGrid.classList.remove("topics-view");
    applyFilters();
  }
}

// ── Tab 事件 ───────────────────────────────────────────────────
tabAllBtn.addEventListener("click",    () => switchTab("all"));
tabTopicsBtn.addEventListener("click", () => switchTab("topics"));

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
