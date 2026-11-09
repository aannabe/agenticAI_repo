---
name: python
description: Conventions for Python projects managed with uv (pandas/numpy-first, few dependencies, type hints, ruff, pytest). Use whenever creating or editing .py files, pyproject.toml or uv.lock, running or packaging Python scripts (including plotting or data-analysis helpers inside a C++ or Bash project), or managing Python dependencies.
---

# Python (uv)

Advisory defaults. Deviate when there is a good reason, and say why.

## Environment: uv only
- Use uv for everything: `uv run <cmd>`, `uv sync`, `uv add <pkg>`, `uv add --dev <pkg>`,
  `uv remove <pkg>`. No bare `pip install`, no hand-made virtualenvs.
- **Ask before adding any dependency** (`uv add`): name it, say why, mention alternatives.
- Commit `pyproject.toml` and `uv.lock`. Never edit `uv.lock` by hand.
- In this template Python code lives in `python/` (tests in `python/tests/`) so it does not clash
  with C++ `src/`. The project is script-style (`package = false`). For a distributable
  package, use `uv init --package` and keep it in its own subfolder.

## Style
- **Numeric or tabular work:** use numpy / pandas vectorized operations rather than hand-written
  loops or extra libraries (no `iterrows` loops; prefer column operations). For plain scripts that
  do not need them, stay on the standard library. Plotting default: matplotlib (ask before adding).
- Type hints on function signatures; docstrings on public functions; small functions with clear names.
- `pathlib.Path` for paths, f-strings, `dataclasses` for simple records, `with open(..., encoding="utf-8")`.
- CLI scripts: an `argparse` parser, a `main()` function, and `if __name__ == "__main__":`.
- Run external programs with `subprocess.run([...], check=True)` (a list, never `shell=True`),
  so it behaves the same on macOS, Linux and Windows.
- Comment generously: algorithms, vectorization tricks, units, non-obvious pandas/numpy calls.
- Use simple functions first; add classes only when they model real state plus behavior.

## Verify before presenting (iterate, at most 5 attempts)
1. `uv run ruff check .` and `uv run ruff format .`
2. `uv run pytest` (tests live in `python/tests/`). With no tests yet, run the script on a small example.
3. Add or update a test for new behavior or a bug fix.
