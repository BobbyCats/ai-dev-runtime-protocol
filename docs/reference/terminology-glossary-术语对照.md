# 术语对照（Terminology Glossary）

这份表不是给你背单词用的，而是帮你把术语和实际动作一一对应起来。

| English | 中文主叫法 | 你可以直接理解成 |
| --- | --- | --- |
| repo-map | 仓库地图 | 这个项目的结构摘要 |
| requirement-brief | 需求简报 | 把模糊想法收敛后的简报 |
| design-token-pack | 设计令牌包 | 把颜色、字号、间距、语义样式变成结构化约束 |
| task-packet | 任务包 | 一次任务的工作单 |
| debug-pack | 排障包 | 一次 bug 的排查资料包 |
| decision-trace | 决策轨迹 | 为什么这么改的记录 |
| eval-case | 回归用例 | 为了防止 bug 再犯的检查项 |
| doc-sync | 文档同步包 | 判断 README 和核心文档该怎么同步 |
| domain-map | 领域地图 | 哪些业务域存在、谁拥有状态 |
| tool-contract | 工具契约 | 工具到底能做什么、失败时怎么返回 |
| execution-plan | 执行计划 | 一次任务内部的步骤计划 |
| observability-correlation | 可观测性关联 | 用编号把日志、计划、故障串起来 |
| cost-privacy-budget | 成本权限预算 | 这条工作流能花多少上下文、推理和权限 |
| discovery interview | 需求访谈 | 用提问把真实需求聊清楚 |
| product review | 产品评审 | 先决定第一版该做什么、不该做什么 |
| engineering review | 工程评审 | 先决定边界、风险、验证与最小改动面 |
| investigate | 根因调查 | 修 bug 前先找到最能解释问题的原因 |
| live QA | 真实验收 | 在真实入口、真实界面、真实流程里验证 |
| stage router | 阶段路由 | 告诉你现在到底该走到哪一阶段 |
| semantic tokens | 语义令牌 | 比如 text.primary、surface.panel 这种不直接绑颜色名的令牌 |
| seed files | 起始文件 | 最先该读的文件 |
| candidate files | 候选文件 | 本任务最相关的文件 |
| context budget | 上下文预算 | 一次最多读多少文件/文本 |
| validation commands | 验证命令 | 改完后必须跑的检查 |
| triage | 初步排查 | 先快速定位问题范围 |
| artifact | 工件 | 存下来的结构化结果 |
| observability | 可观测性 | 出问题后能不能快速定位 |
| trace id | 追踪 ID | 把日志、任务、问题串起来的编号 |
| decision id | 决策 ID | 一次关键判断或分支切换的编号 |
| request id | 请求 ID | 一次请求进入系统时的编号 |
| plan id | 计划 ID | 一次执行计划的编号 |
| tool call id | 工具调用 ID | 某一次工具执行的编号 |
| regression | 回归 | 修好的东西又坏回去 |
| runtime | 运行时 | 这套系统真正执行任务时的状态 |

## 记忆方式

- 不要背定义，先记用途
- 每次只学 2 到 3 个词
- 把词和你自己的 bug、任务、项目对应起来

推荐的理解顺序是：

- 先会说中文
- 再知道英文别名
- 最后再把它和实际动作绑死

你真正要会的不是“翻译”，而是：

- 看到 `task-packet` 就知道要先收范围
- 看到 `debug-pack` 就知道要先找证据
- 看到 `eval-case` 就知道要防回归
- 看到 `requirement-brief` 就知道要先把想法落稳
- 看到 `doc-sync` 就知道要检查 README 是否已经过期
- 看到 `design-token-pack` 就知道 UI 不能再靠感觉往外长
