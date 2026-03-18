# Repo Map

- Generated: `2026-03-18T05:08:15+00:00`
- Root: `F:\开发思路\ai-dev-runtime-protocol`
- Branch: `main`
- Dirty: `True`

## Summary

- Files scanned: `46`
- Languages: `json:9, markdown:15, python:11, text:9, toml:1, yaml:1`
- Roles: `configuration:4, documentation:8, infrastructure:1, schema:6, source:26, test:1`

## Seed Files

- `AGENTS.md`
- `ONBOARDING.md`
- `README.md`
- `pyproject.toml`
- `src/aidrp/cli.py`
- `src/aidrp/debug_pack.py`
- `src/aidrp/repo_map.py`
- `src/aidrp/utils.py`
- `src/aidrp/workspace.py`
- `src/aidrp/eval_case.py`
- `src/aidrp/task_packet.py`
- `examples/README.md`

## Commands

- `python`: `aidrp`

## Top Modules

- `AGENTS.md` (markdown, 24 lines): AGENTS, Working Rules, Validation, Editing Scope
- `ONBOARDING.md` (markdown, 54 lines): Onboarding, The Core Shift, Default Operating Model, Red Flags This Toolkit Is Meant To Prevent
- `README.md` (markdown, 180 lines): AI Dev Runtime Protocol, Why This Exists, What You Get, Install
- `src/aidrp/cli.py` (python, 201 lines): _path, _list, build_parser, main
- `src/aidrp/debug_pack.py` (python, 168 lines): _collect_recent_commits, _collect_search_hits, build_debug_pack, debug_pack_to_markdown
- `src/aidrp/repo_map.py` (python, 261 lines): _classify_role, _parse_python_symbols, _parse_ts_like, _parse_headings
- `src/aidrp/utils.py` (python, 256 lines): now_iso, slugify, sha1_text, ensure_parent
- `src/aidrp/workspace.py` (python, 112 lines): workspace_dir, config_path, load_workspace_config, init_workspace
- `src/aidrp/eval_case.py` (python, 56 lines): build_eval_case, eval_case_to_markdown, write_eval_case
- `src/aidrp/task_packet.py` (python, 115 lines): build_task_packet, task_packet_to_markdown, write_task_packet
- `examples/README.md` (markdown, 11 lines): Examples
- `src/aidrp/trace.py` (python, 44 lines): start_trace, append_trace_event
- `.aidrp/repo-map.md` (markdown, 55 lines): Repo Map, Summary, Seed Files, Commands
- `adapters/python-fastapi.md` (markdown, 27 lines): Adapter: Python + FastAPI, Recommended `.aidrp/config.json` Adjustments, Common Read Order, Common Risk Areas
- `adapters/react-node-monorepo.md` (markdown, 27 lines): Adapter: React + Node Monorepo, Recommended `.aidrp/config.json` Adjustments, Common Read Order, Common Risk Areas
- `pyproject.toml` (toml, 38 lines): configuration
- `templates/debug-pack.md` (markdown, 31 lines): Debug Pack Template, Reproduction Steps, Triage Read Order, Suspected Files
- `templates/eval-case.md` (markdown, 19 lines): Eval Case Template, Reproduction Steps, Assertions, Tags
- `templates/prompts.md` (markdown, 18 lines): Prompt Starters, Task Packet First, Debug Pack First, Trace Discipline
- `templates/task-packet.md` (markdown, 38 lines): Task Packet Template, Scope, Non-Goals, Acceptance Criteria
