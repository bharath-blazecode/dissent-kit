# Maintainer guide

## Sources of truth

`SKILL.md` defines activation, mode selection, Direct Review, and the writing standard. `references/deliberation.md` defines the deeper protocol. Standalone platform adapters repeat the parts their host needs because they cannot import the root skill at runtime.

When the shared behavior changes, run `python scripts/check_repo.py`. Adapter parity validation checks the natural invocation phrases, certainty labels, diagnosis-only exception, response to new evidence, no-invented-flaw rule, chess-derived lenses, execution label, pre-mortem, independence limitation, falsifier, and first action.

The Claude Code adapter installs the root skill, so its README is installation guidance rather than a second copy of the full contract.

## Version updates

Keep the version synchronized in:

- `SKILL.md` metadata
- the README version badge
- the latest `CHANGELOG.md` heading
- the release ZIP name in `INSTALL.md`
- the release title in `docs/launch-kit.md`
- the package filename in `.github/workflows/validate.yml`

The repository validator checks the first five locations. CI will fail if its package filename is stale because the ZIP test will not find the generated archive.

## Package and CI

Run:

```bash
python scripts/check_repo.py
python scripts/build_skill_package.py
python -m zipfile -t dist/dissent-kit-0.3.0.zip
```

CI runs the same checks on Windows with Python 3.10 and Linux with Python 3.13. The Linux job also keeps the ZIP and checksum as a workflow artifact. Attach those two files to the matching GitHub release.

## GitHub repository settings

These settings live on GitHub and cannot be completed by merging files:

- Description: `An open agent skill for verdict-first critique and structured dissent on decisions that are expensive to get wrong.`
- Homepage: `https://github.com/bharath-blazecode/dissent-kit/blob/main/INSTALL.md`
- Topics: use the list in `docs/launch-kit.md`.
- Social preview: upload `assets/dissent-kit-social-preview-v2.jpg`.
- Release: create the version tag, publish the release notes, and attach the generated ZIP and checksum.

After changing repository settings, inspect the public repository page and one shared-link preview. Do not assume that saving the settings updated cached previews immediately.
