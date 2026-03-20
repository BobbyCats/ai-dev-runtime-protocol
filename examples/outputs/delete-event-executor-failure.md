# Debug Pack | 排障包: Delete event executor failure

- Debug ID | 排障 ID: `delete-event-executor-failure`
- Trace ID | 追踪 ID: `trace-77`
- Generated | 生成时间: `2026-03-20T18:24:10+00:00`

## Failure Summary | 问题摘要

- Symptom | 症状: delete action reports failure
- Observed | 实际表现: executor returns version mismatch
- Expected | 期望表现: executor deletes the target event
- Impact | 影响: user cannot delete schedule events
- Entrypoint | 入口: calendar.delete
- Failure Stage | 故障阶段: executor

## Reproduction Steps | 复现步骤

- Delete an event from the schedule list.

## Triage Read Order | 初步排查阅读顺序

- `AGENTS.md`
- `.aidrp/repo-map.md`
- `src/aidrp/debug_pack.py`
- `src/aidrp/doc_sync.py`
- `templates/requirement-brief-需求简报.md`
- `AGENTS.md`
- `ONBOARDING.md`
- `README.md`
- `src/aidrp/trace.py`
- `src/aidrp/cli.py`

## Suspected Files | 疑似文件

- `src/aidrp/debug_pack.py`: Provided explicitly by the reporter
- `src/aidrp/doc_sync.py`: Matched tokens: action
- `templates/requirement-brief-需求简报.md`: Matched tokens: target, user
- `AGENTS.md`: High-signal documentation file
- `ONBOARDING.md`: High-signal documentation file
- `README.md`: High-signal documentation file
- `src/aidrp/trace.py`: Matched tokens: event
- `src/aidrp/cli.py`: High-signal source file
- `src/aidrp/design_token_pack.py`: High-signal source file
- `src/aidrp/repo_map.py`: High-signal source file

## Correlation IDs | 关联编号

- `trace_id`: `trace-77`
- `request_id`: `req-88`
- `decision_id`: `dec-99`
- `plan_id`: `plan-delete-01`
- `tool_call_id`: `tool-delete-01`

## Log Focus | 日志聚焦

- 先按关联编号 grep 日志，再决定是否看代码。
- 优先检查 `executor` 阶段前后的日志连续性。
- 先确认入口 `calendar.delete` 是否真的被触发。
- 只有日志证据不足时，才扩大到代码级搜索。

### Grep Queries | 检索关键词

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

## Log Hits | 日志命中

- `examples/logs/runtime-delete-demo.log:1` matched `trace_id:trace-77`, `trace-77`, `request_id:req-88`, `req-88`, `decision_id:dec-99`, `dec-99`, `plan_id:plan-delete-01`, `plan-delete-01`, `tool_call_id:tool-delete-01`, `tool-delete-01`, `entrypoint:calendar.delete`, `calendar.delete`: 2026-03-21T10:00:01Z level=INFO trace_id:trace-77 request_id:req-88 decision_id:dec-99 plan_id:plan-delete-01 tool_call_id:tool-delete-01 entrypoint:calendar.delete failure_stage:planner msg="delete request received"
- `examples/logs/runtime-delete-demo.log:2` matched `trace_id:trace-77`, `trace-77`, `request_id:req-88`, `req-88`, `decision_id:dec-99`, `dec-99`, `plan_id:plan-delete-01`, `plan-delete-01`, `entrypoint:calendar.delete`, `calendar.delete`: 2026-03-21T10:00:01Z level=INFO trace_id:trace-77 request_id:req-88 decision_id:dec-99 plan_id:plan-delete-01 entrypoint:calendar.delete failure_stage:planner msg="resolved stable event id evt_123"
- `examples/logs/runtime-delete-demo.log:3` matched `trace_id:trace-77`, `trace-77`, `request_id:req-88`, `req-88`, `decision_id:dec-99`, `dec-99`, `plan_id:plan-delete-01`, `plan-delete-01`, `tool_call_id:tool-delete-01`, `tool-delete-01`, `entrypoint:calendar.delete`, `calendar.delete`, `failure_stage:executor`, `executor`, `version mismatched`: 2026-03-21T10:00:02Z level=ERROR trace_id:trace-77 request_id:req-88 decision_id:dec-99 plan_id:plan-delete-01 tool_call_id:tool-delete-01 entrypoint:calendar.delete failure_stage:executor msg="delete failed because event version mismatched

## Recent Commits | 最近提交

- `75045c8 运行协议: 补齐高级工件与编号化排障规范`
- `1bae94e Add HTML preview for design token packs`
- `91ce145 Add design token system to runtime protocol`
- `9b91868 Add stage routing and documentation sync workflow`
- `045ec4b Refine Chinese-first wording and adaptation guidance`
- `81b7b5f Add discovery interview and requirement brief workflow`
- `55fff14 Localize docs and artifacts with bilingual terminology`
- `d986126 Bootstrap runtime-oriented AI dev protocol`
