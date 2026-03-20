# Architecture | 架构说明

`ai-dev-runtime-protocol` 的核心思路是：

不要把聊天上下文当成工程事实来源，而要把关键状态、阶段门和收尾动作落成可复用协议。

## 四层结构

### 1. Protocol Layer | 协议层

这层负责告诉人和 Agent 应该怎么协作。

- [README.md](../README.md)
- [ONBOARDING.md](../ONBOARDING.md)
- [AGENTS.md](../AGENTS.md)
- [docs/playbooks/stage-router-阶段路由.md](playbooks/stage-router-阶段路由.md)

### 2. Stage Layer | 阶段层

这层负责把“什么时候该做什么”讲清楚，而不是让所有工作都直接坠入实现。

- [docs/playbooks/discovery-interview-需求访谈.md](playbooks/discovery-interview-需求访谈.md)
- [docs/playbooks/plan-product-review-产品评审.md](playbooks/plan-product-review-产品评审.md)
- [docs/playbooks/design-token-system-设计令牌体系.md](playbooks/design-token-system-设计令牌体系.md)
- [docs/playbooks/plan-engineering-review-工程评审.md](playbooks/plan-engineering-review-工程评审.md)
- [docs/playbooks/feature-功能开发.md](playbooks/feature-功能开发.md)
- [docs/playbooks/bugfix-缺陷修复.md](playbooks/bugfix-缺陷修复.md)
- [docs/playbooks/investigate-根因调查.md](playbooks/investigate-根因调查.md)
- [docs/playbooks/qa-live-真实验收.md](playbooks/qa-live-真实验收.md)
- [docs/playbooks/documentation-sync-文档同步.md](playbooks/documentation-sync-文档同步.md)

### 3. Artifact Layer | 工件层

这层负责沉淀“当前任务真实需要的上下文”。

- `repo-map` | 仓库地图
- `requirement-brief` | 需求简报
- `design-token-pack` | 设计令牌包
- `task-packet` | 任务包
- `debug-pack` | 排障包
- `decision-trace` | 决策轨迹
- `eval-case` | 回归用例
- `doc-sync` | 文档同步包

这些工件同时存在 JSON 和 Markdown 两种形态：

- JSON 给程序、Agent、自动化脚本使用
- Markdown 给人快速阅读和 review 使用

### 4. Runtime Layer | 运行层

这层就是 `src/aidrp/` 里的 CLI 和生成逻辑。

它负责：

- 初始化 `.aidrp/`
- 扫描仓库并生成仓库地图
- 生成任务包与排障包
- 写入决策轨迹
- 把 bug 固化成回归用例
- 判断文档该补丁更新还是整篇重写

## 为什么不是只写 Prompt？

Prompt 能约束表达方式，但很难解决这些问题：

- 需求还没收敛就提前开工
- 范围没过评审就直接扩大
- 前端没有设计令牌，AI 每次都重新发明一套视觉风格
- 上下文重复读取
- bug 排查没有根因调查和证据链
- 推理中途转向没有留痕
- 线上 bug 修完就忘
- 单元测试通过却没有真实验收
- 文档逐渐失真，却没人判断该重写还是只补丁更新

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

## 为什么 Design Token 也要进入协议？

因为 AI 写前端最容易出现的不是“写不出来”，而是：

- 同一个产品里颜色、字号、间距不断漂移
- 不同页面像不同产品拼在一起
- 设计稿、Web、App 各用各的命名

把 `design-token-pack` 做成正式工件之后，视觉系统就从“感觉”变成“约束”。

## 为什么要把文档同步做成独立工件？

因为 README 漂移不是“写作问题”，而是工程状态管理问题。

只要系统能力、命令表面或阶段路由变了，README 就不再是“顺手补一句”的问题，而是需要重新表达当前系统全貌。

把 `doc-sync` 做成工件以后，收尾动作就从：

- 想起来就改

变成：

- 必须判断这次是 `targeted-update`、`section-rewrite` 还是 `full-rewrite`

## 未来可以继续补的方向

- 运行时 schema 校验
- 更强的语言级索引
- 从 issue / ticket 自动生成任务包
- 自动把排障包转成回归测试
- 工件新鲜度检查
- QA 结果结构化记录
- 文档漂移自动告警
