from __future__ import annotations

from pathlib import Path
from typing import Any

from aidrp.repo_map import rank_candidate_files
from aidrp.utils import now_iso, slugify, tokenize, write_json, write_text
from aidrp.workspace import load_workspace_config


def build_task_packet(
    project_root: Path,
    repo_map: dict[str, Any],
    *,
    title: str,
    objective: str,
    task_type: str,
    scope: list[str],
    non_goals: list[str],
    acceptance_criteria: list[str],
    constraints: list[str],
    search_terms: list[str],
) -> dict[str, Any]:
    config = load_workspace_config(project_root)
    task_id = slugify(title)
    tokens = tokenize(title, objective, *scope, *search_terms)
    candidate_files = rank_candidate_files(
        repo_map,
        tokens=tokens,
        limit=config["context_budget"]["candidate_file_limit"],
    )

    read_order = ["AGENTS.md", ".aidrp/repo-map.md"]
    read_order.extend(item["path"] for item in candidate_files[: config["context_budget"]["candidate_file_limit"]])
    validation = {key: value for key, value in config["validation_commands"].items() if value}
    if not validation:
        validation = repo_map["summary"]["commands"]

    return {
        "schema_version": "0.1.0",
        "task_id": task_id,
        "generated_at": now_iso(),
        "title": title,
        "type": task_type,
        "objective": objective,
        "scope": scope,
        "non_goals": non_goals,
        "acceptance_criteria": acceptance_criteria,
        "constraints": constraints,
        "search_terms": search_terms,
        "context_budget": config["context_budget"],
        "read_order": read_order,
        "candidate_files": candidate_files,
        "validation_commands": validation,
        "deliverables": [
            "Code changes scoped to the task",
            "Updated or new tests for changed behavior",
            "Decision trace for major tradeoffs",
            "Follow-up notes for unresolved risks",
        ],
    }


def task_packet_to_markdown(packet: dict[str, Any]) -> str:
    lines = [
        f"# Task Packet: {packet['title']}",
        "",
        f"- Task ID: `{packet['task_id']}`",
        f"- Type: `{packet['type']}`",
        f"- Generated: `{packet['generated_at']}`",
        "",
        "## Objective",
        "",
        packet["objective"],
        "",
        "## Scope",
        "",
    ]
    for item in packet["scope"]:
        lines.append(f"- {item}")

    if packet["non_goals"]:
        lines.extend(["", "## Non-Goals", ""])
        for item in packet["non_goals"]:
            lines.append(f"- {item}")

    lines.extend(["", "## Acceptance Criteria", ""])
    for item in packet["acceptance_criteria"]:
        lines.append(f"- {item}")

    if packet["constraints"]:
        lines.extend(["", "## Constraints", ""])
        for item in packet["constraints"]:
            lines.append(f"- {item}")

    lines.extend(["", "## Read Order", ""])
    for item in packet["read_order"]:
        lines.append(f"- `{item}`")

    lines.extend(["", "## Candidate Files", ""])
    for item in packet["candidate_files"]:
        lines.append(f"- `{item['path']}`: {item['reason']}")

    lines.extend(["", "## Validation Commands", ""])
    for group, values in packet["validation_commands"].items():
        if not values:
            continue
        lines.append(f"- `{group}`: {', '.join(f'`{value}`' for value in values)}")
    return "\n".join(lines) + "\n"


def write_task_packet(packet: dict[str, Any], output_json: Path, output_markdown: Path) -> None:
    write_json(output_json, packet)
    write_text(output_markdown, task_packet_to_markdown(packet))
