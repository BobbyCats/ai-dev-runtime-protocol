from __future__ import annotations

import ast
import json
import re
import tomllib
from collections import Counter
from pathlib import Path
from typing import Any

from aidrp.utils import (
    count_lines,
    detect_language,
    git_status,
    iter_repo_files,
    now_iso,
    read_text,
    relative_path,
    score_text_match,
    sha1_text,
    write_json,
    write_text,
)
from aidrp.workspace import load_workspace_config


def _classify_role(rel_path: str) -> str:
    lower = rel_path.lower()
    name = Path(rel_path).name.lower()
    if "/tests/" in lower or lower.startswith("tests/") or name.startswith("test_"):
        return "test"
    if name in {"readme.md", "agents.md", "onboarding.md"} or lower.startswith("docs/"):
        return "documentation"
    if lower.startswith(".github/") or name in {"dockerfile", "compose.yml", "compose.yaml"}:
        return "infrastructure"
    if lower.startswith("schemas/"):
        return "schema"
    if any(name.endswith(suffix) for suffix in (".json", ".toml", ".yaml", ".yml", ".ini", ".cfg")):
        return "configuration"
    return "source"


def _parse_python_symbols(text: str) -> tuple[list[str], list[str]]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return [], []
    symbols: list[str] = []
    imports: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            symbols.append(node.name)
        elif isinstance(node, ast.Import):
            for entry in node.names:
                imports.append(entry.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return symbols[:20], imports[:20]


def _parse_ts_like(text: str) -> tuple[list[str], list[str]]:
    symbols = re.findall(
        r"(?:export\s+)?(?:async\s+)?(?:function|class|const|let|var|interface|type)\s+([A-Za-z0-9_]+)",
        text,
    )
    imports = re.findall(r"import\s+.*?from\s+['\"]([^'\"]+)['\"]", text)
    return symbols[:20], imports[:20]


def _parse_headings(text: str) -> list[str]:
    return re.findall(r"^#{1,3}\s+(.+)$", text, flags=re.MULTILINE)[:12]


def _extract_commands(project_root: Path) -> dict[str, list[str]]:
    commands: dict[str, list[str]] = {"npm": [], "python": [], "make": []}

    package_json = project_root / "package.json"
    if package_json.exists():
        try:
            data = json.loads(package_json.read_text(encoding="utf-8"))
            scripts = data.get("scripts", {})
            commands["npm"] = [f"npm run {name}" for name in sorted(scripts)]
        except json.JSONDecodeError:
            pass

    pyproject = project_root / "pyproject.toml"
    if pyproject.exists():
        try:
            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
            project_scripts = data.get("project", {}).get("scripts", {})
            commands["python"] = [f"{name}" for name in sorted(project_scripts)]
        except tomllib.TOMLDecodeError:
            pass

    makefile = project_root / "Makefile"
    if makefile.exists():
        targets = re.findall(r"^([A-Za-z0-9_-]+):", makefile.read_text(encoding="utf-8"), flags=re.MULTILINE)
        commands["make"] = [f"make {target}" for target in targets if not target.startswith(".")]
    return commands


def _summarize_file(path: Path, project_root: Path) -> dict[str, Any]:
    rel = relative_path(path, project_root)
    text = read_text(path)
    language = detect_language(path)
    role = _classify_role(rel)
    symbols: list[str] = []
    imports: list[str] = []
    headings: list[str] = []

    if language == "python":
        symbols, imports = _parse_python_symbols(text)
    elif language in {"javascript", "typescript"}:
        symbols, imports = _parse_ts_like(text)
    elif language == "markdown":
        headings = _parse_headings(text)
        symbols = headings

    score = 0
    if Path(rel).name.lower() in {"readme.md", "agents.md", "onboarding.md", "package.json", "pyproject.toml"}:
        score += 6
    if role in {"source", "test"}:
        score += 2
    score += min(len(symbols), 4)
    score += min(len(imports), 3)

    return {
        "path": rel,
        "language": language,
        "role": role,
        "lines": count_lines(text),
        "symbols": symbols[:12],
        "imports": imports[:12],
        "headings": headings[:10],
        "hash": sha1_text(text)[:12],
        "score": score,
    }


def build_repo_map(project_root: Path) -> dict[str, Any]:
    config = load_workspace_config(project_root)
    files = [
        _summarize_file(path, project_root)
        for path in iter_repo_files(project_root, max_file_size_kb=config["max_file_size_kb"])
    ]
    language_counts = Counter(entry["language"] for entry in files)
    role_counts = Counter(entry["role"] for entry in files)

    preferred = config.get("preferred_entry_files", [])
    preferred_set = set(preferred)
    seed_candidates = sorted(
        files,
        key=lambda item: (
            0 if item["path"] in preferred_set else 1,
            -item["score"],
            item["path"],
        ),
    )
    seed_limit = config["context_budget"]["seed_file_limit"]
    seed_files = [entry["path"] for entry in seed_candidates[:seed_limit]]
    commands = _extract_commands(project_root)

    risk_files = []
    for entry in files:
        for glob in config.get("risk_globs", []):
            if Path(entry["path"]).match(glob):
                risk_files.append(entry["path"])
                break

    return {
        "schema_version": "0.1.0",
        "generated_at": now_iso(),
        "project_root": str(project_root.resolve()),
        "git": git_status(project_root),
        "summary": {
            "file_count": len(files),
            "language_counts": dict(language_counts),
            "role_counts": dict(role_counts),
            "seed_files": seed_files,
            "risk_files": risk_files,
            "commands": commands,
            "context_budget": config["context_budget"],
        },
        "files": files,
    }


def repo_map_to_markdown(repo_map: dict[str, Any]) -> str:
    summary = repo_map["summary"]
    lines = [
        "# Repo Map | 仓库地图",
        "",
        f"- Generated | 生成时间: `{repo_map['generated_at']}`",
        f"- Root | 根目录: `{repo_map['project_root']}`",
        f"- Branch | 分支: `{repo_map['git'].get('branch') or 'unknown'}`",
        f"- Dirty | 有未提交改动: `{repo_map['git'].get('dirty')}`",
        "",
        "## Summary | 概览",
        "",
        f"- Files scanned | 扫描文件数: `{summary['file_count']}`",
        f"- Languages | 语言分布: `{', '.join(f'{k}:{v}' for k, v in sorted(summary['language_counts'].items())) or 'none'}`",
        f"- Roles | 文件角色: `{', '.join(f'{k}:{v}' for k, v in sorted(summary['role_counts'].items())) or 'none'}`",
        "",
        "## Seed Files | 起始文件",
        "",
    ]
    for path in summary["seed_files"]:
        lines.append(f"- `{path}`")

    lines.extend(["", "## Commands | 常用命令", ""])
    for group, values in summary["commands"].items():
        if not values:
            continue
        lines.append(f"- `{group}`: {', '.join(f'`{value}`' for value in values[:8])}")

    lines.extend(["", "## Top Modules | 高信号模块", ""])
    top_files = sorted(repo_map["files"], key=lambda item: (-item["score"], item["path"]))[:20]
    for entry in top_files:
        details = ", ".join(entry["symbols"][:4]) or entry["role"]
        lines.append(f"- `{entry['path']}` ({entry['language']}, {entry['lines']} lines): {details}")
    return "\n".join(lines) + "\n"


def write_repo_map(project_root: Path, output_json: Path, output_markdown: Path) -> dict[str, Any]:
    repo_map = build_repo_map(project_root)
    write_json(output_json, repo_map)
    write_text(output_markdown, repo_map_to_markdown(repo_map))
    return repo_map


def rank_candidate_files(repo_map: dict[str, Any], tokens: list[str], limit: int) -> list[dict[str, Any]]:
    ranked = []
    for entry in repo_map["files"]:
        text = " ".join([entry["path"], *entry.get("symbols", []), *entry.get("imports", [])])
        match_score = score_text_match(text, tokens)
        total_score = entry["score"] + (match_score * 3)
        if total_score <= 0:
            continue
        ranked.append(
            {
                "path": entry["path"],
                "language": entry["language"],
                "role": entry["role"],
                "score": total_score,
                "reason": _candidate_reason(entry, tokens),
            }
        )
    ranked.sort(key=lambda item: (-item["score"], item["path"]))
    return ranked[:limit]


def _candidate_reason(entry: dict[str, Any], tokens: list[str]) -> str:
    hits = []
    haystack = " ".join([entry["path"], *entry.get("symbols", []), *entry.get("imports", [])]).lower()
    for token in tokens:
        if token in haystack:
            hits.append(token)
    if hits:
        return f"Matched tokens: {', '.join(hits[:4])}"
    return f"High-signal {entry['role']} file"
