# Engineering Review | 工程评审: AI 会议助手第一版

- Review ID | 评审 ID: `ai-会议助手第一版-engineering-review`
- Brief ID | 简报 ID: `ai-会议助手第一版`
- Product Review ID | 产品评审 ID: `ai-会议助手第一版-product-review`
- Generated | 生成时间: `2026-03-20T19:11:28+00:00`

## 当前改动目标 | Change Goal

只修删除误删链路，不顺手扩成一次存储层重构

## 最小改动边界 | Write Boundary

- `src/meeting_assistant.py`
- `src/calendar_agent.py`
- `src/event_store.py`

## 尽量不要动的文件 | Avoid Files

- `AGENTS.md`
- `README.md`

## 状态归属 | State Owner

- meeting_assistant

## 候选文件 | Candidate Files

- `AGENTS.md`: High-signal documentation file
- `README.md`: High-signal documentation file
- `pyproject.toml`: High-signal configuration file
- `src/meeting_assistant.py`: High-signal source file
- `src/calendar_agent.py`: High-signal source file
- `src/event_store.py`: High-signal source file
- `src/ui_state.py`: High-signal source file
- `.aidrpignore`: High-signal source file
- `logs/runtime.log`: High-signal source file

## 风险点 | Risks

- 选择器、可见顺序或稳定 ID 不一致时，可能删除错误对象。
- 关键编号没有透传到日志时，排障会退化成大范围扫描。

## 失败模式 | Failure Modes

- 删除确认的是 A，但执行器真正删掉的是 B。
- 操作完成了，但日志里缺少 trace / decision / plan / tool call 编号。
- 代码修通了 happy path，但真实入口仍然复现旧问题。

## 观察点 | Observability Points

- 在入口、计划确认、执行器三个边界记录 trace_id / decision_id / plan_id / tool_call_id。
- 日志里同时记录 expected target 和 actual target，避免只看到“成功/失败”而不知道删的是谁。
- 删除链路必须记录 selection_id、stable_id 和最终写入目标。

## 验证命令 | Validation Commands

- `meeting-demo`
- `python -m unittest discover -s tests -v`

## 真实验收入口与止损 | Live QA And Rollback

- 真实验收入口: 通过聊天创建、改期和删除会议
- 回滚或止损方案: 如果真实验收或日志编号链路不稳定，就回到上一个可验证版本，并保留这次决策轨迹。

## 评审结论 | Review Decision

- 结论: `ready` | 可以开工
- 原因: 写入边界、风险、日志观察点和验证方式已经足够清楚

## 推荐补哪些高级工件 | Recommended Artifacts

- `domain-map` [需要]: 场景开始跨多个业务域时，需要先明确状态归属和编排关系。
- `tool-contract` [需要]: 一旦进入工具调用和执行器阶段，就要明确输入、输出、失败语义和权限边界。
- `execution-plan` [需要]: 涉及多步确认或批量动作时，计划与执行分离能显著减少返工和慢循环。
- `observability-correlation` [需要]: 只要排障可能依赖编号和日志，就应该尽早接入关联定位。
- `cost-privacy-budget` [可选]: AI 原生产品只要要长期运行，就要提前约束上下文、权限和敏感数据暴露范围。

## 下一步 | Next Step

- 写 task-packet 或 debug-pack；如果评审结论不是 ready，就先缩范围或补信息。
