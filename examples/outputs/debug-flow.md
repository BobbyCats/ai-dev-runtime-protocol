# Cost & Privacy Budget | 成本权限预算: debug flow

- Budget ID | 预算 ID: `debug-flow`
- Generated | 生成时间: `2026-03-20T18:22:39+00:00`
- Scope | 适用范围: production bug triage

## Context Budget | 上下文预算

- `seed_file_limit`: `12`
- `candidate_file_limit`: `10`
- `hard_file_cap`: `24`
- `max_file_chars`: `18000`
- `max_snippet_chars`: `1200`

## Reasoning Budget | 推理预算

- `default_profile`: `balanced`
- `upgrade_triggers`: 只有证据不足时，才允许扩大上下文或升级推理强度。

## Permission Budget | 权限预算

- `allowed_tools`: read, grep
- `confirmation_required`: delete

## Data Budget | 数据预算

- `log_safe_fields`: trace_id, request_id, decision_id, plan_id, tool_call_id
- `redact_fields`: token, cookie
- `forbidden_export_fields`: invoice_image
