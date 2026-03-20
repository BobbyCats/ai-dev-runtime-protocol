# Examples | 示例

这个目录存放的是仓库自身生成出来的示例工件。

如果你想知道这些示例分别该在什么场景下使用，先看：

- [docs/guides/usage-guide-完整使用手册.md](../docs/guides/usage-guide-完整使用手册.md)

包括：

- `repo-map | 仓库地图`
- `requirement-brief | 需求简报`
- `design-token-pack | 设计令牌包`
- `domain-map | 领域地图`
- `tool-contract | 工具契约`
- `execution-plan | 执行计划`
- `task-packet | 任务包`
- `debug-pack | 排障包`
- `observability-correlation | 可观测性关联`
- `eval-case | 回归用例`
- `cost-privacy-budget | 成本权限预算`
- `doc-sync | 文档同步包`

另外还包含：

- `examples/logs/` 下的示例运行日志，用于演示真实日志排障流

你可以在安装后重新生成：

```bash
python -m aidrp init-workspace --project-root . --write-agents-template
python -m aidrp repo-map --project-root . --output-dir examples/outputs
python -m aidrp requirement-brief --title "AI meeting helper AI 会议助手" --product-idea "先通过需求访谈把问题聊清楚，再决定写不写代码 | Use a discovery interview before coding" --target-user "脑子里先有感觉、但暂时说不清需求的构建者 | Builders with fuzzy first ideas" --pain-point "想法太散，没法直接开写，也容易一上来做偏 | Ideas are too vague to code directly" --desired-outcome "把对话收敛成一份能继续执行的结构化简报 | Turn conversation into a structured brief" --output-dir examples/outputs
python -m aidrp domain-map --product "AI schedule assistant" --orchestrator "calendar-orchestrator" --domain "schedule|events,availability|create,update,delete|expense tracking" --output-dir examples/outputs
python -m aidrp tool-contract --tool-name "delete_event" --domain "schedule" --purpose "Delete an event by stable ID." --input-field "event_id|string|true|Stable event identifier." --output-field "deleted|boolean|Whether deletion succeeded." --output-dir examples/outputs
python -m aidrp execution-plan --title "Delete event safely" --goal "Delete the targeted event after confirmation." --step "Resolve target|event_id|fetch_event|event snapshot|false" --step "Execute delete|event snapshot|delete_event|delete result|true" --output-dir examples/outputs
python -m aidrp design-token-pack --title "AI schedule UI 日程助手界面" --surface "Conversation-first scheduling and expense assistant 对话优先的日程与费用助手" --brand-direction "Calm productivity with strong structure and low visual noise. 冷静、高效、结构感强、低噪音。" --brand-color "#0F766E" --accent-color "#F59E0B" --output-dir examples/outputs
python -m aidrp observability-correlation --project-root . --title "Delete event correlation" --trace-id "trace-77" --decision-id "dec-99" --entrypoint "calendar.delete" --failure-stage "executor" --log-file "examples/logs/runtime-delete-demo.log" --output-dir examples/outputs
python -m aidrp cost-privacy-budget --project-root . --workflow "debug flow" --allowed-tool "read" --allowed-tool "grep" --confirm-action "delete" --output-dir examples/outputs
python -m aidrp doc-sync --project-root . --title "Stage router refresh 阶段路由升级" --summary "Added stage router, review playbooks, investigate discipline, live QA guidance, and documentation sync." --changed-file src/aidrp/cli.py --changed-file docs/playbooks/stage-router-阶段路由.md --changed-file README.md --output-dir examples/outputs
```
