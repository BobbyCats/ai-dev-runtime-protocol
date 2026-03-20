# Repo Map | 仓库地图

- Generated | 生成时间: `2026-03-20T17:48:10+00:00`
- Root | 根目录: `F:\开发思路\ai-dev-runtime-protocol`
- Branch | 分支: `main`
- Dirty | 有未提交改动: `True`

## Summary | 概览

- Files scanned | 扫描文件数: `61`
- Languages | 语言分布: `json:10, markdown:31, python:14, text:4, toml:1, yaml:1`
- Roles | 文件角色: `configuration:2, documentation:18, infrastructure:1, schema:9, source:30, test:1`

## Seed Files | 起始文件

- `AGENTS.md`
- `ONBOARDING.md`
- `README.md`
- `pyproject.toml`
- `src/aidrp/cli.py`
- `src/aidrp/debug_pack.py`
- `src/aidrp/design_token_pack.py`
- `src/aidrp/doc_sync.py`
- `src/aidrp/repo_map.py`
- `src/aidrp/task_packet.py`
- `src/aidrp/utils.py`
- `src/aidrp/workspace.py`

## Commands | 常用命令

- `python`: `aidrp`

## Top Modules | 高信号模块

- `AGENTS.md` (markdown, 32 lines): AGENTS, 工作规则, 验证, 编辑边界
- `ONBOARDING.md` (markdown, 85 lines): Onboarding | 入门说明, 核心转变, 默认工作模型, 这套系统试图防止的坏味道
- `README.md` (markdown, 323 lines): AI Dev Runtime Protocol（AI 开发运行协议）, 这是什么, 这版新增了什么, 中文化原则
- `src/aidrp/cli.py` (python, 312 lines): _path, _project_path, _list, build_parser
- `src/aidrp/debug_pack.py` (python, 168 lines): _collect_recent_commits, _collect_search_hits, build_debug_pack, debug_pack_to_markdown
- `src/aidrp/design_token_pack.py` (python, 295 lines): _normalize_hex, _hex_to_rgb, _rgb_to_hex, _mix
- `src/aidrp/doc_sync.py` (python, 223 lines): _parse_changed_files, _classify_change, _impact_action, build_doc_sync
- `src/aidrp/repo_map.py` (python, 261 lines): _classify_role, _parse_python_symbols, _parse_ts_like, _parse_headings
- `src/aidrp/task_packet.py` (python, 159 lines): _is_visual_task, _design_token_files, build_task_packet, task_packet_to_markdown
- `src/aidrp/utils.py` (python, 262 lines): now_iso, slugify, sha1_text, ensure_parent
- `src/aidrp/workspace.py` (python, 139 lines): workspace_dir, config_path, load_workspace_config, init_workspace
- `src/aidrp/eval_case.py` (python, 56 lines): build_eval_case, eval_case_to_markdown, write_eval_case
- `src/aidrp/requirement_brief.py` (python, 110 lines): build_requirement_brief, requirement_brief_to_markdown, write_requirement_brief
- `examples/README.md` (markdown, 24 lines): Examples | 示例
- `src/aidrp/trace.py` (python, 44 lines): start_trace, append_trace_event
- `adapters/python-fastapi-适配器.md` (markdown, 30 lines): Adapter | 适配器: Python + FastAPI, 推荐的 `.aidrp/config.json` 调整, 常见阅读顺序, 常见风险点
- `adapters/react-node-monorepo-适配器.md` (markdown, 34 lines): Adapter | 适配器: React + Node Monorepo, 推荐的 `.aidrp/config.json` 调整, 常见阅读顺序, 常见风险点
- `pyproject.toml` (toml, 38 lines): configuration
- `templates/debug-pack-排障包.md` (markdown, 31 lines): Debug Pack | 排障包模板, Reproduction Steps | 复现步骤, Triage Read Order | 初步排查阅读顺序, Suspected Files | 疑似文件
- `templates/design-token-pack-设计令牌包.md` (markdown, 41 lines): 设计令牌包（Design Token Pack）, 视觉方向, 基础令牌, 语义令牌
