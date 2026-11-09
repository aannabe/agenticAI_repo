# Copilot instructions

Follow [AGENTS.md](../AGENTS.md) in the repo root; it is the single source of truth for all agents.
Language and task guidance lives in `.agents/skills/<name>/SKILL.md`: open the one that matches
the files you are editing.

Repeated here in case a Copilot surface (for example code review) does not load AGENTS.md:
- Prefer clear, simple, well-commented code; avoid adding dependencies without asking.
- Never commit, push or open PRs on your own. Build, lint and test code before presenting it
  (at most 5 fix attempts, then report).
- In reviews, focus on correctness, security and readability; skip style nits the linters cover.
