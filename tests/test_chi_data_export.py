"""Tests for CHI 2027 data export pipeline."""

import json


def test_export_eigenform_csv(tmp_path):
    """Eigenform log converts to CSV."""
    from scripts.chi_data_export import eigenform_to_csv

    log_path = tmp_path / "eigenform-log.jsonl"
    log_path.write_text(
        json.dumps(
            {
                "t": 1716000000,
                "presence": 0.9,
                "flow_score": 0.5,
                "imagination_salience": 0.3,
                "stimmung_stance": "nominal",
            }
        )
        + "\n"
        + json.dumps(
            {
                "t": 1716000003,
                "presence": 0.85,
                "flow_score": 0.6,
                "imagination_salience": 0.4,
                "stimmung_stance": "seeking",
            }
        )
        + "\n"
    )
    csv_path = tmp_path / "eigenform.csv"
    eigenform_to_csv(log_path, csv_path)
    assert csv_path.exists()
    lines = csv_path.read_text().strip().split("\n")
    assert len(lines) == 3  # header + 2 rows
    assert "presence" in lines[0]


def test_export_gqi_csv(tmp_path):
    """GQI session summaries convert to CSV."""
    from scripts.chi_data_export import gqi_sessions_to_csv

    log_path = tmp_path / "gqi-sessions.jsonl"
    log_path.write_text(
        json.dumps(
            {"timestamp": 1716000000, "final_gqi": 0.72, "total_dus": 5, "grounded_count": 4}
        )
        + "\n"
    )
    csv_path = tmp_path / "gqi-sessions.csv"
    gqi_sessions_to_csv(log_path, csv_path)
    assert csv_path.exists()
    lines = csv_path.read_text().strip().split("\n")
    assert len(lines) == 2
    assert "final_gqi" in lines[0]


def test_export_density_csv(tmp_path):
    """Density field snapshots convert to CSV."""
    from scripts.chi_data_export import density_snapshots_to_csv

    log_path = tmp_path / "density-snapshots.jsonl"
    log_path.write_text(
        json.dumps(
            {
                "computed_at": 1716000000,
                "aggregate_density": 0.45,
                "dominant_zone": "perception",
                "dominant_mode": "NEWS",
            }
        )
        + "\n"
    )
    csv_path = tmp_path / "density.csv"
    density_snapshots_to_csv(log_path, csv_path)
    assert csv_path.exists()


def test_export_episodes_csv(tmp_path):
    """Episode annotations convert to CSV."""
    from scripts.chi_data_export import episodes_to_csv

    log_path = tmp_path / "chi-episodes.jsonl"
    log_path.write_text(
        json.dumps(
            {
                "episode_id": "abc123",
                "start_ts": 1716000000,
                "end_ts": 1716003600,
                "episode_type": "perspective-integration",
                "notes": "test",
            }
        )
        + "\n"
    )
    csv_path = tmp_path / "episodes.csv"
    episodes_to_csv(log_path, csv_path)
    assert csv_path.exists()
