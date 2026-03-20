# 成本权限预算（Cost & Privacy Budget）

适用场景：

- 你的 Agent 已经能做很多事，但越来越烧 token
- 需要接触发票、联系人、日程、企业数据等敏感信息
- 你开始从 demo 走向真实可用产品

## 这一步解决什么问题

能跑通 demo，不等于能长期使用。  
很多 AI 工作流失败，不是因为模型不够聪明，而是：

- 上下文成本失控
- 敏感数据权限过宽
- 每次都默认最高推理强度
- 没有为不同任务设预算和降级路径

## 至少要定的 4 类预算

1. 上下文预算：一次最多读多少文件
2. 推理预算：什么场景允许长推理，什么场景只准短推理
3. 权限预算：哪些工具默认禁用，哪些操作必须确认
4. 数据预算：什么数据能出本地、能进日志、能给外部模型

## 推荐规则

- 默认用最便宜、最小上下文的路径
- 只有证据不足时才升级模型或扩大上下文
- 敏感字段入日志前先脱敏
- 高风险写操作必须有人类确认门

推荐模板：

- [templates/cost-privacy-budget-成本权限预算.md](../../templates/cost-privacy-budget-成本权限预算.md)

## CLI 用法

```bash
python -m aidrp cost-privacy-budget \
  --project-root . \
  --workflow "debug flow" \
  --allowed-tool "read" \
  --allowed-tool "grep" \
  --confirm-action "delete"
```
