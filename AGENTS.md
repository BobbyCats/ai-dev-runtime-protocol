# AGENTS

这个仓库是中文主导、双语术语的 AI 开发运行协议。

## 工作规则

- 大改之前先读 [ONBOARDING.md](ONBOARDING.md)
- 优先生成 `.aidrp/` 工件，而不是直接大范围扫仓库
- 想法不清楚时，先做 `discovery interview | 需求访谈`，再写 `requirement-brief | 需求简报`
- 非 trivial 任务先生成 `task-packet | 任务包`
- bug 先生成 `debug-pack | 排障包`
- 判断方向变了，就写 `decision-trace | 决策轨迹`
- 真实 bug 修完后，补 `eval-case | 回归用例`

## 验证

- `python -m unittest discover -s tests -v`
- `python -m aidrp repo-map --project-root . --output-dir .aidrp`

## 编辑边界

- 运行时保持无第三方依赖
- 优先 JSON 工件和确定性输出
- 核心逻辑避免绑定特定模型平台
