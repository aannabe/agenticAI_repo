---
name: bash
description: Conventions for safe, portable, readable Bash scripts (strict mode, quoting, shellcheck, shfmt, macOS/Linux/Git-Bash portability). Use whenever creating or editing .sh files, shell scripts, CI/helper scripts, or Bash one-liners that will be saved in the repo.
---

# Bash

Advisory defaults. Deviate when there is a good reason, and say why.

## Skeleton
```bash
#!/usr/bin/env bash
set -euo pipefail # exit on error, on unset variable, and on pipe failures

usage() { echo "Usage: ${0##*/} [--dry-run] <arg>"; }

main() {
  # parse arguments, validate input, then do the work
  :
}

main "$@" # entry point: pass all arguments through unchanged
```
- Put logic in functions; keep top-level code to `main "$@"`. Provide `usage()` and `--help`.
- Use `trap cleanup EXIT` and `mktemp` for temporary files.
- Find the script's own directory with
  `SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"`.

## Safety and style
- Quote every expansion: `"$var"`, `"${arr[@]}"`. Use `[[ ... ]]`, `$(...)`, arrays and `read -r`.
- Never parse `ls`; use globs or `find -print0`. Avoid `eval`. Do not build commands as strings.
- Validate input and required tools up front (`command -v tool >/dev/null || { echo ...; exit 1; }`).
- Destructive operations get a `--dry-run` flag or a confirmation prompt.
- Comment non-obvious syntax (parameter expansion, redirections, process substitution, traps):
  Bash is easy to misread.
- Keep Bash for glue and orchestration. If logic grows (data parsing, math, JSON), suggest Python.

## Portability (macOS, Linux, Windows via Git Bash/WSL)
- macOS ships Bash 3.2: avoid Bash 4+ features (associative arrays, `mapfile`, `${var,,}`) unless
  the script documents a newer Bash requirement.
- GNU and BSD tools differ (`sed -i`, `date`, `readlink -f`, `xargs`, `grep -P`). Use portable
  forms or detect the difference.
- Files must use LF line endings (enforced by `.gitattributes`). Make scripts executable
  (`chmod +x`).

## Verify before presenting (iterate, at most 5 attempts)
1. `shellcheck path/to/script.sh`. Fix findings; justify any `# shellcheck disable=` inline.
2. `shfmt -d path/to/script.sh` (indent settings come from `.editorconfig`); apply with `shfmt -w`.
3. Run it with sample input (use `--dry-run` for anything destructive).
