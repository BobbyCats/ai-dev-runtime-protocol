# 工程评审（Engineering Review）

适用场景：

- 已经知道要做什么，但还没确定最小改动面
- 担心实现时会跨域、扩范围、把系统越改越乱
- 想在开工前把风险、验证、观察点先定下来

## 这一步的目标

工程评审不是让你把所有细节都想完，而是把这些关键约束定住：

- 最小改动边界
- 由谁拥有状态
- 哪些文件该动，哪些最好别动
- 失败会怎么表现
- 怎么验证
- 出问题后怎么定位
- 是否需要补 `领域地图 / 工具契约 / 执行计划 / 可观测性关联 / 成本权限预算`

## 标准问题

- 这次改动最小应该落在哪一层
- 有没有可以复用的现有实现，而不是重写
- 哪个模块拥有这份状态
- 最容易出错的两三个失败模式是什么
- 这次要补哪些日志、trace、断言或测试
- 这次是不是已经大到需要单独补领域地图或工具契约
- 改完以后怎么验证 happy path 和关键边界

## 输出要求

至少要落下这些结论：

- 写入边界
- 非目标文件
- 风险点
- 观察点
- 验证命令
- 回滚或止损思路

推荐模板：

- [templates/plan-engineering-review-工程评审.md](../../templates/plan-engineering-review-工程评审.md)

如果你已经有 `requirement-brief`、`product-review` 和 `repo-map`，建议直接生成结构化工件：

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

这样 `task-packet`、`debug-pack` 和后续 `doc-sync` 会更容易保持一致。

## 硬规则

- 说不清写入边界，不要直接开工
- 说不清验证方式，不要直接开工
- 高风险改动没有观察点和止损方案，不要直接开工
- 一旦评审结论发生变化，要写入 `决策轨迹（decision-trace）`
