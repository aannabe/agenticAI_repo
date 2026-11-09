---
name: docs-and-codemap
description: Maintain README.md, docs and docs/CODEMAP.md (the compact repo map agents read first to save tokens), and regenerate its file/symbol index with scripts/codemap.py. Use when adding, removing, renaming or moving files or modules, when the user asks to document the project or explain its structure, or when the code map looks stale.
---

# Docs and code map

- `docs/CODEMAP.md` is the first thing agents read. It has two parts:
  1. **Overview** (hand-written, keep it short): what each top-level folder/module is for, entry
     points, and how to build/run/test. Update it whenever structure or responsibilities change.
  2. **Generated index** between the `BEGIN/END GENERATED` markers: file tree with line counts,
     language summary and (if `ctags` is installed) top-level symbols. Never edit it by hand.
- Regenerate after structural changes (works on every OS, standard library only):
  `uv run --no-project scripts/codemap.py`
  (or `python3 scripts/codemap.py`; on Windows `py scripts/codemap.py`).
- Keep `README.md` accurate: purpose, setup, build/run/test commands.
- Keep docs short and concrete. Do not document what the code already says clearly; document
  intent, constraints, and non-obvious decisions. Update comments next to code you change.
