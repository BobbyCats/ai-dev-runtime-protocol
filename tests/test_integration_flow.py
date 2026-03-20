from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.helpers import (
    assert_json_snapshot,
    assert_text_snapshot,
    copy_scenario_fixture,
    load_json,
    repo_root,
    run_cli,
    scenario_expected_root,
    tutorial_commands,
)


class IntegrationFlowTests(unittest.TestCase):
    def test_tutorial_commands_run_end_to_end_against_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture = copy_scenario_fixture(root)

            for args in tutorial_commands():
                run_cli(args, cwd=fixture)

            expected_root = scenario_expected_root()
            actual_files = {
                fixture / ".aidrp" / "briefs" / "ai-会议助手第一版.json": expected_root / "ai-会议助手第一版.json",
                fixture / ".aidrp" / "briefs" / "ai-会议助手第一版.md": expected_root / "ai-会议助手第一版.md",
                fixture / ".aidrp" / "product-reviews" / "ai-会议助手第一版-product-review.json": expected_root / "ai-会议助手第一版-product-review.json",
                fixture / ".aidrp" / "product-reviews" / "ai-会议助手第一版-product-review.md": expected_root / "ai-会议助手第一版-product-review.md",
                fixture / ".aidrp" / "repo-map.json": expected_root / "repo-map.json",
                fixture / ".aidrp" / "repo-map.md": expected_root / "repo-map.md",
                fixture / ".aidrp" / "engineering-reviews" / "ai-会议助手第一版-engineering-review.json": expected_root / "ai-会议助手第一版-engineering-review.json",
                fixture / ".aidrp" / "engineering-reviews" / "ai-会议助手第一版-engineering-review.md": expected_root / "ai-会议助手第一版-engineering-review.md",
                fixture / ".aidrp" / "tasks" / "fix-meeting-deletion-drift-修复会议删除漂移.json": expected_root / "fix-meeting-deletion-drift-修复会议删除漂移.json",
                fixture / ".aidrp" / "tasks" / "fix-meeting-deletion-drift-修复会议删除漂移.md": expected_root / "fix-meeting-deletion-drift-修复会议删除漂移.md",
                fixture / ".aidrp" / "debug" / "meeting-deletion-drift-会议删除漂移.json": expected_root / "meeting-deletion-drift-会议删除漂移.json",
                fixture / ".aidrp" / "debug" / "meeting-deletion-drift-会议删除漂移.md": expected_root / "meeting-deletion-drift-会议删除漂移.md",
                fixture / ".aidrp" / "correlations" / "meeting-deletion-correlation-会议删除关联.json": expected_root / "meeting-deletion-correlation-会议删除关联.json",
                fixture / ".aidrp" / "correlations" / "meeting-deletion-correlation-会议删除关联.md": expected_root / "meeting-deletion-correlation-会议删除关联.md",
                fixture / ".aidrp" / "evals" / "regression-for-meeting-deletion-drift-会议删除漂移回归用例.json": expected_root / "regression-for-meeting-deletion-drift-会议删除漂移回归用例.json",
                fixture / ".aidrp" / "evals" / "regression-for-meeting-deletion-drift-会议删除漂移回归用例.md": expected_root / "regression-for-meeting-deletion-drift-会议删除漂移回归用例.md",
                fixture / ".aidrp" / "docsync" / "meeting-deletion-docs-refresh-会议删除修复文档同步.json": expected_root / "meeting-deletion-docs-refresh-会议删除修复文档同步.json",
                fixture / ".aidrp" / "docsync" / "meeting-deletion-docs-refresh-会议删除修复文档同步.md": expected_root / "meeting-deletion-docs-refresh-会议删除修复文档同步.md",
            }

            for actual_path, expected_path in actual_files.items():
                with self.subTest(path=actual_path.name):
                    self.assertTrue(actual_path.exists())
                    if actual_path.suffix == ".json":
                        assert_json_snapshot(self, load_json(actual_path), expected_path)
                    else:
                        assert_text_snapshot(self, actual_path.read_text(encoding="utf-8"), expected_path)

            debug_payload = load_json(fixture / ".aidrp" / "debug" / "meeting-deletion-drift-会议删除漂移.json")
            self.assertTrue(debug_payload["log_snippets"])
            self.assertNotIn("trace_id:trace-meeting-001", debug_payload["log_focus"]["missing_queries"])
            self.assertTrue(any(item["path"] == "src/calendar_agent.py" for item in debug_payload["suspected_files"]))

            correlation_payload = load_json(fixture / ".aidrp" / "correlations" / "meeting-deletion-correlation-会议删除关联.json")
            self.assertTrue(correlation_payload["matched_entries"])
            self.assertEqual(correlation_payload["failure_stage"], "executor")

            self.assertTrue((repo_root() / "examples" / "scenarios" / "meeting-assistant" / "expected").exists())
