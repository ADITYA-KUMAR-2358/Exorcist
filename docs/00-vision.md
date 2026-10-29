# Vision

**Pitch:** Exorcist uses private, local open-weight AI to find and banish
possessed code before it haunts production.

Repositories accumulate leaked secrets, vulnerable or abandoned dependencies,
dead code, and jobs that invoke scripts no longer present. Existing scanners
detect many of these problems but leave developers with noisy output and no
safe, explainable remediation path.

A local model is the right companion because Exorcist is private (source and
secrets stay on the machine), free to run repeatedly, swappable through
`--model`, and usable offline. Open innovation also makes the behavior
inspectable, tunable, and accessible without a hosted service.

## Submission proof points

1. A screenshot showing zero outbound network calls during a scan.
2. A local-versus-cloud accuracy and false-positive comparison table.
3. A live demo on `tests/cursed_repo`, including triage, a fix branch, and the
   generated report.
