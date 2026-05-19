"""CHI 2027 episode annotation tool.

Mark, tag, and query perspective-integration episodes — qualitative evidence
for the CHI paper on human-AI perspective coupling.

Usage:
    uv run python scripts/chi_episode_annotate.py annotate \
        --start 1716000000 --end 1716003600 \
        --type perspective-integration \
        --notes "Density field surfaced pattern operator hadn't noticed" \
        --ref "eigenform:state-log.jsonl:line:42"

    uv run python scripts/chi_episode_annotate.py query \
        --type perspective-integration --after 1716000000 --keyword "density"
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import uuid
from pathlib import Path

VALID_EPISODE_TYPES = frozenset(
    [
        "perspective-integration",
        "governance-constraint",
        "spontaneous-expression",
        "grounding-failure",
        "eigenform-convergence",
        "absence-detection",
    ]
)

DEFAULT_PATH = Path.home() / "hapax-state" / "research" / "chi-episodes.jsonl"


def annotate_episode(
    start_ts: float,
    end_ts: float,
    episode_type: str,
    notes: str,
    evidence_refs: list[str] | None = None,
    path: Path | None = None,
) -> dict:
    """Append a new episode annotation to the JSONL store."""
    if episode_type not in VALID_EPISODE_TYPES:
        raise ValueError(
            f"Invalid episode_type: {episode_type!r}. Must be one of: {sorted(VALID_EPISODE_TYPES)}"
        )

    entry = {
        "episode_id": uuid.uuid4().hex[:12],
        "start_ts": start_ts,
        "end_ts": end_ts,
        "episode_type": episode_type,
        "notes": notes,
        "evidence_refs": evidence_refs or [],
        "annotated_at": time.time(),
    }

    target = path or DEFAULT_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a") as f:
        f.write(json.dumps(entry) + "\n")

    return entry


def query_episodes(
    episode_type: str | None = None,
    after_ts: float | None = None,
    before_ts: float | None = None,
    keyword: str | None = None,
    path: Path | None = None,
) -> list[dict]:
    """Read and filter episodes from the JSONL store."""
    target = path or DEFAULT_PATH
    if not target.exists():
        return []

    episodes = []
    with target.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            episodes.append(json.loads(line))

    results = episodes

    if episode_type is not None:
        results = [e for e in results if e["episode_type"] == episode_type]

    if after_ts is not None:
        results = [e for e in results if e["start_ts"] >= after_ts]

    if before_ts is not None:
        results = [e for e in results if e["start_ts"] <= before_ts]

    if keyword is not None:
        kw_lower = keyword.lower()
        results = [e for e in results if kw_lower in e["notes"].lower()]

    return results


def _cli_annotate(args: argparse.Namespace) -> None:
    entry = annotate_episode(
        start_ts=args.start,
        end_ts=args.end,
        episode_type=args.type,
        notes=args.notes,
        evidence_refs=args.ref or [],
        path=Path(args.path) if args.path else None,
    )
    print(f"Annotated: {entry['episode_id']} ({entry['episode_type']})")


def _cli_query(args: argparse.Namespace) -> None:
    results = query_episodes(
        episode_type=args.type,
        after_ts=args.after,
        before_ts=args.before,
        keyword=args.keyword,
        path=Path(args.path) if args.path else None,
    )
    if not results:
        print("No episodes found.")
        return
    for ep in results:
        print(json.dumps(ep, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="CHI 2027 episode annotation tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # annotate subcommand
    ann = subparsers.add_parser("annotate", help="Annotate a new episode")
    ann.add_argument("--start", type=float, required=True, help="Start timestamp (epoch)")
    ann.add_argument("--end", type=float, required=True, help="End timestamp (epoch)")
    ann.add_argument(
        "--type",
        required=True,
        choices=sorted(VALID_EPISODE_TYPES),
        help="Episode type",
    )
    ann.add_argument("--notes", required=True, help="Free-text description")
    ann.add_argument("--ref", action="append", help="Evidence reference (repeatable)")
    ann.add_argument("--path", help="Override JSONL path")
    ann.set_defaults(func=_cli_annotate)

    # query subcommand
    qry = subparsers.add_parser("query", help="Query episodes")
    qry.add_argument("--type", choices=sorted(VALID_EPISODE_TYPES), help="Filter by type")
    qry.add_argument("--after", type=float, help="Filter: start_ts >= after")
    qry.add_argument("--before", type=float, help="Filter: start_ts <= before")
    qry.add_argument("--keyword", help="Filter by keyword in notes")
    qry.add_argument("--path", help="Override JSONL path")
    qry.set_defaults(func=_cli_query)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
    sys.exit(0)
