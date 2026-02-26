# Gemini 2.5 Flash vs Qwen2.5-7B 差距分析

**数据源**：`preprocessed_BR_first500.csv`（同一批 500 条）  
**分析脚本**：`compare_gemini_7b_analysis.ipynb`

---

## 1. 定义与数量

| 类型 | 定义 | 数量 |
|------|------|------|
| **Good** | 7B 一致率 ≥ Gemini | 229 (46%) |
| **Bad** | Gemini 一致率 > 7B 超 15pp | 90 (18%) |

---

## 2. Bad case 示例（Gemini 明显优于 7B）

| Title | Category | 7B | Gemini | 差距 |
|-------|----------|-----|--------|------|
| Piercing Tragus Cartilagem... | Health | 12.5% | 59.3% | +46.8pp |
| Guarda Chuva Automático Masculino... | Sports | 5.0% | 50.0% | +45.0pp |
| Suporte Chão Estacionar Bike... | Sports | 16.0% | 60.7% | +44.7pp |
| CONJUNTO UNIFORME PRIVATIVO... | Health | 11.8% | 52.6% | +40.9pp |
| Kit 3 Bermudas Ciclista... | Sports | 20.0% | 59.1% | +39.1pp |

### Bad case 典型差异（KSP 用词）

- **7B 问题**：拼写错误（`acel`→`aço`、`acço`→`aço`）、偏材料规格（`92% poliéster`）、短语不够贴近搜索词
- **Gemini 优势**：用词更贴近搜索词库（如 `bermuda ciclista`、`bicicletário`、`proteção UV 50`）、标题关键词利用更好

---

## 3. Good case 示例（7B 优于 Gemini）

| Title | Category | 7B | Gemini | 差距 |
|-------|----------|-----|--------|------|
| CAVALINHO ROSA NO SACO LIDER | Sports | 75.0% | 29.4% | -45.6pp |
| Tesoura Para Bordados De Ponta Curva | Stationery | 72.7% | 33.3% | -39.4pp |
| Personalizado combinado com cliente | Stationery | 50.0% | 11.1% | -38.9pp |
| Bandeja Em Pe 28 X 42 X 7 Cm Nalgon | Health | 47.8% | 10.5% | -37.3pp |
| Kit 7 Caneta Em Formato De Seringa | Stationery | 73.7% | 37.5% | -36.2pp |

### Good case 典型差异（KSP 用词）

- **7B 优势**：更贴近标题原文（`tesoura para bordados` vs `tesoura de bordado`）、尺寸规格更完整（`28 x 42 cm`、`28 centímetros x 42 centímetros`）、品牌/型号保留更好（`LIDER`、`Nalgon`）
- **Gemini 问题**：同义替换偏离搜索词（`etiquetas personalizadas` vs 商品实际为 adesivos）、短语冗长（`cavalinho de brinquedo rosa`）

---

## 4. 分品类统计

| 品类 | Good 数量 | Bad 数量 |
|------|-----------|----------|
| Sports & Outdoors | 87 | 51 |
| Stationery | 78 | 20 |
| Health | 64 | 19 |

Bad 主要集中在 Sports & Outdoors。

---

## 5. 结论与建议

1. **Bad case 改进方向**：减少拼写错误、少用材料规格类短语、多贴近搜索词库用词（可从 title 中提取核心搜索词）。
2. **Good case 保持**：7B 在 Stationery 定制类、尺寸规格类、品牌型号类商品上表现更好，可保留当前策略。
3. **Sports & Outdoors**：Bad 占比最高，建议针对该品类增加 few-shot 或优化 prompt。
