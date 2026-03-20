# Examples | 示例地图

这个目录现在分三类内容，不再只是单个工件的堆叠。

## 1. 单工件示例

目录：

- `examples/outputs/`

这里存放的是仓库自身生成出来的标准工件样例，适合：

- 快速看某个工件长什么样
- 对照 CLI 输出
- 做快照或金样参考

包括：

- `repo-map | 仓库地图`
- `requirement-brief | 需求简报`
- `product-review | 产品评审`
- `engineering-review | 工程评审`
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

## 2. 端到端教程样例

目录：

- `examples/scenarios/meeting-assistant/`

这里是一个完整的教学场景，包含：

- `fixture/`：最小可复现样例仓库
- `inputs/`：需求、bug、trace 和文档同步的输入素材
- `expected/`：关键工件的标准输出

先看：

- [meeting-assistant 场景说明](scenarios/meeting-assistant/README.md)
- [端到端教程](../docs/tutorials/e2e-walkthrough-端到端教程.md)

## 3. 真实日志排障样例

目录：

- `examples/logs/`

这里放的是排障和可观测性关联演示用日志。

如果你想知道这些示例分别该在什么场景下使用，先看：

- [完整使用手册](../docs/guides/usage-guide-完整使用手册.md)
- [CLI 参考](../docs/reference/cli-reference-CLI参考.md)

## 重新生成单工件示例

你可以在安装后重新生成 `examples/outputs/` 里的单工件样例：

```bash
python -m aidrp init-workspace --project-root . --write-agents-template
python -m aidrp repo-map --project-root . --output-dir examples/outputs
python -m aidrp requirement-brief --title "AI meeting helper AI 会议助手" --product-idea "先通过需求访谈把问题聊清楚，再决定写不写代码 | Use a discovery interview before coding" --target-user "脑子里先有感觉、但暂时说不清需求的构建者 | Builders with fuzzy first ideas" --pain-point "想法太散，没法直接开写，也容易一上来做偏 | Ideas are too vague to code directly" --desired-outcome "把对话收敛成一份能继续执行的结构化简报 | Turn conversation into a structured brief" --output-dir examples/outputs
python -m aidrp product-review --brief examples/outputs/ai-meeting-helper-ai-会议助手.json --current-goal "把第一版压成可交付切片" --scope-decision 保持 --scope-reason "先把最小有价值切片做稳，再决定是否扩范围" --output-dir examples/outputs
python -m aidrp engineering-review --project-root . --brief examples/outputs/ai-meeting-helper-ai-会议助手.json --product-review examples/outputs/ai-meeting-helper-ai-会议助手-product-review.json --repo-map examples/outputs/repo-map.json --change-goal "先固定写入边界、候选文件和验证方式" --decision 可以开工 --output-dir examples/outputs
python -m aidrp domain-map --product "AI schedule assistant" --orchestrator "calendar-orchestrator" --domain "schedule|events,availability|create,update,delete|expense tracking" --output-dir examples/outputs
python -m aidrp tool-contract --tool-name "delete_event" --domain "schedule" --purpose "Delete an event by stable ID." --input-field "event_id|string|true|Stable event identifier." --output-field "deleted|boolean|Whether deletion succeeded." --output-dir examples/outputs
python -m aidrp execution-plan --title "Delete event safely" --goal "Delete the targeted event after confirmation." --step "Resolve target|event_id|fetch_event|event snapshot|false" --step "Execute delete|event snapshot|delete_event|delete result|true" --output-dir examples/outputs
python -m aidrp design-token-pack --title "AI schedule UI 日程助手界面" --surface "Conversation-first scheduling and expense assistant 对话优先的日程与费用助手" --brand-direction "Calm productivity with strong structure and low visual noise. 冷静、高效、结构感强、低噪音。" --brand-color "#0F766E" --accent-color "#F59E0B" --output-dir examples/outputs
python -m aidrp observability-correlation --project-root . --title "Delete event correlation" --trace-id "trace-77" --decision-id "dec-99" --entrypoint "calendar.delete" --failure-stage "executor" --log-file "examples/logs/runtime-delete-demo.log" --output-dir examples/outputs
python -m aidrp cost-privacy-budget --project-root . --workflow "debug flow" --allowed-tool "read" --allowed-tool "grep" --confirm-action "delete" --output-dir examples/outputs
python -m aidrp doc-sync --project-root . --title "Stage router refresh 阶段路由升级" --summary "Added stage router, review playbooks, investigate discipline, live QA guidance, and documentation sync." --changed-file src/aidrp/cli.py --changed-file docs/playbooks/stage-router-阶段路由.md --changed-file README.md --output-dir examples/outputs
```
