from __future__ import annotations

from pathlib import Path
from typing import Any

from aidrp.utils import now_iso, slugify, write_json, write_text


def build_domain_map(
    *,
    product: str,
    orchestrator: str,
    domains: list[dict[str, Any]],
    shared_infrastructure: list[str],
    cross_domain_flows: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "schema_version": "0.1.0",
        "domain_map_id": slugify(product),
        "generated_at": now_iso(),
        "product": product,
        "orchestrator": orchestrator,
        "domains": domains,
        "shared_infrastructure": shared_infrastructure,
        "cross_domain_flows": cross_domain_flows,
    }


def domain_map_to_markdown(domain_map: dict[str, Any]) -> str:
    lines = [
        f"# Domain Map | 领域地图: {domain_map['product']}",
        "",
        f"- Domain Map ID | 领域地图 ID: `{domain_map['domain_map_id']}`",
        f"- Generated | 生成时间: `{domain_map['generated_at']}`",
        f"- Orchestrator | 编排层: {domain_map['orchestrator'] or 'n/a'}",
        "",
        "## Domains | 业务域",
        "",
    ]
    for item in domain_map["domains"]:
        lines.append(f"### {item['name']}")
        lines.append("")
        lines.append("- Owned State | 拥有状态")
        for state in item.get("owned_state", []):
            lines.append(f"  - {state}")
        lines.append("- Capabilities | 核心能力")
        for capability in item.get("capabilities", []):
            lines.append(f"  - {capability}")
        if item.get("non_goals"):
            lines.append("- Non-Goals | 不负责什么")
            for entry in item["non_goals"]:
                lines.append(f"  - {entry}")
        lines.append("")

    if domain_map["shared_infrastructure"]:
        lines.extend(["## Shared Infrastructure | 共享基础设施", ""])
        for item in domain_map["shared_infrastructure"]:
            lines.append(f"- {item}")

    if domain_map["cross_domain_flows"]:
        lines.extend(["", "## Cross-Domain Flows | 跨域流程", ""])
        for item in domain_map["cross_domain_flows"]:
            lines.append(
                f"- `{item['name']}`: 发起方 `{item['trigger']}`，涉及 `{', '.join(item.get('domains', []))}`，结果归属 `{item['owner']}`"
            )
    return "\n".join(lines) + "\n"


def write_domain_map(domain_map: dict[str, Any], output_json: Path, output_markdown: Path) -> None:
    write_json(output_json, domain_map)
    write_text(output_markdown, domain_map_to_markdown(domain_map))
