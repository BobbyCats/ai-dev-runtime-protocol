from __future__ import annotations

from pathlib import Path
from typing import Any

from aidrp.repo_map import rank_candidate_files
from aidrp.utils import now_iso, slugify, tokenize, write_json, write_text
from aidrp.workspace import load_workspace_config


REVIEW_DECISION_MAP = {
    "可以开工": "ready",
    "ready": "ready",
    "需要缩范围": "shrink-scope",
    "shrink-scope": "shrink-scope",
    "需要补信息": "needs-info",
    "needs-info": "needs-info",
}

REVIEW_DECISION_LABEL = {
    "ready": "可以开工",
    "shrink-scope": "需要缩范围",
    "needs-info": "需要补信息",
}


def _normalize_review_decision(value: str) -> str:
    normalized = value.strip().lower()
    if not normalized:
        return ""
    return REVIEW_DECISION_MAP.get(normalized, normalized)


def _derive_candidate_files(project_root: Path, repo_map: dict[str, Any], brief: dict[str, Any], product_review: dict[str, Any]) -> list[dict[str, Any]]:
    config = load_workspace_config(project_root)
    tokens = tokenize(
        brief.get("title", ""),
        brief.get("product_idea", ""),
        product_review.get("current_goal", ""),
        product_review.get("core_problem", ""),
        product_review.get("primary_scenario", ""),
        product_review.get("minimum_valuable_slice", ""),
    )
    return rank_candidate_files(repo_map, tokens=tokens, limit=config["context_budget"]["candidate_file_limit"])


def _default_write_boundary(candidate_files: list[dict[str, Any]]) -> list[str]:
    boundary: list[str] = []
    for item in candidate_files:
        if item["role"] != "source":
            continue
        boundary.append(item["path"])
        if len(boundary) >= 3:
            break
    return boundary


def _default_avoid_files(repo_map: dict[str, Any], write_boundary: list[str]) -> list[str]:
    avoid: list[str] = []
    for entry in repo_map["files"]:
        if entry["path"] in write_boundary:
            continue
        if entry["role"] in {"documentation", "infrastructure", "schema"}:
            avoid.append(entry["path"])
        if len(avoid) >= 4:
            break
    return avoid


def _default_state_owner(write_boundary: list[str]) -> str:
    if not write_boundary:
        return "待补充"
    first = Path(write_boundary[0]).stem
    return first


def _default_risks(goal_text: str) -> list[str]:
    lowered = goal_text.lower()
    risks: list[str] = []
    if any(token in lowered for token in ("delete", "remove", "删除")):
        risks.append("选择器、可见顺序或稳定 ID 不一致时，可能删除错误对象。")
    if any(token in lowered for token in ("meeting", "event", "schedule", "会议", "日程")):
        risks.append("展示层和存储层的身份映射一旦漂移，UI 会显示成功但状态实际写错。")
    risks.append("关键编号没有透传到日志时，排障会退化成大范围扫描。")
    return risks


def _default_failure_modes(goal_text: str) -> list[str]:
    lowered = goal_text.lower()
    modes: list[str] = []
    if any(token in lowered for token in ("delete", "remove", "删除")):
        modes.append("删除确认的是 A，但执行器真正删掉的是 B。")
    modes.append("操作完成了，但日志里缺少 trace / decision / plan / tool call 编号。")
    modes.append("代码修通了 happy path，但真实入口仍然复现旧问题。")
    return modes


def _default_observability_points(goal_text: str) -> list[str]:
    points = [
        "在入口、计划确认、执行器三个边界记录 trace_id / decision_id / plan_id / tool_call_id。",
        "日志里同时记录 expected target 和 actual target，避免只看到“成功/失败”而不知道删的是谁。",
    ]
    if any(token in goal_text.lower() for token in ("delete", "remove", "删除")):
        points.append("删除链路必须记录 selection_id、stable_id 和最终写入目标。")
    return points


def _default_validation_commands(repo_map: dict[str, Any]) -> list[str]:
    commands = []
    summary_commands = repo_map.get("summary", {}).get("commands", {})
    for group in ("python", "npm", "make"):
        for command in summary_commands.get(group, []):
            if command not in commands:
                commands.append(command)
    if "python -m unittest discover -s tests -v" not in commands:
        commands.append("python -m unittest discover -s tests -v")
    return commands[:6]


def _recommended_artifacts(brief: dict[str, Any], product_review: dict[str, Any], risks: list[str]) -> list[dict[str, Any]]:
    scenarios = brief.get("core_scenarios", [])
    product_idea = " ".join([brief.get("product_idea", ""), product_review.get("current_goal", "")]).lower()
    recommendations = []
    recommendations.append(
        {
            "artifact": "domain-map",
            "required": len(scenarios) >= 2,
            "reason": "场景开始跨多个业务域时，需要先明确状态归属和编排关系。",
        }
    )
    recommendations.append(
        {
            "artifact": "tool-contract",
            "required": any(token in product_idea for token in ("delete", "create", "update", "tool", "执行", "删除", "创建")),
            "reason": "一旦进入工具调用和执行器阶段，就要明确输入、输出、失败语义和权限边界。",
        }
    )
    recommendations.append(
        {
            "artifact": "execution-plan",
            "required": len(scenarios) >= 2 or any(token in product_idea for token in ("confirm", "batch", "plan", "确认", "批量")),
            "reason": "涉及多步确认或批量动作时，计划与执行分离能显著减少返工和慢循环。",
        }
    )
    recommendations.append(
        {
            "artifact": "observability-correlation",
            "required": any("日志" in item or "编号" in item for item in risks),
            "reason": "只要排障可能依赖编号和日志，就应该尽早接入关联定位。",
        }
    )
    recommendations.append(
        {
            "artifact": "cost-privacy-budget",
            "required": any(token in product_idea for token in ("ai", "agent", "模型", "权限", "token")),
            "reason": "AI 原生产品只要要长期运行，就要提前约束上下文、权限和敏感数据暴露范围。",
        }
    )
    return recommendations


def build_engineering_review(
    project_root: Path,
    repo_map: dict[str, Any],
    brief: dict[str, Any],
    product_review: dict[str, Any],
    *,
    change_goal: str,
    write_boundary: list[str],
    avoid_files: list[str],
    state_owner: str,
    risks: list[str],
    failure_modes: list[str],
    observability_points: list[str],
    validation_commands: list[str],
    live_qa_entry: str,
    rollback_plan: str,
    review_decision: str,
    decision_reason: str,
) -> dict[str, Any]:
    candidate_files = _derive_candidate_files(project_root, repo_map, brief, product_review)
    resolved_write_boundary = write_boundary or _default_write_boundary(candidate_files)
    resolved_avoid_files = avoid_files or _default_avoid_files(repo_map, resolved_write_boundary)
    resolved_state_owner = state_owner or _default_state_owner(resolved_write_boundary)
    resolved_risks = risks or _default_risks(change_goal or product_review.get("current_goal", ""))
    resolved_failure_modes = failure_modes or _default_failure_modes(change_goal or product_review.get("current_goal", ""))
    resolved_observability = observability_points or _default_observability_points(change_goal or product_review.get("current_goal", ""))
    resolved_validation = validation_commands or _default_validation_commands(repo_map)
    resolved_live_qa_entry = live_qa_entry or product_review.get("primary_scenario", "真实入口待补充")
    resolved_rollback = rollback_plan or "如果真实验收或日志编号链路不稳定，就回到上一个可验证版本，并保留这次决策轨迹。"
    resolved_review_decision = _normalize_review_decision(review_decision) or "ready"
    resolved_decision_reason = decision_reason or "改动边界、风险、观察点和验证路径已经明确，可以进入实现。"
    recommendations = _recommended_artifacts(brief, product_review, resolved_risks)

    return {
        "schema_version": "0.1.0",
        "review_id": slugify(f"{brief['title']}-engineering-review"),
        "generated_at": now_iso(),
        "title": brief["title"],
        "brief_id": brief["brief_id"],
        "product_review_id": product_review["review_id"],
        "change_goal": change_goal or product_review.get("current_goal", "待补充"),
        "write_boundary": resolved_write_boundary,
        "avoid_files": resolved_avoid_files,
        "state_owner": resolved_state_owner,
        "candidate_files": candidate_files,
        "risk_points": resolved_risks,
        "failure_modes": resolved_failure_modes,
        "observability_points": resolved_observability,
        "validation_commands": resolved_validation,
        "live_qa_entry": resolved_live_qa_entry,
        "rollback_plan": resolved_rollback,
        "review_decision": resolved_review_decision,
        "review_decision_label": REVIEW_DECISION_LABEL.get(resolved_review_decision, resolved_review_decision),
        "decision_reason": resolved_decision_reason,
        "recommended_artifacts": recommendations,
        "recommended_next_step": "写 task-packet 或 debug-pack；如果评审结论不是 ready，就先缩范围或补信息。",
    }


def engineering_review_to_markdown(review: dict[str, Any]) -> str:
    lines = [
        f"# Engineering Review | 工程评审: {review['title']}",
        "",
        f"- Review ID | 评审 ID: `{review['review_id']}`",
        f"- Brief ID | 简报 ID: `{review['brief_id']}`",
        f"- Product Review ID | 产品评审 ID: `{review['product_review_id']}`",
        f"- Generated | 生成时间: `{review['generated_at']}`",
        "",
        "## 当前改动目标 | Change Goal",
        "",
        review["change_goal"],
        "",
        "## 最小改动边界 | Write Boundary",
        "",
    ]
    for item in review["write_boundary"]:
        lines.append(f"- `{item}`")

    if review["avoid_files"]:
        lines.extend(["", "## 尽量不要动的文件 | Avoid Files", ""])
        for item in review["avoid_files"]:
            lines.append(f"- `{item}`")

    lines.extend(["", "## 状态归属 | State Owner", "", f"- {review['state_owner']}"])

    if review["candidate_files"]:
        lines.extend(["", "## 候选文件 | Candidate Files", ""])
        for item in review["candidate_files"]:
            lines.append(f"- `{item['path']}`: {item['reason']}")

    if review["risk_points"]:
        lines.extend(["", "## 风险点 | Risks", ""])
        for item in review["risk_points"]:
            lines.append(f"- {item}")

    if review["failure_modes"]:
        lines.extend(["", "## 失败模式 | Failure Modes", ""])
        for item in review["failure_modes"]:
            lines.append(f"- {item}")

    if review["observability_points"]:
        lines.extend(["", "## 观察点 | Observability Points", ""])
        for item in review["observability_points"]:
            lines.append(f"- {item}")

    if review["validation_commands"]:
        lines.extend(["", "## 验证命令 | Validation Commands", ""])
        for item in review["validation_commands"]:
            lines.append(f"- `{item}`")

    lines.extend(
        [
            "",
            "## 真实验收入口与止损 | Live QA And Rollback",
            "",
            f"- 真实验收入口: {review['live_qa_entry']}",
            f"- 回滚或止损方案: {review['rollback_plan']}",
            "",
            "## 评审结论 | Review Decision",
            "",
            f"- 结论: `{review['review_decision']}` | {review['review_decision_label']}",
            f"- 原因: {review['decision_reason']}",
        ]
    )

    if review["recommended_artifacts"]:
        lines.extend(["", "## 推荐补哪些高级工件 | Recommended Artifacts", ""])
        for item in review["recommended_artifacts"]:
            marker = "需要" if item["required"] else "可选"
            lines.append(f"- `{item['artifact']}` [{marker}]: {item['reason']}")

    lines.extend(["", "## 下一步 | Next Step", "", f"- {review['recommended_next_step']}"])
    return "\n".join(lines) + "\n"


def write_engineering_review(review: dict[str, Any], output_json: Path, output_markdown: Path) -> None:
    write_json(output_json, review)
    write_text(output_markdown, engineering_review_to_markdown(review))
