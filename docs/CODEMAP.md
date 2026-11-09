# Code map

Agents: read this file first, then search for what you need instead of opening many files.
The **Overview** is maintained by hand (keep it short). The **Generated index** is rewritten by
`uv run --no-project scripts/codemap.py`; never edit it by hand.

## Overview

| Path | Purpose |
|---|---|
| `AGENTS.md` | Universal agent rules (single source of truth for every AI provider) |
| `.agents/skills/<name>/SKILL.md` | On-demand skills: languages (`cpp`, `python`, `bash`) and tasks |
| `include/myproject/`, `src/` | C++ library and executable (`myproject_core`, `myproject`) |
| `tests/` | C++ tests, run with CTest |
| `python/`, `python/tests/` | Python helper scripts and their pytest tests |
| `scripts/` | Bash scripts and tooling (`codemap.py`) |
| `docs/` | Documentation, including this map |

Build and test:
- C++: `cmake --preset debug`, `cmake --build --preset debug`, `ctest --preset debug`
- Python: `uv run ruff check .`, `uv run pytest`
- Bash: `shellcheck scripts/*.sh`

Entry points: `src/main.cpp` (C++ executable), `python/example_tool.py` (Python CLI),
`scripts/example.sh` (Bash).

## Generated index

<!-- BEGIN GENERATED (scripts/codemap.py) -->
### Languages

| Language | Files | Lines |
|---|---:|---:|
| Markdown | 16 | 581 |
| Python | 3 | 247 |
| JSON | 3 | 106 |
| C++ | 4 | 69 |
| Other | 3 | 49 |
| CMake | 2 | 48 |
| Bash | 1 | 39 |
| TOML | 1 | 26 |

### Files (line counts)

```
./
  .editorconfig (22)
  .gitattributes (7)
  .gitignore (20)
  AGENTS.md (63)
  CLAUDE.md (6)
  CMakeLists.txt (43)
  CMakePresets.json (36)
  GEMINI.md (4)
  README.md (109)
  pyproject.toml (26)
.agents/skills/bash/
  SKILL.md (49)
.agents/skills/code-review/
  SKILL.md (21)
.agents/skills/cpp/
  SKILL.md (67)
.agents/skills/debugging/
  SKILL.md (20)
.agents/skills/docs-and-codemap/
  SKILL.md (18)
.agents/skills/git-workflow/
  SKILL.md (17)
.agents/skills/python/
  SKILL.md (34)
.agents/skills/refactoring/
  SKILL.md (18)
.agents/skills/security/
  SKILL.md (22)
.agents/skills/testing/
  SKILL.md (20)
.claude/
  settings.json (40)
.github/
  copilot-instructions.md (11)
.vscode/
  settings.json (30)
docs/
  CODEMAP.md (102)
include/myproject/
  greeter.hpp (12)
python/
  example_tool.py (41)
python/tests/
  test_example_tool.py (16)
scripts/
  codemap.py (190)
  example.sh (39)
src/
  greeter.cpp (13)
  main.cpp (17)
tests/
  CMakeLists.txt (5)
  test_greeter.cpp (27)
```

_Symbols: install universal-ctags (`ctags`) to include them._
<!-- END GENERATED -->
