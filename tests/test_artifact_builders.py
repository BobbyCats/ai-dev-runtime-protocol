from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from aidrp.cost_privacy_budget import build_cost_privacy_budget
from aidrp.debug_pack import build_debug_pack
from aidrp.design_token_pack import (
    build_design_token_pack,
    design_token_pack_to_html,
    write_design_token_pack,
)
from aidrp.doc_sync import build_doc_sync
from aidrp.domain_map import build_domain_map
from aidrp.eval_case import build_eval_case
from aidrp.execution_plan import build_execution_plan
from aidrp.repo_map import build_repo_map
from aidrp.requirement_brief import build_requirement_brief
from aidrp.task_packet import build_task_packet
from aidrp.tool_contract import build_tool_contract
from aidrp.trace import append_trace_event, start_trace
from aidrp.workspace import init_workspace

from tests.helpers import copy_scenario_fixture, scenario_input


class ArtifactBuilderTests(unittest.TestCase):
    def test_requirement_brief_builder_uses_structured_input(self) -> None:
        data = scenario_input("requirement-brief.json")
        brief = build_requirement_brief(
            title=data["title"],
            product_idea=data["product_idea"],
            target_users=data["target_users"],
            pain_points=data["pain_points"],
            desired_outcomes=data["desired_outcomes"],
            core_scenarios=data["core_scenarios"],
            non_goals=data["non_goals"],
            constraints=data["constraints"],
            success_metrics=data["success_metrics"],
            open_questions=data["open_questions"],
            assumptions=data["assumptions"],
        )
        self.assertEqual(brief["brief_id"], "ai-会议助手第一版")
        self.assertIn("task-packet", brief["recommended_next_step"])

    def test_design_token_pack_writes_html_preview(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pack = build_design_token_pack(
                title="AI schedule UI 日程助手界面",
                product_surface="Conversation-first scheduling and expense assistant",
                brand_direction="Calm productivity with strong structure and low visual noise.",
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
            )
            html_preview = design_token_pack_to_html(pack)
            self.assertIn("Design Token Preview / 设计令牌预览", html_preview)
            prefix = root / pack["token_pack_id"]
            write_design_token_pack(pack, prefix.with_suffix(".json"), prefix.with_suffix(".md"), prefix.with_suffix(".html"))
            self.assertTrue(prefix.with_suffix(".html").exists())

    def test_repo_task_debug_and_doc_sync_builders_match_scenario(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture = copy_scenario_fixture(root)
            init_workspace(fixture, write_agents_template=True)
            repo_map = build_repo_map(fixture)

            self.assertIn("README.md", repo_map["summary"]["seed_files"])
            self.assertTrue((fixture / ".aidrp" / "docsync").exists())

            task_data = scenario_input("task-packet.json")
            task = build_task_packet(
                fixture,
                repo_map,
                title=task_data["title"],
                objective=task_data["objective"],
                task_type=task_data["type"],
                scope=task_data["scope"],
                non_goals=task_data["non_goals"],
                acceptance_criteria=task_data["acceptance"],
                constraints=task_data["constraints"],
                search_terms=task_data["search_terms"],
            )
            self.assertEqual(task["task_id"], "fix-meeting-deletion-drift-修复会议删除漂移")
            self.assertTrue(any(item["path"] == "src/calendar_agent.py" for item in task["candidate_files"]))

            debug_data = scenario_input("debug-pack.json")
            debug = build_debug_pack(
                fixture,
                repo_map,
                title=debug_data["title"],
                symptom=debug_data["symptom"],
                observed=debug_data["observed"],
                expected=debug_data["expected"],
                impact=debug_data["impact"],
                trace_id=debug_data["trace_id"],
                request_id=debug_data["request_id"],
                decision_id=debug_data["decision_id"],
                plan_id=debug_data["plan_id"],
                tool_call_id=debug_data["tool_call_id"],
                entrypoint=debug_data["entrypoint"],
                failure_stage=debug_data["failure_stage"],
                reproduction_steps=debug_data["reproduction_steps"],
                suspected_files=debug_data["suspected_files"],
                log_files=debug_data["log_files"],
                search_terms=debug_data["search_terms"],
            )
            self.assertTrue(debug["log_snippets"])
            self.assertNotIn("trace_id:trace-meeting-001", debug["log_focus"]["missing_queries"])
            self.assertTrue(any(item["path"] == "src/calendar_agent.py" for item in debug["suspected_files"]))

            sync_data = scenario_input("doc-sync.json")
            doc_sync = build_doc_sync(
                fixture,
                title=sync_data["title"],
                summary=sync_data["summary"],
                changed_files=sync_data["changed_files"],
                change_notes=sync_data["change_notes"],
            )
            self.assertEqual(doc_sync["readme_strategy"], "targeted-update")
            self.assertTrue(any(item["path"] == "README.md" for item in doc_sync["impacted_docs"]))

    def test_eval_case_and_trace_builders(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            trace_file = root / "trace.json"
            start_trace(trace_file, trace_id="trace-1", task_id="meeting-delete-fix", title="Meeting delete fix")
            trace = append_trace_event(
                trace_file,
                stage="investigate",
                summary="Confirmed mismatch between card selection and stable meeting_id.",
                files=["src/calendar_agent.py"],
                commands=["python -m unittest"],
                outcome="pass",
            )
            self.assertEqual(trace["events"][0]["stage"], "investigate")

            eval_data = scenario_input("eval-case.json")
            eval_case = build_eval_case(
                title=eval_data["title"],
                origin=eval_data["origin"],
                command=eval_data["command"],
                reproduction_steps=eval_data["reproduction_steps"],
                assertions=eval_data["assertions"],
                tags=eval_data["tags"],
            )
            self.assertEqual(eval_case["eval_id"], "regression-for-meeting-deletion-drift-会议删除漂移回归用例")

    def test_advanced_runtime_artifact_builders(self) -> None:
        domain_map = build_domain_map(
            product="AI schedule assistant",
            orchestrator="calendar-orchestrator",
            domains=[
                {
                    "name": "schedule",
                    "owned_state": ["events", "availability"],
                    "capabilities": ["create", "update", "delete"],
                    "non_goals": ["expense tracking"],
                }
            ],
            shared_infrastructure=["logging", "auth"],
            cross_domain_flows=[
                {
                    "name": "travel reimbursement",
                    "trigger": "chat request",
                    "domains": ["schedule", "expense"],
                    "owner": "expense",
                }
            ],
        )
        self.assertEqual(domain_map["domain_map_id"], "ai-schedule-assistant")

        contract = build_tool_contract(
            tool_name="delete_event",
            domain="schedule",
            purpose="Delete an event by stable ID.",
            inputs=[{"name": "event_id", "type": "string", "required": True, "description": "Stable event identifier."}],
            outputs=[{"name": "deleted", "type": "boolean", "description": "Whether deletion succeeded."}],
            idempotency="Deleting an already deleted event is a no-op.",
            permission_boundary="Only schedule domain may delete schedule events.",
            retry_policy="No automatic retry.",
            rollback_policy="Restore from event snapshot only.",
            failure_codes=[
                {
                    "code": "EVENT_NOT_FOUND",
                    "meaning": "Target event is missing.",
                    "caller_action": "Show user-facing error and stop.",
                }
            ],
        )
        self.assertEqual(contract["contract_id"], "delete_event")

        plan = build_execution_plan(
            title="Delete event safely",
            goal="Delete the targeted event after confirmation.",
            trigger="User confirms deletion.",
            preconditions=["Event ID is stable."],
            steps=[
                {
                    "name": "Resolve target",
                    "inputs": ["event_id"],
                    "tools": ["fetch_event"],
                    "outputs": ["event snapshot"],
                    "requires_confirmation": False,
                },
                {
                    "name": "Execute delete",
                    "inputs": ["event snapshot"],
                    "tools": ["delete_event"],
                    "outputs": ["delete result"],
                    "requires_confirmation": True,
                },
            ],
            success_exit="Event disappears and delete result is true.",
            failure_exit="Deletion fails or target is missing.",
            fallbacks=["Ask user to refresh and retry."],
        )
        self.assertEqual(plan["plan_id"], "delete-event-safely")

        budget = build_cost_privacy_budget(
            workflow="debug flow",
            scope="production bug triage",
            context_budget={"seed_file_limit": 12, "candidate_file_limit": 10, "hard_file_cap": 24},
            reasoning_budget={"default_profile": "balanced", "upgrade_triggers": ["Only when evidence is insufficient."]},
            permission_budget={"allowed_tools": ["read", "grep"], "confirmation_required": ["delete"]},
            data_budget={"log_safe_fields": ["trace_id"], "redact_fields": ["token"], "forbidden_export_fields": ["invoice_image"]},
        )
        self.assertEqual(budget["budget_id"], "debug-flow")
