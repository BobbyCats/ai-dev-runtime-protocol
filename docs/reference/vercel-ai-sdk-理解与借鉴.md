# Vercel AI SDK | 理解与借鉴

这份文档回答三个问题：

- `Vercel AI SDK` 到底是什么
- 为什么王自如会把大量时间花在这一层
- 我们这套协议应该从里面借什么，不该机械照搬什么

## 它到底是什么

`Vercel AI SDK` 本质上是一套面向 TypeScript 的 AI 应用与 Agent 开发工具箱。

按照官方文档的划分，它至少有两条主干：

- `AI SDK Core`：统一文本生成、结构化输出、工具调用和 Agent 构建
- `AI SDK UI`：帮助你快速做聊天界面和生成式 UI

对王自如那种产品来说，它重要不是因为“能调模型”，而是因为它处在整个 AI 产品的腰部：

- 上面接模型
- 中间接 Agent 循环与上下文管理
- 下面接工具、结构化输出和前端流式交互

一旦这一层设计不好，后面几乎所有问题都会被放大：

- 工具调用会乱
- 上下文会失控
- 结构化输出会漂
- UI 渲染和后端状态会脱节
- 日志和调试会很难接

## 为什么王自如会把大量时间花在这里

如果回到你整理的 [王自如-AI辅助编程实践分享.md](/F:/开发思路/王自如-AI辅助编程实践分享.md)，他最看重的并不是“换哪个模型”，而是下面这些运行层问题：

- 多工具调用和循环推理怎么组织
- 跨业务域编排怎么拆
- 批量操作怎么避免 ReAct 一步一步太慢
- 结构化计划怎么生成、怎么确认、怎么执行
- 工具怎么保持简单，不变成黑盒
- 出错后怎么快速定位，而不是每次全仓搜索

也就是说，他花时间最多的地方，其实是：

**Agent 的运行框架，而不是业务字段本身。**

这正是 `Vercel AI SDK` 这种库擅长覆盖的层：

- 工具循环
- 上下文管理
- 停止条件
- 结构化输出
- 流式交互
- 生命周期观测能力

但要注意一件事：

它能提供的是“运行底座”，不是“产品判断”。

王自如真正投入时间的部分，不只是会用 SDK，而是把它调成适合自己业务的形状。

## 它最重要的 6 个能力

### 1. 统一模型与 Provider 接口

如果你直接面向不同模型厂商写，最容易出现：

- 接口不统一
- 切模型成本高
- 同一能力在不同厂商下适配代码很散

这类 SDK 的价值，就是把“模型差异”吸收到统一接口后面。

### 2. 工具调用与工具循环

Agent 不是“调用一次模型”就结束，而是：

- 理解输入
- 决定下一步
- 调工具
- 读取结果
- 再决定下一步

这一层如果自己从零写，很容易写出一堆难维护的循环控制代码。

### 3. 结构化输出

王自如的视频里最核心的一点，是把自然语言需求压成结构化计划。

没有稳定的结构化输出能力，后面的：

- 计划确认
- 数据库存储
- GUI 呈现
- 工具执行

都会非常脆弱。

### 4. 上下文管理与循环控制

真正的难点不是“怎么让模型多看点上下文”，而是“怎么控制它每一步只看该看的东西”。

这一层对你现在最有借鉴价值，因为你一直碰到：

- Claude 改一个 bug 要扫很多文件
- token 越来越大
- 任务做到一半开始漂

### 5. 流式 UI / 生成式 UI

王自如的产品本质上就是：

- LUI 在前
- 结构化状态在后
- GUI 负责展示和确认

这种产品天然需要一个“后端 Agent 结果如何稳定推到前端”的层。

### 6. 生命周期观测

如果 SDK 能天然接 telemetry、callback、devtools，它就更容易成为生产系统的一部分，而不只是 demo。

## 从官方文档看，它为什么重要

官方文档现在把它定义成一套帮助开发者构建 AI 应用和 Agent 的 TypeScript 工具箱，并强调它的目标是统一不同模型提供方的接入方式，减少你花在底层对接细节上的时间。

官方文档也明确把 `AI SDK Core` 定义成统一文本、结构化对象、工具调用和 Agent 构建的 API，把 `AI SDK UI` 定义成快速构建聊天与生成式 UI 的 hooks 集合。

在 Agent 部分，官方把 Agent 拆成三部分：

- LLM 决定下一步
- Tool 扩展能力
- Loop 负责上下文管理和停止条件

这和王自如的讲法是高度对齐的，只是表达方式不同。

更关键的是，官方还明确说：

- `ToolLoopAgent` 适合一般 Agent 场景
- 对复杂、可重复、需要显式控制流的工作流，应使用更结构化的 workflow pattern

这正好对应王自如从：

- 纯意图解析
- 到纯 ReAct
- 再到 Plan-then-Execute

这一轮架构演进。

## 我们真正该借的，不是“用这个库”

我们现在这个仓库是：

- Python 标准库实现
- CLI 优先
- 不强绑任何模型厂商
- 不强绑某个前端框架

所以我们不应该机械地把 `Vercel AI SDK` 当依赖搬进来。

我们真正该借的，是它的方法骨架：

- 统一的工具契约
- 稳定的结构化输出
- 明确的循环控制
- 上下文预算和工具可用范围控制
- 生命周期观测
- 前后端之间稳定的数据流

## 它和我们当前协议的对应关系

### 它偏运行时

更接近：

- `tool-contract`
- `execution-plan`
- `observability-correlation`
- `cost-privacy-budget`

### 我们偏运行协议

更接近：

- `requirement-brief`
- `repo-map`
- `task-packet`
- `debug-pack`
- `eval-case`
- `doc-sync`

一句话说：

`Vercel AI SDK` 更像“Agent 引擎层”，  
`ai-dev-runtime-protocol` 更像“Agent 开发治理层 + 上下文压缩层 + 排障闭环层”。

## 它对我们最有帮助的地方

### 1. 帮我们确认一件事

真正值钱的不是多写几个 prompt，而是：

- 工具怎么组织
- 循环怎么控制
- 上下文怎么裁剪
- 输出怎么结构化
- 观测怎么接进去

### 2. 帮我们校正一个误区

不是“让 Agent 自由检索更多文件”就更高级，  
而是“让 Agent 在每一步只看到最有用的信息”才更高级。

### 3. 帮我们补强未来方向

如果你后面真要做 TypeScript / Next.js 的 AI 原生产品，这套 SDK 会很有参考价值，尤其是：

- 聊天界面
- 工具调用
- 结构化计划输出
- 流式 UI
- 调试观测接入

## 它不能替你解决什么

下面这些，SDK 本身不替你做：

- 产品要不要砍 scope
- 业务域怎么拆
- 哪些工具必须幂等
- 哪些动作必须二次确认
- 线上 bug 到底归类成什么回归用例
- README 是补丁更新还是整篇重写

这些正是我们这套协议要补上的部分。

## 我们接下来怎么吸收它的精华

不是“把仓库改成 TypeScript”，而是继续强化这些方向：

- `tool-contract` 更贴近真实工具循环
- `execution-plan` 更贴近计划与执行分离
- `observability-correlation` 更贴近 Agent 生命周期
- `cost-privacy-budget` 更贴近上下文与权限控制
- 未来可以加一层 TypeScript / Vercel 适配示例，但不绑死在它上面

## 参考链接

- AI SDK 介绍：[https://ai-sdk.dev/docs/introduction](https://ai-sdk.dev/docs/introduction)
- Agents 概览：[https://ai-sdk.dev/docs/agents/overview](https://ai-sdk.dev/docs/agents/overview)
- Loop Control：[https://ai-sdk.dev/docs/agents/loop-control](https://ai-sdk.dev/docs/agents/loop-control)
- Tool Calling：[https://ai-sdk.dev/docs/ai-sdk-core/tools-and-tool-calling](https://ai-sdk.dev/docs/ai-sdk-core/tools-and-tool-calling)
- Structured Data：[https://ai-sdk.dev/docs/ai-sdk-core/generating-structured-data](https://ai-sdk.dev/docs/ai-sdk-core/generating-structured-data)
- Telemetry：[https://ai-sdk.dev/docs/ai-sdk-core/telemetry](https://ai-sdk.dev/docs/ai-sdk-core/telemetry)
