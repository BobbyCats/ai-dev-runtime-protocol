# Eval Case | 回归用例: Regression for meeting deletion drift 会议删除漂移回归用例

- Eval ID | 用例 ID: `regression-for-meeting-deletion-drift-会议删除漂移回归用例`
- Origin | 来源: `debug-pack:meeting-deletion-drift-会议删除漂移`
- Command | 命令: `python -m unittest`

## Reproduction Steps | 复现步骤

- 删除会议列表中的第二条会议

## Assertions | 断言

- 只能删除目标会议，其他会议必须保持不变

## Tags | 标签

- `bugfix`
- `meeting`
- `delete`
