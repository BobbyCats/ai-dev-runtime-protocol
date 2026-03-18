# Task Packet: Harden repo map ranking

- Task ID: `harden-repo-map-ranking`
- Type: `refactor`
- Generated: `2026-03-18T05:09:03+00:00`

## Objective

Improve candidate file ranking without expanding scope beyond repo-map logic.

## Scope

- Touch repo-map and ranking logic only.

## Acceptance Criteria

- Repo map still generates JSON and Markdown.
- Candidate ranking remains deterministic.

## Constraints

- Do not add third-party dependencies.

## Read Order

- `AGENTS.md`
- `.aidrp/repo-map.md`
- `src/aidrp/repo_map.py`
- `.aidrp/repo-map.md`
- `src/aidrp/cli.py`
- `src/aidrp/debug_pack.py`
- `templates/task-packet.md`
- `src/aidrp/task_packet.py`
- `AGENTS.md`
- `ONBOARDING.md`
- `README.md`
- `tests/test_runtime_protocol.py`

## Candidate Files

- `src/aidrp/repo_map.py`: Matched tokens: and, candidate, map, repo
- `.aidrp/repo-map.md`: Matched tokens: and, map, repo
- `src/aidrp/cli.py`: Matched tokens: map, repo
- `src/aidrp/debug_pack.py`: Matched tokens: map, repo
- `templates/task-packet.md`: Matched tokens: and, candidate, scope
- `src/aidrp/task_packet.py`: Matched tokens: map, repo
- `AGENTS.md`: Matched tokens: scope
- `ONBOARDING.md`: Matched tokens: only
- `README.md`: Matched tokens: repo
- `tests/test_runtime_protocol.py`: Matched tokens: map, repo

## Validation Commands

- `python`: `aidrp`
