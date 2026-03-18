# Onboarding

This repository is for teams and solo builders who already know how to prompt an AI agent, but need the agent to behave like a disciplined runtime.

## The Core Shift

Move from:

- "read the repo and help me"

to:

- "work from explicit runtime artifacts and only expand context when evidence requires it"

## Default Operating Model

1. Initialize `.aidrp/`
2. Generate a repo map
3. Generate a task packet or debug pack
4. Limit reading to the packet shortlist first
5. Log major decisions in a trace
6. Convert proven failures into eval cases

## Red Flags This Toolkit Is Meant To Prevent

- the agent scans the entire repo for a local bug
- the same architecture explanation is repeated every session
- logs are present but not correlated to a task or trace
- a production bug is fixed once but never becomes a reusable test asset
- validation commands are unclear or too slow to be run consistently

## Required Artifacts

- `.aidrp/repo-map.json`
- `.aidrp/repo-map.md`
- `.aidrp/tasks/*.json` and `*.md` for scoped work
- `.aidrp/debug/*.json` and `*.md` for bugs
- `.aidrp/traces/*.json` for decision history
- `.aidrp/evals/*.json` and `*.md` for regression hardening

## How To Roll This Into Another Project

1. Install this package or copy the relevant files.
2. Run `python -m aidrp init-workspace --project-root /path/to/project`.
3. Customize `.aidrp/config.json`.
4. Commit `.aidrpignore`, config, and the generated `AGENTS.md`.
5. Add packet and debug generation to your normal workflow.

## If You Only Adopt Three Things

- Commit a repo map.
- Require a debug pack before broad bugfix work.
- Turn confirmed production bugs into eval cases.
