# Design Token Pack | 设计令牌包: AI schedule UI 日程助手界面

- Token Pack ID | 令牌包 ID: `ai-schedule-ui-日程助手界面`
- Generated | 生成时间: `2026-03-20T18:01:25+00:00`
- Product Surface | 产品界面: Conversation-first scheduling and expense assistant 对话优先的日程与费用助手

## Brand Direction | 视觉方向

Calm productivity with strong structure and low visual noise. 冷静、高效、结构感强、低噪音。

## Design Principles | 设计原则

- 先定义语义令牌，再写组件，不要在组件里直接写死颜色。
- 同一套令牌要同时约束 Web、App 和设计稿。

## Modes | 模式

- `light`

## Semantic Tokens | 语义令牌

- `surface.canvas` -> `{color.neutral.0}`
- `surface.panel` -> `{color.neutral.50}`
- `surface.panel-elevated` -> `{color.neutral.0}`
- `surface.inverse` -> `{color.neutral.900}`
- `text.primary` -> `{color.neutral.900}`
- `text.secondary` -> `{color.neutral.600}`
- `text.tertiary` -> `{color.neutral.500}`
- `text.inverse` -> `{color.neutral.0}`
- `border.subtle` -> `{color.neutral.200}`
- `border.default` -> `{color.neutral.300}`
- `border.strong` -> `{color.neutral.500}`
- `accent.primary` -> `{color.brand.500}`
- `accent.primary-hover` -> `{color.brand.600}`
- `accent.secondary` -> `{color.accent.500}`
- `accent.on-primary` -> `{color.neutral.0}`
- `feedback.success` -> `{color.success.500}`
- `feedback.warning` -> `{color.warning.500}`
- `feedback.danger` -> `{color.danger.500}`
- `feedback.info` -> `{color.info.500}`
- `focus.ring` -> `{color.brand.300}`

## Component Guidance | 组件指导

- `page-shell`: 页面骨架保持透气，不要用过重阴影和过满填充。标题优先用 display 字体。 Tokens: `surface.canvas`, `text.primary`, `spacing.6`, `spacing.8`
- `conversation-bubble`: AI 产品的对话气质要明确，自己发出的消息和系统回复要有清楚层级，但不要靠花哨颜色取胜。 Tokens: `surface.panel`, `accent.primary`, `text.primary`, `radius.lg`
- `timeline-card`: 时间卡片优先解决扫描效率，状态强调用 semantic token，不直接写业务色。 Tokens: `surface.panel-elevated`, `border.subtle`, `shadow.sm`, `radius.xl`
- `primary-action`: 主操作按钮要稳定，不要在一个页面同时出现多个视觉上等权的主按钮。 Tokens: `accent.primary`, `accent.on-primary`, `radius.pill`, `shadow.sm`
- `input-field`: 输入框优先稳定和可读，不要靠复杂渐变制造存在感。 Tokens: `surface.panel`, `border.default`, `focus.ring`, `text.primary`

## Guardrails | 护栏

- 组件代码里不要直接写十六进制颜色。

## Export Targets | 导出目标

- CSS variables: `:root { --color-accent-primary: ... }`
- Tailwind theme extension or design-tokens.js export
- Native app bridge map for iOS / Android style constants
- Design tool reference table for Figma or Sketch
