# Documentation Sync Pack | 文档同步包: Stage router refresh 阶段路由升级

- Sync ID | 同步 ID: `stage-router-refresh-阶段路由升级`
- Generated | 生成时间: `2026-03-20T17:05:23+00:00`
- README Strategy | README 策略: `full-rewrite`

## Change Summary | 变更摘要

Added stage router, review playbooks, investigate discipline, live QA guidance, and documentation sync.

## Changed Files | 变更文件

- `src/aidrp/cli.py`
- `docs/playbooks/stage-router-阶段路由.md`
- `README.md`

## Change Notes | 变更备注

- README must be reviewed from a whole-system perspective.

## Categories | 变化类别

- `canonical-docs`
- `runtime`
- `stage-flow`
- `workflow-surface`

## README Rewrite Scope | README 重写范围

- 这是什么
- 这版新增了什么
- 阶段路由
- 核心工件
- 文档同步原则
- 快速开始
- 默认工作流
- 仓库结构

## Impacted Docs | 受影响文档

- `README.md` [full-rewrite]: 命令表面、阶段顺序或系统定位发生了变化，README 应该按当前全貌重写。
- `ONBOARDING.md` [section-rewrite]: 默认工作顺序已经变化，入门路径需要同步。
- `AGENTS.md` [section-rewrite]: Agent 规则、优先级或禁止项已经变化，需要同步执行纪律。
- `docs/architecture-架构说明.md` [section-rewrite]: 系统层次、阶段分工或工件职责已经变化，架构说明需要重写相关部分。
- `docs/playbooks/stage-router-阶段路由.md` [section-rewrite]: 阶段流转或阶段门发生变化时，阶段路由必须同步。
- `docs/playbooks/qa-live-真实验收.md` [targeted-update]: 验收方式、真实测试路径或证据要求可能受影响。
- `docs/playbooks/documentation-sync-文档同步.md` [targeted-update]: 确认这次同步策略是否仍符合最新实践。

## Sync Order | 同步顺序

- README.md
- ONBOARDING.md
- AGENTS.md
- docs/architecture-架构说明.md
- docs/playbooks/stage-router-阶段路由.md
- docs/playbooks/documentation-sync-文档同步.md
- 相关 playbook / template / example

## Definition Of Done | 完成定义

- README 反映当前系统全貌，而不是只追加变更说明。
- 默认工作顺序在 README、ONBOARDING、AGENTS 三处保持一致。
- 新增命令、目录、模板或阶段门已经出现在对应文档里。
- 如果系统形态变了，README 已按章节重写，必要时整篇重写。
- 示例、验证命令和术语对照没有停留在旧版本。
