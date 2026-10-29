"""Detect cron and GitHub Actions references to missing scripts."""

import re
from pathlib import Path

from exorcist.findings import Finding
from exorcist.scanners.common import finding


def scan(repo: Path) -> list[Finding]:
    findings: list[Finding] = []
    candidates = list(repo.rglob("*"))
    for path in candidates:
        if not path.is_file() or path.name not in {"crontab", "cron", "schedule"}:
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            for command in re.findall(r"(?:python\s+|bash\s+|sh\s+)?([./\w-]+\.(?:py|sh))", line):
                if not (repo / command).exists():
                    findings.append(
                        finding(
                            type="zombie_job",
                            file=str(path.relative_to(repo)),
                            line=line_no,
                            severity="medium",
                            rule="missing-cron-target",
                            match_redacted=command,
                            snippet_text=line + "\n",
                        )
                    )
    return findings
