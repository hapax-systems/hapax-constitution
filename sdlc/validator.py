"""CLI validator for AuthorityCase YAML files.

Usage:
    uv run python -m sdlc.validator path/to/case.md
    uv run python -m sdlc.validator --strict path/to/case.md
    uv run python -m sdlc.validator path/to/*.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .authority_case import NO_GO_FIELDS, AuthorityCase


def validate_file(path: Path, *, strict: bool = False) -> list[str]:
    """Validate a single case file. Returns list of issues (empty = pass)."""
    issues: list[str] = []

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        return [f"cannot read file: {e}"]

    try:
        case = AuthorityCase.from_yaml(text)
    except ValueError as e:
        return [f"schema validation failed: {e}"]
    except Exception as e:
        return [f"parse error: {e}"]

    no_go = case.no_go_violations()
    for v in no_go:
        issues.append(f"no-go violation: {v}")

    if strict:
        for field_name in NO_GO_FIELDS:
            if field_name not in case.model_fields_set and field_name not in (
                case.model_extra or {}
            ):
                issues.append(
                    f"missing no-go field: {field_name} "
                    f"(fail-closed: treated as true)"
                )

    if case.parsed_stage().requires_axiom_check() and not case.axiom_compliance_checked:
        issues.append(
            f"stage {case.stage} requires axiom_compliance_checked=true"
        )

    rt = case.parsed_risk_tier()
    if rt is not None and rt.requires_axiom_scan() and not case.axiom_compliance_checked:
        issues.append(
            f"risk tier {case.risk_tier} requires axiom_compliance_checked=true"
        )

    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate AuthorityCase YAML files"
    )
    parser.add_argument("files", nargs="+", help="Case file(s) to validate")
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
