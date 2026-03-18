# Prompt Starters

## Task Packet First

Read `.aidrp/repo-map.md`, then create or open the relevant task packet. Do not scan unrelated files until the packet shortlist is exhausted.

## Debug Pack First

Open the relevant debug pack and reproduce the failure before suggesting a fix. Use the triage read order and suspected files first.

## Trace Discipline

Whenever your hypothesis changes or you widen scope, append a decision trace event with the reason.

## Eval Discipline

When a bug is confirmed and fixed, create an eval case so the failure becomes part of the stable verification set.
