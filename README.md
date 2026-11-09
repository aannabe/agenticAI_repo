# Agentic coding template

A starter repository for coding with AI agents (GitHub Copilot in VS Code first; Claude and
Gemini work too). It ships with agent instructions, on-demand skills, safe command approvals,
and a small C++ / Python / Bash skeleton you can delete from.

## Quick start

1. Copy this repo (or use it as a GitHub template) and `git init`.
2. Rename the placeholder `myproject` / `MYPROJECT` (folders, CMake, `pyproject.toml`).
   Easiest: ask your agent, *"Rename the placeholder project `myproject` to `<name>` everywhere."*
3. Delete the languages you do not need (see "Pruning" below).
4. Check that everything works:

   | Language | Commands |
   |---|---|
   | C++ | `cmake --preset debug` then `cmake --build --preset debug` then `ctest --preset debug` |
   | Python | `uv run ruff check .` and `uv run pytest` |
   | Bash | `shellcheck scripts/*.sh` and `shfmt -d scripts/` |

5. Optional: `uv run --no-project scripts/codemap.py` to refresh `docs/CODEMAP.md`.

## Layout

```
AGENTS.md                    universal rules for every agent (single source of truth)
CLAUDE.md, GEMINI.md         one-line pointers: @AGENTS.md
.github/copilot-instructions.md   thin pointer for Copilot surfaces
.agents/skills/<name>/SKILL.md    on-demand skills (languages + tasks)
.claude/skills -> ../.agents/skills   link so Claude Code finds the same skills
.vscode/settings.json        Copilot terminal approvals (what runs freely vs. asks you)
.claude/settings.json        Claude Code permissions (same policy)
docs/CODEMAP.md              compact repo map agents read first (saves tokens)
scripts/                     codemap.py + example.sh
include/ src/ tests/         C++ skeleton (CMake + presets, plain CTest)
python/ pyproject.toml uv.lock   Python skeleton (uv, ruff, pytest)
```

## How it works

- **AGENTS.md** is short and always loaded: principles, workflow, "ask first" boundaries,
  token-saving habits. Rules are advisory.
- **Skills** hold the detail and load only when relevant, so a C++ project with a Python
  plotting script only pays for the Python guidance when Python is touched. Language skills:
  `cpp`, `python`, `bash`. Task skills: `code-review`, `testing`, `debugging`, `git-workflow`,
  `security`, `refactoring`, `docs-and-codemap`.
- **Guardrails:** agents may build, lint, test and run read-only git freely. They must ask you
  before `git commit/push`, `gh`, adding dependencies, installs, or deletions. These are set in
  the two settings files; they are real prompts, not just instructions. If VS Code does not
  apply the workspace-level rules on your version, copy that block to your User Settings.
- **Iteration:** agents compile/lint/test their own code and retry up to 5 times, then report.

## Switching or adding an AI provider

| Provider | Reads | Skills from |
|---|---|---|
| Copilot (VS Code, CLI, cloud agent) | `AGENTS.md`, `.github/copilot-instructions.md` | `.agents/skills` |
| Claude Code | `CLAUDE.md` (imports `AGENTS.md`) | `.claude/skills` (link) |
| Gemini CLI / VS Code agent | `GEMINI.md` (imports `AGENTS.md`) | `.agents/skills` |
| Codex and others | `AGENTS.md` | `.agents/skills` |

To support a new tool: if it reads `AGENTS.md` natively, do nothing. Otherwise add a one-line
pointer file for it, like `CLAUDE.md`. Instructions stay in one place.

## Adding a language or a skill

Create one folder; edit nothing else (AGENTS.md tells agents to discover skills from the folder):

```
.agents/skills/rust/SKILL.md
```
```markdown
---
name: rust            # must match the folder name: lowercase letters, digits, hyphens
description: What it covers and WHEN to use it. Name the file types and tasks (".rs files,
  Cargo.toml, cargo build errors ...") so the agent loads it at the right time.
---
# Rust
Advisory conventions, project layout, and a "Verify before presenting" command list.
```
Keep a skill under ~100 lines; move long reference material into a `references/` subfolder and
link to it from the skill. Optionally add the language to `LANGUAGES` in `scripts/codemap.py`.

## Pruning

Do not need a language? Delete its skill folder in `.agents/skills/`, its skeleton files
(C++: `CMakeLists.txt`, `CMakePresets.json`, `include/`, `src/`, `tests/`; Python: `python/`,
`pyproject.toml`, `uv.lock`; Bash: `scripts/example.sh`), the matching rows in
`docs/CODEMAP.md`, and the matching lines in the two settings files.

## Token efficiency and indexing

- Copilot builds a semantic code index automatically. GitHub-hosted repos are indexed once on
  GitHub; for repos not on GitHub, VS Code builds the index by uploading workspace data to
  GitHub (see GitHub's repository-indexing docs). Command: *Build Codebase semantic index*.
- Independent of that, `docs/CODEMAP.md` gives every agent a cheap map (folders, entry points,
  file sizes, optional symbols), and AGENTS.md tells agents to search before reading and to read
  line ranges. `scripts/codemap.py` works for any language using only the Python standard
  library; install universal-ctags to add top-level symbols.
- Skills load on demand; keep AGENTS.md short.

## Platform notes (macOS, Linux, Windows)

- C++: presets hide generator differences. Sanitizers are skipped on Windows/MSVC.
- Shell scripts need Bash (Git Bash or WSL on Windows). `.gitattributes` forces LF endings.
- `.claude/skills` is a symlink. On Windows either enable Developer Mode and
  `git config core.symlinks true` before cloning, or ignore it: `CLAUDE.md`/`AGENTS.md` tell
  Claude to read `.agents/skills/` directly, and Copilot and Gemini do not need the link.
- Python uses `pathlib` and list-style `subprocess` calls, so it behaves the same everywhere.
