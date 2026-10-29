from pathlib import Path

from typer.testing import CliRunner

from exorcist.cli import app

runner = CliRunner()
FIXTURE = Path(__file__).parent / "cursed_repo"


def test_scan_missing_ollama_model_returns_human_review_json() -> None:
    result = runner.invoke(
        app,
        ["scan", str(FIXTURE), "--model", "model-that-is-not-installed", "--json"],
    )

    assert result.exit_code == 1
    payload = result.stdout
    assert '"verdict": "needs_human_review"' in payload
    assert "Traceback" not in payload


def test_root_command_uses_text_wordmark_without_ghost_art() -> None:
    result = runner.invoke(app, [])

    assert result.exit_code == 0
    assert "EEEE" in result.output
    assert "local-first code cleansing" in result.output.lower()
    assert ".-''''-." not in result.output


def test_invalid_repository_paths_return_tool_error(tmp_path: Path) -> None:
    missing = tmp_path / "missing"

    for command in ("scan", "report", "banish", "init"):
        args = [command, str(missing)]
        if command == "scan":
            args.append("--plain")
        result = runner.invoke(app, args)
        assert result.exit_code == 2, (command, result.stdout)
        assert "repository path does not exist" in result.output


def test_unknown_scanner_type_returns_tool_error() -> None:
    result = runner.invoke(app, ["scan", str(FIXTURE), "--types", "unknown", "--plain"])

    assert result.exit_code == 2
    assert "unknown scanner type(s): unknown" in result.output


def test_empty_scanner_selection_returns_tool_error() -> None:
    result = runner.invoke(app, ["scan", str(FIXTURE), "--types", "", "--plain"])

    assert result.exit_code == 2
    assert "at least one scanner type is required" in result.output


def test_report_missing_parent_returns_tool_error(tmp_path: Path) -> None:
    output = tmp_path / "missing" / "report.html"
    result = runner.invoke(app, ["report", str(FIXTURE), "--out", str(output)])

    assert result.exit_code == 2
    assert "could not write report" in result.output
