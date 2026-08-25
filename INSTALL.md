# Install DissentKit

Choose the assistant you use. You do not need to understand Git or the command line to try DissentKit.

## Try it anywhere without installing

1. Open [the universal prompt](platforms/universal/PROMPT.md).
2. Copy the full prompt into your AI assistant.
3. Say `dissent this` for a direct review or `dissent this deeply` for Deliberation.

This method works for assistants that accept custom instructions or a pasted prompt. It applies to the current conversation unless your assistant lets you save it permanently.

## Codex automatic installation

Open a Codex task and paste this request:

```text
$skill-installer Install DissentKit from https://github.com/bharath-blazecode/dissent-kit using the repository root, and name it dissent-kit.
```

Codex downloads the repository and installs it as a personal skill. It becomes available on the next turn.

Use either call:

```text
$dissent-kit Review this plan.
```

```text
Dissent this.
```

## Codex manual installation

1. On GitHub, select **Code**, then **Download ZIP**.
2. Extract the ZIP and rename the extracted folder to `dissent-kit`.
3. Move it into your personal skills folder at `~/.agents/skills/dissent-kit/`.

On Windows, `~` means your user folder, usually `C:\Users\YOUR-NAME`.

For one repository only, place the folder at `<repo>/.agents/skills/dissent-kit/`.

## Claude Code

Copy the DissentKit folder to `~/.claude/skills/dissent-kit/`. Then say `dissent this` or `dissent this deeply` in Claude Code.

See [the Claude Code notes](platforms/claude-code/README.md) for the shorter technical version.

## ChatGPT

The quickest option is to paste [the universal prompt](platforms/universal/PROMPT.md) into a conversation.

If your account or workspace allows GPT creation, paste [the Custom GPT instructions](platforms/chatgpt/custom-gpt-instructions.md) into the GPT's Instructions field. Save the GPT to make the behavior available in future conversations.

## Cursor

Copy [dissent-kit.mdc](platforms/cursor/.cursor/rules/dissent-kit.mdc) into `.cursor/rules/dissent-kit.mdc` inside your project.

## GitHub Copilot

Copy [copilot-instructions.md](platforms/copilot/copilot-instructions.md) into `.github/copilot-instructions.md` inside your repository.

## What changes when multiple agents are available?

Both DissentKit modes work on every supported platform.

Direct Review uses one focused review pass. Deliberation adds the pre-mortem, five chess-derived lenses, challenge round, confidence movement, unresolved issue, and falsifier.

When the host supports isolated agents, DissentKit can run the lenses as separate passes. Otherwise, it runs the same lenses sequentially in one context. A single-context review provides structured coverage, but it is not independent consensus.
