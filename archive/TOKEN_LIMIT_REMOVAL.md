# API 模式 Token 限制移除说明

## 修改日期
2026-02-27

## 问题背景
在 Gemini 2.5 Flash 评测中发现，123/500 (24.6%) 的 KSP JSON 输出被截断，导致 JSON 解析失败。

**根本原因**：
- 默认 `max_tokens` 设置为 4096
- 对于复杂商品（描述长、特征多），生成完整的双语 KSP JSON 需要更多 tokens
- 当达到 token 限制时，API 强制停止生成，导致 JSON 不完整

## 解决方案
**完全移除 API 模式下的所有 token 限制**，让模型自由生成直到完成。

## 修改内容

### 1. OpenAI 兼容 API (`api_engine.py` 第 487-489 行)
```python
# 修改前
if self.config.model.startswith(("gpt-5", "o")):
    if "max_tokens" in params:
        request_kwargs["max_completion_tokens"] = params["max_tokens"]
else:
    if "max_tokens" in params:
        request_kwargs["max_tokens"] = params["max_tokens"]

# 修改后
# max_tokens 处理：API 模式不限制 token 数量，移除该参数
# 让模型自由生成直到完成
pass
```

### 2. Google Gemini API (`api_engine.py` 第 610 行)
```python
# 修改前
if "max_tokens" in params:
    config_kwargs["max_output_tokens"] = params["max_tokens"]

# 修改后
# API 模式不限制 max_tokens，让模型自由生成
```

### 3. Claude API (`api_engine.py` 第 668-672 行)
```python
# 修改前
request_kwargs = {
    "model": self.config.model,
    "max_tokens": params.get("max_tokens", 4096),
    "messages": [{"role": "user", "content": prompt}],
}

# 修改后
# 构建请求参数（API 模式不限制 max_tokens）
request_kwargs = {
    "model": self.config.model,
    "messages": [{"role": "user", "content": prompt}],
}
```

### 4. 日志输出 (`api_engine.py` 第 373-374 行)
```python
# 修改前
logger.debug(f"API generate: {len(prompts)} prompts, n={n}, "
             f"max_tokens={params.get('max_tokens', 'default')}")

# 修改后
logger.debug(f"API generate: {len(prompts)} prompts, n={n}, "
             f"max_tokens=unlimited (API mode)")
```

## 影响范围
- ✅ **OpenAI 兼容 API**（包括 Compass API 上的 Gemini、GPT 等）
- ✅ **Google Gemini API**（原生 SDK）
- ✅ **Claude API**（Anthropic SDK）

## 预期效果
1. **JSON 不再被截断**：模型可以生成完整的 KSP JSON，无论长度
2. **评测成功率提升**：从 75.4% 提升到接近 100%
3. **无需手动调整**：不需要在 shell 脚本中指定 `--max-tokens` 参数

## 注意事项
1. **成本增加**：移除限制后，模型可能生成更长的输出，导致 token 消耗增加
2. **响应时间**：更长的输出可能导致 API 响应时间增加
3. **API 自身限制**：各 API 提供商可能有自己的 token 上限（如 Claude 默认 4096），但我们不再主动限制

## 验证方法
运行以下命令验证修改：
```bash
python << 'PYEOF'
import re
with open('api_engine.py', 'r') as f:
    content = f.read()
    
# 检查是否还有硬编码的 token 限制
patterns = [r'"max_tokens":\s*\d+', r'"max_output_tokens":\s*\d+']
for pattern in patterns:
    if re.search(pattern, content):
        print(f'⚠️  发现硬编码: {pattern}')
    else:
        print(f'✅ 已移除: {pattern}')
PYEOF
```

## 建议
如果需要重新启用 token 限制（如控制成本），可以：
1. 在 shell 脚本中添加 `--max-tokens 8000` 参数
2. 或在 `config.py` 中设置默认值
3. 但建议至少设置为 8000-10000，以避免 JSON 截断问题
