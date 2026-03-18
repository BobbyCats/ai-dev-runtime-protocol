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

    queries = [trace_id, symptom, observed, expected, *search_terms]
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
        "trace_id": trace_id,
        "reproduction_steps": reproduction_steps,
        "triage_read_order": triage_read_order,
        "suspected_files": chosen,
        "evidence": evidence,
        "log_snippets": log_snippets,
        "recent_commits": _collect_recent_commits(project_root),
        "recommended_next_actions": [
            "Reproduce the bug before editing code.",
            "Read only the triage set first; do not expand to broad scans unless evidence is insufficient.",
            "Capture a decision trace for every hypothesis change.",
            "Convert the confirmed bug into an eval case before closing the task.",
        ],
    }


def debug_pack_to_markdown(pack: dict[str, Any]) -> str:
    lines = [
        f"# Debug Pack: {pack['title']}",
        "",
        f"- Debug ID: `{pack['debug_id']}`",
        f"- Trace ID: `{pack['trace_id'] or 'n/a'}`",
        f"- Generated: `{pack['generated_at']}`",
        "",
        "## Failure Summary",
        "",
        f"- Symptom: {pack['symptom']}",
        f"- Observed: {pack['observed']}",
        f"- Expected: {pack['expected']}",
        f"- Impact: {pack['impact']}",
        "",
        "## Reproduction Steps",
        "",
    ]
    for step in pack["reproduction_steps"]:
        lines.append(f"- {step}")

    lines.extend(["", "## Triage Read Order", ""])
    for item in pack["triage_read_order"]:
        lines.append(f"- `{item}`")

    lines.extend(["", "## Suspected Files", ""])
    for item in pack["suspected_files"]:
        lines.append(f"- `{item['path']}`: {item['reason']}")

    if pack["evidence"]:
        lines.extend(["", "## Evidence", ""])
        for item in pack["evidence"]:
            lines.append(f"- `{item['path']}` matched `{item['query']}`: {item['excerpt']}")

    if pack["recent_commits"]:
        lines.extend(["", "## Recent Commits", ""])
        for item in pack["recent_commits"]:
            lines.append(f"- `{item}`")
    return "\n".join(lines) + "\n"


def write_debug_pack(pack: dict[str, Any], output_json: Path, output_markdown: Path) -> None:
    write_json(output_json, pack)
    write_text(output_markdown, debug_pack_to_markdown(pack))
