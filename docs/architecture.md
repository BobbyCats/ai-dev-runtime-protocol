# Architecture

`ai-dev-runtime-protocol` is organized around one idea: chat context is too fragile to be the source of truth for engineering work.

## Layers

### 1. Protocol layer

Human-readable rules and playbooks:

- [README.md](../README.md)
- [ONBOARDING.md](../ONBOARDING.md)
- [AGENTS.md](../AGENTS.md)
- [docs/playbooks/bugfix.md](playbooks/bugfix.md)
- [docs/playbooks/feature.md](playbooks/feature.md)

### 2. Artifact layer

Machine-readable work units and runtime state:

- `repo-map`
- `task-packet`
- `debug-pack`
- `decision-trace`
- `eval-case`

These artifacts exist in both JSON and Markdown so they are easy to use with agents and humans.

### 3. Runtime layer

The CLI in `src/aidrp/` is the runtime glue that generates and updates the artifacts.

## Why Not Just More Prompts?

Prompts do not solve:

- stale context
- repeated repo scans
- traceable reasoning pivots
- converting production failures into reusable verification assets

Artifacts do.

## Why JSON First?

Because JSON can be:

- diffed
- cached
- piped into other tools
- validated by schema
- summarized into Markdown

This lets the same work order be consumed by Codex, Claude, Cursor, OpenHands, or custom agents.

## Why A Thin CLI?

The CLI is intentionally simple:

- standard library only
- works on Windows, macOS, Linux
- easy to patch inside a project
- easy to embed in other workflows

The first release focuses on explicitness over automation.

## Future Directions

- schema validation at runtime
- richer language-aware indexing
- task packet generation from issue trackers
- auto-promoting debug packs into eval harnesses
- tighter CI and artifact freshness checks
