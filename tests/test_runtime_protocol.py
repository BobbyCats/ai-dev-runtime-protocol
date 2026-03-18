from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from aidrp.debug_pack import build_debug_pack
from aidrp.eval_case import build_eval_case
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
                search_terms=["packet", "task"],
            )
            self.assertEqual(task["task_id"], "create-packet")
            self.assertTrue(task["candidate_files"])

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


if __name__ == "__main__":
    unittest.main()
