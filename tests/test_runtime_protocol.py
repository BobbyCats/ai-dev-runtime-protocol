from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from aidrp.debug_pack import build_debug_pack
from aidrp.design_token_pack import (
    build_design_token_pack,
    design_token_pack_to_html,
    write_design_token_pack,
)
from aidrp.doc_sync import build_doc_sync
from aidrp.eval_case import build_eval_case
from aidrp.requirement_brief import build_requirement_brief
from aidrp.repo_map import build_repo_map
from aidrp.task_packet import build_task_packet
from aidrp.trace import append_trace_event, start_trace
from aidrp.workspace import init_workspace


class RuntimeProtocolTests(unittest.TestCase):
    def test_repo_map_and_packets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            (root / "src").mkdir()
            (root / "design-system").mkdir()
            (root / "design-system" / "app-tokens.json").write_text("{\"ok\": true}\n", encoding="utf-8")
            (root / "src" / "app.py").write_text(
                "import json\n\n"
                "def create_task_packet():\n"
                "    return {'ok': True}\n",
                encoding="utf-8",
            )
            init_workspace(root)
            repo_map = build_repo_map(root)

            self.assertGreaterEqual(repo_map["summary"]["file_count"], 2)
            self.assertIn("README.md", repo_map["summary"]["seed_files"])
            self.assertTrue((root / ".aidrp" / "docsync").exists())

            task = build_task_packet(
                root,
                repo_map,
                title="Create packet",
                objective="Create a task packet for the app flow.",
                task_type="feature",
                scope=["Touch packet generation only."],
                non_goals=["Do not add network calls."],
                acceptance_criteria=["Packet includes candidate files."],
                constraints=["Keep it small."],
                search_terms=["packet", "task", "ui"],
            )
            self.assertEqual(task["task_id"], "create-packet")
            self.assertTrue(task["candidate_files"])
            self.assertIn("design-system/app-tokens.json", task["read_order"])

            debug = build_debug_pack(
                root,
                repo_map,
                title="Packet bug",
                symptom="task packet missing files",
                observed="candidate files are empty",
                expected="candidate files list should be populated",
                impact="developer loses context",
                trace_id="trace-123",
                reproduction_steps=["Run the packet builder."],
                suspected_files=["src/app.py"],
                log_files=[],
                search_terms=["candidate", "packet"],
            )
            self.assertEqual(debug["trace_id"], "trace-123")
            self.assertTrue(debug["suspected_files"])

            doc_sync = build_doc_sync(
                root,
                title="Runtime workflow refresh",
                summary="Added a new runtime command and updated execution workflow.",
                changed_files=["src/aidrp/cli.py", "docs/playbooks/stage-router-阶段路由.md"],
                change_notes=["README should be reviewed from a whole-system perspective."],
            )
            self.assertEqual(doc_sync["readme_strategy"], "full-rewrite")
            self.assertTrue(any(item["path"] == "README.md" for item in doc_sync["impacted_docs"]))

    def test_eval_case_and_trace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            trace_file = root / "trace.json"
            start_trace(trace_file, trace_id="trace-1", task_id="task-1", title="Trace demo")
            trace = append_trace_event(
                trace_file,
                stage="verify",
                summary="Ran a smoke test",
                files=["src/app.py"],
                commands=["python -m unittest"],
                outcome="pass",
            )
            self.assertEqual(trace["events"][0]["stage"], "verify")

            eval_case = build_eval_case(
                title="Regression for missing files",
                origin="debug-pack:packet-bug",
                command="python -m unittest",
                reproduction_steps=["Run the command."],
                assertions=["The packet contains at least one candidate file."],
                tags=["bugfix", "packet"],
            )
            self.assertEqual(eval_case["eval_id"], "regression-for-missing-files")
            self.assertIn("packet", eval_case["tags"])

    def test_requirement_brief(self) -> None:
        brief = build_requirement_brief(
            title="AI meeting helper AI 会议助手",
            product_idea="Use an interview-first workflow to clarify a scheduling assistant before coding. 在编码前用访谈方式先澄清需求。",
            target_users=["Founders who think in ideas first. 先有想法再落产品的创业者。"],
            pain_points=["Requirements are vague at the start. 一开始需求很模糊。"],
            desired_outcomes=["Turn chat into a brief. 把聊天收敛成简报。"],
            core_scenarios=["Clarify the first milestone. 澄清第一个里程碑。"],
            non_goals=["Do not design the full backend yet. 暂不设计完整后端。"],
            constraints=["Keep the first version lightweight. 第一版保持轻量。"],
            success_metrics=["A task packet can be created from the brief. 能从简报继续生成任务包。"],
            open_questions=["Should the interview stop after five questions? 是否限制为五个问题？"],
            assumptions=["The user prefers Chinese-first wording. 默认用户更适合中文主导表达。"],
        )
        self.assertEqual(brief["brief_id"], "ai-meeting-helper-ai-会议助手")
        self.assertIn("Turn chat into a brief", brief["desired_outcomes"][0])

    def test_design_token_pack(self) -> None:
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
            self.assertEqual(pack["token_pack_id"], "ai-schedule-ui-日程助手界面")
            self.assertEqual(pack["semantics"]["accent.primary"], "{color.brand.500}")
            self.assertEqual(pack["component_guidance"][0]["component"], "page-shell")

            html_preview = design_token_pack_to_html(pack)
            self.assertIn("Design Token Preview / 设计令牌预览", html_preview)
            self.assertIn("Color Scales / 色板刻度", html_preview)

            prefix = root / pack["token_pack_id"]
            write_design_token_pack(
                pack,
                prefix.with_suffix(".json"),
                prefix.with_suffix(".md"),
                prefix.with_suffix(".html"),
            )
            self.assertTrue(prefix.with_suffix(".html").exists())


if __name__ == "__main__":
    unittest.main()
