# 术语对照（Terminology Glossary）

这份表不是给你背单词用的，而是帮你把术语和实际动作一一对应起来。

| English | 中文主叫法 | 你可以直接理解成 |
| --- | --- | --- |
| repo-map | 仓库地图 | 这个项目的结构摘要 |
| requirement-brief | 需求简报 | 把模糊想法收敛后的简报 |
| task-packet | 任务包 | 一次任务的工作单 |
| debug-pack | 排障包 | 一次 bug 的排查资料包 |
| decision-trace | 决策轨迹 | 为什么这么改的记录 |
| eval-case | 回归用例 | 为了防止 bug 再犯的检查项 |
| discovery interview | 需求访谈 | 用提问把真实需求聊清楚 |
| seed files | 起始文件 | 最先该读的文件 |
| candidate files | 候选文件 | 本任务最相关的文件 |
| context budget | 上下文预算 | 一次最多读多少文件/文本 |
| validation commands | 验证命令 | 改完后必须跑的检查 |
| triage | 初步排查 | 先快速定位问题范围 |
| artifact | 工件 | 存下来的结构化结果 |
| observability | 可观测性 | 出问题后能不能快速定位 |
| trace id | 追踪 ID | 把日志、任务、问题串起来的编号 |
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
