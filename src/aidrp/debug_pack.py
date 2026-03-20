from __future__ import annotations

from pathlib import Path
from typing import Any

from aidrp.repo_map import rank_candidate_files
from aidrp.utils import compact_excerpt, git_output, now_iso, read_text, slugify, tokenize, write_json, write_text
from aidrp.workspace import load_workspace_config


def _collect_recent_commits(project_root: Path, count: int = 8) -> list[str]:
    output = git_output(project_root, "log", "--oneline", f"-n{count}")
    return [line for line in output.splitlines() if line]


def _collect_search_hits(project_root: Path, repo_map: dict[str, Any], queries: list[str], limit: int) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    lowered_queries = [query for query in queries if query]
    for entry in repo_map["files"]:
        if len(hits) >= limit:
            break
        path = project_root / entry["path"]
        try:
            text = read_text(path, max_chars=24000)
        except OSError:
            continue
        for query in lowered_queries:
            if query.lower() in text.lower():
                hits.append(
                    {
                        "path": entry["path"],
                        "query": query,
                        "excerpt": compact_excerpt(text, query),
                    }
                )
                break
    return hits


def _build_log_focus(
    *,
    trace_id: str,
    request_id: str,
    decision_id: str,
    plan_id: str,
    tool_call_id: str,
    entrypoint: str,
    failure_stage: str,
    log_files: list[str],
    search_terms: list[str],
) -> dict[str, Any]:
    primary_keys = [
        item
        for item in [trace_id, request_id, decision_id, plan_id, tool_call_id]
        if item
    ]
    grep_queries = []
    for label, value in [
        ("trace_id", trace_id),
        ("request_id", request_id),
        ("decision_id", decision_id),
        ("plan_id", plan_id),
        ("tool_call_id", tool_call_id),
        ("entrypoint", entrypoint),
        ("failure_stage", failure_stage),
    ]:
        if value:
            grep_queries.append(f"{label}:{value}")
            grep_queries.append(value)
    grep_queries.extend(item for item in search_terms if item)
    deduped_queries: list[str] = []
    seen = set()
    for query in grep_queries:
        if query not in seen:
            deduped_queries.append(query)
            seen.add(query)

    review_order = []
    if primary_keys:
        review_order.append("先按关联编号搜日志，不要先扫代码。")
    if entrypoint:
        review_order.append(f"先确认入口 `{entrypoint}` 是否真的触发。")
    if failure_stage:
        review_order.append(f"优先检查 `{failure_stage}` 这一阶段前后的日志缺口。")
    if log_files:
        review_order.append("先看提供的日志文件，再扩大到其他模块。")
    review_order.append("只有当日志证据不足时，才扩大代码阅读范围。")

    return {
        "primary_keys": primary_keys,
        "entrypoint": entrypoint,
        "failure_stage": failure_stage,
        "grep_queries": deduped_queries,
        "log_files": log_files[:6],
        "review_order": review_order,
    }


def build_debug_pack(
    project_root: Path,
    repo_map: dict[str, Any],
    *,
    title: str,
    symptom: str,
    observed: str,
    expected: str,
    impact: str,
    trace_id: str,
    request_id: str,
    decision_id: str,
    plan_id: str,
    tool_call_id: str,
    entrypoint: str,
    failure_stage: str,
    reproduction_steps: list[str],
    suspected_files: list[str],
    log_files: list[str],
    search_terms: list[str],
) -> dict[str, Any]:
    config = load_workspace_config(project_root)
    pack_id = slugify(title)
    terms = tokenize(title, symptom, observed, expected, impact, *search_terms)
    ranked = rank_candidate_files(
        repo_map,
        tokens=terms,
        limit=config["context_budget"]["candidate_file_limit"],
    )
    chosen = []
    seen = set()
    for path in suspected_files:
        if path and path not in seen:
            chosen.append({"path": path, "reason": "Provided explicitly by the reporter", "score": 999})
            seen.add(path)
    for item in ranked:
        if item["path"] in seen:
            continue
        chosen.append(item)
        seen.add(item["path"])
        if len(chosen) >= config["context_budget"]["candidate_file_limit"]:
            break

    log_focus = _build_log_focus(
        trace_id=trace_id,
        request_id=request_id,
        decision_id=decision_id,
        plan_id=plan_id,
        tool_call_id=tool_call_id,
        entrypoint=entrypoint,
        failure_stage=failure_stage,
        log_files=log_files,
        search_terms=search_terms,
    )

    queries = [
        trace_id,
        request_id,
        decision_id,
        plan_id,
        tool_call_id,
        entrypoint,
        failure_stage,
        symptom,
        observed,
        expected,
        *search_terms,
    ]
    evidence = _collect_search_hits(project_root, repo_map, queries=queries, limit=12)

    log_snippets = []
    for raw in log_files[:6]:
        path = Path(raw)
        if not path.is_absolute():
            path = project_root / raw
        if not path.exists():
            continue
        text = read_text(path, max_chars=4000)
        needle = trace_id or symptom or observed
        log_snippets.append(
            {
                "path": str(path),
                "excerpt": compact_excerpt(text, needle or text[:120]),
            }
        )

    triage_read_order = ["AGENTS.md", ".aidrp/repo-map.md"]
    triage_read_order.extend(item["path"] for item in chosen[:8])

    return {
        "schema_version": "0.1.0",
        "debug_id": pack_id,
        "generated_at": now_iso(),
        "title": title,
        "symptom": symptom,
        "observed": observed,
        "expected": expected,
        "impact": impact,
        "entrypoint": entrypoint,
        "failure_stage": failure_stage,
        "trace_id": trace_id,
        "correlation_ids": {
            "request_id": request_id,
            "decision_id": decision_id,
            "plan_id": plan_id,
            "tool_call_id": tool_call_id,
        },
        "log_focus": log_focus,
        "reproduction_steps": reproduction_steps,
        "triage_read_order": triage_read_order,
        "suspected_files": chosen,
        "evidence": evidence,
        "log_snippets": log_snippets,
        "recent_commits": _collect_recent_commits(project_root),
        "recommended_next_actions": [
            "Reproduce the bug before editing code.",
            "Search logs and traces by IDs first; do not start from broad symptom scans.",
            "Read only the triage set first; do not expand to broad scans unless evidence is insufficient.",
            "Capture a decision trace for every hypothesis change.",
            "Convert the confirmed bug into an eval case before closing the task.",
        ],
    }


def debug_pack_to_markdown(pack: dict[str, Any]) -> str:
    lines = [
        f"# Debug Pack | 排障包: {pack['title']}",
        "",
        f"- Debug ID | 排障 ID: `{pack['debug_id']}`",
        f"- Trace ID | 追踪 ID: `{pack['trace_id'] or 'n/a'}`",
        f"- Generated | 生成时间: `{pack['generated_at']}`",
        "",
        "## Failure Summary | 问题摘要",
        "",
        f"- Symptom | 症状: {pack['symptom']}",
        f"- Observed | 实际表现: {pack['observed']}",
        f"- Expected | 期望表现: {pack['expected']}",
        f"- Impact | 影响: {pack['impact']}",
        f"- Entrypoint | 入口: {pack['entrypoint'] or 'n/a'}",
        f"- Failure Stage | 故障阶段: {pack['failure_stage'] or 'n/a'}",
        "",
        "## Reproduction Steps | 复现步骤",
        "",
    ]
    for step in pack["reproduction_steps"]:
        lines.append(f"- {step}")

    lines.extend(["", "## Triage Read Order | 初步排查阅读顺序", ""])
    for item in pack["triage_read_order"]:
        lines.append(f"- `{item}`")

    lines.extend(["", "## Suspected Files | 疑似文件", ""])
    for item in pack["suspected_files"]:
        lines.append(f"- `{item['path']}`: {item['reason']}")

    correlation_ids = pack.get("correlation_ids", {})
    lines.extend(["", "## Correlation IDs | 关联编号", ""])
    lines.append(f"- `trace_id`: `{pack['trace_id'] or 'n/a'}`")
    for key in ["request_id", "decision_id", "plan_id", "tool_call_id"]:
        lines.append(f"- `{key}`: `{correlation_ids.get(key) or 'n/a'}`")

    log_focus = pack.get("log_focus", {})
    lines.extend(["", "## Log Focus | 日志聚焦", ""])
    for item in log_focus.get("review_order", []):
        lines.append(f"- {item}")
    if log_focus.get("grep_queries"):
        lines.extend(["", "### Grep Queries | 检索关键词", ""])
        for item in log_focus["grep_queries"]:
            lines.append(f"- `{item}`")

    if pack["evidence"]:
        lines.extend(["", "## Evidence | 证据", ""])
        for item in pack["evidence"]:
            lines.append(f"- `{item['path']}` matched `{item['query']}`: {item['excerpt']}")

    if pack["recent_commits"]:
        lines.extend(["", "## Recent Commits | 最近提交", ""])
        for item in pack["recent_commits"]:
            lines.append(f"- `{item}`")
    return "\n".join(lines) + "\n"


def write_debug_pack(pack: dict[str, Any], output_json: Path, output_markdown: Path) -> None:
    write_json(output_json, pack)
    write_text(output_markdown, debug_pack_to_markdown(pack))
