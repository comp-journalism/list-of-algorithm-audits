// Brand color map for organization tags
const ORG_COLORS = {
  "Google": { bg: "#4285F4", text: "#fff" },
  "YouTube": { bg: "#FF0000", text: "#fff" },
  "Facebook": { bg: "#1877F2", text: "#fff" },
  "Meta": { bg: "#1877F2", text: "#fff" },
  "Instagram": { bg: "#E1306C", text: "#fff" },
  "Twitter": { bg: "#1DA1F2", text: "#fff" },
  "Bing": { bg: "#008373", text: "#fff" },
  "DuckDuckGo": { bg: "#DE5833", text: "#fff" },
  "Yandex": { bg: "#FC3F1D", text: "#fff" },
  "Yahoo": { bg: "#6001D2", text: "#fff" },
  "ChatGPT": { bg: "#10A37F", text: "#fff" },
  "Amazon": { bg: "#FF9900", text: "#222" },
  "TikTok": { bg: "#25F4EE", text: "#222" },
  "Douyin": { bg: "#161823", text: "#fff" },
  "DALL-E": { bg: "#0D7377", text: "#fff" },
  "Baidu": { bg: "#2319DC", text: "#fff" },
  "Spotify": { bg: "#1DB954", text: "#fff" },
  "LinkedIn": { bg: "#0A66C2", text: "#fff" },
  "Reddit": { bg: "#FF4500", text: "#fff" },
  "Apple News": { bg: "#555555", text: "#fff" },
  "Siri": { bg: "#A2AAAD", text: "#222" },
};

// Source color map
const SOURCE_COLORS = {
  "NEEDS HUMAN REVIEW": { bg: "#fff3cd", text: "#856404" },
  "Urman et al. (2025)": { bg: "#d4edda", text: "#155724" },
  "2021 Review (Bandy)": { bg: "#d4edda", text: "#155724" },
  "2026 Review (Bandy)": { bg: "#d4edda", text: "#155724" },
};

let allMethods = [];
let allDomains = [];
let allOrgs = [];
let allSources = [];
let filters = { methods: new Set(), domains: new Set(), orgs: new Set(), sources: new Set(), yearMin: 2012, yearMax: 2026 };
let expanded = { method: false, domain: false, org: false, source: false };
let sortCol = "year";
let sortAsc = false;

function countByField(key, splitComma) {
  const counts = {};
  DATA.forEach(r => {
    const v = r[key] || "";
    if (splitComma) v.split(",").forEach(x => { x = x.trim(); if (x) counts[x] = (counts[x]||0) + 1; });
    else if (v) counts[v] = (counts[v]||0) + 1;
  });
  return Object.entries(counts).sort((a,b) => b[1] - a[1]);
}

function buildCheckboxes(containerId, itemsWithCounts, filterSet, filterKey) {
  const el = document.getElementById(containerId);
  el.innerHTML = "";
  const mainItems = [];
  const extraItems = [];
  itemsWithCounts.forEach(([item, count]) => {
    if (count > 1) mainItems.push([item, count]);
    else extraItems.push([item, count]);
  });

  function addRow(parent, item, count) {
    const row = document.createElement("label");
    row.className = "cb-row";
    const cb = document.createElement("input");
    cb.type = "checkbox";
    cb.checked = filterSet.has(item);
    cb.addEventListener("change", () => {
      if (cb.checked) filterSet.add(item); else filterSet.delete(item);
      render();
    });
    const span = document.createElement("span");
    span.className = "cb-label";
    span.textContent = item;
    const cnt = document.createElement("span");
    cnt.className = "cb-count";
    cnt.textContent = count;
    row.append(cb, span, cnt);
    parent.appendChild(row);
  }

  mainItems.forEach(([item, count]) => addRow(el, item, count));

  if (extraItems.length > 0) {
    const extraContainer = document.createElement("div");
    extraContainer.style.display = expanded[filterKey] ? "block" : "none";
    el.appendChild(extraContainer);
    extraItems.forEach(([item, count]) => addRow(extraContainer, item, count));

    const btn = document.createElement("button");
    btn.className = "show-more-btn";
    btn.textContent = expanded[filterKey] ? "Show fewer" : "Show " + extraItems.length + " more";
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      expanded[filterKey] = !expanded[filterKey];
      render();
    });
    el.appendChild(btn);
  }
}

function toggleMobileFilters() {
  const inner = document.querySelector(".filters-inner");
  const btn = document.querySelector(".filters-toggle");
  inner.classList.toggle("open");
  btn.classList.toggle("active");
}

function toggleDropdown(name) {
  const dd = document.getElementById("dd-" + name);
  const wasOpen = dd.classList.contains("open");
  document.querySelectorAll(".dropdown").forEach(d => d.classList.remove("open"));
  document.querySelectorAll(".filter-label").forEach(l => l.classList.remove("active"));
  if (!wasOpen) {
    dd.classList.add("open");
    dd.previousElementSibling.classList.add("active");
  }
}

document.addEventListener("click", e => {
  if (!e.target.closest(".filter-group")) {
    document.querySelectorAll(".dropdown").forEach(d => d.classList.remove("open"));
    document.querySelectorAll(".filter-label").forEach(l => l.classList.remove("active"));
  }
});

// Year range constants
const YEAR_MIN_ABS = 2012;
const YEAR_MAX_ABS = 2026;
const YEAR_COUNT = YEAR_MAX_ABS - YEAR_MIN_ABS + 1;

function getYearCounts() {
  const counts = {};
  for (let y = YEAR_MIN_ABS; y <= YEAR_MAX_ABS; y++) counts[y] = 0;
  DATA.forEach(r => { const y = +r.Year; if (y >= YEAR_MIN_ABS && y <= YEAR_MAX_ABS) counts[y]++; });
  return counts;
}

function buildYearChart() {
  const chart = document.getElementById("year-chart");
  const labels = document.getElementById("year-labels");
  const counts = getYearCounts();
  const maxCount = Math.max(...Object.values(counts), 1);

  chart.innerHTML = "";
  labels.innerHTML = "";
  for (let y = YEAR_MIN_ABS; y <= YEAR_MAX_ABS; y++) {
    const bar = document.createElement("div");
    bar.className = "year-bar" + (y >= filters.yearMin && y <= filters.yearMax ? " active" : "");
    bar.style.height = Math.max(counts[y] / maxCount * 100, 2) + "%";
    const tip = document.createElement("span");
    tip.className = "year-bar-tip";
    tip.textContent = y + ": " + counts[y];
    bar.appendChild(tip);
    chart.appendChild(bar);

    const lbl = document.createElement("span");
    lbl.textContent = (y % 2 === 0) ? y : "";
    labels.appendChild(lbl);
  }
  updateYearRange();
}

function updateYearRange() {
  const fill = document.getElementById("year-range-fill");
  const hMin = document.getElementById("year-handle-min");
  const hMax = document.getElementById("year-handle-max");
  const pctMin = (filters.yearMin - YEAR_MIN_ABS) / (YEAR_COUNT - 1) * 100;
  const pctMax = (filters.yearMax - YEAR_MIN_ABS) / (YEAR_COUNT - 1) * 100;
  fill.style.left = pctMin + "%";
  fill.style.width = (pctMax - pctMin) + "%";
  hMin.style.left = pctMin + "%";
  hMax.style.left = pctMax + "%";

  document.getElementById("yearMin").value = filters.yearMin;
  document.getElementById("yearMax").value = filters.yearMax;
  document.getElementById("year-count").textContent =
    (filters.yearMin === YEAR_MIN_ABS && filters.yearMax === YEAR_MAX_ABS) ? "" :
    "(" + filters.yearMin + "–" + filters.yearMax + ")";

  // Update bar active states
  document.querySelectorAll(".year-bar").forEach((bar, i) => {
    const y = YEAR_MIN_ABS + i;
    bar.classList.toggle("active", y >= filters.yearMin && y <= filters.yearMax);
  });
}

function yearFromPct(pct) {
  return Math.round(YEAR_MIN_ABS + pct * (YEAR_COUNT - 1));
}

function initYearDrag(handleId, isMin) {
  const handle = document.getElementById(handleId);
  const track = document.getElementById("year-range-track");

  function onMove(clientX) {
    const rect = track.getBoundingClientRect();
    const pct = Math.max(0, Math.min(1, (clientX - rect.left) / rect.width));
    let y = yearFromPct(pct);
    if (isMin) { y = Math.min(y, filters.yearMax); filters.yearMin = y; }
    else { y = Math.max(y, filters.yearMin); filters.yearMax = y; }
    updateYearRange();
    render();
  }

  handle.addEventListener("mousedown", e => {
    e.preventDefault();
    const move = e2 => onMove(e2.clientX);
    const up = () => { document.removeEventListener("mousemove", move); document.removeEventListener("mouseup", up); };
    document.addEventListener("mousemove", move);
    document.addEventListener("mouseup", up);
  });

  handle.addEventListener("touchstart", e => {
    e.preventDefault();
    const move = e2 => onMove(e2.touches[0].clientX);
    const up = () => { document.removeEventListener("touchmove", move); document.removeEventListener("touchend", up); };
    document.addEventListener("touchmove", move);
    document.addEventListener("touchend", up);
  });
}

initYearDrag("year-handle-min", true);
initYearDrag("year-handle-max", false);

document.getElementById("year-range-track").addEventListener("click", e => {
  if (e.target.classList.contains("year-handle")) return;
  const rect = e.currentTarget.getBoundingClientRect();
  const pct = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
  const y = yearFromPct(pct);
  // Snap to whichever handle is closer
  if (Math.abs(y - filters.yearMin) <= Math.abs(y - filters.yearMax)) {
    filters.yearMin = Math.min(y, filters.yearMax);
  } else {
    filters.yearMax = Math.max(y, filters.yearMin);
  }
  updateYearRange(); render();
});

document.getElementById("yearMin").addEventListener("input", e => {
  filters.yearMin = Math.max(YEAR_MIN_ABS, Math.min(+e.target.value, filters.yearMax));
  updateYearRange(); render();
});
document.getElementById("yearMax").addEventListener("input", e => {
  filters.yearMax = Math.min(YEAR_MAX_ABS, Math.max(+e.target.value, filters.yearMin));
  updateYearRange(); render();
});

function matchesFilter(row) {
  const yearStr = (row.Year || "").trim();
  if (yearStr) {
    const year = +yearStr;
    if (year < filters.yearMin || year > filters.yearMax) return false;
  }
  if (filters.methods.size > 0) {
    const rm = (row.Method || "").split(",").map(x => x.trim());
    if (!rm.some(m => filters.methods.has(m))) return false;
  }
  if (filters.domains.size > 0) {
    const rd = (row.Domain || "").split(",").map(x => x.trim());
    if (!rd.some(d => filters.domains.has(d))) return false;
  }
  if (filters.orgs.size > 0) {
    const ro = (row.Organization || "").split(",").map(x => x.trim());
    if (!ro.some(o => filters.orgs.has(o))) return false;
  }
  if (filters.sources.size > 0) {
    const s = (row.Source || "").trim();
    if (!filters.sources.has(s)) return false;
  }
  return true;
}

let shuffled = false;

function sortBy(col) {
  shuffled = false;
  if (sortCol === col) sortAsc = !sortAsc;
  else { sortCol = col; sortAsc = true; }
  render();
}

function shuffleRows() {
  shuffled = true;
  render();
}

function clearFilters() {
  filters = { methods: new Set(), domains: new Set(), orgs: new Set(), sources: new Set(), yearMin: YEAR_MIN_ABS, yearMax: YEAR_MAX_ABS };
  updateYearRange();
  render();
}

function orgTagHtml(name) {
  const trimmed = name.trim();
  const color = ORG_COLORS[trimmed];
  if (color) {
    return `<span class="tag tag-org" style="background:${color.bg};color:${color.text}">${trimmed}</span>`;
  }
  return `<span class="tag tag-org">${trimmed}</span>`;
}

function sourceTagHtml(source) {
  const s = (source || "").trim();
  const color = SOURCE_COLORS[s];
  if (color) {
    return `<span class="tag tag-source" style="background:${color.bg};color:${color.text}">${s}</span>`;
  }
  return `<span class="tag tag-source">${s}</span>`;
}

function render() {
  buildCheckboxes("dd-method", allMethods, filters.methods, "method");
  buildCheckboxes("dd-domain", allDomains, filters.domains, "domain");
  buildCheckboxes("dd-org", allOrgs, filters.orgs, "org");
  buildCheckboxes("dd-source", allSources, filters.sources, "source");
  updateYearRange();

  document.getElementById("method-count").textContent = filters.methods.size ? "(" + filters.methods.size + ")" : "";
  document.getElementById("domain-count").textContent = filters.domains.size ? "(" + filters.domains.size + ")" : "";
  document.getElementById("org-count").textContent = filters.orgs.size ? "(" + filters.orgs.size + ")" : "";
  document.getElementById("source-count").textContent = filters.sources.size ? "(" + filters.sources.size + ")" : "";

  let rows = DATA.filter(matchesFilter);

  if (shuffled) {
    for (let i = rows.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [rows[i], rows[j]] = [rows[j], rows[i]];
    }
  } else {
    const key = { title: "Title", year: "Year", method: "Method", domain: "Domain", org: "Organization", source: "Source" }[sortCol];
    rows.sort((a, b) => {
      let va = (a[key] || "").toLowerCase(), vb = (b[key] || "").toLowerCase();
      if (sortCol === "year") { va = +a.Year; vb = +b.Year; }
      if (va < vb) return sortAsc ? -1 : 1;
      if (va > vb) return sortAsc ? 1 : -1;
      return 0;
    });
  }

  document.querySelectorAll("thead th").forEach(th => th.classList.remove("sorted"));
  const activeTh = document.getElementById("th-" + sortCol);
  if (activeTh) activeTh.classList.add("sorted");

  const tbody = document.getElementById("tbody");
  const noResults = document.getElementById("no-results");

  if (rows.length === 0) {
    tbody.innerHTML = "";
    noResults.style.display = "block";
  } else {
    noResults.style.display = "none";
    tbody.innerHTML = rows.map(r => {
      const title = r.Title || r.Reference;
      const link = r.DOI ? `<a href="${r.DOI}" target="_blank" rel="noopener">${title}</a>` : title;
      const methods = (r.Method || "").split(",").map(m => `<span class="tag tag-method">${m.trim()}</span>`).join("");
      const domains = (r.Domain || "").split(",").map(d => `<span class="tag tag-domain">${d.trim()}</span>`).join("");
      const orgs = (r.Organization || "").split(",").map(o => orgTagHtml(o)).join("");
      const source = sourceTagHtml(r.Source);
      return `<tr><td data-label="Reference">${link}</td><td data-label="Year">${r.Year}</td><td data-label="Method">${methods}</td><td data-label="Domain">${domains}</td><td data-label="Organization">${orgs}</td><td data-label="Source">${source}</td></tr>`;
    }).join("");
  }

  document.getElementById("results-count").textContent = rows.length + " of " + DATA.length + " audits";
}

// Initialize
allMethods = countByField("Method", true);
allDomains = countByField("Domain", true);
allOrgs = countByField("Organization", true);
allSources = countByField("Source", false);
buildYearChart();
render();
