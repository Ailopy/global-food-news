/**
 * app.js — 全球食品资讯聚合前端逻辑 v3
 * 新增：地区筛选、品类筛选、数据统计面板、推荐选题Tab
 */

// ── 选题推荐配置 ─────────────────────────────────────────────
const TOPIC_CONFIGS = [
  {
    id: "head-companies",
    icon: "🏢",
    title: "头部企业动态",
    desc: "全球/国内头部食品企业的新品创意、战略动向、收并购、渠道布局动作",
    color: "#2d7d46",
    bgColor: "#e8f5ec",
    keywords: [
      "nestle", "nestlé", "unilever", "pepsico", "coca-cola", "coca cola",
      "mondelez", "kellogg", "general mills", "mars", "danone", "l'oreal",
      "abbott", "campbell", "kraft heinz", "ADM", " Cargill", " Barry Callebaut",
      "农夫山泉", "伊利", "蒙牛", "光明", "娃哈哈", "康师傅", "统一企业",
      "旺旺", "良品铺子", "三只松鼠", "来伊份", "元气森林",
      "acquisition", "merger", "m&a", "takeover", "战略", "扩张", "布局",
      "收购", "并购", "新品上市", "new product", "launch", "expansion",
      "strategic", "partnership", "collaboration", "joint venture"
    ],
    // 高权重关键词（匹配这些直接入选）
    priorityKeywords: ["acquisition", "merger", "m&a", "收购", "并购", "新品", "launch", "new product", "收购", "战略"]
  },
  {
    id: "channel-innovation",
    icon: "🛒",
    title: "渠道新物种",
    desc: "日韩药店、便利店、零食量贩、餐饮渠道等新兴零售/渠道形态的新案例",
    color: "#1a6b8a",
    bgColor: "#e0f4fb",
    keywords: [
      "pharmacy", "drugstore", "druggist", "convenience store", "convenience-store",
      "conveni", " Lawson", "family mart", "seven-eleven", "7-eleven", "7 eleven",
      "全家", "便利店", "药店", "药妆", "optical", "日域", "OWM",
      "drugstore", "cosme", "松本清", "ain药局",
      "零食量贩", "零食很忙", "赵一鸣", "零食门店", "snack chain",
      "量贩零食", "discount store", "dollar store", "100円店", "百元店",
      "fast fashion", "fast-casual", "ghost kitchen", "dark kitchen",
      "virtual restaurant", "meal kit", "subscription box",
      "auto-service", "自動販売機", "vending machine", "自助售货",
      "OMNI", "omni-channel", "omnichannel", "全渠道", "D2C", "direct-to-consumer",
      "折扣店", "临期食品", "奥特乐", "吉乐熊", "嗨特购",
      "pop-up", "popup", "快闪店", "sample store"
    ]
  },
  {
    id: "market-inspiration",
    icon: "🌏",
    title: "成熟市场启发",
    desc: "日韩、欧美等成熟市场的创新产品、品牌、品类对中国市场的借鉴与启发",
    color: "#7c3aed",
    bgColor: "#ede9fe",
    keywords: [
      "japan", "japanese", "korea", "korean", "k-beauty", "j-food",
      "日本市场", "日式", "韩式", "韩国市场", "三得利", "明治", "森永",
      "朝日", "麒麟", "日清", "龟甲万", "味之素", "kagome",
      "ottogi", "农心", "bibigo", "大韩民国", "韩国",
      "europe", "european", "uk", "germany", "france", "italy", "spain",
      "欧洲市场", "北欧", "功能饮料", "plant-based", "plant based",
      "oatly", "beyond meat", "impossible food", "瑞典燕麦",
      "zero sugar", "no sugar", "low sugar", "减糖", "无糖",
      "alternative protein", "替代蛋白", "precision fermentation",
      "personalized nutrition", "个性化营养", "肠道健康",
      "sleep", "功能性表示食品", "特定保健用食品", "FOSHU",
      "nope", "guilt-free", "罪恶营销", "indulgence", "放纵营销",
      "cocktail", "低酒精", "RTD", "ready-to-drink",
      "shelf-stable", "常温", "long shelf life", "保质期",
      "sustainability", "可持续", "plant forward", "素食",
      "clean label", "clean label", "清洁标签", "天然",
      "adaptogen", "适应原", "mushroom", "蘑菇", "CBD", "汉麻",
      "blue zone", "长寿饮食", "地中海饮食", "mediterranean",
      "social drinking", "无酒精社交", "non-alcoholic", "无醇"
    ]
  },
  {
    id: "packaging-innovation",
    icon: "📦",
    title: "包装设计创新",
    desc: "聚焦包装结构、材料创新如何解决消费痛点或创造新体验，挖掘细分创新点",
    color: "#b45309",
    bgColor: "#fef3c7",
    keywords: [
      "packaging", "package design", "package", "packing",
      "包装", "包装设计", "结构创新", "包装结构", "包装材料",
      "sustainable packaging", "可持续包装", "eco-friendly", "环保包装",
      "biodegradable", "可降解", "compostable", "植物基包装",
      "paper packaging", "纸包装", "金属罐", "aluminum can",
      "plastic reduction", "减塑", "plastic-free", "无塑",
      "refill", "refillable", " refill", "补充装", "替换装",
      "recyclable", "可回收", "recycled content", "再生塑料",
      "mono-material", "单一材质", "pouch", "自立袋", "软包装",
      "portion control", "小包装", "single serve", "一人份",
      "smart packaging", "智能包装", "NFC tag", "AR packaging",
      "QR code", "二维码", "interactive packaging", "互动包装",
      "convenience", "易撕", "易开", "微波适用", "自热",
      "on-the-go", "即食", "ready to eat", "RTE",
      "gift packaging", "礼盒", "seasonal packaging", "节日包装",
      "minimalist design", "极简包装", "design award", "包装大奖",
      "worldstar", "pentaward", "if design award",
      "shelf impact", "货架陈列", "point of sale", "POSM",
      "brand identity", "品牌视觉", "typography", "字体设计",
      "premium packaging", "高端包装", "luxury", "质感包装"
    ]
  }
];

// 计算文章与选题方向的匹配分
function topicMatchScore(art, config) {
  const text = ((art.title || "") + " " + (art.summary || "")).toLowerCase();
  let score = 0;
  // 精确匹配高权重关键词
  for (const kw of (config.priorityKeywords || [])) {
    if (text.includes(kw.toLowerCase())) score += 10;
  }
  // 匹配普通关键词
  for (const kw of config.keywords) {
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
  // 清空并隐藏主内容区的统计和文章容器
  const statsBar = document.getElementById("statsBar");
  const articlesGrid = document.getElementById("articlesGrid");
  const emptyState = document.getElementById("emptyState");
  const loadMoreWrap = document.getElementById("loadMoreWrap");
  if (statsBar) statsBar.style.display = "none";
  articlesGrid.innerHTML = "";
  emptyState.classList.add("hidden");
  loadMoreWrap.classList.add("hidden");

  // 如果还没加载数据
  if (allArticles.length === 0) {
    articlesGrid.innerHTML = `
      <div style="grid-column:1/-1;text-align:center;padding:60px 24px;color:#7a9478;">
        <div style="font-size:3rem;margin-bottom:16px;">📋</div>
        <p style="font-weight:600;font-size:1rem;">资讯加载中…</p>
        <p style="font-size:.875rem;margin-top:8px;opacity:.7;">数据加载完成后将显示选题推荐</p>
      </div>`;
    return;
  }

  // 选题推荐面板容器
  let topicsHTML = `
  <div class="topics-intro">
    <h2 class="topics-heading">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="22" height="22">
        <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
      </svg>
      选题方向严选
    </h2>
    <p class="topics-sub">基于近期资讯自动挖掘，每个方向精选 <strong>2 条</strong>最具代表性内容，供选题参考</p>
  </div>
  <div class="topics-grid">`;

  TOPIC_CONFIGS.forEach(config => {
    // 找出匹配分最高的前 2 条文章
    const scored = allArticles
      .map(art => ({ art, score: topicMatchScore(art, config) }))
      .filter(x => x.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 2);

    const count = scored.length;

    let articlesHTML = scored.map(({ art }, i) => {
      const timeStr = formatTime(art.published_at);
      return `
      <a href="${art.url}" target="_blank" rel="noopener noreferrer" class="topic-art-item" style="animation-delay:${i * 60}ms">
        <div class="topic-art-header">
          <span class="source-tag" style="background:${sourceColor(art.source)}20;color:${sourceColor(art.source)};border-color:${sourceColor(art.source)}40">${art.source}</span>
          <span class="topic-art-time">${timeStr}</span>
        </div>
        <h3 class="topic-art-title">${highlight(truncate(art.title || "（无标题）", 80), "")}</h3>
        ${art.summary ? `<p class="topic-art-summary">${highlight(truncate(art.summary, 120), "")}</p>` : ""}
      </a>`;
    }).join("");

    const emptyMsg = `
      <div class="topic-empty">
        <span>暂未匹配到相关资讯</span>
        <small>来源覆盖后将自动呈现</small>
      </div>`;

    topicsHTML += `
    <div class="topic-card" style="--topic-color:${config.color};--topic-bg:${config.bgColor};animation-delay:${TOPIC_CONFIGS.indexOf(config) * 80}ms">
      <div class="topic-card-header">
        <span class="topic-icon">${config.icon}</span>
        <div>
          <h3 class="topic-title">${config.title}</h3>
          <p class="topic-desc">${config.desc}</p>
        </div>
      </div>
      <div class="topic-arts">
        ${count > 0 ? articlesHTML : emptyMsg}
      </div>
      <div class="topic-footer">
        <span class="topic-count">${count > 0 ? `${count} 条相关资讯` : "暂无匹配"}</span>
      </div>
    </div>`;
  });

  topicsHTML += `</div>`;

  // 底部说明
  topicsHTML += `
  <div class="topics-note">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
      <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
    </svg>
    以上内容基于近7天资讯关键词自动匹配生成，选题方向供参考，具体报道请以原文为准。如需进一步筛选，请切换至「全部资讯」使用搜索和筛选功能。
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
