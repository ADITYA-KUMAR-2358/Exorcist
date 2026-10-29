from pathlib import Path

from exorcist.findings import FindingType
from exorcist.scanners import scan

FIXTURE = Path(__file__).parent / "cursed_repo"


def test_scanners_find_expected_fixture_hauntings() -> None:
    findings = scan(FIXTURE, "secrets,deps,deadcode,cron")
    types = {item.type for item in findings}
    assert FindingType.SECRET in types
    assert FindingType.DEPENDENCY in types
    assert FindingType.DEAD_CODE in types
    assert FindingType.ZOMBIE_JOB in types
    secrets = [item for item in findings if item.type == FindingType.SECRET]
    assert len(secrets) == 2
    assert any(item.raw["placeholder"] for item in secrets)


def test_secret_scanner_redacts_matches() -> None:
    findings = scan(FIXTURE, "secrets")
    assert len(findings) == 2
    assert all(item.raw["match_redacted"].endswith("****") for item in findings)
    assert all("AKIA1234567890" not in item.snippet for item in findings)
