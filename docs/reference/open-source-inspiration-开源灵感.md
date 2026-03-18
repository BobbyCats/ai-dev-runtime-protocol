# Open-Source Inspiration | 开源灵感

这个仓库不是照抄任何一个项目，而是吸收了几个强项目里最有价值的部分。

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

## OpenTelemetry

参考：

- [OpenTelemetry trace-log correlation](https://opentelemetry.io/bn/docs/zero-code/obi/trace-log-correlation/)

吸收点：

- trace 和 log 一旦共享 ID，定位效率会大幅提高

落地到本仓库：

- `trace_id`
- `decision-trace`
- 排障包里的证据链
