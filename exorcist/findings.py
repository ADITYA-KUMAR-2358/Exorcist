"""Validated data contracts shared by scanners, triage, and reports."""

from enum import StrEnum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class FindingType(StrEnum):
    SECRET = "secret"
    DEPENDENCY = "dependency"
    DEAD_CODE = "dead_code"
    ZOMBIE_JOB = "zombie_job"


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Verdict(StrEnum):
    REAL_HAUNTING = "real_haunting"
    FALSE_ALARM = "false_alarm"
    NEEDS_HUMAN_REVIEW = "needs_human_review"


class FindingStatus(StrEnum):
    FOUND = "found"
    TRIAGED = "triaged"
    BANISHED = "banished"
    PR_OPENED = "pr_opened"


class FixKind(StrEnum):
    ENV_VAR = "env_var"
    BUMP_DEP = "bump_dep"
    DELETE = "delete"
    COMMENT_OUT = "comment_out"


class ProposedFix(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: FixKind
    diff: str


class Finding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: UUID = Field(default_factory=uuid4)
    type: FindingType
    file: str = Field(min_length=1)
    line: int = Field(ge=1)
    severity: Severity
    raw: dict[str, Any]
    snippet: str
    verdict: Verdict | None = None
    reason: str = Field(default="", max_length=240)
    proposed_fix: ProposedFix | None = None
    status: FindingStatus = FindingStatus.FOUND


class TriageResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    verdict: Literal[Verdict.REAL_HAUNTING, Verdict.FALSE_ALARM]
    reason: str = Field(min_length=1, max_length=240)


class FixResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: FixKind
    diff: str


class ReportContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    repository: str
    scan_time: str
    duration_seconds: float = Field(ge=0)
    model: str
    network_calls: int = Field(ge=0)
    findings: list[Finding]
