---
name: debugging
description: Systematic debugging of failing builds, crashes, wrong output, flaky tests and sanitizer reports. Use when something fails, errors, hangs or behaves unexpectedly, or the user says "it doesn't work", pastes a stack trace or compiler error, or asks to find the cause of a bug.
---

# Debugging

1. **Reproduce.** Get the exact command, input and error. Make it fail reliably and as small as possible.
2. **Read the evidence** before touching code: the full error, the first error (not the last), stack
   trace, sanitizer output, and the relevant lines (not whole files).
3. **Form 2-3 hypotheses**, rank them, and test the cheapest first with a targeted print/log,
   a smaller input, a debugger, or a sanitizer (C++ debug preset has ASan/UBSan).
4. **Narrow down.** Bisect by hand: disable half the code or inputs, or compare against the last
   working state with read-only git (`git diff`, `git log`). Do not run `git bisect`, `git stash`
   or `git checkout` without asking.
5. **Fix the root cause**, not the symptom. Do not silence errors, add blanket `try/except`, or
   suppress warnings to make output disappear.
6. **Prove it.** Add a regression test, run the full verify loop, and remove temporary debug output.
7. **Stop after 5 failed attempts.** Report what you observed, what you ruled out and what you
   would try next; ask the user for missing information.
