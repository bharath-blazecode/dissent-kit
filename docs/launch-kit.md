# DissentKit launch kit

No launch copy can guarantee stars. The aim is to make the project easy to understand, test, and share.

## GitHub description

Use this as the repository description:

> An open agent skill for verdict-first critique and structured dissent on decisions that are expensive to get wrong.

## Suggested topics

```text
agent-skills
ai-agents
codex
claude-code
cursor
github-copilot
llm-evaluation
decision-making
prompt-engineering
open-source
```

## Social preview

Upload `assets/dissent-kit-social-preview-v2.png` in the repository's social preview settings. The same image appears at the top of the README. The internal workflow graphic is `assets/dissent-kit-internal-workflow.png`.

## Release title

```text
DissentKit 0.2.0: dissent this, then fix it
```

## Release notes

```markdown
DissentKit is an open agent skill with two levels of review.

Direct Review handles ordinary writing, plans, arguments, and reversible choices. It opens with a verdict, names the largest risk and missing tradeoff, then returns a corrected version.

Deliberation is reserved for decisions with material downside or lock-in. Its five functional lenses come from chess: Rook for Direct, Bishop for Strategy, Knight for Blind spot, Queen for Synthesis, and King for Stakes. It challenges weak premises, tracks confidence changes, and ends with a falsifier and review point.

The first release includes adapters for Codex, Claude Code, ChatGPT, Cursor, GitHub Copilot, and assistants that accept a pasted prompt. It also states whether a deliberation used isolated model passes or one shared context.
```

## Launch post

```text
AI assistants are often agreeable at the moment you need resistance.

I built DissentKit, an open agent skill with two modes. Say "dissent this" for a verdict, the main risk, and a corrected version. Say "dissent this deeply" when a decision is expensive to reverse.

The deeper mode uses five chess-derived lenses with plain working names: Rook for Direct, Bishop for Strategy, Knight for Blind spot, Queen for Synthesis, and King for Stakes. Evidence runs through all five.

One design choice mattered to me: if five lenses run inside one model context, DissentKit says so. It does not sell a simulated panel as independent consensus.

The repo includes adapters for Codex, Claude Code, ChatGPT, Cursor, and GitHub Copilot, plus evaluation cases and the full decision pathway.

Repository: [add the public URL after publishing]
```

## Launch checklist

1. Create the public repository with the name `dissent-kit`.
2. Add the description and topics above.
3. Upload the social preview image.
4. Pin the worked example near the top of the README if early readers miss it.
5. Create the `0.1.0` release with the supplied notes.
6. Run every case in `evals/cases.json` on the main host you plan to advertise.
7. Publish the raw outputs and scoring notes before quoting a pass rate.
8. Share one concrete before-and-after example, not a list of features.
9. Ask early users for failed prompts and turn recurring failures into fixtures.
10. Tag the first stable revision only after installation has been tested from a clean folder.

## What to avoid

- Do not buy stars or imply adoption that has not happened.
- Do not call single-context lenses independent experts.
- Do not lead with the number of supported platforms. Lead with the problem and one convincing example.
- Do not publish a benchmark score without raw outputs and scoring notes.
