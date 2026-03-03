# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an SFT (Supervised Fine-Tuning) data generation system for e-commerce product selling points extraction. The system takes product listings (title, description, category) and generates search-optimized keyword candidates through a 4-step LLM pipeline, producing training data for search ranking models.

## Architecture

The codebase follows a modular architecture with three inference modes:

```
┌─────────────────────────────────────────────────────────┐
│                    Entry Points                          │
├─────────────────┬─────────────────┬─────────────────────┤
│ extractor_     │ extractor_      │ extractor_          │
│ distributed_   │ api.py          │ pp.py               │
│ v11.py         │                 │                     │
│ (vLLM local)   │ (API inference) │ (Pipeline parallel) │
└────────┬────────┴────────┬────────┴──────────┬──────────┘
         │                 │                    │
         ▼                 ▼                    ▼
┌─────────────────────────────────────────────────────────┐
│               processor.py (SellingPointsProcessor)     │
│         4-Step Pipeline: User Profile → Keywords →    │
│         Candidates → Evaluation                         │
└────────────────────────┬────────────────────────────────┘
                         │
    ┌────────────────────┼────────────────────┐
    ▼                    ▼                    ▼
┌─────────────┐  ┌─────────────┐      ┌─────────────┐
│ prompts_v2  │  │ schema.py   │      │ data_loader │
│ (LLM prompts)│  │ (category   │      │ (S3/CSV     │
│             │  │  schemas)   │      │  loading)   │
└─────────────┘  └─────────────┘      └─────────────┘
```

### Key Modules

| File | Purpose |
|------|---------|
| `processor.py` | Core 4-step extraction pipeline (SellingPointsProcessor class) |
| `prompts_v2.py` | Prompt templates for Steps 1-4, region-language mapping |
| `schema.py` | Product category to selling point schema mapping |
| `data_loader.py` | S3/CSV data loading, preprocessing, token-based sharding |
| `api_engine.py` | OpenAI/Gemini-compatible API wrapper |
| `config.py` | Centralized configuration (paths, model params, batch sizes) |
| `utils.py` | Utilities: token counting, dynamic batch sizing, metrics |
| `eval/` | Evaluation module for KSP (keyword search performance) |

### 4-Step Extraction Pipeline

1. **Step 1 - User Profile**: Analyze target user and search intent from product info
2. **Step 2 - Keywords**: Extract search-friendly keywords based on schema attributes
3. **Step 3 - Candidates**: Generate 5 keyword candidates per schema attribute
4. **Step 4 - Evaluation**: Evaluate and select the best candidate

## Common Commands

### Data Extraction (Local vLLM)

```bash
# Single machine inference
python extractor_distributed_v11.py --data-csv /path/to/input.csv --region BR

# Multi-GPU inference (torchrun)
torchrun --nproc_per_node=4 extractor_distributed_v11.py --data-csv /path/to/input.csv
```

### Data Extraction (API Mode)

```bash
# Using remote vLLM server
python extractor_api.py \
    --api-provider openai \
    --api-base http://server:8000/v1 \
    --api-model Qwen3-32B \
    --data-csv /path/to/input.csv \
    --region BR

# Using OpenAI API
python extractor_api.py \
    --api-provider openai \
    --api-base https://api.openai.com/v1 \
    --api-key sk-xxx \
    --api-model gpt-4o \
    --data-csv /path/to/input.csv

# Using Google Gemini
python extractor_api.py \
    --api-provider google \
    --api-model gemini-2.5-flash \
    --data-csv /path/to/input.csv

# Using Alibaba DashScope
python extractor_api.py \
    --api-provider openai \
    --api-base https://dashscope-intl.aliyuncs.com/compatible-mode/v1 \
    --api-model qwen-max \
    --data-csv /path/to/input.csv
```

### Evaluation

```bash
# Run evaluation on generated CSV
python -m eval.main \
    --search-term-index /path/to/search_term_index_BR \
    --benchmark-csv /path/to/output.csv \
    --output-dir /path/to/eval_results
```

### Key Parameters

| Parameter | Description |
|-----------|-------------|
| `--data-csv` | Input CSV file path |
| `--region` | Target market (BR, MX, CO, CL, TW, TH, VN, ID, MY, SG, PH, PL) |
| `--job-tag` | Job identifier for output directory |
| `--max-infer` | Limit number of items to process |
| `--batch-size` | Override default batch size |

## Configuration

All configuration is centralized in `config.py`:

- `PathConfig`: Model paths, S3 config, output directories
- `ModelConfig`: vLLM params (tensor_parallel_size, gpu_memory_utilization, max_model_len), sampling params
- `BatchConfig`: Dynamic batch sizing rules based on token count
- `APIConfig`: API provider, endpoint, concurrency settings
- `ProcessConfig`: Data limits, progress logging intervals

## Data Format

### Input CSV Expected Columns
- `title` or `enhanced_title`: Product title
- `description`: Product description
- `global_category1`: Primary category
- `category_l1_l3`: Detailed category path
- `region`: Target market code

### Output CSV Columns
- `title`, `description`, `global_category1`, `category_l1_l3`, `region`
- `matched_schema`: Selected schema attributes
- `user_profile_and_schema`: Step 1 output
- `keywords`: Step 2 output
- `attractiveness_1` to `attractiveness_N`: Step 3 candidates
- `attractiveness_selected`: Step 4 selection
- `step1_think`, `step2_think`, `step3_think`: Model reasoning (if enabled)
- `time_used`, `batch_size`, `avg_tokens`, `success`, `error`: Execution metadata

## Region Support

The system supports multiple e-commerce markets with language-specific optimization. Each region maps to a target language in `prompts_v2.py:REGION_LANGUAGE_MAP`:

- **BR**: Portuguese (Brazil)
- **MX, CO, CL**: Spanish (Latin America)
- **TW**: Traditional Chinese
- **TH**: Thai
- **VN**: Vietnamese
- **ID**: Indonesian
- **MY**: Malay/English
- **SG, PH**: English
- **PL**: Polish
