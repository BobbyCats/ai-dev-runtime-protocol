from __future__ import annotations

from pathlib import Path
from typing import Any

from aidrp.repo_map import rank_candidate_files
from aidrp.utils import now_iso, slugify, tokenize, write_json, write_text
from aidrp.workspace import load_workspace_config


VISUAL_KEYWORDS = {
    "ui",
    "ux",
    "design",
    "theme",
    "component",
    "components",
    "frontend",
    "style",
    "styles",
    "layout",
    "page",
    "screen",
    "token",
    "tokens",
    "tailwind",
}

VISUAL_HINTS_ZH = ("界面", "组件", "主题", "前端", "视觉", "样式", "颜色", "排版", "设计")


def _is_visual_task(title: str, objective: str, scope: list[str], search_terms: list[str]) -> bool:
    tokens = set(tokenize(title, objective, *scope, *search_terms))
    if tokens & VISUAL_KEYWORDS:
        return True
    merged = " ".join([title, objective, *scope, *search_terms])
    return any(keyword in merged for keyword in VISUAL_HINTS_ZH)


def _design_token_files(project_root: Path) -> list[str]:
    design_root = project_root / "design-system"
    if not design_root.exists():
        return []
    candidates = sorted(
        path.relative_to(project_root).as_posix()
        for path in design_root.rglob("*")
        if path.is_file() and path.suffix.lower() in {".json", ".md", ".css", ".ts", ".js"}
    )
    return candidates[:4]


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
    if _is_visual_task(title, objective, scope, search_terms):
        read_order.extend(_design_token_files(project_root))
    read_order.extend(item["path"] for item in candidate_files[: config["context_budget"]["candidate_file_limit"]])
    read_order = list(dict.fromkeys(read_order))
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
        f"# Task Packet | 任务包: {packet['title']}",
        "",
        f"- Task ID | 任务 ID: `{packet['task_id']}`",
        f"- Type | 类型: `{packet['type']}`",
        f"- Generated | 生成时间: `{packet['generated_at']}`",
        "",
        "## Objective | 目标",
        "",
        packet["objective"],
        "",
        "## Scope | 范围",
        "",
    ]
    for item in packet["scope"]:
        lines.append(f"- {item}")

    if packet["non_goals"]:
        lines.extend(["", "## Non-Goals | 不做什么", ""])
        for item in packet["non_goals"]:
            lines.append(f"- {item}")

    lines.extend(["", "## Acceptance Criteria | 验收标准", ""])
    for item in packet["acceptance_criteria"]:
        lines.append(f"- {item}")

    if packet["constraints"]:
        lines.extend(["", "## Constraints | 约束", ""])
        for item in packet["constraints"]:
            lines.append(f"- {item}")

    lines.extend(["", "## Read Order | 阅读顺序", ""])
    for item in packet["read_order"]:
        lines.append(f"- `{item}`")

    lines.extend(["", "## Candidate Files | 候选文件", ""])
    for item in packet["candidate_files"]:
        lines.append(f"- `{item['path']}`: {item['reason']}")

    lines.extend(["", "## Validation Commands | 验证命令", ""])
    for group, values in packet["validation_commands"].items():
        if not values:
            continue
        lines.append(f"- `{group}`: {', '.join(f'`{value}`' for value in values)}")
    return "\n".join(lines) + "\n"


def write_task_packet(packet: dict[str, Any], output_json: Path, output_markdown: Path) -> None:
    write_json(output_json, packet)
    write_text(output_markdown, task_packet_to_markdown(packet))
