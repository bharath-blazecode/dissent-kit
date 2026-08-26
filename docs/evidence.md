# What the repository proves

DissentKit separates inspectable evidence from claims that still need testing.

## Available now

- The repository validator checks packaging, links, skill metadata, fixture structure, public claims, and artwork requirements.
- Thirteen behavioral cases cover non-activation, Direct Review, escalation, Deliberation, pushback, new evidence, diagnosis-only requests, and strong work that should not be rewritten.
- The worked example exposes the complete Direct Review and single-context Deliberation structure.
- The quick comparison shows the difference between general caution and the specific Direct Review contract.
- The package builder fixes file order, paths, timestamps, permissions, and compression settings for its five-file installation ZIP, then writes a SHA-256 checksum. Matching bytes are verified within the tested toolchain; compressed output may differ across Python or zlib versions.

These checks show that the repository is internally consistent and testable. They do not establish that every host or model will behave identically.

## Not claimed yet

DissentKit does not currently publish a model pass rate, an independent comparison against other review prompts, or evidence that five lenses remove model bias. Publishing those claims would require dated runs, exact host and model names, fresh conversations, raw outputs, and visible grading notes.

## How to add model evidence

1. Run every request in `evals/cases.json` in a fresh conversation.
2. Save each raw output without editing it.
3. Grade each listed check as true or false.
4. Record the host, exact model, model settings, adapter, source commit, grader, date, and DissentKit version.
5. Generate the report with `scripts/eval_report.py`.
6. Review the raw outputs for private information before publishing them.

The reporting script rejects unknown cases, duplicate cases, missing raw outputs, non-boolean grades, and incomplete runs. A partial report must be requested explicitly and is labeled as partial.
