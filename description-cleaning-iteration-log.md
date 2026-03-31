# Description 清洗方案 — 迭代记录

> 完整的技术探索、实验验证和规则迭代过程记录

---

## 1. 项目背景

### 1.1 问题

Shopee 电商 `description` 字段是 KSP 卖点生成（P0）和标题优化（P4）的核心输入，但普遍混杂运营噪音：

- 物流发货（frete / ongkir / 出貨 / จัดส่ง）
- 退换货政策（退貨須知 / retur / devolução）
- 客服联系（whatsapp / 聊聊 / hubungi kami）
- 店铺介绍（歡迎光臨 / welcome / tentang toko）
- Emoji / URL / 电话号码

### 1.2 影响量化

对 29 万条已有 KSP 输出做静态分析：

- **15.6%** 含噪音的商品中，KSP 的卖点词来自噪音文本
- 典型泄漏：BR KSP 含 `frete por conta do comprador`（运费），TW KSP 含 `代開發票`（发票服务）

---

## 2. 方案演进

### 2.1 初始设计（v1.0）：三级管线

```
原始 description
  → Level 1: 预处理（HTML/控制符/空白规范化）
  → Level 2: 段落级过滤（按 \n\n 分段，6类噪音关键词，全噪音段删除）
  → Level 3: 句级分类（拆句后逐句判断 fact/noise/keep）
  → 输出
```

**核心问题**：

| 问题 | 根因 |
|------|------|
| 句级拆分引入额外换行 | `_split_sentences` 按句号拆句后用 `\n` 重组 |
| 单 `\n` 变双 `\n\n` | `_split_paragraphs` 把单换行也当段落分隔 |
| 22% 商品只有单换行 | L2 把整个 description 当一个段落处理 |

### 2.2 句级噪音正则的引入与移除

引入了针对主观/促销/健康声称的正则（6种语言）：

```python
SENTENCE_NOISE_PATTERNS = {
    "ID": [r"\b(terbaik|terpercaya|berkualitas)\b", ...],
    "EN": [r"\b(best quality|top rated|cheap)\b", ...],
    ...
}
```

**发现问题**：`"Wireless, Easy to use everywhere"` — `easy to use` 命中正则，整行含产品特性被删。

**决策**：删除句级噪音正则，主观/促销词不再删除。理由：

- 主观词和产品特性经常共存于同一行
- 删除主观词的收益（KSP 更"干净"）远小于误删产品信息的风险
- KSP 模型自身可以过滤主观词，不需要预清洗

### 2.3 L2 段落级过滤的移除

对 L2 的不可替代贡献做了量化分析：

```
L2 总删除: 15,301 chars
其中 L3 删不掉的: 5 行 / 403 chars (2.6%)
```

**结论**：L2 的 97.4% 工作可以被 L3 逐行过滤替代，仅 5 行（装饰分隔线和长噪音句）依赖 L2 整段判断。

**决策**：移除 L2，简化为两阶段管线。

### 2.4 最终架构：两阶段管线

```
原始 description
  → 阶段一: 预处理（结构清理）
  → 阶段二: 逐行过滤（classify_line）
  → 输出
```

---

## 3. 阶段一：预处理（结构清理）

按顺序执行，不涉及语义判断：

| 步骤 | 操作 | 示例 |
|------|------|------|
| HTML 标签/实体 | 去除 | `<br>` `<p>` `&amp;` |
| 控制符/零宽字符 | 去除 | `\x00` `\ufeff` `\u200b` |
| Emoji | 去除（保留 ❌✅✔✖⭕） | 💎📦⚠️🛒⭐ → 删；❌✅ → 保留 |
| URL / Email | 去除 | `https://shopee.tw/...` `@gmail.com` |
| 电话号码 | 去除（仅 `+XX` 或 `0XX` 格式） | `+6016-661-6081` → 删 |
| EAN 保护 | 预先占位防电话正则误删 | `EAN: 7899430218153` → 保护 |
| 行级去重 | 相同行只保留首次 | |
| 空白规范化 | 多空格→单空格，连续空行合并 | |

### 3.1 Emoji 保留语义符号

`❌` `✅` 在 SG 商品描述中用于表示"有/无"（如 `(Set ❌ boot ribbon)` = 不含丝带）。如果删掉，语义丢失。

**方案**：定义 `_KEEP_SYMBOLS` 集合，emoji 正则跳过这些字符。

### 3.2 电话号码正则演进

| 版本 | 正则 | 问题 |
|------|------|------|
| v1 | `\d{2,4}[\s.-]?\d{3,4}[\s.-]?\d{3,5}` | 匹配 EAN 条码（13位数字） |
| v2 | 加词边界 `(?<![0-9])...(?![0-9])` | 匹配年份序列 `2020 2021 2022` |
| v3（当前） | 仅匹配 `+XX` 国际格式或 `0XX` 本地格式 | 年份和型号不再误删 |

v3 正则：
```python
_PHONE = re.compile(
    r'\+\d{1,3}[\s\-]?\(?\d{2,4}\)?[\s\-.]?\d{3,5}[\s\-.]?\d{3,5}'  # +XX 格式
    r'|'
    r'(?<![0-9])0\d{1,3}[\s\-.]?\d{3,5}[\s\-.]?\d{3,5}(?![0-9])'    # 0XX 格式
)
```

### 3.3 EAN 保护

`EAN: 7899430218153` 的 13 位数字会被电话正则误删。方案：在删电话之前，先用正则找到 `EAN:`/`SKU:`/`Código:` 等标签及其后的编号，用占位符保护，删完电话后恢复。

---

## 4. 阶段二：逐行过滤（classify_line）

对预处理后的每一行独立分类：

```python
def classify_line(line, region):
    1. 含规格单位 / 型号 / 认证词 / 产地词  → fact（强制保留）
    2. 行长度 > 100 字符                    → keep（混合内容安全保留）
    3. 命中 ≥2 类噪音关键词                  → noise（高置信，直接删除）
    4. 命中 1 类噪音词 → 去掉噪音短语后检查剩余内容
       4a. 剩余 ≥40 字符 且 本身无噪音词    → keep（混合行保留）
       4b. 否则                            → noise（删除）
    5. 其余                                → keep（保留）
```

### 4.1 保护机制（词库驱动）

| 类型 | 规模 | 示例 |
|------|------|------|
| 规格单位 | 65+ 个 | g/kg/ml/cm/mAh/GB/VAC/VDC/OHMS |
| 型号模式 | 正则 | `CB300F` `YH-8004` |
| 认证词 | 8 个 | Halal/BPOM/FDA/ISO/SNI |
| 产地词（拉丁） | 68 个 | Kerinci/Sumatera/Minas Gerais |
| 产地词（CJK/泰语） | 25 个 | 阿里山/เชียงราย/Đà Lạt |

### 4.2 噪音关键词库

6 类 × 6 语言（228 个短语），存储在 `cleaning_keywords.json`。

MY 地区同时使用 EN + ID 两套规则（覆盖双语混用）。

### 4.3 多类命中规则

当一行同时命中 ≥2 个噪音类别（如 shipping + customer_service），直接判定为 noise，跳过混合行检查。

理由：一行同时包含物流+客服+退换等多类噪音信号，几乎不可能同时包含有价值的产品信息。

### 4.4 混合行保留规则

单类命中时，去掉噪音短语后检查剩余内容：
- `"150 Closed Heart Mustard seeds (fr SG). Free shipping."` → 去掉 `Free shipping` → 剩 `150 Closed Heart Mustard seeds (fr SG)` (48字符 ≥40) → **keep**
- `"Free shipping"` → 去掉后剩 0 字符 → **noise**

额外约束：剩余内容本身也要通过噪音检测（防止长物流句被保留）。

### 4.5 空描述兜底

如果清洗后 description 为空但原文有内容，返回原文。防止单行 description 被整体清空。

---

## 5. 关键词迭代记录

### 5.1 移除的歧义关键词

| 词 | 语言 | 移除原因 | 发现方式 |
|----|------|---------|---------|
| `suporte` | BR | "支架"被当"客服" | Gemini judge |
| `importante` | BR | 安装说明被当警告 | Gemini judge |
| `troca` | BR | "换零件"被当退换 | Gemini judge |
| `atenção` | BR | 安装提示被当噪音 | Gemini judge |
| `catatan` | ID | 定制说明被当注意 | Gemini judge |
| `請注意` | TW | 兼容性说明被删 | 人工标注 |
| `lưu ý` | VN | 使用说明被删 | 人工标注 |
| `賣場` | TW | 颜色说明被删 | 人工标注 |

### 5.2 精化的关键词

| 词 | 改为 | 原因 |
|----|------|------|
| `ทางร้าน` (TH) | `ทางร้านจัดส่ง` 等具体搭配 | 产品保证声明含 `ทางร้าน` |
| `atenção` (BR) | `atenção ao comprar` / `atenção importante` | 安装说明含 `ATENÇÃO:` |
| `aviso` (BR) | `aviso importante` | `aviso` 太泛 |
| `troca` (BR) | `política de troca` | "零件更换"含 `troca` |

### 5.3 新增的保护

| 类型 | 内容 |
|------|------|
| 规格单位 | VAC / VDC / OHMS / RMS / gramas / 毫升 / 公克 |
| 产地词 | Kerinci / Toraja / เชียงราย / ดอยอินทนนท์ / 阿里山 / Đà Lạt |
| 语义 emoji | ❌ ✅ ✔ ✖ ⭕（不被 emoji 正则删除） |

---

## 6. 验证体系

### 6.1 规则验证（8000 条 · 每地区 1000 条）

| 指标 | 结果 |
|------|------|
| 规格保留率 | 19710 / 19710 = **100%** |
| 认证保留率 | 358 / 358 = **100%** |
| 引入额外换行 | **0** |
| 总删除率 | **~2%** |

### 6.2 KSP AB Test（1966 条 · AIS GPU 推理）

使用 `sft_datagen_re/p0_ksp.py`（Qwen2.5-7B-Instruct）对原始 vs 清洗后 description 分别跑 KSP 生成：

| 指标 | Control（原始） | Treatment（清洗后） |
|------|----------------|-------------------|
| KSP 噪音词来源 | 0.010 | 0.003（**-66.7%**） |
| TW 短语命中率 | 9.1% | 9.2%（+0.9%） |
| BR 覆盖曝光 | 1349M | 1553M（**+15.1%**） |
| Factscore | 0.527 / 0.747 | 0.510 / 0.748 |

### 6.3 Gemini Judge（669 条有变化条目）

使用 `gemini-2.5-flash` 对清洗质量做 LLM-as-judge 评测：

| 指标 | 结果 |
|------|------|
| ok 率 | **94.6%** |
| over_cleaned 率 | **5.4%** |
| avg score | **4.84 / 5** |

地区明细：

| Region | ok% | score |
|--------|-----|-------|
| BR | 89% | 4.68 |
| ID | 97% | 4.91 |
| MY | 91% | 4.74 |
| PH | 97% | 4.92 |
| SG | 95% | 4.84 |
| TH | 93% | 4.78 |
| TW | 96% | 4.89 |
| VN | 100% | 5.00 |

### 6.4 "变软"验证

对新逻辑比旧逻辑少删的 1447 条做 judge：

- **96.3% ok** — 这些多保留的内容确实是产品信息
- 仅 3.7%（约 54 条）是真正应删的噪音

结论：清洗强度降低是正确的，旧逻辑误删了大量产品信息。

### 6.5 人工标注（50 条 over_cleaned 样本）

通过 [在线标注工具](https://nauyisu022.github.io/temp-web/annotation.html) 人工审核：

- ✅ 清洗正确: 25 (50%)
- 🔴 过度清洗: 19 (38%)
- ⚠️ 轻微问题: 6 (12%)

人工标注发现的问题直接推动了 6 个关键词修正（§5.1）。

---

## 7. 工程产出

### 7.1 代码

| 文件 | 说明 |
|------|------|
| `reranker_sft_old/data/description_cleaner.py` | 清洗模块主体 |
| `reranker_sft_old/data/cleaning_keywords.json` | 关键词库（噪音词 + 保护词） |
| `data/scripts/judge_description_cleaning.py` | Gemini-as-judge 评测脚本 |
| `data/scripts/gen_annotation_data.py` | 标注数据生成脚本 |
| `data/scripts/push.sh` | 一键推送脚本 |

### 7.2 可视化

| URL | 说明 |
|-----|------|
| [标注工具](https://nauyisu022.github.io/temp-web/annotation.html) | 人工打标（word-level diff + 规则标签） |
| [清洗流程图](https://nauyisu022.github.io/temp-web/cleaning_flow.html) | 两阶段管线可视化 + Case 对比 |
| [项目报告](https://nauyisu022.github.io/temp-web/cleaning_report.html) | 完整报告（动机→方案→结果） |

### 7.3 接入方式

```python
from data.description_cleaner import clean_description

cleaned = clean_description(description, region)
# region: 'BR' | 'ID' | 'MY' | 'PH' | 'SG' | 'TH' | 'TW' | 'VN'
```

词库维护：修改 `cleaning_keywords.json`，无需改代码。

---

## 8. 关键设计决策总结

| 决策 | 选择 | 理由 |
|------|------|------|
| 三级 vs 两级管线 | 两级 | L2 段落过滤仅贡献 2.6%，复杂度不值得 |
| 句级拆分 vs 行级 | 行级 | 避免引入额外换行，保持原始格式 |
| 主观词删除 vs 保留 | 保留 | 产品特性与主观词共存，误删风险大于收益 |
| 数字保护 vs 规格单位保护 | 规格单位 | `5-7天` 不应被保护，`500g` 应该 |
| 固定长度阈值 vs 混合行检查 | 两者结合 | >100字符直接保留 + 剩余内容≥40字符保留 |
| 单类 vs 多类噪音判定 | ≥2 类直接删 | 多类命中几乎 100% 是纯噪音 |
| 关键词硬编码 vs JSON 外置 | JSON 外置 | 改词不改代码，降低维护成本 |
