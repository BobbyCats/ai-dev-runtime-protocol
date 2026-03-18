# Eval Case | 回归用例: Regression for bootstrap import order 首次安装导入顺序回归用例

- Eval ID | 用例 ID: `regression-for-bootstrap-import-order-首次安装导入顺序回归用例`
- Origin | 来源: `debug-pack:cli-import-failure-首次安装导入失败`
- Command | 命令: `python -m unittest discover -s tests -v`

## Reproduction Steps | 复现步骤

- Install the package before running tests 先安装再运行测试

## Assertions | 断言

- The test suite imports aidrp successfully 测试套件可以正确导入 aidrp

## Tags | 标签

- `bootstrap`
- `unittest`
