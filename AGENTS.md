# Exorcist Agent Instructions

## Role

Exorcist is a local-first CLI that finds possessed code in Python and
JavaScript/TypeScript repositories, uses a local open-weight model to triage
scanner findings, applies safe fixes on branches, and produces an offline HTML
report.

## Read first

Read `docs/00-vision.md` through `docs/07-roadmap.md`, then `docs/backlog.md`,
all ADRs in `docs/decisions/`, and the files in `design/`.

## Hard constraints

- Scanners find; the LLM only classifies, explains, and drafts fixes.
- Scans may call only localhost Ollama. No telemetry or cloud model in product
  paths; cloud comparison is restricted to `benchmarks/`.
- Validate every LLM response with Pydantic. Retry malformed JSON once, then
  use `needs_human_review`; never crash.
- Default model is `qwen2.5-coder:3b`, with `--model` for swapping.
- Use about 20 context lines and Ollama `num_ctx=2048`.
- Redact secrets to their first four characters. Default to `--dry-run`, never
  push a default branch, and use `exorcist/<type>-<n>` fix branches.
- Python 3.11+, Typer, Pydantic v2, Ollama, GitPython, Jinja2, pytest, and ruff.
- Keep changes milestone-sized, typed, tested against `tests/cursed_repo`, and
  documented. Do not add out-of-scope features; put ideas in `docs/backlog.md`.
