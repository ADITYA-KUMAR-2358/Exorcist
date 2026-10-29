"""Dependency scanner with offline manifest checks."""

import re
from pathlib import Path

from exorcist.findings import Finding
from exorcist.scanners.common import finding


def scan(repo: Path) -> list[Finding]:
    findings: list[Finding] = []
    requirements = repo / "requirements.txt"
    if requirements.exists():
        for line_no, line in enumerate(requirements.read_text(encoding="utf-8").splitlines(), 1):
            match = re.match(r"\s*([A-Za-z0-9_.-]+)==([0-2]\.\d+(?:\.\d+)*)", line)
            if match:
                findings.append(
                    finding(
                        type="dependency",
                        file="requirements.txt",
                        line=line_no,
                        severity="high",
                        rule="old-pinned-dependency",
                        match_redacted=match.group(0),
                        snippet_text=line + "\n",
                    )
                )
    package = repo / "package.json"
    if package.exists():
        for line_no, line in enumerate(package.read_text(encoding="utf-8").splitlines(), 1):
            if re.search(r'"[^"]+"\s*:\s*"\^?[0-3]\.', line):
                findings.append(
                    finding(
                        type="dependency",
                        file="package.json",
                        line=line_no,
                        severity="medium",
                        rule="legacy-major-dependency",
                        match_redacted=line.strip()[:80],
                        snippet_text=line + "\n",
                    )
                )
    return findings
