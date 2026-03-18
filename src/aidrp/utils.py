from __future__ import annotations

import fnmatch
import hashlib
import json
import re
import subprocess
from collections.abc import Iterable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TEXT_EXTENSIONS = {
    ".c",
    ".cc",
    ".cfg",
    ".conf",
    ".cpp",
    ".cs",
    ".css",
    ".csv",
    ".env",
    ".go",
    ".graphql",
    ".h",
    ".hpp",
    ".html",
    ".ini",
    ".java",
    ".js",
    ".json",
    ".jsx",
    ".kt",
    ".kts",
    ".md",
    ".mjs",
    ".php",
    ".properties",
    ".ps1",
    ".py",
    ".rb",
    ".rs",
    ".scss",
    ".sh",
    ".sql",
    ".svg",
    ".swift",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".vue",
    ".xml",
    ".yaml",
    ".yml",
}

LANGUAGE_BY_EXTENSION = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".json": "json",
    ".md": "markdown",
    ".toml": "toml",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".sh": "shell",
    ".ps1": "powershell",
    ".css": "css",
    ".scss": "scss",
    ".html": "html",
    ".sql": "sql",
    ".go": "go",
    ".rs": "rust",
    ".java": "java",
    ".kt": "kotlin",
    ".swift": "swift",
}

DEFAULT_IGNORE_GLOBS = [
    ".git/*",
    ".venv/*",
    "venv/*",
    "__pycache__/*",
    ".pytest_cache/*",
    ".mypy_cache/*",
    "node_modules/*",
    "dist/*",
    "build/*",
    "coverage/*",
    ".next/*",
    ".turbo/*",
    ".idea/*",
    ".vscode/*",
    ".aidrp/cache/*",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "task"


def sha1_text(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: dict[str, Any] | list[Any]) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, content: str) -> None:
    ensure_parent(path)
    path.write_text(content, encoding="utf-8")


def read_text(path: Path, max_chars: int | None = None) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if max_chars is None:
        return text
    return text[:max_chars]


def is_text_file(path: Path) -> bool:
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    try:
        with path.open("rb") as handle:
            chunk = handle.read(1024)
        return b"\x00" not in chunk
    except OSError:
        return False


def detect_language(path: Path) -> str:
    return LANGUAGE_BY_EXTENSION.get(path.suffix.lower(), "text")


def relative_path(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def count_lines(text: str) -> int:
    if not text:
        return 0
    return text.count("\n") + 1


def load_ignore_patterns(project_root: Path) -> list[str]:
    patterns = list(DEFAULT_IGNORE_GLOBS)
    ignore_file = project_root / ".aidrpignore"
    if ignore_file.exists():
        for line in ignore_file.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                patterns.append(stripped)
    return patterns


def should_ignore(rel_path: str, patterns: Iterable[str]) -> bool:
    for pattern in patterns:
        normalized = pattern.replace("\\", "/")
        if fnmatch.fnmatch(rel_path, normalized):
            return True
        if rel_path == normalized.rstrip("/"):
            return True
    return False


def iter_repo_files(project_root: Path, max_file_size_kb: int) -> list[Path]:
    patterns = load_ignore_patterns(project_root)
    candidates: list[Path] = []
    for path in project_root.rglob("*"):
        if not path.is_file():
            continue
        rel = relative_path(path, project_root)
        if should_ignore(rel, patterns):
            continue
        try:
            if path.stat().st_size > max_file_size_kb * 1024:
                continue
        except OSError:
            continue
        if not is_text_file(path):
            continue
        candidates.append(path)
    return sorted(candidates)


def git_output(project_root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=project_root,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except OSError:
        return ""
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def git_status(project_root: Path) -> dict[str, Any]:
    return {
        "branch": git_output(project_root, "branch", "--show-current"),
        "head": git_output(project_root, "rev-parse", "HEAD"),
        "dirty": bool(git_output(project_root, "status", "--short")),
    }


def tokenize(*parts: str) -> list[str]:
    text = " ".join(parts)
    tokens = {
        token
        for token in re.findall(r"[a-zA-Z0-9_]{3,}", text.lower())
        if token not in {"the", "with", "from", "that", "this", "task", "file", "code"}
    }
    return sorted(tokens)


def score_text_match(text: str, tokens: Iterable[str]) -> int:
    lowered = text.lower()
    return sum(1 for token in tokens if token in lowered)


def compact_excerpt(text: str, needle: str, radius: int = 180) -> str:
    lowered = text.lower()
    index = lowered.find(needle.lower())
    if index < 0:
        snippet = text[: radius * 2]
    else:
        start = max(0, index - radius)
        end = min(len(text), index + len(needle) + radius)
        snippet = text[start:end]
    return re.sub(r"\s+", " ", snippet).strip()
