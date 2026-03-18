# Debug Pack: CLI import failure on fresh setup

- Debug ID: `cli-import-failure-on-fresh-setup`
- Trace ID: `demo-trace-001`
- Generated: `2026-03-18T05:09:03+00:00`

## Failure Summary

- Symptom: Tests cannot import the package in a cold environment
- Observed: unittest fails with ModuleNotFoundError before install completes
- Expected: tests import the package after installation or with a clear documented invocation order
- Impact: bootstrap workflow becomes misleading

## Reproduction Steps

- Run install and tests in parallel.
- Observe the import error from unittest.

## Triage Read Order

- `AGENTS.md`
- `.aidrp/repo-map.md`
- `tests/test_runtime_protocol.py`
- `.github/workflows/ci.yml`
- `README.md`
- `src/aidrp/cli.py`
- `AGENTS.md`
- `ONBOARDING.md`
- `adapters/python-fastapi.md`
- `adapters/react-node-monorepo.md`

## Suspected Files

- `tests/test_runtime_protocol.py`: Provided explicitly by the reporter
- `.github/workflows/ci.yml`: Provided explicitly by the reporter
- `README.md`: Matched tokens: install, workflow
- `src/aidrp/cli.py`: Matched tokens: cli
- `AGENTS.md`: High-signal documentation file
- `ONBOARDING.md`: High-signal documentation file
- `adapters/python-fastapi.md`: Matched tokens: order
- `adapters/react-node-monorepo.md`: Matched tokens: order
- `src/aidrp/debug_pack.py`: High-signal source file
- `src/aidrp/repo_map.py`: High-signal source file

## Evidence

- `.aidrp/repo-map.json` matched `import`: rs": 1200 } }, "files": [ { "path": ".aidrp/config.json", "language": "json", "role": "configuration", "lines": 36, "symbols": [], "imports": [], "headings": [], "hash": "71aeba148b77", "score": 0 }, { "path": ".aidrpignore", "language": "text", "role": "source", "lin
- `.github/workflows/ci.yml` matched `unittest`: -python@v5 with: python-version: "3.12" - name: Install package run: python -m pip install -e . - name: Run unit tests run: python -m unittest discover -s tests -v - name: Smoke test repo map run: python -m aidrp repo-map --project-root . --output-dir .aidrp
- `adapters/python-fastapi.md` matched `unittest`: web stack. ## Recommended `.aidrp/config.json` Adjustments - Add `src/main.py`, `app/main.py`, and `tests/` to preferred entry files. - Set validation commands around `python -m unittest`, `pytest`, or both. - Add migration and settings files to risk globs. ## Common Read Order 1. `README.md` 2. `AGENTS.md` 3. `pyproject.toml` 4. `src/main.py` or `app/main.py` 5
- `AGENTS.md` matched `unittest`: k before proposing a fix. - When reasoning changes direction, record it in a decision trace. - When a bug is fixed, create or update an eval case. ## Validation - Run `python -m unittest discover -s tests -v` - Run `python -m aidrp repo-map --project-root . --output-dir .aidrp` ## Editing Scope - Keep the toolkit dependency-free at runtime. - Favor JSON artifact
- `README.md` matched `import`: ─ AGENTS.md ├── ONBOARDING.md ├── adapters/ ├── docs/ ├── examples/ ├── schemas/ ├── src/aidrp/ ├── templates/ └── tests/ ``` ## Design Principles - Artifacts over chat history: important state should survive the session. - Read less, decide better: agents should start from packets and repo maps, not whole-repo scans. - Logs need trace IDs: debugging should be e
- `schemas/repo-map.schema.json` matched `import`: "role": { "type": "string" }, "lines": { "type": "integer", "minimum": 0 }, "symbols": { "type": "array", "items": { "type": "string" } }, "imports": { "type": "array", "items": { "type": "string" } }, "headings": { "type": "array", "items": { "type": "string" } }, "hash": { "type": "string" },
- `src/ai_dev_runtime_protocol.egg-info/PKG-INFO` matched `import`: ─ AGENTS.md ├── ONBOARDING.md ├── adapters/ ├── docs/ ├── examples/ ├── schemas/ ├── src/aidrp/ ├── templates/ └── tests/ ``` ## Design Principles - Artifacts over chat history: important state should survive the session. - Read less, decide better: agents should start from packets and repo maps, not whole-repo scans. - Logs need trace IDs: debugging should be e
- `src/aidrp/__main__.py` matched `import`: from aidrp.cli import main if __name__ == "__main__": raise SystemExit(main())
- `src/aidrp/cli.py` matched `import`: from __future__ import annotations import argparse from pathlib import Path from aidrp.debug_pack import build_debug_pack, write_debug_pack from aidrp.eval_case import build_eval_case, write_eval_case
- `src/aidrp/debug_pack.py` matched `import`: from __future__ import annotations from pathlib import Path from typing import Any from aidrp.repo_map import rank_candidate_files from aidrp.utils import compact_excerpt, git_output, now_iso, read_te
- `src/aidrp/eval_case.py` matched `import`: from __future__ import annotations from pathlib import Path from aidrp.utils import now_iso, slugify, write_json, write_text def build_eval_case( *, title: str, origin: str, command:
- `src/aidrp/repo_map.py` matched `import`: from __future__ import annotations import ast import json import re import tomllib from collections import Counter from pathlib import Path from typing import Any from aidrp.utils import ( count_l

## Recent Commits

- `283dc53 Initial commit`
