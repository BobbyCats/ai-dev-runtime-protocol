# Bugfix Playbook

Use this when a user reports a bug, a test fails unexpectedly, or production behavior drifts from the intended result.

## Sequence

1. Generate or refresh the repo map.
2. Create a debug pack.
3. Reproduce the bug before editing.
4. Read only the triage shortlist first.
5. Record hypothesis changes in a decision trace.
6. Patch the smallest surface that explains the bug.
7. Add or update an eval case.
8. Run the relevant validation commands.

## Rules

- Do not scan the entire repo unless the triage set fails to explain the issue.
- Do not change behavior before reproduction unless the issue is a trivial typo or syntax error.
- Do not close the bug without an eval artifact when the issue had real user impact.
- Do not bury new assumptions in chat only; put them in the trace or packet.

## Minimum Artifacts

- `repo-map`
- `debug-pack`
- `decision-trace`
- `eval-case`
