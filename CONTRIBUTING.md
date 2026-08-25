# Contributing

Keep changes small enough to review against a real failure case.

For behavior changes:

1. Add or update a case in `evals/cases.json`.
2. Explain which host and model exposed the problem.
3. Include the original prompt, raw output, expected behavior, and proposed correction.
4. Run `python scripts/check_repo.py`.

Do not add a universal rule for one unusual output unless the same failure is likely to recur. DissentKit should stay useful for ordinary reviews without turning every response into a template.

Documentation should use plain language, avoid unsupported claims, and distinguish single-context lenses from isolated model passes.
