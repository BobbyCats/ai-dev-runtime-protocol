# AI Dev Runtime Protocol（AI 开发运行协议）

这不是一个“多写几条 Prompt”的仓库，而是一套让 AI Agent 按阶段工作、按工件交付、按证据排障的开发运行协议。

它主要解决这些问题：

- 改一个 bug 就全仓扫描
- token 和上下文持续膨胀
- 任务做到一半开始偏航
- UI 风格越写越漂
- 排障没有根因解释，只能靠猜
- 真实用户路径没人验
- 代码已经变了，README 还停在过去时

核心目标只有一句话：

**不要让 Agent 每次都重新认识你的项目，也不要让文档永远落后于代码。**

## 一句话理解

如果你经常遇到这些场景：

- 新会话一开就要重新解释整个项目
- 改一个 bug 要扫十几二十个文件
- AI 明明写了代码，但 README、示例和测试还停在旧版本

这个仓库就是拿来解决这些问题的。

## 先看哪里

如果你第一次接触这个仓库，建议直接从这里开始：

- [完整使用手册](docs/guides/usage-guide-完整使用手册.md)
- [端到端教程](docs/tutorials/e2e-walkthrough-端到端教程.md)
- [CLI 参考](docs/reference/cli-reference-CLI参考.md)
- [架构说明](docs/architecture-架构说明.md)
- [阶段路由](docs/playbooks/stage-router-阶段路由.md)
- [Vercel AI SDK 理解与借鉴](docs/reference/vercel-ai-sdk-理解与借鉴.md)
- [示例目录](examples/README.md)

## 入口导航

- 想完整跑一遍：
  [端到端教程](docs/tutorials/e2e-walkthrough-端到端教程.md)
- 想按命令查：
  [CLI 参考](docs/reference/cli-reference-CLI参考.md)
- 想按场景选流程：
  [完整使用手册里的场景路线](docs/guides/usage-guide-完整使用手册.md#你到底该怎么用)
- 想先看一个真实样例工作区：
  [meeting-assistant 场景](examples/scenarios/meeting-assistant/README.md)

## 这套系统包含什么

### 阶段层

- `需求访谈 | discovery interview`
- `产品评审 | product review`
- `设计令牌体系 | design token system`
- `工程评审 | engineering review`
- `根因调查 | investigate`
- `真实验收 | live QA`
- `文档同步 | documentation sync`

### 工件层

- `repo-map | 仓库地图`
- `requirement-brief | 需求简报`
- `design-token-pack | 设计令牌包`
- `task-packet | 任务包`
- `debug-pack | 排障包`
- `decision-trace | 决策轨迹`
- `eval-case | 回归用例`
- `doc-sync | 文档同步包`
- `domain-map | 领域地图`
- `tool-contract | 工具契约`
- `execution-plan | 执行计划`
- `observability-correlation | 可观测性关联`
- `cost-privacy-budget | 成本权限预算`

## 默认工作流

功能开发默认走：

1. 需求访谈
2. 需求简报
3. 产品评审
4. 设计令牌包（UI 任务时）
5. 工程评审
6. 仓库地图
7. 任务包
8. 实现
9. 真实验收
10. 文档同步

缺陷修复默认走：

1. 仓库地图
2. 排障包
3. 可观测性关联
4. 根因调查
5. 定点修复
6. 真实验收
7. 回归用例
8. 文档同步

更详细的流程、场景、建议和示范，见：

- [完整使用手册](docs/guides/usage-guide-完整使用手册.md)
- [端到端教程](docs/tutorials/e2e-walkthrough-端到端教程.md)

## CLI 命令总览

```bash
python -m aidrp --help
```

当前支持：

- `init-workspace`
- `repo-map`
- `requirement-brief`
- `domain-map`
- `tool-contract`
- `execution-plan`
- `task-packet`
- `debug-pack`
- `eval-case`
- `design-token-pack`
- `observability-correlation`
- `cost-privacy-budget`
- `doc-sync`
- `trace-start`
- `trace-event`

按阶段组织的命令说明见：

- [CLI 参考](docs/reference/cli-reference-CLI参考.md)

## 安装

```bash
python -m pip install -e .
```

## 快速开始

```bash
python -m aidrp init-workspace --project-root . --write-agents-template
python -m aidrp repo-map --project-root . --output-dir .aidrp
python -m aidrp requirement-brief \
  --title "First idea 第一个想法" \
  --product-idea "Use AI to narrow fuzzy work into executable tasks." \
  --target-user "Builders who think before they can fully specify." \
  --pain-point "Ideas are vague and easy to overbuild too early." \
  --desired-outcome "Turn a fuzzy idea into a scoped brief."
```

如果你是从模糊想法开始，不要跳过：

- [需求访谈](templates/discovery-interview-需求访谈.md)
- [需求简报](templates/requirement-brief-需求简报.md)

如果你想直接拿一个样例仓库练手：

- [端到端教程](docs/tutorials/e2e-walkthrough-端到端教程.md)
- [meeting-assistant 场景目录](examples/scenarios/meeting-assistant/README.md)

## 推荐文档地图

### 入门

- [ONBOARDING.md](ONBOARDING.md)
- [AGENTS.md](AGENTS.md)
- [完整使用手册](docs/guides/usage-guide-完整使用手册.md)
- [端到端教程](docs/tutorials/e2e-walkthrough-端到端教程.md)
- [CLI 参考](docs/reference/cli-reference-CLI参考.md)

### 方法与架构

- [架构说明](docs/architecture-架构说明.md)
- [阶段路由](docs/playbooks/stage-router-阶段路由.md)
- [Vercel AI SDK 理解与借鉴](docs/reference/vercel-ai-sdk-理解与借鉴.md)
- [开源灵感](docs/reference/open-source-inspiration-开源灵感.md)

### 关键 playbook

- [产品评审](docs/playbooks/plan-product-review-产品评审.md)
- [工程评审](docs/playbooks/plan-engineering-review-工程评审.md)
- [根因调查](docs/playbooks/investigate-根因调查.md)
- [真实验收](docs/playbooks/qa-live-真实验收.md)
- [可观测性关联](docs/playbooks/observability-correlation-可观测性关联.md)
- [文档同步](docs/playbooks/documentation-sync-文档同步.md)

### 参考

- [术语对照](docs/reference/terminology-glossary-术语对照.md)
- [本土化改写原则](docs/reference/adaptation-principles-本土化改写原则.md)
- [开源引用规范](docs/reference/open-source-citation-开源引用规范.md)

## 这套系统的定位

它不是：

- 单纯 Prompt 模板库
- 某一个模型专用的 workflow
- 只管写代码、不管验证与文档的半流程系统

它更像：

- 需求澄清层
- 阶段路由层
- Agent 的上下文压缩层
- 运行时边界定义层
- 根因调查与真实验收层
- 回归与文档同步守门层

## License

MIT
