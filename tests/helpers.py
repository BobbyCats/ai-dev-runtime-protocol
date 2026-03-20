from __future__ import annotations

import io
import json
import os
import re
import shlex
import shutil
from contextlib import contextmanager, redirect_stdout
from pathlib import Path
from typing import Any

from aidrp.cli import main


ISO_TIMESTAMP_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\+\d{2}:\d{2}|Z)")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def scenario_root() -> Path:
    return repo_root() / "examples" / "scenarios" / "meeting-assistant"


def scenario_fixture_source() -> Path:
    return scenario_root() / "fixture"


def scenario_expected_root() -> Path:
    return scenario_root() / "expected"


def scenario_input(name: str) -> dict[str, Any]:
    return json.loads((scenario_root() / "inputs" / name).read_text(encoding="utf-8"))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def copy_scenario_fixture(destination: Path) -> Path:
    target = destination / "fixture"
    shutil.copytree(scenario_fixture_source(), target)
    return target


@contextmanager
def working_directory(path: Path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


def run_cli(args: list[str], *, cwd: Path | None = None) -> list[str]:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        if cwd is None:
            exit_code = main(args)
        else:
            with working_directory(cwd):
                exit_code = main(args)
    if exit_code != 0:
        raise AssertionError(f"CLI exited with {exit_code}: {args}")
    return [line.strip() for line in stdout.getvalue().splitlines() if line.strip()]


def normalize_text_snapshot(text: str) -> str:
    normalized = ISO_TIMESTAMP_RE.sub("<TIMESTAMP>", text)
    normalized = re.sub(r'("project_root":\s*")[^"]+(")', r'\1<PROJECT_ROOT>\2', normalized)
    normalized = re.sub(r"(- Root \| 根目录: `)[^`]+(`)", r"\1<PROJECT_ROOT>\2", normalized)
    return normalized.replace("\r\n", "\n")


def normalize_json_snapshot(value: Any) -> Any:
    if isinstance(value, dict):
        normalized: dict[str, Any] = {}
        for key, item in value.items():
            if key == "project_root" and isinstance(item, str):
                normalized[key] = "<PROJECT_ROOT>"
            else:
                normalized[key] = normalize_json_snapshot(item)
        return normalized
    if isinstance(value, list):
        return [normalize_json_snapshot(item) for item in value]
    if isinstance(value, str):
        return ISO_TIMESTAMP_RE.sub("<TIMESTAMP>", value)
    return value


def assert_text_snapshot(test_case, actual: str, expected_path: Path) -> None:
    expected = expected_path.read_text(encoding="utf-8")
    test_case.assertMultiLineEqual(normalize_text_snapshot(expected), normalize_text_snapshot(actual))


def assert_json_snapshot(test_case, actual: Any, expected_path: Path) -> None:
    expected = load_json(expected_path)
    test_case.assertEqual(normalize_json_snapshot(expected), normalize_json_snapshot(actual))


def _validate_type(test_case, value: Any, expected_type: str, path: str) -> None:
    if expected_type == "object":
        test_case.assertIsInstance(value, dict, path)
    elif expected_type == "array":
        test_case.assertIsInstance(value, list, path)
    elif expected_type == "string":
        test_case.assertIsInstance(value, str, path)
    elif expected_type == "integer":
        test_case.assertTrue(isinstance(value, int) and not isinstance(value, bool), path)
    elif expected_type == "boolean":
        test_case.assertIsInstance(value, bool, path)


def assert_schema_subset(test_case, payload: Any, schema: dict[str, Any], path: str = "root") -> None:
    expected_type = schema.get("type")
    if isinstance(expected_type, str):
        _validate_type(test_case, payload, expected_type, path)

    if "enum" in schema:
        test_case.assertIn(payload, schema["enum"], path)

    if "minimum" in schema:
        test_case.assertGreaterEqual(payload, schema["minimum"], path)

    if expected_type == "object":
        required = schema.get("required", [])
        for key in required:
            test_case.assertIn(key, payload, f"{path}.{key}")
        properties = schema.get("properties", {})
        for key, sub_schema in properties.items():
            if key in payload:
                assert_schema_subset(test_case, payload[key], sub_schema, f"{path}.{key}")
        additional = schema.get("additionalProperties")
        if isinstance(additional, dict):
            for key, value in payload.items():
                if key not in properties:
                    assert_schema_subset(test_case, value, additional, f"{path}.{key}")

    if expected_type == "array":
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(payload):
                assert_schema_subset(test_case, item, item_schema, f"{path}[{index}]")


def tutorial_commands() -> list[list[str]]:
    markdown = (repo_root() / "docs" / "tutorials" / "e2e-walkthrough-端到端教程.md").read_text(encoding="utf-8")
    commands: list[list[str]] = []
    inside = False
    block: list[str] = []
    for raw in markdown.splitlines():
        line = raw.rstrip("\n")
        if line.startswith("```"):
            if inside:
                text = "\n".join(block).strip()
                merged: list[str] = []
                current = ""
                for part in text.splitlines():
                    stripped = part.strip()
                    if not stripped or stripped.startswith("#") or stripped.startswith("cd "):
                        continue
                    if stripped.endswith("\\"):
                        current += stripped[:-1].rstrip() + " "
                        continue
                    current += stripped
                    merged.append(current.strip())
                    current = ""
                for command in merged:
                    if not command.startswith("python -m aidrp "):
                        continue
                    tokens = shlex.split(command, posix=True)
                    commands.append(tokens[3:])
                inside = False
                block = []
            else:
                inside = True
                block = []
            continue
        if inside:
            block.append(line)
    return commands


def readme_command_list() -> list[str]:
    lines = (repo_root() / "README.md").read_text(encoding="utf-8").splitlines()
    commands: list[str] = []
    collecting = False
    for line in lines:
        stripped = line.strip()
        if stripped == "当前支持：":
            collecting = True
            continue
        if collecting and stripped.startswith("按阶段组织的命令说明见："):
            break
        if collecting and stripped.startswith("- `") and stripped.endswith("`"):
            commands.append(stripped[3:-1])
    return commands
