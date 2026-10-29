# Run Exorcist

Exorcist is a Python CLI. The commands below work from the repository root.

## 1. Install

PowerShell:

```powershell
python -m pip install -e ".[dev]"
```

Check the local tools:

```powershell
exorcist doctor
```

The doctor command checks Ollama, the selected model, scanner tools, npm, and
GPU visibility. Ollama and its model are required for live model triage.

## 2. Install the local model

Install Ollama from its official installer, start it, then pull the default
open-weight model:

```powershell
ollama pull qwen2.5-coder:3b
```

For this project, the portable runtime can also live under
`tools\ollama\ollama.exe`, with model files under `.ollama-models\`. Those
paths are ignored by Git. The Gemma prize-track profile uses:

```powershell
& .\tools\ollama\ollama.exe serve
$env:OLLAMA_MODELS = "$PWD\.ollama-models"
& .\tools\ollama\ollama.exe pull gemma3:4b
```

Or start the project-local service with:

```powershell
.\scripts\start-ollama.ps1
```

Exorcist only connects to Ollama on localhost. No cloud model is used in the
product path.

## 3. Scan a repository

### Start from a Git URL

The scan command intentionally accepts a local path. This keeps the product
path local-first: scanning never silently performs a network operation. Clone
the repository explicitly, then scan the resulting directory:

```powershell
exorcist clone https://github.com/owner/project.git
exorcist scan .\project
exorcist report .\project --out report.html
```

You can choose the checkout directory and shallow depth:

```powershell
exorcist clone git@github.com:owner/project.git .\haunted-project --depth 1
```

The clone step uses the installed Git client and requires network access. After
it finishes, `scan`, `report`, and `banish` operate on the local checkout.

The project-local prerequisite layout is:

```text
tools\ollama\ollama.exe
tools\gitleaks\gitleaks.exe
.ollama-models\
```

These are ignored by Git and are detected automatically by `exorcist doctor`.

Run the colorful terminal experience:

```powershell
exorcist scan tests/cursed_repo
```

Use plain output for logs or terminals without color:

```powershell
exorcist scan tests/cursed_repo --plain
```

Use JSON for automation:

```powershell
exorcist scan tests/cursed_repo --json
```

Select scanner families with comma-separated aliases:

```powershell
exorcist scan . --types secrets,deps,deadcode,cron
```

Exit codes are `0` for no findings, `1` when findings exist, and `2` for a
tool or environment error. If Ollama is unavailable, findings are preserved
and marked `needs_human_review`.

## 4. Generate the colorful HTML report

```powershell
exorcist report tests/cursed_repo --out report.html
Start-Process .\report.html
```

The report is a single offline HTML file. It includes the colorful Exorcist
mascot, finding cards, redacted matches, verdicts, proposed diffs, and the
zero-network badge. The generated `report.html` is intentionally ignored by
Git.

## 5. Preview a banishment

Always start with dry-run mode:

```powershell
exorcist banish tests/cursed_repo --dry-run
```

This prints a redacted environment-variable migration diff. Apply mode checks
that the target is a clean Git repository before any write operation:

```powershell
exorcist banish path\to\repo --apply
```

Do not use `--apply` on a working tree containing unrelated changes. Pull
requests and ritual bundling require a later release with explicit GitHub
authentication and patch approval.

## 6. Run tests and lint

```powershell
python -m pytest -q
python -m ruff check exorcist tests
```

## Command map

```powershell
exorcist --help
exorcist -help
exorcist help
exorcist version
exorcist guide
exorcist guide scan
exorcist guide report
exorcist guide banish
exorcist rules
exorcist rules --json
exorcist tracks
exorcist explain secret
exorcist explain dependency
exorcist init .
exorcist clone https://github.com/owner/project.git .\project
```

Running `exorcist` with no command opens the colorful command map. The
`--help`, `-h`, and `-help` spellings all open the complete command reference.
`guide` is a copy-paste tutorial, `rules` describes scanner coverage, and
`explain` gives a plain-language explanation of a finding type.

## Prize-track demo

This build targets **Best Use of Gemma**. Run the local Gemma profile after
pulling the model:

```powershell
ollama pull gemma3:4b
exorcist doctor --model gemma3:4b
exorcist scan tests/cursed_repo --model gemma3:4b --json
exorcist report tests/cursed_repo --out report.html
exorcist report tests/cursed_repo --model gemma3:4b --out report.html
```

The scanner remains the source of findings. Gemma only classifies and explains
those findings, and the report records the selected model and zero network
calls.

## Offline demo

1. Pull the model while connected.
2. Turn Wi-Fi off.
3. Run the scan and report commands above.
4. Open `report.html` locally.
5. Confirm the report says `0 network calls`.
