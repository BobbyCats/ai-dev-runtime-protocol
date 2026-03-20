from __future__ import annotations

from pathlib import Path
from typing import Any

from aidrp.utils import git_output, now_iso, slugify, write_json, write_text
from aidrp.workspace import load_workspace_config


def _parse_changed_files(project_root: Path) -> list[str]:
    output = git_output(project_root, "status", "--porcelain")
    files: list[str] = []
    for line in output.splitlines():
        if len(line) < 4:
            continue
        raw_path = line[3:].strip()
        if " -> " in raw_path:
            raw_path = raw_path.split(" -> ", 1)[1].strip()
        if raw_path and raw_path not in files:
            files.append(raw_path.replace("\\", "/"))
    return files


def _classify_change(path: str) -> set[str]:
    categories: set[str] = set()
    normalized = path.replace("\\", "/")

    if normalized in {"README.md", "ONBOARDING.md", "AGENTS.md"}:
        categories.add("canonical-docs")
    if normalized.startswith("src/aidrp/"):
        categories.add("runtime")
        if normalized.endswith("cli.py") or normalized.endswith("workspace.py"):
            categories.add("workflow-surface")
    if normalized.startswith("schemas/"):
        categories.add("runtime")
        categories.add("workflow-surface")
    if normalized.startswith("templates/"):
        categories.add("workflow-surface")
    if normalized.startswith("docs/playbooks/"):
        categories.add("stage-flow")
        categories.add("workflow-surface")
    if normalized.startswith("docs/reference/") or normalized == "docs/architecture-架构说明.md":
        categories.add("reference")
    if normalized.startswith("adapters/"):
        categories.add("integration")
    if normalized.startswith(".github/") or normalized == "pyproject.toml":
        categories.add("setup")
    if normalized.startswith("tests/"):
        categories.add("verification")
    return categories


def _impact_action(path: str, categories: set[str], strategy: str) -> tuple[str, str]:
    if path == "README.md":
        if strategy == "full-rewrite":
            return "full-rewrite", "命令表面、阶段顺序或系统定位发生了变化，README 应该按当前全貌重写。"
        if strategy == "section-rewrite":
            return "section-rewrite", "变更已经影响多个核心面，README 至少要按章节重写，而不是只加一条补丁说明。"
        return "targeted-update", "需要确认 README 的快速开始、命令或定位描述仍然准确。"
    if path == "ONBOARDING.md":
        if "stage-flow" in categories or "workflow-surface" in categories:
            return "section-rewrite", "默认工作顺序已经变化，入门路径需要同步。"
        return "targeted-update", "确认默认执行顺序和当前工件一致。"
    if path == "AGENTS.md":
        if "stage-flow" in categories or "workflow-surface" in categories:
            return "section-rewrite", "Agent 规则、优先级或禁止项已经变化，需要同步执行纪律。"
        return "targeted-update", "确认 Agent 仍遵守当前工作边界。"
    if path == "docs/architecture-架构说明.md":
        if "runtime" in categories or "stage-flow" in categories:
            return "section-rewrite", "系统层次、阶段分工或工件职责已经变化，架构说明需要重写相关部分。"
        return "targeted-update", "确认架构说明仍能解释当前结构。"
    return "review", "需要人工确认这份文档是否受本次改动影响。"


def build_doc_sync(
    project_root: Path,
    *,
    title: str,
    summary: str,
    changed_files: list[str],
    change_notes: list[str],
) -> dict[str, Any]:
    config = load_workspace_config(project_root)
    normalized_files = [path.replace("\\", "/") for path in changed_files if path]
    if not normalized_files:
        normalized_files = _parse_changed_files(project_root)

    categories: set[str] = set()
    for path in normalized_files:
        categories.update(_classify_change(path))

    thresholds = config["documentation"]
    category_count = len(categories)
    if category_count >= thresholds["full_rewrite_threshold"] or {"runtime", "stage-flow", "workflow-surface"} <= categories:
        readme_strategy = "full-rewrite"
    elif category_count >= thresholds["section_rewrite_threshold"] or {"runtime", "workflow-surface"} <= categories:
        readme_strategy = "section-rewrite"
    else:
        readme_strategy = "targeted-update"

    impacted_docs: list[dict[str, str]] = []
    for path in thresholds["canonical_docs"]:
        action, reason = _impact_action(path, categories, readme_strategy)
        impacted_docs.append({"path": path, "action": action, "reason": reason})

    if "stage-flow" in categories:
        impacted_docs.append(
            {
                "path": "docs/playbooks/stage-router-阶段路由.md",
                "action": "section-rewrite",
                "reason": "阶段流转或阶段门发生变化时，阶段路由必须同步。",
            }
        )
    if "stage-flow" in categories or "verification" in categories:
        impacted_docs.append(
            {
                "path": "docs/playbooks/qa-live-真实验收.md",
                "action": "targeted-update",
                "reason": "验收方式、真实测试路径或证据要求可能受影响。",
            }
        )
    impacted_docs.append(
        {
            "path": "docs/playbooks/documentation-sync-文档同步.md",
            "action": "targeted-update",
            "reason": "确认这次同步策略是否仍符合最新实践。",
        }
    )

    readme_sections = list(thresholds["readme_priority_sections"])
    if "setup" in categories and "安装" not in readme_sections:
        readme_sections.insert(0, "安装")
    if "stage-flow" in categories and "阶段路由" not in readme_sections:
        readme_sections.insert(0, "阶段路由")
    if "integration" in categories and "适配器" not in readme_sections:
        readme_sections.append("适配器")

    sync_order = [
        "README.md",
        "ONBOARDING.md",
        "AGENTS.md",
        "docs/architecture-架构说明.md",
        "docs/playbooks/stage-router-阶段路由.md",
        "docs/playbooks/documentation-sync-文档同步.md",
        "相关 playbook / template / example",
    ]

    done_definition = [
        "README 反映当前系统全貌，而不是只追加变更说明。",
        "默认工作顺序在 README、ONBOARDING、AGENTS 三处保持一致。",
        "新增命令、目录、模板或阶段门已经出现在对应文档里。",
        "如果系统形态变了，README 已按章节重写，必要时整篇重写。",
        "示例、验证命令和术语对照没有停留在旧版本。",
    ]

    return {
        "schema_version": "0.1.0",
        "sync_id": slugify(title),
        "generated_at": now_iso(),
        "title": title,
        "summary": summary,
        "changed_files": normalized_files,
        "change_notes": change_notes,
        "categories": sorted(categories),
        "readme_strategy": readme_strategy,
        "readme_sections": readme_sections,
        "impacted_docs": impacted_docs,
        "sync_order": sync_order,
        "definition_of_done": done_definition,
    }


def doc_sync_to_markdown(pack: dict[str, Any]) -> str:
    lines = [
        f"# Documentation Sync Pack | 文档同步包: {pack['title']}",
        "",
        f"- Sync ID | 同步 ID: `{pack['sync_id']}`",
        f"- Generated | 生成时间: `{pack['generated_at']}`",
        f"- README Strategy | README 策略: `{pack['readme_strategy']}`",
        "",
        "## Change Summary | 变更摘要",
        "",
        pack["summary"],
        "",
        "## Changed Files | 变更文件",
        "",
    ]
    for path in pack["changed_files"]:
        lines.append(f"- `{path}`")

    if pack["change_notes"]:
        lines.extend(["", "## Change Notes | 变更备注", ""])
        for note in pack["change_notes"]:
            lines.append(f"- {note}")

    if pack["categories"]:
        lines.extend(["", "## Categories | 变化类别", ""])
        for category in pack["categories"]:
            lines.append(f"- `{category}`")

    lines.extend(["", "## README Rewrite Scope | README 重写范围", ""])
    for section in pack["readme_sections"]:
        lines.append(f"- {section}")

    lines.extend(["", "## Impacted Docs | 受影响文档", ""])
    for item in pack["impacted_docs"]:
        lines.append(f"- `{item['path']}` [{item['action']}]: {item['reason']}")

    lines.extend(["", "## Sync Order | 同步顺序", ""])
    for item in pack["sync_order"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Definition Of Done | 完成定义", ""])
    for item in pack["definition_of_done"]:
        lines.append(f"- {item}")

    return "\n".join(lines) + "\n"


def write_doc_sync(pack: dict[str, Any], output_json: Path, output_markdown: Path) -> None:
    write_json(output_json, pack)
    write_text(output_markdown, doc_sync_to_markdown(pack))
