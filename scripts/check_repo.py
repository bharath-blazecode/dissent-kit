#!/usr/bin/env python3
"""Validate the DissentKit repository without third-party packages."""

from __future__ import annotations

import ast
import json
import re
import struct
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
INSTRUCTION_ADAPTERS = (
    "SKILL.md",
    "platforms/chatgpt/custom-gpt-instructions.md",
    "platforms/codex/AGENTS.example.md",
    "platforms/copilot/copilot-instructions.md",
    "platforms/cursor/.cursor/rules/dissent-kit.mdc",
    "platforms/universal/PROMPT.md",
)
PACKAGE_FILES = {
    "SKILL.md",
    "LICENSE",
    "NOTICE.md",
    "agents/openai.yaml",
    "references/deliberation.md",
}


def fail(message: str) -> None:
    ERRORS.append(message)


def check_required_files() -> None:
    required = [
        "SKILL.md",
        "README.md",
        "LICENSE",
        "NOTICE.md",
        "agents/openai.yaml",
        "references/deliberation.md",
        "examples/example-review.md",
        "examples/quick-comparison.md",
        "evals/cases.json",
        "evals/results/README.md",
        "docs/evidence.md",
        "assets/dissent-kit-social-preview-v2.jpg",
        "assets/dissent-kit-internal-workflow.jpg",
        "scripts/build_skill_package.py",
        "scripts/eval_report.py",
        "docs/maintainer-guide.md",
        ".github/CODEOWNERS",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/workflows/validate.yml",
        ".github/ISSUE_TEMPLATE/bug_report.yml",
        ".github/ISSUE_TEMPLATE/feature_request.yml",
        ".github/ISSUE_TEMPLATE/config.yml",
        "platforms/codex/README.md",
        "platforms/codex/AGENTS.example.md",
        "platforms/chatgpt/custom-gpt-instructions.md",
        "platforms/claude-code/README.md",
        "platforms/copilot/copilot-instructions.md",
        "platforms/universal/PROMPT.md",
        "platforms/cursor/.cursor/rules/dissent-kit.mdc",
    ]
    for relative in required:
        if not (ROOT / relative).is_file():
            fail(f"Missing required file: {relative}")


def check_skill_frontmatter() -> None:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail("SKILL.md has no valid YAML frontmatter block")
        return

    frontmatter = match.group(1)
    name_match = re.search(r"^name:\s*([^\n]+)$", frontmatter, re.MULTILINE)
    description_match = re.search(
        r"^description:\s*([^\n]+)$", frontmatter, re.MULTILINE
    )
    if not name_match or name_match.group(1).strip() != "dissent-kit":
        fail("SKILL.md name must be dissent-kit")
    if not description_match or len(description_match.group(1).strip()) < 40:
        fail("SKILL.md needs a discriminating description")
    if len(text.splitlines()) > 180:
        fail("SKILL.md is too long for the entrypoint; move detail to references")


def skill_version() -> str | None:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r'^\s*version:\s*["\']?([^"\'\n]+)', text, re.MULTILINE)
    if not match:
        fail("SKILL.md metadata needs a version")
        return None
    return match.group(1).strip()


def check_version_consistency() -> None:
    version = skill_version()
    if version is None:
        return
    expected = {
        "README.md": f"version-{version}-",
        "CHANGELOG.md": f"## {version}",
        "INSTALL.md": f"dissent-kit-{version}.zip",
        "docs/launch-kit.md": f"DissentKit {version}:",
    }
    for relative, marker in expected.items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        if marker not in text:
            fail(f"Version {version} is not reflected in {relative}")


def check_openai_metadata() -> None:
    path = ROOT / "agents" / "openai.yaml"
    text = path.read_text(encoding="utf-8")
    values = {}
    for key in ("display_name", "short_description", "brand_color", "default_prompt"):
        match = re.search(rf'^\s+{key}:\s+"([^"]+)"\s*$', text, re.MULTILINE)
        if not match:
            fail(f"agents/openai.yaml needs a quoted {key}")
            continue
        values[key] = match.group(1)
    if values.get("display_name") != "DissentKit":
        fail("agents/openai.yaml display_name must be DissentKit")
    short_description = values.get("short_description", "")
    if short_description and not 25 <= len(short_description) <= 64:
        fail("agents/openai.yaml short_description must be 25 to 64 characters")
    brand_color = values.get("brand_color", "")
    if brand_color and not re.fullmatch(r"#[0-9A-Fa-f]{6}", brand_color):
        fail("agents/openai.yaml brand_color must be a six-digit hex color")
    if "$dissent-kit" not in values.get("default_prompt", ""):
        fail("agents/openai.yaml default_prompt must mention $dissent-kit")
    if not re.search(
        r"^\s+allow_implicit_invocation:\s+true\s*$", text, re.MULTILINE
    ):
        fail("agents/openai.yaml must preserve implicit invocation")


def check_adapter_parity() -> None:
    markers = {
        "direct invocation": "dissent this",
        "deep invocation": "dissent this deeply",
        "certainty labels": "[certain]",
        "diagnosis-only exception": "diagnosis only",
        "new-evidence update": "new evidence",
        "no invented flaw": "already strong",
        "execution label": "single-context deliberation",
        "pre-mortem": "pre-mortem",
        "falsifier": "falsifier",
        "first action": "first action",
        "independence limitation": "independent",
    }
    chess_markers = ("rook", "bishop", "knight", "queen", "king")
    for relative in INSTRUCTION_ADAPTERS:
        text = (ROOT / relative).read_text(encoding="utf-8").lower()
        if relative == "SKILL.md":
            text += (ROOT / "references" / "deliberation.md").read_text(
                encoding="utf-8"
            ).lower()
        for label, marker in markers.items():
            if marker not in text:
                fail(f"Adapter parity failed in {relative}: missing {label}")
        for marker in chess_markers:
            if marker not in text:
                fail(f"Adapter parity failed in {relative}: missing {marker} lens")


def check_package_manifest() -> None:
    path = ROOT / "scripts" / "build_skill_package.py"
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    manifest = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "PACKAGE_FILES"
            for target in node.targets
        ):
            try:
                manifest = set(ast.literal_eval(node.value))
            except (TypeError, ValueError):
                fail("Package manifest must be a literal sequence of file paths")
                return
            break
    if manifest != PACKAGE_FILES:
        fail("Package manifest must contain exactly the five core skill files")


def check_markdown_links() -> None:
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in list(ROOT.rglob("*.md")) + list(ROOT.rglob("*.mdc")):
        text = path.read_text(encoding="utf-8")
        for target in pattern.findall(text):
            clean = target.strip().split("#", 1)[0]
            if not clean or re.match(r"^(https?://|mailto:)", clean):
                continue
            resolved = (path.parent / clean).resolve()
            if not resolved.exists():
                fail(f"Broken local link in {path.relative_to(ROOT)}: {target}")


def check_public_prose() -> None:
    banned_claims = [
        "five independent passes",
        "install once",
        "works natively across",
        "only claude code",
    ]
    for path in list(ROOT.rglob("*.md")) + list(ROOT.rglob("*.mdc")):
        text = path.read_text(encoding="utf-8")
        if "\u2014" in text or "\u2013" in text:
            fail(f"Humanizer check failed in {path.relative_to(ROOT)}: dash character")
        lower = text.lower()
        for claim in banned_claims:
            if claim in lower:
                fail(f"Overclaim in {path.relative_to(ROOT)}: {claim}")


def check_eval_cases() -> None:
    path = ROOT / "evals/cases.json"
    try:
        cases = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"Cannot parse evals/cases.json: {exc}")
        return

    if not isinstance(cases, list) or len(cases) < 10:
        fail("evals/cases.json must contain at least 10 cases")
        return

    seen: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            fail(f"Eval case {index} is not an object")
            continue
        missing = {"id", "request", "expected_mode", "checks"} - set(case)
        if missing:
            fail(f"Eval case {index} is missing: {sorted(missing)}")
        case_id = case.get("id")
        if case_id in seen:
            fail(f"Duplicate eval id: {case_id}")
        if isinstance(case_id, str):
            seen.add(case_id)
        if not isinstance(case.get("checks"), list) or not case.get("checks"):
            fail(f"Eval case {case_id} has no checks")


def read_jpeg_size(relative: str) -> tuple[int, int] | None:
    path = ROOT / relative
    try:
        with path.open("rb") as handle:
            if handle.read(2) != b"\xff\xd8":
                fail(f"{relative} is not a valid JPEG")
                return None

            while True:
                byte = handle.read(1)
                if not byte:
                    break
                if byte != b"\xff":
                    continue

                marker = handle.read(1)
                while marker == b"\xff":
                    marker = handle.read(1)
                if not marker or marker in {b"\xd8", b"\xd9"}:
                    continue

                length_bytes = handle.read(2)
                if len(length_bytes) != 2:
                    break
                segment_length = struct.unpack(">H", length_bytes)[0]
                if segment_length < 2:
                    break

                if marker[0] in {
                    0xC0,
                    0xC1,
                    0xC2,
                    0xC3,
                    0xC5,
                    0xC6,
                    0xC7,
                    0xC9,
                    0xCA,
                    0xCB,
                    0xCD,
                    0xCE,
                    0xCF,
                }:
                    dimensions = handle.read(5)
                    if len(dimensions) != 5:
                        break
                    height, width = struct.unpack(">HH", dimensions[1:])
                    return width, height

                handle.seek(segment_length - 2, 1)
    except OSError as exc:
        fail(f"Cannot read {relative}: {exc}")
        return None

    fail(f"Cannot read JPEG dimensions from {relative}")
    return None


def check_preview_images() -> None:
    preview = "assets/dissent-kit-social-preview-v2.jpg"
    preview_size = read_jpeg_size(preview)
    if preview_size is None:
        return
    width, height = preview_size
    if width < 1200 or height < 600:
        fail(f"Social preview is too small: {width}x{height}")
    ratio = width / height
    if not 1.8 <= ratio <= 2.2:
        fail(f"Social preview should be close to 2:1, got {width}x{height}")
    if (ROOT / preview).stat().st_size >= 1_000_000:
        fail(f"Social preview must be under 1 MB: {preview}")

    workflow = "assets/dissent-kit-internal-workflow.jpg"
    workflow_size = read_jpeg_size(workflow)
    if workflow_size is None:
        return
    width, height = workflow_size
    if width < 1400 or height < 750:
        fail(f"Internal workflow image is too small: {width}x{height}")
    ratio = width / height
    if not 1.6 <= ratio <= 1.95:
        fail(f"Internal workflow image should be wide, got {width}x{height}")
    if (ROOT / workflow).stat().st_size >= 1_000_000:
        fail(f"Internal workflow image must be under 1 MB: {workflow}")


def check_deprecated_files() -> None:
    if any(ROOT.rglob(".cursorrules")):
        fail("Deprecated .cursorrules file found; use .cursor/rules/*.mdc")


def check_python_syntax() -> None:
    for path in (ROOT / "scripts").glob("*.py"):
        try:
            source = path.read_text(encoding="utf-8")
            compile(source, str(path), "exec")
        except (OSError, SyntaxError) as exc:
            fail(f"Invalid Python script {path.relative_to(ROOT)}: {exc}")


def check_empty_files() -> None:
    ignored_parts = {".git", "dist", "__pycache__"}
    for path in ROOT.rglob("*"):
        relative_parts = path.relative_to(ROOT).parts
        if not path.is_file() or ignored_parts.intersection(relative_parts):
            continue
        if path.stat().st_size == 0:
            fail(f"Empty repository file: {path.relative_to(ROOT)}")


def main() -> int:
    check_required_files()
    check_skill_frontmatter()
    check_version_consistency()
    check_openai_metadata()
    check_adapter_parity()
    check_package_manifest()
    check_markdown_links()
    check_public_prose()
    check_eval_cases()
    check_preview_images()
    check_deprecated_files()
    check_python_syntax()
    check_empty_files()

    if ERRORS:
        print("DissentKit validation failed:")
        for error in ERRORS:
            print(f"- {error}")
        return 1

    print("DissentKit validation passed.")
    print(
        "Checked skill metadata, links, prose, fixtures, scripts, platform files, "
        "and artwork."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
