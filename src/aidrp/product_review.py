from __future__ import annotations

from pathlib import Path
from typing import Any

from aidrp.utils import now_iso, slugify, write_json, write_text


SCOPE_DECISION_MAP = {
    "扩": "expand",
    "扩展": "expand",
    "expand": "expand",
    "保持": "hold",
    "保": "hold",
    "hold": "hold",
    "shrink": "shrink",
    "缩": "shrink",
    "缩范围": "shrink",
}

SCOPE_DECISION_LABEL = {
    "expand": "扩",
    "hold": "保持",
    "shrink": "缩",
}


def _normalize_scope_decision(value: str) -> str:
    normalized = value.strip().lower()
    if not normalized:
        return ""
    return SCOPE_DECISION_MAP.get(normalized, normalized)


def _recommend_scope_decision(brief: dict[str, Any]) -> tuple[str, str]:
    scenario_count = len(brief.get("core_scenarios", []))
    non_goal_count = len(brief.get("non_goals", []))
    constraint_count = len(brief.get("constraints", []))
    if scenario_count >= 3:
        return "shrink", "核心场景已经超过两个，第一版范围偏大，建议先缩成最先发生的一条主线。"
    if scenario_count >= 2 and non_goal_count == 0:
        return "shrink", "场景已经开始扩散，但没有明确非目标，建议先砍范围。"
    if scenario_count == 1 and (non_goal_count > 0 or constraint_count > 0):
        return "hold", "第一版已经有明确边界，建议先保持范围，把最小切片做稳。"
    return "hold", "需求已具备第一版雏形，先保持范围，避免过早扩张。"


def build_product_review(
    brief: dict[str, Any],
    *,
    current_goal: str,
    core_user: str,
    core_problem: str,
    primary_scenario: str,
    minimum_slice: str,
    non_goals: list[str],
    scope_decision: str,
    scope_reason: str,
    success_signals: list[str],
    expansion_triggers: list[str],
    open_questions: list[str],
    assumptions: list[str],
) -> dict[str, Any]:
    recommended_decision, recommended_reason = _recommend_scope_decision(brief)
    final_decision = _normalize_scope_decision(scope_decision) or recommended_decision
    final_reason = scope_reason or recommended_reason
    review_id = slugify(f"{brief['title']}-product-review")

    resolved_core_user = core_user or (brief.get("target_users") or ["待补充"])[0]
    resolved_core_problem = core_problem or (brief.get("pain_points") or ["待补充"])[0]
    resolved_primary_scenario = primary_scenario or (brief.get("core_scenarios") or ["待补充"])[0]
    resolved_minimum_slice = minimum_slice or (brief.get("desired_outcomes") or ["待补充"])[0]
    resolved_non_goals = non_goals or list(brief.get("non_goals", []))
    resolved_success = success_signals or list(brief.get("success_metrics", []))
    resolved_expansion = expansion_triggers or [
        "当前最小切片已经稳定通过真实验收，且用户重复提出同一扩展需求。",
        "现有第一版已经能稳定指导 task-packet 和实现，不再反复返工。",
    ]
    resolved_open_questions = open_questions or list(brief.get("open_questions", []))
    resolved_assumptions = assumptions or list(brief.get("assumptions", []))
    resolved_goal = current_goal or "把第一版范围压成一个最小有价值切片。"

    return {
        "schema_version": "0.1.0",
        "review_id": review_id,
        "generated_at": now_iso(),
        "title": brief["title"],
        "brief_id": brief["brief_id"],
        "current_goal": resolved_goal,
        "core_user": resolved_core_user,
        "core_problem": resolved_core_problem,
        "primary_scenario": resolved_primary_scenario,
        "minimum_valuable_slice": resolved_minimum_slice,
        "non_goals": resolved_non_goals,
        "scope_decision": final_decision,
        "scope_decision_label": SCOPE_DECISION_LABEL.get(final_decision, final_decision),
        "scope_reason": final_reason,
        "recommended_scope_decision": recommended_decision,
        "recommended_scope_reason": recommended_reason,
        "success_signals": resolved_success,
        "expansion_triggers": resolved_expansion,
        "open_questions": resolved_open_questions,
        "assumptions": resolved_assumptions,
        "recommended_next_step": "进入 engineering-review；如果 scope 决策是 shrink，就先回写 requirement-brief 再继续。",
    }


def product_review_to_markdown(review: dict[str, Any]) -> str:
    lines = [
        f"# Product Review | 产品评审: {review['title']}",
        "",
        f"- Review ID | 评审 ID: `{review['review_id']}`",
        f"- Brief ID | 简报 ID: `{review['brief_id']}`",
        f"- Generated | 生成时间: `{review['generated_at']}`",
        "",
        "## 当前目标 | Current Goal",
        "",
        review["current_goal"],
        "",
        "## 核心用户与问题 | User And Problem",
        "",
        f"- 核心用户: {review['core_user']}",
        f"- 核心问题: {review['core_problem']}",
        f"- 最先发生的场景: {review['primary_scenario']}",
        "",
        "## 第一版切片 | First Slice",
        "",
        f"- 最小有价值切片: {review['minimum_valuable_slice']}",
    ]
    if review["non_goals"]:
        lines.extend(["", "## 非目标 | Non-Goals", ""])
        for item in review["non_goals"]:
            lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Scope 决策 | Scope Decision",
            "",
            f"- 决策: `{review['scope_decision']}` | {review['scope_decision_label']}",
            f"- 决策理由: {review['scope_reason']}",
            f"- 默认推荐: `{review['recommended_scope_decision']}` | {review['recommended_scope_reason']}",
        ]
    )

    if review["success_signals"]:
        lines.extend(["", "## 成功信号 | Success Signals", ""])
        for item in review["success_signals"]:
            lines.append(f"- {item}")

    if review["expansion_triggers"]:
        lines.extend(["", "## 什么时候值得扩 | Expansion Triggers", ""])
        for item in review["expansion_triggers"]:
            lines.append(f"- {item}")

    if review["open_questions"]:
        lines.extend(["", "## 未决问题 | Open Questions", ""])
        for item in review["open_questions"]:
            lines.append(f"- {item}")

    if review["assumptions"]:
        lines.extend(["", "## 假设 | Assumptions", ""])
        for item in review["assumptions"]:
            lines.append(f"- {item}")

    lines.extend(["", "## 下一步 | Next Step", "", f"- {review['recommended_next_step']}"])
    return "\n".join(lines) + "\n"


def write_product_review(review: dict[str, Any], output_json: Path, output_markdown: Path) -> None:
    write_json(output_json, review)
    write_text(output_markdown, product_review_to_markdown(review))
