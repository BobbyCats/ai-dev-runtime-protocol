# AI Dev Runtime Protocol（AI 开发运行协议）

一套面向真实开发现场的工作流系统，重点不是“怎么多写点 Prompt”，而是：

- 怎么减少 AI 重复读仓库
- 怎么避免改 bug 越改越偏
- 怎么把 bug 排查过程结构化
- 怎么把线上问题沉淀成回归资产
- 怎么让 Agent 变得更可观测、更可控

## 这是什么

`ai-dev-runtime-protocol` 是一套 **中文主导、术语双语** 的 AI 开发运行协议。

它把原来只存在于聊天窗口里的临时上下文，沉淀成一组可复用工件（artifacts）：

- `repo-map` | 仓库地图
- `task-packet` | 任务包
- `debug-pack` | 排障包
- `decision-trace` | 决策轨迹
- `eval-case` | 回归用例

核心目标只有一句话：

**不要让 Agent 每次都重新认识你的项目。**

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
- 任务包 / 排障包 / 回归用例 / 决策轨迹 生成能力
- JSON Schema
- 中文主导的文档、模板、手册
- 适配器（adapter）示例
- 单测和 CI

## 核心术语

| English | 中文 | 直接理解 |
| --- | --- | --- |
| repo-map | 仓库地图 | 项目结构摘要 |
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

### 1. 初始化工作区

```bash
python -m aidrp init-workspace --project-root . --write-agents-template
```

### 2. 生成 `repo-map | 仓库地图`

```bash
python -m aidrp repo-map --project-root . --output-dir .aidrp
```

### 3. 开工前先生成 `task-packet | 任务包`

```bash
python -m aidrp task-packet \
  --project-root . \
  --title "Fix schedule deletion drift 修复日程删除漂移" \
  --objective "Fix the deletion path without broadening scope. 修复删除路径，但不要扩大范围。" \
  --type bugfix \
  --scope "Only touch deletion flow and its tests. 只改删除流程和相关测试。" \
  --acceptance "Deletion uses the correct event identity. 删除必须命中正确事件。" \
  --constraint "Do not rewrite unrelated scheduling logic. 不要改无关排程逻辑。" \
  --search-term delete \
  --search-term schedule
```

### 4. 修 bug 前先生成 `debug-pack | 排障包`

```bash
python -m aidrp debug-pack \
  --project-root . \
  --title "Schedule deletion bug 日程删除错误" \
  --symptom "Deleting one event removes the wrong item 删除一个事件却删掉了错误条目" \
  --observed "UI reports success but the wrong row disappears UI 显示成功，但删错了行" \
  --expected "Only the targeted event should be deleted 只能删除目标事件" \
  --impact "Users lose trust in scheduling data 用户会失去对日程数据的信任" \
  --trace-id trace-2026-03-18-001 \
  --repro-step "Open the schedule page 打开日程页" \
  --repro-step "Delete the second item 删除第二条" \
  --repro-step "Observe the wrong row disappears 观察删错对象" \
  --suspected-file src/schedule/delete.py \
  --search-term delete \
  --search-term event
```

### 5. 记录 `decision-trace | 决策轨迹`

```bash
python -m aidrp trace-start --title "Fix schedule deletion drift 修复日程删除漂移" --task-id fix-schedule-deletion-drift-修复日程删除漂移
python -m aidrp trace-event \
  --trace-file .aidrp/traces/fix-schedule-deletion-drift-修复日程删除漂移.json \
  --stage investigate \
  --summary "Confirmed identity mismatch in delete handler. 已确认删除处理器存在身份标识错配。" \
  --file src/schedule/delete.py \
  --command "python -m unittest" \
  --outcome "Need targeted patch 需要定点修复"
```

### 6. 修完后生成 `eval-case | 回归用例`

```bash
python -m aidrp eval-case \
  --title "Regression for schedule deletion drift 日程删除漂移回归用例" \
  --origin "debug-pack:schedule-deletion-bug-日程删除错误" \
  --command "python -m unittest" \
  --repro-step "Delete the second item in the schedule list 删除列表第二项" \
  --assertion "Only the targeted event is removed 只能删掉目标事件" \
  --tag bugfix \
  --tag schedule
```

## 推荐工作流

1. 初始化 `.aidrp/`
2. 提交一份仓库地图
3. 非 trivial 任务先写任务包
4. bug 先写排障包
5. 判断转向时补决策轨迹
6. 修复真实 bug 后补回归用例

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
