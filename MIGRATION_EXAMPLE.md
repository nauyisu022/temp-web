# 迁移示例：从 lib/llm_api.py 到 api_engine.py

本文档展示如何将现有代码从 `lib/llm_api.py` 迁移到融合后的 `api_engine.py`。

## 示例 1: title_optimization_v6/p4_generate.py

### 旧代码（使用 lib/llm_api.py）

```python
from lib.llm_api import LLM_API, ContentFilterError, BudgetExhaustedError

class TitleOptimizer:
    def __init__(self, model):
        self.model = model
        self.llm_api = LLM_API(model)
    
    async def generate(self, row):
        item = row._asdict()
        
        try:
            # 第一次调用
            points_text, usage1 = await self.llm_api.async_generate(
                prompt_template.format_points(
                    original_title=item['original_title'],
                    search_terms=item['search_terms_cleaned'],
                    points=item.get('points', '')
                )
            )
            
            # 第二次调用
            title_text, usage2 = await self.llm_api.async_generate(
                prompt_template.format_title(
                    region=item["region"],
                    original_title=item['original_title'],
                    points=points_text,
                    good_keywords=item.get("good_keywords", ""),
                    bad_keywords=item.get("bad_keywords", ""),
                    expert_knowledge=item.get("expert_knowledge", ""),
                )
            )
            
            # Token 统计
            total_usage = {
                "prompt_tokens": usage1["prompt_tokens"] + usage2["prompt_tokens"],
                "completion_tokens": usage1["completion_tokens"] + usage2["completion_tokens"],
                "total_tokens": usage1["total_tokens"] + usage2["total_tokens"]
            }
            
            item['points_cleaned'] = points_text
            item['optimized_title'] = title_text
            item['prompt_tokens'] = total_usage['prompt_tokens']
            item['completion_tokens'] = total_usage['completion_tokens']
            item['total_tokens'] = total_usage['total_tokens']
            
        except ContentFilterError:
            print(f"⚠️ Content filter triggered: {item.get('item_id')}")
            item['points_cleaned'] = ''
            item['optimized_title'] = item['original_title']
        except BudgetExhaustedError:
            raise
        
        return item
```

### 新代码（使用 api_engine.py）

```python
from api_engine import APIModelWrapper, APIConfig, ContentFilterError, BudgetExhaustedError

class TitleOptimizer:
    def __init__(self, model):
        self.model = model
        
        # 配置 API
        config = APIConfig(
            provider="openai",
            model=model,
            reasoning_effort="minimal",  # 可选：为 gpt-5 系列设置
            return_usage=True
        )
        self.llm_api = APIModelWrapper(config)
    
    async def generate(self, row):
        item = row._asdict()
        
        try:
            # 第一次调用
            points_text, usage1 = await self.llm_api.async_generate_single(
                prompt_template.format_points(
                    original_title=item['original_title'],
                    search_terms=item['search_terms_cleaned'],
                    points=item.get('points', '')
                )
            )
            
            # 第二次调用
            title_text, usage2 = await self.llm_api.async_generate_single(
                prompt_template.format_title(
                    region=item["region"],
                    original_title=item['original_title'],
                    points=points_text,
                    good_keywords=item.get("good_keywords", ""),
                    bad_keywords=item.get("bad_keywords", ""),
                    expert_knowledge=item.get("expert_knowledge", ""),
                )
            )
            
            # Token 统计（相同逻辑）
            total_usage = {
                "prompt_tokens": usage1["prompt_tokens"] + usage2["prompt_tokens"],
                "completion_tokens": usage1["completion_tokens"] + usage2["completion_tokens"],
                "total_tokens": usage1["total_tokens"] + usage2["total_tokens"]
            }
            
            item['points_cleaned'] = points_text
            item['optimized_title'] = title_text
            item['prompt_tokens'] = total_usage['prompt_tokens']
            item['completion_tokens'] = total_usage['completion_tokens']
            item['total_tokens'] = total_usage['total_tokens']
            
        except ContentFilterError:
            print(f"⚠️ Content filter triggered: {item.get('item_id')}")
            item['points_cleaned'] = ''
            item['optimized_title'] = item['original_title']
        except BudgetExhaustedError:
            raise
        
        return item
```

### 主要变化

1. **导入变化**：
   ```python
   # 旧
   from lib.llm_api import LLM_API, ContentFilterError, BudgetExhaustedError
   
   # 新
   from api_engine import APIModelWrapper, APIConfig, ContentFilterError, BudgetExhaustedError
   ```

2. **初始化变化**：
   ```python
   # 旧
   self.llm_api = LLM_API(model)
   
   # 新
   config = APIConfig(provider="openai", model=model, return_usage=True)
   self.llm_api = APIModelWrapper(config)
   ```

3. **调用方法名变化**：
   ```python
   # 旧
   text, usage = await self.llm_api.async_generate(prompt)
   
   # 新
   text, usage = await self.llm_api.async_generate_single(prompt)
   ```

4. **返回格式**：完全相同，无需修改

## 示例 2: expert_knowledge/ek1_mining.py

### 旧代码

```python
from lib.llm_api import LLM_API

class KnowledgeMiner:
    def __init__(self, model):
        self.llm = LLM_API(model)
    
    def extract_knowledge(self, prompt):
        text, usage = self.llm.generate(prompt)
        return text
```

### 新代码

```python
from api_engine import APIModelWrapper, APIConfig

class KnowledgeMiner:
    def __init__(self, model):
        config = APIConfig(
            provider="openai",
            model=model,
            reasoning_effort="medium",  # 专家知识提取可能需要更高的 reasoning
            return_usage=True
        )
        self.llm = APIModelWrapper(config)
    
    def extract_knowledge(self, prompt):
        text, usage = self.llm.generate_single(prompt)
        return text
```

## 迁移检查清单

- [ ] 更新导入语句
- [ ] 创建 `APIConfig` 对象
- [ ] 将 `LLM_API(model)` 替换为 `APIModelWrapper(config)`
- [ ] 将 `async_generate()` 替换为 `async_generate_single()`
- [ ] 将 `generate()` 替换为 `generate_single()`
- [ ] 测试异常处理是否正常工作
- [ ] 验证 token 统计是否正确
- [ ] （可选）添加 `reasoning_effort` 或 `thinking_budget` 参数

## 高级配置示例

### GPT-5 系列

```python
config = APIConfig(
    provider="openai",
    model="gpt-5.2",
    reasoning_effort="high",    # 高级推理
    verbosity="detailed",       # 详细输出
    return_usage=True
)
```

### Google Gemini

```python
config = APIConfig(
    provider="google",
    model="gemini-2.5-flash",
    thinking_budget=0,          # 关闭 thinking 节省 token
    return_usage=True
)
```

### 自定义 API 端点

```python
config = APIConfig(
    provider="openai",
    api_base="http://your-server:8000/v1",
    api_key="your-api-key",
    model="custom-model",
    max_concurrent=32,          # 提高并发
    timeout=600,                # 增加超时
    return_usage=True
)
```

## 性能优化建议

1. **批量任务**：如果需要处理大量独立的 prompts，考虑使用 `generate(prompts)` 批量接口
2. **并发控制**：通过 `max_concurrent` 参数调整并发数
3. **Token 统计**：只在需要时启用 `return_usage=True`
4. **Thinking 控制**：对于 Gemini 模型，设置 `thinking_budget=0` 可以节省 token

## 常见问题

### Q: 迁移后性能有变化吗？

A: 单次调用性能基本相同。`api_engine.py` 使用 `ThreadPoolExecutor` 实现异步，与 `lib/llm_api.py` 的 `asyncio.to_thread()` 性能相当。

### Q: 需要修改现有的异常处理吗？

A: 不需要。异常类型和行为保持一致。

### Q: 可以同时使用两个库吗？

A: 可以，但建议统一使用 `api_engine.py` 以简化维护。

### Q: 如何验证迁移成功？

A: 运行现有的测试用例，确保：
1. 输出结果相同
2. Token 统计正确
3. 异常处理正常
4. 性能无明显下降

## 回滚方案

如果迁移后遇到问题，可以快速回滚：

1. 恢复原始导入：
   ```python
   from lib.llm_api import LLM_API
   ```

2. 恢复原始初始化：
   ```python
   self.llm_api = LLM_API(model)
   ```

3. 恢复原始方法调用：
   ```python
   text, usage = await self.llm_api.async_generate(prompt)
   ```

`lib/llm_api.py` 仍然保留，可以随时切换回去。
