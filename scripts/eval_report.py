#!/usr/bin/env python3
"""Validate a manual DissentKit evaluation run and write a Markdown report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_raw_output(run_dir: Path, relative: str) -> Path:
    candidate = (run_dir / relative).resolve()
    try:
        candidate.relative_to(run_dir.resolve())
    except ValueError as exc:
        raise ValueError(f"Raw output escapes the run directory: {relative}") from exc
    if not candidate.is_file():
        raise ValueError(f"Raw output does not exist: {relative}")
    if candidate.stat().st_size == 0:
        raise ValueError(f"Raw output is empty: {relative}")
    return candidate


def make_report(run_path: Path, allow_partial: bool) -> str:
    cases = load_json(ROOT / "evals" / "cases.json")
    run = load_json(run_path)
    if not isinstance(cases, list) or not isinstance(run, dict):
        raise ValueError("Cases must be a list and the run must be an object")

    metadata = run.get("metadata")
    results = run.get("results")
    required_metadata = {
        "host",
        "model",
        "model_settings",
        "adapter",
        "source_commit",
        "grader",
        "date",
        "dissent_kit_version",
    }
    if not isinstance(metadata, dict) or not required_metadata <= metadata.keys():
        raise ValueError(f"metadata must include {sorted(required_metadata)}")
    if not isinstance(results, list):
        raise ValueError("results must be a list")
    if not results:
        raise ValueError("results must contain at least one graded case")
    for field in sorted(required_metadata):
        if not isinstance(metadata[field], str) or not metadata[field].strip():
            raise ValueError(f"metadata.{field} must be a non-empty string")

    cases_by_id = {case["id"]: case for case in cases}
    seen: set[str] = set()
    normalized: list[dict[str, object]] = []

    for result in results:
        if not isinstance(result, dict):
            raise ValueError("Every result must be an object")
        case_id = result.get("id")
        if case_id not in cases_by_id:
            raise ValueError(f"Unknown evaluation case: {case_id}")
        if case_id in seen:
            raise ValueError(f"Duplicate evaluation result: {case_id}")
        seen.add(case_id)

        grades = result.get("checks")
        expected_checks = cases_by_id[case_id]["checks"]
        if not isinstance(grades, list) or len(grades) != len(expected_checks):
            raise ValueError(
                f"{case_id} needs exactly {len(expected_checks)} check grades"
            )
        if any(type(grade) is not bool for grade in grades):
            raise ValueError(f"{case_id} check grades must be true or false")

        raw_output = result.get("raw_output")
        if not isinstance(raw_output, str) or not raw_output.strip():
            raise ValueError(f"{case_id} needs a raw_output path")
        safe_raw_output(run_path.parent, raw_output)

        normalized.append(
            {
                "id": case_id,
                "mode": cases_by_id[case_id]["expected_mode"],
                "passed": all(grades),
                "checks_passed": sum(grades),
                "checks_total": len(grades),
                "raw_output": raw_output.replace("\\", "/"),
                "notes": str(result.get("notes", "")).strip(),
            }
        )

    missing = set(cases_by_id) - seen
    if missing and not allow_partial:
        raise ValueError(
            "Run is incomplete. Missing cases: " + ", ".join(sorted(missing))
        )

    passed_cases = sum(bool(item["passed"]) for item in normalized)
    passed_checks = sum(int(item["checks_passed"]) for item in normalized)
    total_checks = sum(int(item["checks_total"]) for item in normalized)
    status = "Partial run" if missing else "Complete run"

    lines = [
        "# DissentKit evaluation report",
        "",
        f"- Host: {metadata['host']}",
        f"- Model: {metadata['model']}",
        f"- Model settings: {metadata['model_settings']}",
        f"- Adapter: {metadata['adapter']}",
        f"- Source commit: {metadata['source_commit']}",
        f"- Grader: {metadata['grader']}",
        f"- Date: {metadata['date']}",
        f"- DissentKit version: {metadata['dissent_kit_version']}",
        f"- Status: {status}",
        f"- Cases passed: {passed_cases}/{len(normalized)}",
        f"- Checks passed: {passed_checks}/{total_checks}",
        "",
        "A case passes only when every listed check passes. Raw outputs remain in the run directory.",
        "",
        "| Case | Expected mode | Result | Checks | Raw output | Notes |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in normalized:
        outcome = "Pass" if item["passed"] else "Fail"
        notes = (
            str(item["notes"]).replace("|", "\\|").replace("\n", "<br>") or "None"
        )
        lines.append(
            f"| {item['id']} | {item['mode']} | {outcome} | "
            f"{item['checks_passed']}/{item['checks_total']} | "
            f"[open]({quote(str(item['raw_output']), safe='/._-')}) | {notes} |"
        )
    if missing:
        lines.extend(["", "Missing cases: " + ", ".join(sorted(missing))])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path, help="Path to the run JSON file")
    parser.add_argument("--allow-partial", action="store_true")
    parser.add_argument("--output", type=Path, help="Write the report to this path")
    args = parser.parse_args()

    try:
        report = make_report(args.run.resolve(), args.allow_partial)
        if args.output:
            args.output.write_text(report, encoding="utf-8")
        else:
            print(report, end="")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Evaluation run is invalid: {exc}")
        return 1

    if args.output:
        print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
