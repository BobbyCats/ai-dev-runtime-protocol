from __future__ import annotations

from pathlib import Path
from typing import Any

from aidrp.utils import now_iso, slugify, write_json, write_text


def build_requirement_brief(
    *,
    title: str,
    product_idea: str,
    target_users: list[str],
    pain_points: list[str],
    desired_outcomes: list[str],
    core_scenarios: list[str],
    non_goals: list[str],
    constraints: list[str],
    success_metrics: list[str],
    open_questions: list[str],
    assumptions: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "0.1.0",
        "brief_id": slugify(title),
        "generated_at": now_iso(),
        "title": title,
        "product_idea": product_idea,
        "target_users": target_users,
        "pain_points": pain_points,
        "desired_outcomes": desired_outcomes,
        "core_scenarios": core_scenarios,
        "non_goals": non_goals,
        "constraints": constraints,
        "success_metrics": success_metrics,
        "open_questions": open_questions,
        "assumptions": assumptions,
        "recommended_next_step": "Run product review first, then engineering review, and only convert to a task-packet after scope is stable. | 先过产品评审和工程评审，范围稳定后再转成 task-packet | 任务包。",
    }


def requirement_brief_to_markdown(brief: dict[str, Any]) -> str:
    lines = [
        f"# Requirement Brief | 需求简报: {brief['title']}",
        "",
        f"- Brief ID | 简报 ID: `{brief['brief_id']}`",
        f"- Generated | 生成时间: `{brief['generated_at']}`",
        "",
        "## Product Idea | 产品想法",
        "",
        brief["product_idea"],
        "",
        "## Target Users | 目标用户",
        "",
    ]
    for item in brief["target_users"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Pain Points | 痛点", ""])
    for item in brief["pain_points"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Desired Outcomes | 期望结果", ""])
    for item in brief["desired_outcomes"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Core Scenarios | 核心场景", ""])
    for item in brief["core_scenarios"]:
        lines.append(f"- {item}")

    if brief["non_goals"]:
        lines.extend(["", "## Non-Goals | 不做什么", ""])
        for item in brief["non_goals"]:
            lines.append(f"- {item}")

    if brief["constraints"]:
        lines.extend(["", "## Constraints | 约束", ""])
        for item in brief["constraints"]:
            lines.append(f"- {item}")

    if brief["success_metrics"]:
        lines.extend(["", "## Success Metrics | 成功标准", ""])
        for item in brief["success_metrics"]:
            lines.append(f"- {item}")

    if brief["open_questions"]:
        lines.extend(["", "## Open Questions | 未决问题", ""])
        for item in brief["open_questions"]:
            lines.append(f"- {item}")

    if brief["assumptions"]:
        lines.extend(["", "## Assumptions | 假设", ""])
        for item in brief["assumptions"]:
            lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Next Step | 下一步",
            "",
            f"- {brief['recommended_next_step']}",
        ]
    )
    return "\n".join(lines) + "\n"


def write_requirement_brief(brief: dict[str, Any], output_json: Path, output_markdown: Path) -> None:
    write_json(output_json, brief)
    write_text(output_markdown, requirement_brief_to_markdown(brief))
