"""Small fallback dead-code scanner for Python modules."""

import ast
from pathlib import Path

from exorcist.findings import Finding
from exorcist.scanners.common import finding


def scan(repo: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in repo.rglob("*.py"):
        relative_parts = path.relative_to(repo).parts
        if any(part in {".git", ".venv", "node_modules", "__pycache__"} for part in relative_parts):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            continue
        module_names = {
            node.id for node in ast.walk(tree) if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
        }
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name not in module_names:
                findings.append(
                    finding(
                        type="dead_code",
                        file=str(path.relative_to(repo)),
                        line=node.lineno,
                        severity="low",
                        rule="unused-function",
                        match_redacted=node.name,
                        snippet_text=f"def {node.name}(...)\n",
                    )
                )
    return findings
