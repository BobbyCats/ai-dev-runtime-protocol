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
    "reasoning_budget": {
        "default_profile": "balanced",
        "upgrade_triggers": [
            "只有证据不足时，才允许扩大上下文或升级推理强度。",
        ],
    },
    "permission_budget": {
        "allowed_tools": [],
        "confirmation_required": [
            "删除",
            "批量修改",
            "外部发送",
        ],
    },
    "data_budget": {
        "log_safe_fields": ["trace_id", "request_id", "decision_id", "plan_id", "tool_call_id"],
        "redact_fields": ["token", "cookie", "password", "secret", "authorization"],
        "forbidden_export_fields": [],
    },
    "observability": {
        "log_globs": ["logs/*.log", "logs/*.txt", "logs/*.jsonl", "*.log", "*.txt", "*.jsonl"],
        "max_log_files": 8,
        "max_log_matches": 24,
        "max_log_line_chars": 240,
        "max_log_file_size_kb": 512,
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
    "documentation": {
        "canonical_docs": [
            "README.md",
            "ONBOARDING.md",
            "AGENTS.md",
            "docs/architecture-架构说明.md",
        ],
        "readme_priority_sections": [
            "这是什么",
            "这版新增了什么",
            "阶段路由",
            "核心工件",
            "文档同步原则",
            "快速开始",
            "默认工作流",
            "仓库结构",
        ],
        "section_rewrite_threshold": 2,
        "full_rewrite_threshold": 3,
    },
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
    if "reasoning_budget" in data:
        merged["reasoning_budget"] = {
            **DEFAULT_CONFIG["reasoning_budget"],
            **data["reasoning_budget"],
        }
    if "permission_budget" in data:
        merged["permission_budget"] = {
            **DEFAULT_CONFIG["permission_budget"],
            **data["permission_budget"],
        }
    if "data_budget" in data:
        merged["data_budget"] = {
            **DEFAULT_CONFIG["data_budget"],
            **data["data_budget"],
        }
    if "observability" in data:
        merged["observability"] = {
            **DEFAULT_CONFIG["observability"],
            **data["observability"],
        }
    if "documentation" in data:
        merged["documentation"] = {
            **DEFAULT_CONFIG["documentation"],
            **data["documentation"],
        }
    return merged


def init_workspace(project_root: Path, write_agents_template: bool = False) -> list[Path]:
    created: list[Path] = []
    workspace = workspace_dir(project_root)
    for relative in [
        "briefs",
        "product-reviews",
        "engineering-reviews",
        "tasks",
        "debug",
        "evals",
        "traces",
        "docsync",
        "cache",
        "artifacts",
        "domains",
        "contracts",
        "plans",
        "correlations",
        "budgets",
    ]:
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
            "# Paths excluded from repo-map scanning and runtime searches. | 仓库地图扫描与运行时检索时忽略这些路径。\n"
            ".git/*\n"
            "node_modules/*\n"
            "dist/*\n"
            "build/*\n"
            ".next/*\n"
            ".turbo/*\n"
            ".aidrp/*\n"
            ".venv/*\n"
            "venv/*\n"
            "__pycache__/*\n"
            "*.egg-info/*\n"
            ".aidrp/cache/*\n",
        )
        created.append(ignore_file)

    if write_agents_template:
        agents = project_root / "AGENTS.md"
        if not agents.exists():
            write_text(
                agents,
                "# AGENTS\n"
                "先读 `.aidrp/repo-map.md`、当前 `.aidrp/tasks/` 下的任务包，以及当前排障/回归工件，再决定是否扩大仓库扫描范围。\n",
            )
            created.append(agents)
    return created
