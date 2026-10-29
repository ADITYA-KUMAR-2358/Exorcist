# CLI Specification

```text
exorcist scan <path>   [--model qwen2.5-coder:3b] [--types secrets,deps,deadcode,cron] [--json] [--plain]
exorcist banish <path> [--dry-run (default)] [--open-prs] [--ritual] [--model ...]
exorcist report <path> [--out report.html]
exorcist doctor
```

`scan` finds and triages. `banish` proposes or applies safe branch changes.
`report` renders the latest findings. `doctor` checks Ollama, the selected
model, scanner binaries, and GPU visibility. `--plain` removes persona text.

Exit codes: `0` means clean, `1` means findings are present, and `2` means a
tool or environment error.

Persona output example:

```text
The crypt has been opened. A restless spirit lingers in config.py:12.
Verdict: real_haunting | Move the credential to an environment variable.
```

Equivalent `--plain` output:

```text
Findings: 1
config.py:12 | real_haunting | Move the credential to an environment variable.
```
