# 500 条同数据源公平对比

**数据源**：`data/preprocessed_BR_first500.csv`（preprocessed_BR 前 500 行）

**结果文件**：
- Qwen3-4B: `outputs/selling_points_BR_4b.csv`
- Qwen3.5: `outputs/selling_points_BR_qwen3.5.csv`
- Qwen3.5-new: `outputs/selling_points_BR_qwen3.5-new.csv`（含 matched_schema）
- Qwen2.5-7B: `outputs/selling_points_BR_qwen2.5-7b.csv`
- Qwen2.5-14B: `outputs/selling_points_BR_qwen2.5-14b.csv`
- Qwen3-8B nothink: `outputs/selling_points_BR_qwen_nothink-new.csv`
- Qwen3-32B: `outputs/selling_points_BR_qwen3-32b.csv`
- Gemini 2.5 Flash: `outputs/output_api_500_merged/selling_points_BR_500_merged.csv`

**评测时间**：2026-02-24

---

## Top 4 对比（Gemini 2.5 Flash > Qwen2.5-7B > Qwen2.5-14B > Qwen3-8B nothink）

| 指标 | Qwen3-8B nothink | Qwen2.5-7B | Qwen2.5-14B | Gemini 2.5 Flash |
|------|------------------|------------|-------------|------------------|
| 商品数 | 499 | 500 | 500 | 500 |
| 一致率 | 30.2% | 34.4% | 33.2% | 35.8% |
| 短语命中率 | 48.1% | 54.4% | 53.0% | 56.3% |
| 单词命中率 | 96.7% | 95.6% | 96.5% | 96.6% |
| FactScore | 62.9% | 64.9% | 66.0% | 67.8% |
| L1 品牌品类一致率 | 66.1% | 71.1% | 69.9% | 76.7% |
| L2 USP 一致率 | 30.6% | 30.2% | 29.1% | 32.1% |
| L3 长尾词一致率 | 18.2% | 32.5% | 29.8% | 33.3% |

---

## 全量指标对比

| 指标 | Qwen3-4B | Qwen3.5 | Qwen3.5-new | Qwen3-32B | Qwen2.5-7B | Qwen2.5-14B | Qwen3-8B nothink | Gemini 2.5 Flash |
|------|----------|---------|-------------|-----------|------------|-------------|------------------|------------------|
| 商品数 | 500 | 500 | 500 | 500 | 500 | 500 | 499 | 500 |
| 一致率 | 19.3% | 19.8% | 18.5% | 23.5% | 34.4% | 33.2% | 30.2% | 35.8% |
| 短语命中率 | 34.0% | 32.4% | 33.9% | 43.5% | 54.4% | 53.0% | 48.1% | 56.3% |
| 单词命中率 | 96.5% | 96.5% | 96.4% | 96.7% | 95.6% | 96.5% | 96.7% | 96.6% |
| FactScore | 61.7% | 63.3% | 60.8% | 57.1% | 64.9% | 66.0% | 62.9% | 67.8% |
| L1 品牌品类一致率 | 54.8% | 56.7% | 52.5% | 60.5% | 71.1% | 69.9% | 66.1% | 76.7% |
| L2 USP 一致率 | 20.1% | 21.3% | 19.7% | 24.4% | 30.2% | 29.1% | 30.6% | 32.1% |
| L3 长尾词一致率 | 8.2% | 7.5% | 7.2% | 11.1% | 32.5% | 29.8% | 18.2% | 33.3% |

> 注：Qwen3-8B 为 499 条，其余模型均为 500 条。

---

## 结论

- 同数据、同 500 条下，**Gemini 2.5 Flash > Qwen2.5-7B > Qwen2.5-14B > Qwen3-8B nothink > Qwen3-32B > Qwen3.5 ≈ Qwen3-4B > Qwen3.5-new**。
- 4B 与 3.5 接近：3.5 在一致率、FactScore、L1 略高，4B 在短语命中率、L3 略高。
- 3.5-new（含 matched_schema）略低于 3.5：一致率 -1.3pp、FactScore -2.5pp、L1 -4.2pp。
- **Qwen2.5-7B** 表现突出：一致率 34.4%、L3 长尾词 32.5%，均优于 Qwen3-8B，接近 Gemini。
- **Qwen2.5-14B**（500 条）：一致率 33.2%，介于 8B 与 7B 之间，优于 8B 约 +3.0pp。
- **Qwen3-32B**：一致率 23.5%，低于 8B（-6.7pp），可能因 prompt/配置不同。
- 4B/3.5 与 8B 差距：一致率约 -10pp、短语命中率约 -15pp、L3 长尾词约 -10pp。
- 8B 与 Gemini 差距：一致率 -5.6pp、L3 长尾词 -15.1pp、L1 品牌品类 -10.6pp。
- 单词命中率各模型接近（约 96.5%）。

---

## 对应 eval 目录

- Qwen3-4B: `eval_results/eval_4b_500/`
- Qwen3.5: `eval_results/eval_qwen3.5_500/`
- Qwen3.5-new: `eval_results/eval_qwen3.5_new_500/`
- Qwen2.5-7B: `eval_results/eval_qwen2.5_7b_500/`
- Qwen2.5-14B: `eval_results/eval_qwen2.5_14b_500/`
- Qwen3-8B: `eval_results/eval_qwen_nothink_first500/`
- Qwen3-32B: `eval_results/eval_qwen3_32b_500/`
- Gemini: `eval_results/eval_gemini_500/`
