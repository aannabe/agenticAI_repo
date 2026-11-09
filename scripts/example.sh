#!/usr/bin/env bash
# Example script showing the project's Bash conventions. Replace it with real scripts.
set -euo pipefail # exit on error, on unset variable, and on failures inside pipes

usage() {
  echo "Usage: ${0##*/} [--dry-run] [--help] [NAME]"
  echo "Prints a greeting. With --dry-run, only shows what would be printed."
}

main() {
  local dry_run=0
  local name="world"

  # Parse arguments; unknown options are an error so typos are not silently ignored.
  while [[ $# -gt 0 ]]; do
    case "$1" in
    --dry-run) dry_run=1 ;;
    -h | --help)
      usage
      return 0
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage >&2
      return 2
      ;;
    *) name="$1" ;;
    esac
    shift # drop the argument we just handled
  done

  if [[ $dry_run -eq 1 ]]; then
    echo "[dry-run] would print: Hello, ${name}!"
  else
    echo "Hello, ${name}!"
  fi
}

main "$@" # pass all command-line arguments through unchanged
