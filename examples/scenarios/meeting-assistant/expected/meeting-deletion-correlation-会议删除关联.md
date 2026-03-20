# Observability Correlation | 可观测性关联: Meeting deletion correlation 会议删除关联

- Correlation ID | 关联 ID: `meeting-deletion-correlation-会议删除关联`
- Generated | 生成时间: `2026-03-20T18:50:32+00:00`

## Correlation Keys | 关联编号

- `trace_id`: `trace-meeting-001`
- `request_id`: `req-meeting-001`
- `decision_id`: `dec-meeting-001`
- `plan_id`: `plan-delete-001`
- `tool_call_id`: `tool-delete-001`
- `entrypoint`: `meeting.delete`
- `failure_stage`: `executor`

## Log Files | 日志文件

- `logs/runtime.log`

## Grep Queries | 检索关键词

- `trace_id:trace-meeting-001`
- `trace-meeting-001`
- `request_id:req-meeting-001`
- `req-meeting-001`
- `decision_id:dec-meeting-001`
- `dec-meeting-001`
- `plan_id:plan-delete-001`
- `plan-delete-001`
- `tool_call_id:tool-delete-001`
- `tool-delete-001`
- `entrypoint:meeting.delete`
- `meeting.delete`
- `failure_stage:executor`
- `executor`
- `wrong meeting removed`

## Review Order | 排查顺序

- 先按关联编号 grep 日志，再决定是否看代码。
- 优先检查 `executor` 阶段前后的日志连续性。
- 先确认入口 `meeting.delete` 是否真的被触发。
- 只有日志证据不足时，才扩大到代码级搜索。

## Matched Entries | 命中日志

- `logs/runtime.log:1` matched `trace_id:trace-meeting-001`, `trace-meeting-001`, `request_id:req-meeting-001`, `req-meeting-001`, `decision_id:dec-meeting-001`, `dec-meeting-001`, `plan_id:plan-delete-001`, `plan-delete-001`, `tool_call_id:tool-delete-001`, `tool-delete-001`, `entrypoint:meeting.delete`, `meeting.delete`: trace_id:trace-meeting-001 request_id:req-meeting-001 decision_id:dec-meeting-001 plan_id:plan-delete-001 tool_call_id:tool-delete-001 entrypoint:meeting.delete failure_stage:planner msg="resolved delete request from selected card"
- `logs/runtime.log:2` matched `trace_id:trace-meeting-001`, `trace-meeting-001`, `request_id:req-meeting-001`, `req-meeting-001`, `decision_id:dec-meeting-001`, `dec-meeting-001`, `plan_id:plan-delete-001`, `plan-delete-001`, `tool_call_id:tool-delete-001`, `tool-delete-001`, `entrypoint:meeting.delete`, `meeting.delete`, `failure_stage:executor`, `executor`, `wrong meeting removed`: trace_id:trace-meeting-001 request_id:req-meeting-001 decision_id:dec-meeting-001 plan_id:plan-delete-001 tool_call_id:tool-delete-001 entrypoint:meeting.delete failure_stage:executor msg="wrong meeting removed" selection_id=card-2 expected

## Failure Signature | 故障签名

- 入口 `meeting.delete` 已有日志，可继续向下缩到故障阶段。
- 故障阶段 `executor` 已有日志，可继续比对前后阶段差异。
- 关键编号已经能串起来，优先比较计划、工具调用和状态写入的差异。
