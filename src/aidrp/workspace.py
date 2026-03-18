from __future__ import annotations

from pathlib import Path
from typing import Any

from aidrp.utils import load_json, write_json, write_text


DEFAULT_CONFIG: dict[str, Any] = {
    "schema_version": "0.1.0",
    "ignore_globs": [],
    "max_file_size_kb": 256,
    "context_budget": {
        "seed_file_limit": 12,
        "candidate_file_limit": 10,
        "hard_file_cap": 24,
        "max_file_chars": 18000,
        "max_snippet_chars": 1200,
    },
    "validation_commands": {
        "quick": [],
        "precommit": [],
        "ship": [],
    },
    "preferred_entry_files": [
        "README.md",
        "AGENTS.md",
        "ONBOARDING.md",
        "package.json",
        "pyproject.toml",
        "apps/web/src/main.tsx",
        "apps/api/src/index.ts",
        "src/main.py",
    ],
    "risk_globs": [
        "migrations/*",
        "infra/*",
        "deploy/*",
        "security/*",
        "auth/*",
        "payments/*",
    ],
}


def workspace_dir(project_root: Path) -> Path:
    return project_root / ".aidrp"


def config_path(project_root: Path) -> Path:
    return workspace_dir(project_root) / "config.json"


def load_workspace_config(project_root: Path) -> dict[str, Any]:
    path = config_path(project_root)
    if not path.exists():
        return DEFAULT_CONFIG.copy()
    data = load_json(path)
    merged = DEFAULT_CONFIG.copy()
    merged.update(data)
    if "context_budget" in data:
        merged["context_budget"] = {**DEFAULT_CONFIG["context_budget"], **data["context_budget"]}
    if "validation_commands" in data:
        merged["validation_commands"] = {
            **DEFAULT_CONFIG["validation_commands"],
            **data["validation_commands"],
        }
    return merged


def init_workspace(project_root: Path, write_agents_template: bool = False) -> list[Path]:
    created: list[Path] = []
    workspace = workspace_dir(project_root)
    for relative in ["tasks", "debug", "evals", "traces", "cache", "artifacts"]:
        path = workspace / relative
        path.mkdir(parents=True, exist_ok=True)
        created.append(path)

    config = config_path(project_root)
    if not config.exists():
        write_json(config, DEFAULT_CONFIG)
        created.append(config)

    ignore_file = project_root / ".aidrpignore"
    if not ignore_file.exists():
        write_text(
            ignore_file,
            "# Paths excluded from repo-map scanning and runtime searches.\n"
            ".git/*\n"
            "node_modules/*\n"
            "dist/*\n"
            "build/*\n"
            ".next/*\n"
            ".turbo/*\n"
            ".venv/*\n"
            "venv/*\n"
            "__pycache__/*\n"
            ".aidrp/cache/*\n",
        )
        created.append(ignore_file)

    if write_agents_template:
        agents = project_root / "AGENTS.md"
        if not agents.exists():
            write_text(
                agents,
                "# AGENTS\n"
                "Read `.aidrp/repo-map.md`, the active task packet in `.aidrp/tasks/`, and the current debug/eval artifacts before broad codebase scans.\n",
            )
            created.append(agents)
    return created
