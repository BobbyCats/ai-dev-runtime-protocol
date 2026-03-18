# Adapter | 适配器: Python + FastAPI

适用于：

- Python 服务
- FastAPI 或类似的 Web 框架

## 推荐的 `.aidrp/config.json` 调整

- 把 `src/main.py`、`app/main.py`、`tests/` 放进 `preferred_entry_files`
- 把 `pytest` 或 `python -m unittest` 写进验证命令
- 把 migration、settings、auth 相关路径放进风险区域

## 常见阅读顺序

1. `README.md`
2. `AGENTS.md`
3. `pyproject.toml`
4. `src/main.py` 或 `app/main.py`
5. 路由层
6. 服务层
7. 当前任务包里的候选文件

## 常见风险点

- 请求校验和持久化校验不一致
- 数据库 session 生命周期混乱
- async / sync 边界出错
- 依赖注入静默失效
