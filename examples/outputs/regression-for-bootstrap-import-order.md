# Eval Case: Regression for bootstrap import order

- Eval ID: `regression-for-bootstrap-import-order`
- Origin: `debug-pack:cli-import-failure-on-fresh-setup`
- Command: `python -m unittest discover -s tests -v`

## Reproduction Steps

- Install the package before running tests.

## Assertions

- The test suite imports aidrp successfully.

## Tags

- `bootstrap`
- `unittest`
