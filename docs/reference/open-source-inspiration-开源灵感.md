# Open-Source Inspiration | 开源灵感

这个仓库不是照抄任何一个项目，而是吸收了几个强项目里最有价值的部分。

引用方式统一遵循：

- [docs/reference/open-source-citation-开源引用规范.md](open-source-citation-开源引用规范.md)

## Aider

参考：

- [Aider](https://github.com/Aider-AI/aider)

吸收点：

- 需要有一份紧凑的 repo map，避免每次都读整个仓库

落地到本仓库：

- `repo-map | 仓库地图`
- `seed files | 起始文件`
- `candidate file ranking | 候选文件排序`

## OpenHands

参考：

- [OpenHands](https://github.com/OpenHands/OpenHands)

吸收点：

- 把运行流程、评测流程、操作流程拆开，而不是混在聊天里

落地到本仓库：

- `task-packet`
- `debug-pack`
- `eval-case`
- CI smoke check

## HyperAgent

参考：

- [HyperAgent](https://github.com/FSoft-AI4Code/HyperAgent)

吸收点：

- 软件工程 Agent 需要明确的导航、编辑、验证阶段

落地到本仓库：

- 任务包收窄阅读范围
- 排障包做故障定位
- 决策轨迹记录推理转向

## gstack

参考：

- [gstack](https://github.com/garrytan/gstack)

吸收点：

- 用阶段路由把“想法 -> 计划 -> 实现 -> 验收 -> 收尾”串起来
- 在正式开工前设置产品评审和工程评审
- 明确“没有根因调查就不要修 bug”
- 强调真实入口、真实界面的 QA，而不是只看单元测试

落地到本仓库：

- `docs/playbooks/stage-router-阶段路由.md`
- `docs/playbooks/plan-product-review-产品评审.md`
- `docs/playbooks/plan-engineering-review-工程评审.md`
- `docs/playbooks/investigate-根因调查.md`
- `docs/playbooks/qa-live-真实验收.md`

没有照搬的部分：

- 常驻浏览器 daemon
- 宿主平台强绑定
- 它特有的人设和交互语气

## Vercel AI SDK

参考：

- [AI SDK 介绍](https://ai-sdk.dev/docs/introduction)
- [Agents 概览](https://ai-sdk.dev/docs/agents/overview)
- [Loop Control](https://ai-sdk.dev/docs/agents/loop-control)

吸收点：

- Agent 运行层需要统一处理工具循环、上下文管理和停止条件
- 结构化输出、工具调用、流式 UI 和观测能力应该放在同一运行层思考
- 对复杂场景不能只依赖自由循环，需要显式的 workflow pattern

落地到本仓库：

- `tool-contract`
- `execution-plan`
- `observability-correlation`
- `cost-privacy-budget`
- [docs/reference/vercel-ai-sdk-理解与借鉴.md](vercel-ai-sdk-理解与借鉴.md)

没有照搬的部分：

- TypeScript / React / Next.js 宿主绑定
- 它自己的 UI hooks 体系
- 直接依赖某个模型或平台生态

## OpenTelemetry

参考：

- [OpenTelemetry trace-log correlation](https://opentelemetry.io/bn/docs/zero-code/obi/trace-log-correlation/)

吸收点：

- trace 和 log 一旦共享 ID，定位效率会大幅提高

落地到本仓库：

- `trace_id`
- `decision-trace`
- `observability-correlation`
- `debug-pack` 里的日志聚焦与命中证据
