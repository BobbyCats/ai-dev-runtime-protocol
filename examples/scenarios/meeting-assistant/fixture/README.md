# Meeting Assistant Fixture

这是一个最小的 AI 会议助手样例仓库。

它故意只保留最少结构：

- `src/calendar_agent.py`
- `src/event_store.py`
- `src/ui_state.py`
- `design-system/meeting-ui-tokens.json`
- `logs/runtime.log`

这个样例的核心 bug 是：

**删除会议时，系统有时按可见卡片顺序删，而不是按稳定的 `meeting_id` 删。**

这正好适合演示：

- `task-packet`
- `debug-pack`
- `observability-correlation`
- `eval-case`
- `doc-sync`
