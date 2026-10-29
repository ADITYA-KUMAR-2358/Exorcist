# Testing and Benchmark

## Cursed repository fixture

`tests/cursed_repo` contains a fake AWS key that is a real positive, an
`EXAMPLE` placeholder key that is a false positive, a 2019-pinned vulnerable
dependency, an unused function, a cron entry calling a deleted script, and a
test fixture containing a fake token that should remain a false positive.

## Test plan

Unit-test each scanner's parser and redaction, each fixer against the fixture,
Pydantic validation and malformed-output repair, CLI exit codes, and report
rendering. Every scanner and fixer must have a fixture-based test.

## Benchmark protocol

Run on 10 abandoned public repositories and record findings, false-positive
rate, and seconds per finding for `qwen2.5-coder:3b`,
`qwen2.5-coder:7b`, `mistral:7b-instruct`, and one cloud comparison model.
Write results to `benchmarks/results.csv`; cloud calls are never part of the
product path.

## Offline proof

Pull the local model, disable Wi-Fi, run a scan, capture the network monitor
showing no outbound calls, and save the screenshot with the final submission.
