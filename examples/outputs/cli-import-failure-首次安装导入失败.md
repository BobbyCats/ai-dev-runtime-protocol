# Debug Pack | 排障包: CLI import failure 首次安装导入失败

- Debug ID | 排障 ID: `cli-import-failure-首次安装导入失败`
- Trace ID | 追踪 ID: `demo-trace-001-示例追踪`
- Generated | 生成时间: `2026-03-18T05:29:38+00:00`

## Failure Summary | 问题摘要

- Symptom | 症状: Tests cannot import the package in a cold environment 首次环境中测试无法导入包
- Observed | 实际表现: unittest fails with ModuleNotFoundError before install completes 安装流程不当时 unittest 会报导入错误
- Expected | 期望表现: tests import the package successfully after the documented install flow 按文档流程安装后测试应能正常导入
- Impact | 影响: bootstrap workflow becomes misleading 首次接入体验会被误导

## Reproduction Steps | 复现步骤

- Run install and tests out of order 打乱安装和测试顺序执行
- Observe the import error from unittest 观察导入错误

## Triage Read Order | 初步排查阅读顺序

- `AGENTS.md`
- `.aidrp/repo-map.md`
- `tests/test_runtime_protocol.py`
- `.github/workflows/ci.yml`
- `src/aidrp/cli.py`
- `AGENTS.md`
- `ONBOARDING.md`
- `README.md`
- `src/aidrp/debug_pack.py`
- `src/aidrp/repo_map.py`

## Suspected Files | 疑似文件

- `tests/test_runtime_protocol.py`: Provided explicitly by the reporter
- `.github/workflows/ci.yml`: Provided explicitly by the reporter
- `src/aidrp/cli.py`: Matched tokens: cli
- `AGENTS.md`: High-signal documentation file
- `ONBOARDING.md`: High-signal documentation file
- `README.md`: High-signal documentation file
- `src/aidrp/debug_pack.py`: High-signal source file
- `src/aidrp/repo_map.py`: High-signal source file
- `src/aidrp/utils.py`: High-signal source file
- `src/aidrp/workspace.py`: High-signal source file

## Evidence | 证据

- `.github/workflows/ci.yml` matched `unittest`: -python@v5 with: python-version: "3.12" - name: Install package run: python -m pip install -e . - name: Run unit tests run: python -m unittest discover -s tests -v - name: Smoke test repo map run: python -m aidrp repo-map --project-root . --output-dir .aidrp
- `adapters/python-fastapi-适配器.md` matched `unittest`: n + FastAPI 适用于： - Python 服务 - FastAPI 或类似的 Web 框架 ## 推荐的 `.aidrp/config.json` 调整 - 把 `src/main.py`、`app/main.py`、`tests/` 放进 `preferred_entry_files` - 把 `pytest` 或 `python -m unittest` 写进验证命令 - 把 migration、settings、auth 相关路径放进风险区域 ## 常见阅读顺序 1. `README.md` 2. `AGENTS.md` 3. `pyproject.toml` 4. `src/main.py` 或 `app/main.py` 5. 路由层 6. 服务层 7. 当前任务包里的候选文件 ## 常见风险
- `AGENTS.md` matched `unittest`: idrp/` 工件，而不是直接大范围扫仓库 - 非 trivial 任务先生成 `task-packet | 任务包` - bug 先生成 `debug-pack | 排障包` - 判断方向变了，就写 `decision-trace | 决策轨迹` - 真实 bug 修完后，补 `eval-case | 回归用例` ## 验证 - `python -m unittest discover -s tests -v` - `python -m aidrp repo-map --project-root . --output-dir .aidrp` ## 编辑边界 - 运行时保持无第三方依赖 - 优先 JSON 工件和确定性输出 - 核心逻辑避免绑定特定模型平台
- `README.md` matched `unittest`: t-修复日程删除漂移.json \ --stage investigate \ --summary "Confirmed identity mismatch in delete handler. 已确认删除处理器存在身份标识错配。" \ --file src/schedule/delete.py \ --command "python -m unittest" \ --outcome "Need targeted patch 需要定点修复" ``` ### 6. 修完后生成 `eval-case | 回归用例` ```bash python -m aidrp eval-case \ --title "Regression for schedule deletion drift 日程删除漂移回归用例"
- `schemas/repo-map.schema.json` matched `import`: "role": { "type": "string" }, "lines": { "type": "integer", "minimum": 0 }, "symbols": { "type": "array", "items": { "type": "string" } }, "imports": { "type": "array", "items": { "type": "string" } }, "headings": { "type": "array", "items": { "type": "string" } }, "hash": { "type": "string" },
- `src/aidrp/__main__.py` matched `import`: from aidrp.cli import main if __name__ == "__main__": raise SystemExit(main())
- `src/aidrp/cli.py` matched `import`: from __future__ import annotations import argparse from pathlib import Path from aidrp.debug_pack import build_debug_pack, write_debug_pack from aidrp.eval_case import build_eval_case, write_eval_case
- `src/aidrp/debug_pack.py` matched `import`: from __future__ import annotations from pathlib import Path from typing import Any from aidrp.repo_map import rank_candidate_files from aidrp.utils import compact_excerpt, git_output, now_iso, read_te
- `src/aidrp/eval_case.py` matched `import`: from __future__ import annotations from pathlib import Path from aidrp.utils import now_iso, slugify, write_json, write_text def build_eval_case( *, title: str, origin: str, command:
- `src/aidrp/repo_map.py` matched `import`: from __future__ import annotations import ast import json import re import tomllib from collections import Counter from pathlib import Path from typing import Any from aidrp.utils import ( count_l
- `src/aidrp/task_packet.py` matched `import`: from __future__ import annotations from pathlib import Path from typing import Any from aidrp.repo_map import rank_candidate_files from aidrp.utils import now_iso, slugify, tokenize, write_json, write
- `src/aidrp/trace.py` matched `import`: from __future__ import annotations from pathlib import Path from typing import Any from aidrp.utils import load_json, now_iso, write_json def start_trace(trace_file: Path, *, trace_id: str, task_id:

## Recent Commits | 最近提交

- `d986126 Bootstrap runtime-oriented AI dev protocol`
- `283dc53 Initial commit`
