"""Offline high-signal secret scanner."""

import re
from pathlib import Path

from exorcist.findings import Finding
from exorcist.scanners.common import files_in, finding, snippet

AWS_KEY = re.compile(r"\bAKIA[0-9A-Z]{16}\b")
TOKEN = re.compile(r"(?i)\b(?:token|secret|password|api[_-]?key)\b\s*[:=]\s*['\"]([^'\"]{12,})['\"]")


def _redact(value: str) -> str:
    return f"{value[:4]}****"


def _safe_snippet(lines: list[str], line: int) -> str:
    text = snippet(lines, line)
    text = AWS_KEY.sub(lambda match: _redact(match.group(0)), text)
    return TOKEN.sub(lambda match: match.group(0).replace(match.group(1), _redact(match.group(1))), text)


def scan(repo: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in files_in(repo):
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines(keepends=True)
        except OSError:
            continue
        for index, text in enumerate(lines, start=1):
            for match in AWS_KEY.finditer(text):
                value = match.group(0)
                placeholder = "EXAMPLE" in value.upper() or "example" in text.lower()
                findings.append(
                    finding(
                        type="secret",
                        file=str(path.relative_to(repo)),
                        line=index,
                        severity="low" if placeholder else "critical",
                        rule="aws-access-key",
                        match_redacted=_redact(value),
                        snippet_text=_safe_snippet(lines, index),
                    )
                )
                findings[-1].raw["placeholder"] = placeholder
            match = TOKEN.search(text)
            if match and "example" not in text.lower() and "fake" not in text.lower():
                findings.append(
                    finding(
                        type="secret",
                        file=str(path.relative_to(repo)),
                        line=index,
                        severity="high",
                        rule="hardcoded-secret",
                        match_redacted=_redact(match.group(1)),
                        snippet_text=_safe_snippet(lines, index),
                    )
                )
    return findings
