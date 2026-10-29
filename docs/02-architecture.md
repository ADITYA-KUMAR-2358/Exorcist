# Architecture

## Data flow

`scan -> scanners (raw JSON) -> Finding[] -> triage (LLM) -> verdicts ->
banish (fixer on branch) -> pr (optional) -> report (Jinja2 HTML)`

## Module responsibilities

- `cli.py`: Typer commands, flags, exit codes, and plain/persona output.
- `findings.py`: Pydantic Finding, triage, fix, and report context contracts.
- `scanners/`: adapters for gitleaks, pip/npm audit, vulture/knip, and cron/CI
  parsers; each scanner returns `list[Finding]` and never invents evidence.
- `llm/`: Ollama client with `triage(finding)` and `propose_fix(finding)`;
  validates JSON, retries repair once, and marks invalid results for review.
- `banish/`: validates a clean tree, creates `exorcist/<type>-<n>` branches,
  generates redacted diffs, and guards writes behind an explicit apply mode.
- `report/`: renders one self-contained static HTML document with no external
  assets.

## Failure handling

Missing Ollama or model: report a tool error with setup guidance. Missing
gitleaks or another scanner: identify the unavailable scanner and return exit
code 2. Malformed model JSON: repair once, then use
`needs_human_review` without crashing. Dirty git tree: refuse a write
operation. Missing GitHub authentication: keep the local branch and explain
why PR opening was skipped.

## Performance and privacy

Use the 3B model by default, `num_ctx=2048`, temperature 0, and roughly 20
context lines per finding. Scanners run locally and can be selected with
`--types`; only localhost Ollama is allowed in the product path.
