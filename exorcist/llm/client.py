"""Strict, localhost-only Ollama integration."""

from collections.abc import Callable
from typing import Any

from pydantic import ValidationError

from exorcist.findings import (
    Finding,
    FindingStatus,
    FixResponse,
    TriageResponse,
    Verdict,
)

DEFAULT_MODEL = "qwen2.5-coder:3b"
GEMMA_MODEL = "gemma3:4b"
TRIAGE_TEMPLATE = """You are triaging a static-analysis finding.
Rule: {rule}
Finding metadata: {metadata}
Snippet: {snippet}
The scanner already found this issue; do not invent findings. Treat direct
scanner evidence as real_haunting unless the metadata or snippet explicitly
identifies a placeholder, example, test fixture, or other false-alarm marker.
For a hardcoded credential rule, a redacted value is still real evidence.
Reply ONLY with JSON:
{{"verdict":"real_haunting|false_alarm","reason":"string under 30 words"}}"""
REPAIR_TEMPLATE = """Your previous response was not valid for this schema.
Return ONLY valid JSON matching this schema: {schema}.
Previous response: {response}"""


class LLMClientError(RuntimeError):
    """Raised when Ollama cannot provide a usable response."""


class OllamaClient:
    """Small adapter that can be tested with an injected chat function."""

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        chat: Callable[..., Any] | None = None,
    ) -> None:
        self.model = model
        self._chat = chat

    def _chat_once(self, prompt: str) -> Any:
        if self._chat is not None:
            return self._chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                format="json",
                options={"temperature": 0, "num_ctx": 2048, "num_predict": 150},
            )
        try:
            from ollama import RequestError, ResponseError, chat
        except ImportError as exc:
            raise LLMClientError(
                "The ollama package is not installed; install project dependencies."
            ) from exc
        try:
            return chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                format="json",
                options={"temperature": 0, "num_ctx": 2048, "num_predict": 150},
            )
        except (ConnectionError, OSError, RequestError, ResponseError) as exc:
            raise LLMClientError("Ollama is unavailable at localhost.") from exc

    @staticmethod
    def _content(response: Any) -> Any:
        if isinstance(response, dict):
            message = response.get("message", response)
            return message.get("content", message) if isinstance(message, dict) else message
        message = getattr(response, "message", response)
        return getattr(message, "content", message)

    def triage(self, finding: Finding) -> TriageResponse:
        rule = str(finding.raw.get("rule", "unknown"))
        prompt = TRIAGE_TEMPLATE.format(
            rule=rule,
            metadata=finding.raw,
            snippet=finding.snippet,
        )
        response = self._chat_once(prompt)
        content = self._content(response)
        try:
            result = TriageResponse.model_validate_json(content)
        except (ValidationError, TypeError, ValueError):
            repair = REPAIR_TEMPLATE.format(
                schema=TriageResponse.model_json_schema(),
                response=content,
            )
            try:
                result = TriageResponse.model_validate_json(
                    self._content(self._chat_once(repair))
                )
            except (ValidationError, TypeError, ValueError) as exc:
                raise LLMClientError("Ollama returned invalid triage JSON.") from exc
        if result.verdict not in (Verdict.REAL_HAUNTING, Verdict.FALSE_ALARM):
            raise LLMClientError("Triage response contained an unsupported verdict.")
        return result

    def apply_triage(self, finding: Finding) -> Finding:
        try:
            result = self.triage(finding)
        except LLMClientError as exc:
            finding.verdict = Verdict.NEEDS_HUMAN_REVIEW
            finding.reason = str(exc)
            return finding
        if finding.raw.get("placeholder") is True:
            result.verdict = Verdict.FALSE_ALARM
            result.reason = "Scanner metadata marks this credential as an example placeholder."
        finding.verdict = result.verdict
        finding.reason = result.reason
        finding.status = FindingStatus.TRIAGED
        return finding

    def propose_fix(self, finding: Finding) -> FixResponse:
        prompt = (
            f"Draft a safe unified diff for this scanner finding in {finding.file}:{finding.line}.\n"
            f"Rule: {finding.raw.get('rule')}\nSnippet: {finding.snippet}\n"
            'Reply ONLY with JSON: {"kind":"env_var|bump_dep|delete|comment_out","diff":"unified diff"}'
        )
        response = self._content(self._chat_once(prompt))
        try:
            return FixResponse.model_validate_json(response)
        except (ValidationError, TypeError, ValueError) as exc:
            raise LLMClientError("Ollama returned invalid fix JSON.") from exc
