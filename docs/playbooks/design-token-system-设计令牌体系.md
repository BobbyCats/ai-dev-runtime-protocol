# 设计令牌体系（Design Token System）

适用场景：

- 新产品要定第一版视觉语言
- 现有前端已经开始漂移，不同页面像不同产品
- 要做 Web、App、设计稿三端统一
- 你发现 AI 很会写界面，但每次都写成不一样的一套

## 为什么这一步重要

在 AI 写前端的时代，真正的问题不再是“能不能写出页面”，而是：

- 能不能持续写出同一款产品的页面
- 能不能让设计稿、代码、跨端实现说的是同一种语言
- 能不能在下一次改版时只改令牌，而不是重刷所有组件

`Design Token` 的价值，就是把“视觉感觉”变成“结构化约束”。

## 令牌层次

推荐至少分 4 层：

1. `Brand Direction | 视觉方向`
2. `Primitive Tokens | 基础令牌`
3. `Semantic Tokens | 语义令牌`
4. `Component Guidance | 组件指导`

### 1. 视觉方向

先回答这些问题：

- 这产品是冷静、专业，还是活泼、热烈
- 要强调效率，还是强调情绪感染
- 哪些质感一定不能出现

没有这一步，后面的颜色和字体系都容易漂。

### 2. 基础令牌

这里定义最原始的设计材料：

- 色板
- 间距刻度
- 圆角刻度
- 字体
- 字号
- 阴影
- 动效时长和 easing

这一层可以带颜色名或数值刻度，例如：

- `color.brand.500`
- `spacing.4`
- `radius.lg`

### 3. 语义令牌

这一层最关键。

不要让组件直接使用 `brand.500` 或 `neutral.200`，而是先映射成语义：

- `text.primary`
- `surface.panel`
- `border.subtle`
- `accent.primary`
- `feedback.success`

这样以后品牌色改了，组件不用跟着一处处重写。

### 4. 组件指导

组件层不一定要把每个值都做成独立 token，但至少要说明：

- 这个组件优先用哪些语义令牌
- 这个组件的视觉重点是什么
- 哪些变化不允许随便发生

例如：

- `conversation-bubble`
- `timeline-card`
- `primary-action`
- `input-field`

## 标准顺序

1. 先定视觉方向和非目标
2. 再定基础令牌
3. 再映射语义令牌
4. 再补组件指导
5. 导出到代码和设计工具
6. 用真实页面做一次验收

如果仓库里已经存在 `design-system/` 目录，视觉相关的 `任务包（task-packet）` 应该把这些文件自动排进阅读顺序前列。

## 硬规则

- 组件代码里不要直接写十六进制颜色
- 组件代码里不要随意跳过 spacing / radius / typography 令牌
- 新增令牌前先确认是不是已有令牌表达得不够好，而不是你没想到
- 语义令牌不要绑定具体颜色名
- 令牌一旦影响大量页面，改动后必须走真实验收和文档同步

## CLI 用法

```bash
python -m aidrp design-token-pack \
  --title "AI schedule UI 日程助手界面" \
  --surface "Conversation-first scheduling and expense assistant 对话优先的日程与费用助手" \
  --brand-direction "Calm productivity with strong structure and low visual noise. 冷静、高效、结构感强、低噪音。" \
  --brand-color "#0F766E" \
  --accent-color "#F59E0B"
```

推荐模板：

- [templates/design-token-pack-设计令牌包.md](../../templates/design-token-pack-设计令牌包.md)

## 最终产物应该长什么样

至少要有：

- 一份可读的 Markdown 说明
- 一份可被程序使用的 JSON
- 一套能导出到 CSS Variables / Tailwind / Native 的命名方式

如果没有这些，通常还不算“体系”，只是几条零散的样式决定。
