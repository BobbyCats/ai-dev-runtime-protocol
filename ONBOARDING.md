# Onboarding | 入门说明

这个仓库不是教你“怎么写更花哨的 Prompt”，而是教你：

怎么把 AI 开发从聊天模式，升级成可控的运行模式。

## 核心转变

从：

- “你先读一下仓库，然后帮我改”

转成：

- “你先根据工件工作，只有证据不足时才扩大上下文”

## 默认工作模型

1. 初始化 `.aidrp/`
2. 生成 `repo-map | 仓库地图`
3. 想法不清楚时，先做 `discovery interview | 需求访谈` 并落成 `requirement-brief | 需求简报`
4. 任务生成 `task-packet | 任务包`，bug 生成 `debug-pack | 排障包`
5. 优先阅读短名单，不要一上来全仓扫描
6. 关键推理变化写入 `decision-trace | 决策轨迹`
7. 被确认的 bug 变成 `eval-case | 回归用例`

## 这套系统试图防止的坏味道

- 一个本地 bug 却要扫整个仓库
- 每次新会话都重新讲架构
- 有日志但没有 trace id，串不起来
- 线上问题修一次，后面还会回来
- 验证命令太慢或者根本没人知道该跑什么

## 必备工件

- `.aidrp/repo-map.json`
- `.aidrp/repo-map.md`
- `.aidrp/briefs/*.json` 与 `*.md`
- `.aidrp/tasks/*.json` 与 `*.md`
- `.aidrp/debug/*.json` 与 `*.md`
- `.aidrp/traces/*.json`
- `.aidrp/evals/*.json` 与 `*.md`

## 集成到其他项目的步骤

1. 安装这个包，或者把核心文件复制过去
2. 运行 `python -m aidrp init-workspace --project-root /path/to/project`
3. 修改 `.aidrp/config.json`
4. 提交 `.aidrpignore`、配置文件和生成后的 `AGENTS.md`
5. 把任务包 / 排障包 生成加入你的日常流程

## 如果你现在只能落三件事

- 固定提交 `repo-map | 仓库地图`
- 想法没收敛前先写 `requirement-brief | 需求简报`
- 修 bug 前必须先写 `debug-pack | 排障包`
- 真实 bug 修完后必须补 `eval-case | 回归用例`
