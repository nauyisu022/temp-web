# Qwen2.5-14B 与 7B/8B eval 仅重合 385 条的原因分析

## 现象

- **7B / 8B / Gemini**：均在 `preprocessed_BR_first500.csv` 上评测，约 500 条
- **14B**：与 8B eval 按 `title` 合并后仅 **385 条**重合

---

## 诊断结果（已运行验证）

| 数据 | 条数 | 与 first500 title 重合 |
|------|------|------------------------|
| preprocessed_BR_first500 | 500 | — |
| 14B 原始输出 (selling_points_BR_qwen2.5-14b.csv) | 500 | **421** |
| 14B 过滤版 (selling_points_BR_qwen2.5-14b_first500.csv) | 385 | 349 |
| 8B eval | 497 | — |

**结论**：14B 原始输出的 500 条中，只有 **421 条**的 title 与 first500 重合，说明 **14B 的输入数据与 first500 不同**。

---

## 根本原因：输入数据源不同

14B 的 500 条输入**不是**来自 `preprocessed_BR_first500.csv`，而是来自其他数据源或切片，导致：

- 14B 有 **79 条** (500−421) 的 title 不在 first500 中
- first500 有 **79 条** (498−421) 的 title 不在 14B 中
- 两者按 title 合并后最多只有 421 条可对齐

**14B 可能的数据来源：**

1. **S3 加载**：`load_from_s3(region, data_limit=500)`  
   S3 list 顺序可能与本地 CSV 行顺序不一致，取到的 500 条与 first500 不同。

2. **preprocessed_BR.csv 前 500 行**：若 first500 来自不同版本或不同时间点的 preprocessed_BR，两者前 500 行可能不一致。

3. **不同切片/分片**：14B 可能用了 `start_from`、分片或其它参数，导致实际处理的 500 条与 first500 不同。

**selling_points_BR_qwen2.5-14b_first500.csv**（385 条）是对 14B 原始输出做过滤后得到的，用于与 first500 对齐；但受限于 14B 原始与 first500 仅 421 条重合，过滤后只能得到 385 条（部分可能因 KSP 解析失败被剔除）。

## 诊断步骤

运行以下脚本可帮助定位原因：

```python
# scripts/diagnose_14b_overlap.py
import pandas as pd
from pathlib import Path

BASE = Path(".")
PATH_FIRST500 = BASE / "data/preprocessed_BR_first500.csv"
PATH_8B = BASE / "eval_results/eval_qwen_nothink_first500/details_selling_points_BR_qwen_nothink-new.csv"
PATH_14B_SOURCE = BASE / "outputs/selling_points_BR_qwen2.5-14b.csv"  # 14B 原始输出
PATH_14B_EVAL = BASE / "eval_results/eval_qwen2.5_14b_500/details_selling_points_BR_qwen2.5-14b_first500.csv"

# 1. 加载 first500 的 title 集合
df_first500 = pd.read_csv(PATH_FIRST500)
titles_first500 = set(df_first500["title"].astype(str).str.strip())

# 2. 加载 8B eval 的 title
df_8b = pd.read_csv(PATH_8B)
titles_8b = set(df_8b["title"].astype(str).str.strip())

# 3. 加载 14B 的 title（优先用 eval details，若不存在则用 source）
if PATH_14B_EVAL.exists():
    df_14b = pd.read_csv(PATH_14B_EVAL)
else:
    df_14b = pd.read_csv(PATH_14B_SOURCE)
titles_14b = set(df_14b["title"].astype(str).str.strip())

# 4. 重叠分析
overlap_14b_8b = titles_14b & titles_8b
overlap_14b_first500 = titles_14b & titles_first500
only_in_14b = titles_14b - titles_first500
only_in_first500 = titles_first500 - titles_14b

print("=== 14B 与 8B eval 重合分析 ===")
print(f"first500 条数: {len(titles_first500)}")
print(f"8B eval 条数: {len(titles_8b)}")
print(f"14B 条数: {len(titles_14b)}")
print(f"14B ∩ 8B: {len(overlap_14b_8b)}")
print(f"14B ∩ first500: {len(overlap_14b_first500)}")
print(f"仅在 14B 中（不在 first500）: {len(only_in_14b)}")
print(f"仅在 first500 中（不在 14B）: {len(only_in_first500)}")

# 5. 若 14B 有 item_id，可进一步对比
if "item_id" in df_first500.columns and "item_id" in df_14b.columns:
    ids_first500 = set(df_first500["item_id"].astype(str))
    ids_14b = set(df_14b["item_id"].astype(str))
    print(f"\n按 item_id 重叠: {len(ids_first500 & ids_14b)}")
```

## 建议

1. **统一输入**：14B 使用与 7B/8B 相同的 `data/preprocessed_BR_first500.csv` 重新生成，确保 500 条完全对齐。
2. **记录配置**：在生成脚本中记录 `--data-csv`、`--data-limit` 等参数，便于复现。
3. **用 item_id 对齐**：若各表都有 `item_id`，建议以 `item_id` 为主键做合并，比 `title` 更稳定。
