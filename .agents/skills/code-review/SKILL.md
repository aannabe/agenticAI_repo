---
name: code-review
description: Review code changes for correctness, security, readability and test coverage, and report findings by severity. Use when the user asks to review, audit, critique or sanity-check code, a diff, a branch or a pull request, or asks "is this OK?" about code they or an agent wrote.
---

# Code review

1. **Get the change.** Use read-only git: `git status`, `git diff` (add `--staged` if relevant),
   `git log -p -n 3`. Read only the files the diff touches, plus callers when behavior changes.
2. **Check, in this order:**
   - *Correctness:* logic errors, off-by-one, edge cases (empty, null, huge, negative), error handling,
     resource cleanup, concurrency hazards.
   - *Security:* see the `security` skill (input validation, secrets, injection, unsafe APIs).
   - *Tests:* is new or changed behavior covered? Do the tests fail without the change?
   - *Readability and simplicity:* clear names, small functions, needless abstraction or
     dependencies, missing comments on obscure logic, stale comments.
   - *Performance:* only when it plausibly matters (hot loops, repeated I/O, quadratic behavior).
3. **Run the project's verify commands** from the language skill if you have not already.
4. **Report** concisely. For each finding give `file:line`, what is wrong, why it matters and a
   suggested fix. Group as **Must fix**, **Should fix**, **Nit**. Finish with a one-line verdict.
   Do not rewrite the code unless asked, and do not nitpick what a formatter or linter enforces.
