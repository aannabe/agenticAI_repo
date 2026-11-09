---
name: testing
description: Write, extend and run automated tests with good coverage of behavior and edge cases. Use when adding a feature, fixing a bug, the user asks for tests or coverage, tests fail, or code is about to be refactored without a safety net.
---

# Testing

- **Test behavior, not implementation.** One logical assertion per test, descriptive names
  (`test_empty_name_falls_back_to_default`), arrange / act / assert layout.
- **Always cover:** the normal case, boundaries (empty, one item, maximum), invalid input and error
  paths. For a bug fix, first write a test that fails because of the bug, then fix it.
- **Keep tests deterministic and fast:** no network, no real clock or randomness (inject or seed),
  no order dependence, temp dirs for files. Do not test third-party code.
- **Run commands** (details in the language skills):
  C++ `ctest --preset debug`; Python `uv run pytest`; Bash: run the script on sample input
  (use `bats` only if the user approves adding it).
- **Never** weaken, skip or delete a failing test to get green. If a test is wrong, explain why
  before changing it.
- After writing tests, run them and show the result. If you changed behavior, say which tests
  changed and why.
