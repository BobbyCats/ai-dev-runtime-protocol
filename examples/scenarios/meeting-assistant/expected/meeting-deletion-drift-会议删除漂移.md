# Debug Pack | 排障包: Meeting deletion drift 会议删除漂移

- Debug ID | 排障 ID: `meeting-deletion-drift-会议删除漂移`
- Trace ID | 追踪 ID: `trace-meeting-001`
- Generated | 生成时间: `2026-03-20T19:11:28+00:00`

## Failure Summary | 问题摘要

- Symptom | 症状: 删除选中的会议时，另一条会议也可能被误删
- Observed | 实际表现: 界面提示删除成功，但消失的是错误的会议卡片
- Expected | 期望表现: 只能删除用户点中的会议
- Impact | 影响: 团队会对会议状态失去信任，后续改期和确认都不可靠
- Entrypoint | 入口: meeting.delete
- Failure Stage | 故障阶段: executor

## Reproduction Steps | 复现步骤

- 打开会议列表并删除第二条会议
- 确认弹窗后观察实际消失的卡片

## Triage Read Order | 初步排查阅读顺序

- `AGENTS.md`
- `.aidrp/repo-map.md`
- `src/calendar_agent.py`
- `src/ui_state.py`
- `README.md`
- `src/meeting_assistant.py`
- `AGENTS.md`
- `pyproject.toml`
- `design-system/meeting-ui-tokens.json`
- `src/event_store.py`

## Suspected Files | 疑似文件

- `src/calendar_agent.py`: Provided explicitly by the reporter
- `src/ui_state.py`: Provided explicitly by the reporter
- `README.md`: Matched tokens: meeting
- `src/meeting_assistant.py`: Matched tokens: meeting
- `AGENTS.md`: High-signal documentation file
- `pyproject.toml`: High-signal configuration file
- `design-system/meeting-ui-tokens.json`: Matched tokens: meeting
- `src/event_store.py`: High-signal source file
- `.aidrpignore`: High-signal source file
- `logs/runtime.log`: High-signal source file

## Correlation IDs | 关联编号

- `trace_id`: `trace-meeting-001`
- `request_id`: `req-meeting-001`
- `decision_id`: `dec-meeting-001`
- `plan_id`: `plan-delete-001`
- `tool_call_id`: `tool-delete-001`

## Log Focus | 日志聚焦

- 先按关联编号 grep 日志，再决定是否看代码。
- 优先检查 `executor` 阶段前后的日志连续性。
- 先确认入口 `meeting.delete` 是否真的被触发。
- 只有日志证据不足时，才扩大到代码级搜索。

### Grep Queries | 检索关键词

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
- `selection_id`
- `meeting_id`

## Log Hits | 日志命中

- `logs/runtime.log:1` matched `trace_id:trace-meeting-001`, `trace-meeting-001`, `request_id:req-meeting-001`, `req-meeting-001`, `decision_id:dec-meeting-001`, `dec-meeting-001`, `plan_id:plan-delete-001`, `plan-delete-001`, `tool_call_id:tool-delete-001`, `tool-delete-001`, `entrypoint:meeting.delete`, `meeting.delete`: trace_id:trace-meeting-001 request_id:req-meeting-001 decision_id:dec-meeting-001 plan_id:plan-delete-001 tool_call_id:tool-delete-001 entrypoint:meeting.delete failure_stage:planner msg="resolved delete request from selected card"
- `logs/runtime.log:2` matched `trace_id:trace-meeting-001`, `trace-meeting-001`, `request_id:req-meeting-001`, `req-meeting-001`, `decision_id:dec-meeting-001`, `dec-meeting-001`, `plan_id:plan-delete-001`, `plan-delete-001`, `tool_call_id:tool-delete-001`, `tool-delete-001`, `entrypoint:meeting.delete`, `meeting.delete`, `failure_stage:executor`, `executor`, `wrong meeting removed`, `selection_id`, `meeting_id`: trace_id:trace-meeting-001 request_id:req-meeting-001 decision_id:dec-meeting-001 plan_id:plan-delete-001 tool_call_id:tool-delete-001 entrypoint:meeting.delete failure_stage:executor msg="wrong meeting removed" selection_id=card-2 expected

## Evidence | 证据

- `logs/runtime.log` matched `wrong meeting removed`: trace-meeting-001 request_id:req-meeting-001 decision_id:dec-meeting-001 plan_id:plan-delete-001 tool_call_id:tool-delete-001 entrypoint:meeting.delete failure_stage:executor msg="wrong meeting removed" selection_id=card-2 expected_meeting_id=meeting-2 actual_meeting_id=meeting-1
- `README.md` matched `meeting_id`: - `src/calendar_agent.py` - `src/event_store.py` - `src/ui_state.py` - `design-system/meeting-ui-tokens.json` - `logs/runtime.log` 这个样例的核心 bug 是： **删除会议时，系统有时按可见卡片顺序删，而不是按稳定的 `meeting_id` 删。** 这正好适合演示： - `task-packet` - `debug-pack` - `observability-correlation` - `eval-case` - `doc-sync`
- `src/calendar_agent.py` matched `selection_id`: ENTRYPOINT = "meeting.delete" def build_delete_plan(selection_id: str) -> dict[str, str]: return { "entrypoint": ENTRYPOINT, "selection_id": selection_id, "intent": "delete meeting by user-selected card", } def
- `src/event_store.py` matched `meeting_id`: -> None: self.items = list(items) def delete_by_index(self, visible_index: int) -> dict[str, str]: return self.items.pop(visible_index - 1) def delete_by_meeting_id(self, meeting_id: str) -> dict[str, str]: for index, item in enumerate(self.items): if item["meeting_id"] == meeting_id: return self.items.pop(
- `src/meeting_assistant.py` matched `selection_id`: ": "Design Critique"}, {"meeting_id": "meeting-3", "title": "Hiring Sync"}, ] ) cards = visible_meeting_cards(store.items) plan = build_delete_plan(selection_id="card-2") result = delete_selected_meeting(selection_id="card-2", visible_cards=cards, store=store) return f"{plan['entrypoint']} -> {result['deleted_meeting_id']}" if _
- `src/ui_state.py` matched `meeting_id`: cards = [] for visible_index, meeting in enumerate(meetings, start=1): cards.append( { "card_id": f"card-{visible_index}", "meeting_id": meeting["meeting_id"], "visible_index": visible_index, "title": meeting["title"], } ) return cards
