# AI Dev Runtime Protocol

Runtime-oriented protocol for observable, context-efficient AI development.

This repository is designed for the problem that appears after "AI can write code" is no longer the bottleneck:

- the agent reads too much
- bug fixing drifts off target
- context windows explode
- token costs spike
- issue triage is slow
- production failures do not turn into stable regression coverage

`ai-dev-runtime-protocol` turns those failure modes into explicit runtime artifacts:

- `repo-map`: a compact, machine-readable summary of the repository
- `task-packet`: a scoped work order with read order, file shortlist, constraints, and validation commands
- `debug-pack`: a bug triage bundle with evidence, suspected files, recent commits, and next actions
- `decision trace`: a structured record of why the agent changed direction
- `eval-case`: a regression artifact created from a confirmed failure

The goal is simple: stop making agents re-discover the same context on every turn.

## Why This Exists

Most agent workflows already have decent prompt templates and project rules. The missing layer is runtime discipline:

- what is the smallest reliable context slice for this task?
- which files should the agent read first?
- what evidence justified the change?
- how does a bug become a reusable regression case?

This repository answers those questions with a small Python CLI, JSON schemas, Markdown templates, and playbooks.

## What You Get

- A cross-platform CLI with no runtime dependencies outside the Python standard library
- Workspace scaffolding for `.aidrp/` artifacts
- Repo scanning with seed files, commands, and candidate file ranking
- Task, debug, trace, and eval artifacts in both JSON and Markdown
- JSON schemas for integrating with other agents or tools
- Playbooks for bugfix and feature work
- Adapters for common project shapes
- CI and tests for the toolkit itself

## Install

```bash
python -m pip install -e .
```

## Quick Start

Initialize a target project:

```bash
python -m aidrp init-workspace --project-root . --write-agents-template
```

Generate a repository map:

```bash
python -m aidrp repo-map --project-root . --output-dir .aidrp
```

Create a scoped task packet before changing code:

```bash
python -m aidrp task-packet \
  --project-root . \
  --title "Fix schedule deletion drift" \
  --objective "Fix the deletion path without broadening scope." \
  --type bugfix \
  --scope "Only touch deletion flow and its tests." \
  --acceptance "Deletion uses the correct event identity." \
  --constraint "Do not rewrite unrelated scheduling logic." \
  --search-term delete \
  --search-term schedule
```

Create a debug pack before deep debugging:

```bash
python -m aidrp debug-pack \
  --project-root . \
  --title "Schedule deletion bug" \
  --symptom "Deleting one event removes the wrong item" \
  --observed "UI reports success but the wrong row disappears" \
  --expected "Only the targeted event should be deleted" \
  --impact "Users lose trust in scheduling data" \
  --trace-id trace-2026-03-18-001 \
  --repro-step "Open the schedule page." \
  --repro-step "Delete the second item in the list." \
  --repro-step "Observe that the wrong item is removed." \
  --suspected-file src/schedule/delete.py \
  --search-term delete \
  --search-term event
```

Start and append a decision trace:

```bash
python -m aidrp trace-start --title "Fix schedule deletion drift" --task-id fix-schedule-deletion-drift
python -m aidrp trace-event \
  --trace-file .aidrp/traces/fix-schedule-deletion-drift.json \
  --stage investigate \
  --summary "Confirmed identity mismatch in delete handler." \
  --file src/schedule/delete.py \
  --command "python -m unittest" \
  --outcome "Need targeted patch"
```

Convert a confirmed bug into an eval case:

```bash
python -m aidrp eval-case \
  --title "Regression for schedule deletion drift" \
  --origin "debug-pack:schedule-deletion-bug" \
  --command "python -m unittest" \
  --repro-step "Delete the second item in the schedule list." \
  --assertion "Only the targeted event is removed." \
  --tag bugfix \
  --tag schedule
```

## Intended Workflow

1. Initialize `.aidrp/` in the target repository.
2. Generate and commit a repo map.
3. For every non-trivial task, generate a task packet first.
4. For every bug, generate a debug pack before broad repo scans.
5. Record major reasoning pivots in a decision trace.
6. Convert confirmed bugs into eval cases and add them to the validation path.

## Repository Layout

```text
.
├── AGENTS.md
├── ONBOARDING.md
├── adapters/
├── docs/
├── examples/
├── schemas/
├── src/aidrp/
├── templates/
└── tests/
```

## Design Principles

- Artifacts over chat history: important state should survive the session.
- Read less, decide better: agents should start from packets and repo maps, not whole-repo scans.
- Logs need trace IDs: debugging should be evidence-led, not guess-led.
- Bugs become evals: every expensive production failure should harden the system.
- Keep tools dumb enough to compose: artifacts should be easy to generate, inspect, diff, and reuse.

## References

This repository is influenced by several strong open-source or official projects:

- [Aider](https://github.com/Aider-AI/aider)
- [OpenHands](https://github.com/OpenHands/OpenHands)
- [HyperAgent](https://github.com/FSoft-AI4Code/HyperAgent)
- [OpenTelemetry trace-log correlation](https://opentelemetry.io/bn/docs/zero-code/obi/trace-log-correlation/)

See [docs/reference/open-source-inspiration.md](docs/reference/open-source-inspiration.md) for the mapping from those ideas to this repository.

## Status

This is a pragmatic first release, not a finished framework. The current version intentionally favors:

- explicit artifacts over hidden orchestration
- portable Python scripts over heavy dependencies
- repository-level discipline over model-specific prompting tricks

## License

MIT
