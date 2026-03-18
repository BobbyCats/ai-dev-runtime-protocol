from __future__ import annotations

from pathlib import Path
from typing import Any

from aidrp.utils import load_json, now_iso, write_json


def start_trace(trace_file: Path, *, trace_id: str, task_id: str, title: str) -> dict[str, Any]:
    trace = {
        "schema_version": "0.1.0",
        "trace_id": trace_id,
        "task_id": task_id,
        "title": title,
        "started_at": now_iso(),
        "events": [],
    }
    write_json(trace_file, trace)
    return trace


def append_trace_event(
    trace_file: Path,
    *,
    stage: str,
    summary: str,
    files: list[str],
    commands: list[str],
    outcome: str,
) -> dict[str, Any]:
    trace = load_json(trace_file)
    trace.setdefault("events", []).append(
        {
            "timestamp": now_iso(),
            "stage": stage,
            "summary": summary,
            "files": files,
            "commands": commands,
            "outcome": outcome,
        }
    )
    write_json(trace_file, trace)
    return trace
