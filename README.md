# AI Dev Runtime Protocol（AI 开发运行协议）

这不是一个“多写几条 Prompt”的仓库，而是一套把 AI 开发从聊天模式拉回工程模式的协议。

它重点解决 7 个高频问题：

- 为了改一个 bug 反复全仓扫描
- 上下文和 token 成本失控
- 任务做到一半不断偏航
- UI 越写越漂，不同页面像不同产品拼在一起
- 修 bug 没有根因调查，越修越像猜
- 单元测试过了，但真实流程根本没验收
- 代码已经变了，README 还停在过去时

## 这是什么

`ai-dev-runtime-protocol` 是一套 **中文主导、术语双语、阶段清晰** 的 AI 开发运行协议。

它把原本散落在聊天窗口里的临时上下文，收敛成一组真正可复用的工件（artifacts）和阶段门（stage gates）：

- `repo-map` | 仓库地图
- `requirement-brief` | 需求简报
- `design-token-pack` | 设计令牌包
- `task-packet` | 任务包
- `debug-pack` | 排障包
- `decision-trace` | 决策轨迹
- `eval-case` | 回归用例
- `doc-sync` | 文档同步包

核心目标只有一句话：

**不要让 Agent 每次都重新认识你的项目，也不要让文档永远落后于代码。**

## 这版新增了什么

这次把原来偏“执行工件”的仓库，升级成了带阶段路由的完整流程：

- 引入 `阶段路由（stage router）`
- 引入 `产品评审（product review）`
- 引入 `设计令牌体系（design token system）`
- 引入 `工程评审（engineering review）`
- 引入 `根因调查（investigate）`
- 引入 `真实验收（live QA）`
- 引入 `文档同步包（doc-sync）`

也就是说，这套协议现在不只管“怎么执行”，还开始管：

- 什么时候该收需求
- 什么时候该砍 scope
- 什么时候该先把视觉语言结构化，而不是让 AI 凭感觉生成新界面
- 什么时候先查根因，不能直接修
- 什么时候必须去真实环境验收
- 什么时候 README 应该整篇重写，而不是只补一条

## 中文化原则

这套协议的中文化，不是逐字翻译，而是把方法论重写成你真正能拿来开工的中文工作语言。

- 保留真正有用的机制，不照搬别人的语气和包装
- 中文负责承载动作，英文负责帮助你逐步熟悉术语
- 优先写成你能直接执行的话，不写翻译腔
- 同一个概念在中文里尽量只保留一个主叫法

详细说明见：

- [docs/reference/adaptation-principles-本土化改写原则.md](docs/reference/adaptation-principles-本土化改写原则.md)

## 阶段路由

这套系统现在的默认路线不是“读仓库 -> 写代码”，而是下面这条：

| 阶段 | 解决的问题 | 主要输出 |
| --- | --- | --- |
| 需求访谈 | 你到底想解决什么问题 | `requirement-brief` |
| 产品评审 | 第一版该做什么，不该做什么 | 产品评审结论 |
| 设计令牌包（可选） | UI 任务先统一视觉语言，避免 AI 随机出风格 | `design-token-pack` |
| 工程评审 | 最小改动面、边界、风险、验证怎么定 | 工程评审结论 |
| 仓库地图 | 先压缩项目上下文 | `repo-map` |
| 任务包 / 排障包 | 把一次工作限制在清晰范围内 | `task-packet` / `debug-pack` |
| 根因调查 | 先找到解释问题的最小原因 | 更新后的 `debug-pack` + `decision-trace` |
| 实现 | 在受控范围内改代码 | 代码 + 测试 |
| 真实验收 | 在真实界面/真实入口验证 | QA 记录 |
| 回归与文档同步 | 防回归、防文档漂移 | `eval-case` + `doc-sync` |

完整说明见：

- [docs/playbooks/stage-router-阶段路由.md](docs/playbooks/stage-router-阶段路由.md)

## 核心工件

| English | 中文主叫法 | 用途 |
| --- | --- | --- |
| repo-map | 仓库地图 | 项目结构摘要与高信号入口 |
| requirement-brief | 需求简报 | 把模糊想法压成可以继续推进的简报 |
| design-token-pack | 设计令牌包 | 把品牌方向、语义色、尺寸、字体系成前端可执行约束，并输出可视化 HTML 预览 |
| task-packet | 任务包 | 一次功能任务的工作单、范围和验证清单 |
| debug-pack | 排障包 | 一次 bug 的证据包和排查短名单 |
| decision-trace | 决策轨迹 | 推理转向、关键判断和权衡记录 |
| eval-case | 回归用例 | 把真实 bug 变成可重复验证的资产 |
| doc-sync | 文档同步包 | 判断 README 和核心文档该补丁更新还是整篇重写 |

完整术语对照见：

- [docs/reference/terminology-glossary-术语对照.md](docs/reference/terminology-glossary-术语对照.md)

## 文档同步原则

这个仓库现在明确反对一种常见坏习惯：

**代码改完以后，只往 README 底部追加一条说明。**

README 在这里不是 changelog，也不是想到什么写什么，而是“当前系统全貌图”。

所以现在的规则是：

- 任何非 trivial 改动，收尾前都要跑一次 `doc-sync | 文档同步包`
- README 优先于其他文档更新
- 如果命令表面、阶段顺序、系统定位或目录结构变了，README 应该按章节重写
- 如果核心工作流都变了，README 应该整篇重写

对应手册见：

- [docs/playbooks/documentation-sync-文档同步.md](docs/playbooks/documentation-sync-文档同步.md)

## 安装

```bash
python -m pip install -e .
```

## 快速开始

### 0. 需求还不清楚时，先做 `需求访谈（discovery interview）`

- 模板：[templates/discovery-interview-需求访谈.md](templates/discovery-interview-需求访谈.md)
- 手册：[docs/playbooks/discovery-interview-需求访谈.md](docs/playbooks/discovery-interview-需求访谈.md)

### 1. 初始化工作区

```bash
python -m aidrp init-workspace --project-root . --write-agents-template
```

### 2. 生成 `仓库地图（repo-map）`

```bash
python -m aidrp repo-map --project-root . --output-dir .aidrp
```

### 3. 生成 `需求简报（requirement-brief）`

```bash
python -m aidrp requirement-brief \
  --title "AI meeting helper AI 会议助手" \
  --product-idea "先通过需求访谈把问题聊清楚，再决定写不写代码 | Use a discovery interview before coding" \
  --target-user "脑子里先有感觉、但暂时说不清需求的构建者 | Builders with fuzzy first ideas" \
  --pain-point "想法太散，没法直接开写，也容易一上来做偏 | Ideas are too vague to code directly" \
  --desired-outcome "把对话收敛成一份能继续执行的结构化简报 | Turn conversation into a structured brief"
```

### 4. 进入评审层

- 产品评审手册：[docs/playbooks/plan-product-review-产品评审.md](docs/playbooks/plan-product-review-产品评审.md)
- 设计令牌手册：[docs/playbooks/design-token-system-设计令牌体系.md](docs/playbooks/design-token-system-设计令牌体系.md)
- 工程评审手册：[docs/playbooks/plan-engineering-review-工程评审.md](docs/playbooks/plan-engineering-review-工程评审.md)

如果这次任务包含新界面、主题系统、组件库或多端 UI，先补 `设计令牌包（design-token-pack）`：

```bash
python -m aidrp design-token-pack \
  --title "AI schedule UI 日程助手界面" \
  --surface "Conversation-first scheduling and expense assistant 对话优先的日程与费用助手" \
  --brand-direction "Calm productivity with strong structure and low visual noise. 冷静、高效、结构感强、低噪音。" \
  --brand-color "#0F766E" \
  --accent-color "#F59E0B" \
  --design-principle "先定义语义令牌，再写组件，不要在组件里直接写死颜色。" \
  --guardrail "组件代码里不要直接写十六进制颜色。"
```

默认会生成三份产物：

- `design-system/ai-schedule-ui-日程助手界面.json`
- `design-system/ai-schedule-ui-日程助手界面.md`
- `design-system/ai-schedule-ui-日程助手界面.html`

其中 `.html` 是可直接打开的视觉预览页，用来快速检查色板、语义令牌和示例界面气质有没有跑偏。

### 5. 进入执行层

功能任务生成 `任务包（task-packet）`：

```bash
python -m aidrp task-packet \
  --project-root . \
  --title "Fix schedule deletion drift 修复日程删除漂移" \
  --objective "只修删除路径，不顺手扩成一次大重构 | Fix the deletion path without broadening scope" \
  --type bugfix \
  --scope "只改删除流程和相关测试，不碰无关调度逻辑 | Only touch deletion flow and its tests" \
  --acceptance "删除动作必须命中正确事件，且不会误删其他记录 | Deletion uses the correct event identity"
```

Bug 任务先生成 `排障包（debug-pack）`：

```bash
python -m aidrp debug-pack \
  --project-root . \
  --title "Schedule deletion bug 日程删除错误" \
  --symptom "删一个事件，结果被删掉的是另一个条目 | Deleting one event removes the wrong item" \
  --observed "界面显示删除成功，但消失的是错误那一行 | UI reports success but the wrong row disappears" \
  --expected "只能删除用户点中的那条事件 | Only the targeted event should be deleted"
```

### 6. 记录 `决策轨迹（decision-trace）`

```bash
python -m aidrp trace-start --title "Fix schedule deletion drift 修复日程删除漂移" --task-id fix-schedule-deletion-drift-修复日程删除漂移
python -m aidrp trace-event \
  --trace-file .aidrp/traces/fix-schedule-deletion-drift-修复日程删除漂移.json \
  --stage investigate \
  --summary "已确认删除处理器里用了错误的身份标识，对应不上目标事件 | Confirmed identity mismatch in delete handler"
```

### 7. 修完后补 `回归用例（eval-case）`

```bash
python -m aidrp eval-case \
  --title "Regression for schedule deletion drift 日程删除漂移回归用例" \
  --origin "debug-pack:schedule-deletion-bug-日程删除错误" \
  --command "python -m unittest" \
  --repro-step "删除日程列表里的第二项 | Delete the second item in the schedule list" \
  --assertion "只能删掉目标事件，其他记录必须保持不变 | Only the targeted event is removed"
```

### 8. 收尾前补 `文档同步包（doc-sync）`

```bash
python -m aidrp doc-sync \
  --project-root . \
  --title "Stage router refresh 阶段路由升级" \
  --summary "Added stage router, review playbooks, investigate discipline, and live QA guidance." \
  --changed-file src/aidrp/cli.py \
  --changed-file docs/playbooks/stage-router-阶段路由.md \
  --change-note "README 需要按全局视角检查，不允许只追加补丁说明。"
```

## 默认工作流

功能开发默认走这条：

1. 需求访谈
2. 需求简报
3. 产品评审
4. UI 任务先补设计令牌包
5. 工程评审
6. 仓库地图
7. 任务包
8. 实现
9. 真实验收
10. 文档同步

Bug 修复默认走这条：

1. 仓库地图
2. 排障包
3. 根因调查
4. 定点修复
5. 真实验收
6. 回归用例
7. 文档同步

## 仓库结构

```text
.
├── AGENTS.md
├── ONBOARDING.md
├── adapters/
├── docs/
├── examples/
├── schemas/
├── src/aidrp/
├── templates/
└── tests/
```

## 先看哪些文件

- [ONBOARDING.md](ONBOARDING.md)
- [AGENTS.md](AGENTS.md)
- [docs/architecture-架构说明.md](docs/architecture-架构说明.md)
- [docs/playbooks/stage-router-阶段路由.md](docs/playbooks/stage-router-阶段路由.md)
- [docs/playbooks/plan-product-review-产品评审.md](docs/playbooks/plan-product-review-产品评审.md)
- [docs/playbooks/design-token-system-设计令牌体系.md](docs/playbooks/design-token-system-设计令牌体系.md)
- [docs/playbooks/plan-engineering-review-工程评审.md](docs/playbooks/plan-engineering-review-工程评审.md)
- [docs/playbooks/investigate-根因调查.md](docs/playbooks/investigate-根因调查.md)
- [docs/playbooks/qa-live-真实验收.md](docs/playbooks/qa-live-真实验收.md)
- [docs/playbooks/documentation-sync-文档同步.md](docs/playbooks/documentation-sync-文档同步.md)
- [docs/reference/open-source-inspiration-开源灵感.md](docs/reference/open-source-inspiration-开源灵感.md)

## 吸收了哪些项目的优点

- [Aider](https://github.com/Aider-AI/aider)
- [OpenHands](https://github.com/OpenHands/OpenHands)
- [HyperAgent](https://github.com/FSoft-AI4Code/HyperAgent)
- [gstack](https://github.com/garrytan/gstack)
- [OpenTelemetry trace-log correlation](https://opentelemetry.io/bn/docs/zero-code/obi/trace-log-correlation/)

对应关系见：

- [docs/reference/open-source-inspiration-开源灵感.md](docs/reference/open-source-inspiration-开源灵感.md)

## 这套系统的定位

它不是：

- 单纯 Prompt 模板库
- 只会写 `AGENTS.md` 的规则包
- 某一个模型专用的 workflow
- 只管写代码、不管验证和文档的半流程系统

它更像：

- 需求澄清层
- 阶段路由层
- Agent 的上下文压缩层
- 根因调查与真实验收层
- 回归与文档同步守门层

## License

MIT
