from exorcist.findings import Finding, Verdict
from exorcist.llm.client import OllamaClient


def _finding() -> Finding:
    return Finding(
        type="secret",
        file="config.py",
        line=12,
        severity="high",
        raw={"rule": "aws-access-key", "match_redacted": "AKIA****"},
        snippet="AWS_ACCESS_KEY_ID = 'AKIA****'",
    )


def test_triage_validates_local_json_response() -> None:
    def chat(**_: object) -> dict[str, object]:
        return {"message": {"content": '{"verdict":"real_haunting","reason":"Credential is hardcoded."}'}}

    result = OllamaClient(chat=chat).triage(_finding())
    assert result.verdict == Verdict.REAL_HAUNTING


def test_triage_repairs_invalid_json_once() -> None:
    responses = iter(
        [
            {"message": {"content": "not json"}},
            {"message": {"content": '{"verdict":"false_alarm","reason":"Placeholder key."}'}},
        ]
    )

    def chat(**_: object) -> dict[str, object]:
        return next(responses)

    result = OllamaClient(chat=chat).triage(_finding())
    assert result.verdict == Verdict.FALSE_ALARM


def test_invalid_json_becomes_human_review() -> None:
    def chat(**_: object) -> dict[str, object]:
        return {"message": {"content": "not json"}}

    result = OllamaClient(chat=chat).apply_triage(_finding())
    assert result.verdict == Verdict.NEEDS_HUMAN_REVIEW
