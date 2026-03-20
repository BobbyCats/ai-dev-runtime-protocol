from __future__ import annotations

from pathlib import Path
from typing import Any

from aidrp.utils import now_iso, slugify, write_json, write_text


def build_execution_plan(
    *,
    title: str,
    goal: str,
    trigger: str,
    preconditions: list[str],
    steps: list[dict[str, Any]],
    success_exit: str,
    failure_exit: str,
    fallbacks: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "0.1.0",
        "plan_id": slugify(title),
        "generated_at": now_iso(),
        "title": title,
        "goal": goal,
        "trigger": trigger,
        "preconditions": preconditions,
        "steps": steps,
        "success_exit": success_exit,
        "failure_exit": failure_exit,
        "fallbacks": fallbacks,
    }


def execution_plan_to_markdown(plan: dict[str, Any]) -> str:
    lines = [
        f"# Execution Plan | 执行计划: {plan['title']}",
        "",
        f"- Plan ID | 计划 ID: `{plan['plan_id']}`",
        f"- Generated | 生成时间: `{plan['generated_at']}`",
        f"- Goal | 目标: {plan['goal']}",
        f"- Trigger | 触发条件: {plan['trigger'] or 'n/a'}",
        "",
    ]
    if plan["preconditions"]:
        lines.extend(["## Preconditions | 前置条件", ""])
        for item in plan["preconditions"]:
            lines.append(f"- {item}")

    lines.extend(["", "## Steps | 步骤", ""])
    for index, step in enumerate(plan["steps"], start=1):
        lines.append(f"### {index}. {step['name']}")
        lines.append("")
        if step.get("inputs"):
            lines.append(f"- Inputs | 输入: {', '.join(step['inputs'])}")
        if step.get("tools"):
            lines.append(f"- Tools | 工具: {', '.join(step['tools'])}")
        if step.get("outputs"):
            lines.append(f"- Outputs | 输出: {', '.join(step['outputs'])}")
        lines.append(
            f"- Requires Confirmation | 是否需要确认: {'yes' if step.get('requires_confirmation') else 'no'}"
        )
        lines.append("")

    lines.extend(
        [
            "## Exit Conditions | 退出条件",
            "",
            f"- Success | 成功: {plan['success_exit'] or 'n/a'}",
            f"- Failure | 失败: {plan['failure_exit'] or 'n/a'}",
        ]
    )

    if plan["fallbacks"]:
        lines.extend(["", "## Fallback | 降级路径", ""])
        for item in plan["fallbacks"]:
            lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def write_execution_plan(plan: dict[str, Any], output_json: Path, output_markdown: Path) -> None:
    write_json(output_json, plan)
    write_text(output_markdown, execution_plan_to_markdown(plan))
