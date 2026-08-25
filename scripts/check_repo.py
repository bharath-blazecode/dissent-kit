#!/usr/bin/env python3
"""Validate the DissentKit repository without third-party packages."""

from __future__ import annotations

import json
import re
import struct
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


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
        "evals/cases.json",
        "assets/dissent-kit-social-preview-v2.png",
        "assets/dissent-kit-internal-workflow.png",
        "platforms/codex/README.md",
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


def read_png_size(relative: str) -> tuple[int, int] | None:
    path = ROOT / relative
    try:
        with path.open("rb") as handle:
            signature = handle.read(24)
    except OSError as exc:
        fail(f"Cannot read {relative}: {exc}")
        return None

    if len(signature) < 24 or signature[:8] != b"\x89PNG\r\n\x1a\n":
        fail(f"{relative} is not a valid PNG")
        return None
    return struct.unpack(">II", signature[16:24])


def check_preview_images() -> None:
    preview = "assets/dissent-kit-social-preview-v2.png"
    preview_size = read_png_size(preview)
    if preview_size is None:
        return
    width, height = preview_size
    if width < 1200 or height < 600:
        fail(f"Social preview is too small: {width}x{height}")
    ratio = width / height
    if not 1.8 <= ratio <= 2.2:
        fail(f"Social preview should be close to 2:1, got {width}x{height}")

    workflow = "assets/dissent-kit-internal-workflow.png"
    workflow_size = read_png_size(workflow)
    if workflow_size is None:
        return
    width, height = workflow_size
    if width < 1400 or height < 750:
        fail(f"Internal workflow image is too small: {width}x{height}")
    ratio = width / height
    if not 1.6 <= ratio <= 1.95:
        fail(f"Internal workflow image should be wide, got {width}x{height}")


def check_deprecated_files() -> None:
    if any(ROOT.rglob(".cursorrules")):
        fail("Deprecated .cursorrules file found; use .cursor/rules/*.mdc")


def main() -> int:
    check_required_files()
    check_skill_frontmatter()
    check_markdown_links()
    check_public_prose()
    check_eval_cases()
    check_preview_images()
    check_deprecated_files()

    if ERRORS:
        print("DissentKit validation failed:")
        for error in ERRORS:
            print(f"- {error}")
        return 1

    print("DissentKit validation passed.")
    print("Checked skill metadata, links, prose, fixtures, platform files, and artwork.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
