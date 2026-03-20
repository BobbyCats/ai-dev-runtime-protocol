# 工程评审（Engineering Review）

如果你已经有 `requirement-brief`、`product-review` 和 `repo-map`，优先直接生成正式工件：

```bash
python -m aidrp engineering-review \
  --project-root . \
  --brief .aidrp/briefs/<brief-id>.json \
  --product-review .aidrp/product-reviews/<review-id>.json \
  --repo-map .aidrp/repo-map.json \
  --change-goal "只修这次任务需要的最小改动面" \
  --decision 可以开工 \
  --decision-reason "写入边界、观察点和验证路径已经清楚" \
  --output-dir .aidrp/engineering-reviews
```

## 输入

- 需求简报：
- 产品评审结论：
- 仓库地图：

## 最小改动边界

- 预计改动模块：
- 尽量不要动的模块：
- 状态归属：

## 风险与失败模式

- 主要风险：
- 最可能的失败模式：
- 需要补的观察点：

## 验证与止损

- 验证命令：
- 真实验收入口：
- 回滚或止损方案：

## 评审结论

- 可以开工 / 需要缩范围 / 需要补信息：
- 备注：
