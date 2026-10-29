# Roadmap

- **M0:** Scaffold, `doctor`, Ollama client, and Finding model. Done when
  `exorcist doctor` passes and hello-world triage returns validated JSON.
- **M1:** Cursed repo, secrets scanner, and triage. Done when the fake AWS key
  is `real_haunting` and the EXAMPLE key is `false_alarm`.
- **M2:** Secrets fixer. Done when a branch contains an env-var diff and
  `.env.example` is updated.
- **M3:** HTML report from findings.
- **M4:** Dependency, dead-code, and zombie-job scanners with triage.
- **M5:** PR opening and `--ritual` bundled mode.
- **M6:** Benchmark, offline proof, final README, and demo script.

Each milestone requires tests, clean ruff output, acceptance evidence, demo
command output, and documentation updates before the next begins.

## Implementation status

The current implementation includes the M0 runtime, M1 offline secret and
fixture scanning, M2 redacted environment-variable diff generation, M3
self-contained HTML reports, M4 dependency/dead-code/zombie-job scanners, and
the M5 dry-run/ritual command surface. Full branch patch application and
GitHub PR creation remain guarded until a clean git repository and explicit
patch application policy are available. M6 benchmark rows are a checked-in
output template; external repository measurements are intentionally not
fabricated.
