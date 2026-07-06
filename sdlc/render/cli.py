"""CLI entry point for ``python -m hapax_sdlc.render``.

Modes:
    --repo <id>           render every artifact for one repo
    --all                 render every first-party repo
    --check               diff-mode (no-write); exit 1 on drift
    --dry-run             print to stdout instead of writing
    --target-root <path>  override the directory where files are written
                          (defaults to a sibling of hapax-constitution
                          named after the repo id)

Each render produces these artifacts:
    CITATION.cff
    codemeta.json
    .zenodo.json
    NOTICE.md
    CONTRIBUTING.md
    SECURITY.md
    SUPPORT.md
    GOVERNANCE.md
    .github/ISSUE_TEMPLATE/config.yml
    README.md (preamble section-replaced; rest preserved)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable

from sdlc.render import (
    citation_cff,
    codemeta_json,
    contributing_md,
    governance_md,
    issue_template_config_yml,
    notice_md,
    readme_section,
    security_md,
    support_md,
    zenodo_json,
)
from sdlc.render.repo_export import GENERATED_ARTIFACTS
from sdlc.render.repo_registry import (
    OperatorIdentity,
    RepoSpec,
    load_operator_identity,
    load_registry,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hapax_sdlc.render",
        description=(
            "Render repo-presentation files (CITATION.cff, codemeta.json, "
            ".zenodo.json, NOTICE.md, CONTRIBUTING.md, SECURITY.md, "
            "SUPPORT.md, GOVERNANCE.md, .github/ISSUE_TEMPLATE/config.yml, "
            "README.md preamble) for one or all repos."
        ),
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--repo", help="Repo id from repos.yaml")
    target.add_argument(
        "--all",
        action="store_true",
        help="Render every first-party repo (skips upstream forks)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Drift-detection mode: print diffs and exit 1 if any drift exists",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print rendered files to stdout instead of writing",
    )
    parser.add_argument(
        "--target-root",
        type=Path,
        default=None,
        help=(
            "Override the directory where files are written. Defaults to "
            "`<hapax-constitution-parent>/<repo_id>/`."
        ),
    )
    parser.add_argument(
        "--file",
        choices=GENERATED_ARTIFACTS,
        help="Render a single artifact instead of the full set",
    )
    return parser


def render_artifacts(repo: RepoSpec, identity: OperatorIdentity) -> dict[str, str]:
    """Return the full rendered-artifact map for ``repo``."""
    if not repo.is_first_party:
        return {}
    return {
        "CITATION.cff": citation_cff.render(repo, identity),
        "codemeta.json": codemeta_json.render(repo, identity),
        ".zenodo.json": zenodo_json.render(repo, identity),
        "NOTICE.md": notice_md.render(repo),
        "CONTRIBUTING.md": contributing_md.render(repo),
        "SECURITY.md": security_md.render(repo, identity),
        "SUPPORT.md": support_md.render(repo),
        "GOVERNANCE.md": governance_md.render(repo),
        ".github/ISSUE_TEMPLATE/config.yml": issue_template_config_yml.render(repo),
        "README.md": readme_section.render(repo),
    }


def default_target_root(repo: RepoSpec) -> Path:
    """Default location to write rendered files for ``repo``.

    Renderer is invoked from `hapax-constitution`; sibling directory
    named after the repo id is the deploy target. This is just a
    default — `--target-root` overrides.
    """
    constitution_root = Path(__file__).resolve().parent.parent.parent
    return constitution_root.parent / repo.name


def write_or_compare(target_root: Path, artifacts: dict[str, str], *, check_only: bool) -> int:
    """Write artifacts to ``target_root`` or compare for drift.

    Returns the count of drifted (or written) files. README is treated
    specially: existing body is preserved.
    """
    drift_count = 0
    target_root.mkdir(parents=True, exist_ok=True)
    for filename, body in artifacts.items():
        target = target_root / filename
        if filename == "README.md":
            existing = target.read_text(encoding="utf-8") if target.exists() else ""
            new_body = readme_section.replace_section(existing, body)
        else:
            new_body = body
        if check_only:
            current = target.read_text(encoding="utf-8") if target.exists() else ""
            if current != new_body:
                drift_count += 1
                print(f"DRIFT {target}", file=sys.stderr)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(new_body, encoding="utf-8")
    return drift_count


def render_repo(
    repo: RepoSpec,
    identity: OperatorIdentity,
    *,
    target_root: Path | None,
    dry_run: bool,
    check_only: bool,
    only_file: str | None,
) -> int:
    """Render one repo. Returns drift count (0 if clean / wrote OK)."""
    if not repo.is_first_party:
        print(
            f"skipping upstream fork '{repo.id}' (render is inert for forks)",
            file=sys.stderr,
        )
        return 0
    artifacts = render_artifacts(repo, identity)
    if only_file:
        artifacts = {only_file: artifacts[only_file]}
    if dry_run:
        for filename, body in artifacts.items():
            sep = "=" * 70
            print(f"\n{sep}\n# {filename}\n{sep}")
            print(body)
        return 0
    actual_target = target_root or default_target_root(repo)
    return write_or_compare(actual_target, artifacts, check_only=check_only)


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    registry = load_registry()
    identity = load_operator_identity()

    repo_ids: list[str]
    if args.all:
        repo_ids = [rid for rid, spec in registry.items() if spec.is_first_party]
    else:
        if args.repo not in registry:
            parser.error(f"unknown repo id '{args.repo}'; known: {sorted(registry)}")
        repo_ids = [args.repo]

    total_drift = 0
    for rid in repo_ids:
        repo = registry[rid]
        total_drift += render_repo(
            repo,
            identity,
            target_root=args.target_root,
            dry_run=args.dry_run,
            check_only=args.check,
            only_file=args.file,
        )
    if args.check and total_drift:
        print(f"check failed: {total_drift} drift(s)", file=sys.stderr)
        return 1
    return 0
