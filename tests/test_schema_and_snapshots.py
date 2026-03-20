from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from aidrp.cli import build_parser
from aidrp.cost_privacy_budget import build_cost_privacy_budget
from aidrp.debug_pack import build_debug_pack
from aidrp.design_token_pack import build_design_token_pack, design_token_pack_to_html
from aidrp.doc_sync import build_doc_sync, doc_sync_to_markdown
from aidrp.domain_map import build_domain_map
from aidrp.engineering_review import build_engineering_review, engineering_review_to_markdown
from aidrp.eval_case import build_eval_case
from aidrp.execution_plan import build_execution_plan
from aidrp.observability_correlation import build_observability_correlation, observability_correlation_to_markdown
from aidrp.product_review import build_product_review, product_review_to_markdown
from aidrp.repo_map import build_repo_map, repo_map_to_markdown
from aidrp.requirement_brief import build_requirement_brief
from aidrp.task_packet import build_task_packet
from aidrp.tool_contract import build_tool_contract
from aidrp.trace import append_trace_event, start_trace
from aidrp.workspace import DEFAULT_CONFIG, init_workspace

from tests.helpers import (
    assert_json_snapshot,
    assert_schema_subset,
    assert_text_snapshot,
    copy_scenario_fixture,
    load_json,
    readme_command_list,
    repo_root,
    scenario_expected_root,
    scenario_input,
)


class SchemaAndSnapshotTests(unittest.TestCase):
    def test_generated_payloads_follow_repo_schemas(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture = copy_scenario_fixture(root)
            init_workspace(fixture, write_agents_template=True)
            repo_map = build_repo_map(fixture)

            task_input = scenario_input("task-packet.json")
            debug_input = scenario_input("debug-pack.json")
            eval_input = scenario_input("eval-case.json")
            sync_input = scenario_input("doc-sync.json")
            brief_input = scenario_input("requirement-brief.json")
            product_review_input = scenario_input("product-review.json")
            engineering_review_input = scenario_input("engineering-review.json")

            trace_file = root / "trace.json"
            start_trace(trace_file, trace_id="trace-1", task_id="task-1", title="Trace demo")
            trace = append_trace_event(
                trace_file,
                stage="verify",
                summary="Smoke test",
                files=["src/calendar_agent.py"],
                commands=[],
                outcome="pass",
            )

            requirement_brief = build_requirement_brief(
                title=brief_input["title"],
                product_idea=brief_input["product_idea"],
                target_users=brief_input["target_users"],
                pain_points=brief_input["pain_points"],
                desired_outcomes=brief_input["desired_outcomes"],
                core_scenarios=brief_input["core_scenarios"],
                non_goals=brief_input["non_goals"],
                constraints=brief_input["constraints"],
                success_metrics=brief_input["success_metrics"],
                open_questions=brief_input["open_questions"],
                assumptions=brief_input["assumptions"],
            )
            product_review = build_product_review(
                requirement_brief,
                current_goal=product_review_input["current_goal"],
                core_user=product_review_input["core_user"],
                core_problem=product_review_input["core_problem"],
                primary_scenario=product_review_input["primary_scenario"],
                minimum_slice=product_review_input["minimum_slice"],
                non_goals=product_review_input["non_goals"],
                scope_decision=product_review_input["scope_decision"],
                scope_reason=product_review_input["scope_reason"],
                success_signals=product_review_input["success_signals"],
                expansion_triggers=product_review_input["expansion_triggers"],
                open_questions=product_review_input["open_questions"],
                assumptions=product_review_input["assumptions"],
            )
            engineering_review = build_engineering_review(
                fixture,
                repo_map,
                requirement_brief,
                product_review,
                change_goal=engineering_review_input["change_goal"],
                write_boundary=engineering_review_input["write_boundary"],
                avoid_files=engineering_review_input["avoid_files"],
                state_owner=engineering_review_input["state_owner"],
                risks=engineering_review_input["risks"],
                failure_modes=engineering_review_input["failure_modes"],
                observability_points=engineering_review_input["observability_points"],
                validation_commands=engineering_review_input["validation_commands"],
                live_qa_entry=engineering_review_input["live_qa_entry"],
                rollback_plan=engineering_review_input["rollback_plan"],
                review_decision=engineering_review_input["review_decision"],
                decision_reason=engineering_review_input["decision_reason"],
            )

            payloads = {
                "workspace-config": DEFAULT_CONFIG,
                "repo-map": repo_map,
                "requirement-brief": requirement_brief,
                "product-review": product_review,
                "engineering-review": engineering_review,
                "task-packet": build_task_packet(
                    fixture,
                    repo_map,
                    title=task_input["title"],
                    objective=task_input["objective"],
                    task_type=task_input["type"],
                    scope=task_input["scope"],
                    non_goals=task_input["non_goals"],
                    acceptance_criteria=task_input["acceptance"],
                    constraints=task_input["constraints"],
                    search_terms=task_input["search_terms"],
                ),
                "debug-pack": build_debug_pack(
                    fixture,
                    repo_map,
                    title=debug_input["title"],
                    symptom=debug_input["symptom"],
                    observed=debug_input["observed"],
                    expected=debug_input["expected"],
                    impact=debug_input["impact"],
                    trace_id=debug_input["trace_id"],
                    request_id=debug_input["request_id"],
                    decision_id=debug_input["decision_id"],
                    plan_id=debug_input["plan_id"],
                    tool_call_id=debug_input["tool_call_id"],
                    entrypoint=debug_input["entrypoint"],
                    failure_stage=debug_input["failure_stage"],
                    reproduction_steps=debug_input["reproduction_steps"],
                    suspected_files=debug_input["suspected_files"],
                    log_files=debug_input["log_files"],
                    search_terms=debug_input["search_terms"],
                ),
                "eval-case": build_eval_case(
                    title=eval_input["title"],
                    origin=eval_input["origin"],
                    command=eval_input["command"],
                    reproduction_steps=eval_input["reproduction_steps"],
                    assertions=eval_input["assertions"],
                    tags=eval_input["tags"],
                ),
                "decision-trace": trace,
                "design-token-pack": build_design_token_pack(
                    title="AI schedule UI 日程助手界面",
                    product_surface="Conversation-first scheduling assistant",
                    brand_direction="Calm productivity with low visual noise.",
                    brand_color="#0F766E",
                    accent_color="#F59E0B",
                    canvas_color="#F8FAFC",
                    text_color="#0F172A",
                    font_sans="IBM Plex Sans, PingFang SC, sans-serif",
                    font_display="IBM Plex Sans, PingFang SC, sans-serif",
                    font_mono="JetBrains Mono, SFMono-Regular, monospace",
                    design_principles=["Use semantic tokens before component-level overrides."],
                    modes=["light"],
                    guardrails=["Do not hard-code hex colors inside components."],
                ),
                "domain-map": build_domain_map(
                    product="AI schedule assistant",
                    orchestrator="calendar-orchestrator",
                    domains=[{"name": "schedule", "owned_state": ["events"], "capabilities": ["create", "delete"], "non_goals": []}],
                    shared_infrastructure=["logging"],
                    cross_domain_flows=[{"name": "travel reimbursement", "trigger": "chat request", "domains": ["schedule", "expense"], "owner": "expense"}],
                ),
                "tool-contract": build_tool_contract(
                    tool_name="delete_event",
                    domain="schedule",
                    purpose="Delete an event by stable ID.",
                    inputs=[{"name": "event_id", "type": "string", "required": True, "description": "Stable ID."}],
                    outputs=[{"name": "deleted", "type": "boolean", "description": "Deletion result."}],
                    idempotency="Deleting an already deleted event is a no-op.",
                    permission_boundary="Only schedule domain may delete schedule events.",
                    retry_policy="No automatic retry.",
                    rollback_policy="Restore from event snapshot only.",
                    failure_codes=[{"code": "EVENT_NOT_FOUND", "meaning": "Target missing.", "caller_action": "Stop."}],
                ),
                "execution-plan": build_execution_plan(
                    title="Delete event safely",
                    goal="Delete after confirmation.",
                    trigger="User confirms.",
                    preconditions=["Event ID is stable."],
                    steps=[{"name": "Resolve target", "inputs": ["event_id"], "tools": ["fetch_event"], "outputs": ["event snapshot"], "requires_confirmation": False}],
                    success_exit="Deleted.",
                    failure_exit="Target missing.",
                    fallbacks=["Ask user to refresh."],
                ),
                "observability-correlation": build_observability_correlation(
                    fixture,
                    title="Meeting deletion correlation 会议删除关联",
                    trace_id=debug_input["trace_id"],
                    request_id=debug_input["request_id"],
                    decision_id=debug_input["decision_id"],
                    plan_id=debug_input["plan_id"],
                    tool_call_id=debug_input["tool_call_id"],
                    entrypoint=debug_input["entrypoint"],
                    failure_stage=debug_input["failure_stage"],
                    log_files=debug_input["log_files"],
                    search_terms=["wrong meeting removed"],
                ),
                "cost-privacy-budget": build_cost_privacy_budget(
                    workflow="debug flow",
                    scope="production bug triage",
                    context_budget={"seed_file_limit": 12, "candidate_file_limit": 10, "hard_file_cap": 24},
                    reasoning_budget={"default_profile": "balanced", "upgrade_triggers": ["Only when evidence is insufficient."]},
                    permission_budget={"allowed_tools": ["read", "grep"], "confirmation_required": ["delete"]},
                    data_budget={"log_safe_fields": ["trace_id"], "redact_fields": ["token"], "forbidden_export_fields": ["invoice_image"]},
                ),
                "doc-sync": build_doc_sync(
                    fixture,
                    title=sync_input["title"],
                    summary=sync_input["summary"],
                    changed_files=sync_input["changed_files"],
                    change_notes=sync_input["change_notes"],
                ),
            }

            for schema_path in (repo_root() / "schemas").glob("*.schema.json"):
                key = schema_path.name.replace(".schema.json", "")
                with self.subTest(schema=key):
                    assert_schema_subset(self, payloads[key], load_json(schema_path))

    def test_key_readable_outputs_match_goldens(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture = copy_scenario_fixture(root)
            init_workspace(fixture, write_agents_template=True)
            repo_map = build_repo_map(fixture)
            brief_input = scenario_input("requirement-brief.json")
            product_review_input = scenario_input("product-review.json")
            engineering_review_input = scenario_input("engineering-review.json")
            requirement_brief = build_requirement_brief(
                title=brief_input["title"],
                product_idea=brief_input["product_idea"],
                target_users=brief_input["target_users"],
                pain_points=brief_input["pain_points"],
                desired_outcomes=brief_input["desired_outcomes"],
                core_scenarios=brief_input["core_scenarios"],
                non_goals=brief_input["non_goals"],
                constraints=brief_input["constraints"],
                success_metrics=brief_input["success_metrics"],
                open_questions=brief_input["open_questions"],
                assumptions=brief_input["assumptions"],
            )
            product_review = build_product_review(
                requirement_brief,
                current_goal=product_review_input["current_goal"],
                core_user=product_review_input["core_user"],
                core_problem=product_review_input["core_problem"],
                primary_scenario=product_review_input["primary_scenario"],
                minimum_slice=product_review_input["minimum_slice"],
                non_goals=product_review_input["non_goals"],
                scope_decision=product_review_input["scope_decision"],
                scope_reason=product_review_input["scope_reason"],
                success_signals=product_review_input["success_signals"],
                expansion_triggers=product_review_input["expansion_triggers"],
                open_questions=product_review_input["open_questions"],
                assumptions=product_review_input["assumptions"],
            )
            engineering_review = build_engineering_review(
                fixture,
                repo_map,
                requirement_brief,
                product_review,
                change_goal=engineering_review_input["change_goal"],
                write_boundary=engineering_review_input["write_boundary"],
                avoid_files=engineering_review_input["avoid_files"],
                state_owner=engineering_review_input["state_owner"],
                risks=engineering_review_input["risks"],
                failure_modes=engineering_review_input["failure_modes"],
                observability_points=engineering_review_input["observability_points"],
                validation_commands=engineering_review_input["validation_commands"],
                live_qa_entry=engineering_review_input["live_qa_entry"],
                rollback_plan=engineering_review_input["rollback_plan"],
                review_decision=engineering_review_input["review_decision"],
                decision_reason=engineering_review_input["decision_reason"],
            )

            assert_text_snapshot(self, repo_map_to_markdown(repo_map), scenario_expected_root() / "repo-map.md")
            assert_json_snapshot(self, repo_map, scenario_expected_root() / "repo-map.json")
            assert_text_snapshot(
                self,
                product_review_to_markdown(product_review),
                scenario_expected_root() / "ai-会议助手第一版-product-review.md",
            )
            assert_json_snapshot(self, product_review, scenario_expected_root() / "ai-会议助手第一版-product-review.json")
            assert_text_snapshot(
                self,
                engineering_review_to_markdown(engineering_review),
                scenario_expected_root() / "ai-会议助手第一版-engineering-review.md",
            )
            assert_json_snapshot(
                self,
                engineering_review,
                scenario_expected_root() / "ai-会议助手第一版-engineering-review.json",
            )

            debug_input = scenario_input("debug-pack.json")
            correlation = build_observability_correlation(
                fixture,
                title="Meeting deletion correlation 会议删除关联",
                trace_id=debug_input["trace_id"],
                request_id=debug_input["request_id"],
                decision_id=debug_input["decision_id"],
                plan_id=debug_input["plan_id"],
                tool_call_id=debug_input["tool_call_id"],
                entrypoint=debug_input["entrypoint"],
                failure_stage=debug_input["failure_stage"],
                log_files=debug_input["log_files"],
                search_terms=["wrong meeting removed"],
            )
            assert_text_snapshot(
                self,
                observability_correlation_to_markdown(correlation),
                scenario_expected_root() / "meeting-deletion-correlation-会议删除关联.md",
            )

            sync_input = scenario_input("doc-sync.json")
            sync_pack = build_doc_sync(
                fixture,
                title=sync_input["title"],
                summary=sync_input["summary"],
                changed_files=sync_input["changed_files"],
                change_notes=sync_input["change_notes"],
            )
            assert_text_snapshot(
                self,
                doc_sync_to_markdown(sync_pack),
                scenario_expected_root() / "meeting-deletion-docs-refresh-会议删除修复文档同步.md",
            )

            token_pack = build_design_token_pack(
                title="AI schedule UI 日程助手界面",
                product_surface="Conversation-first scheduling and expense assistant 对话优先的日程与费用助手",
                brand_direction="Calm productivity with strong structure and low visual noise. 冷静、高效、结构感强、低噪音。",
                brand_color="#0F766E",
                accent_color="#F59E0B",
                canvas_color="#F8FAFC",
                text_color="#0F172A",
                font_sans="IBM Plex Sans, PingFang SC, sans-serif",
                font_display="IBM Plex Sans, PingFang SC, sans-serif",
                font_mono="JetBrains Mono, SFMono-Regular, monospace",
                design_principles=[],
                modes=[],
                guardrails=[],
            )
            expected_html = (repo_root() / "examples" / "outputs" / "ai-schedule-ui-日程助手界面.html").read_text(encoding="utf-8")
            self.assertMultiLineEqual(expected_html.replace("\r\n", "\n"), design_token_pack_to_html(token_pack).replace("\r\n", "\n"))

    def test_documentation_indices_stay_in_sync_with_cli_and_examples(self) -> None:
        parser = build_parser()
        subparsers = next(action for action in parser._actions if getattr(action, "choices", None))
        cli_commands = set(subparsers.choices)
        self.assertEqual(set(readme_command_list()), cli_commands)
        self.assertTrue((repo_root() / "docs" / "tutorials" / "e2e-walkthrough-端到端教程.md").exists())
        self.assertTrue((repo_root() / "docs" / "reference" / "cli-reference-CLI参考.md").exists())
        self.assertTrue((repo_root() / "examples" / "scenarios" / "meeting-assistant").exists())
