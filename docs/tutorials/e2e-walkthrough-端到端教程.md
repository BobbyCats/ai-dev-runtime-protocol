# End-to-End Walkthrough | 端到端教程

这份教程不是“看看命令长什么样”，而是让你真的完整跑一遍：

从一个模糊需求开始，到排出一个真实 bug，再到补回归和文档同步。

## 这次会用到什么

本教程绑定仓库里的这个场景：

- [meeting-assistant 场景说明](../../examples/scenarios/meeting-assistant/README.md)

你会用到里面三类资产：

- `fixture/`：最小样例仓库
- `inputs/`：需求、bug、trace 和同步输入
- `expected/`：关键工件的标准输出

## 你会走完哪条链

1. 初始化工作区
2. 生成 `requirement-brief`
3. 用产品评审和工程评审 playbook 锁范围
4. 生成 `repo-map`
5. 生成 `task-packet`
6. 为删除误删 bug 生成 `debug-pack`
7. 跑 `observability-correlation`
8. 写 `eval-case`
9. 生成 `doc-sync`

这条链刻意没有塞满所有工件。

原因很简单：

- 你第一次上手时，最重要的是先把“需求 -> 实现 -> 排障 -> 收尾”的主链跑通
- `domain-map / tool-contract / execution-plan / cost-privacy-budget` 更适合第二轮再加

## 0. 进入样例工作区

进入这里：

- `examples/scenarios/meeting-assistant/fixture`

如果你已经在仓库根目录，执行：

```bash
cd examples/scenarios/meeting-assistant/fixture
```

## 1. 初始化 `.aidrp`

```bash
python -m aidrp init-workspace --project-root . --write-agents-template
```

你应该看到：

- `.aidrp/config.json`
- `.aidrp/briefs/`
- `.aidrp/tasks/`
- `.aidrp/debug/`
- `.aidrp/evals/`
- `.aidrp/docsync/`
- `AGENTS.md`

这一步的意义不是“多建几个目录”，而是给后续工件一个稳定落点。

## 2. 从模糊想法生成 `requirement-brief`

这个场景的目标是做一个 AI 会议助手第一版。

输入素材在：

- `../inputs/requirement-brief.json`

执行：

```bash
python -m aidrp requirement-brief \
  --title "AI 会议助手第一版" \
  --product-idea "把模糊会议安排需求收敛成结构化计划，再交给用户确认和执行。" \
  --target-user "高频安排评审会和同步会的团队负责人" \
  --pain-point "会议安排总在聊天里反复改，最后没人能准确回答到底定在哪个时间" \
  --desired-outcome "先得到一份范围稳定的第一版简报" \
  --scenario "通过聊天创建、改期和删除会议" \
  --scenario "在删除前给出可确认的计划" \
  --non-goal "第一版不做外部日历双向同步" \
  --constraint "第一版只处理团队内部会议" \
  --success-metric "能稳定生成 task-packet 并指导后续实现" \
  --assumption "默认用户更在意收敛速度而不是花哨交互" \
  --output-dir .aidrp/briefs
```

对照标准输出：

- `../expected/ai-会议助手第一版.json`
- `../expected/ai-会议助手第一版.md`

## 3. 用评审层锁住范围

这一步没有 CLI，走 playbook。

先看：

- [产品评审](../playbooks/plan-product-review-产品评审.md)
- [工程评审](../playbooks/plan-engineering-review-工程评审.md)

在这个场景里，我们固定这两个结论：

- 产品评审：第一版只做“创建 / 查看 / 删除会议”，不做日历同步、邀请邮件和复杂权限
- 工程评审：本轮只修删除误删链路，不把存储层或前端状态整体重构

如果你想看这次教程的人工评审输入，可以看：

- `../inputs/review-decisions.md`

## 4. 生成 `repo-map`

```bash
python -m aidrp repo-map --project-root . --output-dir .aidrp
```

这一步完成后，先看：

- `.aidrp/repo-map.md`

你应该能快速识别这些高信号文件：

- `README.md`
- `src/calendar_agent.py`
- `src/event_store.py`
- `src/ui_state.py`
- `design-system/meeting-ui-tokens.json`

对照标准输出：

- `../expected/repo-map.json`
- `../expected/repo-map.md`

## 5. 生成 `task-packet`

这里我们把这次工作明确压成“修删除漂移”，而不是“顺手重构整个会议系统”。

输入素材在：

- `../inputs/task-packet.json`

执行：

```bash
python -m aidrp task-packet \
  --project-root . \
  --repo-map .aidrp/repo-map.json \
  --title "Fix meeting deletion drift 修复会议删除漂移" \
  --objective "只修删除解析和执行链路，不顺手扩成一次存储层重构" \
  --type bugfix \
  --scope "只改删除目标解析、执行器和相关测试" \
  --non-goal "不重做整个会议列表状态管理" \
  --acceptance "删除动作必须命中正确会议" \
  --acceptance "日志里能串起删除链路的关键编号" \
  --constraint "不要扩大到邀请、同步或提醒功能" \
  --search-term "meeting" \
  --search-term "delete" \
  --search-term "selection" \
  --search-term "event" \
  --output-dir .aidrp/tasks
```

看这两个点：

- `read_order` 已经把范围收窄了
- `candidate_files` 不应该乱飘到无关文件

对照标准输出：

- `../expected/fix-meeting-deletion-drift-修复会议删除漂移.json`
- `../expected/fix-meeting-deletion-drift-修复会议删除漂移.md`

## 6. 为误删 bug 生成 `debug-pack`

现在进入真实 bug。

症状是：

- 用户点第二个会议卡片
- 实际删掉的是另一条会议

输入素材在：

- `../inputs/debug-pack.json`

执行：

```bash
python -m aidrp debug-pack \
  --project-root . \
  --repo-map .aidrp/repo-map.json \
  --title "Meeting deletion drift 会议删除漂移" \
  --symptom "删除选中的会议时，另一条会议也可能被误删" \
  --observed "界面提示删除成功，但消失的是错误的会议卡片" \
  --expected "只能删除用户点中的会议" \
  --impact "团队会对会议状态失去信任，后续改期和确认都不可靠" \
  --trace-id "trace-meeting-001" \
  --request-id "req-meeting-001" \
  --decision-id "dec-meeting-001" \
  --plan-id "plan-delete-001" \
  --tool-call-id "tool-delete-001" \
  --entrypoint "meeting.delete" \
  --failure-stage "executor" \
  --repro-step "打开会议列表并删除第二条会议" \
  --repro-step "确认弹窗后观察实际消失的卡片" \
  --suspected-file "src/calendar_agent.py" \
  --suspected-file "src/ui_state.py" \
  --log-file "logs/runtime.log" \
  --search-term "wrong meeting removed" \
  --search-term "selection_id" \
  --search-term "meeting_id" \
  --output-dir .aidrp/debug
```

这里重点看三件事：

- `triage_read_order` 是否仍然收敛
- `log_focus` 是否已经带出关键编号
- `evidence` 是否开始给出像样的代码和日志证据

对照标准输出：

- `../expected/meeting-deletion-drift-会议删除漂移.json`
- `../expected/meeting-deletion-drift-会议删除漂移.md`

## 7. 单独跑 `observability-correlation`

这一步是把“不要先扫全仓”做实。

执行：

```bash
python -m aidrp observability-correlation \
  --project-root . \
  --title "Meeting deletion correlation 会议删除关联" \
  --trace-id "trace-meeting-001" \
  --request-id "req-meeting-001" \
  --decision-id "dec-meeting-001" \
  --plan-id "plan-delete-001" \
  --tool-call-id "tool-delete-001" \
  --entrypoint "meeting.delete" \
  --failure-stage "executor" \
  --log-file "logs/runtime.log" \
  --search-term "wrong meeting removed" \
  --output-dir .aidrp/correlations
```

你应该能直接看到：

- 关键编号已经能命中日志
- 故障阶段是 `executor`
- 当前应该优先看 `calendar_agent.py` 和 `event_store.py`

对照标准输出：

- `../expected/meeting-deletion-correlation-会议删除关联.json`
- `../expected/meeting-deletion-correlation-会议删除关联.md`

## 8. 写 `eval-case`

修完以后，不要只停在“这次好了”。

执行：

```bash
python -m aidrp eval-case \
  --title "Regression for meeting deletion drift 会议删除漂移回归用例" \
  --origin "debug-pack:meeting-deletion-drift-会议删除漂移" \
  --command "python -m unittest" \
  --repro-step "删除会议列表中的第二条会议" \
  --assertion "只能删除目标会议，其他会议必须保持不变" \
  --tag "bugfix" \
  --tag "meeting" \
  --tag "delete" \
  --output-dir .aidrp/evals
```

对照标准输出：

- `../expected/regression-for-meeting-deletion-drift-会议删除漂移回归用例.json`
- `../expected/regression-for-meeting-deletion-drift-会议删除漂移回归用例.md`

## 9. 最后跑 `doc-sync`

只要这个修复改变了：

- 用户可见行为
- 默认工作流
- 教程或示例

就不应该跳过这一步。

执行：

```bash
python -m aidrp doc-sync \
  --project-root . \
  --title "Meeting deletion docs refresh 会议删除修复文档同步" \
  --summary "删除链路已经改成稳定 meeting_id，相关 walkthrough、示例和 README 索引都需要同步。" \
  --changed-file "src/calendar_agent.py" \
  --changed-file "src/event_store.py" \
  --changed-file "docs/tutorials/e2e-walkthrough-端到端教程.md" \
  --change-note "不要只补一句，先检查 README 的工作流表达是否仍然准确。" \
  --output-dir .aidrp/docsync
```

对照标准输出：

- `../expected/meeting-deletion-docs-refresh-会议删除修复文档同步.json`
- `../expected/meeting-deletion-docs-refresh-会议删除修复文档同步.md`

## 这条链跑完后你应该得到什么

- 你知道初始化一个新项目时先跑什么
- 你知道不是所有问题都应该直接进写代码
- 你知道排障时为什么先看编号和日志，而不是症状和猜测
- 你知道修完后为什么必须补回归和文档同步

## 下一步怎么继续

如果你已经把这条主链跑通，第二轮建议补这三类工件：

- `domain-map`
- `tool-contract`
- `execution-plan`

然后再把：

- `cost-privacy-budget`

接进你的真实项目。

## 相关阅读

- [完整使用手册](../guides/usage-guide-完整使用手册.md)
- [CLI 参考](../reference/cli-reference-CLI参考.md)
- [meeting-assistant 场景说明](../../examples/scenarios/meeting-assistant/README.md)
