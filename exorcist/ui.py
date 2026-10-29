"""Small zero-dependency terminal identity for Exorcist."""

from contextlib import contextmanager
from enum import StrEnum

from typer import secho


class Ink(StrEnum):
    CYAN = "bright_cyan"
    MAGENTA = "bright_magenta"
    YELLOW = "bright_yellow"
    GREEN = "bright_green"
    RED = "bright_red"
    BLUE = "bright_blue"
    WHITE = "bright_white"


def heading(title: str, subtitle: str = "") -> None:
    secho(f"\n  {title}", fg=Ink.CYAN, bold=True)
    if subtitle:
        secho(f"  {subtitle}", fg=Ink.WHITE, dim=True)


def banner() -> None:
    wordmark = (
        "  EEEEE X   X  OOO  RRRR   CCCC  III  SSS  TTTTT",
        "  E      X X  O   O R   R  C       I  S       T  ",
        "  EEEE    X   O   O RRRR   C       I   SSS    T  ",
        "  E      X X  O   O R R    C       I      S   T  ",
        "  EEEEE X   X  OOO  R  RR  CCCC  III  SSS    T  ",
    )
    secho("", nl=True)
    for line in wordmark:
        secho(line, fg=Ink.CYAN, bold=True)
    secho("  LOCAL-FIRST CODE CLEANSING RITUAL", fg=Ink.MAGENTA, bold=True)
    secho("  scanners find  /  local Ollama triages  /  zero telemetry", fg=Ink.WHITE, dim=True)


@contextmanager
def ritual(label: str, enabled: bool = True):
    """Show a short animated phase without polluting JSON output."""
    if not enabled:
        yield
        return
    frames = ("[   ]", "[.  ]", "[.. ]", "[...]")
    secho(f"  {frames[0]} {label}", fg=Ink.MAGENTA, nl=False)
    try:
        yield
    finally:
        secho("\r  [ok] " + label, fg=Ink.GREEN)


def command_table() -> None:
    rows = (
        ("scan", "Find and triage possessed code"),
        ("report", "Seal an offline HTML report"),
        ("banish", "Preview safe fixes on a branch"),
        ("doctor", "Check local tools and Ollama"),
        ("init", "Create local Exorcist configuration"),
        ("clone", "Clone a Git repository locally"),
        ("rules", "List scanner rules and aliases"),
        ("tracks", "Show prize-track evidence"),
        ("explain", "Explain a finding type"),
        ("guide", "Open the terminal tutorial"),
        ("version", "Show version and runtime"),
    )
    secho("\n  COMMANDS", fg=Ink.YELLOW, bold=True)
    secho("  ------------------------------------------------------------------", fg=Ink.BLUE, dim=True)
    for command, description in rows:
        secho(f"  {command:<12}", fg=Ink.CYAN, bold=True, nl=False)
        secho(description, fg=Ink.WHITE)


def status(ok: bool, label: str, detail: str) -> None:
    secho("  + " if ok else "  ! ", fg=Ink.GREEN if ok else Ink.RED, bold=True, nl=False)
    secho(f"{label:<20}", fg=Ink.WHITE, nl=False)
    secho(detail, fg=Ink.GREEN if ok else Ink.YELLOW)


def finding(file: str, line: int, verdict: str, detail: str) -> None:
    color = {
        "real_haunting": Ink.RED,
        "false_alarm": Ink.GREEN,
        "needs_human_review": Ink.YELLOW,
        "found": Ink.MAGENTA,
    }.get(verdict, Ink.WHITE)
    secho(f"  * {file}:{line} ", fg=Ink.CYAN, bold=True, nl=False)
    secho(f"[{verdict}] ", fg=color, bold=True, nl=False)
    secho(detail, fg=Ink.WHITE)
