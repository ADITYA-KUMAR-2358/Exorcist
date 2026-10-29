# Exorcist

Exorcist is a local-first CLI for finding and banishing possessed code:
secrets, vulnerable dependencies, dead code, and zombie jobs.

## Node CLI

The npm CLI is available as `@aditya-kumar-2358/exorcist` and provides a
Windows Terminal-inspired experience with a cyan `EXORCIST` wordmark, local
Ollama metadata, step-by-step scans, and offline HTML reports.

```powershell
npx @aditya-kumar-2358/exorcist scan .
npx @aditya-kumar-2358/exorcist scan . --json
```

The package requires Node 18 or newer. Use `--no-color` for legacy consoles,
`--json` for automation, and `--verbose` for diagnostic stack traces.

### Sample terminal output

```text
  EEEEE  X   X   OOO   RRRR    CCCC  III  SSS   TTTTT
  E       X X   O   O  R   R  C       I  S       T
  EEEE     X    O   O  RRRR   C       I   SSS    T
  E       X X   O   O  R R    C       I      S   T
  EEEEE  X   X   OOO   R  RR   CCCC  III  SSS    T
  @exorcist/cli  v0.2.0
  Local-first AI code exorcism  (Ollama + open-weight models)

  i Summoning Exorcist in E:\my-project...
    -> Detecting project type and languages...
    -> Checking Ollama and model (qwen2.5-coder:3b)...
  √ Environment ready!
```

### Command table

| Command | Purpose |
| --- | --- |
| `exorcist init [path]` | Create local scanner configuration |
| `exorcist scan [path]` | Scan and write an offline HTML report |
| `exorcist report [path]` | Generate a report explicitly |
| `exorcist fix --dry-run` | Preview guarded fix proposals |

### FAQ

**Does Exorcist send source code to the cloud?** No. Product-path model calls
target only localhost Ollama.

**Can I use it in CI?** Yes. Use `--json --no-color --yes`; animations and the
banner are skipped for non-TTY and CI output.

**What does exit code 1 mean?** Findings at high or critical severity were
detected. Exit code 2 is reserved for runtime errors.

## Quickstart

```powershell
python -m pip install -e ".[dev]"
exorcist doctor
exorcist scan tests/cursed_repo --json
exorcist report tests/cursed_repo --out report.html
```

For a remote repository, clone it explicitly first:

```powershell
exorcist clone https://github.com/owner/project.git
exorcist scan .\project
```

This separation is intentional. `clone` is the only network-facing setup
command. Scanning stays local and never silently contacts a Git host.

For the full terminal tutorial and command map, run `exorcist guide` or read
[docs/RUN.md](docs/RUN.md). `exorcist --help`, `exorcist -help`, and
`exorcist help` all show the complete command suite.

The scanner works without network access. When Ollama is running locally, use
`--model qwen2.5-coder:3b` to triage findings. If it is unavailable, findings
are explicitly marked `needs_human_review`.

## Why open-source AI

- **Private:** repository contents stay local.
- **Free:** no per-scan hosted inference bill.
- **Swappable:** `--model` selects another Ollama model.
- **Offline:** scanners and report generation work with Wi-Fi disabled.

The product path calls only localhost Ollama and reports zero network calls.
The current sponsor-track implementation is **Best Use of Gemma**. Run
`exorcist tracks` for the evidence path, then use
`--model gemma3:4b` for a local Gemma triage run.
See [docs/](docs/) for the architecture, contracts, safety rules, and
milestone evidence.
