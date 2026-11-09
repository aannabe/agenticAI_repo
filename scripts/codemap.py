"""Regenerate the machine-written part of docs/CODEMAP.md.

Works for any language and on any OS, using only the Python standard library.

What it writes (between the BEGIN/END GENERATED markers; the rest of the file is never touched):
  * a language summary (files and lines per language, by file extension)
  * a file tree (one block per directory, with line counts)
  * top-level symbols per file, ONLY if universal-ctags (`ctags`) is installed

Run:  uv run --no-project scripts/codemap.py      (or: python3 scripts/codemap.py)
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

BEGIN = "<!-- BEGIN GENERATED (scripts/codemap.py) -->"
END = "<!-- END GENERATED -->"

# Used only when the folder is not a git repository (otherwise `git ls-files` decides).
SKIP_DIRS = {".git", "build", "out", "dist", "node_modules", "__pycache__", ".venv", "venv"}
SKIP_FILES = {"uv.lock", "package-lock.json", "yarn.lock", "poetry.lock", "Cargo.lock"}
MAX_FILE_BYTES = 2_000_000  # larger files are listed but not line-counted
MAX_FILES_PER_DIR = 25  # directories with more files are truncated in the tree
MAX_SYMBOLS_PER_FILE = 12
MAX_SYMBOLS_TOTAL = 300

# File extension -> language name (extend as you add languages).
LANGUAGES = {
    ".py": "Python", ".cpp": "C++", ".cc": "C++", ".cxx": "C++", ".hpp": "C++", ".hh": "C++",
    ".h": "C/C++ header", ".c": "C", ".sh": "Bash", ".bash": "Bash", ".cmake": "CMake",
    ".rs": "Rust", ".go": "Go", ".js": "JavaScript", ".ts": "TypeScript", ".java": "Java",
    ".md": "Markdown", ".json": "JSON", ".toml": "TOML", ".yml": "YAML", ".yaml": "YAML",
}  # fmt: skip

# ctags "kind" values worth listing, with short labels (keeps the output compact).
SYMBOL_KINDS = {
    "function": "fn", "class": "class", "struct": "struct", "namespace": "ns",
    "enum": "enum", "interface": "iface", "module": "mod", "typedef": "type",
}  # fmt: skip


def list_files(root: Path) -> list[Path]:
    """Return repo files (relative paths). Prefers git, so .gitignore is respected."""
    try:
        out = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=root, capture_output=True, text=True, check=True,
        ).stdout  # fmt: skip
        files = [Path(line) for line in out.splitlines() if line]
    except (OSError, subprocess.CalledProcessError):
        # Not a git repo (or git is missing): walk the tree ourselves.
        files = [
            p.relative_to(root)
            for p in root.rglob("*")
            if p.is_file() and not (set(p.relative_to(root).parts[:-1]) & SKIP_DIRS)
        ]
    # `git ls-files` can still list files that were deleted from disk; keep only real files.
    return sorted(f for f in files if f.name not in SKIP_FILES and (root / f).is_file())


def count_lines(path: Path) -> int | None:
    """Count lines in a text file; None for binary or very large files."""
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return None
        data = path.read_bytes()
    except OSError:
        return None
    if b"\0" in data:  # NUL byte => binary file
        return None
    return data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)


def language_of(path: Path) -> str:
    name = path.name
    if name == "CMakeLists.txt":
        return "CMake"
    return LANGUAGES.get(path.suffix.lower(), "Other")


def collect_symbols(root: Path, files: list[Path]) -> dict[str, list[str]]:
    """Ask universal-ctags for top-level symbols. Returns {} if ctags is unavailable."""
    if shutil.which("ctags") is None:
        return {}
    try:
        # -x = human-readable table; -L - = read the file list from stdin.
        proc = subprocess.run(
            ["ctags", "-x", "--sort=no", "-L", "-"],
            cwd=root, input="\n".join(f.as_posix() for f in files),
            capture_output=True, text=True, check=True,
        )  # fmt: skip
    except (OSError, subprocess.CalledProcessError):
        return {}

    symbols: dict[str, list[str]] = defaultdict(list)
    total = 0
    for line in proc.stdout.splitlines():
        parts = line.split(None, 4)  # name, kind, line number, file, source text
        if len(parts) < 4 or parts[1] not in SYMBOL_KINDS:
            continue
        name, kind, _lineno, file = parts[0], parts[1], parts[2], parts[3]
        if len(symbols[file]) < MAX_SYMBOLS_PER_FILE and total < MAX_SYMBOLS_TOTAL:
            symbols[file].append(f"{SYMBOL_KINDS[kind]} {name}")
            total += 1
    return dict(symbols)


def build_section(root: Path, use_symbols: bool) -> str:
    files = list_files(root)
    lines_of = {f: count_lines(root / f) for f in files}

    # --- language summary ---
    per_lang_files: Counter[str] = Counter()
    per_lang_lines: Counter[str] = Counter()
    for f in files:
        lang = language_of(f)
        per_lang_files[lang] += 1
        per_lang_lines[lang] += lines_of[f] or 0
    out = ["### Languages", "", "| Language | Files | Lines |", "|---|---:|---:|"]
    for lang, n in sorted(per_lang_files.items(), key=lambda kv: (-per_lang_lines[kv[0]], kv[0])):
        out.append(f"| {lang} | {n} | {per_lang_lines[lang]} |")

    # --- file tree, one block per directory ---
    by_dir: dict[str, list[Path]] = defaultdict(list)
    for f in files:
        by_dir[f.parent.as_posix()].append(f)
    out += ["", "### Files (line counts)", "", "```"]
    for directory in sorted(by_dir):
        out.append("./" if directory == "." else f"{directory}/")
        entries = by_dir[directory]
        for f in entries[:MAX_FILES_PER_DIR]:
            n = lines_of[f]
            out.append(f"  {f.name}" + (f" ({n})" if n is not None else ""))
        if len(entries) > MAX_FILES_PER_DIR:
            out.append(f"  ... +{len(entries) - MAX_FILES_PER_DIR} more files")
    out.append("```")

    # --- symbols (optional) ---
    if use_symbols:
        symbols = collect_symbols(root, files)
        if symbols:
            out += ["", "### Top-level symbols (from ctags)", "", "```"]
            for file in sorted(symbols):
                out.append(f"{file}: " + ", ".join(symbols[file]))
            out.append("```")
        else:
            out += ["", "_Symbols: install universal-ctags (`ctags`) to include them._"]
    return "\n".join(out)


def update_file(path: Path, section: str) -> None:
    """Replace the generated block in `path`, creating the file or the block if needed."""
    block = f"{BEGIN}\n{section}\n{END}"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.DOTALL)
        if pattern.search(text):
            # A function replacement avoids backslash handling in the generated text.
            text = pattern.sub(lambda _m: block, text, count=1)
        else:
            text = text.rstrip("\n") + "\n\n## Generated index\n\n" + block + "\n"
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        text = "# Code map\n\n## Generated index\n\n" + block + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate the generated part of CODEMAP.md.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent,
                        help="repository root (default: parent of scripts/)")  # fmt: skip
    parser.add_argument("--output", type=Path, default=Path("docs/CODEMAP.md"),
                        help="map file, relative to --root (default: docs/CODEMAP.md)")  # fmt: skip
    parser.add_argument("--no-symbols", action="store_true", help="skip ctags symbol extraction")
    args = parser.parse_args()

    root = args.root.resolve()
    update_file(root / args.output, build_section(root, use_symbols=not args.no_symbols))
    print(f"Updated {args.output.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
