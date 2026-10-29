"""Safe branch-based fix application."""

import subprocess
from pathlib import Path

from exorcist.findings import Finding, FixKind, ProposedFix


class BanishError(RuntimeError):
    """Raised when a fix cannot be safely applied."""


def secret_env_fix(finding: Finding) -> ProposedFix:
    """Create a deterministic redacted env-var migration diff."""
    variable = "EXORCIST_SECRET"
    original = finding.raw.get("match_redacted", "REDACTED")
    replacement = f'os.environ["{variable}"]'
    diff = (
        f"--- a/{finding.file}\n+++ b/{finding.file}\n"
        f"@@ -{finding.line},1 +{finding.line},1 @@\n"
        f"-{original}\n+{replacement}\n"
        f"--- /dev/null\n+++ b/.env.example\n"
        f"@@ -0,0 +1 @@\n+{variable}=\n"
    )
    return ProposedFix(kind=FixKind.ENV_VAR, diff=diff)


def ensure_clean(repo: Path) -> None:
    result = subprocess.run(
        ["git", "-C", str(repo), "status", "--porcelain"],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        raise BanishError("Target is not a git repository.")
    if result.stdout.strip():
        raise BanishError("Refusing to banish with a dirty git tree.")


def apply_finding(repo: Path, finding: Finding, dry_run: bool = True) -> Finding:
    if finding.proposed_fix is None:
        raise BanishError(f"No proposed fix is available for {finding.file}:{finding.line}.")
    if dry_run:
        return finding
    ensure_clean(repo)
    branch = f"exorcist/{finding.type.value}-1"
    subprocess.run(["git", "-C", str(repo), "switch", "-c", branch], check=True)
    raise BanishError("Automatic diff application requires an explicit patch parser.")
