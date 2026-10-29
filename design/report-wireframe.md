# Report Wireframe

The report is dark, responsive, single-column, keyboard accessible, and
contains no external assets or fonts.

```text
+--------------------------------------------------+
| ghost logo | repo name | scan time                |
| 3 spirits found, 1 banished                       |
+--------------------------------------------------+
| SECRETS 2 | DEPS 1 | DEAD CODE 0 | ZOMBIE JOBS 0 |
+--------------------------------------------------+
| [real_haunting] config.py:12              [open] |
| redacted match | model reason | proposed diff    |
| [false_alarm] tests/fixture.py:4          [open] |
+--------------------------------------------------+
| model: qwen... | duration: 2.4s | 0 network calls |
+--------------------------------------------------+
```

The header includes logo, repository, timestamp, and summary. Cards show count
and severity color. Findings are collapsible with verdict, file and line,
redacted evidence, plain model reasoning, and a diff view. Expand/collapse
must work from the keyboard, with accessible contrast throughout.
