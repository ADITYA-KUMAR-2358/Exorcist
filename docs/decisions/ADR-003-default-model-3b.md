# ADR-003: Default to a 3B model

## Context

The target machine has about 10 GB usable RAM and a 4 GB GPU.

## Decision

Use `qwen2.5-coder:3b` by default, with `--model` for alternatives.

## Consequences

The default is practical on modest hardware; benchmarked larger models remain
available when users have more resources.
