# LLM Prompts

## Triage

```text
You are triaging a static-analysis finding.
Rule: {rule}
Snippet: {snippet}
Reply ONLY with JSON:
{"verdict":"real_haunting|false_alarm","reason":"string under 30 words"}
```

The snippet contains only about 20 lines around the finding. The prompt must
state that the model cannot create new findings and must decide only from the
scanner evidence.

## Fix

Ask for JSON with the appropriate kind (`env_var`, `bump_dep`, `delete`, or
`comment_out`) and a unified diff. The model must preserve unrelated lines,
avoid printing secrets, and explain no more than needed for the diff.

## Repair

```text
Your previous response was not valid for this schema. Return ONLY valid JSON
matching this schema: {schema}. Do not use markdown fences.
Previous response: {response}
```

The client uses temperature 0, Ollama `format="json"`, `num_ctx=2048`, and a
triage output budget of about 150 tokens. Invalid output is repaired once,
then becomes `needs_human_review`.

## Few-shot coverage

Prompts include two real and two false-alarm examples for each finding type:
real credentials versus placeholders, vulnerable versus current dependencies,
reachable unused code versus test-only helpers, and live versus deleted-script
jobs. Examples must be redacted and must not teach the model to invent
findings.
