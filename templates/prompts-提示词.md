# Prompt Starters | 提示词起手式

## Discovery Interview First | 先需求访谈

如果需求本身还模糊，不要直接写方案或写代码。先按 `templates/discovery-interview-需求访谈.md` 做访谈，再输出 `需求简报（requirement-brief）`。

## Product Review First | 先产品评审

如果需求刚收敛，还没明确第一版范围，不要直接拆工程任务。先按 `docs/playbooks/plan-product-review-产品评审.md` 判断是扩 scope、保持 scope，还是缩 scope。

## Engineering Review First | 先工程评审

如果你已经知道要做什么，但还没确定最小改动面、验证方式和风险边界，不要直接开写。先按 `docs/playbooks/plan-engineering-review-工程评审.md` 做工程评审。

## Task Packet First | 先任务包

先读 `.aidrp/repo-map.md`，再创建或打开对应的 `任务包（task-packet）`。在任务包候选文件读完之前，不要全仓扫描。

## Debug Pack First | 先排障包

先打开 `排障包（debug-pack）`，先复现，再提修复建议。优先按照排障包中的阅读顺序和疑似文件排查。

## Investigate First | 先根因调查

Bug 不要一上来就修。先按 `docs/playbooks/investigate-根因调查.md` 建立假设、收证据、缩小原因，再决定修哪一层。

## Live QA First | 先真实验收

只跑单元测试，不等于已经验证完成。涉及真实用户路径、CLI、API 或文件输出的改动，按 `docs/playbooks/qa-live-真实验收.md` 去真实入口验一次。

## Trace Discipline | 轨迹纪律

一旦你的判断方向改变，或者你准备扩大范围，就追加一条 `决策轨迹（decision-trace）`。

## Eval Discipline | 回归纪律

一旦真实 bug 被确认并修复，就创建 `回归用例（eval-case）`，把这次失败沉淀下来。

## Documentation Sync Discipline | 文档同步纪律

非 trivial 变更收尾前，先生成 `文档同步包（doc-sync）`。如果命令表面、阶段顺序或系统定位变了，README 不能只追加一段，必须按章节或整篇重写。
