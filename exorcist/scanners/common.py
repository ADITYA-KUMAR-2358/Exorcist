"""Shared scanner utilities."""

from pathlib import Path

from exorcist.findings import Finding

TEXT_SUFFIXES = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".yaml", ".yml", ".json", ".toml",
    ".ini", ".cfg", ".txt", ".md", ".sh", ".env",
}


def files_in(repo: Path) -> list[Path]:
    ignored = {".git", ".venv", "node_modules", "__pycache__", ".pytest_cache"}
    return [
        path
        for path in repo.rglob("*")
        if path.is_file()
        and not any(part in ignored for part in path.parts)
        and (path.suffix.lower() in TEXT_SUFFIXES or path.name in {"Dockerfile", "crontab"})
    ]


def snippet(lines: list[str], line: int, radius: int = 10) -> str:
    start = max(0, line - 1 - radius)
    end = min(len(lines), line + radius)
    return "".join(lines[start:end])


def finding(
    *,
    type: str,
    file: str,
    line: int,
    severity: str,
    rule: str,
    match_redacted: str,
    snippet_text: str,
) -> Finding:
    return Finding(
        type=type,
        file=file,
        line=line,
        severity=severity,
        raw={"rule": rule, "match_redacted": match_redacted},
        snippet=snippet_text,
    )
