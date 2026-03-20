# 领域地图（Domain Map）

适用场景：

- 你开始从单一功能走向多业务域
- 你发现不同 Agent、模块、服务之间开始互相污染
- 你想做的是 AI 原生产品，而不是只有一个聊天入口的脚本集合

## 这一步解决什么问题

王自如方法里一个很关键的点，不是“多 Agent”，而是**先把业务域拆清楚**。

没有领域地图时，最常见的问题是：

- 日程、费用、搜索、OCR、通知混成一个大流程
- 谁拥有状态、谁能改状态说不清
- 一次小改动就牵连所有工具
- Agent 看起来很聪明，实际上没有边界

## 最少要画清楚的 5 件事

1. 领域列表：有哪些独立业务域
2. 领域拥有的状态：每个域真正拥有哪类数据
3. 域内能力：这个域自己能做什么
4. 跨域协调者：哪些任务由 orchestrator 统一编排
5. 共享基础设施：日志、鉴权、存储、队列、搜索这类底座由谁提供

## 推荐规则

- 一个业务状态只能有一个主拥有域
- 跨域需求优先交给编排层，不要让领域互相直连写库
- 共享基础设施是共享，不是共享业务语义
- 领域拆分先服务真实任务，不为了“看起来高级”而拆

## 产物要求

至少沉淀：

- `domain-map.schema.json` 对应的结构化文件
- 一份人能直接阅读的领域地图说明
- 每个域的边界、状态归属和跨域协作说明

推荐模板：

- [templates/domain-map-领域地图.md](../../templates/domain-map-领域地图.md)

## CLI 用法

```bash
python -m aidrp domain-map \
  --product "AI schedule assistant" \
  --orchestrator "calendar-orchestrator" \
  --domain "schedule|events,availability|create,update,delete|expense tracking" \
  --domain "expense|expense records,reimbursement items|record expense,link receipt,export reimbursement|calendar rendering"
```
