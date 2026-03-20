# Onboarding | 入门说明

这个仓库不是教你“怎么写更花哨的 Prompt”，而是教你：

怎么把 AI 开发从聊天模式，升级成一个有阶段门、有工件、有验收、有文档守门的运行模式。

## 核心转变

从：

- “你先读一下仓库，然后帮我改”

转成：

- “你先按阶段工作，先读工件，只有证据不足时才扩大上下文”

再往前一步，现在还要做到：

- “代码改完以后，必须确认 README 和核心文档是否还是当前事实”

## 默认工作模型

功能开发默认顺序：

1. 初始化 `.aidrp/`
2. 想法不清楚时，先做 `需求访谈（discovery interview）`
3. 落成 `需求简报（requirement-brief）`
4. 过 `产品评审（product review）`
5. UI / 多端任务先补 `设计令牌包（design-token-pack）`
6. 过 `工程评审（engineering review）`
7. 生成 `仓库地图（repo-map）`
8. 生成 `任务包（task-packet）`
9. 按短名单实现，不要直接全仓扫描
10. 做 `真实验收（live QA）`
11. 用 `文档同步包（doc-sync）` 收尾

Bug 修复默认顺序：

1. 生成或刷新 `仓库地图（repo-map）`
2. 生成 `排障包（debug-pack）`
3. 先做 `可观测性关联（observability-correlation）`
4. 再做 `根因调查（investigate）`
5. 必要时记录 `决策轨迹（decision-trace）`
6. 定点修复
7. 做 `真实验收（live QA）`
8. 把 bug 变成 `回归用例（eval-case）`
9. 用 `文档同步包（doc-sync）` 收尾

## 这套系统试图防止的坏味道

- 一个本地 bug 却要扫整个仓库
- 每次新会话都重新讲架构
- 需求还没收敛就直接设计系统
- 界面刚开始写就漂，越写越像几个产品拼在一起
- 没有根因调查就开始修 bug
- 只跑了单元测试，就宣布已经验证完成
- 代码和 README 慢慢分叉，最后互相误导

## 必备工件

- `.aidrp/repo-map.json`
- `.aidrp/repo-map.md`
- `.aidrp/briefs/*.json` 与 `*.md`
- `.aidrp/tasks/*.json` 与 `*.md`
- `.aidrp/debug/*.json` 与 `*.md`
- `.aidrp/traces/*.json`
- `.aidrp/evals/*.json` 与 `*.md`
- `.aidrp/docsync/*.json` 与 `*.md`
- `.aidrp/domains/*.json` 与 `*.md`
- `.aidrp/contracts/*.json` 与 `*.md`
- `.aidrp/plans/*.json` 与 `*.md`
- `.aidrp/correlations/*.json` 与 `*.md`
- `.aidrp/budgets/*.json` 与 `*.md`

## 集成到其他项目的步骤

1. 安装这个包，或者把核心文件复制过去
2. 运行 `python -m aidrp init-workspace --project-root /path/to/project`
3. 修改 `.aidrp/config.json`
4. 提交 `.aidrpignore`、配置文件和生成后的 `AGENTS.md`
5. 把 `任务包 / 排障包 / 文档同步包` 加入你的日常流程
6. 把真实验收和回归用例纳入默认收尾
7. 把中文提交规范与开源引用规范纳入日常协作

## 如果你现在只能先落四件事

- 固定提交 `仓库地图（repo-map）`
- 想法没收敛前先写 `需求简报（requirement-brief）`
- 前端或多端任务先补 `设计令牌包（design-token-pack）`
- 修 bug 前必须先写 `排障包（debug-pack）`，并先做根因调查
- 非 trivial 变更收尾前必须补 `文档同步包（doc-sync）`

## 协作补充规则

- bug 排查先按 `trace_id / decision_id / request_id / plan_id / tool_call_id` 查日志和证据，再决定是否扩大代码扫描
- 提交信息默认使用中文，并按 [docs/playbooks/git-commit-提交规范.md](docs/playbooks/git-commit-提交规范.md) 编写
- 吸收外部开源项目思路时，按 [docs/reference/open-source-citation-开源引用规范.md](docs/reference/open-source-citation-开源引用规范.md) 记录来源、吸收点与落地位置
