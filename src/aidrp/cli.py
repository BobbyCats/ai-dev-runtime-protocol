from __future__ import annotations

import argparse
from pathlib import Path

from aidrp.cost_privacy_budget import build_cost_privacy_budget, write_cost_privacy_budget
from aidrp.debug_pack import build_debug_pack, write_debug_pack
from aidrp.design_token_pack import build_design_token_pack, write_design_token_pack
from aidrp.domain_map import build_domain_map, write_domain_map
from aidrp.doc_sync import build_doc_sync, write_doc_sync
from aidrp.eval_case import build_eval_case, write_eval_case
from aidrp.execution_plan import build_execution_plan, write_execution_plan
from aidrp.observability_correlation import (
    build_observability_correlation,
    write_observability_correlation,
)
from aidrp.requirement_brief import build_requirement_brief, write_requirement_brief
from aidrp.repo_map import write_repo_map
from aidrp.task_packet import build_task_packet, write_task_packet
from aidrp.trace import append_trace_event, start_trace
from aidrp.tool_contract import build_tool_contract, write_tool_contract
from aidrp.utils import load_json, slugify
from aidrp.workspace import init_workspace, load_workspace_config


def _path(value: str) -> Path:
    return Path(value).expanduser().resolve()


def _project_path(project_root: Path, value: str) -> Path:
    path = Path(value).expanduser()
    if path.is_absolute():
        return path.resolve()
    return (project_root / path).resolve()


def _list(values: list[str] | None) -> list[str]:
    return [value for value in (values or []) if value]


def _csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _split_spec(value: str, minimum_parts: int, label: str) -> list[str]:
    parts = [item.strip() for item in value.split("|")]
    if len(parts) < minimum_parts:
        raise ValueError(f"{label} 需要至少 {minimum_parts} 段，当前收到: {value}")
    return parts


def _to_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y", "是"}


def _parse_domain_specs(values: list[str]) -> list[dict[str, object]]:
    domains = []
    for value in values:
        parts = _split_spec(value, 3, "domain")
        non_goals = _csv(parts[3]) if len(parts) > 3 else []
        domains.append(
            {
                "name": parts[0],
                "owned_state": _csv(parts[1]),
                "capabilities": _csv(parts[2]),
                "non_goals": non_goals,
            }
        )
    return domains


def _parse_cross_flow_specs(values: list[str]) -> list[dict[str, object]]:
    flows = []
    for value in values:
        parts = _split_spec(value, 4, "cross-flow")
        flows.append(
            {
                "name": parts[0],
                "trigger": parts[1],
                "domains": _csv(parts[2]),
                "owner": parts[3],
            }
        )
    return flows


def _parse_input_field_specs(values: list[str]) -> list[dict[str, object]]:
    fields = []
    for value in values:
        parts = _split_spec(value, 4, "input-field")
        fields.append(
            {
                "name": parts[0],
                "type": parts[1],
                "required": _to_bool(parts[2]),
                "description": parts[3],
            }
        )
    return fields


def _parse_output_field_specs(values: list[str]) -> list[dict[str, str]]:
    fields = []
    for value in values:
        parts = _split_spec(value, 3, "output-field")
        fields.append(
            {
                "name": parts[0],
                "type": parts[1],
                "description": parts[2],
            }
        )
    return fields


def _parse_failure_code_specs(values: list[str]) -> list[dict[str, str]]:
    codes = []
    for value in values:
        parts = _split_spec(value, 3, "failure-code")
        codes.append(
            {
                "code": parts[0],
                "meaning": parts[1],
                "caller_action": parts[2],
            }
        )
    return codes


def _parse_step_specs(values: list[str]) -> list[dict[str, object]]:
    steps = []
    for value in values:
        parts = _split_spec(value, 5, "step")
        steps.append(
            {
                "name": parts[0],
                "inputs": _csv(parts[1]),
                "tools": _csv(parts[2]),
                "outputs": _csv(parts[3]),
                "requires_confirmation": _to_bool(parts[4]),
            }
        )
    return steps


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aidrp", description="AI Dev Runtime Protocol toolkit | AI 开发运行协议工具集")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_cmd = subparsers.add_parser("init-workspace", help="Create .aidrp workspace scaffolding | 初始化工作区")
    init_cmd.add_argument("--project-root", default=".")
    init_cmd.add_argument("--write-agents-template", action="store_true")

    repo_cmd = subparsers.add_parser("repo-map", help="Generate repo map JSON and Markdown | 生成仓库地图")
    repo_cmd.add_argument("--project-root", default=".")
    repo_cmd.add_argument("--output-dir", default=".aidrp")

    brief_cmd = subparsers.add_parser("requirement-brief", help="Generate a requirement brief | 生成需求简报")
    brief_cmd.add_argument("--title", required=True)
    brief_cmd.add_argument("--product-idea", required=True)
    brief_cmd.add_argument("--target-user", action="append", default=[])
    brief_cmd.add_argument("--pain-point", action="append", default=[])
    brief_cmd.add_argument("--desired-outcome", action="append", default=[])
    brief_cmd.add_argument("--scenario", action="append", default=[])
    brief_cmd.add_argument("--non-goal", action="append", default=[])
    brief_cmd.add_argument("--constraint", action="append", default=[])
    brief_cmd.add_argument("--success-metric", action="append", default=[])
    brief_cmd.add_argument("--open-question", action="append", default=[])
    brief_cmd.add_argument("--assumption", action="append", default=[])
    brief_cmd.add_argument("--output-dir", default=".aidrp/briefs")

    domain_cmd = subparsers.add_parser("domain-map", help="Generate a domain map artifact | 生成领域地图")
    domain_cmd.add_argument("--product", required=True)
    domain_cmd.add_argument("--orchestrator", default="")
    domain_cmd.add_argument("--domain", action="append", default=[])
    domain_cmd.add_argument("--shared-infra", action="append", default=[])
    domain_cmd.add_argument("--cross-flow", action="append", default=[])
    domain_cmd.add_argument("--output-dir", default=".aidrp/domains")

    contract_cmd = subparsers.add_parser("tool-contract", help="Generate a tool contract artifact | 生成工具契约")
    contract_cmd.add_argument("--tool-name", required=True)
    contract_cmd.add_argument("--domain", default="")
    contract_cmd.add_argument("--purpose", required=True)
    contract_cmd.add_argument("--input-field", action="append", default=[])
    contract_cmd.add_argument("--output-field", action="append", default=[])
    contract_cmd.add_argument("--idempotency", default="")
    contract_cmd.add_argument("--permission-boundary", default="")
    contract_cmd.add_argument("--retry-policy", default="")
    contract_cmd.add_argument("--rollback-policy", default="")
    contract_cmd.add_argument("--failure-code", action="append", default=[])
    contract_cmd.add_argument("--output-dir", default=".aidrp/contracts")

    plan_cmd = subparsers.add_parser("execution-plan", help="Generate an execution plan artifact | 生成执行计划")
    plan_cmd.add_argument("--title", required=True)
    plan_cmd.add_argument("--goal", required=True)
    plan_cmd.add_argument("--trigger", default="")
    plan_cmd.add_argument("--precondition", action="append", default=[])
    plan_cmd.add_argument("--step", action="append", default=[])
    plan_cmd.add_argument("--success-exit", default="")
    plan_cmd.add_argument("--failure-exit", default="")
    plan_cmd.add_argument("--fallback", action="append", default=[])
    plan_cmd.add_argument("--output-dir", default=".aidrp/plans")

    task_cmd = subparsers.add_parser("task-packet", help="Generate a task packet from a repo map | 生成任务包")
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

    debug_cmd = subparsers.add_parser("debug-pack", help="Generate a bug triage pack | 生成排障包")
    debug_cmd.add_argument("--project-root", default=".")
    debug_cmd.add_argument("--repo-map", default=".aidrp/repo-map.json")
    debug_cmd.add_argument("--title", required=True)
    debug_cmd.add_argument("--symptom", required=True)
    debug_cmd.add_argument("--observed", required=True)
    debug_cmd.add_argument("--expected", required=True)
    debug_cmd.add_argument("--impact", default="Unknown")
    debug_cmd.add_argument("--trace-id", default="")
    debug_cmd.add_argument("--request-id", default="")
    debug_cmd.add_argument("--decision-id", default="")
    debug_cmd.add_argument("--plan-id", default="")
    debug_cmd.add_argument("--tool-call-id", default="")
    debug_cmd.add_argument("--entrypoint", default="")
    debug_cmd.add_argument("--failure-stage", default="")
    debug_cmd.add_argument("--repro-step", action="append", default=[])
    debug_cmd.add_argument("--suspected-file", action="append", default=[])
    debug_cmd.add_argument("--log-file", action="append", default=[])
    debug_cmd.add_argument("--search-term", action="append", default=[])
    debug_cmd.add_argument("--output-dir", default=".aidrp/debug")

    eval_cmd = subparsers.add_parser("eval-case", help="Generate an eval case artifact | 生成回归用例")
    eval_cmd.add_argument("--title", required=True)
    eval_cmd.add_argument("--origin", required=True)
    eval_cmd.add_argument("--command", dest="runner_command", default="")
    eval_cmd.add_argument("--repro-step", action="append", default=[])
    eval_cmd.add_argument("--assertion", action="append", default=[])
    eval_cmd.add_argument("--tag", action="append", default=[])
    eval_cmd.add_argument("--output-dir", default=".aidrp/evals")

    token_cmd = subparsers.add_parser("design-token-pack", help="Generate a design token starter pack | 生成设计令牌包")
    token_cmd.add_argument("--title", required=True)
    token_cmd.add_argument("--surface", required=True)
    token_cmd.add_argument("--brand-direction", required=True)
    token_cmd.add_argument("--brand-color", required=True)
    token_cmd.add_argument("--accent-color", default="#F59E0B")
    token_cmd.add_argument("--canvas-color", default="#F8FAFC")
    token_cmd.add_argument("--text-color", default="#0F172A")
    token_cmd.add_argument("--font-sans", default="IBM Plex Sans, PingFang SC, sans-serif")
    token_cmd.add_argument("--font-display", default="IBM Plex Sans, PingFang SC, sans-serif")
    token_cmd.add_argument("--font-mono", default="JetBrains Mono, SFMono-Regular, monospace")
    token_cmd.add_argument("--design-principle", action="append", default=[])
    token_cmd.add_argument("--mode", action="append", default=[])
    token_cmd.add_argument("--guardrail", action="append", default=[])
    token_cmd.add_argument("--output-dir", default="design-system")

    correlation_cmd = subparsers.add_parser(
        "observability-correlation",
        help="Generate an observability correlation artifact | 生成可观测性关联",
    )
    correlation_cmd.add_argument("--project-root", default=".")
    correlation_cmd.add_argument("--title", required=True)
    correlation_cmd.add_argument("--trace-id", default="")
    correlation_cmd.add_argument("--request-id", default="")
    correlation_cmd.add_argument("--decision-id", default="")
    correlation_cmd.add_argument("--plan-id", default="")
    correlation_cmd.add_argument("--tool-call-id", default="")
    correlation_cmd.add_argument("--entrypoint", default="")
    correlation_cmd.add_argument("--failure-stage", default="")
    correlation_cmd.add_argument("--log-file", action="append", default=[])
    correlation_cmd.add_argument("--search-term", action="append", default=[])
    correlation_cmd.add_argument("--output-dir", default=".aidrp/correlations")

    budget_cmd = subparsers.add_parser(
        "cost-privacy-budget",
        help="Generate a cost and privacy budget artifact | 生成成本权限预算",
    )
    budget_cmd.add_argument("--project-root", default=".")
    budget_cmd.add_argument("--workflow", required=True)
    budget_cmd.add_argument("--scope", default="")
    budget_cmd.add_argument("--max-seed-files", type=int, default=None)
    budget_cmd.add_argument("--max-candidate-files", type=int, default=None)
    budget_cmd.add_argument("--hard-file-cap", type=int, default=None)
    budget_cmd.add_argument("--default-profile", default="")
    budget_cmd.add_argument("--upgrade-trigger", action="append", default=[])
    budget_cmd.add_argument("--allowed-tool", action="append", default=[])
    budget_cmd.add_argument("--confirm-action", action="append", default=[])
    budget_cmd.add_argument("--log-safe-field", action="append", default=[])
    budget_cmd.add_argument("--redact-field", action="append", default=[])
    budget_cmd.add_argument("--forbid-export-field", action="append", default=[])
    budget_cmd.add_argument("--output-dir", default=".aidrp/budgets")

    doc_sync_cmd = subparsers.add_parser("doc-sync", help="Generate a documentation sync pack | 生成文档同步包")
    doc_sync_cmd.add_argument("--project-root", default=".")
    doc_sync_cmd.add_argument("--title", required=True)
    doc_sync_cmd.add_argument("--summary", required=True)
    doc_sync_cmd.add_argument("--changed-file", action="append", default=[])
    doc_sync_cmd.add_argument("--change-note", action="append", default=[])
    doc_sync_cmd.add_argument("--output-dir", default=".aidrp/docsync")

    trace_start_cmd = subparsers.add_parser("trace-start", help="Create a new decision trace file | 创建决策轨迹")
    trace_start_cmd.add_argument("--title", required=True)
    trace_start_cmd.add_argument("--task-id", required=True)
    trace_start_cmd.add_argument("--trace-id", default="")
    trace_start_cmd.add_argument("--output-dir", default=".aidrp/traces")

    trace_event_cmd = subparsers.add_parser("trace-event", help="Append an event to a decision trace | 追加决策事件")
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

    if args.command == "requirement-brief":
        brief = build_requirement_brief(
            title=args.title,
            product_idea=args.product_idea,
            target_users=_list(args.target_user),
            pain_points=_list(args.pain_point),
            desired_outcomes=_list(args.desired_outcome),
            core_scenarios=_list(args.scenario),
            non_goals=_list(args.non_goal),
            constraints=_list(args.constraint),
            success_metrics=_list(args.success_metric),
            open_questions=_list(args.open_question),
            assumptions=_list(args.assumption),
        )
        output_dir = _path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        prefix = output_dir / brief["brief_id"]
        write_requirement_brief(brief, prefix.with_suffix(".json"), prefix.with_suffix(".md"))
        print(prefix.with_suffix(".json"))
        print(prefix.with_suffix(".md"))
        return 0

    if args.command == "domain-map":
        try:
            domain_map = build_domain_map(
                product=args.product,
                orchestrator=args.orchestrator,
                domains=_parse_domain_specs(_list(args.domain)),
                shared_infrastructure=_list(args.shared_infra),
                cross_domain_flows=_parse_cross_flow_specs(_list(args.cross_flow)),
            )
        except ValueError as exc:
            parser.error(str(exc))
        output_dir = _path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        prefix = output_dir / domain_map["domain_map_id"]
        write_domain_map(domain_map, prefix.with_suffix(".json"), prefix.with_suffix(".md"))
        print(prefix.with_suffix(".json"))
        print(prefix.with_suffix(".md"))
        return 0

    if args.command == "tool-contract":
        try:
            contract = build_tool_contract(
                tool_name=args.tool_name,
                domain=args.domain,
                purpose=args.purpose,
                inputs=_parse_input_field_specs(_list(args.input_field)),
                outputs=_parse_output_field_specs(_list(args.output_field)),
                idempotency=args.idempotency,
                permission_boundary=args.permission_boundary,
                retry_policy=args.retry_policy,
                rollback_policy=args.rollback_policy,
                failure_codes=_parse_failure_code_specs(_list(args.failure_code)),
            )
        except ValueError as exc:
            parser.error(str(exc))
        output_dir = _path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        prefix = output_dir / contract["contract_id"]
        write_tool_contract(contract, prefix.with_suffix(".json"), prefix.with_suffix(".md"))
        print(prefix.with_suffix(".json"))
        print(prefix.with_suffix(".md"))
        return 0

    if args.command == "execution-plan":
        try:
            plan = build_execution_plan(
                title=args.title,
                goal=args.goal,
                trigger=args.trigger,
                preconditions=_list(args.precondition),
                steps=_parse_step_specs(_list(args.step)),
                success_exit=args.success_exit,
                failure_exit=args.failure_exit,
                fallbacks=_list(args.fallback),
            )
        except ValueError as exc:
            parser.error(str(exc))
        output_dir = _path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        prefix = output_dir / plan["plan_id"]
        write_execution_plan(plan, prefix.with_suffix(".json"), prefix.with_suffix(".md"))
        print(prefix.with_suffix(".json"))
        print(prefix.with_suffix(".md"))
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
            request_id=args.request_id,
            decision_id=args.decision_id,
            plan_id=args.plan_id,
            tool_call_id=args.tool_call_id,
            entrypoint=args.entrypoint,
            failure_stage=args.failure_stage,
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

    if args.command == "design-token-pack":
        pack = build_design_token_pack(
            title=args.title,
            product_surface=args.surface,
            brand_direction=args.brand_direction,
            brand_color=args.brand_color,
            accent_color=args.accent_color,
            canvas_color=args.canvas_color,
            text_color=args.text_color,
            font_sans=args.font_sans,
            font_display=args.font_display,
            font_mono=args.font_mono,
            design_principles=_list(args.design_principle),
            modes=_list(args.mode),
            guardrails=_list(args.guardrail),
        )
        output_dir = _path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        prefix = output_dir / pack["token_pack_id"]
        write_design_token_pack(
            pack,
            prefix.with_suffix(".json"),
            prefix.with_suffix(".md"),
            prefix.with_suffix(".html"),
        )
        print(prefix.with_suffix(".json"))
        print(prefix.with_suffix(".md"))
        print(prefix.with_suffix(".html"))
        return 0

    if args.command == "observability-correlation":
        project_root = _path(args.project_root)
        correlation = build_observability_correlation(
            project_root,
            title=args.title,
            trace_id=args.trace_id,
            request_id=args.request_id,
            decision_id=args.decision_id,
            plan_id=args.plan_id,
            tool_call_id=args.tool_call_id,
            entrypoint=args.entrypoint,
            failure_stage=args.failure_stage,
            log_files=_list(args.log_file),
            search_terms=_list(args.search_term),
        )
        output_dir = _project_path(project_root, args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        prefix = output_dir / correlation["correlation_id"]
        write_observability_correlation(correlation, prefix.with_suffix(".json"), prefix.with_suffix(".md"))
        print(prefix.with_suffix(".json"))
        print(prefix.with_suffix(".md"))
        return 0

    if args.command == "cost-privacy-budget":
        project_root = _path(args.project_root)
        config = load_workspace_config(project_root)
        context_budget = dict(config["context_budget"])
        if args.max_seed_files is not None:
            context_budget["seed_file_limit"] = args.max_seed_files
        if args.max_candidate_files is not None:
            context_budget["candidate_file_limit"] = args.max_candidate_files
        if args.hard_file_cap is not None:
            context_budget["hard_file_cap"] = args.hard_file_cap

        reasoning_budget = dict(config.get("reasoning_budget", {}))
        if args.default_profile:
            reasoning_budget["default_profile"] = args.default_profile
        if _list(args.upgrade_trigger):
            reasoning_budget["upgrade_triggers"] = _list(args.upgrade_trigger)

        permission_budget = dict(config.get("permission_budget", {}))
        if _list(args.allowed_tool):
            permission_budget["allowed_tools"] = _list(args.allowed_tool)
        if _list(args.confirm_action):
            permission_budget["confirmation_required"] = _list(args.confirm_action)

        data_budget = dict(config.get("data_budget", {}))
        if _list(args.log_safe_field):
            data_budget["log_safe_fields"] = _list(args.log_safe_field)
        if _list(args.redact_field):
            data_budget["redact_fields"] = _list(args.redact_field)
        if _list(args.forbid_export_field):
            data_budget["forbidden_export_fields"] = _list(args.forbid_export_field)

        budget = build_cost_privacy_budget(
            workflow=args.workflow,
            scope=args.scope,
            context_budget=context_budget,
            reasoning_budget=reasoning_budget,
            permission_budget=permission_budget,
            data_budget=data_budget,
        )
        output_dir = _project_path(project_root, args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        prefix = output_dir / budget["budget_id"]
        write_cost_privacy_budget(budget, prefix.with_suffix(".json"), prefix.with_suffix(".md"))
        print(prefix.with_suffix(".json"))
        print(prefix.with_suffix(".md"))
        return 0

    if args.command == "doc-sync":
        project_root = _path(args.project_root)
        pack = build_doc_sync(
            project_root,
            title=args.title,
            summary=args.summary,
            changed_files=_list(args.changed_file),
            change_notes=_list(args.change_note),
        )
        output_dir = _project_path(project_root, args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        prefix = output_dir / pack["sync_id"]
        write_doc_sync(pack, prefix.with_suffix(".json"), prefix.with_suffix(".md"))
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
