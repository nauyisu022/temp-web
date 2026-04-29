const state = {
  manifest: null,
  selectedIndex: 0,
  selectedCase: null,
  query: "",
  region: "",
  flag: "",
  density: "all",
  sort: "idx",
  outputMode: "final",
  stepPreset: "all",
};

const els = {
  liveBadge: document.getElementById("liveBadge"),
  searchInput: document.getElementById("searchInput"),
  regionSelect: document.getElementById("regionSelect"),
  sortSelect: document.getElementById("sortSelect"),
  flagSelect: document.getElementById("flagSelect"),
  densitySelect: document.getElementById("densitySelect"),
  caseCount: document.getElementById("caseCount"),
  selectedMeta: document.getElementById("selectedMeta"),
  caseList: document.getElementById("caseList"),
  caseKicker: document.getElementById("caseKicker"),
  caseTitle: document.getElementById("caseTitle"),
  sourceTitle: document.getElementById("sourceTitle"),
  sourceDescription: document.getElementById("sourceDescription"),
  runSummary: document.getElementById("runSummary"),
  metricNote: document.getElementById("metricNote"),
  metricTable: document.getElementById("metricTable"),
  outputNote: document.getElementById("outputNote"),
  stepGrid: document.getElementById("stepGrid"),
  stepPreset: document.getElementById("stepPreset"),
  outputMode: document.getElementById("outputMode"),
};

const metricRows = [
  ["reward", "reward"],
  ["live_reward", "live reward"],
  ["live_reward_delta_vs_no_live", "live Δ"],
  ["faithfulness", "faith"],
  ["search_value", "search"],
  ["live_search_value", "live search"],
  ["live_reranker_score", "reranker"],
  ["recall_match", "recall"],
  ["richness", "richness"],
  ["total_terms", "terms"],
  ["usp_value_count", "USP values"],
  ["long_tail_unique_count", "long-tail"],
  ["coverage_breadth_score", "cov score"],
  ["coverage_breadth_hack", "cov hack"],
  ["guarded_hack", "guarded"],
  ["single_char_hack", "single char"],
  ["policy_noise_hack", "policy"],
];

function fmt(value, digits = 3) {
  if (value === undefined || value === null || value === "") return "-";
  if (typeof value === "boolean") return value ? "yes" : "no";
  const num = Number(value);
  if (!Number.isFinite(num)) return String(value);
  if (Math.abs(num) >= 10 || Number.isInteger(num)) return String(Math.round(num * 100) / 100);
  return num.toFixed(digits);
}

function clsDelta(value) {
  const num = Number(value);
  if (!Number.isFinite(num) || Math.abs(num) < 0.0001) return "";
  return num > 0 ? "good" : "bad";
}

function stepList() {
  const steps = state.manifest.steps;
  if (state.stepPreset === "ends") return [steps[0], steps[steps.length - 1]];
  if (state.stepPreset === "key") return steps.filter((step) => [0, 20, 50, 70].includes(step));
  return steps;
}

function filteredCases() {
  const q = state.query.trim().toLowerCase();
  let rows = state.manifest.cases.filter((item) => {
    if (state.region && item.region !== state.region) return false;
    if (state.flag && !item.flags.includes(state.flag)) return false;
    if (state.density === "flagged" && item.flags.length === 0) return false;
    if (state.density === "live" && !item.has_live) return false;
    if (!q) return true;
    return [item.item_id, item.region, item.title, String(item.row_idx)]
      .join(" ")
      .toLowerCase()
      .includes(q);
  });

  rows = rows.slice();
  rows.sort((a, b) => {
    if (state.sort === "rewardDown") return a.reward_delta - b.reward_delta;
    if (state.sort === "rewardUp") return b.reward_delta - a.reward_delta;
    if (state.sort === "termsDown") return a.terms_delta - b.terms_delta;
    if (state.sort === "step70") return Number(b.step70_reward) - Number(a.step70_reward);
    return a.row_idx - b.row_idx;
  });
  return rows;
}

function trendClass(value) {
  const num = Number(value);
  if (!Number.isFinite(num)) return "";
  if (num >= 0.65) return "high";
  if (num >= 0.45) return "mid";
  return "low";
}

function renderCaseList() {
  const rows = filteredCases();
  els.caseCount.textContent = `${rows.length} / ${state.manifest.total_cases} cases`;
  const selectedPos = rows.findIndex((row) => row.row_idx === state.selectedIndex);
  els.selectedMeta.textContent = selectedPos >= 0 ? `#${selectedPos + 1}` : "-";
  els.caseList.innerHTML = "";
  const frag = document.createDocumentFragment();
  rows.forEach((item) => {
    const button = document.createElement("button");
    button.className = `case-row${item.row_idx === state.selectedIndex ? " active" : ""}`;
    button.dataset.idx = item.row_idx;
    const rewards = state.manifest.steps
      .map((step) => {
        const metrics = item.metrics_by_step[String(step)] || {};
        return `<span class="trend-cell ${trendClass(metrics.reward)}" title="step ${step}: ${fmt(metrics.reward)}"></span>`;
      })
      .join("");
    button.innerHTML = `
      <div class="case-row-title">
        <span>${escapeHtml(item.title || "(no title)")}</span>
        <span>${escapeHtml(item.region || "-")}</span>
      </div>
      <div class="case-row-sub">idx ${item.row_idx} · ${escapeHtml(item.item_id)} · Δreward ${fmt(item.reward_delta)} · Δterms ${fmt(item.terms_delta)}</div>
      <div class="trend-strip">${rewards}</div>
    `;
    button.addEventListener("click", () => selectCase(item.row_idx));
    frag.appendChild(button);
  });
  els.caseList.appendChild(frag);
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

async function selectCase(idx) {
  state.selectedIndex = Number(idx);
  history.replaceState(null, "", `#${state.selectedIndex}`);
  renderCaseList();
  els.stepGrid.innerHTML = '<div class="empty-state">Loading case...</div>';
  const response = await fetch(`./data/cases/${state.selectedIndex}.json`);
  state.selectedCase = await response.json();
  renderSelectedCase();
}

function renderSummary(item) {
  const steps = state.manifest.steps;
  const first = item.metrics_by_step[String(steps[0])] || {};
  const last = item.metrics_by_step[String(steps[steps.length - 1])] || {};
  const rows = [
    ["row", `#${item.row_idx}`],
    ["item", item.item_id],
    ["region", item.region],
    ["reward Δ", `<strong class="${clsDelta(item.reward_delta)}">${fmt(item.reward_delta)}</strong>`],
    ["terms Δ", `<strong class="${clsDelta(item.terms_delta)}">${fmt(item.terms_delta)}</strong>`],
    ["step0", `${fmt(first.reward)} / ${fmt(first.total_terms)} terms`],
    ["step70", `${fmt(last.reward)} / ${fmt(last.total_terms)} terms`],
    ["flags", item.flags.length ? item.flags.join(", ") : "clean"],
  ];
  els.runSummary.innerHTML = rows
    .map(([label, value]) => `<div class="summary-line"><span>${label}</span><strong>${value}</strong></div>`)
    .join("");
}

function renderSelectedCase() {
  const item = state.manifest.cases.find((row) => row.row_idx === state.selectedIndex);
  const data = state.selectedCase;
  if (!item || !data) return;
  els.caseKicker.textContent = `${data.region} · item ${data.item_id}`;
  els.caseTitle.textContent = data.title || "(no title)";
  els.sourceTitle.textContent = data.title || "";
  els.sourceDescription.textContent = data.description || data.source_text || "";
  renderSummary(item);
  renderMetricTable(data);
  renderStepGrid(data);
}

function renderMetricTable(data) {
  const steps = stepList();
  const hasLive = steps.some((step) => {
    const metrics = data.steps[String(step)]?.metrics || {};
    return metrics.live_available || metrics.live_reward !== undefined;
  });
  const rows = metricRows.filter(([key]) => hasLive || !key.startsWith("live_"));
  els.metricNote.textContent = hasLive ? "包含离线 live reranker 重打分" : "当前只包含训练时保存的 reward 指标";
  const head = `<thead><tr><th>metric</th>${steps.map((step) => `<th>step ${step}</th>`).join("")}</tr></thead>`;
  const body = rows
    .map(([key, label]) => {
      const cells = steps
        .map((step) => {
          const value = data.steps[String(step)]?.metrics?.[key];
          const flagClass = Number(value) > 0 && key.endsWith("_hack") ? " flag-on" : "";
          return `<td class="${flagClass}">${fmt(value)}</td>`;
        })
        .join("");
      return `<tr><td>${label}</td>${cells}</tr>`;
    })
    .join("");
  els.metricTable.innerHTML = `${head}<tbody>${body}</tbody>`;
}

function renderStepGrid(data) {
  const steps = stepList();
  els.stepGrid.style.setProperty("--step-count", String(steps.length));
  els.outputNote.textContent = `${steps.length} steps · ${state.outputMode}`;
  els.stepGrid.innerHTML = steps
    .map((step) => {
      const stepData = data.steps[String(step)];
      if (!stepData) return "";
      const metrics = stepData.metrics || {};
      const text =
        state.outputMode === "analysis"
          ? stepData.analysis || "(empty analysis)"
          : state.outputMode === "full"
            ? stepData.output || "(empty output)"
            : stepData.final || "(empty final)";
      const flags = stepData.flags || [];
      return `
        <article class="step-panel">
          <header class="step-panel-header">
            <div class="step-panel-title">
              <span>step ${step}</span>
              <span>${metrics.valid === false ? "invalid" : "valid"}</span>
            </div>
            <div class="step-stats">
              <span><strong>${fmt(metrics.reward)}</strong>reward</span>
              <span><strong>${fmt(metrics.faithfulness)}</strong>faith</span>
              <span><strong>${fmt(metrics.total_terms)}</strong>terms</span>
            </div>
            <div class="flag-row">
              ${flags.length ? flags.map((flag) => `<span class="flag bad">${escapeHtml(flag)}</span>`).join("") : '<span class="flag">clean</span>'}
            </div>
          </header>
          <pre class="step-output">${escapeHtml(text)}</pre>
        </article>
      `;
    })
    .join("");
}

function populateFilters() {
  els.regionSelect.innerHTML =
    '<option value="">全部</option>' +
    state.manifest.regions.map((region) => `<option value="${region}">${region}</option>`).join("");
}

function bindControls() {
  els.searchInput.addEventListener("input", (event) => {
    state.query = event.target.value;
    renderCaseList();
  });
  els.regionSelect.addEventListener("change", (event) => {
    state.region = event.target.value;
    renderCaseList();
  });
  els.sortSelect.addEventListener("change", (event) => {
    state.sort = event.target.value;
    renderCaseList();
  });
  els.flagSelect.addEventListener("change", (event) => {
    state.flag = event.target.value;
    renderCaseList();
  });
  els.densitySelect.addEventListener("change", (event) => {
    state.density = event.target.value;
    renderCaseList();
  });
  els.stepPreset.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-preset]");
    if (!button) return;
    state.stepPreset = button.dataset.preset;
    els.stepPreset.querySelectorAll("button").forEach((node) => node.classList.toggle("active", node === button));
    if (state.selectedCase) renderSelectedCase();
  });
  els.outputMode.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-mode]");
    if (!button) return;
    state.outputMode = button.dataset.mode;
    els.outputMode.querySelectorAll("button").forEach((node) => node.classList.toggle("active", node === button));
    if (state.selectedCase) renderStepGrid(state.selectedCase);
  });
  window.addEventListener("keydown", (event) => {
    if (event.target.matches("input, select")) return;
    const rows = filteredCases();
    const current = rows.findIndex((row) => row.row_idx === state.selectedIndex);
    if (event.key === "ArrowDown" && current < rows.length - 1) selectCase(rows[current + 1].row_idx);
    if (event.key === "ArrowUp" && current > 0) selectCase(rows[current - 1].row_idx);
  });
}

async function init() {
  const response = await fetch("./data/manifest.json");
  state.manifest = await response.json();
  const liveCount = state.manifest.live_steps_available?.length || 0;
  els.liveBadge.textContent = liveCount ? `live ${liveCount}/${state.manifest.steps.length}` : "no live";
  els.liveBadge.className = `status-pill ${liveCount ? "ready" : "pending"}`;
  populateFilters();
  bindControls();
  const hashIndex = Number(location.hash.replace("#", ""));
  const firstIndex = Number.isFinite(hashIndex) && hashIndex >= 0 ? hashIndex : 0;
  renderCaseList();
  await selectCase(firstIndex);
}

init().catch((error) => {
  console.error(error);
  els.stepGrid.innerHTML = `<div class="empty-state">${escapeHtml(error.message)}</div>`;
});
