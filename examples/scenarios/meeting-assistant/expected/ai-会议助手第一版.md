# Requirement Brief | 需求简报: AI 会议助手第一版

- Brief ID | 简报 ID: `ai-会议助手第一版`
- Generated | 生成时间: `2026-03-20T18:50:32+00:00`

## Product Idea | 产品想法

把模糊会议安排需求收敛成结构化计划，再交给用户确认和执行。

## Target Users | 目标用户

- 高频安排评审会和同步会的团队负责人

## Pain Points | 痛点

- 会议安排总在聊天里反复改，最后没人能准确回答到底定在哪个时间

## Desired Outcomes | 期望结果

- 先得到一份范围稳定的第一版简报

## Core Scenarios | 核心场景

- 通过聊天创建、改期和删除会议
- 在删除前给出可确认的计划

## Non-Goals | 不做什么

- 第一版不做外部日历双向同步

## Constraints | 约束

- 第一版只处理团队内部会议

## Success Metrics | 成功标准

- 能稳定生成 task-packet 并指导后续实现

## Assumptions | 假设

- 默认用户更在意收敛速度而不是花哨交互

## Next Step | 下一步

- Run product review first, then engineering review, and only convert to a task-packet after scope is stable. | 先过产品评审和工程评审，范围稳定后再转成 task-packet | 任务包。
