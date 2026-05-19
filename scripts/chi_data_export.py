"""CHI 2027 data export pipeline.

Exports operational metrics from JSONL logs into CSV files suitable
for publication figures. Stdlib only (csv + json), no pandas dependency.

Usage:
    uv run python scripts/chi_data_export.py [--output-dir docs/chi-2027/data/]

Authority: CASE-PERSPECTIVE-001
CC-task: perspective-chi-evidence-infrastructure
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

# Default source directory for operational logs
DEFAULT_SOURCE_DIR = Path.home() / "hapax-state" / "research"

EIGENFORM_FIELDS = ["t", "presence", "flow_score", "imagination_salience", "stimmung_stance"]
GQI_FIELDS = ["timestamp", "final_gqi", "total_dus", "grounded_count"]
DENSITY_FIELDS = ["computed_at", "aggregate_density", "dominant_zone", "dominant_mode"]
EPISODE_FIELDS = ["episode_id", "start_ts", "end_ts", "episode_type", "notes"]


def _jsonl_to_csv(jsonl_path: Path, csv_path: Path, fields: list[str]) -> None:
    """Generic JSONL → CSV conversion with explicit field ordering."""
    rows: list[dict] = []
    with jsonl_path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def eigenform_to_csv(jsonl_path: Path, csv_path: Path) -> None:
    """Convert eigenform JSONL log to CSV."""
    _jsonl_to_csv(jsonl_path, csv_path, EIGENFORM_FIELDS)


def gqi_sessions_to_csv(jsonl_path: Path, csv_path: Path) -> None:
    """Convert GQI session summaries to CSV."""
    _jsonl_to_csv(jsonl_path, csv_path, GQI_FIELDS)


def density_snapshots_to_csv(jsonl_path: Path, csv_path: Path) -> None:
    """Convert density field snapshots to CSV."""
    _jsonl_to_csv(jsonl_path, csv_path, DENSITY_FIELDS)


def episodes_to_csv(jsonl_path: Path, csv_path: Path) -> None:
    """Convert episode annotations to CSV."""
    _jsonl_to_csv(jsonl_path, csv_path, EPISODE_FIELDS)


def export_all(output_dir: Path, source_dir: Path | None = None) -> None:
    """Run all exports from source_dir JSONL files into output_dir CSVs."""
    src = source_dir or DEFAULT_SOURCE_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    exports = [
        ("eigenform-log.jsonl", "eigenform.csv", eigenform_to_csv),
        ("gqi-sessions.jsonl", "gqi-sessions.csv", gqi_sessions_to_csv),
        ("density-snapshots.jsonl", "density.csv", density_snapshots_to_csv),
        ("chi-episodes.jsonl", "episodes.csv", episodes_to_csv),
    ]

    for source_name, dest_name, fn in exports:
        source_path = src / source_name
        if source_path.exists():
            fn(source_path, output_dir / dest_name)
            print(f"  exported {source_name} → {dest_name}")
        else:
            print(f"  skipped {source_name} (not found)")


def main() -> None:
    parser = argparse.ArgumentParser(description="CHI 2027 data export pipeline")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/chi-2027/data/"),
        help="Directory for output CSVs (default: docs/chi-2027/data/)",
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=None,
        help=f"Source JSONL directory (default: {DEFAULT_SOURCE_DIR})",
    )
    args = parser.parse_args()

    print(f"CHI 2027 data export → {args.output_dir}")
    export_all(args.output_dir, args.source_dir)
    print("done.")


if __name__ == "__main__":
    main()
    sys.exit(0)
