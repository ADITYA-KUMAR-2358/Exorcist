# Product Requirements

## User stories

- As a developer, I can scan a repository and see findings grouped by type and
  severity.
- As a developer, I can read a static HTML report with exact file locations,
  redacted evidence, model reasoning, and proposed diffs.
- As a developer, I can banish one finding in dry-run mode or on a safe branch.
- As a developer, I can use `--ritual` to bundle all approved fixes into one
  themed PR.
- As a developer, I can run `doctor` to check local prerequisites.

## In scope

Secrets, dependencies, dead code, zombie cron/CI jobs, local Ollama triage,
Pydantic-validated JSON, HTML reports, branch-based fixes, optional PRs, and
`--ritual`.

## Non-goals

No hosted backend, auto-merge, languages beyond Python and JS/TS, IDE plugin,
or telemetry.

## Success criteria

The challenge demo proves privacy while offline, shows the cursed fixture
correctly classifying a real and an example secret, demonstrates a safe fix
branch, and publishes a readable report and local-versus-cloud benchmark.
