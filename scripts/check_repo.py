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
        "examples/quick-comparison.md",
        "evals/cases.json",
        "evals/results/README.md",
        "docs/evidence.md",
        "assets/dissent-kit-social-preview-v2.jpg",
        "assets/dissent-kit-internal-workflow.jpg",
        "scripts/build_skill_package.py",
        "scripts/eval_report.py",
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


def main() -> int:
    check_required_files()
    check_skill_frontmatter()
    check_markdown_links()
    check_public_prose()
    check_eval_cases()
    check_preview_images()
    check_deprecated_files()
    check_python_syntax()

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
