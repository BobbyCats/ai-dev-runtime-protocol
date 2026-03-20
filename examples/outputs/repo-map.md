# Repo Map | 仓库地图

- Generated | 生成时间: `2026-03-20T18:24:59+00:00`
- Root | 根目录: `F:\开发思路\ai-dev-runtime-protocol`
- Branch | 分支: `main`
- Dirty | 有未提交改动: `True`

## Summary | 概览

- Files scanned | 扫描文件数: `85`
- Languages | 语言分布: `json:15, markdown:44, python:19, text:5, toml:1, yaml:1`
- Roles | 文件角色: `configuration:2, documentation:25, infrastructure:1, schema:14, source:42, test:1`

## Seed Files | 起始文件

- `AGENTS.md`
- `ONBOARDING.md`
- `README.md`
- `pyproject.toml`
- `src/aidrp/cli.py`
- `src/aidrp/debug_pack.py`
- `src/aidrp/design_token_pack.py`
- `src/aidrp/doc_sync.py`
- `src/aidrp/observability_correlation.py`
- `src/aidrp/repo_map.py`
- `src/aidrp/task_packet.py`
- `src/aidrp/utils.py`

## Commands | 常用命令

- `python`: `aidrp`

## Top Modules | 高信号模块

- `AGENTS.md` (markdown, 35 lines): AGENTS, 工作规则, 验证, 编辑边界
- `ONBOARDING.md` (markdown, 98 lines): Onboarding | 入门说明, 核心转变, 默认工作模型, 这套系统试图防止的坏味道
- `README.md` (markdown, 413 lines): AI Dev Runtime Protocol（AI 开发运行协议）, 这是什么, 这版新增了什么, 中文化原则
- `src/aidrp/cli.py` (python, 646 lines): _path, _project_path, _list, _csv
- `src/aidrp/debug_pack.py` (python, 230 lines): _collect_recent_commits, _collect_search_hits, build_debug_pack, debug_pack_to_markdown
- `src/aidrp/design_token_pack.py` (python, 644 lines): _normalize_hex, _hex_to_rgb, _rgb_to_hex, _mix
- `src/aidrp/doc_sync.py` (python, 223 lines): _parse_changed_files, _classify_change, _impact_action, build_doc_sync
- `src/aidrp/observability_correlation.py` (python, 264 lines): _display_path, _resolve_log_paths, _build_queries, _collect_log_matches
- `src/aidrp/repo_map.py` (python, 261 lines): _classify_role, _parse_python_symbols, _parse_ts_like, _parse_headings
- `src/aidrp/task_packet.py` (python, 159 lines): _is_visual_task, _design_token_files, build_task_packet, task_packet_to_markdown
- `src/aidrp/utils.py` (python, 262 lines): now_iso, slugify, sha1_text, ensure_parent
- `src/aidrp/workspace.py` (python, 199 lines): workspace_dir, config_path, load_workspace_config, init_workspace
- `src/aidrp/cost_privacy_budget.py` (python, 71 lines): build_cost_privacy_budget, cost_privacy_budget_to_markdown, write_cost_privacy_budget
- `src/aidrp/domain_map.py` (python, 72 lines): build_domain_map, domain_map_to_markdown, write_domain_map
- `src/aidrp/eval_case.py` (python, 56 lines): build_eval_case, eval_case_to_markdown, write_eval_case
- `src/aidrp/execution_plan.py` (python, 84 lines): build_execution_plan, execution_plan_to_markdown, write_execution_plan
- `src/aidrp/requirement_brief.py` (python, 110 lines): build_requirement_brief, requirement_brief_to_markdown, write_requirement_brief
- `src/aidrp/tool_contract.py` (python, 85 lines): build_tool_contract, tool_contract_to_markdown, write_tool_contract
- `examples/README.md` (markdown, 38 lines): Examples | 示例
- `src/aidrp/trace.py` (python, 44 lines): start_trace, append_trace_event
