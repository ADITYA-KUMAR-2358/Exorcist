# ADR-001: Local-first execution

## Context

Repositories and secrets are sensitive, and scans should work without Wi-Fi.

## Decision

The product path may call only localhost Ollama. Cloud models are limited to
benchmark comparison.

## Consequences

Users get privacy and predictable cost, but must install Ollama and a model.
