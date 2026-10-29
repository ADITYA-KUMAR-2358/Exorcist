# Exorcist CLI UX

The Node CLI uses a dark, Windows-Terminal-inspired visual language: a large
cyan-to-teal `EXORCIST` wordmark, dim local-model metadata, cyan information
steps, green completion marks, yellow warnings, and red errors.

Human output is automatically reduced when stdout is not a TTY or `CI=true`.
`--no-color` disables ANSI styling. `--json` emits only machine-readable data
and never imports or renders terminal UI.

## Commands

- `exorcist init [path]` writes local model and rule configuration.
- `exorcist scan [path]` runs local repository checks and creates an offline
  `exorcist-report.html`.
- `exorcist report [path] --out report.html` seals a standalone report.
- `exorcist fix --dry-run` previews the guarded fix flow.

Global flags include `--help`, `--version`, `--no-color`, `--json`,
`--verbose`, `--quiet`, `--yes`, and `--dry-run`.

Exit code `0` means no high-severity findings, `1` means findings above the
threshold exist, and `2` means the runtime could not complete the command.
