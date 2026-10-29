"""Offline scanner collection."""

from pathlib import Path

from exorcist.findings import Finding
from exorcist.scanners.dead_code import scan as scan_dead_code
from exorcist.scanners.dependencies import scan as scan_dependencies
from exorcist.scanners.secrets import scan as scan_secrets
from exorcist.scanners.zombie_jobs import scan as scan_zombie_jobs

ALIASES = {
    "secrets": "secrets", "secret": "secrets", "deps": "deps",
    "dependencies": "deps", "deadcode": "deadcode", "dead_code": "deadcode",
    "cron": "cron", "zombie_job": "cron",
}


def scan(repo: Path, selected: str) -> list[Finding]:
    names = {
        ALIASES.get(item.strip(), item.strip())
        for item in selected.split(",")
        if item.strip()
    }
    if not names:
        raise ValueError("at least one scanner type is required")
    unknown = names.difference({"secrets", "deps", "deadcode", "cron"})
    if unknown:
        choices = ", ".join(sorted(unknown))
        raise ValueError(f"unknown scanner type(s): {choices}")
    scanners = {
        "secrets": scan_secrets, "deps": scan_dependencies,
        "deadcode": scan_dead_code, "cron": scan_zombie_jobs,
    }
    findings: list[Finding] = []
    for name, scanner in scanners.items():
        if name in names:
            findings.extend(scanner(repo))
    return findings
