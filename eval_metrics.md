# 评测指标说明

本文档说明 KSP 评测中的核心指标含义及计算逻辑。

---

## 1. 一致率（identical_rate）

**定义**：KSP 短语与搜索词库中某个搜索词**完全一致**（或词干化后一致）的比例。

**计算逻辑**：
- 对每个 KSP 短语调用 `exact_lookup`：
  - **identical**：字符串完全相等（如 `caderno` = `caderno`）
  - **stem_identical**：词干化后相等（如 `cadernos` 与 `caderno`）
- `identical_rate` = 命中的短语数 / 总短语数

**衡量内容**：模型生成的短语有多少与真实用户搜索词**完全一致**，要求最严格。

---

## 2. 短语命中率（hit_rate_phrase）

**定义**：KSP 短语能被搜索词库**匹配到**（含子串、词干等）的比例。

**计算逻辑**：
- 对每个 KSP 短语调用 `search`：
  - **exact**：KSP 短语是某个搜索词的子串（如 `vestido praia` 在 `vestido de praia feminino` 中）
  - **stem**：词干化后 KSP 是搜索词的子串
- `hit_rate_phrase` = 有匹配的短语数 / 总短语数

**衡量内容**：模型生成的短语有多少能被索引/搜索命中，比一致率更宽松。

---

## 3. 两者区别

| 维度 | 一致率 | 短语命中率 |
|------|--------|------------|
| 严格程度 | 更严格：必须完全等于搜索词 | 更宽松：子串/词干匹配即可 |
| 衡量内容 | 与真实搜索词的一致性 | 能否被搜索/索引命中 |
| 业务含义 | 是否贴近用户真实搜索习惯 | 是否可被检索到 |

**举例**：
- 搜索词库有：`saída de praia feminina`
- KSP 短语：`saída de praia`
  - 一致率：❌ 不相等，不计入
  - 短语命中率：✅ 是子串，计入命中

---

## 4. 相关代码

- 评测逻辑：`eval/batch_evaluator.py`
- 搜索词库匹配：`eval/search_library.py`（`exact_lookup`、`search`）
- KSP 短语提取：`eval/ksp_utils.py`（`extract_ksp_terms`）


# 500 条同数据源公平对比

**数据源**：`data/preprocessed_BR_first500.csv`（preprocessed_BR 前 500 行）

**Qwen 结果文件**：`outputs/selling_points_BR_qwen_nothink-new.csv`  
**Gemini 结果文件**：`outputs/output_api_500_merged/selling_points_BR_500_merged.csv`

**评测时间**：2026-02-24

---

## 指标对比

| 指标 | Qwen3-8B nothink | Gemini 2.5 Flash | 差距 |
|------|------------------|------------------|------|
| 商品数 | 499 | 500 | — |
| 一致率 | 30.2% | 35.8% | -5.6pp |
| 短语命中率 | 48.1% | 56.3% | -8.2pp |
| 单词命中率 | 96.7% | 96.6% | +0.1pp |
| FactScore | 62.9% | 67.8% | -4.9pp |
| L1 品牌品类一致率 | 66.1% | 76.7% | -10.6pp |
| L2 USP 一致率 | 30.6% | 32.1% | -1.5pp |
| L3 长尾词一致率 | 18.2% | 33.3% | -15.1pp |

> 注：L1/L2/L3 为**一致率**（identical_rate）按层统计，非短语命中率。

### L1/L2/L3 数据来源

L1/L2/L3 为**按层统计的一致率**（identical_rate），来自 eval 的 `layer_stats`：

1. **KSP 分层**（`eval/ksp_utils.py`）：
   - **L1 品牌品类**：`top_attractiveness`（brand、product_type、compatibility）
   - **L2 USP**：`unique_selling_points` 下各属性
   - **L3 长尾词**：`long_tail_keywords`

2. **计算方式**（`eval/batch_evaluator.py`）：
   - 对每个 KSP 短语记录其 layer（如 `Layer1_品牌品类`、`Layer2_USP`、`Layer3_长尾词`）
   - 按 layer 聚合：`identical + stem_identical` 为命中数，`total` 为该层短语总数
   - **Lx 一致率** = (identical + stem_identical) / total

3. **数据文件**：
   - Qwen: `eval_results/eval_qwen_nothink_first500/summary_selling_points_BR_qwen_nothink-new.json` → `layer_stats`
   - Gemini: `eval_results/eval_gemini_500/summary_selling_points_BR_500_merged.json` → `layer_stats`

---

## 结论

- 同数据、同 500 条下，Gemini 2.5 Flash 各项均优于 Qwen3-8B nothink。
- 差距最大：L3 长尾词一致率（-15.1pp）、L1 品牌品类一致率（-10.6pp）、短语命中率（-8.2pp）。
- 单词命中率两者接近；一致率、FactScore、L2 为小幅落后。

---

## 对应 eval 目录

- Qwen: `eval_results/eval_qwen_nothink_first500/`
- Gemini: `eval_results/eval_gemini_500/`
