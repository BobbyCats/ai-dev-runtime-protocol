# Domain Map | 领域地图: AI schedule assistant

- Domain Map ID | 领域地图 ID: `ai-schedule-assistant`
- Generated | 生成时间: `2026-03-20T18:22:39+00:00`
- Orchestrator | 编排层: calendar-orchestrator

## Domains | 业务域

### schedule

- Owned State | 拥有状态
  - events
  - availability
- Capabilities | 核心能力
  - create
  - update
  - delete
- Non-Goals | 不负责什么
  - expense tracking

### expense

- Owned State | 拥有状态
  - expense records
  - reimbursement items
- Capabilities | 核心能力
  - record expense
  - link receipt
  - export reimbursement
- Non-Goals | 不负责什么
  - calendar rendering

## Shared Infrastructure | 共享基础设施

- logging
- auth

## Cross-Domain Flows | 跨域流程

- `travel reimbursement`: 发起方 `chat request`，涉及 `schedule, expense`，结果归属 `expense`
