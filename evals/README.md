# Evaluation guide

`cases.json` is a small contract suite for DissentKit. It tests mode selection and review behavior. It is not a benchmark result, and the repository does not claim that every model will pass it.

## Run a manual evaluation

1. Choose a host and model.
2. Install or paste the matching DissentKit adapter.
3. Send each `request` from `cases.json` in a fresh conversation.
4. Check the output against every item in `checks`.
5. Record the host, model, date, pass count, failures, and raw outputs.

Use a fresh conversation for each case so earlier examples do not steer later responses.

## What to record

```text
Host:
Model:
Date:
DissentKit version:
Cases passed:
Cases failed:
Failure notes:
Raw output location:
```

Do not publish a pass rate without the raw outputs and scoring notes. Small prompt suites are useful for regression checks, but they do not prove general reliability.

## Repository checks

Run:

```bash
python scripts/check_repo.py
```

This validates packaging, frontmatter, local links, fixture structure, the social-preview asset, deprecated Cursor files, and a short list of claims the project must not make.
