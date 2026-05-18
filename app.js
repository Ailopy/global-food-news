/**
 * app.js — 全球食品资讯聚合前端逻辑 v2
 * 新增：地区筛选、品类筛选、数据统计面板
 */

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

// ── 事件绑定 ───────────────────────────────────────────────────
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
