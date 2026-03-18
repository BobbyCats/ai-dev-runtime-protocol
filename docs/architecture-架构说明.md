# Architecture | 架构说明

`ai-dev-runtime-protocol` 的核心思路是：

不要把聊天上下文当成工程事实来源，而要把关键状态落成可复用工件。

## 三层结构

### 1. Protocol Layer | 协议层

这层负责告诉人和 Agent 应该怎么协作。

- [README.md](../README.md)
- [ONBOARDING.md](../ONBOARDING.md)
- [AGENTS.md](../AGENTS.md)
- [docs/playbooks/bugfix-缺陷修复.md](playbooks/bugfix-缺陷修复.md)
- [docs/playbooks/feature-功能开发.md](playbooks/feature-功能开发.md)

### 2. Artifact Layer | 工件层

这层负责沉淀“当前任务真实需要的上下文”。

- `repo-map` | 仓库地图
- `task-packet` | 任务包
- `debug-pack` | 排障包
- `decision-trace` | 决策轨迹
- `eval-case` | 回归用例

这些工件同时存在 JSON 和 Markdown 两种形态：

- JSON 给程序、Agent、自动化脚本使用
- Markdown 给人快速阅读和 review 使用

### 3. Runtime Layer | 运行层

这层就是 `src/aidrp/` 里的 CLI 和生成逻辑。

它负责：

- 初始化 `.aidrp/`
- 扫描仓库并生成仓库地图
- 生成任务包与排障包
- 写入决策轨迹
- 把 bug 固化成回归用例

## 为什么不是只写 Prompt？

Prompt 能约束表达方式，但很难解决这些问题：

- 上下文重复读取
- bug 排查没有证据链
- 推理中途转向没有留痕
- 线上 bug 修完就忘
- 每次新会话都重新解释项目

所以这里的重点不是“更会提示模型”，而是“给模型一个更稳的运行面”。

## 为什么坚持 JSON First？

因为 JSON 天然适合：

- diff
- 缓存
- 校验
- 传递给其他工具
- 再生成 Markdown 摘要

这会让同一份任务状态可以被 Codex、Claude、Cursor、OpenHands 或你自己的脚本共用。

## 为什么 CLI 要保持很薄？

因为第一版追求的是：

- 可移植
- 可读
- 可补丁
- 低依赖

所以当前实现只用 Python 标准库，不强绑任何模型平台，不强绑任何云服务。

## 未来可以继续补的方向

- 运行时 schema 校验
- 更强的语言级索引
- 从 issue / ticket 自动生成任务包
- 自动把排障包转成回归测试
- 工件新鲜度检查
