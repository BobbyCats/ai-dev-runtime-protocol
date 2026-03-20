from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.helpers import copy_scenario_fixture, run_cli, scenario_input


class CliCommandTests(unittest.TestCase):
    def test_all_cli_success_paths_generate_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture = copy_scenario_fixture(root)
            out = root / "generated"

            run_cli(["init-workspace", "--project-root", ".", "--write-agents-template"], cwd=fixture)
            self.assertTrue((fixture / ".aidrp" / "config.json").exists())
            self.assertTrue((fixture / "AGENTS.md").exists())

            run_cli(["repo-map", "--project-root", ".", "--output-dir", ".aidrp"], cwd=fixture)
            self.assertTrue((fixture / ".aidrp" / "repo-map.json").exists())

            brief = scenario_input("requirement-brief.json")
            run_cli(
                [
                    "requirement-brief",
                    "--title",
                    brief["title"],
                    "--product-idea",
                    brief["product_idea"],
                    *sum([["--target-user", item] for item in brief["target_users"]], []),
                    *sum([["--pain-point", item] for item in brief["pain_points"]], []),
                    *sum([["--desired-outcome", item] for item in brief["desired_outcomes"]], []),
                    *sum([["--scenario", item] for item in brief["core_scenarios"]], []),
                    *sum([["--non-goal", item] for item in brief["non_goals"]], []),
                    *sum([["--constraint", item] for item in brief["constraints"]], []),
                    *sum([["--success-metric", item] for item in brief["success_metrics"]], []),
                    *sum([["--assumption", item] for item in brief["assumptions"]], []),
                    "--output-dir",
                    str(out / "briefs"),
                ]
            )
            self.assertTrue((out / "briefs" / "ai-会议助手第一版.json").exists())

            product_review = scenario_input("product-review.json")
            run_cli(
                [
                    "product-review",
                    "--brief",
                    str(out / "briefs" / "ai-会议助手第一版.json"),
                    "--current-goal",
                    product_review["current_goal"],
                    "--core-user",
                    product_review["core_user"],
                    "--core-problem",
                    product_review["core_problem"],
                    "--primary-scenario",
                    product_review["primary_scenario"],
                    "--mvs",
                    product_review["minimum_slice"],
                    *sum([["--non-goal", item] for item in product_review["non_goals"]], []),
                    "--scope-decision",
                    product_review["scope_decision"],
                    "--scope-reason",
                    product_review["scope_reason"],
                    *sum([["--success-signal", item] for item in product_review["success_signals"]], []),
                    *sum([["--expand-trigger", item] for item in product_review["expansion_triggers"]], []),
                    *sum([["--open-question", item] for item in product_review["open_questions"]], []),
                    *sum([["--assumption", item] for item in product_review["assumptions"]], []),
                    "--output-dir",
                    str(out / "product-reviews"),
                ]
            )
            self.assertTrue((out / "product-reviews" / "ai-会议助手第一版-product-review.json").exists())

            engineering_review = scenario_input("engineering-review.json")
            run_cli(
                [
                    "engineering-review",
                    "--project-root",
                    ".",
                    "--brief",
                    str(out / "briefs" / "ai-会议助手第一版.json"),
                    "--product-review",
                    str(out / "product-reviews" / "ai-会议助手第一版-product-review.json"),
                    "--repo-map",
                    ".aidrp/repo-map.json",
                    "--change-goal",
                    engineering_review["change_goal"],
                    *sum([["--write-boundary", item] for item in engineering_review["write_boundary"]], []),
                    *sum([["--avoid-file", item] for item in engineering_review["avoid_files"]], []),
                    "--state-owner",
                    engineering_review["state_owner"],
                    *sum([["--risk", item] for item in engineering_review["risks"]], []),
                    *sum([["--failure-mode", item] for item in engineering_review["failure_modes"]], []),
                    *sum([["--observe", item] for item in engineering_review["observability_points"]], []),
                    *sum([["--validation-command", item] for item in engineering_review["validation_commands"]], []),
                    "--live-qa-entry",
                    engineering_review["live_qa_entry"],
                    "--rollback-plan",
                    engineering_review["rollback_plan"],
                    "--decision",
                    engineering_review["review_decision"],
                    "--decision-reason",
                    engineering_review["decision_reason"],
                    "--output-dir",
                    str(out / "engineering-reviews"),
                ],
                cwd=fixture,
            )
            self.assertTrue((out / "engineering-reviews" / "ai-会议助手第一版-engineering-review.json").exists())

            run_cli(
                [
                    "domain-map",
                    "--product",
                    "AI schedule assistant",
                    "--orchestrator",
                    "calendar-orchestrator",
                    "--domain",
                    "schedule|events,availability|create,update,delete|expense tracking",
                    "--shared-infra",
                    "logging",
                    "--cross-flow",
                    "travel reimbursement|chat request|schedule,expense|expense",
                    "--output-dir",
                    str(out / "domains"),
                ]
            )
            self.assertTrue((out / "domains" / "ai-schedule-assistant.json").exists())

            run_cli(
                [
                    "tool-contract",
                    "--tool-name",
                    "delete_event",
                    "--domain",
                    "schedule",
                    "--purpose",
                    "Delete an event by stable ID.",
                    "--input-field",
                    "event_id|string|true|Stable event identifier.",
                    "--output-field",
                    "deleted|boolean|Whether deletion succeeded.",
                    "--output-dir",
                    str(out / "contracts"),
                ]
            )
            self.assertTrue((out / "contracts" / "delete_event.json").exists())

            run_cli(
                [
                    "execution-plan",
                    "--title",
                    "Delete event safely",
                    "--goal",
                    "Delete the selected event after confirmation.",
                    "--step",
                    "Resolve target|event_id|fetch_event|event snapshot|false",
                    "--step",
                    "Execute delete|event snapshot|delete_event|delete result|true",
                    "--output-dir",
                    str(out / "plans"),
                ]
            )
            self.assertTrue((out / "plans" / "delete-event-safely.json").exists())

            task = scenario_input("task-packet.json")
            run_cli(
                [
                    "task-packet",
                    "--project-root",
                    ".",
                    "--repo-map",
                    ".aidrp/repo-map.json",
                    "--title",
                    task["title"],
                    "--objective",
                    task["objective"],
                    "--type",
                    task["type"],
                    *sum([["--scope", item] for item in task["scope"]], []),
                    *sum([["--non-goal", item] for item in task["non_goals"]], []),
                    *sum([["--acceptance", item] for item in task["acceptance"]], []),
                    *sum([["--constraint", item] for item in task["constraints"]], []),
                    *sum([["--search-term", item] for item in task["search_terms"]], []),
                    "--output-dir",
                    str(out / "tasks"),
                ],
                cwd=fixture,
            )
            self.assertTrue((out / "tasks" / "fix-meeting-deletion-drift-修复会议删除漂移.json").exists())

            debug = scenario_input("debug-pack.json")
            run_cli(
                [
                    "debug-pack",
                    "--project-root",
                    ".",
                    "--repo-map",
                    ".aidrp/repo-map.json",
                    "--title",
                    debug["title"],
                    "--symptom",
                    debug["symptom"],
                    "--observed",
                    debug["observed"],
                    "--expected",
                    debug["expected"],
                    "--impact",
                    debug["impact"],
                    "--trace-id",
                    debug["trace_id"],
                    "--request-id",
                    debug["request_id"],
                    "--decision-id",
                    debug["decision_id"],
                    "--plan-id",
                    debug["plan_id"],
                    "--tool-call-id",
                    debug["tool_call_id"],
                    "--entrypoint",
                    debug["entrypoint"],
                    "--failure-stage",
                    debug["failure_stage"],
                    *sum([["--repro-step", item] for item in debug["reproduction_steps"]], []),
                    *sum([["--suspected-file", item] for item in debug["suspected_files"]], []),
                    *sum([["--log-file", item] for item in debug["log_files"]], []),
                    *sum([["--search-term", item] for item in debug["search_terms"]], []),
                    "--output-dir",
                    str(out / "debug"),
                ],
                cwd=fixture,
            )
            self.assertTrue((out / "debug" / "meeting-deletion-drift-会议删除漂移.json").exists())

            eval_case = scenario_input("eval-case.json")
            run_cli(
                [
                    "eval-case",
                    "--title",
                    eval_case["title"],
                    "--origin",
                    eval_case["origin"],
                    "--command",
                    eval_case["command"],
                    *sum([["--repro-step", item] for item in eval_case["reproduction_steps"]], []),
                    *sum([["--assertion", item] for item in eval_case["assertions"]], []),
                    *sum([["--tag", item] for item in eval_case["tags"]], []),
                    "--output-dir",
                    str(out / "evals"),
                ]
            )
            self.assertTrue((out / "evals" / "regression-for-meeting-deletion-drift-会议删除漂移回归用例.json").exists())

            run_cli(
                [
                    "design-token-pack",
                    "--title",
                    "AI schedule UI 日程助手界面",
                    "--surface",
                    "Conversation-first scheduling assistant",
                    "--brand-direction",
                    "Calm productivity with low visual noise.",
                    "--brand-color",
                    "#0F766E",
                    "--output-dir",
                    str(out / "design-system"),
                ]
            )
            self.assertTrue((out / "design-system" / "ai-schedule-ui-日程助手界面.html").exists())

            run_cli(
                [
                    "observability-correlation",
                    "--project-root",
                    ".",
                    "--title",
                    "Meeting deletion correlation 会议删除关联",
                    "--trace-id",
                    "trace-meeting-001",
                    "--request-id",
                    "req-meeting-001",
                    "--decision-id",
                    "dec-meeting-001",
                    "--plan-id",
                    "plan-delete-001",
                    "--tool-call-id",
                    "tool-delete-001",
                    "--entrypoint",
                    "meeting.delete",
                    "--failure-stage",
                    "executor",
                    "--log-file",
                    "logs/runtime.log",
                    "--search-term",
                    "wrong meeting removed",
                    "--output-dir",
                    str(out / "correlations"),
                ],
                cwd=fixture,
            )
            self.assertTrue((out / "correlations" / "meeting-deletion-correlation-会议删除关联.json").exists())

            run_cli(
                [
                    "cost-privacy-budget",
                    "--project-root",
                    ".",
                    "--workflow",
                    "debug flow",
                    "--allowed-tool",
                    "read",
                    "--allowed-tool",
                    "grep",
                    "--confirm-action",
                    "delete",
                    "--output-dir",
                    str(out / "budgets"),
                ],
                cwd=fixture,
            )
            self.assertTrue((out / "budgets" / "debug-flow.json").exists())

            doc_sync = scenario_input("doc-sync.json")
            run_cli(
                [
                    "doc-sync",
                    "--project-root",
                    ".",
                    "--title",
                    doc_sync["title"],
                    "--summary",
                    doc_sync["summary"],
                    *sum([["--changed-file", item] for item in doc_sync["changed_files"]], []),
                    *sum([["--change-note", item] for item in doc_sync["change_notes"]], []),
                    "--output-dir",
                    str(out / "docsync"),
                ],
                cwd=fixture,
            )
            self.assertTrue((out / "docsync" / "meeting-deletion-docs-refresh-会议删除修复文档同步.json").exists())

            trace_lines = run_cli(
                [
                    "trace-start",
                    "--title",
                    "Fix meeting deletion drift 修复会议删除漂移",
                    "--task-id",
                    "meeting-delete-fix",
                    "--output-dir",
                    str(out / "traces"),
                ]
            )
            trace_file = Path(trace_lines[0])
            self.assertTrue(trace_file.exists())

            run_cli(
                [
                    "trace-event",
                    "--trace-file",
                    str(trace_file),
                    "--stage",
                    "investigate",
                    "--summary",
                    "Confirmed mismatch between selection_id and meeting_id.",
                ]
            )
            self.assertTrue(trace_file.exists())

    def test_invalid_domain_spec_exits(self) -> None:
        with self.assertRaises(SystemExit):
            run_cli(["domain-map", "--product", "demo", "--domain", "schedule|events"])

    def test_invalid_tool_contract_spec_exits(self) -> None:
        with self.assertRaises(SystemExit):
            run_cli(["tool-contract", "--tool-name", "delete", "--purpose", "demo", "--input-field", "event_id|string|true"])

    def test_invalid_execution_step_spec_exits(self) -> None:
        with self.assertRaises(SystemExit):
            run_cli(["execution-plan", "--title", "demo", "--goal", "demo", "--step", "Resolve target|event_id|fetch_event"])
