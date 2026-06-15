"""CLI validator for ResearchCase YAML files (the claim-assertion sibling of the
AuthorityCase validator).

Usage:
    uv run python -m rdlc.validator path/to/research-case.md
    uv run python -m rdlc.validator --strict path/to/research-case.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rdlc.research_case import RESEARCH_NO_GO_FIELDS, ResearchCase


def validate_file(path: Path, *, strict: bool = False) -> list[str]:
    """Validate a single research-case file. Returns a list of issues (empty = pass)."""
    issues: list[str] = []

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        return [f"cannot read file: {e}"]

    try:
        case = ResearchCase.from_yaml(text)
    except ValueError as e:
        return [f"schema validation failed: {e}"]
    except Exception as e:  # noqa: BLE001 - surface any parse failure as an issue, not a crash
        return [f"parse error: {e}"]

    for violation in case.no_go_violations():
        issues.append(f"no-go violation: {violation}")

    if strict:
        for field_name in RESEARCH_NO_GO_FIELDS:
            if field_name not in case.model_fields_set and field_name not in (
                case.model_extra or {}
            ):
                issues.append(f"missing no-go field: {field_name} (fail-closed: treated as true)")

    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate ResearchCase YAML files")
    parser.add_argument("files", nargs="+", help="Research-case file(s) to validate")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Require all no-go fields to be explicitly present",
    )
    args = parser.parse_args(argv)

    exit_code = 0
    for file_path in args.files:
        path = Path(file_path)
        issues = validate_file(path, strict=args.strict)
        if issues:
            print(f"FAIL {path}:")
            for issue in issues:
                print(f"  - {issue}")
            exit_code = 1
        else:
            print(f"PASS {path}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
