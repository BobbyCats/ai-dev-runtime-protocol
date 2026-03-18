# Task Packet | 任务包: Harden repo map ranking 仓库地图排序加固

- Task ID | 任务 ID: `harden-repo-map-ranking-仓库地图排序加固`
- Type | 类型: `refactor`
- Generated | 生成时间: `2026-03-18T05:29:38+00:00`

## Objective | 目标

Improve candidate file ranking without expanding scope beyond repo-map logic. 在不扩大范围的前提下改进候选文件排序。

## Scope | 范围

- Touch repo-map and ranking logic only. 只改仓库地图与排序逻辑。

## Acceptance Criteria | 验收标准

- Repo map still generates JSON and Markdown. 仓库地图仍能生成 JSON 和 Markdown。
- Candidate ranking remains deterministic. 候选排序必须保持确定性。

## Constraints | 约束

- Do not add third-party dependencies. 不要引入第三方依赖。

## Read Order | 阅读顺序

- `AGENTS.md`
- `.aidrp/repo-map.md`
- `src/aidrp/repo_map.py`
- `README.md`
- `src/aidrp/cli.py`
- `src/aidrp/debug_pack.py`
- `templates/task-packet-任务包.md`
- `src/aidrp/task_packet.py`
- `tests/test_runtime_protocol.py`
- `AGENTS.md`
- `ONBOARDING.md`
- `adapters/react-node-monorepo-适配器.md`

## Candidate Files | 候选文件

- `src/aidrp/repo_map.py`: Matched tokens: and, candidate, map, repo
- `README.md`: Matched tokens: map, repo
- `src/aidrp/cli.py`: Matched tokens: map, repo
- `src/aidrp/debug_pack.py`: Matched tokens: map, repo
- `templates/task-packet-任务包.md`: Matched tokens: and, candidate, scope
- `src/aidrp/task_packet.py`: Matched tokens: map, repo
- `tests/test_runtime_protocol.py`: Matched tokens: map, repo
- `AGENTS.md`: High-signal documentation file
- `ONBOARDING.md`: High-signal documentation file
- `adapters/react-node-monorepo-适配器.md`: Matched tokens: repo

## Validation Commands | 验证命令

- `python`: `aidrp`
