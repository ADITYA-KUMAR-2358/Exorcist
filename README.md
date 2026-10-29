# Exorcist

Exorcist is a local-first CLI for finding and banishing possessed code:
secrets, vulnerable dependencies, dead code, and zombie jobs.

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
