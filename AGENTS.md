# AGENTS.md — universal instructions for AI coding agents

These rules apply to every agent (GitHub Copilot, Claude, Gemini, ...) and every language.
This file is loaded into every session, so it is deliberately short. Language- and
task-specific guidance lives in **skills** (see below). Everything here is an advisory
default: if a rule clearly does not fit the situation, use judgment and say why.

## Skills: load only what you need
- Skills live in `.agents/skills/<name>/SKILL.md` (`.claude/skills` is a link to the same folder).
- If your tool lists skills automatically, use that. Otherwise list `.agents/skills/`, read only
  the `name`/`description` header of each `SKILL.md`, and open the full file for the ones that
  match your task.
- Mixed-language repo? Load a language skill only when you touch that language's files
  (`cpp` for `.cpp/.hpp/CMakeLists.txt`, `python` for `.py/pyproject.toml`, `bash` for `.sh`).
- Do not load unrelated skills "just in case"; it wastes context.

## Principles
1. **Clarity over cleverness.** Write code a human can read, understand and edit later.
2. **Keep it simple.** Use object-oriented design only when it models real state plus behavior;
   otherwise prefer plain functions and data. No abstractions, options or generality for
   hypothetical future needs.
3. **Comment generously and usefully.** Explain obscure syntax, logic, algorithms, units,
   assumptions and the *why*. Skip comments that merely restate trivial code (e.g. `i++`).
4. **Few dependencies.** Prefer the standard library and what the project already uses.
5. **Small, focused changes.** Do not reformat or refactor unrelated code. If a requirement is
   ambiguous, ask one concise question before building.

## Workflow
1. **Orient:** read `docs/CODEMAP.md`, then search for what you need (see Token efficiency).
2. **Load skills** for the languages/tasks involved.
3. **Implement** in small steps.
4. **Verify and iterate** (next section) before showing code to the user.
5. **Report:** what changed, how you verified it (commands + result), assumptions, and anything
   unresolved. Suggest a commit message, but do not commit.

## Verify before presenting code
Build/compile, lint and run tests using the commands in the language skill. If a step fails,
read the error, fix the cause and re-run. Make at most **5 attempts** per problem; then stop
and report what fails, what you tried and your best hypothesis. Never present code you have not
compiled or run without saying so. Never weaken or delete tests just to make them pass.

## Boundaries: ask first
Unless the user explicitly asks, do **not**:
- run `git commit`, `git push`, open PRs/issues, or change git remotes/config. Read-only git
  (`status`, `diff`, `log`, `show`) is fine. Leave changes in the working tree.
- add, remove or upgrade a dependency in any form (`uv add`, `pip install`, CMake
  `FetchContent`, system packages). Propose it with the reason and alternatives, then wait.
- run destructive or system-wide commands (`rm -rf`, `sudo`, force flags, global installs) or
  delete files you did not create.
- write secrets into files, or read `.env` / credential files.

## Token efficiency
- Read `docs/CODEMAP.md` before exploring. Search (grep / symbol search) before opening files;
  read line ranges, not whole files.
- Skip lock files, `build/`, `.venv/`, vendored and generated code unless the task is about them.
- Limit noisy command output (`| tail -n 40`, `grep`, quiet flags).
- Keep `docs/CODEMAP.md` current when you add, remove or rename files/modules
  (see the `docs-and-codemap` skill).

## Platforms
This repo must work on macOS, Linux and Windows. Prefer cross-platform tools (`cmake --preset`,
`uv`, `pathlib`); never hardcode path separators. Shell scripts need Bash (Git Bash or WSL on
Windows) and LF line endings. Use the shell the user actually has (PowerShell on Windows).
