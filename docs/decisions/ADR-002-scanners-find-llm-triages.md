# ADR-002: Scanners find, the LLM triages

## Context

An LLM should not be the source of security findings.

## Decision

Established scanners and parsers provide evidence. The LLM only classifies,
explains, and drafts a constrained fix.

## Consequences

Findings are reproducible and auditable, while model output remains bounded
and requires schema validation.
