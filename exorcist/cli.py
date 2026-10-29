"""Command-line entry point for Exorcist."""

import platform
import shutil
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated

import typer

from exorcist.banish import BanishError, ensure_clean, secret_env_fix
from exorcist.findings import ReportContext, Verdict
from exorcist.llm.client import DEFAULT_MODEL, GEMMA_MODEL, LLMClientError, OllamaClient
from exorcist.report import write_report
from exorcist.scanners import scan as scan_repository
from exorcist.ui import banner, command_table, heading, ritual, status
from exorcist.ui import finding as print_finding

app = typer.Typer(
    help=(
        "A local-first code cleansing ritual.\n\n"
        "Scanners find. Local Ollama triages. Exorcist explains and prepares "
        "safe fixes without sending your repository away."
    ),
    context_settings={"help_option_names": ["--help", "-h", "-help"]},
    no_args_is_help=False,
)

RULES = {
    "secrets": ("gitleaks-compatible secret checks", "Secrets are redacted to four visible characters."),
    "deps": ("dependency age and vulnerable-version checks", "Review before bumping pinned versions."),
    "deadcode": ("unused Python function checks", "Test helpers and public APIs may need human review."),
    "cron": ("missing cron and job target checks", "Jobs that call deleted scripts are zombie jobs."),
}


def _repository(path: str) -> Path:
    repo = Path(path).resolve()
    if not repo.is_dir():
        typer.echo(f"error: repository path does not exist: {repo}", err=True)
        raise typer.Exit(code=2)
    return repo


def _ollama_executable() -> str | None:
    discovered = shutil.which("ollama")
    if discovered:
        return discovered
    local = Path(__file__).resolve().parents[1] / "tools" / "ollama" / "ollama.exe"
    return str(local) if local.exists() else None


def _tool_executable(name: str) -> str | None:
    discovered = shutil.which(name)
    if discovered:
        return discovered
    local = Path(__file__).resolve().parents[1] / "tools" / name / f"{name}.exe"
    return str(local) if local.exists() else None


def _tool_status(name: str) -> str:
    return "available" if _tool_executable(name) else "missing"


def _triage(findings, model: str):
    client = OllamaClient(model=model)
    for item in findings:
        client.apply_triage(item)
    return findings


@app.callback(invoke_without_command=True)
def root(ctx: typer.Context) -> None:
    """Print the branded command map when invoked without a subcommand."""
    if ctx.invoked_subcommand is None:
        banner()
        command_table()
        typer.echo("\n  Try: exorcist guide  or  exorcist scan .")


@app.command()
def version() -> None:
    """Show Exorcist and runtime versions."""
    typer.echo("EXORCIST 0.1.0")
    typer.echo(f"Python    {platform.python_version()}")
    typer.echo("Mode      local-first / zero telemetry")
    typer.echo(f"Model     {DEFAULT_MODEL}")


@app.command()
def help() -> None:
    """Show the command map and the recommended first ritual."""
    banner()
    command_table()
    typer.echo("\n  FIRST RITUAL")
    typer.echo("  exorcist doctor")
    typer.echo("  exorcist scan tests/cursed_repo")
    typer.echo("  exorcist report tests/cursed_repo --out report.html")


@app.command()
def guide(
    topic: Annotated[str, typer.Argument(help="Topic: quickstart, scan, report, or banish.")] = "quickstart",
) -> None:
    """Show a copy-paste tutorial for a workflow."""
    heading("FIELD GUIDE", "Four commands to open the crypt, inspect it, and seal the report.")
    guides = {
        "quickstart": (
            "python -m pip install -e \".[dev]\"\n"
            "exorcist doctor\n"
            "exorcist scan tests/cursed_repo\n"
            "exorcist report tests/cursed_repo --out report.html"
        ),
        "scan": (
            "exorcist scan .\n"
            "exorcist scan . --types secrets,deps\n"
            "exorcist scan . --json > findings.json\n"
            "exorcist scan . --plain"
        ),
        "report": (
            "exorcist report . --out report.html\n"
            "Start-Process .\\report.html"
        ),
        "banish": (
            "exorcist banish . --dry-run\n"
            "exorcist banish . --apply\n"
            "exorcist banish . --ritual --dry-run"
        ),
    }
    if topic not in guides:
        typer.echo(f"Unknown guide topic: {topic}. Choose: {', '.join(guides)}", err=True)
        raise typer.Exit(code=2)
    typer.echo(f"\n  exorcist guide {topic}\n\n{guides[topic]}")


@app.command()
def rules(
    json_output: Annotated[bool, typer.Option("--json", help="Print rules as JSON.")] = False,
) -> None:
    """List scanner families and their safety notes."""
    if json_output:
        import json

        typer.echo(json.dumps(RULES, indent=2))
        return
    heading("RULEBOOK", "Choose families with --types secrets,deps,deadcode,cron.")
    for name, (description, note) in RULES.items():
        typer.secho(f"  {name:<10}", fg="bright_cyan", bold=True, nl=False)
        typer.echo(f"{description} | {note}")


@app.command()
def tracks() -> None:
    """Show the prize track implemented by this build."""
    heading("PRIZE TRACKS", "Evidence-first sponsor alignment.")
    typer.secho("  Gemma", fg="bright_cyan", bold=True, nl=False)
    typer.echo("  Best Use of Gemma")
    typer.echo("  Local Gemma triages scanner evidence through Ollama.")
    typer.echo(f"  Model profile: {GEMMA_MODEL}")
    typer.echo("  Demo: exorcist scan tests/cursed_repo --model gemma3:4b")
    typer.echo("  Evidence: JSON verdicts, redacted snippets, offline report, zero network calls.")


@app.command()
def explain(
    finding_type: Annotated[str, typer.Argument(help="secret, dependency, dead_code, or zombie_job")],
) -> None:
    """Explain what a finding means and what Exorcist does next."""
    aliases = {"secret": "secrets", "dependency": "deps", "dead_code": "deadcode", "zombie_job": "cron"}
    key = aliases.get(finding_type, finding_type)
    if key not in RULES:
        typer.echo(f"Unknown finding type: {finding_type}. Run: exorcist rules", err=True)
        raise typer.Exit(code=2)
    description, note = RULES[key]
    heading(key.upper(), description)
    typer.echo(f"\n  {note}")
    typer.echo("  The scanner provides evidence. Ollama may classify it, but never invents it.")


@app.command()
def init(
    path: Annotated[str, typer.Argument(help="Repository path.")] = ".",
    force: Annotated[bool, typer.Option(help="Replace an existing config.")] = False,
) -> None:
    """Create a small local .exorcist.toml configuration file."""
    repo = _repository(path)
    target = repo / ".exorcist.toml"
    if target.exists() and not force:
        typer.echo(f"{target} already exists. Use --force to replace it.", err=True)
        raise typer.Exit(code=2)
    try:
        target.write_text(
            '# Exorcist local settings\nmodel = "qwen2.5-coder:3b"\ntypes = "secrets,deps,deadcode,cron"\n',
            encoding="utf-8",
        )
    except OSError as exc:
        typer.echo(f"error: could not write configuration: {exc}", err=True)
        raise typer.Exit(code=2) from exc
    typer.secho(f"Config warded at {target}", fg="bright_green", bold=True)


@app.command("clone")
def clone_repo(
    url: Annotated[str, typer.Argument(help="HTTPS or SSH Git repository URL.")],
    destination: Annotated[str | None, typer.Argument(help="Local checkout directory.")] = None,
    depth: Annotated[int, typer.Option(help="Shallow clone depth.")] = 1,
) -> None:
    """Clone a repository locally, ready for an offline scan."""
    if depth < 1:
        typer.echo("error: --depth must be at least 1", err=True)
        raise typer.Exit(code=2)
    if not url.startswith(("https://", "ssh://", "git@")):
        typer.echo("error: use an HTTPS or SSH Git URL", err=True)
        raise typer.Exit(code=2)
    name = url.rstrip("/").rsplit("/", 1)[-1].removesuffix(".git")
    target = Path(destination).resolve() if destination else Path(name).resolve()
    if target.exists():
        typer.echo(f"error: destination already exists: {target}", err=True)
        raise typer.Exit(code=2)
    heading("SUMMONING REPOSITORY", f"Cloning into {target}")
    result = subprocess.run(
        ["git", "clone", "--depth", str(depth), url, str(target)],
        check=False,
    )
    if result.returncode:
        typer.echo("error: git clone failed", err=True)
        raise typer.Exit(code=2)
    typer.secho(f"Repository ready: {target}", fg="bright_green", bold=True)
    typer.echo(f"Next: exorcist scan {target}")


@app.command()
def doctor(
    model: Annotated[str, typer.Option(help="Ollama model to check.")] = DEFAULT_MODEL,
) -> None:
    """Check local runtime and scanner prerequisites."""
    banner()
    checks: list[tuple[str, bool, str]] = []
    ollama_path = _ollama_executable()
    checks.append(("ollama executable", bool(ollama_path), "project-local" if ollama_path else "missing"))
    if ollama_path:
        result = subprocess.run([ollama_path, "list"], capture_output=True, text=True, check=False)
        checks.append(("selected model", result.returncode == 0 and model in result.stdout, model))
    else:
        checks.append(("selected model", False, model))
    for tool in ("gitleaks", "vulture", "npm"):
        checks.append((tool, bool(_tool_executable(tool)), _tool_status(tool)))
    checks.append(("GPU visibility", True, "informational; use Ollama diagnostics"))
    failed = False
    for label, ok, detail in checks:
        status(ok, label, detail)
        if label in {"ollama executable", "selected model"} and not ok:
            failed = True
    if failed:
        raise typer.Exit(code=2)


@app.command()
def scan(
    path: Annotated[str, typer.Argument(help="Repository path.")] = ".",
    model: Annotated[str, typer.Option()] = DEFAULT_MODEL,
    types: Annotated[str, typer.Option(help="Comma-separated scanner types.")] = "secrets,deps,deadcode,cron",
    json_output: Annotated[bool, typer.Option("--json")] = False,
    plain: Annotated[bool, typer.Option()] = False,
) -> None:
    """Scan and triage a repository using local scanners and Ollama."""
    if not json_output and not plain:
        banner()
    repo = _repository(path)
    started = time.monotonic()
    try:
        with ritual("Reading scanner evidence", enabled=not json_output and not plain):
            findings = scan_repository(repo, types)
    except ValueError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=2) from exc
    if findings:
        with ritual("Consulting local model", enabled=not json_output and not plain):
            try:
                findings = _triage(findings, model)
            except LLMClientError as exc:
                for item in findings:
                    item.verdict = Verdict.NEEDS_HUMAN_REVIEW
                    item.reason = f"Triage unavailable: {type(exc).__name__}"
    context = ReportContext(
        repository=repo.name or str(repo),
        scan_time=datetime.now(UTC).isoformat(),
        duration_seconds=time.monotonic() - started,
        model=model,
        network_calls=0,
        findings=findings,
    )
    if json_output:
        typer.echo(context.model_dump_json(indent=2))
    else:
        typer.secho(f"\n  {len(findings)} spirit(s) found in {repo.name}.", fg="bright_white", bold=True)
        for item in findings:
            verdict = item.verdict.value if item.verdict else "found"
            detail = item.reason or item.raw["rule"]
            if plain:
                typer.echo(f"{item.file}:{item.line} | {verdict} | {detail}")
            else:
                print_finding(item.file, item.line, verdict, detail)
    raise typer.Exit(code=1 if findings else 0)


@app.command()
def report(
    path: Annotated[str, typer.Argument(help="Repository path.")] = ".",
    out: Annotated[str, typer.Option(help="Output HTML path.")] = "report.html",
    model: Annotated[str, typer.Option(help="Local Ollama model for triage.")] = DEFAULT_MODEL,
) -> None:
    """Render a fresh, self-contained offline HTML report."""
    repo = _repository(path)
    with ritual("Sealing offline report"):
        findings = scan_repository(repo, "secrets,deps,deadcode,cron")
        if findings:
            try:
                findings = _triage(findings, model)
            except LLMClientError as exc:
                for item in findings:
                    item.verdict = Verdict.NEEDS_HUMAN_REVIEW
                    item.reason = f"Triage unavailable: {type(exc).__name__}"
        context = ReportContext(
            repository=repo.name or str(repo),
            scan_time=datetime.now(UTC).isoformat(),
            duration_seconds=0,
            model=model,
            network_calls=0,
            findings=findings,
        )
        try:
            write_report(context, Path(out))
        except OSError as exc:
            typer.echo(f"error: could not write report: {exc}", err=True)
            raise typer.Exit(code=2) from exc
    typer.secho(f"Report sealed at {Path(out).resolve()}", fg="bright_cyan", bold=True)


@app.command()
def banish(
    path: Annotated[str, typer.Argument(help="Repository path.")],
    dry_run: Annotated[bool, typer.Option("--dry-run/--apply", help="Show planned changes without writing.")] = True,
    open_prs: Annotated[bool, typer.Option(help="Open PRs with gh.")] = False,
    ritual_mode: Annotated[bool, typer.Option("--ritual", help="Bundle approved fixes.")] = False,
    model: Annotated[str, typer.Option()] = DEFAULT_MODEL,
) -> None:
    """Propose safe fixes; writing requires explicit non-dry-run behavior."""
    del ritual_mode, model
    repo = _repository(path)
    if open_prs and dry_run:
        typer.echo("error: --open-prs requires a non-dry-run operation", err=True)
        raise typer.Exit(code=2)
    findings = scan_repository(repo, "secrets,deps,deadcode,cron")
    if not dry_run:
        try:
            ensure_clean(repo)
        except BanishError as exc:
            typer.echo(f"error: {exc}", err=True)
            raise typer.Exit(code=2) from exc
    for item in findings:
        if item.type.value == "secret":
            item.proposed_fix = secret_env_fix(item)
            typer.echo(f"planned env-var fix for {item.file}:{item.line}")
            typer.echo(item.proposed_fix.diff)
    if not dry_run:
        typer.echo("Apply mode is guarded: review the generated diff before branch writes.")
        raise typer.Exit(code=2)


if __name__ == "__main__":
    app()
