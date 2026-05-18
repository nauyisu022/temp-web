# Pipeline Flowchart Lanes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `pipeline_flowchart 1.html` so the major components are three parallel lanes that converge into `LLM Title Generator`, with KSP going directly to the title generator rather than through Search Simulator.

**Architecture:** This is a single-file canvas diagram update. The implementation should preserve the existing rough.js drawing style and component content while changing the high-level layout into three parallel lanes: Search Terms Processing, KSP Extraction, and Knowledge & Pattern. The bottom `LLM Title Generator`, `Blacklist Filter`, and `Enhanced Title` remain the convergence path.

**Tech Stack:** HTML canvas, JavaScript, rough.js CDN.

---

## File Structure

- Modify: `/Users/admin/git_repos/temp-web/pipeline_flowchart 1.html`
  - Responsible for all canvas sizing, drawing helper functions, layout constants, component rectangles, labels, and arrows.
- No new runtime files.
- No automated tests are expected for this static canvas diagram; verification is by opening the HTML in a browser and checking the rendered relationships.

---

### Task 1: Resize Canvas and Define Three-Lane Layout Constants

**Files:**
- Modify: `/Users/admin/git_repos/temp-web/pipeline_flowchart 1.html:17-70`

- [ ] **Step 1: Open the target HTML file**

Use the editor or `Read` tool to inspect `/Users/admin/git_repos/temp-web/pipeline_flowchart 1.html`.

- [ ] **Step 2: Increase canvas width for three parallel lanes**

Replace the current canvas size constants:

```js
const W = 1050, H = 1850;
```

with:

```js
const W = 1900, H = 1650;
```

- [ ] **Step 3: Replace center/right layout anchors with lane anchors**

Replace:

```js
const mx = 350;
const rx = 810;
```

with:

```js
const lane1X = 315;
const lane2X = 950;
const lane3X = 1585;
const laneW = 520;
const mx = lane2X;
const rx = lane3X;
```

- [ ] **Step 4: Save the file**

Save `/Users/admin/git_repos/temp-web/pipeline_flowchart 1.html`.

---

### Task 2: Convert the Top Section to Shared Inputs and Three Lane Fan-Out

**Files:**
- Modify: `/Users/admin/git_repos/temp-web/pipeline_flowchart 1.html:71-97`

- [ ] **Step 1: Replace the two separate input boxes with a single shared input band**

Replace the current Row 0 block:

```js
const y0 = 95;
rect(220, y0, 180, 42, C.input);
text('item Catalog', 310, y0 + 26, { font: '13px', bold: true });

rect(650, y0, 220, 42, C.input);
text('item with performance', 760, y0 + 26, { font: '13px', bold: true });

arrow(310, y0 + 42, 310, y0 + 70);
arrow(420, y0 + 15, 650, y0 + 15);
```

with:

```js
const y0 = 100;
rect(40, y0, W - 80, 70, C.input);
text('Inputs', 70, y0 + 25, { font: '16px', bold: true, color: '#0d47a1', align: 'left' });
text('item Catalog · item with Performance · Search Terms (with Performance)', 70, y0 + 52, { font: '13px', align: 'left' });
```

- [ ] **Step 2: Center product selection below the input band**

Replace the current Row 1 block:

```js
const y1 = 170;
rect(mx - 140, y1, 280, 55, C.select);
text('Product Selection', mx, y1 + 22, { font: '15px', bold: true });
text('Choosing Items with CPO Improvement Space', mx, y1 + 42, { font: '11px', color: '#666' });

arrow(mx, y1 + 55, mx, y1 + 85);
```

with:

```js
const y1 = 205;
rect(mx - 240, y1, 480, 62, C.select);
text('Product Selection', mx, y1 + 25, { font: '16px', bold: true });
text('Choosing Items with CPO Improvement Space', mx, y1 + 47, { font: '12px', color: '#666' });
arrow(mx, y0 + 70, mx, y1);
```

- [ ] **Step 3: Add fan-out arrows from Product Selection to the three lanes**

Immediately after the product selection block, add:

```js
const laneTopY = 335;
arrow(mx - 130, y1 + 62, lane1X, laneTopY);
arrow(mx, y1 + 62, lane2X, laneTopY);
arrow(mx + 130, y1 + 62, lane3X, laneTopY);
```

- [ ] **Step 4: Save the file**

Save `/Users/admin/git_repos/temp-web/pipeline_flowchart 1.html`.

---

### Task 3: Rebuild Lane 1 as Search Terms Processing with Search Simulator and Sorting

**Files:**
- Modify: `/Users/admin/git_repos/temp-web/pipeline_flowchart 1.html:191-257`

- [ ] **Step 1: Move Search Terms into Lane 1**

Use the existing `Search Terms`, `Search Simulator`, `Sorting`, and data annotation drawing code as the source content, but place it inside a Lane 1 container.

Add this Lane 1 container and heading before drawing the Lane 1 components:

```js
const laneY = laneTopY;
const laneH = 750;
rect(lane1X - laneW / 2, laneY, laneW, laneH, C.sim, { stroke: '#00897b', strokeWidth: 2 });
text('Lane 1: Search Terms Processing', lane1X - laneW / 2 + 20, laneY + 28, { font: '17px', bold: true, color: '#00796b', align: 'left' });
```

- [ ] **Step 2: Draw Search Terms at the top of Lane 1**

```js
const stY = laneY + 60;
rect(lane1X - 230, stY, 460, 70, C.white, { stroke: '#00897b' });
text('Search Terms (with Performance)', lane1X - 210, stY + 24, { font: '13px', bold: true, align: 'left' });
text('good_terms · bad_terms · rerank_extra', lane1X - 210, stY + 48, { font: '11px', color: '#666', align: 'left' });
```

- [ ] **Step 3: Reposition Search Simulator below Search Terms within Lane 1**

Set:

```js
const y4 = stY + 100;
const ssW = 460, ssH = 270;
```

Then update every Search Simulator coordinate in the existing block from `mx` to `lane1X`, keeping the same relative offsets. For example:

```js
rect(lane1X - ssW/2, y4, ssW, ssH, C.sim, { stroke: '#00897b' });
text('Search Simulator', lane1X, y4 + 24, { font: '16px', bold: true });
```

Use `lane1X` for the word segmentation, inverted index, similarity recall, and relevance reranking boxes.

- [ ] **Step 4: Connect Search Terms to both word segmentation boxes**

Replace the old arrows from Product Information/Search Terms into Search Simulator with:

```js
arrow(lane1X - 110, stY + 70, lane1X - 105, y4);
arrow(lane1X + 110, stY + 70, lane1X + 105, y4);
```

- [ ] **Step 5: Place Sorting and LLM data output inside Lane 1**

Set:

```js
const y5 = y4 + ssH + 35;
```

Draw sorting centered on `lane1X`:

```js
rect(lane1X - 180, y5, 360, 45, C.white, { stroke: '#00897b' });
text('Sorting', lane1X - 160, y5 + 18, { font: '13px', bold: true, color: '#00796b', align: 'left' });
text('Conversion score × Relevance score', lane1X - 160, y5 + 36, { font: '11px', color: '#555', align: 'left' });
arrow(lane1X, y4 + ssH, lane1X, y5);
```

Set:

```js
const y5b = y5 + 70;
const dataBoxW = 460, dataBoxH = 85;
```

Draw the data output centered on `lane1X`:

```js
rect(lane1X - dataBoxW/2, y5b, dataBoxW, dataBoxH, C.white, { stroke: '#00897b' });
text('Output → LLM', lane1X - dataBoxW/2 + 18, y5b + 22, { font: '13px', bold: true, color: '#00796b', align: 'left' });
text('Original Title + KSP', lane1X - dataBoxW/2 + 18, y5b + 44, { font: '11px', color: '#555', align: 'left' });
text('High-Relevance Good search terms', lane1X - dataBoxW/2 + 18, y5b + 60, { font: '11px', color: '#555', align: 'left' });
text('High-Relevance Bad search terms', lane1X - dataBoxW/2 + 18, y5b + 76, { font: '11px', color: '#555', align: 'left' });
arrow(lane1X, y5 + 45, lane1X, y5b);
fmt('.pkl', lane1X + dataBoxW/2 + 8, y5b + 70);
```

- [ ] **Step 6: Save the file**

Save `/Users/admin/git_repos/temp-web/pipeline_flowchart 1.html`.

---

### Task 4: Rebuild Lane 2 as KSP Extraction with Direct Output to LLM

**Files:**
- Modify: `/Users/admin/git_repos/temp-web/pipeline_flowchart 1.html:98-190`

- [ ] **Step 1: Wrap KSP content in a Lane 2 container**

Replace the standalone KSP container setup:

```js
const y2 = 265;
const kw = 380, kh = 290;
rect(mx - kw/2, y2, kw, kh, C.ksp);
```

with:

```js
const y2 = laneY;
const kw = 460, kh = 430;
rect(lane2X - laneW / 2, laneY, laneW, laneH, C.ksp, { stroke: '#c62828', strokeWidth: 2 });
text('Lane 2: KSP Extraction', lane2X - laneW / 2 + 20, laneY + 28, { font: '17px', bold: true, color: '#c62828', align: 'left' });
rect(lane2X - kw/2, y2 + 60, kw, kh, C.white, { stroke: '#c62828' });
```

- [ ] **Step 2: Move KSP title text into the inner KSP box**

Replace:

```js
text('Product KSP Extraction', mx, y2 + 22, { font: '15px', bold: true });
text('4-Round Multi-turn CoT', mx, y2 + 40, { font: '11px', bold: true, color: '#c62828' });
```

with:

```js
text('Product KSP Extraction', lane2X, y2 + 86, { font: '15px', bold: true, color: '#c62828' });
text('4-Round Multi-turn CoT', lane2X, y2 + 106, { font: '11px', bold: true, color: '#c62828' });
```

- [ ] **Step 3: Reposition all KSP internal boxes around `lane2X`**

Set:

```js
const stepX = lane2X - kw/2 + 20;
const stepW = kw - 40;
const stepH = 42;
const stepGap = 14;
let sy = y2 + 125;
```

Then replace uses of `mx` in the KSP step boxes and output labels with `lane2X`.

- [ ] **Step 4: Draw Product Information below KSP inside Lane 2**

After the KSP output field labels, add:

```js
const piY = y2 + 520;
rect(lane2X - 230, piY, 460, 105, C.white, { stroke: '#c62828' });
text('Product Information', lane2X - 210, piY + 24, { font: '13px', bold: true, color: '#c62828', align: 'left' });
rect(lane2X - 200, piY + 42, 180, 45, C.white);
text('Original Title', lane2X - 110, piY + 60, { font: '10px' });
text('+ Description', lane2X - 110, piY + 76, { font: '10px' });
rect(lane2X + 20, piY + 42, 180, 45, C.white);
text('Original Title', lane2X + 110, piY + 60, { font: '10px' });
text('+ KSP', lane2X + 110, piY + 76, { font: '10px' });
arrow(lane2X, y2 + 60 + kh, lane2X, piY);
```

- [ ] **Step 5: Draw explicit KSP output-to-LLM box inside Lane 2**

Below Product Information, add:

```js
const kspOutY = piY + 125;
rect(lane2X - 230, kspOutY, 460, 70, C.white, { stroke: '#c62828' });
text('Output → LLM', lane2X - 210, kspOutY + 24, { font: '13px', bold: true, color: '#c62828', align: 'left' });
text('Product Info + KSP fields', lane2X - 210, kspOutY + 48, { font: '11px', color: '#555', align: 'left' });
arrow(lane2X, piY + 105, lane2X, kspOutY);
```

- [ ] **Step 6: Remove old KSP-to-Product-Information and item-performance-to-Search-Terms arrows**

Delete the old Row 3 `Product Information + Search Terms` block and its arrows that originally connected KSP to Product Information and `item with performance` to Search Terms. Those responsibilities now live inside Lane 1 and Lane 2.

- [ ] **Step 7: Save the file**

Save `/Users/admin/git_repos/temp-web/pipeline_flowchart 1.html`.

---

### Task 5: Rebuild Lane 3 as Knowledge & Pattern

**Files:**
- Modify: `/Users/admin/git_repos/temp-web/pipeline_flowchart 1.html:154-162` and `/Users/admin/git_repos/temp-web/pipeline_flowchart 1.html:287-314`

- [ ] **Step 1: Add Lane 3 container and heading**

Before drawing cluster/pattern/expert knowledge, add:

```js
rect(lane3X - laneW / 2, laneY, laneW, laneH, C.pattern, { stroke: '#ef6c00', strokeWidth: 2 });
text('Lane 3: Knowledge & Pattern', lane3X - laneW / 2 + 20, laneY + 28, { font: '17px', bold: true, color: '#e65100', align: 'left' });
```

- [ ] **Step 2: Move Cluster by ProductType to top of Lane 3**

Replace the old `cy2` block with:

```js
const cy2 = laneY + 60;
rect(lane3X - 230, cy2, 460, 75, C.white, { stroke: '#ef6c00' });
text('Cluster by ProductType', lane3X - 210, cy2 + 25, { font: '13px', bold: true, color: '#e65100', align: 'left' });
text('Group items by KSP product_type field', lane3X - 210, cy2 + 52, { font: '11px', color: '#666', align: 'left' });
```

- [ ] **Step 3: Move Title Pattern Generation under Cluster**

Replace the old `tpY` block with:

```js
const tpY = cy2 + 110;
rect(lane3X - 230, tpY, 460, 150, C.white, { stroke: '#ef6c00' });
text('Title Pattern Generation', lane3X - 210, tpY + 25, { font: '13px', bold: true, color: '#e65100', align: 'left' });
text('offline', lane3X + 185, tpY + 25, { font: '9px', bold: true, color: '#e65100' });
rect(lane3X - 205, tpY + 45, 410, 32, C.white);
text('Mining Good / Bad Title Examples', lane3X, tpY + 66, { font: '10px' });
rect(lane3X - 205, tpY + 88, 410, 32, C.white);
text('Pattern Generation (LLM & CoT)', lane3X, tpY + 109, { font: '10px' });
text('→ SQLite DB', lane3X - 210, tpY + 135, { font: '9px', color: '#999', align: 'left' });
arrow(lane3X, cy2 + 75, lane3X, tpY);
```

- [ ] **Step 4: Move Expert Knowledge under Title Pattern Generation**

Replace the old `ekY` block with:

```js
const ekY = tpY + 185;
rect(lane3X - 230, ekY, 460, 140, C.white, { stroke: '#ef6c00' });
text('Expert Knowledge', lane3X - 210, ekY + 25, { font: '13px', bold: true, color: '#e65100', align: 'left' });
text('by cluster priority:', lane3X - 210, ekY + 52, { font: '11px', color: '#555', align: 'left' });
text('1. Product Type', lane3X - 210, ekY + 74, { font: '11px', color: '#555', align: 'left' });
text('2. L3 Category', lane3X - 210, ekY + 94, { font: '11px', color: '#555', align: 'left' });
text('3. L2 Category', lane3X - 210, ekY + 114, { font: '11px', color: '#555', align: 'left' });
arrow(lane3X, tpY + 150, lane3X, ekY);
```

- [ ] **Step 5: Add Lane 3 output box**

Below Expert Knowledge, add:

```js
const ekOutY = ekY + 175;
rect(lane3X - 230, ekOutY, 460, 70, C.white, { stroke: '#ef6c00' });
text('Output → LLM', lane3X - 210, ekOutY + 24, { font: '13px', bold: true, color: '#e65100', align: 'left' });
text('Merged EK + Title Patterns', lane3X - 210, ekOutY + 48, { font: '11px', color: '#555', align: 'left' });
arrow(lane3X, ekY + 140, lane3X, ekOutY);
```

- [ ] **Step 6: Remove the old horizontal Expert Knowledge to LLM arrow**

Delete:

```js
const ekArrowY = ekY + 48;
arrow(rx - 120, ekArrowY, mx + lgW / 2, ekArrowY);
```

- [ ] **Step 7: Save the file**

Save `/Users/admin/git_repos/temp-web/pipeline_flowchart 1.html`.

---

### Task 6: Move LLM Title Generator to the Convergence Area

**Files:**
- Modify: `/Users/admin/git_repos/temp-web/pipeline_flowchart 1.html:259-285` and `/Users/admin/git_repos/temp-web/pipeline_flowchart 1.html:315-335`

- [ ] **Step 1: Place LLM Title Generator below all three lanes**

Replace:

```js
const y6 = y5b + dataBoxH + 20;
const lgW = 380, lgH = 170;
rect(mx - lgW/2, y6, lgW, lgH, C.llm);
```

with:

```js
const y6 = laneY + laneH + 70;
const lgW = 1450, lgH = 210;
rect(mx - lgW/2, y6, lgW, lgH, C.llm, { stroke: '#1565c0', strokeWidth: 2 });
```

- [ ] **Step 2: Update LLM internal layout for the wider box**

Replace the two vertically stacked call boxes with horizontal call boxes:

```js
text('LLM Title Generator', mx - lgW/2 + 35, y6 + 32, { font: '20px', bold: true, color: '#1565c0', align: 'left' });
text('GPT-5-mini · async · concurrency=200', mx + lgW/2 - 35, y6 + 32, { font: '10px', color: '#888', align: 'right' });

rect(mx - lgW/2 + 40, y6 + 60, 620, 78, C.white);
text('Call 1: Extract Facts + Policy', mx - lgW/2 + 60, y6 + 84, { font: '13px', bold: true, color: '#1565c0', align: 'left' });
text('brand · product_type · specs · core_usp · signals', mx - lgW/2 + 60, y6 + 108, { font: '10px', color: '#666', align: 'left' });
text('→ select policy (max_len, structure rules, frontload)', mx - lgW/2 + 60, y6 + 126, { font: '10px', color: '#666', align: 'left' });

arrow(mx - 30, y6 + 99, mx + 30, y6 + 99);

rect(mx + 80, y6 + 60, 670, 78, C.white);
text('Call 2: Generate Optimized Title', mx + 105, y6 + 84, { font: '13px', bold: true, color: '#1565c0', align: 'left' });
text('facts + policy + search terms + EK → N candidates', mx + 105, y6 + 108, { font: '10px', color: '#666', align: 'left' });
text('DAG scoring → select best candidate', mx + 105, y6 + 126, { font: '10px', color: '#666', align: 'left' });

text('Data flow: Search Terms (Lane 1) + Product Info (Lane 2) → Call 1 → facts + policy → Call 2 ← EK (Lane 3)', mx - lgW/2 + 40, y6 + 170, { font: '11px', color: '#555', align: 'left' });
text('Output: title_candidates_json → DAG selection → selected_candidate', mx - lgW/2 + 40, y6 + 190, { font: '11px', color: '#0d47a1', align: 'left' });
```

- [ ] **Step 3: Connect all three lanes directly to LLM Title Generator**

After the LLM box is drawn, add:

```js
arrow(lane1X, laneY + laneH, lane1X, y6);
arrow(lane2X, laneY + laneH, lane2X, y6);
arrow(lane3X, laneY + laneH, lane3X, y6);
```

These arrows are the key relationship: KSP (`lane2X`) goes directly into the LLM, not through Search Simulator.

- [ ] **Step 4: Move Blacklist Filter and Enhanced Title below the wide LLM box**

Set:

```js
const y7 = y6 + lgH + 55;
```

Keep the existing Blacklist Filter content centered on `mx`.

Set:

```js
const y8 = y7 + 90;
```

Keep the existing Enhanced Title output centered on `mx`.

- [ ] **Step 5: Remove old vertical arrows that assumed single-column flow**

Delete or replace arrows that connect:

```js
arrow(mx, y5b + dataBoxH, mx, y6);
arrow(mx, y6 + lgH, mx, y7);
arrow(mx, y7 + 60, mx, y8);
```

Keep only the updated LLM-to-filter and filter-to-output arrows:

```js
arrow(mx, y6 + lgH, mx, y7);
arrow(mx, y7 + 60, mx, y8);
```

- [ ] **Step 6: Save the file**

Save `/Users/admin/git_repos/temp-web/pipeline_flowchart 1.html`.

---

### Task 7: Clean Up Old Highlight Boxes and Verify Rendered Diagram

**Files:**
- Modify: `/Users/admin/git_repos/temp-web/pipeline_flowchart 1.html:337-346`

- [ ] **Step 1: Update v9 highlight boxes to match new lane positions**

Replace the old highlight block:

```js
rc.rectangle(mx - kw/2 - 6, y2 - 6, kw + 12, kh + 12, redDash);
text('v9 changed', mx + kw/2 + 20, y2 + 15, { font: '11px', bold: true, color: '#c62828', align: 'left' });

rc.rectangle(mx - lgW/2 - 6, y6 - 6, lgW + 12, lgH + 12, redDash);
text('v9 changed', mx + lgW/2 + 20, y6 + 15, { font: '11px', bold: true, color: '#c62828', align: 'left' });
```

with:

```js
rc.rectangle(lane2X - laneW / 2 + 8, laneY + 8, laneW - 16, laneH - 16, redDash);
text('v9 changed', lane2X + laneW / 2 - 105, laneY + 28, { font: '11px', bold: true, color: '#c62828', align: 'left' });

rc.rectangle(mx - lgW/2 - 6, y6 - 6, lgW + 12, lgH + 12, redDash);
text('v9 changed', mx + lgW/2 - 100, y6 + 20, { font: '11px', bold: true, color: '#c62828', align: 'left' });
```

- [ ] **Step 2: Open the HTML locally**

Run:

```bash
open "/Users/admin/git_repos/temp-web/pipeline_flowchart 1.html"
```

Expected: the browser opens the updated canvas diagram.

- [ ] **Step 3: Visual verification checklist**

Confirm all of the following are true:

```text
- The diagram has three parallel large lanes above the LLM Title Generator.
- Lane 1 contains Search Terms, Search Simulator, Sorting, and Output → LLM.
- Lane 2 contains Product KSP Extraction, Product Information, and Output → LLM.
- Lane 3 contains Cluster, Title Pattern Generation, Expert Knowledge, and Output → LLM.
- All three lanes connect directly downward into LLM Title Generator.
- KSP does not have an arrow into Search Simulator.
- LLM Title Generator connects to Blacklist Filter and then Enhanced Title.
- No arrows or labels visibly overlap important text.
```

- [ ] **Step 4: If browser verification shows overlap, adjust only spacing constants**

Prefer changing these constants rather than rewriting component logic:

```js
const W = 1900, H = 1650;
const lane1X = 315;
const lane2X = 950;
const lane3X = 1585;
const laneW = 520;
const laneH = 750;
const y6 = laneY + laneH + 70;
```

- [ ] **Step 5: Do not commit unless explicitly requested**

Leave the working tree modified. The user did not request a git commit.

---

## Self-Review

- Spec coverage: The plan covers the requested A layout: three parallel big components, convergence into `LLM Title Generator`, and explicit KSP direct-to-LLM output.
- Placeholder scan: No `TBD`, `TODO`, or unspecified implementation steps remain.
- Type consistency: The plan consistently uses `lane1X`, `lane2X`, `lane3X`, `laneW`, `laneY`, `laneH`, `mx`, and `rx` as JavaScript layout constants.
