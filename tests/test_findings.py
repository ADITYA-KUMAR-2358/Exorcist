from uuid import UUID

import pytest
from pydantic import ValidationError

from exorcist.findings import Finding, FindingType, Severity, TriageResponse, Verdict


def test_finding_defaults_and_contract() -> None:
    finding = Finding(
        type=FindingType.SECRET,
        file="config.py",
        line=12,
        severity=Severity.HIGH,
        raw={"rule": "aws-access-key", "match_redacted": "AKIA****"},
        snippet="AWS_ACCESS_KEY_ID = 'AKIA****'",
    )
    assert isinstance(finding.id, UUID)
    assert finding.status == "found"
    assert finding.verdict is None


def test_finding_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        Finding(
            type="secret",
            file="config.py",
            line=12,
            severity="high",
            raw={},
            snippet="",
            unexpected=True,
        )


def test_triage_response_rejects_human_review_verdict() -> None:
    with pytest.raises(ValidationError):
        TriageResponse(verdict=Verdict.NEEDS_HUMAN_REVIEW, reason="review")
