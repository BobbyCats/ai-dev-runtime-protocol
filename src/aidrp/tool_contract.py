from __future__ import annotations

from pathlib import Path
from typing import Any

from aidrp.utils import now_iso, slugify, write_json, write_text


def build_tool_contract(
    *,
    tool_name: str,
    domain: str,
    purpose: str,
    inputs: list[dict[str, Any]],
    outputs: list[dict[str, Any]],
    idempotency: str,
    permission_boundary: str,
    retry_policy: str,
    rollback_policy: str,
    failure_codes: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "schema_version": "0.1.0",
        "contract_id": slugify(tool_name),
        "generated_at": now_iso(),
        "tool_name": tool_name,
        "domain": domain,
        "purpose": purpose,
        "inputs": inputs,
        "outputs": outputs,
        "idempotency": idempotency,
        "permission_boundary": permission_boundary,
        "retry_policy": retry_policy,
        "rollback_policy": rollback_policy,
        "failure_codes": failure_codes,
    }


def tool_contract_to_markdown(contract: dict[str, Any]) -> str:
    lines = [
        f"# Tool Contract | 工具契约: {contract['tool_name']}",
        "",
        f"- Contract ID | 契约 ID: `{contract['contract_id']}`",
        f"- Generated | 生成时间: `{contract['generated_at']}`",
        f"- Domain | 所属领域: {contract['domain'] or 'n/a'}",
        "",
        "## Purpose | 用途",
        "",
        contract["purpose"],
        "",
        "## Input | 输入",
        "",
    ]
    for item in contract["inputs"]:
        required = "required" if item.get("required") else "optional"
        lines.append(f"- `{item['name']}` ({item['type']}, {required}): {item['description']}")

    lines.extend(["", "## Output | 输出", ""])
    for item in contract["outputs"]:
        lines.append(f"- `{item['name']}` ({item['type']}): {item['description']}")

    lines.extend(
        [
            "",
            "## Guardrails | 护栏",
            "",
            f"- Idempotency | 幂等规则: {contract['idempotency'] or 'n/a'}",
            f"- Permission Boundary | 权限边界: {contract['permission_boundary'] or 'n/a'}",
            f"- Retry Policy | 重试策略: {contract['retry_policy'] or 'n/a'}",
            f"- Rollback Policy | 回滚策略: {contract['rollback_policy'] or 'n/a'}",
        ]
    )

    if contract["failure_codes"]:
        lines.extend(["", "## Failure Codes | 失败码", ""])
        for item in contract["failure_codes"]:
            lines.append(f"- `{item['code']}`: {item['meaning']} | 调用方处理: {item['caller_action']}")

    return "\n".join(lines) + "\n"


def write_tool_contract(contract: dict[str, Any], output_json: Path, output_markdown: Path) -> None:
    write_json(output_json, contract)
    write_text(output_markdown, tool_contract_to_markdown(contract))
