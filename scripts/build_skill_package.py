#!/usr/bin/env python3
"""Build a small, deterministic DissentKit installation archive."""

from __future__ import annotations

import argparse
import hashlib
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_FILES = (
    "SKILL.md",
    "LICENSE",
    "NOTICE.md",
    "agents/openai.yaml",
    "references/deliberation.md",
)
ZIP_TIMESTAMP = (2020, 1, 1, 0, 0, 0)


def skill_version() -> str:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r'^\s*version:\s*["\']?([^"\'\n]+)', text, re.MULTILINE)
    if not match:
        raise ValueError("SKILL.md metadata does not contain a version")
    return match.group(1).strip()


def build(output_dir: Path) -> tuple[Path, Path]:
    missing = [relative for relative in PACKAGE_FILES if not (ROOT / relative).is_file()]
    if missing:
        raise FileNotFoundError(f"Missing package files: {', '.join(missing)}")

    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"dissent-kit-{skill_version()}.zip"

    with zipfile.ZipFile(
        archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as bundle:
        for relative in PACKAGE_FILES:
            data = (ROOT / relative).read_bytes()
            info = zipfile.ZipInfo(f"dissent-kit/{relative}", ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, data)

    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum = archive.with_suffix(".zip.sha256")
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="ascii")
    return archive, checksum


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "dist",
        help="Directory for the ZIP and SHA-256 file (default: dist)",
    )
    args = parser.parse_args()

    archive, checksum = build(args.output_dir.resolve())
    with zipfile.ZipFile(archive) as bundle:
        names = bundle.namelist()

    print(f"Built {archive}")
    print(f"Checksum {checksum}")
    print("Contents:")
    for name in names:
        print(f"- {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
