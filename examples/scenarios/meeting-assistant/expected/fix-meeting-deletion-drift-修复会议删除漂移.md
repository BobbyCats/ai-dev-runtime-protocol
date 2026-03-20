# Task Packet | 任务包: Fix meeting deletion drift 修复会议删除漂移

- Task ID | 任务 ID: `fix-meeting-deletion-drift-修复会议删除漂移`
- Type | 类型: `bugfix`
- Generated | 生成时间: `2026-03-20T18:50:32+00:00`

## Objective | 目标

只修删除解析和执行链路，不顺手扩成一次存储层重构

## Scope | 范围

- 只改删除目标解析、执行器和相关测试

## Non-Goals | 不做什么

- 不重做整个会议列表状态管理

## Acceptance Criteria | 验收标准

- 删除动作必须命中正确会议
- 日志里能串起删除链路的关键编号

## Constraints | 约束

- 不要扩大到邀请、同步或提醒功能

## Read Order | 阅读顺序

- `AGENTS.md`
- `.aidrp/repo-map.md`
- `README.md`
- `src/meeting_assistant.py`
- `src/calendar_agent.py`
- `pyproject.toml`
- `src/event_store.py`
- `src/ui_state.py`
- `design-system/meeting-ui-tokens.json`
- `.aidrpignore`
- `logs/runtime.log`

## Candidate Files | 候选文件

- `README.md`: Matched tokens: fix, meeting
- `src/meeting_assistant.py`: Matched tokens: event, meeting
- `src/calendar_agent.py`: Matched tokens: delete, meeting
- `AGENTS.md`: High-signal documentation file
- `pyproject.toml`: High-signal configuration file
- `src/event_store.py`: Matched tokens: event
- `src/ui_state.py`: Matched tokens: meeting
- `design-system/meeting-ui-tokens.json`: Matched tokens: meeting
- `.aidrpignore`: High-signal source file
- `logs/runtime.log`: High-signal source file

## Validation Commands | 验证命令

- `python`: `meeting-demo`
