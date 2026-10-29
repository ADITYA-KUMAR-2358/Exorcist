# Runtime Validation Report

**Generated**: 2026-10-29T13:16:39+05:30
**Target**: `D:\Exorcist`

## Summary

| Step | Status | Exit Code | Details |
|------|--------|-----------|---------|
| Startup | N/A | n/a | Exorcist is a CLI; no long-running application server is required. |
| Unit/integration tests | PASS | 0 | `python -m pytest -q`: 14 passed. |
| Lint | PASS | 0 | `python -m ruff check exorcist tests`: clean. |
| CLI workflow smoke | PASS | 0/1 as designed | Help, guide, rules, tracks, explain, doctor, scan, report, banish, init, and clone validation exercised. |
| Browser/report smoke | PASS | n/a | Generated static report opened successfully; mascot, counts, Gemma metadata, and zero-network badge rendered. |

**Overall**: PASS

## Environment

```text
Python: 3.12.3
Node.js: v22.13.1
npm: 10.9.2
Playwright CLI: 1.64.1
Docker: unavailable (docker info exit code 1; no container tier needed)
Ollama: project-local and responsive
Gemma: gemma3:4b available locally
```

## Coverage

- Finding model validation and report contracts.
- Scanner families: secrets, dependencies, dead code, and zombie jobs.
- Secret redaction and placeholder metadata.
- Ollama JSON validation, repair retry, and human-review fallback.
- Missing-model behavior.
- JSON scan output parsing.
- HTML report generation and browser rendering.
- CLI help aliases: `--help`, `-h`, and `-help`.
- Tutorial and discovery commands: `help`, `guide`, `rules`, `tracks`, `explain`, and `version`.
- Safety paths: invalid repository, invalid scanner type, empty scanner selection,
  invalid clone depth, dry-run banishment, and guarded PR/apply behavior.
- Local Gemma scan of `jersey-paglu`: 0 findings, exit code 0, 0 network calls.

## Bugs Found and Fixed

| # | Severity | Defect | Resolution |
|---|----------|--------|------------|
| 1 | High | An installed Ollama service with a missing model raised an uncaught `ResponseError` traceback. | Catch Ollama request/response errors and mark findings `needs_human_review`. |
| 2 | Medium | `report` and `banish` accepted nonexistent repository paths. | Shared repository validation now returns exit code 2. |
| 3 | Medium | `init` on a nonexistent path produced a filesystem traceback. | Validate the repository path before writing configuration. |
| 4 | Medium | Unknown scanner types silently produced a clean result. | Validate scanner aliases and reject unknown or empty selections. |
| 5 | Low | Report output with a missing parent directory produced an uncaught filesystem error. | Convert report write failures into a clear exit-code-2 error. |

## Evidence

- Fixture findings JSON: `demo/verified-fixture.json`
- `jersey-paglu` findings JSON: `demo/verified-jersey.json`
- `jersey-paglu` report: `demo/verified-jersey-report.html`
- Real terminal transcript: `demo/jersey-paglu-real-transcript.txt`
- Real terminal screenshot: `demo/jersey-paglu-real-terminal.png`

## Verdict

```text
environment:
  docker: UNAVAILABLE — docker info exit code 1; no container-backed service is required
  node: AVAILABLE — v22.13.1
  playwright: AVAILABLE — 1.64.1; static report rendered successfully in browser
  infra-tier: NOT APPLICABLE — Exorcist is a local CLI with no database or service dependency
  browser-tier: PRIMARY(HTML browser smoke) — generated offline report opened and rendered
startup: PASS — CLI entry point and local Ollama doctor check succeeded
integration: PASS — exit_code: 0, passed: 14, failed: 0, skipped: 0
e2e: PASS — static report browser smoke passed; 0 findings and offline badge visible
overall: PASS — regression suite and end-to-end CLI/report workflows are green
```
