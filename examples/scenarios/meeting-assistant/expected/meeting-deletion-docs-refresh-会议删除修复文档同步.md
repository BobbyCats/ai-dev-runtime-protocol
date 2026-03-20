# Documentation Sync Pack | 文档同步包: Meeting deletion docs refresh 会议删除修复文档同步

- Sync ID | 同步 ID: `meeting-deletion-docs-refresh-会议删除修复文档同步`
- Generated | 生成时间: `2026-03-20T18:50:32+00:00`
- README Strategy | README 策略: `targeted-update`

## Change Summary | 变更摘要

删除链路已经改成稳定 meeting_id，相关 walkthrough、示例和 README 索引都需要同步。

## Changed Files | 变更文件

- `src/calendar_agent.py`
- `src/event_store.py`
- `docs/tutorials/e2e-walkthrough-端到端教程.md`

## Change Notes | 变更备注

- 不要只补一句，先检查 README 的工作流表达是否仍然准确。

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

- `README.md` [targeted-update]: 需要确认 README 的快速开始、命令或定位描述仍然准确。
- `ONBOARDING.md` [targeted-update]: 确认默认执行顺序和当前工件一致。
- `AGENTS.md` [targeted-update]: 确认 Agent 仍遵守当前工作边界。
- `docs/architecture-架构说明.md` [targeted-update]: 确认架构说明仍能解释当前结构。
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
