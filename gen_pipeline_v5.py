#!/usr/bin/env python3
"""Generate pipeline_flowchart_v5.excalidraw with three-column parallel layout."""
import json
import random

random.seed(42)
elements = []
_id_counter = [0]

def uid():
    _id_counter[0] += 1
    return f"el_{_id_counter[0]:04d}"

def make_rect(x, y, w, h, stroke="#000", bg="#fff", stroke_width=2, style="solid", roundness=True):
    eid = uid()
    el = {
        "id": eid, "type": "rectangle",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": bg,
        "fillStyle": "solid", "strokeWidth": stroke_width,
        "strokeStyle": style, "roughness": 1, "opacity": 100,
        "groupIds": [], "frameId": None, "seed": random.randint(1000, 99999),
        "version": 2, "versionNonce": random.randint(1, 2**30),
        "isDeleted": False, "boundElements": [],
        "updated": 1778148713483, "link": None, "locked": False,
        "index": f"a{_id_counter[0]:03d}",
    }
    if roundness:
        el["roundness"] = {"type": 3}
    else:
        el["roundness"] = None
    elements.append(el)
    return eid

def make_text(x, y, text, font_size=14, color="#222", align="center", bold=False, w=None, family=3):
    eid = uid()
    width = w if w else len(text) * font_size * 0.6
    height = font_size * 1.4
    el = {
        "id": eid, "type": "text",
        "x": x, "y": y, "width": width, "height": height,
        "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
        "roughness": 1, "opacity": 100,
        "groupIds": [], "frameId": None, "roundness": None,
        "seed": random.randint(1000, 99999),
        "version": 2, "versionNonce": random.randint(1, 2**30),
        "isDeleted": False, "boundElements": [],
        "updated": 1778148713483, "link": None, "locked": False,
        "fontSize": font_size, "fontFamily": family,
        "text": text, "originalText": text,
        "textAlign": align, "verticalAlign": "top",
        "containerId": None, "lineHeight": 1.25,
        "index": f"a{_id_counter[0]:03d}", "autoResize": True,
    }
    if bold:
        el["fontWeight"] = "bold"
    elements.append(el)
    return eid

def make_arrow(x1, y1, x2, y2, color="#64748b", width=2, style="solid"):
    eid = uid()
    el = {
        "id": eid, "type": "arrow",
        "x": x1, "y": y1,
        "width": abs(x2 - x1), "height": abs(y2 - y1),
        "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": width,
        "strokeStyle": style, "roughness": 1, "opacity": 100,
        "groupIds": [], "frameId": None, "roundness": {"type": 2},
        "seed": random.randint(1000, 99999),
        "version": 2, "versionNonce": random.randint(1, 2**30),
        "isDeleted": False, "boundElements": [],
        "updated": 1778148713483, "link": None, "locked": False,
        "points": [[0, 0], [x2 - x1, y2 - y1]],
        "lastCommittedPoint": None,
        "startBinding": None, "endBinding": None,
        "startArrowhead": None, "endArrowhead": "arrow",
        "elbowed": False,
        "index": f"a{_id_counter[0]:03d}",
    }
    elements.append(el)
    return eid

# ═══════════════════════════════════════════════════════════════
# Layout constants
# ═══════════════════════════════════════════════════════════════
TOTAL_W = 1400
COL_W = 400
GAP = 50
L_X = 50          # Left column start
C_X = 500         # Center column start
R_X = 950         # Right column start
CENTER = TOTAL_W // 2 + 50  # Center of canvas

# Colors
GREEN = {"stroke": "#059669", "bg": "#d1fae5", "text": "#065f46", "title": "#059669"}
PINK = {"stroke": "#c62828", "bg": "#fce4ec", "text": "#4a148c", "title": "#c62828"}
ORANGE = {"stroke": "#ea580c", "bg": "#fff3e0", "text": "#c2410c", "title": "#ea580c"}
BLUE = {"stroke": "#1565c0", "bg": "#e3f2fd", "text": "#0d47a1", "title": "#1565c0"}
CYAN = {"stroke": "#0891b2", "bg": "#cffafe", "text": "#164e63", "title": "#0891b2"}
GRAY = {"stroke": "#64748b", "bg": "#f1f5f9", "text": "#334155", "title": "#1e40af"}

# ═══════════════════════════════════════════════════════════════
# Title
# ═══════════════════════════════════════════════════════════════
make_text(350, 20, "Title Optimization v9 Pipeline", 28, "#1e40af", "center", bold=True, w=700, family=1)
make_text(300, 58, "Shopee Google Ads · Three Parallel Lanes → Convergence", 13, "#888", "center", w=800)

# ═══════════════════════════════════════════════════════════════
# Row 0: Inputs
# ═══════════════════════════════════════════════════════════════
y = 95
make_rect(L_X, y, TOTAL_W, 55, GRAY["stroke"], GRAY["bg"])
make_text(L_X + 20, y + 8, "Inputs", 16, GRAY["title"], "left", bold=True, w=100, family=1)
make_text(L_X + 20, y + 30, "item Catalog · item with Performance · Search Terms (with Performance)", 12, GRAY["text"], "left", w=600)

# ═══════════════════════════════════════════════════════════════
# Row 1: Product Selection
# ═══════════════════════════════════════════════════════════════
y = 175
make_arrow(CENTER, 150, CENTER, y)
make_rect(CENTER - 180, y, 360, 50, "#64748b", "#fff3e0")
make_text(CENTER - 160, y + 8, "Product Selection", 16, "#222", "left", bold=True, w=200, family=1)
make_text(CENTER - 160, y + 30, "Choosing Items with CPO Improvement Space", 11, "#666", "left", w=320)

# Arrows from Product Selection to three columns
y_sel_bottom = y + 50
y_col_top = 280
make_arrow(CENTER - 100, y_sel_bottom, L_X + COL_W // 2, y_col_top)
make_arrow(CENTER, y_sel_bottom, C_X + COL_W // 2, y_col_top)
make_arrow(CENTER + 100, y_sel_bottom, R_X + COL_W // 2, y_col_top)

# ═══════════════════════════════════════════════════════════════
# LEFT COLUMN: Search Terms Processing
# ═══════════════════════════════════════════════════════════════
col_y = y_col_top
col_h = 580

# Column background
make_rect(L_X, col_y, COL_W, col_h, GREEN["stroke"], GREEN["bg"], stroke_width=3)
make_text(L_X + 15, col_y + 10, "Lane 1: Search Terms Processing", 16, GREEN["title"], "left", bold=True, w=350, family=1)

# Search Terms input
sy = col_y + 45
make_rect(L_X + 15, sy, COL_W - 30, 55, "#059669", "#ffffff")
make_text(L_X + 25, sy + 5, "Search Terms (with Performance)", 12, "#222", "left", bold=True, w=280)
make_text(L_X + 25, sy + 25, "good_terms · bad_terms · rerank_extra", 10, "#666", "left", w=300)

# Search Simulator
sy += 75
make_rect(L_X + 15, sy, COL_W - 30, 200, "#059669", "#e8f5e9")
make_text(L_X + 25, sy + 5, "Search Simulator", 14, GREEN["title"], "left", bold=True, w=200, family=1)

# Sub-steps inside simulator
ssy = sy + 30
make_rect(L_X + 25, ssy, COL_W - 50, 28, "#388e3c", "#fff")
make_text(L_X + 35, ssy + 6, "Word Segmentation", 11, "#222", "left", w=180)
ssy += 35
make_arrow(L_X + COL_W // 2, ssy - 7, L_X + COL_W // 2, ssy)
make_rect(L_X + 25, ssy, COL_W - 50, 35, "#388e3c", "#fff")
make_text(L_X + 35, ssy + 4, "Inverted Index", 11, "#222", "left", bold=True, w=150)
make_text(L_X + 35, ssy + 19, "BM25s + Qwen3 Semantic Emb", 9, "#666", "left", w=250)
ssy += 42
make_arrow(L_X + COL_W // 2, ssy - 7, L_X + COL_W // 2, ssy)
make_rect(L_X + 25, ssy, COL_W - 50, 28, "#388e3c", "#fff")
make_text(L_X + 35, ssy + 6, "Similarity Recall", 11, "#222", "left", w=180)
ssy += 35
make_arrow(L_X + COL_W // 2, ssy - 7, L_X + COL_W // 2, ssy)
make_rect(L_X + 25, ssy, COL_W - 50, 35, "#388e3c", "#fff")
make_text(L_X + 35, ssy + 4, "Relevance Re-ranking", 11, "#222", "left", bold=True, w=200)
make_text(L_X + 35, ssy + 19, "Qwen3 Reranker · Fine-tuned", 9, "#c62828", "left", w=250)

# Sorting
sy += 220
make_arrow(L_X + COL_W // 2, sy - 15, L_X + COL_W // 2, sy)
make_rect(L_X + 15, sy, COL_W - 30, 50, "#059669", "#ffffff")
make_text(L_X + 25, sy + 5, "Sorting", 13, GREEN["title"], "left", bold=True, w=100, family=1)
make_text(L_X + 25, sy + 25, "Conversion score × Relevance score", 10, "#666", "left", w=300)

# Data output
sy += 65
make_rect(L_X + 15, sy, COL_W - 30, 65, "#059669", "#ffffff", style="dashed")
make_text(L_X + 25, sy + 5, "Output → LLM", 11, GREEN["title"], "left", bold=True, w=150)
make_text(L_X + 25, sy + 22, "• Original Title + KSP", 10, "#555", "left", w=250)
make_text(L_X + 25, sy + 36, "• High-Relevance Good search terms", 10, "#555", "left", w=280)
make_text(L_X + 25, sy + 50, "• High-Relevance Bad search terms", 10, "#555", "left", w=280)

# Format annotation
make_text(L_X + COL_W - 50, sy + 50, ".pkl", 9, "#999", "left", w=40)

# ═══════════════════════════════════════════════════════════════
# CENTER COLUMN: KSP Extraction
# ═══════════════════════════════════════════════════════════════
col_y2 = y_col_top

# Column background
make_rect(C_X, col_y2, COL_W, col_h, PINK["stroke"], PINK["bg"], stroke_width=3)
make_text(C_X + 15, col_y2 + 10, "Lane 2: KSP Extraction", 16, PINK["title"], "left", bold=True, w=300, family=1)
make_text(C_X + 280, col_y2 + 12, "v9 changed", 11, "#c62828", "left", bold=True, w=100)

# 4-step CoT box
sy = col_y2 + 45
make_rect(C_X + 15, sy, COL_W - 30, 310, "#c62828", "#fff8f8")
make_text(C_X + 25, sy + 5, "4-Round Multi-turn CoT", 12, "#c62828", "left", bold=True, w=250)

# Step 1
ssy = sy + 28
make_rect(C_X + 25, ssy, COL_W - 50, 45, "#000", "#fff")
make_text(C_X + 35, ssy + 5, "Step 1: User Profile", 12, "#222", "left", bold=True, w=200)
make_text(C_X + 35, ssy + 24, "target user · search intent · select schema", 9, "#666", "left", w=300)

# Step 2
ssy += 55
make_arrow(C_X + COL_W // 2, ssy - 10, C_X + COL_W // 2, ssy)
make_rect(C_X + 25, ssy, COL_W - 50, 45, "#000", "#fff")
make_text(C_X + 35, ssy + 5, "Step 2: Keywords Extraction", 12, "#222", "left", bold=True, w=250)
make_text(C_X + 35, ssy + 24, "extract + expand search keywords by attribute", 9, "#666", "left", w=300)

# Step 3
ssy += 55
make_arrow(C_X + COL_W // 2, ssy - 10, C_X + COL_W // 2, ssy)
make_rect(C_X + 25, ssy, COL_W - 50, 45, "#000", "#fff")
make_text(C_X + 35, ssy + 5, "Step 3: Candidates Generation", 12, "#222", "left", bold=True, w=270)
make_text(C_X + 35, ssy + 24, "brand → USP → long_tail · n=5 candidates", 9, "#666", "left", w=300)

# Step 4
ssy += 55
make_arrow(C_X + COL_W // 2, ssy - 10, C_X + COL_W // 2, ssy)
make_rect(C_X + 25, ssy, COL_W - 50, 45, "#000", "#fff")
make_text(C_X + 35, ssy + 5, "Step 4: Evaluation & Selection", 12, "#222", "left", bold=True, w=270)
make_text(C_X + 35, ssy + 24, "4-dim scoring · pick best of 5 candidates", 9, "#666", "left", w=300)

# KSP output fields
ssy += 55
labels = ["Brand", "Product Type", "USP", "Long-tail KW"]
lx = C_X + 30
for lb in labels:
    make_rect(lx, ssy, 80, 24, "#000", "#fff")
    make_text(lx + 5, ssy + 5, lb, 9, "#222", "left", w=70)
    lx += 86

# Format annotation
make_text(C_X + COL_W - 60, ssy + 5, ".parquet", 9, "#999", "left", w=60)

# Product Information
sy = col_y2 + 380
make_arrow(C_X + COL_W // 2, sy - 10, C_X + COL_W // 2, sy)
make_rect(C_X + 15, sy, COL_W - 30, 80, "#c62828", "#ffffff")
make_text(C_X + 25, sy + 5, "Product Information", 13, PINK["title"], "left", bold=True, w=200, family=1)
make_rect(C_X + 25, sy + 28, 160, 40, "#000", "#f5f5f5")
make_text(C_X + 35, sy + 33, "Original Title", 10, "#222", "left", w=120)
make_text(C_X + 35, sy + 48, "+ Description", 10, "#666", "left", w=120)
make_rect(C_X + 200, sy + 28, 160, 40, "#000", "#f5f5f5")
make_text(C_X + 210, sy + 33, "Original Title", 10, "#222", "left", w=120)
make_text(C_X + 210, sy + 48, "+ KSP", 10, "#666", "left", w=120)

# Output to LLM
sy += 95
make_rect(C_X + 15, sy, COL_W - 30, 45, "#c62828", "#ffffff", style="dashed")
make_text(C_X + 25, sy + 5, "Output → LLM", 11, PINK["title"], "left", bold=True, w=150)
make_text(C_X + 25, sy + 22, "Product Info + KSP fields", 10, "#555", "left", w=250)

# ═══════════════════════════════════════════════════════════════
# RIGHT COLUMN: Expert Knowledge + Title Pattern
# ═══════════════════════════════════════════════════════════════
col_y3 = y_col_top

# Column background
make_rect(R_X, col_y3, COL_W, col_h, ORANGE["stroke"], ORANGE["bg"], stroke_width=3)
make_text(R_X + 15, col_y3 + 10, "Lane 3: Knowledge & Pattern", 16, ORANGE["title"], "left", bold=True, w=350, family=1)

# Cluster by ProductType
sy = col_y3 + 45
make_rect(R_X + 15, sy, COL_W - 30, 55, "#ea580c", "#ffffff")
make_text(R_X + 25, sy + 5, "Cluster by ProductType", 13, ORANGE["title"], "left", bold=True, w=250, family=1)
make_text(R_X + 25, sy + 25, "Group items by KSP product_type field", 10, "#666", "left", w=300)

# Title Pattern Generation
sy += 75
make_arrow(R_X + COL_W // 2, sy - 20, R_X + COL_W // 2, sy)
make_rect(R_X + 15, sy, COL_W - 30, 130, "#ea580c", "#fff8f0")
make_text(R_X + 25, sy + 5, "Title Pattern Generation", 13, ORANGE["title"], "left", bold=True, w=250, family=1)
make_text(R_X + COL_W - 70, sy + 7, "offline", 9, "#e65100", "left", bold=True, w=50)

make_rect(R_X + 25, sy + 30, COL_W - 50, 28, "#000", "#fff")
make_text(R_X + 35, sy + 36, "Mining Good / Bad Title Examples", 10, "#222", "left", w=280)
make_rect(R_X + 25, sy + 65, COL_W - 50, 28, "#000", "#fff")
make_text(R_X + 35, sy + 71, "Pattern Generation (LLM & CoT)", 10, "#222", "left", w=280)
make_text(R_X + 25, sy + 105, "→ SQLite DB", 10, "#999", "left", w=100)

# Expert Knowledge
sy += 150
make_arrow(R_X + COL_W // 2, sy - 20, R_X + COL_W // 2, sy)
make_rect(R_X + 15, sy, COL_W - 30, 130, "#ea580c", "#ffffff")
make_text(R_X + 25, sy + 5, "Expert Knowledge", 13, ORANGE["title"], "left", bold=True, w=200, family=1)
make_text(R_X + 25, sy + 28, "by cluster priority:", 11, "#555", "left", w=200)
make_text(R_X + 25, sy + 46, "1. Virtual Category (vc)", 11, "#555", "left", w=250)
make_text(R_X + 25, sy + 64, "2. L3 Category", 11, "#555", "left", w=200)
make_text(R_X + 25, sy + 82, "3. L2 Category", 11, "#555", "left", w=200)
make_text(R_X + 25, sy + 105, "Blacklist filtering applied", 9, "#999", "left", w=200)

# Output to LLM
sy += 145
make_rect(R_X + 15, sy, COL_W - 30, 45, "#ea580c", "#ffffff", style="dashed")
make_text(R_X + 25, sy + 5, "Output → LLM", 11, ORANGE["title"], "left", bold=True, w=150)
make_text(R_X + 25, sy + 22, "Merged EK + Title Patterns", 10, "#555", "left", w=250)

# ═══════════════════════════════════════════════════════════════
# CONVERGENCE: LLM Title Generator
# ═══════════════════════════════════════════════════════════════
llm_y = col_y + col_h + 50
llm_h = 200

# Arrows from three columns to LLM
make_arrow(L_X + COL_W // 2, col_y + col_h, L_X + COL_W // 2, llm_y)
make_arrow(C_X + COL_W // 2, col_y + col_h, C_X + COL_W // 2, llm_y)
make_arrow(R_X + COL_W // 2, col_y + col_h, R_X + COL_W // 2, llm_y)

# LLM box
make_rect(L_X, llm_y, TOTAL_W, llm_h, BLUE["stroke"], BLUE["bg"], stroke_width=3)
make_text(L_X + 20, llm_y + 10, "LLM Title Generator", 20, BLUE["title"], "left", bold=True, w=300, family=1)
make_text(L_X + 320, llm_y + 14, "v9 changed", 11, "#c62828", "left", bold=True, w=100)
make_text(L_X + 900, llm_y + 14, "GPT-5-mini · async · concurrency=200", 10, "#888", "left", w=300)

# Call 1
c1y = llm_y + 45
make_rect(L_X + 20, c1y, 640, 60, "#1565c0", "#ffffff")
make_text(L_X + 30, c1y + 5, "Call 1: Extract Facts + Policy", 13, BLUE["title"], "left", bold=True, w=300, family=1)
make_text(L_X + 30, c1y + 25, "brand · product_type · specs · core_usp · signals", 10, "#666", "left", w=400)
make_text(L_X + 30, c1y + 40, "→ select policy (max_len, structure rules, frontload)", 10, "#666", "left", w=450)

# Call 2
make_rect(L_X + 680, c1y, 680, 60, "#1565c0", "#ffffff")
make_text(L_X + 690, c1y + 5, "Call 2: Generate Optimized Title", 13, BLUE["title"], "left", bold=True, w=300, family=1)
make_text(L_X + 690, c1y + 25, "facts + policy + search terms + EK → N candidates", 10, "#666", "left", w=450)
make_text(L_X + 690, c1y + 40, "DAG scoring → select best candidate", 10, "#666", "left", w=350)

# Flow arrow between Call1 and Call2
make_arrow(L_X + 660, c1y + 30, L_X + 680, c1y + 30, BLUE["stroke"])

# Data flow description
make_text(L_X + 20, c1y + 75, "Data flow: Search Terms (Lane 1) + Product Info (Lane 2) → Call 1 → facts + policy → Call 2 ← EK (Lane 3)", 10, "#555", "left", w=900)

# Output
make_text(L_X + 20, c1y + 95, "Output: title_candidates_json → DAG selection → selected_candidate", 11, BLUE["text"], "left", bold=True, w=600)

# Format annotation
make_text(L_X + TOTAL_W - 100, c1y + 95, ".db (SQLite)", 9, "#999", "left", w=100)

# ═══════════════════════════════════════════════════════════════
# Blacklist Filter
# ═══════════════════════════════════════════════════════════════
bf_y = llm_y + llm_h + 40
make_arrow(CENTER, llm_y + llm_h, CENTER, bf_y)
make_rect(CENTER - 200, bf_y, 400, 55, CYAN["stroke"], CYAN["bg"])
make_text(CENTER - 180, bf_y + 5, "Blacklist Filter", 15, CYAN["title"], "left", bold=True, w=200, family=1)
make_text(CENTER - 180, bf_y + 28, "flashtext (Aho-Corasick) · CJK cleanup · Google GMC Policy", 10, "#666", "left", w=380)

# ═══════════════════════════════════════════════════════════════
# Output
# ═══════════════════════════════════════════════════════════════
out_y = bf_y + 75
make_arrow(CENTER, bf_y + 55, CENTER, out_y)
make_rect(CENTER - 130, out_y, 260, 50, "#2e7d32", "#e8f5e9", stroke_width=3)
make_text(CENTER - 110, out_y + 5, "Enhanced Title", 16, "#2e7d32", "left", bold=True, w=200, family=1)
make_text(CENTER - 110, out_y + 28, "→ Hive (Parquet)", 11, "#555", "left", w=150)

# Region support
make_text(CENTER - 180, out_y + 60, "BR · ID · MY · PH · SG · TH · TW · VN · MX · CO · CL · PL", 11, "#aaa", "center", w=360)

# ═══════════════════════════════════════════════════════════════
# Write output
# ═══════════════════════════════════════════════════════════════
doc = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://marketplace.visualstudio.com/items?itemName=pomdtr.excalidraw-editor",
    "elements": elements,
    "appState": {
        "gridSize": 20,
        "gridStep": 5,
        "gridModeEnabled": False,
        "viewBackgroundColor": "#ffffff"
    },
    "files": {}
}

with open("/Users/admin/git_repos/temp-web/pipeline_flowchart_v5.excalidraw", "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print(f"Generated {len(elements)} elements")
print(f"Canvas: {TOTAL_W}x{out_y + 120}px")
print("Output: pipeline_flowchart_v5.excalidraw")
