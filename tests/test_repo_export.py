"""Tests for the canonical repo-presentation export."""

from __future__ import annotations

import json

from sdlc.render.repo_export import GENERATED_ARTIFACTS, build_export


def test_repo_export_is_json_serializable() -> None:
    export = build_export()
    encoded = json.dumps(export, sort_keys=True)
    assert '"schema_version": 1' in encoded


def test_repo_export_includes_generated_artifacts_and_settings_policy() -> None:
    export = build_export()
    assert export["generated_artifacts"] == list(GENERATED_ARTIFACTS)
    assert "SUPPORT.md" in export["generated_artifacts"]
    assert ".github/ISSUE_TEMPLATE/config.yml" in export["generated_artifacts"]
    assert export["settings_policy"] == {
        "issues": "redirect",
        "wiki": "disabled_except_hapax_constitution",
        "projects": "disabled",
        "discussions": "disabled",
        "funding": "no_perk_research_support_only",
    }


def test_repo_export_orders_repos_by_derived_dependency_order() -> None:
    export = build_export()
    by_id = {repo["id"]: repo for repo in export["repos"]}
    assert by_id["hapax-constitution"]["dependency_order"] == 0
    assert (
        by_id["hapax-council"]["dependency_order"]
        > (by_id["hapax-constitution"]["dependency_order"])
    )
    assert by_id["hapax-spine"]["dependency_order"] > (by_id["hapax-council"]["dependency_order"])
    assert by_id["reins"]["dependency_order"] > by_id["hapax-spine"]["dependency_order"]


def test_repo_export_carries_frontmatter_policy_fields() -> None:
    export = build_export()
    by_id = {repo["id"]: repo for repo in export["repos"]}
    agentgov = by_id["agentgov"]
    assert agentgov["surface_class"] == "adoption_commons"
    assert agentgov["support_posture"] == "bounded_adoption_redirect"
    assert agentgov["github_settings"] == {
        "has_issues": True,
        "has_wiki": False,
        "has_projects": False,
        "has_discussions": False,
    }

    constitution = by_id["hapax-constitution"]
    assert constitution["github_settings"]["has_wiki"] is True
    assert "SUPPORT.md" in constitution["public_files"]


def test_repo_export_marks_upstream_forks_inert() -> None:
    export = build_export()
    by_id = {repo["id"]: repo for repo in export["repos"]}
    tabby = by_id["tabbyAPI"]
    assert tabby["is_first_party"] is False
    assert tabby["support_posture"] == "upstream_preserved"
    assert tabby["generated_artifacts"] == []
    assert tabby["github_settings"] is None
