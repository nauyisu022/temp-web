# API Engine 使用指南

`api_engine.py` 已成功融合 `lib/llm_api.py` 的核心功能，现在同时支持：
- **批量推理**（vLLM 兼容接口）
- **单次调用**（简单易用接口）
- **异步支持**
- **Token 统计**
- **高级参数**（reasoning_effort, verbosity, thinking_budget）

## 快速开始

### 1. 单次同步调用（类似 lib/llm_api.py）

```python
from api_engine import APIModelWrapper, APIConfig

# 配置
config = APIConfig(
    provider="openai",
    model="gpt-4o-mini",
    reasoning_effort="minimal",  # 可选: none/minimal/low/medium/high/xhigh
    verbosity="medium",          # 可选: concise/medium/detailed
    return_usage=True            # 返回 token 统计
)

wrapper = APIModelWrapper(config)

# 单次调用
text, usage = wrapper.generate_single("Hello, how are you?")
print(f"Response: {text}")
print(f"Usage: {usage}")

wrapper.shutdown()
```

### 2. 单次异步调用

```python
import asyncio
from api_engine import APIModelWrapper, APIConfig

async def main():
    config = APIConfig(
        provider="openai",
        model="gpt-4o-mini",
        return_usage=True
    )
    
    wrapper = APIModelWrapper(config)
    
    # 异步调用
    text, usage = await wrapper.async_generate_single("What is AI?")
    print(f"Response: {text}")
    print(f"Tokens: {usage['total_tokens']}")
    
    wrapper.shutdown()

asyncio.run(main())
```

### 3. 批量推理（vLLM 兼容）

```python
from api_engine import APIModelWrapper, APIConfig

config = APIConfig(
    provider="openai",
    model="gpt-4o-mini",
    max_concurrent=16,
    return_usage=True  # 批量调用也支持 token 统计
)

wrapper = APIModelWrapper(config)

# 批量调用
prompts = ["Hello", "Goodbye", "Thank you"]
outputs = wrapper.generate(prompts)

for i, output in enumerate(outputs):
    print(f"Prompt {i+1}: {prompts[i]}")
    print(f"  Response: {output.outputs[0].text}")
    print(f"  Usage: {output.usage}")

wrapper.shutdown()
```

## 高级功能

### GPT-5 系列：Reasoning Effort

```python
config = APIConfig(
    provider="openai",
    model="gpt-5.2",
    reasoning_effort="high",  # none/minimal/low/medium/high/xhigh
    verbosity="detailed"      # concise/medium/detailed
)

wrapper = APIModelWrapper(config)
text, usage = wrapper.generate_single("Solve: 2+2=?")
```

**Reasoning Floor/Ceiling 自动处理：**
- `gpt-5`: floor=minimal, ceil=high
- `gpt-5.1`: floor=none, ceil=high
- `gpt-5.2`: floor=none, ceil=xhigh
- `o1/o3/o4`: floor=low, ceil=high

### Google Gemini：Thinking Budget

```python
config = APIConfig(
    provider="google",
    model="gemini-2.5-flash",
    thinking_budget=0,  # 关闭 thinking（节省 token）
    return_usage=True
)

wrapper = APIModelWrapper(config)
text, usage = await wrapper.async_generate_single("Explain quantum computing")
```

**Thinking Budget 说明：**
- `None`: 使用默认行为（thinking 模型自动关闭）
- `0`: 显式关闭 thinking
- `4096/8192/16384/32768`: 指定 thinking token 预算

### 异常处理

```python
from api_engine import (
    APIModelWrapper, APIConfig,
    ContentFilterError,
    BudgetExhaustedError,
    EmptyResponseError
)

config = APIConfig(provider="openai", model="gpt-4o-mini")
wrapper = APIModelWrapper(config)

try:
    text, usage = wrapper.generate_single("Your prompt here")
except ContentFilterError:
    print("Content was filtered by API")
except BudgetExhaustedError:
    print("API quota exhausted")
except EmptyResponseError:
    print("API returned empty response")
except Exception as e:
    print(f"Other error: {e}")
```

## 迁移指南

### 从 lib/llm_api.py 迁移

**旧代码：**
```python
from lib.llm_api import LLM_API

llm = LLM_API(model="gpt-4o-mini")
text, usage = await llm.async_generate(prompt)
```

**新代码：**
```python
from api_engine import APIModelWrapper, APIConfig

config = APIConfig(
    provider="openai",
    model="gpt-4o-mini",
    reasoning_effort="minimal"  # 如果需要
)
wrapper = APIModelWrapper(config)
text, usage = await wrapper.async_generate_single(prompt)
```

### 配置对照表

| lib/llm_api.py | api_engine.py | 说明 |
|----------------|---------------|------|
| `model` | `config.model` | 模型名称 |
| `api_key` | `config.api_key` | API 密钥 |
| `base_url` | `config.api_base` | API 端点 |
| `default_reasoning` | `config.reasoning_effort` | Reasoning 级别 |
| `max_tokens` | `params.max_tokens` | 最大输出 token |
| `temperature` | `params.temperature` | 温度参数 |

## 性能对比

### 单次调用
- **lib/llm_api.py**: 直接调用，延迟最低
- **api_engine.py**: 通过 ThreadPoolExecutor，略有开销但可忽略

### 批量调用
- **lib/llm_api.py**: 不支持批量
- **api_engine.py**: 原生批量支持，性能优秀

### 异步支持
- **lib/llm_api.py**: `asyncio.to_thread()`
- **api_engine.py**: `asyncio.to_thread()`（相同实现）

## 配置参数完整列表

```python
@dataclass
class APIConfig:
    # 基础配置
    provider: str = "openai"              # "openai" 或 "google"
    api_base: str = "http://..."          # API 端点
    api_key: str = ""                     # API 密钥
    model: str = "default"                # 模型名称
    
    # Vertex AI（仅 Google）
    vertexai_project: Optional[str] = None
    vertexai_location: Optional[str] = None
    
    # 并发控制
    max_concurrent: int = 16              # 最大并发数
    timeout: int = 300                    # 超时（秒）
    max_retries: int = 3                  # 重试次数
    retry_delay: float = 1.0              # 重试延迟基数
    
    # 扩展参数
    extra_body: Dict[str, Any] = {}       # 额外参数（vLLM 等）
    
    # 高级参数（来自 lib/llm_api.py）
    reasoning_effort: Optional[str] = None    # gpt-5/o 系列
    verbosity: Optional[str] = "medium"       # gpt-5 系列
    thinking_budget: Optional[int] = None     # Gemini thinking
    return_usage: bool = False                # 返回 token 统计
```

## 测试

运行测试脚本：

```bash
# 设置 API key
export OPENAI_API_KEY="sk-..."

# 运行测试
python test_api_engine_merge.py
```

## 注意事项

1. **向后兼容**：现有使用 `generate(prompts)` 的代码无需修改
2. **Token 统计**：需要设置 `return_usage=True` 才会收集 token 统计
3. **Reasoning Effort**：仅 gpt-5/o 系列支持
4. **Thinking Budget**：仅 Gemini 系列支持
5. **异常处理**：建议捕获 `BudgetExhaustedError` 以优雅处理配额耗尽

## 常见问题

### Q: 如何在 p4_generate.py 中使用？

A: 修改导入和初始化：

```python
# 旧代码
from lib.llm_api import LLM_API
self.llm_api = LLM_API(model)

# 新代码
from api_engine import APIModelWrapper, APIConfig
config = APIConfig(provider="openai", model=model, reasoning_effort="minimal")
self.llm_api = APIModelWrapper(config)

# 调用方式相同
text, usage = await self.llm_api.async_generate_single(prompt)
```

### Q: 批量调用如何获取 token 统计？

A: 设置 `return_usage=True`：

```python
config = APIConfig(..., return_usage=True)
wrapper = APIModelWrapper(config)
outputs = wrapper.generate(prompts)

for output in outputs:
    print(output.usage)  # 每个输出都有 usage 信息
```

### Q: 如何关闭 Gemini 的 thinking？

A: 设置 `thinking_budget=0`：

```python
config = APIConfig(
    provider="google",
    model="gemini-2.5-flash",
    thinking_budget=0  # 显式关闭
)
```

## 更多示例

查看以下文件获取更多示例：
- `test_api_engine_merge.py` - 完整测试套件
- `extractor_api.py` - 批量推理示例
- `title_optimization_v6/p4_generate.py` - 异步标题优化示例（可迁移）
