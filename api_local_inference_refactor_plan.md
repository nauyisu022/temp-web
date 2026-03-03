# API / 本地推理分层改造方案

## 背景

当前仓库同时支持：

- API 推理：`extractor_api.py`
- 本地 / 分布式 vLLM 推理：`extractor_distributed.py`
- Pipeline Parallelism 实验：`extractor_pp.py`

问题不在于“同时支持两种推理模式”，而在于模式差异已经渗透进共享核心，导致以下现象：

- 共享核心需要理解 API 模式和本地模式
- 配置对象重复定义
- `utils.py` 承担了过多后端适配职责
- 入口文件之间有大量重复组装逻辑

目标不是拆成两套系统，而是把“业务流程”和“推理后端”分层。

## 当前结构问题

### 1. 核心流程被模式分支侵入

`processor.py` 目前同时承担：

- 卖点抽取 4-step 主流程
- vLLM `SamplingParams` 兼容
- API 模式分支
- tokenizer / batch 策略差异处理

这使它既是业务层，又像后端适配层。

### 2. 配置定义重复

当前至少有两套 API 配置：

- `config.py` 中的 `APIConfig`
- `api_engine.py` 中的 `APIConfig`

这会带来两个问题：

- 字段可能漂移
- 调用方不清楚哪套才是真正生效的配置

### 3. 通用工具模块边界过宽

`utils.py` 当前混合了：

- 文件与目录工具
- tokenizer 兼容逻辑
- thinking 存储
- batch size 控制
- metric 追踪
- 数据分片

它已经不是“工具模块”，而是多个子系统的堆叠点。

### 4. 入口层重复组装

这些入口有明显重叠：

- `extractor_api.py`
- `extractor_distributed.py`
- `extractor_distributed_v11.py`
- `extractor_pp.py`

它们都在做类似事情：

- 解析参数
- 初始化 tokenizer
- 初始化 schema / data loader / metrics
- 初始化后端
- 调用 processor

区别主要是后端初始化方式不同，但现在重复代码偏多。

## 目标结构

建议最终分成三层。

### 1. Core 层

职责：只负责卖点抽取业务流程，不知道 API / vLLM / PP 的存在。

建议模块：

```text
core/
  pipeline.py
  prompts.py
  schema.py
  batching.py
  thinking.py
  result_writer.py
```

这里面只保留：

- Step1~Step4 的 prompt 编排与结果解析
- batch 调度规则
- schema 拼接
- 输出字段生成

不应该出现：

- `is_api_mode`
- `try: import vllm`
- OpenAI / Claude / Gemini provider 判断

### 2. Backend 层

职责：把不同推理引擎适配成统一接口。

建议模块：

```text
backends/
  base.py
  api_backend.py
  vllm_backend.py
  pp_backend.py
```

统一接口建议保持很小，例如：

```python
class InferenceBackend:
    def generate(self, prompts, sampling_config):
        ...
```

可选扩展：

- `count_tokens(text)`
- `truncate(text, max_tokens)`
- `shutdown()`

这样 `processor` 只依赖抽象接口，不依赖具体 provider。

### 3. Entrypoint 层

职责：参数解析、配置组装、依赖注入。

建议模块：

```text
entrypoints/
  extract_api.py
  extract_vllm.py
  extract_pp.py
  eval_ksp.py
```

入口层只做：

- 读参数
- 构造配置
- 选择 backend
- 初始化数据源
- 调用 core pipeline

## 按现有文件的映射建议

### 保留为 Core 候选

- `processor.py`
- `prompts_v2.py`
- `schema.py`

但需要逐步清理其中的后端分支。

### 保留为 Backend 候选

- `api_engine.py`
- `pp_engine.py`

后续新增：

- `vllm_backend.py`
- `base.py`

### 拆分或下沉的模块

- `utils.py`
  - `SimpleTokenizer` 更适合放到 backend 或 tokenization 模块
  - `DynamicBatchSizeController` 更适合放到 core/batching
  - `ThinkingStorage` 更适合放到 core/thinking
  - `MetricTracker` 更适合放到 infra/metrics
- `data_loader.py`
  - S3 读取
  - 本地 CSV 读取
  - 预处理
  - rank 分片
  这四类职责建议拆开

### 保留为 Entrypoint 候选

- `extractor_api.py`
- `extractor_distributed.py`
- `extractor_pp.py`
- `eval/main.py`

`extractor_distributed_v11.py` 如果不是长期并行维护版本，建议尽快归档，不要继续作为正式入口。

## 推荐的中间态结构

考虑到你现在不想大改逻辑，更稳妥的是先进入一个中间态：

```text
inference/
  backends/
    base.py
    api_backend.py
    vllm_backend.py
    pp_backend.py
  core/
    processor_core.py
    prompt_builder.py
    batch_controller.py
  infra/
    metrics.py
    tokenizers.py
    thinking_storage.py
```

入口文件暂时还放在根目录，但只负责组装。

这样迁移成本低于直接上完整包结构。

## 迁移顺序

建议按下面顺序做，避免一次性重写。

### Phase 1: 明确边界，不改行为

目标：

- 先抽出统一后端接口
- 不改主流程

动作：

1. 新建 `backends/base.py`
2. 把 `api_engine.py` 包一层 backend 适配器
3. 新增 `vllm_backend.py`
4. 让 `extractor_api.py` 和 `extractor_distributed.py` 都返回同一种 backend 对象

完成标准：

- `processor` 接收的是统一 backend，而不是 `APIModelWrapper` / `LLM` 混合对象

### Phase 2: 从 processor 中移除后端细节

目标：

- `processor` 只保留业务流程

动作：

1. 去掉 `try import vllm`
2. 去掉轻量 `SamplingParams` 替代实现
3. 把采样配置抽成独立数据结构
4. 把 `is_api_mode` 分支下沉到 backend

完成标准：

- `processor` 不再关心当前是 API 还是本地推理

### Phase 3: 收口配置

目标：

- 同类配置只保留一份定义

动作：

1. 删除 `config.py` 与 `api_engine.py` 的重复 `APIConfig`
2. 拆分为：
   - `PathConfig`
   - `ModelConfig`
   - `BackendConfig`
   - `RuntimeConfig`
3. provider 专属字段只留在 backend 配置里

完成标准：

- 调用方能明确知道配置归属

### Phase 4: 拆 utils 与 data_loader

目标：

- 清理“大杂烩模块”

动作：

1. `utils.py` 拆分为：
   - `fs.py`
   - `metrics.py`
   - `thinking.py`
   - `batching.py`
   - `tokenizers.py`
2. `data_loader.py` 拆分为：
   - `sources/s3_loader.py`
   - `sources/csv_loader.py`
   - `preprocess.py`
   - `splitter.py`

完成标准：

- 每个模块职责单一

### Phase 5: 最后处理入口与目录

目标：

- 整理文件布局

动作：

1. 统一入口参数风格
2. 删除历史入口
3. 将正式入口迁到 `entrypoints/` 或 `scripts/`

## 一个可接受的统一接口示例

下面这个接口足够小，也适合平滑兼容现有代码：

```python
from dataclasses import dataclass
from typing import Any


@dataclass
class SamplingConfig:
    temperature: float = 0.6
    top_p: float = 0.95
    top_k: int = 20
    max_tokens: int = 4096
    n: int = 1
    repetition_penalty: float = 1.0
    skip_special_tokens: bool = True


class InferenceBackend:
    def generate(self, prompts: list[str], sampling: SamplingConfig) -> list[Any]:
        raise NotImplementedError

    def count_tokens(self, text: str) -> int:
        raise NotImplementedError

    def truncate(self, text: str, max_tokens: int) -> str:
        raise NotImplementedError

    def shutdown(self) -> None:
        pass
```

有了这层后：

- API backend 决定如何请求 OpenAI / Gemini / Claude
- vLLM backend 决定如何调用本地模型
- processor 只消费统一输出格式

## 风险点

### 1. 不要同时重写 prompt 和 backend

`prompts_v2.py` 已经是业务策略核心。改后端分层时不要顺手改 prompt，否则很难定位回归来源。

### 2. 不要先拆 processor 大文件

虽然 `processor.py` 很大，但在边界未稳定前先拆文件，容易把耦合藏起来。应该先抽接口，再拆实现。

### 3. 不要保留两套正式配置对象

如果改造后还同时存在两套 `APIConfig`，那这次重构价值会明显下降。

### 4. 历史版本入口要尽早归档

例如 `extractor_distributed_v11.py` 这类文件，如果继续留在正式路径，会持续制造“哪个入口才是最新”的认知成本。

## 结论

当前的“杂乱”本质上是：

- 后端适配层侵入了核心流程
- 入口层和基础设施层界限不清

正确方向不是按 API / 本地推理复制两套逻辑，而是：

1. 保留一套 core pipeline
2. 为不同推理方式做 backend 适配
3. 让入口层只负责组装

这样你既能继续兼容 API 和本地推理，也不会让后续功能都堆进 `processor.py` 和 `utils.py`。
