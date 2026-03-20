from __future__ import annotations

from pathlib import Path
from typing import Any

from aidrp.utils import now_iso, slugify, write_json, write_text


def build_cost_privacy_budget(
    *,
    workflow: str,
    scope: str,
    context_budget: dict[str, Any],
    reasoning_budget: dict[str, Any],
    permission_budget: dict[str, Any],
    data_budget: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "0.1.0",
        "budget_id": slugify(workflow),
        "generated_at": now_iso(),
        "workflow": workflow,
        "scope": scope,
        "context_budget": context_budget,
        "reasoning_budget": reasoning_budget,
        "permission_budget": permission_budget,
        "data_budget": data_budget,
    }


def cost_privacy_budget_to_markdown(budget: dict[str, Any]) -> str:
    lines = [
        f"# Cost & Privacy Budget | 成本权限预算: {budget['workflow']}",
        "",
        f"- Budget ID | 预算 ID: `{budget['budget_id']}`",
        f"- Generated | 生成时间: `{budget['generated_at']}`",
        f"- Scope | 适用范围: {budget['scope'] or 'n/a'}",
        "",
        "## Context Budget | 上下文预算",
        "",
    ]
    for key, value in budget["context_budget"].items():
        lines.append(f"- `{key}`: `{value}`")

    lines.extend(["", "## Reasoning Budget | 推理预算", ""])
    for key, value in budget["reasoning_budget"].items():
        if isinstance(value, list):
            lines.append(f"- `{key}`: {', '.join(str(item) for item in value) or 'n/a'}")
        else:
            lines.append(f"- `{key}`: `{value}`")

    lines.extend(["", "## Permission Budget | 权限预算", ""])
    for key, value in budget["permission_budget"].items():
        if isinstance(value, list):
            lines.append(f"- `{key}`: {', '.join(str(item) for item in value) or 'n/a'}")
        else:
            lines.append(f"- `{key}`: `{value}`")

    lines.extend(["", "## Data Budget | 数据预算", ""])
    for key, value in budget["data_budget"].items():
        if isinstance(value, list):
            lines.append(f"- `{key}`: {', '.join(str(item) for item in value) or 'n/a'}")
        else:
            lines.append(f"- `{key}`: `{value}`")
    return "\n".join(lines) + "\n"


def write_cost_privacy_budget(budget: dict[str, Any], output_json: Path, output_markdown: Path) -> None:
    write_json(output_json, budget)
    write_text(output_markdown, cost_privacy_budget_to_markdown(budget))
