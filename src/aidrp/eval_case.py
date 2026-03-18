from __future__ import annotations

from pathlib import Path

from aidrp.utils import now_iso, slugify, write_json, write_text


def build_eval_case(
    *,
    title: str,
    origin: str,
    command: str,
    reproduction_steps: list[str],
    assertions: list[str],
    tags: list[str],
) -> dict[str, object]:
    return {
        "schema_version": "0.1.0",
        "eval_id": slugify(title),
        "generated_at": now_iso(),
        "title": title,
        "origin": origin,
        "command": command,
        "reproduction_steps": reproduction_steps,
        "assertions": assertions,
        "tags": tags,
    }


def eval_case_to_markdown(case: dict[str, object]) -> str:
    lines = [
        f"# Eval Case: {case['title']}",
        "",
        f"- Eval ID: `{case['eval_id']}`",
        f"- Origin: `{case['origin']}`",
        f"- Command: `{case['command']}`",
        "",
        "## Reproduction Steps",
        "",
    ]
    for step in case["reproduction_steps"]:
        lines.append(f"- {step}")
    lines.extend(["", "## Assertions", ""])
    for item in case["assertions"]:
        lines.append(f"- {item}")
    if case["tags"]:
        lines.extend(["", "## Tags", ""])
        for tag in case["tags"]:
            lines.append(f"- `{tag}`")
    return "\n".join(lines) + "\n"


def write_eval_case(case: dict[str, object], output_json: Path, output_markdown: Path) -> None:
    write_json(output_json, case)
    write_text(output_markdown, eval_case_to_markdown(case))
