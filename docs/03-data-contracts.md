# Data Contracts

The canonical Finding shape is in `schemas/finding.schema.json`. Python models
must mirror it exactly and reject unknown or invalid enum values.

## Finding

`id` is a UUID; `type` is `secret`, `dependency`, `dead_code`, or
`zombie_job`; `file` and `line` locate evidence; `severity` is low/medium/high/
critical; `raw` contains redacted scanner data; `snippet` is about 20 lines;
`verdict` is `real_haunting`, `false_alarm`, or `needs_human_review`;
`reason` is under 30 words; `proposed_fix` has a fix `kind` and unified `diff`;
and `status` is found, triaged, banished, or pr_opened.

## LLM response models

Triage response: `verdict` (`real_haunting` or `false_alarm`) and a reason
under 30 words. Invalid output is retried once with a repair prompt, then
converted to `needs_human_review`.

Fix response: `kind` (`env_var`, `bump_dep`, `delete`, or `comment_out`) and a
unified diff. A fix is never applied without a human-visible diff.

## Report context

The report context contains repository name, scan timestamp, duration, model,
network-call count, counts by finding type, and the complete Finding list.
Secrets in raw evidence are always redacted before serialization.
