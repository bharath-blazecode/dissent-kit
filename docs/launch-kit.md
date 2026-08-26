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

## Homepage

Use the plain-language installation guide:

```text
https://github.com/bharath-blazecode/dissent-kit/blob/main/INSTALL.md
```

## Social preview

Upload `assets/dissent-kit-social-preview-v2.jpg` in the repository's social preview settings. The file is under GitHub's 1 MB limit. After uploading it, share the repository URL once and confirm that the custom image appears. The internal workflow graphic is `assets/dissent-kit-internal-workflow.jpg`.

## Release title

```text
DissentKit 0.3.0: dissent this, then fix it
```

## Release notes

```markdown
DissentKit is an open agent skill with two levels of review.

Direct Review handles ordinary writing, plans, arguments, and reversible choices. It opens with a verdict, names the largest risk and missing tradeoff, then returns a corrected version.

Deliberation is reserved for decisions with material downside or lock-in. Its five functional lenses come from chess: Rook for Direct, Bishop for Strategy, Knight for Blind spot, Queen for Synthesis, and King for Stakes. It challenges weak premises, tracks confidence changes, and ends with a falsifier and review point.

Version 0.3.0 includes adapters for Codex, Claude Code, ChatGPT, Cursor, GitHub Copilot, and assistants that accept a pasted prompt. People can try it without installing anything, and Codex users can request installation in one sentence. DissentKit states whether a deliberation used isolated model passes or one shared context.
```

## Launch post

```text
AI assistants are often agreeable at the moment you need resistance.

I built DissentKit, an open agent skill with two modes. Say "dissent this" for a verdict, the main risk, and a corrected version. Say "dissent this deeply" when a decision is expensive to reverse.

The deeper mode uses five chess-derived lenses with plain working names: Rook for Direct, Bishop for Strategy, Knight for Blind spot, Queen for Synthesis, and King for Stakes. Evidence runs through all five.

One design choice mattered to me: if five lenses run inside one model context, DissentKit says so. It does not sell a simulated panel as independent consensus.

The repo includes adapters for Codex, Claude Code, ChatGPT, Cursor, and GitHub Copilot, plus evaluation cases and the full decision pathway.

Repository: https://github.com/bharath-blazecode/dissent-kit
```

## Launch checklist

1. Confirm the release-preparation changes are on `main` and CI passes.
2. Add the description, homepage, and topics above in the repository settings.
3. Upload `assets/dissent-kit-social-preview-v2.jpg` and verify the shared-link preview.
4. Test installation from a clean folder.
5. Build the release ZIP and SHA-256 checksum with `python scripts/build_skill_package.py`.
6. Create and push the `v0.3.0` tag.
7. Create the GitHub release with the supplied notes and attach both generated files.
8. Run every case in `evals/cases.json` on the main host you plan to advertise.
9. Publish raw outputs and scoring notes before quoting a pass rate.
10. Share one concrete before-and-after example and turn recurring failures into evaluation fixtures.

## What to avoid

- Do not buy stars or imply adoption that has not happened.
- Do not call single-context lenses independent experts.
- Do not lead with the number of supported platforms. Lead with the problem and one convincing example.
- Do not publish a benchmark score without raw outputs and scoring notes.
