# Description 清洗策略文档

> 版本：v1.5 | 更新：2026-03-31

---

## 目标

对电商商品 `description` 字段做规则化清洗，去除运营噪音（物流、退换货、促销语、主观评价、店铺说明），保留产品事实（规格、型号、成分、兼容性、产地），输出 `description_cleaned` 供下游 KSP 生成（P0）和标题生成（P4）使用。

---

## 三级过滤管线

```
原始 description
  → Level 1: 预处理（HTML/字符规范化）
  → Level 2: 段落级过滤（双换行分隔的块）
  → Level 3: 行级过滤（逐行判断）
  → 输出: description_cleaned
```

### Level 1：预处理

纯结构清理，不删内容：

- 去除 HTML 标签（`<br>` / `<p>` 转换为换行）、HTML 实体
- 去除控制字符（`\x00-\x1f`）、零宽字符（`\u200b` / `\ufeff` 等）
- 规范化行内空白（多个空格合并，保留换行）
- 合并连续空行（`\n{3,}` → `\n\n`）

### Level 2：段落级过滤

按**双换行**（`\n\n`）分段，对整个段落判断是否为噪音：

```
_is_noise_paragraph(para, region):
  1. 为空 / 极短 (<10字符)       → 删除
  2. 含规格/型号/认证/产地词      → 保留（硬保护，跳过后续判断）
  3. 无噪音关键词                → 保留
  4. 有噪音关键词 → 逐行扫描:
       若任一行为 fact            → 整段保留
       若全为 noise              → 整段删除
       其余                      → 保留
```

### Level 3：行级过滤

对 Level 2 保留的段落，逐行判断：

```
classify_sentence(line, region):
  1. 空行                               → noise
  2. 含 SPEC_PATTERN / 型号 / 认证 / 产地  → fact（保留）
  3. 长度 ≤ 150 且命中促销/主观正则
     且不含规格单位                      → noise（删除）
  4. 长度 ≤ 120 且命中段落噪音关键词
     且不含规格单位                      → noise（删除）
  5. 其余                               → keep（保留）
```

**数字保护规则**：保护条件是含有规格单位（`g/kg/ml/cm/mAh` 等），而不是含任意数字。`5-7 个工作日`、`09:00-23:00` 这类物流/时间数字不触发保护。

---

## 保护机制（免死规则）

任何文本命中以下任一条件，无论周围内容如何嘈杂，**强制保留**：

### 规格数字（SPEC_PATTERN）

数字 + 质量/体积/尺寸/电气/容量单位：

```
g / gr / gram / gramas / kg / mg / ml / l / liter / cl
cm / mm / m / km / inch / in
pcs / pc / buah / 件 / 個 / 入 / 包 / 箱 / 瓶
pack / set / unit / sachet / capsule / tablet
W / kW / V / mAh / Ah / Wh / GB / TB / MB / MHz / GHz / Hz
oz / lb / rpm / nm / ℃ / °C
毫升 / 公克 / 公斤 / 公分 / 毫米  （繁中）
gramas  （葡语）
```

示例：`500g` / `4000 mAh` / `2.5cm` / `128 GB`

### 型号模式

`[A-Z]{2,}[A-Z0-9-]*\d{3,}` — 如 `CB300F` / `YH-8004` / `iPhone 15`

### 认证词

`Halal / BPOM / FDA / SNI / ISO / HACCP / GMP / MUI`

### 产地词

| 语言 | 示例 |
|------|------|
| 印尼（拉丁） | Sumatera / Jawa / Kerinci / Toraja / Flores / lereng gunung / perkebunan |
| 马来西亚 | Sabah / Sarawak / Cameron Highland |
| 泰国（拉丁） | Chiang Rai / Chiang Mai / Doi Inthanon |
| 泰国（泰语） | เชียงราย / เชียงใหม่ / ดอยอินทนนท์ |
| 越南 | Đà Lạt / Sa Pa / Mộc Châu |
| 台湾（繁中） | 阿里山 / 高山茶 / 玉山 / 梨山 / 台灣 |
| 巴西 | Minas Gerais / Cerrado / Sul de Minas |
| 通用 | dataran tinggi / dari Indonesia / dari Malaysia / dari Japan … |

**设计意图**：`Teh terbaik dari perkebunan di lereng gunung Kerinci, Sumatera` 含 `terbaik`（主观词）但也含产地词，整句保留。

---

## 段落级噪音关键词（6 类 · 8 地区）

| 类别 | EN | ID | BR | TW | TH | VN |
|------|----|----|----|----|----|----|
| 📦 物流发货 | free shipping / COD | ongkir / pengiriman | frete / envio | 運費 / 出貨 / 宅配 / 超商取貨 | จัดส่ง / ค่าส่ง | giao hàng / phí ship |
| ↩ 退换货 | return policy / refund | retur / pengembalian | devolução / troca | 退貨 / 退款 / 鑑賞期 | คืนสินค้า / เคลมสินค้า | đổi trả / hoàn tiền |
| 💬 客服 | contact us / whatsapp | hubungi kami / CS | fale conosco | 客服 / 聊聊 / 服務時間 / 服務保障 | ติดต่อเรา / แชทหาเรา | liên hệ / hotline |
| 🏪 店铺介绍 | welcome to our store | tentang toko / kami adalah | nossa loja | 歡迎光臨 / 本店 / 賣場 | ทางร้าน / ร้านของเรา | về chúng tôi / cảm ơn |
| ⚠ 免责声明 | image for reference | gambar hanya ilustrasi | imagem ilustrativa | 圖片僅供參考 / 色差 | สีอาจแตกต่าง | màu sắc có thể khác |
| ⛔ 警告/注意 | safety warning | perhatian / catatan | atenção / aviso | 溫馨提示 / 注意事項 | คำเตือน / หมายเหตุ | lưu ý / cảnh báo |

---

## 句级噪音正则（主观 / 促销 / 健康声称）

按地区语言，对短句（≤ 150 字符）且无规格单位的句子进行检测：

| 语言 | 适用地区 | 噪音模式示例 |
|------|---------|------------|
| ID | ID / MY | `terbaik` · `berkualitas` · `terpercaya` · `promo` · `diskon` · `murah` · `menyehatkan` |
| BR | BR | `melhor` · `confiável` · `qualidade superior` · `promoção` · `desconto` · `fácil de usar` |
| EN | MY / SG / PH | `best quality` · `top rated` · `cheap` · `affordable` · `easy to use` |
| TW | TW | `最優惠` · `超值` · `限時` · `促銷` · `熱銷` · `品質保證` · `真心推薦` |
| TH | TH | `ดีที่สุด` · `คุ้มค่า` · `ราคาถูก` · `โปรโมชั่น` · `คุณภาพดี` |
| VN | VN | `tốt nhất` · `chất lượng cao` · `giá rẻ` · `khuyến mãi` · `dễ sử dụng` |

> MY 同时应用 EN + ID 两套规则（马来语双语混用）。

---

## 去重

全文范围内（跨段落），对规范化后相同的行**只保留首次出现**：

- 规范化方式：小写 + 合并空白
- 覆盖场景：`"Produk 500g\nProduk 500g"` → `"Produk 500g"`

---

## 设计原则

| 原则 | 实现 |
|------|------|
| **宁可留多** | 默认 keep；只删高置信度噪音 |
| **规格免死** | 含规格单位的行，无论其他内容如何，强制保留 |
| **产地保护** | 含已知产地词的行，即使含主观词（terbaik/melhor）也保留 |
| **长句豁免** | 句级噪音模式只对 ≤ 150 字符短句生效 |
| **数字精准保护** | 仅规格单位后的数字触发保护，物流时间/价格数字不触发 |
| **行级输出** | 以行为单位判断和输出，不拆句、不重组，保持原始格式 |
| **MY 双规则** | 马来西亚同时应用 EN + ID 规则 |

---

## 已知边界情况

| 场景 | 当前行为 | 说明 |
|------|---------|------|
| 有序列表（`1. 2. 3.`）中有噪音行 | 噪音行删除，编号保留 | 可接受 |
| 物流限制含产品尺寸（`45cm×30cm` 为超商尺寸上限） | 因含 `cm` 被保留 | 保守，不误删 |
| 店铺优惠券行（`點關注領取10元優惠券`） | 保留（无法匹配现有模式） | 已知漏检 |
| 极短描述（清洗后所剩无几） | 保留原文 | 原数据质量问题 |
| 认证词夹在噪音段落（`Halal, gratis ongkir`） | 整行保留 | 保守，正确 |

---

## 实测结果（1966 条）

| 指标 | 结果 |
|------|------|
| 有变化条目 | 44.0%（865 条） |
| 规格保留率 | 100%（0 条误删） |
| 引入额外换行 | 0 条 |
| 平均 token 节省 | 5.8%（Qwen tokenizer） |
| TW 效果最显著 | token 节省 16.1% |
| KSP 噪音词来源减少 | -66.7%（`from_noise` 指标） |
| Factscore 影响 | TW -1.6% / BR +0.1% |

---

## 代码位置

| 文件 | 说明 |
|------|------|
| `reranker_sft_old/data/description_cleaner.py` | 清洗模块主体 |
| `reranker_sft_old/data/__init__.py` | 导出 `clean_description` / `clean_csv` |
| `data/current/annotation_data.json` | 200 条人工标注样本 |
| `data/scripts/run_ksp_abtest.py` | KSP AB test 批量运行脚本 |

### 主要 API

```python
from data.description_cleaner import clean_description, clean_description_with_labels

# 单条清洗
cleaned = clean_description(description, region)
# region: 'BR' | 'ID' | 'MY' | 'PH' | 'SG' | 'TH' | 'TW' | 'VN'

# 带标签（用于调试/标注，返回每行操作原因）
result = clean_description_with_labels(description, region)
# result = {'cleaned': str, 'lines': [{'text', 'action', 'reason', 'level'}, ...]}

# 批量 CSV 清洗
from data.description_cleaner import clean_csv
clean_csv(input_csv, output_csv, region, report_path=None)
```

### 接入 P0 KSP（建议）

在 `p0_ksp.py` 的 `load_items` 之后插入：

```python
from reranker_sft_old.data.description_cleaner import clean_description
df['description'] = df.apply(
    lambda r: clean_description(r['description'], r['grass_region']), axis=1
)
```

---

## 迭代记录

| 版本 | 变更 |
|------|------|
| v1.0 | 三级管线初始实现；段落/句级关键词；SPEC_PATTERN |
| v1.1 | 修复：全噪音描述返回原文 → 改返回空字符串 |
| v1.2 | 修复：短段落（<10字符）覆盖规格保护，调整判定顺序 |
| v1.3 | 扩充：地区特定规格单位（gramas / 毫升 / 公克） |
| v1.4 | 修复：`pd.NA` 类型安全处理 |
| v1.5 | 修复：BR 长句含 `fácil de usar` 被误删（长句豁免 ≤150字符）|
| v1.6 | 修复：TW `現貨` 误删产品名称行（从运费词表移除） |
| v1.7 | 新增：产地词保护（Kerinci / Sumatera / Minas Gerais / เชียงราย 等） |
| v1.8 | 修复：行级输出替代句级重组，消除额外换行 |
| v1.9 | 修复：`_split_paragraphs` 只按双换行分段，单换行保留 |
| v1.10 | 新增：全局去重（连续重复行只保留首次） |
| v1.11 | 修复：数字保护改为规格单位保护（`_has_spec` 替代 `re.search(r"\d")`） |
| v1.12 | 扩充 TW：`服務時間` / `服務保障` / `超商取貨` / `宅配通` |
