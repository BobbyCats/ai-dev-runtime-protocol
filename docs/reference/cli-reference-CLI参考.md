# CLI Reference | CLI 参考

这份文档不是 `--help` 的复制版，而是按阶段组织的命令使用说明。

阅读方法：

- 想知道“现在该用哪个命令”，按阶段看
- 想知道“某个命令最少需要什么参数”，看每条里的最小用法
- 想知道“它通常和谁一起用”，看常见搭配

## 0. 初始化与全局认知

### `init-workspace`

用途：

- 初始化 `.aidrp/` 工作区
- 生成默认 `config.json`
- 可选写入最小 `AGENTS.md`

最小用法：

```bash
python -m aidrp init-workspace --project-root . --write-agents-template
```

何时使用：

- 第一次把这套协议接进一个项目
- 端到端教程起点

常见搭配：

- `repo-map`
- `task-packet`
- `debug-pack`

典型输出：

- `.aidrp/config.json`
- `.aidrp/briefs/`
- `.aidrp/tasks/`
- `.aidrp/debug/`

### `repo-map`

用途：

- 压缩仓库上下文
- 给后续任务包和排障包提供候选文件

最小用法：

```bash
python -m aidrp repo-map --project-root . --output-dir .aidrp
```

何时使用：

- 几乎所有中等以上项目
- 不清楚先读哪些文件时

常见搭配：

- `task-packet`
- `debug-pack`

典型输出：

- `repo-map.json`
- `repo-map.md`

## 1. 需求与评审输入

### `requirement-brief`

用途：

- 把模糊想法压成结构化简报

最小用法：

```bash
python -m aidrp requirement-brief \
  --title "AI 会议助手第一版" \
  --product-idea "先把模糊会议需求收敛成结构化计划。" \
  --target-user "需要高频安排会议的团队负责人" \
  --pain-point "需求一开始太散，容易直接做偏" \
  --desired-outcome "先得到一份稳定简报再进入工程评审"
```

何时使用：

- 需求还不稳定
- 想先砍范围再开工

常见搭配：

- `product-review`
- `repo-map`
- `engineering-review`
- `task-packet`

典型输出：

- `briefs/*.json`
- `briefs/*.md`

说明：

- `需求访谈` 当前以模板和 playbook 为主，不是 CLI 命令

### `product-review`

用途：

- 把产品评审结论结构化，不再只停留在一段会后总结

最小用法：

```bash
python -m aidrp product-review \
  --brief .aidrp/briefs/<brief-id>.json \
  --current-goal "把第一版压成可交付切片" \
  --scope-decision 保持 \
  --scope-reason "第一版边界已经清楚，先做稳"
```

何时使用：

- 已有 `requirement-brief`
- 还没决定第一版是扩、保持还是缩

常见搭配：

- `repo-map`
- `engineering-review`
- `task-packet`

典型输出：

- `product-reviews/*.json`
- `product-reviews/*.md`

### `engineering-review`

用途：

- 把工程评审从会前共识变成可复用工件

最小用法：

```bash
python -m aidrp engineering-review \
  --project-root . \
  --brief .aidrp/briefs/<brief-id>.json \
  --product-review .aidrp/product-reviews/<review-id>.json \
  --repo-map .aidrp/repo-map.json \
  --change-goal "只修最小改动面" \
  --decision 可以开工
```

何时使用：

- 已经知道要做什么，但还没定写入边界和验证方式
- 已经有 `repo-map`，想把候选文件、写入边界和验证路径压成正式工件

常见搭配：

- `repo-map`
- `task-packet`
- `debug-pack`

典型输出：

- `engineering-reviews/*.json`
- `engineering-reviews/*.md`

## 2. 任务执行输入

### `task-packet`

用途：

- 给一次功能或定点修复收窄阅读范围
- 明确范围、约束、验收标准

最小用法：

```bash
python -m aidrp task-packet \
  --project-root . \
  --repo-map .aidrp/repo-map.json \
  --title "Fix meeting deletion drift 修复会议删除漂移" \
  --objective "只修删除链路，不顺手扩成重构" \
  --type bugfix \
  --scope "只改删除解析、执行和相关测试" \
  --acceptance "删除动作必须命中正确会议"
```

何时使用：

- 知道要做什么，但不想让 AI 扩散扫描

常见搭配：

- `repo-map`
- `trace-start`
- `doc-sync`

典型输出：

- `tasks/*.json`
- `tasks/*.md`

### `debug-pack`

用途：

- 把一次 bug 的症状、证据和初步排查短名单结构化

最小用法：

```bash
python -m aidrp debug-pack \
  --project-root . \
  --repo-map .aidrp/repo-map.json \
  --title "Meeting deletion drift 会议删除漂移" \
  --symptom "删除选中的会议时误删了另一条" \
  --observed "界面提示成功，但消失的是错误卡片" \
  --expected "只能删除用户点中的会议" \
  --trace-id "trace-meeting-001" \
  --entrypoint "meeting.delete" \
  --failure-stage "executor"
```

何时使用：

- 本地 bug
- 线上 bug
- UI 表象和根因脱节时

常见搭配：

- `observability-correlation`
- `trace-start`
- `eval-case`

典型输出：

- `debug/*.json`
- `debug/*.md`

## 3. 架构与边界

### `domain-map`

用途：

- 明确业务域、状态归属和跨域编排关系

最小用法：

```bash
python -m aidrp domain-map \
  --product "AI schedule assistant" \
  --orchestrator "calendar-orchestrator" \
  --domain "schedule|events,availability|create,update,delete|expense tracking"
```

何时使用：

- 项目开始出现多个业务域
- Agent 之间开始跨域协调

常见搭配：

- `tool-contract`
- `execution-plan`

典型输出：

- `domains/*.json`
- `domains/*.md`

### `tool-contract`

用途：

- 把工具的输入、输出、幂等、失败语义和权限边界写清楚

最小用法：

```bash
python -m aidrp tool-contract \
  --tool-name "delete_event" \
  --domain "schedule" \
  --purpose "Delete a schedule event by stable ID." \
  --input-field "event_id|string|true|Stable event identifier." \
  --output-field "deleted|boolean|Whether deletion succeeded."
```

何时使用：

- 工具越来越多
- 不想让工具内部继续塞隐性逻辑

常见搭配：

- `execution-plan`
- `cost-privacy-budget`

典型输出：

- `contracts/*.json`
- `contracts/*.md`

### `execution-plan`

用途：

- 把“先计划、后执行”的流水线落成结构化工件

最小用法：

```bash
python -m aidrp execution-plan \
  --title "Delete event safely" \
  --goal "Delete the selected event after confirmation." \
  --step "Resolve target|event_id|fetch_event|event snapshot|false" \
  --step "Execute delete|event snapshot|delete_event|delete result|true"
```

何时使用：

- Agent 任务不止一步
- ReAct 循环开始太慢或太散

常见搭配：

- `tool-contract`
- `observability-correlation`

典型输出：

- `plans/*.json`
- `plans/*.md`

### `cost-privacy-budget`

用途：

- 约束上下文预算、推理预算、权限预算和数据暴露预算

最小用法：

```bash
python -m aidrp cost-privacy-budget \
  --project-root . \
  --workflow "debug flow" \
  --allowed-tool "read" \
  --allowed-tool "grep" \
  --confirm-action "delete"
```

何时使用：

- 项目开始走向生产或多人协作
- 需要控制 token、权限和敏感信息

常见搭配：

- `domain-map`
- `tool-contract`
- `execution-plan`

典型输出：

- `budgets/*.json`
- `budgets/*.md`

## 4. 排障与可观测性

### `observability-correlation`

用途：

- 用 trace、request、decision、plan、tool call 编号缩圈日志

最小用法：

```bash
python -m aidrp observability-correlation \
  --project-root . \
  --title "Meeting deletion correlation 会议删除关联" \
  --trace-id "trace-meeting-001" \
  --decision-id "dec-meeting-001" \
  --entrypoint "meeting.delete" \
  --failure-stage "executor" \
  --log-file "logs/runtime.log"
```

何时使用：

- 有真实日志
- 不想再从症状反推全仓代码

常见搭配：

- `debug-pack`
- `eval-case`

典型输出：

- `correlations/*.json`
- `correlations/*.md`

### `trace-start`

用途：

- 创建一条决策轨迹

最小用法：

```bash
python -m aidrp trace-start \
  --title "Fix meeting deletion drift 修复会议删除漂移" \
  --task-id meeting-delete-fix
```

何时使用：

- 需要记录关键假设和转向

常见搭配：

- `trace-event`
- `task-packet`
- `debug-pack`

典型输出：

- `traces/*.json`

### `trace-event`

用途：

- 追加一次决策、排查或验证事件

最小用法：

```bash
python -m aidrp trace-event \
  --trace-file .aidrp/traces/meeting-delete-fix.json \
  --stage investigate \
  --summary "Confirmed selection_id resolves to visible_index, not stable meeting_id."
```

何时使用：

- 每次关键判断发生变化时

常见搭配：

- `trace-start`

典型输出：

- 更新现有 `traces/*.json`

### `eval-case`

用途：

- 把真实 bug 沉淀成回归用例

最小用法：

```bash
python -m aidrp eval-case \
  --title "Regression for meeting deletion drift 会议删除漂移回归用例" \
  --origin "debug-pack:meeting-deletion-drift-会议删除漂移" \
  --command "python -m unittest" \
  --repro-step "删除列表中的第二个会议" \
  --assertion "只能删除目标会议"
```

何时使用：

- 修完 bug 之后
- 上线前需要固定回归场景

常见搭配：

- `debug-pack`
- `doc-sync`

典型输出：

- `evals/*.json`
- `evals/*.md`

## 5. 视觉系统

### `design-token-pack`

用途：

- 把颜色、字号、间距、语义令牌和组件指导结构化
- 同时输出 HTML 预览，防止风格漂移

最小用法：

```bash
python -m aidrp design-token-pack \
  --title "AI schedule UI 日程助手界面" \
  --surface "Conversation-first scheduling assistant" \
  --brand-direction "Calm productivity with low visual noise." \
  --brand-color "#0F766E"
```

何时使用：

- 新页面
- 新主题
- 组件系统漂移

常见搭配：

- `task-packet`
- `doc-sync`

典型输出：

- `design-system/*.json`
- `design-system/*.md`
- `design-system/*.html`

## 6. 收尾与治理

### `doc-sync`

用途：

- 判断 README 和核心文档该补丁更新、章节重写还是整篇重写

最小用法：

```bash
python -m aidrp doc-sync \
  --project-root . \
  --title "Meeting deletion docs refresh 会议删除修复文档同步" \
  --summary "Tightened deletion flow and refreshed walkthrough references." \
  --changed-file src/calendar_agent.py \
  --changed-file docs/tutorials/e2e-walkthrough-端到端教程.md
```

何时使用：

- 所有非 trivial 变更的收尾阶段

常见搭配：

- `eval-case`
- `README` 重写

典型输出：

- `docsync/*.json`
- `docsync/*.md`

## 错误输入与失败路径

最常见的失败来自三类命令：

- `domain-map`
  `--domain` 字段段数不足
- `tool-contract`
  `--input-field` 或 `--output-field` 格式不完整
- `execution-plan`
  `--step` 不是 5 段结构

这些命令失败时会直接走 `parser.error(...)`，这是预期行为。

## 相关阅读

- [完整使用手册](../guides/usage-guide-完整使用手册.md)
- [端到端教程](../tutorials/e2e-walkthrough-端到端教程.md)
- [meeting-assistant 场景](../../examples/scenarios/meeting-assistant/README.md)
