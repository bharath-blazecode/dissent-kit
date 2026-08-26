# Contributing

Keep changes small enough to review against a real failure case.

For behavior changes:

1. Add or update a case in `evals/cases.json`.
2. Explain which host and model exposed the problem.
3. Include the original prompt, raw output, expected behavior, and proposed correction.
4. Run `python scripts/check_repo.py`.

Remove private or identifying information from prompts and outputs before attaching them to an issue or pull request.

Do not add a universal rule for one unusual output unless the same failure is likely to recur. DissentKit should stay useful for ordinary reviews without turning every response into a template.

Documentation should use plain language, avoid unsupported claims, and distinguish single-context lenses from isolated model passes.

When a behavior change affects the shared review contract, update every standalone adapter or explain why an adapter is intentionally different. The repository validator checks the invocation phrases, Direct Review exceptions, chess-derived lenses, execution label, and final Deliberation fields across adapters.

See [the maintainer guide](docs/maintainer-guide.md) for version updates, package creation, CI coverage, and GitHub metadata that cannot be set through a pull request.
