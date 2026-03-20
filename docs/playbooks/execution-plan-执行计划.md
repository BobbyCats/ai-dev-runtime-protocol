# 执行计划（Execution Plan）

适用场景：

- 一次任务不是单步操作，而是多步计划
- ReAct 式逐步推理太慢、太贵、太容易上下文漂移
- 你希望先统一规划，再统一执行

## 这一步解决什么问题

“任务包”解决的是一次开发任务的边界。  
“执行计划”解决的是一次任务内部的动作流水线。

也就是说：

- 任务包负责定义做什么
- 执行计划负责定义这次具体怎么一步步执行

## 一份执行计划至少包含

- 目标
- 前置条件
- 计划步骤
- 每一步依赖什么输入
- 每一步调用什么工具
- 哪些步骤需要人工确认
- 成功条件与失败退出条件

## 推荐规则

- 先规划批量动作，再执行批量动作
- 计划阶段可以慢一点，执行阶段要尽量确定性
- 高风险步骤前必须有确认门
- 一个计划里的步骤数量不要无限膨胀，必要时拆子计划

推荐模板：

- [templates/execution-plan-执行计划.md](../../templates/execution-plan-执行计划.md)

## CLI 用法

```bash
python -m aidrp execution-plan \
  --title "Delete event safely" \
  --goal "Delete the targeted event after confirmation." \
  --step "Resolve target|event_id|fetch_event|event snapshot|false" \
  --step "Execute delete|event snapshot|delete_event|delete result|true"
```
