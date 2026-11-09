---
name: refactoring
description: Restructure existing code without changing behavior (rename, extract, simplify, de-duplicate, reorganize). Use when the user asks to clean up, simplify, restructure, rename, split or modernize code, or when code is hard to read or duplicated.
---

# Refactoring

1. **Safety net first.** Make sure tests cover the code (see the `testing` skill) and pass. If
   they do not exist, write characterization tests before changing anything.
2. **One kind of change at a time.** Never mix refactoring with new features or bug fixes.
3. **Small steps; verify after each** using the language skill's verify loop.
4. **Prefer simplicity:** delete dead code, flatten nesting, name things clearly, extract a function
   when a block needs a comment to explain it. Do not introduce classes, patterns or abstractions
   unless they remove real duplication or complexity.
5. **Keep public interfaces stable** (function names, CLI flags, file formats) unless the user
   asks to change them; if you must, list every caller you updated (search, do not guess).
6. **Finish:** update comments and `docs/CODEMAP.md` if files or modules moved, and summarize what
   changed and what behavior was verified unchanged.
