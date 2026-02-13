// Brand color map for organization tags
const ORG_COLORS = {
  "Google": { bg: "#4285F4", text: "#fff" },
  "YouTube": { bg: "#FF0000", text: "#fff" },
  "Facebook": { bg: "#1877F2", text: "#fff" },
  "Meta": { bg: "#1877F2", text: "#fff" },
  "Instagram": { bg: "#1877F2", text: "#fff" },
  "Twitter": { bg: "#000000", text: "#fff" },
  "Bing": { bg: "#008373", text: "#fff" },
  "DuckDuckGo": { bg: "#DE5833", text: "#fff" },
  "Yandex": { bg: "#FF0000", text: "#fff" },
  "Yahoo": { bg: "#6001D2", text: "#fff" },
  "ChatGPT": { bg: "#10A37F", text: "#fff" },
  "Amazon": { bg: "#FF9900", text: "#222" },
  "TikTok": { bg: "#000000", text: "#fff" },
  "Douyin": { bg: "#000000", text: "#fff" },
  "DALL-E": { bg: "#10A37F", text: "#fff" },
  "Baidu": { bg: "#2319DC", text: "#fff" },
  "Spotify": { bg: "#1DB954", text: "#fff" },
  "LinkedIn": { bg: "#0A66C2", text: "#fff" },
  "Reddit": { bg: "#FF4500", text: "#fff" },
  "Apple News": { bg: "#555555", text: "#fff" },
  "Siri": { bg: "#555555", text: "#fff" },
};

let allMethods = [];
let allDomains = [];
let allOrgs = [];
let filters = { methods: new Set(), domains: new Set(), orgs: new Set(), yearMin: 2012, yearMax: 2024 };
let expanded = { method: false, domain: false, org: false };
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

document.getElementById("yearMin").addEventListener("input", e => { filters.yearMin = +e.target.value; render(); });
document.getElementById("yearMax").addEventListener("input", e => { filters.yearMax = +e.target.value; render(); });

function matchesFilter(row) {
  const year = +row.Year;
  if (year < filters.yearMin || year > filters.yearMax) return false;
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
  return true;
}

function sortBy(col) {
  if (sortCol === col) sortAsc = !sortAsc;
  else { sortCol = col; sortAsc = true; }
  render();
}

function clearFilters() {
  filters = { methods: new Set(), domains: new Set(), orgs: new Set(), yearMin: 2012, yearMax: 2024 };
  document.getElementById("yearMin").value = 2012;
  document.getElementById("yearMax").value = 2024;
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

function render() {
  buildCheckboxes("dd-method", allMethods, filters.methods, "method");
  buildCheckboxes("dd-domain", allDomains, filters.domains, "domain");
  buildCheckboxes("dd-org", allOrgs, filters.orgs, "org");

  document.getElementById("method-count").textContent = filters.methods.size ? "(" + filters.methods.size + ")" : "";
  document.getElementById("domain-count").textContent = filters.domains.size ? "(" + filters.domains.size + ")" : "";
  document.getElementById("org-count").textContent = filters.orgs.size ? "(" + filters.orgs.size + ")" : "";

  let rows = DATA.filter(matchesFilter);

  const key = { title: "Title", year: "Year", method: "Method", domain: "Domain", org: "Organization" }[sortCol];
  rows.sort((a, b) => {
    let va = (a[key] || "").toLowerCase(), vb = (b[key] || "").toLowerCase();
    if (sortCol === "year") { va = +a.Year; vb = +b.Year; }
    if (va < vb) return sortAsc ? -1 : 1;
    if (va > vb) return sortAsc ? 1 : -1;
    return 0;
  });

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
      return `<tr><td>${link}</td><td>${r.Year}</td><td>${methods}</td><td>${domains}</td><td>${orgs}</td></tr>`;
    }).join("");
  }

  document.getElementById("results-count").textContent = rows.length + " of " + DATA.length + " audits";
}

// Initialize
allMethods = countByField("Method", true);
allDomains = countByField("Domain", true);
allOrgs = countByField("Organization", true);
render();
