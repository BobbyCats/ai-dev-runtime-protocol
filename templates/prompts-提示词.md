# Prompt Starters | 提示词起手式

## Task Packet First | 先任务包

先读 `.aidrp/repo-map.md`，再创建或打开对应的 `task-packet | 任务包`。在任务包候选文件读完之前，不要全仓扫描。

## Debug Pack First | 先排障包

先打开 `debug-pack | 排障包`，先复现，再提修复建议。优先按照排障包中的阅读顺序和疑似文件排查。

## Trace Discipline | 轨迹纪律

一旦你的判断方向改变，或者你准备扩大范围，就追加一条 `decision-trace | 决策轨迹`。

## Eval Discipline | 回归纪律

一旦真实 bug 被确认并修复，就创建 `eval-case | 回归用例`，把这次失败沉淀下来。
