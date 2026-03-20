## Stack
- `uv` for package management and running tools. If mise tasks aren't sufficient: `uv run <xyz>`
- pytest

## Code Quality

MUST run `mise run check` after code changes and fix all errors/warnings (0 warnings policy).

MUST NEVER use `# type: ignore` or similar type suppression comments. Fix type errors properly by correcting types, adding proper annotations, or refactoring. If a type error seems unfixable, investigate root cause and solve at the source.

### Mise Tasks

- `mise run check` - full check: ruff lint+fix, ruff format, ty typecheck
- `mise run lint` - ruff lint only
- `mise run format` - ruff format only
- `mise run typecheck` - ty typecheck only

## Testing

MUST prefer fixtures over monkeypatch. Use `tests/conftest.py` or local fixtures for dependency setup. Monkeypatch only when no fixture alternative exists (global/env/module patch points).
