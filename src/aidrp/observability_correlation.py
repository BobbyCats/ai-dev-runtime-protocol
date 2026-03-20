from __future__ import annotations

import fnmatch
from pathlib import Path
from typing import Any

from aidrp.utils import iter_repo_files, now_iso, relative_path, slugify, write_json, write_text
from aidrp.workspace import load_workspace_config


DEFAULT_LOG_GLOBS = ["logs/*.log", "logs/*.txt", "logs/*.jsonl", "*.log", "*.txt", "*.jsonl"]


def _display_path(path: Path, project_root: Path) -> str:
    try:
        return relative_path(path, project_root)
    except ValueError:
        return str(path)


def _resolve_log_paths(project_root: Path, log_files: list[str]) -> list[Path]:
    config = load_workspace_config(project_root)
    max_log_files = config.get("observability", {}).get("max_log_files", 8)
    max_file_size_kb = config.get("observability", {}).get("max_log_file_size_kb", config["max_file_size_kb"])

    resolved: list[Path] = []
    seen = set()
    for raw in log_files:
        path = Path(raw)
        if not path.is_absolute():
            path = (project_root / raw).resolve()
        if path.exists() and path.is_file():
            marker = str(path).lower()
            if marker not in seen:
                resolved.append(path)
                seen.add(marker)
        if len(resolved) >= max_log_files:
            return resolved

    patterns = config.get("observability", {}).get("log_globs", DEFAULT_LOG_GLOBS)
    for path in iter_repo_files(project_root, max_file_size_kb=max_file_size_kb):
        rel = _display_path(path, project_root)
        if not any(fnmatch.fnmatch(rel, pattern.replace("\\", "/")) for pattern in patterns):
            continue
        marker = str(path).lower()
        if marker in seen:
            continue
        resolved.append(path)
        seen.add(marker)
        if len(resolved) >= max_log_files:
            break
    return resolved


def _build_queries(
    *,
    trace_id: str,
    request_id: str,
    decision_id: str,
    plan_id: str,
    tool_call_id: str,
    entrypoint: str,
    failure_stage: str,
    search_terms: list[str],
) -> list[str]:
    queries: list[str] = []
    for label, value in [
        ("trace_id", trace_id),
        ("request_id", request_id),
        ("decision_id", decision_id),
        ("plan_id", plan_id),
        ("tool_call_id", tool_call_id),
        ("entrypoint", entrypoint),
        ("failure_stage", failure_stage),
    ]:
        if not value:
            continue
        queries.append(f"{label}:{value}")
        queries.append(value)
    queries.extend(item for item in search_terms if item)

    deduped: list[str] = []
    seen = set()
    for item in queries:
        normalized = item.strip()
        if not normalized or normalized in seen:
            continue
        deduped.append(normalized)
        seen.add(normalized)
    return deduped


def _collect_log_matches(project_root: Path, log_paths: list[Path], queries: list[str]) -> tuple[list[dict[str, Any]], list[str]]:
    config = load_workspace_config(project_root)
    max_matches = config.get("observability", {}).get("max_log_matches", 24)
    max_line_chars = config.get("observability", {}).get("max_log_line_chars", 240)
    matches: list[dict[str, Any]] = []
    matched_queries: set[str] = set()

    lowered_queries = [(query, query.lower()) for query in queries]
    for path in log_paths:
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for line_number, line in enumerate(lines, start=1):
            lowered_line = line.lower()
            line_matches: list[str] = []
            for original, lowered in lowered_queries:
                if lowered in lowered_line:
                    line_matches.append(original)
                    matched_queries.add(original)
            if line_matches:
                matches.append(
                    {
                        "path": _display_path(path, project_root),
                        "line": line_number,
                        "query": line_matches[0],
                        "matched_queries": line_matches,
                        "excerpt": line.strip()[:max_line_chars],
                    }
                )
            if len(matches) >= max_matches:
                break
        if len(matches) >= max_matches:
            break
    missing = [query for query in queries if query not in matched_queries]
    return matches, missing


def build_observability_correlation(
    project_root: Path,
    *,
    title: str,
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
    log_paths = _resolve_log_paths(project_root, log_files)
    grep_queries = _build_queries(
        trace_id=trace_id,
        request_id=request_id,
        decision_id=decision_id,
        plan_id=plan_id,
        tool_call_id=tool_call_id,
        entrypoint=entrypoint,
        failure_stage=failure_stage,
        search_terms=search_terms,
    )
    matched_entries, missing_queries = _collect_log_matches(project_root, log_paths, grep_queries)

    review_order = []
    if grep_queries:
        review_order.append("先按关联编号 grep 日志，再决定是否看代码。")
    if failure_stage:
        review_order.append(f"优先检查 `{failure_stage}` 阶段前后的日志连续性。")
    if entrypoint:
        review_order.append(f"先确认入口 `{entrypoint}` 是否真的被触发。")
    if not matched_entries:
        review_order.append("当前日志里还没有命中结果，先确认日志路径和埋点是否完整。")
    elif missing_queries:
        review_order.append("部分关键编号没有命中，优先补齐缺失埋点或确认编号是否真实透传。")
    review_order.append("只有日志证据不足时，才扩大到代码级搜索。")

    failure_signature: list[str] = []
    if entrypoint:
        if f"entrypoint:{entrypoint}" in missing_queries and entrypoint in missing_queries:
            failure_signature.append(f"入口 `{entrypoint}` 可能没有被触发，或者入口日志没有透传出来。")
        else:
            failure_signature.append(f"入口 `{entrypoint}` 已有日志，可继续向下缩到故障阶段。")
    if failure_stage:
        if f"failure_stage:{failure_stage}" in missing_queries and failure_stage in missing_queries:
            failure_signature.append(f"故障阶段 `{failure_stage}` 缺少直接日志，需要确认阶段边界和埋点。")
        else:
            failure_signature.append(f"故障阶段 `{failure_stage}` 已有日志，可继续比对前后阶段差异。")
    if missing_queries:
        failure_signature.append("部分关键编号仍有缺口，优先补齐透传链路或埋点，再扩大代码搜索。")
    else:
        failure_signature.append("关键编号已经能串起来，优先比较计划、工具调用和状态写入的差异。")

    return {
        "schema_version": "0.1.0",
        "correlation_id": slugify(title),
        "generated_at": now_iso(),
        "title": title,
        "trace_id": trace_id,
        "request_id": request_id,
        "decision_id": decision_id,
        "plan_id": plan_id,
        "tool_call_id": tool_call_id,
        "entrypoint": entrypoint,
        "failure_stage": failure_stage,
        "log_files": [_display_path(path, project_root) for path in log_paths],
        "grep_queries": grep_queries,
        "matched_entries": matched_entries,
        "missing_queries": missing_queries,
        "review_order": review_order,
        "failure_signature": failure_signature,
    }


def observability_correlation_to_markdown(correlation: dict[str, Any]) -> str:
    lines = [
        f"# Observability Correlation | 可观测性关联: {correlation['title']}",
        "",
        f"- Correlation ID | 关联 ID: `{correlation['correlation_id']}`",
        f"- Generated | 生成时间: `{correlation['generated_at']}`",
        "",
        "## Correlation Keys | 关联编号",
        "",
        f"- `trace_id`: `{correlation['trace_id'] or 'n/a'}`",
        f"- `request_id`: `{correlation['request_id'] or 'n/a'}`",
        f"- `decision_id`: `{correlation['decision_id'] or 'n/a'}`",
        f"- `plan_id`: `{correlation['plan_id'] or 'n/a'}`",
        f"- `tool_call_id`: `{correlation['tool_call_id'] or 'n/a'}`",
        f"- `entrypoint`: `{correlation['entrypoint'] or 'n/a'}`",
        f"- `failure_stage`: `{correlation['failure_stage'] or 'n/a'}`",
        "",
        "## Log Files | 日志文件",
        "",
    ]
    for item in correlation["log_files"]:
        lines.append(f"- `{item}`")

    lines.extend(["", "## Grep Queries | 检索关键词", ""])
    for item in correlation["grep_queries"]:
        lines.append(f"- `{item}`")

    lines.extend(["", "## Review Order | 排查顺序", ""])
    for item in correlation["review_order"]:
        lines.append(f"- {item}")

    if correlation["matched_entries"]:
        lines.extend(["", "## Matched Entries | 命中日志", ""])
        for item in correlation["matched_entries"]:
            queries = ", ".join(f"`{query}`" for query in item.get("matched_queries", [item["query"]]))
            lines.append(f"- `{item['path']}:{item['line']}` matched {queries}: {item['excerpt']}")

    if correlation["missing_queries"]:
        lines.extend(["", "## Missing Queries | 未命中关键词", ""])
        for item in correlation["missing_queries"]:
            lines.append(f"- `{item}`")

    lines.extend(["", "## Failure Signature | 故障签名", ""])
    for item in correlation["failure_signature"]:
        if item:
            lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def write_observability_correlation(
    correlation: dict[str, Any],
    output_json: Path,
    output_markdown: Path,
) -> None:
    write_json(output_json, correlation)
    write_text(output_markdown, observability_correlation_to_markdown(correlation))
