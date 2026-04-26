"""Tests for ``sdlc.render.repo_settings``.

Tests the policy logic + registry traversal. Network calls into ``gh``
are mocked — the live drift-correction path is exercised by the
operator-side enforce script and a future CI drift-check workflow.
"""

from __future__ import annotations

from unittest.mock import patch

from sdlc.render.repo_registry import LicenseClass, RepoSpec
from sdlc.render.repo_settings import (
    DriftReport,
    RepoSettings,
    WIKI_REPURPOSED,
    desired_settings,
    detect_drift,
    first_party_repos,
)


def _stub_repo(name: str, *, is_first_party: bool = True) -> RepoSpec:
    return RepoSpec(
        id=name,
        name=name,
        description="stub",
        repo_type="library",
        role_in_constellation="stub",
        license_class=LicenseClass.MIT,
        is_first_party=is_first_party,
    )


def test_wiki_repurposed_set_is_constitution_only() -> None:
    """Only hapax-constitution keeps its wiki — for the axiom registry."""
    assert WIKI_REPURPOSED == frozenset({"hapax-constitution"})


def test_desired_settings_for_constitution_keeps_wiki() -> None:
    settings = desired_settings(_stub_repo("hapax-constitution"))
    assert settings == RepoSettings(
        has_wiki=True, has_projects=False, has_discussions=False
    )


def test_desired_settings_for_other_repos_disables_wiki() -> None:
    for name in ("hapax-council", "hapax-mcp", "hapax-phone"):
        settings = desired_settings(_stub_repo(name))
        assert settings == RepoSettings(
            has_wiki=False, has_projects=False, has_discussions=False
        )


def test_first_party_repos_excludes_upstream_forks() -> None:
    repos = first_party_repos()
    assert all(r.is_first_party for r in repos)
    assert "tabbyAPI" not in {r.name for r in repos}
    assert "atlas-voice-training" not in {r.name for r in repos}


def test_first_party_repos_count_matches_registry_invariant() -> None:
    """The constellation has 7 first-party repos (per test_render.py
    ``test_registry_has_seven_first_party_repos``). The enforcer governs
    all of them."""
    assert len(first_party_repos()) == 7


def test_detect_drift_reports_per_repo_when_observed_matches() -> None:
    repos = [_stub_repo("hapax-council"), _stub_repo("hapax-constitution")]
    desired_council = desired_settings(repos[0])
    desired_constitution = desired_settings(repos[1])

    def fake_current(_owner: str, name: str) -> RepoSettings:
        return desired_council if name == "hapax-council" else desired_constitution

    with patch("sdlc.render.repo_settings.current_settings", side_effect=fake_current):
        reports = detect_drift("ryanklee", repos)

    assert all(isinstance(r, DriftReport) for r in reports)
    assert all(not r.has_drift for r in reports)


def test_detect_drift_reports_drift_when_observed_differs() -> None:
    repo = _stub_repo("hapax-council")
    bad_observed = RepoSettings(has_wiki=True, has_projects=True, has_discussions=True)

    with patch("sdlc.render.repo_settings.current_settings", return_value=bad_observed):
        reports = detect_drift("ryanklee", [repo])

    assert len(reports) == 1
    assert reports[0].has_drift
    assert reports[0].desired == RepoSettings(False, False, False)
    assert reports[0].observed == bad_observed


def test_repo_settings_is_hashable_for_set_dedup() -> None:
    """Frozen dataclass invariant — used in dedup paths if the enforcer
    ever batches repos by desired-settings shape."""
    a = RepoSettings(has_wiki=False, has_projects=False, has_discussions=False)
    b = RepoSettings(has_wiki=False, has_projects=False, has_discussions=False)
    assert hash(a) == hash(b)
    assert {a, b} == {a}
