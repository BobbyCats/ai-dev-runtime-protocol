# Observability Correlation | 可观测性关联: Delete event correlation

- Correlation ID | 关联 ID: `delete-event-correlation`
- Generated | 生成时间: `2026-03-20T18:22:39+00:00`

## Correlation Keys | 关联编号

- `trace_id`: `trace-77`
- `request_id`: `req-88`
- `decision_id`: `dec-99`
- `plan_id`: `plan-delete-01`
- `tool_call_id`: `tool-delete-01`
- `entrypoint`: `calendar.delete`
- `failure_stage`: `executor`

## Log Files | 日志文件

- `examples/logs/runtime-delete-demo.log`

## Grep Queries | 检索关键词

- `trace_id:trace-77`
- `trace-77`
- `request_id:req-88`
- `req-88`
- `decision_id:dec-99`
- `dec-99`
- `plan_id:plan-delete-01`
- `plan-delete-01`
- `tool_call_id:tool-delete-01`
- `tool-delete-01`
- `entrypoint:calendar.delete`
- `calendar.delete`
- `failure_stage:executor`
- `executor`
- `version mismatched`

## Review Order | 排查顺序

- 先按关联编号 grep 日志，再决定是否看代码。
- 优先检查 `executor` 阶段前后的日志连续性。
- 先确认入口 `calendar.delete` 是否真的被触发。
- 只有日志证据不足时，才扩大到代码级搜索。

## Matched Entries | 命中日志

- `examples/logs/runtime-delete-demo.log:1` matched `trace_id:trace-77`, `trace-77`, `request_id:req-88`, `req-88`, `decision_id:dec-99`, `dec-99`, `plan_id:plan-delete-01`, `plan-delete-01`, `tool_call_id:tool-delete-01`, `tool-delete-01`, `entrypoint:calendar.delete`, `calendar.delete`: 2026-03-21T10:00:01Z level=INFO trace_id:trace-77 request_id:req-88 decision_id:dec-99 plan_id:plan-delete-01 tool_call_id:tool-delete-01 entrypoint:calendar.delete failure_stage:planner msg="delete request received"
- `examples/logs/runtime-delete-demo.log:2` matched `trace_id:trace-77`, `trace-77`, `request_id:req-88`, `req-88`, `decision_id:dec-99`, `dec-99`, `plan_id:plan-delete-01`, `plan-delete-01`, `entrypoint:calendar.delete`, `calendar.delete`: 2026-03-21T10:00:01Z level=INFO trace_id:trace-77 request_id:req-88 decision_id:dec-99 plan_id:plan-delete-01 entrypoint:calendar.delete failure_stage:planner msg="resolved stable event id evt_123"
- `examples/logs/runtime-delete-demo.log:3` matched `trace_id:trace-77`, `trace-77`, `request_id:req-88`, `req-88`, `decision_id:dec-99`, `dec-99`, `plan_id:plan-delete-01`, `plan-delete-01`, `tool_call_id:tool-delete-01`, `tool-delete-01`, `entrypoint:calendar.delete`, `calendar.delete`, `failure_stage:executor`, `executor`, `version mismatched`: 2026-03-21T10:00:02Z level=ERROR trace_id:trace-77 request_id:req-88 decision_id:dec-99 plan_id:plan-delete-01 tool_call_id:tool-delete-01 entrypoint:calendar.delete failure_stage:executor msg="delete failed because event version mismatched

## Failure Signature | 故障签名

- 入口 `calendar.delete` 已有日志，可继续向下缩到故障阶段。
- 故障阶段 `executor` 已有日志，可继续比对前后阶段差异。
- 关键编号已经能串起来，优先比较计划、工具调用和状态写入的差异。
