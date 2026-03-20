# Tool Contract | 工具契约: delete_event

- Contract ID | 契约 ID: `delete_event`
- Generated | 生成时间: `2026-03-20T18:22:39+00:00`
- Domain | 所属领域: schedule

## Purpose | 用途

Delete an event by stable ID.

## Input | 输入

- `event_id` (string, required): Stable event identifier.
- `actor_id` (string, required): User performing the deletion.

## Output | 输出

- `deleted` (boolean): Whether deletion succeeded.
- `deleted_event_id` (string): Stable identifier of the deleted event.

## Guardrails | 护栏

- Idempotency | 幂等规则: Deleting an already deleted event is a no-op.
- Permission Boundary | 权限边界: Only schedule domain may delete schedule events.
- Retry Policy | 重试策略: No automatic retry.
- Rollback Policy | 回滚策略: Restore from event snapshot only.

## Failure Codes | 失败码

- `EVENT_NOT_FOUND`: Target event is missing. | 调用方处理: Show error and stop.
- `VERSION_MISMATCH`: Event version is stale. | 调用方处理: Refresh event snapshot before retry.
