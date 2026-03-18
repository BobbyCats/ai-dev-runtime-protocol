# Repo Map | 仓库地图

- Generated | 生成时间: `2026-03-18T05:29:27+00:00`
- Root | 根目录: `F:\开发思路\ai-dev-runtime-protocol`
- Branch | 分支: `main`
- Dirty | 有未提交改动: `True`

## Summary | 概览

- Files scanned | 扫描文件数: `39`
- Languages | 语言分布: `json:7, markdown:15, python:11, text:4, toml:1, yaml:1`
- Roles | 文件角色: `configuration:2, documentation:9, infrastructure:1, schema:6, source:20, test:1`

## Seed Files | 起始文件

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

## Commands | 常用命令

- `python`: `aidrp`

## Top Modules | 高信号模块

- `AGENTS.md` (markdown, 24 lines): AGENTS, 工作规则, 验证, 编辑边界
- `ONBOARDING.md` (markdown, 56 lines): Onboarding | 入门说明, 核心转变, 默认工作模型, 这套系统试图防止的坏味道
- `README.md` (markdown, 215 lines): AI Dev Runtime Protocol（AI 开发运行协议）, 这是什么, 解决什么问题, 你会得到什么
- `src/aidrp/cli.py` (python, 208 lines): _path, _project_path, _list, build_parser
- `src/aidrp/debug_pack.py` (python, 168 lines): _collect_recent_commits, _collect_search_hits, build_debug_pack, debug_pack_to_markdown
- `src/aidrp/repo_map.py` (python, 261 lines): _classify_role, _parse_python_symbols, _parse_ts_like, _parse_headings
- `src/aidrp/utils.py` (python, 262 lines): now_iso, slugify, sha1_text, ensure_parent
- `src/aidrp/workspace.py` (python, 114 lines): workspace_dir, config_path, load_workspace_config, init_workspace
- `src/aidrp/eval_case.py` (python, 56 lines): build_eval_case, eval_case_to_markdown, write_eval_case
- `src/aidrp/task_packet.py` (python, 115 lines): build_task_packet, task_packet_to_markdown, write_task_packet
- `examples/README.md` (markdown, 11 lines): Examples | 示例
- `src/aidrp/trace.py` (python, 44 lines): start_trace, append_trace_event
- `adapters/python-fastapi-适配器.md` (markdown, 30 lines): Adapter | 适配器: Python + FastAPI, 推荐的 `.aidrp/config.json` 调整, 常见阅读顺序, 常见风险点
- `adapters/react-node-monorepo-适配器.md` (markdown, 31 lines): Adapter | 适配器: React + Node Monorepo, 推荐的 `.aidrp/config.json` 调整, 常见阅读顺序, 常见风险点
- `pyproject.toml` (toml, 38 lines): configuration
- `templates/debug-pack-排障包.md` (markdown, 31 lines): Debug Pack | 排障包模板, Reproduction Steps | 复现步骤, Triage Read Order | 初步排查阅读顺序, Suspected Files | 疑似文件
- `templates/eval-case-回归用例.md` (markdown, 19 lines): Eval Case | 回归用例模板, Reproduction Steps | 复现步骤, Assertions | 断言, Tags | 标签
- `templates/prompts-提示词.md` (markdown, 18 lines): Prompt Starters | 提示词起手式, Task Packet First | 先任务包, Debug Pack First | 先排障包, Trace Discipline | 轨迹纪律
- `templates/task-packet-任务包.md` (markdown, 38 lines): Task Packet | 任务包模板, Scope | 范围, Non-Goals | 不做什么, Acceptance Criteria | 验收标准
- `tests/test_runtime_protocol.py` (python, 94 lines): RuntimeProtocolTests
