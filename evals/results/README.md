# Local evaluation results

Create one folder per run and keep its raw model outputs beside `run.json`:

```text
evals/results/2026-08-26-codex-model/
|-- run.json
`-- raw/
    |-- factual-lookup-does-not-trigger.md
    `-- ...
```

The repository ignores local run folders because raw outputs can be large and may contain private prompts. Review them for sensitive information before publishing.

Use this shape for `run.json`:

```json
{
  "metadata": {
    "host": "Codex desktop",
    "model": "record the exact model name",
    "model_settings": "record relevant settings or say default",
    "adapter": "root SKILL.md",
    "source_commit": "full commit SHA",
    "grader": "human name or documented grading method",
    "date": "2026-08-26",
    "dissent_kit_version": "0.3.0"
  },
  "results": [
    {
      "id": "factual-lookup-does-not-trigger",
      "raw_output": "raw/factual-lookup-does-not-trigger.md",
      "checks": [true, true],
      "notes": "Optional grading note"
    }
  ]
}
```

Generate a report:

```bash
python scripts/eval_report.py evals/results/2026-08-26-codex-model/run.json --output evals/results/2026-08-26-codex-model/report.md
```

Incomplete runs fail by default. Add `--allow-partial` only when the report clearly needs to describe a partial run.
