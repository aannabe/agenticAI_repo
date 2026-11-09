---
name: security
description: Security and safety checklist for code, scripts and dependencies (secrets, input validation, injection, unsafe APIs, dependency hygiene). Use when handling user input, files, paths, shell commands, network access, credentials or authentication, adding dependencies, or when the user asks for a security review.
---

# Security

- **Secrets:** never hardcode or log keys, tokens or passwords; load from environment or a secrets
  manager; keep `.env` out of git; do not read credential files.
- **Validate all external input** (arguments, files, network data): type, length, range, allowed
  characters. Fail closed with a clear error.
- **No command injection:** Python `subprocess.run([...])` as a list, never `shell=True` with
  user input; Bash quote every expansion and avoid `eval`; C++ avoid `system()`/`popen()` with
  unvalidated strings.
- **Paths and files:** resolve and check paths against an allowed base directory (path traversal);
  create temp files securely (`mktemp`, `tempfile`); least-privilege permissions.
- **Memory safety (C/C++):** bounds checks, RAII, no raw owning pointers, no unchecked
  `memcpy`/`strcpy`/`sprintf` (see the `cpp` skill); run the sanitizer build.
- **Dependencies:** minimal, from trusted sources, version-pinned (`uv.lock`, pinned FetchContent
  tags). Ask before adding any; mention maintenance status and license.
- **Errors and logs:** no stack traces, secrets or personal data in user-facing messages or logs.
- Report any vulnerability you notice, even outside the task, instead of silently fixing it.
