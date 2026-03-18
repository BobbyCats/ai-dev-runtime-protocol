from __future__ import annotations

import argparse
from pathlib import Path

from aidrp.debug_pack import build_debug_pack, write_debug_pack
from aidrp.eval_case import build_eval_case, write_eval_case
from aidrp.repo_map import write_repo_map
from aidrp.task_packet import build_task_packet, write_task_packet
from aidrp.trace import append_trace_event, start_trace
from aidrp.utils import load_json, slugify
from aidrp.workspace import init_workspace


def _path(value: str) -> Path:
    return Path(value).expanduser().resolve()


def _project_path(project_root: Path, value: str) -> Path:
    path = Path(value).expanduser()
    if path.is_absolute():
        return path.resolve()
    return (project_root / path).resolve()


def _list(values: list[str] | None) -> list[str]:
    return [value for value in (values or []) if value]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aidrp", description="AI Dev Runtime Protocol toolkit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_cmd = subparsers.add_parser("init-workspace", help="Create .aidrp workspace scaffolding")
    init_cmd.add_argument("--project-root", default=".")
    init_cmd.add_argument("--write-agents-template", action="store_true")

    repo_cmd = subparsers.add_parser("repo-map", help="Generate repo map JSON and Markdown")
    repo_cmd.add_argument("--project-root", default=".")
    repo_cmd.add_argument("--output-dir", default=".aidrp")

    task_cmd = subparsers.add_parser("task-packet", help="Generate a task packet from a repo map")
    task_cmd.add_argument("--project-root", default=".")
    task_cmd.add_argument("--repo-map", default=".aidrp/repo-map.json")
    task_cmd.add_argument("--title", required=True)
    task_cmd.add_argument("--objective", required=True)
    task_cmd.add_argument("--type", default="feature")
    task_cmd.add_argument("--scope", action="append", default=[])
    task_cmd.add_argument("--non-goal", action="append", default=[])
    task_cmd.add_argument("--acceptance", action="append", default=[])
    task_cmd.add_argument("--constraint", action="append", default=[])
    task_cmd.add_argument("--search-term", action="append", default=[])
    task_cmd.add_argument("--output-dir", default=".aidrp/tasks")

    debug_cmd = subparsers.add_parser("debug-pack", help="Generate a bug triage pack")
    debug_cmd.add_argument("--project-root", default=".")
    debug_cmd.add_argument("--repo-map", default=".aidrp/repo-map.json")
    debug_cmd.add_argument("--title", required=True)
    debug_cmd.add_argument("--symptom", required=True)
    debug_cmd.add_argument("--observed", required=True)
    debug_cmd.add_argument("--expected", required=True)
    debug_cmd.add_argument("--impact", default="Unknown")
    debug_cmd.add_argument("--trace-id", default="")
    debug_cmd.add_argument("--repro-step", action="append", default=[])
    debug_cmd.add_argument("--suspected-file", action="append", default=[])
    debug_cmd.add_argument("--log-file", action="append", default=[])
    debug_cmd.add_argument("--search-term", action="append", default=[])
    debug_cmd.add_argument("--output-dir", default=".aidrp/debug")

    eval_cmd = subparsers.add_parser("eval-case", help="Generate an eval case artifact")
    eval_cmd.add_argument("--title", required=True)
    eval_cmd.add_argument("--origin", required=True)
    eval_cmd.add_argument("--command", dest="runner_command", default="")
    eval_cmd.add_argument("--repro-step", action="append", default=[])
    eval_cmd.add_argument("--assertion", action="append", default=[])
    eval_cmd.add_argument("--tag", action="append", default=[])
    eval_cmd.add_argument("--output-dir", default=".aidrp/evals")

    trace_start_cmd = subparsers.add_parser("trace-start", help="Create a new decision trace file")
    trace_start_cmd.add_argument("--title", required=True)
    trace_start_cmd.add_argument("--task-id", required=True)
    trace_start_cmd.add_argument("--trace-id", default="")
    trace_start_cmd.add_argument("--output-dir", default=".aidrp/traces")

    trace_event_cmd = subparsers.add_parser("trace-event", help="Append an event to a decision trace")
    trace_event_cmd.add_argument("--trace-file", required=True)
    trace_event_cmd.add_argument("--stage", required=True)
    trace_event_cmd.add_argument("--summary", required=True)
    trace_event_cmd.add_argument("--file", action="append", default=[])
    trace_event_cmd.add_argument("--command", dest="shell_commands", action="append", default=[])
    trace_event_cmd.add_argument("--outcome", default="")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "init-workspace":
        project_root = _path(args.project_root)
        created = init_workspace(project_root, write_agents_template=args.write_agents_template)
        for item in created:
            print(item)
        return 0

    if args.command == "repo-map":
        project_root = _path(args.project_root)
        output_dir = _project_path(project_root, args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        write_repo_map(
            project_root,
            output_json=output_dir / "repo-map.json",
            output_markdown=output_dir / "repo-map.md",
        )
        print(output_dir / "repo-map.json")
        print(output_dir / "repo-map.md")
        return 0

    if args.command == "task-packet":
        project_root = _path(args.project_root)
        repo_map = load_json(_project_path(project_root, args.repo_map))
        packet = build_task_packet(
            project_root,
            repo_map,
            title=args.title,
            objective=args.objective,
            task_type=args.type,
            scope=_list(args.scope),
            non_goals=_list(args.non_goal),
            acceptance_criteria=_list(args.acceptance),
            constraints=_list(args.constraint),
            search_terms=_list(args.search_term),
        )
        output_dir = _project_path(project_root, args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        prefix = output_dir / packet["task_id"]
        write_task_packet(packet, prefix.with_suffix(".json"), prefix.with_suffix(".md"))
        print(prefix.with_suffix(".json"))
        print(prefix.with_suffix(".md"))
        return 0

    if args.command == "debug-pack":
        project_root = _path(args.project_root)
        repo_map = load_json(_project_path(project_root, args.repo_map))
        pack = build_debug_pack(
            project_root,
            repo_map,
            title=args.title,
            symptom=args.symptom,
            observed=args.observed,
            expected=args.expected,
            impact=args.impact,
            trace_id=args.trace_id,
            reproduction_steps=_list(args.repro_step),
            suspected_files=_list(args.suspected_file),
            log_files=_list(args.log_file),
            search_terms=_list(args.search_term),
        )
        output_dir = _project_path(project_root, args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        prefix = output_dir / pack["debug_id"]
        write_debug_pack(pack, prefix.with_suffix(".json"), prefix.with_suffix(".md"))
        print(prefix.with_suffix(".json"))
        print(prefix.with_suffix(".md"))
        return 0

    if args.command == "eval-case":
        case = build_eval_case(
            title=args.title,
            origin=args.origin,
            command=args.runner_command,
            reproduction_steps=_list(args.repro_step),
            assertions=_list(args.assertion),
            tags=_list(args.tag),
        )
        output_dir = _path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        prefix = output_dir / case["eval_id"]
        write_eval_case(case, prefix.with_suffix(".json"), prefix.with_suffix(".md"))
        print(prefix.with_suffix(".json"))
        print(prefix.with_suffix(".md"))
        return 0

    if args.command == "trace-start":
        output_dir = _path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        trace_id = args.trace_id or slugify(args.title)
        trace_file = output_dir / f"{trace_id}.json"
        start_trace(trace_file, trace_id=trace_id, task_id=args.task_id, title=args.title)
        print(trace_file)
        return 0

    if args.command == "trace-event":
        trace_file = _path(args.trace_file)
        append_trace_event(
            trace_file,
            stage=args.stage,
            summary=args.summary,
            files=_list(args.file),
            commands=_list(args.shell_commands),
            outcome=args.outcome,
        )
        print(trace_file)
        return 0

    parser.error(f"Unsupported command: {args.command}")
    return 2
