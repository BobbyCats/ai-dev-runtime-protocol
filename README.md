# AI Dev Runtime Protocol（AI 开发运行协议）

一套面向真实开发现场的工作流系统，重点不是“怎么多写点 Prompt”，而是：

- 怎么减少 AI 重复读仓库
- 怎么避免改 bug 越改越偏
- 怎么把 bug 排查过程结构化
- 怎么把线上问题沉淀成回归资产
- 怎么让 Agent 变得更可观测、更可控

## 这是什么

`ai-dev-runtime-protocol` 是一套 **中文主导、术语双语** 的 AI 开发运行协议。

它不是把英文工作流原样翻成中文，而是把原来只存在于聊天窗口里的临时上下文，沉淀成一组可复用工件（artifacts）：

- `repo-map` | 仓库地图
- `requirement-brief` | 需求简报
- `task-packet` | 任务包
- `debug-pack` | 排障包
- `decision-trace` | 决策轨迹
- `eval-case` | 回归用例

核心目标只有一句话：

**不要让 Agent 每次都重新认识你的项目。**

## 中文化原则

这套协议的中文化，不是术语逐字翻译，而是按下面几条原则重写：

- 保留真正有用的机制，不照搬别人的语气和包装
- 中文负责承载实际动作，英文负责帮你逐步熟悉行业术语
- 优先写成你能直接拿来开工的话，不写翻译腔
- 同一个概念在中文里尽量只保留一个主叫法，减少脑内切换

详细说明见：

- [docs/reference/adaptation-principles-本土化改写原则.md](docs/reference/adaptation-principles-本土化改写原则.md)

## 解决什么问题

当项目稍微复杂一点之后，常见问题会变成：

- Claude / Cursor / Codex 为了改一个 bug 看完一堆相关文件
- 上下文爆炸，token 爆炸
- 任务越做越偏，最后不是在修问题，而是在重写系统
- 出 bug 只能“凭感觉排查”，没有证据链
- 线上问题修过一次，过两周又回来

这个仓库就是为了解决这些问题而设计的。

## 你会得到什么

- 一个跨平台、零第三方运行时依赖的 Python CLI
- 一套 `.aidrp/` 工作区结构
- 仓库扫描与高信号文件排序
- 需求访谈 / 需求简报 生成能力
- 任务包 / 排障包 / 回归用例 / 决策轨迹 生成能力
- JSON Schema
- 中文主导的文档、模板、手册
- 适配器（adapter）示例
- 单测和 CI

## 核心术语

| English | 中文 | 直接理解 |
| --- | --- | --- |
| repo-map | 仓库地图 | 项目结构摘要 |
| requirement-brief | 需求简报 | 把模糊想法压成简报 |
| task-packet | 任务包 | 一次任务的工作单 |
| debug-pack | 排障包 | 一次 bug 的排查资料包 |
| decision-trace | 决策轨迹 | 为什么这么改的记录 |
| eval-case | 回归用例 | 防止 bug 再犯的检查项 |

完整对照见：

- [docs/reference/terminology-glossary-术语对照.md](docs/reference/terminology-glossary-术语对照.md)

## 安装

```bash
python -m pip install -e .
```

## 快速开始

### 0. 需求还不清楚时，先做 `需求访谈（discovery interview）`

直接使用这个模板：

- [templates/discovery-interview-需求访谈.md](templates/discovery-interview-需求访谈.md)

访谈的目标不是一直追问，而是尽快收敛出 `需求简报（requirement-brief）`。

### 1. 初始化工作区

```bash
python -m aidrp init-workspace --project-root . --write-agents-template
```

### 2. 生成 `仓库地图（repo-map）`

```bash
python -m aidrp repo-map --project-root . --output-dir .aidrp
```

### 3. 用 CLI 生成 `需求简报（requirement-brief）`

```bash
python -m aidrp requirement-brief \
  --title "AI meeting helper AI 会议助手" \
  --product-idea "先通过需求访谈把问题聊清楚，再决定写不写代码 | Use a discovery interview before coding" \
  --target-user "脑子里先有感觉、但暂时说不清需求的构建者 | Builders with fuzzy first ideas" \
  --pain-point "想法太散，没法直接开写，也容易一上来做偏 | Ideas are too vague to code directly" \
  --desired-outcome "把对话收敛成一份能继续执行的结构化简报 | Turn conversation into a structured brief" \
  --scenario "先把第一阶段要不要做、做什么聊清楚 | Clarify the first milestone" \
  --non-goal "暂时不设计全系统，也不提前扩 scope | Do not design the whole system yet" \
  --constraint "第一版流程要轻，不要把前置访谈做成重文档流程 | Keep the first workflow lightweight" \
  --success-metric "这份简报可以顺利转成任务包并指导开工 | The brief can be converted into a task packet" \
  --open-question "访谈问到什么程度就该收口 | How many interview rounds are enough" \
  --assumption "中文是主工作语言，英文术语作为辅助记忆 | Chinese-first wording is preferred"
```

### 4. 开工前再生成 `任务包（task-packet）`

```bash
python -m aidrp task-packet \
  --project-root . \
  --title "Fix schedule deletion drift 修复日程删除漂移" \
  --objective "只修删除路径，不顺手扩成一次大重构 | Fix the deletion path without broadening scope" \
  --type bugfix \
  --scope "只改删除流程和相关测试，不碰无关调度逻辑 | Only touch deletion flow and its tests" \
  --acceptance "删除动作必须命中正确事件，且不会误删其他记录 | Deletion uses the correct event identity" \
  --constraint "不要借这个 bug 顺手重写整段日程逻辑 | Do not rewrite unrelated scheduling logic" \
  --search-term delete \
  --search-term schedule
```

### 5. 修 bug 前先生成 `排障包（debug-pack）`

```bash
python -m aidrp debug-pack \
  --project-root . \
  --title "Schedule deletion bug 日程删除错误" \
  --symptom "删一个事件，结果被删掉的是另一个条目 | Deleting one event removes the wrong item" \
  --observed "界面显示删除成功，但消失的是错误那一行 | UI reports success but the wrong row disappears" \
  --expected "只能删除用户点中的那条事件 | Only the targeted event should be deleted" \
  --impact "这种错误会直接破坏用户对日程数据的信任 | Users lose trust in scheduling data" \
  --trace-id trace-2026-03-18-001 \
  --repro-step "打开日程页 | Open the schedule page" \
  --repro-step "删除第二条记录 | Delete the second item" \
  --repro-step "观察消失的是否是错误对象 | Observe the wrong row disappears" \
  --suspected-file src/schedule/delete.py \
  --search-term delete \
  --search-term event
```

### 6. 记录 `决策轨迹（decision-trace）`

```bash
python -m aidrp trace-start --title "Fix schedule deletion drift 修复日程删除漂移" --task-id fix-schedule-deletion-drift-修复日程删除漂移
python -m aidrp trace-event \
  --trace-file .aidrp/traces/fix-schedule-deletion-drift-修复日程删除漂移.json \
  --stage investigate \
  --summary "已确认删除处理器里用了错误的身份标识，对应不上目标事件 | Confirmed identity mismatch in delete handler" \
  --file src/schedule/delete.py \
  --command "python -m unittest" \
  --outcome "需要定点修复，不需要扩大改动面 | Need targeted patch"
```

### 7. 修完后生成 `回归用例（eval-case）`

```bash
python -m aidrp eval-case \
  --title "Regression for schedule deletion drift 日程删除漂移回归用例" \
  --origin "debug-pack:schedule-deletion-bug-日程删除错误" \
  --command "python -m unittest" \
  --repro-step "删除日程列表里的第二项 | Delete the second item in the schedule list" \
  --assertion "只能删掉目标事件，其他记录必须保持不变 | Only the targeted event is removed" \
  --tag bugfix \
  --tag schedule
```

## 推荐工作流

1. 初始化 `.aidrp/`
2. 提交一份仓库地图
3. 想法模糊时先做需求访谈并落成需求简报
4. 非 trivial 任务先写任务包
5. bug 先写排障包
6. 判断转向时补决策轨迹
7. 修复真实 bug 后补回归用例

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
- [docs/playbooks/discovery-interview-需求访谈.md](docs/playbooks/discovery-interview-需求访谈.md)
- [docs/playbooks/bugfix-缺陷修复.md](docs/playbooks/bugfix-缺陷修复.md)
- [docs/playbooks/feature-功能开发.md](docs/playbooks/feature-功能开发.md)
- [docs/reference/open-source-inspiration-开源灵感.md](docs/reference/open-source-inspiration-开源灵感.md)

## 吸收了哪些项目的优点

- [Aider](https://github.com/Aider-AI/aider)
- [OpenHands](https://github.com/OpenHands/OpenHands)
- [HyperAgent](https://github.com/FSoft-AI4Code/HyperAgent)
- [OpenTelemetry trace-log correlation](https://opentelemetry.io/bn/docs/zero-code/obi/trace-log-correlation/)

对应关系见：

- [docs/reference/open-source-inspiration-开源灵感.md](docs/reference/open-source-inspiration-开源灵感.md)

## 这套系统的定位

它不是：

- 单纯 Prompt 模板库
- 只会写 `AGENTS.md` 的规则包
- 某一个模型专用的 workflow

它更像：

- 需求澄清层
- AI 开发运行时协议
- Agent 的上下文压缩层
- bug 排查与回归沉淀层

## 当前状态

这是第一版可用骨架，优先解决的是：

- 结构清楚
- 文档清楚
- 命令能跑
- 工件能生成
- 后续容易继续打磨

## License

MIT
