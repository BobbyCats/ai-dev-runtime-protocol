# Examples | 示例

这个目录存放的是仓库自身生成出来的示例工件。

包括：

- `repo-map | 仓库地图`
- `requirement-brief | 需求简报`
- `task-packet | 任务包`
- `debug-pack | 排障包`
- `eval-case | 回归用例`
- `doc-sync | 文档同步包`

你可以在安装后重新生成：

```bash
python -m aidrp init-workspace --project-root . --write-agents-template
python -m aidrp repo-map --project-root . --output-dir examples/outputs
python -m aidrp requirement-brief --title "AI meeting helper AI 会议助手" --product-idea "先通过需求访谈把问题聊清楚，再决定写不写代码 | Use a discovery interview before coding" --target-user "脑子里先有感觉、但暂时说不清需求的构建者 | Builders with fuzzy first ideas" --pain-point "想法太散，没法直接开写，也容易一上来做偏 | Ideas are too vague to code directly" --desired-outcome "把对话收敛成一份能继续执行的结构化简报 | Turn conversation into a structured brief" --output-dir examples/outputs
python -m aidrp doc-sync --project-root . --title "Stage router refresh 阶段路由升级" --summary "Added stage router, review playbooks, investigate discipline, live QA guidance, and documentation sync." --changed-file src/aidrp/cli.py --changed-file docs/playbooks/stage-router-阶段路由.md --changed-file README.md --output-dir examples/outputs
```
