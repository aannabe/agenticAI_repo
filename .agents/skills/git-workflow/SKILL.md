---
name: git-workflow
description: Prepare commits, commit messages, branch names, PR descriptions and change summaries WITHOUT committing or pushing. Use when the user asks for a commit message, a summary of changes, a PR description, a changelog entry, or help with git history and branching.
---

# Git workflow (read-only by default)

- **Never** run `git commit`, `git push`, `git tag`, `git remote`, `git reset`, `git rebase`,
  `git merge` or `gh pr/issue/release` unless the user explicitly asks in this conversation.
  Read-only commands are fine: `git status`, `git diff`, `git log`, `git show`, `git branch --list`.
- **Commit message:** Conventional Commits. `type(scope): imperative summary` (<= 72 chars), blank
  line, then a short body explaining *why*. Types: feat, fix, docs, refactor, test, chore, build, ci.
- **Suggest commit boundaries:** one logical change per commit; list which files go in each.
- **PR description:** what and why, how it was tested (commands + results), risks, follow-ups.
- **Branch names:** `type/short-description`, e.g. `feat/csv-export`.
- Never rewrite published history or commit secrets, build outputs, or `.venv`/`build/` folders.
  If something sensitive was staged, tell the user instead of fixing history yourself.
