# AGENTS

This repository exists to reduce wasted context and improve debugging discipline in AI-assisted development.

## Working Rules

- Read [ONBOARDING.md](ONBOARDING.md) before major edits.
- Prefer generating `.aidrp/` artifacts over broad repository scans.
- For any non-trivial code change, create a task packet first.
- For any bug, create a debug pack before proposing a fix.
- When reasoning changes direction, record it in a decision trace.
- When a bug is fixed, create or update an eval case.

## Validation

- Run `python -m unittest discover -s tests -v`
- Run `python -m aidrp repo-map --project-root . --output-dir .aidrp`

## Editing Scope

- Keep the toolkit dependency-free at runtime.
- Favor JSON artifacts and deterministic outputs.
- Avoid model-specific assumptions in core logic.
