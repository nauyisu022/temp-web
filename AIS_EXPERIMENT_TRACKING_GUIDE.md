# AIS Experiment Tracking SDK 使用指南

## 概述

AIS Experiment Tracking SDK (`shopee-aip-metric-track`) 是用于在 AIS 平台上记录和可视化实验指标的工具。它可以帮助你：
- 记录标量参数（如准确率、损失值等）
- 绘制线性图表（如训练过程中的 loss 曲线）
- 在 Run List 中比较不同实验的参数
- 在 Charts 页面可视化训练过程

## 安装

```bash
pip install shopee-aip-metric-track -i https://pypi.shopee.io/simple/
```

## 快速开始

### 1. 初始化 MetricLog

在 AIS 平台上使用时，可以直接使用默认参数初始化（平台会自动识别环境）：

```python
from metriclog import MetricLog
from metricstore.types import GREY_ENDPOINT

# 在 AIS 平台上使用（推荐）
log = MetricLog()

# 如果不在 AIS 平台上，需要手动指定参数
log = MetricLog(
    project_id=76,
    run_id=292,
    email="your.email@shopee.com",
    token="your_token_here",
    endpoint=GREY_ENDPOINT
)
```

### 2. 记录标量值（Scalar）

用于记录单个数值指标，这些值会在 Run List 页面显示，方便比较不同实验：

```python
# 记录最终损失值
log.log_scalar(name='final_loss', value=0.95)

# 记录最佳准确率
log.log_scalar(name='best_accuracy', value=0.977)

# 记录平均准确率
log.log_scalar(name='avg_accuracy', value=0.977)
```

**使用场景：**
- 记录实验的关键指标（如最佳准确率、最终损失等）
- 记录超参数（如学习率、批次大小等）
- 记录实验配置信息

**注意事项：**
- 所有通过 `log_scalar` 记录的参数都会自动显示在 Run List 页面
- 可以用于对比不同实验的参数和结果

### 3. 记录线性图表（Line Chart）

用于记录训练过程中的指标变化，绘制成曲线图：

```python
# 基本用法：记录训练过程中的指标
step = 0
for epoch in range(10):
    for batch_idx in range(100):
        # 模拟训练过程
        acc1 = 0.8 + step / 1000.0
        loss = 0.2 - step / 1000.0
        
        # 记录线性图表数据
        log.log_linearchart(
            epoch=epoch + 1,
            step=step,
            data={
                "acc1": acc1,
                "loss": loss
            }
        )
        step += 1
```

**参数说明：**
- `epoch`: 当前 epoch 编号（从 1 开始）
- `step`: 当前步数（全局步数，用于 x 轴）
- `data`: 字典类型，key 为指标名称，value 为指标值

**使用场景：**
- 记录训练过程中的 loss 变化
- 记录验证集上的准确率变化
- 记录多个指标在同一图表中对比

**注意事项：**
- `data` 必须是字典类型
- 同一个 `name` 的指标在不同 Run 中会自动组织在一起，方便对比
- 所有图表会显示在 Charts 页面

## 完整示例

```python
from io import BytesIO
from metriclog import MetricLog
from metricstore.types import GREY_ENDPOINT

if __name__ == "__main__":
    # 初始化（在 AIS 平台上会自动识别环境）
    log = MetricLog()
    
    # ========== 记录超参数 ==========
    log.log_scalar(name='learning_rate', value=0.001)
    log.log_scalar(name='batch_size', value=32)
    log.log_scalar(name='epochs', value=10)
    
    # ========== 模拟训练过程 ==========
    best_accuracy = 0.0
    step = 0
    
    for epoch in range(10):
        for batch_idx in range(100):
            # 模拟训练指标
            train_loss = 0.5 - (epoch * 100 + batch_idx) / 2000.0
            train_acc = 0.6 + (epoch * 100 + batch_idx) / 2000.0
            
            # 记录训练过程指标
            log.log_linearchart(
                epoch=epoch + 1,
                step=step,
                data={
                    "train_loss": train_loss,
                    "train_acc": train_acc
                }
            )
            
            # 每 10 个 batch 记录一次验证指标
            if batch_idx % 10 == 0:
                val_loss = train_loss * 0.9
                val_acc = train_acc * 1.05
                
                log.log_linearchart(
                    epoch=epoch + 1,
                    step=step,
                    data={
                        "val_loss": val_loss,
                        "val_acc": val_acc
                    }
                )
                
                # 更新最佳准确率
                if val_acc > best_accuracy:
                    best_accuracy = val_acc
            
            step += 1
    
    # ========== 记录最终结果 ==========
    log.log_scalar(name='best_accuracy', value=best_accuracy)
    log.log_scalar(name='final_train_loss', value=train_loss)
    log.log_scalar(name='final_val_loss', value=val_loss)
```

## 功能对比

| 功能 | 方法 | 显示位置 | 用途 |
|------|------|----------|------|
| 标量参数 | `log_scalar()` | Run List 页面 | 记录单个数值，用于对比不同实验 |
| 线性图表 | `log_linearchart()` | Charts 页面 | 记录训练过程，绘制曲线图 |

## 最佳实践

### 1. 记录超参数
在训练开始前记录所有重要的超参数，方便后续对比：

```python
log.log_scalar(name='learning_rate', value=0.001)
log.log_scalar(name='batch_size', value=32)
log.log_scalar(name='model_name', value='resnet50')
log.log_scalar(name='optimizer', value='adam')
```

### 2. 记录训练过程
定期记录训练指标，建议：
- 每个 epoch 记录一次验证指标
- 每 N 个 batch 记录一次训练指标（避免过于频繁）

```python
# 每个 epoch 记录一次
for epoch in range(num_epochs):
    # ... 训练代码 ...
    
    # 记录 epoch 级别的指标
    log.log_linearchart(
        epoch=epoch + 1,
        step=epoch,
        data={
            "train_loss": avg_train_loss,
            "val_loss": avg_val_loss,
            "val_acc": val_accuracy
        }
    )
```

### 3. 记录最终结果
训练结束后记录关键指标：

```python
log.log_scalar(name='best_accuracy', value=best_acc)
log.log_scalar(name='final_loss', value=final_loss)
log.log_scalar(name='training_time', value=training_time_seconds)
```

### 4. 命名规范
- 使用有意义的名称：`best_accuracy` 而不是 `acc`
- 保持一致性：在不同实验中使用相同的指标名称
- 使用下划线分隔：`train_loss` 而不是 `trainLoss`

## 常见问题

### Q: 如何在非 AIS 平台使用？
A: 需要手动指定 `project_id`, `run_id`, `email`, `token` 和 `endpoint` 参数。

### Q: 可以记录哪些类型的数据？
A: 目前支持标量值（数字）和线性图表数据。`log_scalar` 记录单个值，`log_linearchart` 记录时间序列数据。

### Q: 如何对比多个实验？
A: 使用相同的指标名称记录数据，平台会自动将不同 Run 的数据组织在一起进行对比。

### Q: step 参数的作用是什么？
A: `step` 是全局步数，用作图表的 x 轴。应该是一个递增的数值，可以是 batch 数、样本数或其他全局计数。

## 参考资源

- AIS 平台文档：Experiment Tracking SDK
- 联系支持：kexin.wu@shopee.com (AIS)
