# Adapter: Python + FastAPI

Use this when the target project is primarily a Python service with FastAPI or a similar web stack.

## Recommended `.aidrp/config.json` Adjustments

- Add `src/main.py`, `app/main.py`, and `tests/` to preferred entry files.
- Set validation commands around `python -m unittest`, `pytest`, or both.
- Add migration and settings files to risk globs.

## Common Read Order

1. `README.md`
2. `AGENTS.md`
3. `pyproject.toml`
4. `src/main.py` or `app/main.py`
5. routing layer
6. service layer
7. packet shortlist

## Common Risk Areas

- silent dependency injection changes
- database session lifecycle bugs
- partial validation between request schema and persistence schema
- async and sync boundary mistakes
