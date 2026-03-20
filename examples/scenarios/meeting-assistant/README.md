# Meeting Assistant Scenario | AI 会议助手场景

这是仓库内置的端到端教学场景。

它不是一个“假装完整”的大项目，而是一个专门拿来练这套协议主链的最小样例。

## 你能在这里练什么

- 从模糊需求生成 `requirement-brief`
- 生成 `product-review` 和 `engineering-review`
- 给样例仓库生成 `repo-map`
- 为一次定点修复生成 `task-packet`
- 为“删除会议误删对象”生成 `debug-pack`
- 用真实日志跑 `observability-correlation`
- 修完后补 `eval-case`
- 收尾时补 `doc-sync`

## 目录说明

- `fixture/`
  最小样例仓库，包含少量源码、设计令牌和运行日志
- `inputs/`
  教程用到的需求、评审、bug、trace 和文档同步输入
  包括 `requirement-brief.json`、`product-review.json`、`engineering-review.json`
- `expected/`
  关键工件的标准输出，用于教学和测试

## 对应文档

- [端到端教程](../../../docs/tutorials/e2e-walkthrough-端到端教程.md)
- [CLI 参考](../../../docs/reference/cli-reference-CLI参考.md)
- [完整使用手册](../../../docs/guides/usage-guide-完整使用手册.md)
