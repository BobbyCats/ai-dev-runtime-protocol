# Open-Source Inspiration

This repository does not try to clone any single project. It borrows specific strengths from several strong public systems.

## Aider

Reference: [Aider](https://github.com/Aider-AI/aider)

Borrowed idea:

- keep a compact map of the repository so the agent does not need to read everything every time

How it shows up here:

- `repo-map`
- seed files
- candidate file ranking

## OpenHands

Reference: [OpenHands](https://github.com/OpenHands/OpenHands)

Borrowed idea:

- separate runtime work from evaluation and operational workflows

How it shows up here:

- explicit artifact workflow instead of free-form chat only
- task/debug/eval separation
- CI smoke checks for the toolkit itself

## HyperAgent

Reference: [HyperAgent](https://github.com/FSoft-AI4Code/HyperAgent)

Borrowed idea:

- software engineering agents need explicit navigation and execution structure

How it shows up here:

- task packets to narrow navigation
- debug packs for fault localization
- clear hand-off between triage, edit, and verification

## OpenTelemetry

Reference: [OpenTelemetry trace-log correlation](https://opentelemetry.io/bn/docs/zero-code/obi/trace-log-correlation/)

Borrowed idea:

- traces and logs become much more useful once they share identifiers

How it shows up here:

- debug packs carry `trace_id`
- decision traces are first-class artifacts
- the recommended workflow expects logs, traces, and validation output to point to the same task
