"""Tests for CHI 2027 episode annotation CLI tool."""

from __future__ import annotations


def test_annotate_creates_episode(tmp_path):
    """Episode annotation creates a JSONL entry."""
    from scripts.chi_episode_annotate import annotate_episode, query_episodes

    path = tmp_path / "chi-episodes.jsonl"
    annotate_episode(
        start_ts=1716000000.0,
        end_ts=1716003600.0,
        episode_type="perspective-integration",
        notes="Density field surfaced pattern operator hadn't noticed",
        evidence_refs=["eigenform:state-log.jsonl:line:42"],
        path=path,
    )
    episodes = query_episodes(path=path)
    assert len(episodes) == 1
    assert episodes[0]["episode_type"] == "perspective-integration"
    assert episodes[0]["notes"] == "Density field surfaced pattern operator hadn't noticed"
    assert episodes[0]["evidence_refs"] == ["eigenform:state-log.jsonl:line:42"]
    assert episodes[0]["start_ts"] == 1716000000.0
    assert episodes[0]["end_ts"] == 1716003600.0
    assert len(episodes[0]["episode_id"]) == 12
    assert "annotated_at" in episodes[0]


def test_query_by_type(tmp_path):
    """Episodes can be filtered by type."""
    from scripts.chi_episode_annotate import annotate_episode, query_episodes

    path = tmp_path / "chi-episodes.jsonl"
    annotate_episode(
        start_ts=1.0, end_ts=2.0, episode_type="perspective-integration", notes="a", path=path
    )
    annotate_episode(
        start_ts=3.0, end_ts=4.0, episode_type="governance-constraint", notes="b", path=path
    )

    results = query_episodes(episode_type="perspective-integration", path=path)
    assert len(results) == 1
    assert results[0]["notes"] == "a"


def test_query_by_date_range(tmp_path):
    """Episodes can be filtered by timestamp range."""
    from scripts.chi_episode_annotate import annotate_episode, query_episodes

    path = tmp_path / "chi-episodes.jsonl"
    annotate_episode(
        start_ts=100.0,
        end_ts=200.0,
        episode_type="perspective-integration",
        notes="early",
        path=path,
    )
    annotate_episode(
        start_ts=500.0,
        end_ts=600.0,
        episode_type="perspective-integration",
        notes="late",
        path=path,
    )

    results = query_episodes(after_ts=400.0, path=path)
    assert len(results) == 1
    assert results[0]["notes"] == "late"


def test_query_before_ts(tmp_path):
    """Episodes can be filtered with before_ts."""
    from scripts.chi_episode_annotate import annotate_episode, query_episodes

    path = tmp_path / "chi-episodes.jsonl"
    annotate_episode(
        start_ts=100.0,
        end_ts=200.0,
        episode_type="perspective-integration",
        notes="early",
        path=path,
    )
    annotate_episode(
        start_ts=500.0,
        end_ts=600.0,
        episode_type="perspective-integration",
        notes="late",
        path=path,
    )

    results = query_episodes(before_ts=300.0, path=path)
    assert len(results) == 1
    assert results[0]["notes"] == "early"


def test_query_by_keyword(tmp_path):
    """Episodes can be filtered by keyword in notes."""
    from scripts.chi_episode_annotate import annotate_episode, query_episodes

    path = tmp_path / "chi-episodes.jsonl"
    annotate_episode(
        start_ts=1.0,
        end_ts=2.0,
        episode_type="perspective-integration",
        notes="density field convergence observed",
        path=path,
    )
    annotate_episode(
        start_ts=3.0,
        end_ts=4.0,
        episode_type="perspective-integration",
        notes="voice grounding episode",
        path=path,
    )

    results = query_episodes(keyword="density", path=path)
    assert len(results) == 1
    assert "density" in results[0]["notes"]


def test_annotate_validates_episode_type(tmp_path):
    """Invalid episode types are rejected."""
    import pytest

    from scripts.chi_episode_annotate import annotate_episode

    path = tmp_path / "chi-episodes.jsonl"
    with pytest.raises(ValueError, match="Invalid episode_type"):
        annotate_episode(
            start_ts=1.0, end_ts=2.0, episode_type="invalid-type", notes="x", path=path
        )


def test_annotate_default_evidence_refs(tmp_path):
    """evidence_refs defaults to empty list."""
    from scripts.chi_episode_annotate import annotate_episode, query_episodes

    path = tmp_path / "chi-episodes.jsonl"
    annotate_episode(
        start_ts=1.0, end_ts=2.0, episode_type="spontaneous-expression", notes="x", path=path
    )
    episodes = query_episodes(path=path)
    assert episodes[0]["evidence_refs"] == []


def test_query_empty_file(tmp_path):
    """Querying a non-existent file returns empty list."""
    from scripts.chi_episode_annotate import query_episodes

    path = tmp_path / "chi-episodes.jsonl"
    results = query_episodes(path=path)
    assert results == []
