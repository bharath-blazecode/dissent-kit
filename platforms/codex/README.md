# Codex adapter

The preferred Codex installation is the root DissentKit skill, not an `AGENTS.md` file.

For personal use, place the repository at `~/.agents/skills/dissent-kit/`. For one project, place it at `<repo>/.agents/skills/dissent-kit/`.

Use `$dissent-kit` for explicit invocation. The natural call phrase is `dissent this`; use `dissent this deeply` for Deliberation. Codex may also select the skill when the request matches its description.

## Optional repository-wide instructions

Copy [AGENTS.example.md](AGENTS.example.md) into an existing repository's `AGENTS.md` only when you want DissentKit's review style applied to every relevant Codex task in that repository. Merge the section with existing instructions instead of replacing them.

`AGENTS.md` is persistent project guidance. It is broader than an optional skill and can affect review behavior throughout the repository.
