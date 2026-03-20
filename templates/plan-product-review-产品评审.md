# 产品评审（Product Review）

如果你现在已经有 `requirement-brief`，优先直接生成正式工件：

```bash
python -m aidrp product-review \
  --brief .aidrp/briefs/<brief-id>.json \
  --current-goal "把第一版压成可交付的最小切片" \
  --scope-decision 保持 \
  --scope-reason "第一版边界已经清楚，先不要扩张" \
  --output-dir .aidrp/product-reviews
```

## 输入

- 需求简报：
- 当前版本目标：

## 用户与问题

- 核心用户：
- 核心痛点：
- 最先发生的场景：

## 第一版切片

- 最小有价值功能：
- 现在不做什么：
- 为什么是现在：

## Scope 决策

- 决策：扩 / 保持 / 缩
- 决策理由：

## 成功标准

- 第一阶段成功信号：
- 什么情况下才值得继续扩：

## 未决问题

- 
