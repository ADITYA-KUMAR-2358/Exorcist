from pathlib import Path

from exorcist.findings import Finding, ReportContext
from exorcist.report import render, write_report


def test_report_is_self_contained_and_redacted(tmp_path: Path) -> None:
    context = ReportContext(
        repository="fixture",
        scan_time="2026-01-01T00:00:00Z",
        duration_seconds=1.2,
        model="qwen2.5-coder:3b",
        network_calls=0,
        findings=[
            Finding(
                type="secret",
                file="config.py",
                line=1,
                severity="critical",
                raw={"rule": "aws", "match_redacted": "AKIA****"},
                snippet="AKIA****",
                verdict="real_haunting",
            )
        ],
    )
    html = render(context)
    assert "0 network calls" in html
    assert "AKIA****" in html
    output = tmp_path / "report.html"
    write_report(context, output)
    assert output.exists()
