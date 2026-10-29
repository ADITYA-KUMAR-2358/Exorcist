# Two-minute demo script

1. Disable Wi-Fi and show Ollama with `qwen2.5-coder:3b` already pulled.
2. Run `exorcist scan tests/cursed_repo --json` and show redacted evidence.
3. Explain that unavailable Ollama responses become `needs_human_review`
   instead of crashing.
4. Run `exorcist report tests/cursed_repo --out report.html` and open the
   generated local file.
5. Show the report cards, expandable findings, and `0 network calls` footer.
6. On a prepared clean clone, run `exorcist banish ...` in dry-run mode.
7. Re-enable Wi-Fi only after the offline proof is complete.
