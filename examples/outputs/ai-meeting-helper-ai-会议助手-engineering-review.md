# Engineering Review | 工程评审: AI meeting helper AI 会议助手

- Review ID | 评审 ID: `ai-meeting-helper-ai-会议助手-engineering-review`
- Brief ID | 简报 ID: `ai-meeting-helper-ai-会议助手`
- Product Review ID | 产品评审 ID: `ai-meeting-helper-ai-会议助手-product-review`
- Generated | 生成时间: `2026-03-20T19:11:29+00:00`

## 当前改动目标 | Change Goal

先固定写入边界、候选文件和验证方式

## 最小改动边界 | Write Boundary

- `templates/prompts-提示词.md`
- `src/aidrp/cli.py`
- `src/aidrp/utils.py`

## 尽量不要动的文件 | Avoid Files

- `.github/workflows/ci.yml`
- `AGENTS.md`
- `docs/architecture-架构说明.md`
- `docs/playbooks/bugfix-缺陷修复.md`

## 状态归属 | State Owner

- prompts-提示词

## 候选文件 | Candidate Files

- `README.md`: Matched tokens: discovery, interview
- `templates/prompts-提示词.md`: Matched tokens: discovery, first, interview
- `src/aidrp/cli.py`: Matched tokens: brief
- `src/aidrp/utils.py`: Matched tokens: are
- `templates/requirement-brief-需求简报.md`: Matched tokens: brief, use
- `src/aidrp/requirement_brief.py`: Matched tokens: brief
- `src/aidrp/tool_contract.py`: Matched tokens: too
- `AGENTS.md`: High-signal documentation file
- `ONBOARDING.md`: High-signal documentation file
- `docs/playbooks/discovery-interview-需求访谈.md`: Matched tokens: discovery, interview

## 风险点 | Risks

- 关键编号没有透传到日志时，排障会退化成大范围扫描。

## 失败模式 | Failure Modes

- 操作完成了，但日志里缺少 trace / decision / plan / tool call 编号。
- 代码修通了 happy path，但真实入口仍然复现旧问题。

## 观察点 | Observability Points

- 在入口、计划确认、执行器三个边界记录 trace_id / decision_id / plan_id / tool_call_id。
- 日志里同时记录 expected target 和 actual target，避免只看到“成功/失败”而不知道删的是谁。

## 验证命令 | Validation Commands

- `aidrp`
- `python -m unittest discover -s tests -v`

## 真实验收入口与止损 | Live QA And Rollback

- 真实验收入口: 先把第一阶段要不要做、做什么聊清楚 | Clarify the first milestone
- 回滚或止损方案: 如果真实验收或日志编号链路不稳定，就回到上一个可验证版本，并保留这次决策轨迹。

## 评审结论 | Review Decision

- 结论: `ready` | 可以开工
- 原因: 改动边界、风险、观察点和验证路径已经明确，可以进入实现。

## 推荐补哪些高级工件 | Recommended Artifacts

- `domain-map` [可选]: 场景开始跨多个业务域时，需要先明确状态归属和编排关系。
- `tool-contract` [可选]: 一旦进入工具调用和执行器阶段，就要明确输入、输出、失败语义和权限边界。
- `execution-plan` [可选]: 涉及多步确认或批量动作时，计划与执行分离能显著减少返工和慢循环。
- `observability-correlation` [需要]: 只要排障可能依赖编号和日志，就应该尽早接入关联定位。
- `cost-privacy-budget` [可选]: AI 原生产品只要要长期运行，就要提前约束上下文、权限和敏感数据暴露范围。

## 下一步 | Next Step

- 写 task-packet 或 debug-pack；如果评审结论不是 ready，就先缩范围或补信息。
