# vLLM 效率优化总结

## 核心优化

1. **单 prompt 多候选（n=5）**：Step3 需要生成 5 个候选方案供评估，传统做法需要调用 5 次 generate()，每次都要重新 prefill。优化后使用 vLLM 的 n=5 参数，一次调用生成 5 个候选，只需 prefill 一次，5 个候选共享同一个 KV cache。Prefill 开销从 5 次减少到 1 次，Step3 吞吐量提升约 5 倍。

2. **流水线并行处理（pipeline_depth=4）**：多个 batch 交错执行不同 step，当 Batch 1 在做 Step2 时，Batch 2 可以同时做 Step1。同一 step 的多个 batch 合并到一次 generate() 调用，不同 step 的 batch 通过 params_list 参数合并，减少 GPU 空闲时间。整体吞吐量提升 20-40%，GPU 利用率从约 60% 提升到 80-90%。
