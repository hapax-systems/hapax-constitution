"""Tests for ``sdlc.render`` (published as ``hapax_sdlc.render``).

Per workspace conventions: ``unittest.mock`` only, file is self-contained,
no shared conftest fixtures.
"""

from __future__ import annotations

import io
import json
import os
import subprocess
import sys
from contextlib import redirect_stdout
from dataclasses import replace
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from sdlc.render import (
    citation_cff,
    cli,
    codemeta_json,
    contributing_md,
    governance_md,
    issue_template_config_yml,
    notice_md,
    org_profile_readme,
    readme_section,
    security_md,
    support_md,
    zenodo_json,
)
from sdlc.render.operator_referent import REFERENTS, OperatorReferentPicker
from sdlc.render.repo_registry import (
    LicenseClass,
    OperatorIdentity,
    RepoSpec,
    RepoVisibility,
    SourceOfTruth,
    SurfaceClass,
    ValuePartition,
    load_operator_identity,
    load_registry,
)


# --- Registry --------------------------------------------------------------


def test_registry_has_current_first_party_repos() -> None:
    registry = load_registry()
    first_party = [s for s in registry.values() if s.is_first_party]
    assert len(first_party) == 12
    ids = sorted(s.id for s in first_party)
    assert ids == [
        "agentgov",
        "hapax-assets",
        "hapax-constitution",
        "hapax-coord",
        "hapax-council",
        "hapax-mcp",
        "hapax-officium",
        "hapax-phone",
        "hapax-research-ledger",
        "hapax-spine",
        "hapax-watch",
        "reins",
    ]


def test_registry_includes_two_upstream_forks() -> None:
    registry = load_registry()
    forks = [s for s in registry.values() if not s.is_first_party]
    assert len(forks) == 2
    assert {s.id for s in forks} == {"tabbyAPI", "atlas-voice-training"}
    for f in forks:
        assert f.license_class is LicenseClass.UPSTREAM


def test_registry_license_assignments_match_research_drop() -> None:
    """Drop 4 §3 license matrix:
    - Runtime: PolyForm Strict 1.0.0 (council, officium, watch, phone)
    - MCP: MIT (per-operator divergence; MCP ecosystem norm)
    - Spec/docs: CC BY-NC-ND 4.0 (constitution)
    - Aesthetic library blend: CC BY-SA 4.0 (assets)
    """
    registry = load_registry()
    assert registry["hapax-council"].license_class is LicenseClass.POLYFORM_STRICT_1_0_0
    assert registry["hapax-officium"].license_class is LicenseClass.POLYFORM_STRICT_1_0_0
    assert registry["hapax-watch"].license_class is LicenseClass.POLYFORM_STRICT_1_0_0
    assert registry["hapax-phone"].license_class is LicenseClass.POLYFORM_STRICT_1_0_0
    assert registry["hapax-constitution"].license_class is LicenseClass.CC_BY_NC_ND_4_0
    assert registry["hapax-mcp"].license_class is LicenseClass.MIT
    assert registry["hapax-assets"].license_class is LicenseClass.CC_BY_SA_4_0
    assert registry["agentgov"].license_class is LicenseClass.MIT
    assert registry["reins"].license_class is LicenseClass.BUSL_1_1
    assert registry["hapax-spine"].license_class is LicenseClass.BUSL_1_1
    assert registry["hapax-coord"].license_class is LicenseClass.POLYFORM_STRICT_1_0_0
    assert registry["hapax-research-ledger"].license_class is LicenseClass.CC0_1_0


def test_registry_value_partitions_match_ratified_license_posture() -> None:
    registry = load_registry()
    assert registry["agentgov"].value_partition is ValuePartition.EVIDENCE_ARTIFACT
    assert registry["agentgov"].license_posture.startswith(
        "Archived historical MIT-licensed source"
    )
    assert "must not imply broader Hapax runtime rights or support obligations" in (
        registry["agentgov"].license_posture
    )

    for repo_id in ("reins", "hapax-spine"):
        repo = registry[repo_id]
        assert repo.value_partition is ValuePartition.COMMERCIAL_MOAT
        assert "not open source" in repo.license_posture.lower()

    for repo_id in ("hapax-council", "hapax-coord", "hapax-phone", "hapax-watch"):
        assert registry[repo_id].value_partition is ValuePartition.INTERNAL_APPARATUS

    for repo_id in ("hapax-constitution", "hapax-assets", "hapax-research-ledger"):
        assert registry[repo_id].value_partition is ValuePartition.EVIDENCE_ARTIFACT


def test_registry_frontmatter_policy_fields_are_populated() -> None:
    registry = load_registry()
    for repo in registry.values():
        assert repo.reader_promise
        assert repo.reader_value
        assert repo.claim_ceiling
        assert repo.primary_audience
        assert isinstance(repo.source_of_truth, SourceOfTruth)
        assert isinstance(repo.surface_class, SurfaceClass)
        assert isinstance(repo.visibility, RepoVisibility)
        if repo.is_first_party:
            assert repo.public_files


def test_registry_surface_classes_match_portfolio_decisions() -> None:
    registry = load_registry()
    assert registry["agentgov"].surface_class is SurfaceClass.EVIDENCE_ARTIFACT
    assert registry["reins"].surface_class is SurfaceClass.PRODUCT_FRONT_DOOR
    assert registry["hapax-spine"].surface_class is SurfaceClass.RUNTIME_MECHANISM
    assert registry["hapax-council"].surface_class is SurfaceClass.RESEARCH_APPARATUS
    assert registry["hapax-constitution"].surface_class is SurfaceClass.GOVERNANCE_SPEC
    assert registry["hapax-mcp"].surface_class is SurfaceClass.ECOSYSTEM_BRIDGE
    assert registry["hapax-assets"].surface_class is SurfaceClass.ASSET_MIRROR
    assert registry["hapax-research-ledger"].surface_class is SurfaceClass.EVIDENCE_ARTIFACT


def test_registry_visibility_matches_current_public_boundary() -> None:
    registry = load_registry()
    public = {repo.id for repo in registry.values() if repo.visibility is RepoVisibility.PUBLIC}
    assert public == {
        "agentgov",
        "hapax-assets",
        "hapax-constitution",
        "hapax-council",
        "hapax-mcp",
        "hapax-officium",
        "hapax-phone",
        "hapax-research-ledger",
        "hapax-spine",
        "hapax-watch",
        "reins",
    }


def test_registry_dependency_order_is_derived_from_dependencies() -> None:
    registry = load_registry()
    assert registry["hapax-constitution"].dependency_order == 0
    assert registry["agentgov"].dependency_order == 0
    assert registry["hapax-council"].dependency_order > (
        registry["hapax-constitution"].dependency_order
    )
    assert registry["hapax-spine"].dependency_order > registry["hapax-council"].dependency_order
    assert registry["reins"].dependency_order > registry["hapax-spine"].dependency_order


def test_registry_rejects_hand_authored_dependency_order(tmp_path: Path) -> None:
    registry_path = tmp_path / "repos.yaml"
    registry_path.write_text(
        yaml.safe_dump(
            {
                "repos": {
                    "demo": {
                        "name": "demo",
                        "description": "demo",
                        "repo_type": "library",
                        "role_in_constellation": "demo",
                        "license_class": "MIT",
                        "value_partition": "adoption_commons",
                        "license_posture": "demo",
                        "dependency_order": 99,
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="dependency_order is derived"):
        load_registry(registry_path)


def test_registry_first_party_repos_default_to_hapax_systems_owner() -> None:
    registry = load_registry()
    first_party = [s for s in registry.values() if s.is_first_party]
    assert all(s.github_owner == "hapax-systems" for s in first_party)
    assert registry["hapax-council"].github_url == (
        "https://github.com/hapax-systems/hapax-council"
    )


def test_load_operator_identity_returns_placeholder_when_no_local_override(
    tmp_path: Path,
) -> None:
    bogus = tmp_path / "missing.yaml"
    bogus_local = tmp_path / "missing.local.yaml"
    identity = load_operator_identity(bogus, bogus_local)
    assert identity.full_name == "<operator-name-unset>"
    assert identity.orcid is None


def test_load_operator_identity_prefers_local_override(
    tmp_path: Path,
) -> None:
    canonical = tmp_path / "operator.yaml"
    canonical.write_text(yaml.safe_dump({"full_name": "From Canonical"}), encoding="utf-8")
    local = tmp_path / "operator.local.yaml"
    local.write_text(
        yaml.safe_dump(
            {
                "full_name": "From Local",
                "orcid": "https://orcid.org/0000-0000-0000-0001",
                "contact_url": "https://hapax.weblog.lol/disclosure",
            }
        ),
        encoding="utf-8",
    )
    identity = load_operator_identity(canonical, local)
    assert identity.full_name == "From Local"
    assert identity.orcid == "https://orcid.org/0000-0000-0000-0001"


# --- Operator referent ------------------------------------------------------


def test_operator_referent_is_sticky_per_repo() -> None:
    a1 = OperatorReferentPicker.pick_for_artifact("hapax-council")
    a2 = OperatorReferentPicker.pick_for_artifact("hapax-council")
    assert a1 == a2  # sticky-per-repo
    assert a1 in REFERENTS


def test_operator_referent_differs_across_seeds() -> None:
    """At least one pair across seven repos must differ; otherwise the
    picker is broken (all four referents should be reachable).
    """
    repo_ids = [
        "hapax-council",
        "hapax-officium",
        "hapax-mcp",
        "hapax-watch",
        "hapax-phone",
        "hapax-constitution",
        "hapax-assets",
    ]
    picks = {OperatorReferentPicker.pick_for_artifact(r) for r in repo_ids}
    assert len(picks) >= 2


# --- Renderer outputs -------------------------------------------------------


@pytest.fixture
def identity() -> OperatorIdentity:
    # Use a unique synthetic name that cannot collide with any of the
    # four ratified non-formal referents ("The Operator", "Oudepode",
    # "Oudepode The Operator", "OTO").
    return OperatorIdentity(
        full_name="Quentin Zarbacaster",
        orcid="https://orcid.org/0000-0000-0000-0001",
        contact_url="https://hapax.weblog.lol/disclosure",
    )


@pytest.fixture
def council_repo() -> RepoSpec:
    return load_registry()["hapax-council"]


@pytest.fixture
def constitution_repo() -> RepoSpec:
    return load_registry()["hapax-constitution"]


def test_citation_cff_yaml_parses_and_carries_required_fields(
    council_repo: RepoSpec, identity: OperatorIdentity
) -> None:
    body = citation_cff.render(council_repo, identity)
    parsed = yaml.safe_load(body)
    assert parsed["cff-version"] == "1.2.0"
    assert parsed["title"] == "hapax-council"
    assert parsed["type"] == "software"
    assert parsed["authors"][0]["name"] == "Hapax Systems"
    assert "family-names" not in parsed["authors"][0]
    assert "orcid" not in parsed["authors"][0]
    assert parsed["doi"] == "10.5281/zenodo.20113515"
    assert parsed["license"] == "PolyForm-Strict-1.0.0"
    assert "research-software" in parsed["keywords"]


def test_codemeta_json_parses_and_aligns_to_v3_jsonld(
    council_repo: RepoSpec, identity: OperatorIdentity
) -> None:
    body = codemeta_json.render(council_repo, identity)
    parsed = json.loads(body)
    assert parsed["@context"] == "https://w3id.org/codemeta/3.0"
    assert parsed["@type"] == "SoftwareSourceCode"
    assert parsed["author"][0]["@type"] == "Organization"
    assert parsed["author"][0]["name"] == "Hapax Systems"
    assert parsed["author"][0]["url"] == "https://github.com/hapax-systems"
    assert "@id" not in parsed["author"][0]
    assert parsed["identifier"] == "https://doi.org/10.5281/zenodo.20113515"
    assert parsed["license"] == ("https://polyformproject.org/licenses/strict/1.0.0/")
    assert parsed["codeRepository"] == "https://github.com/hapax-systems/hapax-council"


def test_zenodo_json_carries_related_identifier_graph(
    council_repo: RepoSpec, identity: OperatorIdentity
) -> None:
    body = zenodo_json.render(council_repo, identity)
    parsed = json.loads(body)
    assert parsed["upload_type"] == "software"
    assert parsed["access_right"] == "open"
    assert parsed["creators"][0]["name"] == "Hapax Systems"
    assert "orcid" not in parsed["creators"][0]
    assert parsed["doi"] == "10.5281/zenodo.20113515"
    assert parsed["conceptdoi"] == "10.5281/zenodo.20113514"
    assert parsed["license"] == "other-closed"
    assert "PolyForm Strict" in parsed["notes"]
    related = parsed["related_identifiers"]
    assert any(
        ri["identifier"].endswith("hapax-constitution") and ri["relation"] == "isPartOf"
        for ri in related
    )


def test_zenodo_json_constitution_uses_publication_upload_type(
    constitution_repo: RepoSpec, identity: OperatorIdentity
) -> None:
    body = zenodo_json.render(constitution_repo, identity)
    parsed = json.loads(body)
    assert parsed["upload_type"] == "publication"
    assert parsed["publication_type"] == "other"


def test_notice_md_uses_referent_not_legal_name(
    council_repo: RepoSpec, identity: OperatorIdentity
) -> None:
    body = notice_md.render(council_repo)
    assert identity.full_name not in body  # legal name banned in body
    assert "Reader promise" in body
    assert "Reader value" in body
    assert "Claim ceiling" in body
    assert "License and rights" in body
    assert "hapax-systems" in body
    assert "hapax-manifesto-v0" not in body
    assert "https://github.com/hapax-systems/hapax-constitution" in body


def test_contributing_md_refuses_explicitly(council_repo: RepoSpec) -> None:
    body = contributing_md.render(council_repo)
    assert "does not accept contributions" in body
    assert "single_user" in body
    assert "Refusal Brief" in body


def test_security_md_publishes_sigstore_path_not_email(
    council_repo: RepoSpec, identity: OperatorIdentity
) -> None:
    body = security_md.render(council_repo, identity)
    assert identity.contact_url in body
    assert "Sigstore" in body
    # No email pattern (rough heuristic — no '@example' or similar)
    assert "@" not in body or "@type" in body  # JSON-LD @type is fine


def test_security_md_keeps_critical_disclosures_out_of_band(
    council_repo: RepoSpec, identity: OperatorIdentity
) -> None:
    body = security_md.render(council_repo, identity)
    assert "no SLA" in body
    assert "triaged out of band" in body
    # Regression pin: critical disclosures must never be deferred to a
    # maintenance window on a public security policy.
    assert "next maintenance window handles critical" not in body
    # No freshness-rotting advisory claims ("None to date" class).
    assert "None to date" not in body


def test_security_and_contributing_do_not_publish_operator_referent(
    council_repo: RepoSpec, identity: OperatorIdentity
) -> None:
    for body in (
        security_md.render(council_repo, identity),
        contributing_md.render(council_repo),
    ):
        for referent in ("Oudepode", "OTO", "The Operator"):
            assert referent not in body


def test_support_md_redirects_without_support_entitlement() -> None:
    registry = load_registry()
    body = support_md.render(registry["agentgov"])
    assert "research or boundary artifact" in body
    assert "not as a staffed support surface" in body
    assert "Blank issues are disabled" in body
    assert "no-perk research support only" in body
    assert "does not create an SLA" in body


def test_product_and_archived_preambles_follow_current_surface_classes() -> None:
    registry = load_registry()

    reins_body = readme_section.render(registry["reins"])
    assert "product front door" in reins_body
    assert "governed command preview" in reins_body
    assert "Reader promise" in reins_body
    assert "Reader value" in reins_body
    assert "Claim ceiling" in reins_body
    assert "License and rights" in reins_body
    assert "autonomous write authority" in reins_body
    assert "not a product" not in reins_body
    assert "research infrastructure published as artifact" not in reins_body
    assert "Authorship is indeterminate" not in reins_body
    assert "hapax-manifesto-v0" not in reins_body

    agentgov_body = readme_section.render(registry["agentgov"])
    assert "evidence-artifact repository" in agentgov_body
    assert "governance-hook source" in agentgov_body
    assert "Archived historical MIT-licensed source" in agentgov_body
    assert "not a product" not in agentgov_body
    assert "research infrastructure published as artifact" not in agentgov_body


def test_asset_mirror_preamble_uses_per_asset_authority_surfaces() -> None:
    registry = load_registry()
    body = readme_section.render(registry["hapax-assets"])

    assert "See `LICENSE`" not in body
    assert "`NOTICE.md`, `_NOTICES.md`, and `_manifest.yaml`" in body
    assert "licenses remain per-asset" in body


def test_notice_and_contributing_follow_surface_class_boundaries() -> None:
    registry = load_registry()

    reins_notice = notice_md.render(registry["reins"])
    assert "product front door" in reins_notice
    assert "read and command-preview claim ceiling" in reins_notice
    assert "not a product" not in reins_notice

    agentgov_contributing = contributing_md.render(registry["agentgov"])
    assert "not a staffed product, service, or community library" in agentgov_contributing
    assert "community maintenance" in agentgov_contributing
    assert "not a product" not in agentgov_contributing


def test_org_profile_readme_orients_public_portfolio_without_private_repo_table() -> None:
    body = org_profile_readme.render(load_registry())
    assert body.startswith("# Hapax Systems")
    assert "public research program of Hapax Systems" in body
    for repo_id in (
        "hapax-mcp",
        "reins",
        "hapax-spine",
        "hapax-council",
        "hapax-constitution",
        "hapax-research-ledger",
        "hapax-officium",
        "hapax-phone",
        "hapax-watch",
        "hapax-assets",
        "agentgov",
    ):
        assert f"[{repo_id}](https://github.com/hapax-systems/{repo_id})" in body
    assert "hapax-coord](https://github.com/hapax-systems/hapax-coord)" not in body
    assert "| [agentgov]" not in body
    assert "**archived historical\nrepository**" in body
    assert "not the current adoption entry point" in body
    assert "releases/tag/v0.1.1" in body
    assert "profile source" in body
    assert "Corrections should identify" in body


def test_org_profile_readme_pins_claim_ceiling_and_license_boundaries() -> None:
    body = org_profile_readme.render(load_registry())
    assert "private during restructure" not in body
    assert "describe measured capability" not in body
    assert "Hapax is open source" not in body
    assert "generic agent OS" not in body
    assert "guaranteed safe" not in body
    assert "The license in each repository defines its terms" in body
    assert "Split by path: CC BY-NC-ND 4.0 / Apache-2.0" in body
    assert "per-asset notices take precedence" in body
    assert "Business Source License 1.1" in body
    assert "PolyForm Strict 1.0.0" in body
    assert "Source availability does not" in body
    assert "not a claim of an established prospective scoring record" in body
    assert "numeric research ledger is not a prediction register" in body
    assert "These are separate dimensions" in body
    assert "Original predictions and timestamped amendments" in body
    assert "late or omitted outcomes" in body
    assert "registry-asserted today; measured calibration is planned" not in body


@pytest.mark.parametrize("renderer", [support_md, contributing_md, readme_section, notice_md])
def test_archived_agentgov_consumers_do_not_invite_adoption(renderer) -> None:
    body = renderer.render(load_registry()["agentgov"])
    for invitation in (
        "bounded adoption surface",
        "bounded adoption-commons repository",
        "Permissive adoption surface",
        "inspect and pilot",
        "pilot use",
        "evaluate the adoption surface",
    ):
        assert invitation not in body


def test_org_profile_matches_committed_bytes_and_full_hash(tmp_path: Path) -> None:
    # This reviewed artifact is also the candidate for hapax-systems/.github#7.
    # Update the fixture and digest only alongside a reviewed consumer update.
    expected = (Path(__file__).parent / "fixtures" / "org-profile-README.md").read_bytes()
    assert sha256(expected).hexdigest() == (
        "899abd054d37be681894f88f2237d675b569987817d43b95e919818fad24009f"
    )
    assert org_profile_readme.render(load_registry()).encode("utf-8") == expected
    assert cli.main(["--org-profile", "--target-root", str(tmp_path)]) == 0
    assert (tmp_path / "profile" / "README.md").read_bytes() == expected
    assert cli.main(["--org-profile", "--check", "--target-root", str(tmp_path)]) == 0


@pytest.mark.parametrize(
    "repo_id",
    [
        "hapax-mcp",
        "reins",
        "hapax-spine",
        "hapax-council",
        "hapax-constitution",
        "hapax-research-ledger",
        "hapax-officium",
        "hapax-phone",
        "hapax-watch",
        "hapax-assets",
        "agentgov",
    ],
)
@pytest.mark.parametrize(
    "invalid_state", ["missing", "private", "local_only", "third_party", "outside_owner"]
)
def test_org_profile_rejects_ineligible_required_entries(repo_id: str, invalid_state: str) -> None:
    registry = load_registry()
    if invalid_state == "missing":
        del registry[repo_id]
        reason = "missing"
    elif invalid_state == "third_party":
        registry[repo_id] = replace(registry[repo_id], is_first_party=False)
        reason = "not first-party"
    elif invalid_state == "outside_owner":
        registry[repo_id] = replace(registry[repo_id], github_owner="unapproved-owner")
        assert registry[repo_id].is_first_party
        reason = "github_owner=unapproved-owner; expected hapax-systems"
    else:
        registry[repo_id] = replace(registry[repo_id], visibility=RepoVisibility(invalid_state))
        reason = invalid_state
    with pytest.raises(ValueError) as error:
        org_profile_readme.render(registry)
    message = str(error.value)
    assert repo_id in message
    assert reason in message
    assert "sdlc/render/repos.yaml" in message
    assert "Verify the approved public first-party inventory" in message
    assert "before rerendering" in message
    assert "visibility or ownership changes require separate authority" in message


def test_constitution_readme_describes_agentgov_as_archived_evidence() -> None:
    body = (Path(__file__).resolve().parents[1] / "README.md").read_text(encoding="utf-8")
    related = body.split("## Related Repositories\n", 1)[1]
    entry = next(line for line in related.splitlines() if line.startswith("- [agentgov]"))
    assert "https://github.com/hapax-systems/agentgov" in entry
    assert "archived historical governance-hook source" in entry
    assert "inspection and citation" in entry
    assert "not the current adoption entry point" in entry
    assert "MIT adoption commons" not in body
    assert "portable governance hooks" not in entry


def test_org_profile_ignores_ineligible_entries_outside_required_portfolio() -> None:
    registry = load_registry()
    expected = org_profile_readme.render(registry)
    for repo_id in ("hapax-coord", "tabbyAPI", "atlas-voice-training"):
        del registry[repo_id]
    assert org_profile_readme.render(registry) == expected


@pytest.mark.parametrize(
    ("repo_id", "label", "path"),
    [
        ("hapax-mcp", "MIT", "LICENSE"),
        ("reins", "Business Source License 1.1", "LICENSE"),
        ("hapax-spine", "Business Source License 1.1", "LICENSE"),
        ("hapax-council", "PolyForm Strict 1.0.0", "LICENSE"),
        ("hapax-constitution", "Split by path: CC BY-NC-ND 4.0 / Apache-2.0", "LICENSE"),
        ("hapax-research-ledger", "CC0-1.0 for the declared data surface", "LICENSE"),
        ("hapax-officium", "PolyForm Strict 1.0.0", "LICENSE"),
        ("hapax-phone", "PolyForm Strict 1.0.0", "LICENSE"),
        ("hapax-watch", "PolyForm Strict 1.0.0", "LICENSE"),
        (
            "hapax-assets",
            "CC BY 4.0 default; per-asset notices take precedence",
            "LICENSE-SCOPE.md",
        ),
    ],
)
def test_org_profile_license_links_use_existing_repository_authority(
    repo_id: str, label: str, path: str
) -> None:
    body = org_profile_readme.render(load_registry())
    row = next(line for line in body.splitlines() if line.startswith(f"| [{repo_id}]"))
    assert f"[{label}](https://github.com/hapax-systems/{repo_id}/blob/main/{path})" in row


def test_issue_template_config_yml_disables_blank_issues(council_repo: RepoSpec) -> None:
    body = issue_template_config_yml.render(council_repo)
    parsed = yaml.safe_load(body)
    assert parsed["blank_issues_enabled"] is False
    contact_links = parsed["contact_links"]
    assert {link["name"] for link in contact_links} == {
        "Read the repository overview",
        "Read the support boundary",
        "Read the security disclosure path",
        "Read Hapax governance",
    }
    assert all({"name", "url", "about"} == set(link) for link in contact_links)
    assert (
        parsed["contact_links"][1]["url"]
        == "https://github.com/hapax-systems/hapax-council/blob/main/SUPPORT.md"
    )


def test_governance_md_anchor_vs_redirect(
    council_repo: RepoSpec, constitution_repo: RepoSpec
) -> None:
    anchor_body = governance_md.render(constitution_repo)
    redirect_body = governance_md.render(council_repo)
    assert "canonical axiom registry" in anchor_body
    assert "`hapax-constitution` governs this repository" in redirect_body
    assert "https://github.com/hapax-systems/hapax-constitution" in redirect_body


def test_readme_section_replacement_preserves_existing_body(
    council_repo: RepoSpec,
) -> None:
    preamble = readme_section.render(council_repo)
    existing = (
        f"{readme_section.PREAMBLE_BEGIN}\n# OLD PREAMBLE\n{readme_section.PREAMBLE_END}\n"
        "\n## Architecture\n\nDetailed body content that must survive.\n"
    )
    rendered = readme_section.replace_section(existing, preamble)
    assert "# OLD PREAMBLE" not in rendered
    assert "## Architecture" in rendered
    assert "Detailed body content that must survive." in rendered
    assert preamble in rendered


def test_readme_section_prepends_when_no_markers_present(
    council_repo: RepoSpec,
) -> None:
    preamble = readme_section.render(council_repo)
    existing = "## Body without markers\n\nPre-existing content.\n"
    rendered = readme_section.replace_section(existing, preamble)
    assert rendered.startswith(readme_section.PREAMBLE_BEGIN)
    assert "## Body without markers" in rendered


def test_readme_section_coemits_public_surface_markers(
    council_repo: RepoSpec,
) -> None:
    """D4 marker convergence: the claim-bearing hapax-public family is
    co-emitted INSIDE the hapax-sdlc replacement anchors."""
    preamble = readme_section.render(council_repo)
    public_begin, public_end = readme_section.public_surface_marker_pair(council_repo.name)
    assert "hapax-public:surface=github.repo.hapax-council.readme.preamble" in public_begin
    lines = preamble.splitlines()
    assert lines[0] == readme_section.PREAMBLE_BEGIN
    assert lines[1] == public_begin
    assert lines[-2] == public_end
    assert lines[-1] == readme_section.PREAMBLE_END
    # Replacement still keys on the OLD family only: replacing a legacy
    # preamble (no inner markers) must succeed and produce the new region.
    legacy = f"{readme_section.PREAMBLE_BEGIN}\n# OLD\n{readme_section.PREAMBLE_END}\n\n## Body\n"
    rendered = readme_section.replace_section(legacy, preamble)
    assert public_begin in rendered
    assert rendered.count(readme_section.PREAMBLE_BEGIN) == 1
    assert "## Body" in rendered


# --- CLI -------------------------------------------------------------------


def test_cli_dry_run_prints_all_artifacts() -> None:
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = cli.main(["--repo", "hapax-council", "--dry-run"])
    output = buf.getvalue()
    assert rc == 0
    for filename in (
        "CITATION.cff",
        "codemeta.json",
        ".zenodo.json",
        "NOTICE.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "SUPPORT.md",
        "GOVERNANCE.md",
        ".github/ISSUE_TEMPLATE/config.yml",
        "README.md",
    ):
        assert f"# {filename}" in output


def test_cli_dry_run_prints_org_profile() -> None:
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = cli.main(["--org-profile", "--dry-run"])
    output = buf.getvalue()
    assert rc == 0
    assert "# profile/README.md" in output
    assert "# Hapax Systems" in output
    assert "https://github.com/hapax-systems/reins" in output


def test_cli_org_profile_write_creates_nested_profile_readme(tmp_path: Path) -> None:
    rc = cli.main(["--org-profile", "--target-root", str(tmp_path)])
    assert rc == 0
    written = tmp_path / "profile" / "README.md"
    assert written.exists()
    assert written.read_text(encoding="utf-8").startswith("# Hapax Systems")


def test_cli_unknown_repo_errors() -> None:
    with pytest.raises(SystemExit):
        cli.main(["--repo", "no-such-repo"])


def test_cli_check_mode_detects_drift(tmp_path: Path) -> None:
    """--check against an empty target dir reports drift on every artifact."""
    rc = cli.main(
        [
            "--repo",
            "hapax-council",
            "--check",
            "--target-root",
            str(tmp_path),
        ]
    )
    assert rc == 1  # every rendered file drifted


@pytest.mark.parametrize(
    ("target_args", "filename"),
    [
        (["--org-profile"], "profile/README.md"),
        (["--repo", "hapax-council", "--file", "SUPPORT.md"], "SUPPORT.md"),
        (["--all", "--file", "SUPPORT.md"], "SUPPORT.md"),
    ],
)
@pytest.mark.parametrize("existing_consumer", [False, True], ids=["missing", "changed"])
def test_cli_check_drift_is_actionable_and_preserves_consumers(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    target_args: list[str],
    filename: str,
    existing_consumer: bool,
) -> None:
    target_root = tmp_path / "consumer checkout"
    target_root.mkdir()
    target = (
        target_root / "hapax-council" / filename
        if "--all" in target_args
        else target_root / filename
    )
    if existing_consumer:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"Existing consumer content that requires reconciliation.\n")
    (target_root / "unrelated.txt").write_bytes(b"Preserve this consumer file too.\n")

    def snapshot() -> dict[str, tuple[bytes, int, int]]:
        return {
            str(path.relative_to(target_root)): (
                path.read_bytes(),
                path.stat().st_mode,
                path.stat().st_mtime_ns,
            )
            for path in target_root.rglob("*")
            if path.is_file()
        }

    before = snapshot()
    args = list(target_args)
    if "--all" not in args:
        args.extend(["--target-root", str(target_root)])
    with patch.object(cli, "default_target_root", side_effect=lambda repo: target_root / repo.name):
        rc = cli.main([*args, "--check"])
    output = capsys.readouterr()

    assert rc == 1
    assert snapshot() == before
    assert output.out == ""
    assert f"DRIFT {target}" in output.err
    assert "check failed:" in output.err
    assert "Next action:" in output.err
    assert "sdlc/render/repos.yaml" in output.err
    assert "renderer in sdlc/render/" in output.err
    assert "Reconcile" in output.err
    assert "same target/file options without --check" in output.err
    assert "review the generated diff" in output.err
    assert "then rerun --check" in output.err
    with patch.object(cli, "default_target_root", side_effect=lambda repo: target_root / repo.name):
        assert cli.main(args) == 0
        assert cli.main([*args, "--check"]) == 0


def test_cli_check_mode_clean_after_write(tmp_path: Path) -> None:
    """Write then re-check — should report zero drift."""
    rc_write = cli.main(
        [
            "--repo",
            "hapax-council",
            "--target-root",
            str(tmp_path),
        ]
    )
    assert rc_write == 0
    rc_check = cli.main(
        [
            "--repo",
            "hapax-council",
            "--check",
            "--target-root",
            str(tmp_path),
        ]
    )
    assert rc_check == 0


@pytest.mark.parametrize("mode", [[], ["--check"], ["--dry-run"]])
@pytest.mark.parametrize("only_file", [[], ["--file", "SUPPORT.md"]])
@pytest.mark.parametrize("existing_target", [False, True])
def test_cli_all_rejects_shared_target_before_writes(
    tmp_path: Path, mode: list[str], only_file: list[str], existing_target: bool
) -> None:
    """A shared destination must fail before creating or overwriting consumers."""
    root = Path(__file__).resolve().parents[1]
    target = tmp_path / "consumer checkout"
    if existing_target:
        target.mkdir()
        (target / "SUPPORT.md").write_bytes(b"Keep existing support.\n")
        (target / "README.md").write_bytes(b"Keep existing README.\n")
    before = {
        p.name: (p.read_bytes(), p.stat().st_mode, p.stat().st_mtime_ns) for p in target.glob("*")
    }
    result = subprocess.run(
        [
            sys.executable,
            "-B",
            "-m",
            "hapax_sdlc.render",
            "--all",
            "--target-root",
            str(target),
            *only_file,
            *mode,
        ],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert result.stdout == ""
    assert "--all cannot be combined with --target-root" in result.stderr
    assert "overwrite" in result.stderr
    assert "--repo <id> --target-root <path>" in result.stderr
    assert "--check" in result.stderr
    assert target.exists() is existing_target
    assert {
        p.name: (p.read_bytes(), p.stat().st_mode, p.stat().st_mtime_ns) for p in target.glob("*")
    } == before

    # Follow the stated repair with the real CLI, retaining the artifact selection.
    args = [
        sys.executable,
        "-B",
        "-m",
        "hapax_sdlc.render",
        "--repo",
        "hapax-council",
        "--target-root",
        str(target),
        *only_file,
    ]
    for extra in ([], ["--check"]):
        repaired = subprocess.run(
            [*args, *extra], cwd=root, capture_output=True, text=True, check=False
        )
        assert repaired.returncode == 0, repaired.stderr
        assert repaired.stderr == ""
    assert (target / "SUPPORT.md").read_text() == support_md.render(
        load_registry()["hapax-council"]
    )


def test_cli_all_default_targets_converge(tmp_path: Path) -> None:
    """The supported --all form retains separate repository destinations."""
    with patch.object(cli, "default_target_root", side_effect=lambda repo: tmp_path / repo.name):
        args = ["--all", "--file", "SUPPORT.md"]
        assert cli.main(args) == 0
        assert cli.main([*args, "--check"]) == 0
    registry = load_registry()
    assert {p.name for p in tmp_path.iterdir()} == {
        repo.name for repo in registry.values() if repo.is_first_party
    }
    for repo in registry.values():
        if repo.is_first_party:
            assert (tmp_path / repo.name / "SUPPORT.md").read_text() == support_md.render(repo)


def test_org_profile_recheck_records_successful_observations(tmp_path: Path) -> None:
    """Pin the real witness's read-only requests and output; no live API is used."""
    root = Path(__file__).resolve().parents[1]
    agentgov_head = "0123456789abcdef0123456789abcdef01234567"
    release_fields = "{html_url, tag_name, target_commitish, draft, prerelease, published_at}"
    expected_calls = [
        [
            "api",
            "--paginate",
            "orgs/hapax-systems/repos?type=public&per_page=100",
            "--jq",
            "[.[] | {full_name, html_url, visibility, archived, default_branch}]",
        ],
        ["api", "repos/hapax-systems/hapax-spine/releases/tags/v0.1.1", "--jq", release_fields],
        ["api", "repos/hapax-systems/hapax-spine/releases/latest", "--jq", release_fields],
        [
            "api",
            "repos/hapax-systems/agentgov",
            "--jq",
            "{full_name, html_url, visibility, archived, default_branch, license}",
        ],
        ["api", "repos/hapax-systems/agentgov/releases/latest", "--jq", release_fields],
        ["api", "repos/hapax-systems/agentgov/commits/main", "--jq", ".sha"],
        [
            "api",
            f"repos/hapax-systems/agentgov/license?ref={agentgov_head}",
            "--jq",
            "{html_url, path, sha, license}",
        ],
        [
            "api",
            "-H",
            "Accept: application/vnd.github.raw+json",
            f"repos/hapax-systems/agentgov/contents/LICENSE?ref={agentgov_head}",
        ],
    ]
    archived = {
        "full_name": "hapax-systems/agentgov",
        "html_url": "https://github.com/hapax-systems/agentgov",
        "visibility": "public",
        "archived": True,
        "default_branch": "main",
    }
    spine = {
        **archived,
        "full_name": "hapax-systems/hapax-spine",
        "html_url": "https://github.com/hapax-systems/hapax-spine",
        "archived": False,
    }
    linked_release = {
        "html_url": "https://github.com/hapax-systems/hapax-spine/releases/tag/v0.1.1",
        "tag_name": "v0.1.1",
        "target_commitish": "main",
        "draft": False,
        "prerelease": False,
        "published_at": "2026-09-01T12:00:00Z",
    }
    latest_release = {
        **linked_release,
        "tag_name": "v0.2.0",
        "prerelease": True,
        "html_url": "https://github.com/hapax-systems/hapax-spine/releases/tag/v0.2.0",
        "published_at": "2026-09-23T12:00:00Z",
    }
    archived_release = {
        **linked_release,
        "tag_name": "v0.3.1",
        "html_url": "https://github.com/hapax-systems/agentgov/releases/tag/v0.3.1",
    }
    license_info = {"key": "mit", "name": "MIT License", "spdx_id": "MIT"}
    license_source = {
        "html_url": f"https://github.com/hapax-systems/agentgov/blob/{agentgov_head}/LICENSE",
        "path": "LICENSE",
        "sha": "f" * 40,
        "license": license_info,
    }
    # Deliberately synthetic text, distinct from GitHub's license detection.
    license_text = "SYNTHETIC LICENSE SOURCE\nRead the pinned terms, not just SPDX.\n"
    responses = [
        *(
            json.dumps(item) + "\n"
            for item in [
                [spine, archived],
                linked_release,
                latest_release,
                {**archived, "license": license_info},
                archived_release,
            ]
        ),
        agentgov_head + "\n",
        json.dumps(license_source) + "\n",
        license_text,
    ]
    response_file = tmp_path / "responses.json"
    response_file.write_text(json.dumps(responses))
    trace = tmp_path / "calls.json"
    stub = tmp_path / "gh"
    stub.write_text(
        f"#!{sys.executable}\n"
        "import json, os, sys\n"
        "from pathlib import Path\n"
        "trace = Path(os.environ['RECHECK_TEST_TRACE'])\n"
        "calls = json.loads(trace.read_text()) if trace.exists() else []\n"
        "calls.append(sys.argv[1:])\n"
        "trace.write_text(json.dumps(calls))\n"
        "responses = json.loads(Path(os.environ['RECHECK_TEST_RESPONSES']).read_text())\n"
        "sys.stdout.write(responses[len(calls) - 1])\n"
    )
    stub.chmod(0o755)
    source_paths = [
        "sdlc/render/org_profile_readme.py",
        "sdlc/render/repos.yaml",
        "tests/fixtures/org-profile-README.md",
    ]
    before = {path: ((root / path).read_bytes(), (root / path).stat()) for path in source_paths}
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True)
    status = subprocess.check_output(["git", "status", "--short"], cwd=root, text=True)
    start = datetime.now(timezone.utc).replace(microsecond=0)
    result = subprocess.run(
        ["bash", "docs/recheck-org-profile.sh"],
        cwd=root,
        capture_output=True,
        text=True,
        env={
            **os.environ,
            "PATH": f"{tmp_path}{os.pathsep}{os.environ['PATH']}",
            "GH_TOKEN": "synthetic-test-token-do-not-emit",
            "GITHUB_TOKEN": "synthetic-test-token-do-not-emit",
            "RECHECK_TEST_TRACE": str(trace),
            "RECHECK_TEST_RESPONSES": str(response_file),
        },
        check=False,
    )
    end = datetime.now(timezone.utc)
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    assert json.loads(trace.read_text()) == expected_calls
    observed_line, remaining = result.stdout.split("\n", 1)
    observed = datetime.strptime(observed_line, "Observed at: %Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc
    )
    assert start <= observed <= end
    expected = head + status
    for path, (data, stat) in before.items():
        expected += f"{sha256(data).hexdigest()}  {path}\n"
        assert (root / path).read_bytes() == data
        after = (root / path).stat()
        assert (after.st_mode, after.st_mtime_ns) == (stat.st_mode, stat.st_mtime_ns)
    expected += "Repository and release status checked September 24, 2026.\n"
    expected += "".join(responses[:5])
    expected += f"agentgov source commit: {agentgov_head}\n"
    expected += "".join(responses[6:])
    assert remaining == expected
    assert "synthetic-test-token-do-not-emit" not in result.stdout + result.stderr


@pytest.mark.parametrize("fail_at", range(1, 9))
def test_org_profile_recheck_stops_on_failed_observation(tmp_path: Path, fail_at: int) -> None:
    """Run the real shell witness; each failed API call must stop later observations."""
    root = Path(__file__).resolve().parents[1]
    stub = tmp_path / "gh"
    stub.write_text(
        f"#!{sys.executable}\n"
        "import os, sys\n"
        "from pathlib import Path\n"
        "trace = Path(os.environ['RECHECK_TEST_TRACE'])\n"
        "calls = trace.read_text().splitlines() if trace.exists() else []\n"
        "calls.append(' '.join(sys.argv[1:]))\n"
        "trace.write_text('\\n'.join(calls) + '\\n')\n"
        "if len(calls) == int(os.environ['RECHECK_TEST_FAIL_AT']):\n"
        "    print('simulated API observation failure', file=sys.stderr)\n"
        "    sys.exit(42)\n"
        "print('0123456789abcdef0123456789abcdef01234567' if len(calls) == 6 else '{}')\n"
    )
    stub.chmod(0o755)
    trace = tmp_path / "calls.txt"
    env = {
        **os.environ,
        "PATH": f"{tmp_path}{os.pathsep}{os.environ['PATH']}",
        "GH_TOKEN": "synthetic-test-token-do-not-emit",
        "GITHUB_TOKEN": "synthetic-test-token-do-not-emit",
        "RECHECK_TEST_TRACE": str(trace),
        "RECHECK_TEST_FAIL_AT": str(fail_at),
    }
    result = subprocess.run(
        ["bash", "docs/recheck-org-profile.sh"],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 42
    assert result.stderr == "simulated API observation failure\n"
    assert len(trace.read_text().splitlines()) == fail_at
    assert "synthetic-test-token-do-not-emit" not in result.stdout + result.stderr
    if fail_at <= 6:
        assert "agentgov source commit:" not in result.stdout


def test_cli_write_creates_nested_issue_template_config(tmp_path: Path) -> None:
    rc = cli.main(
        [
            "--repo",
            "hapax-council",
            "--target-root",
            str(tmp_path),
            "--file",
            ".github/ISSUE_TEMPLATE/config.yml",
        ]
    )
    assert rc == 0
    written = tmp_path / ".github" / "ISSUE_TEMPLATE" / "config.yml"
    assert written.exists()
    assert yaml.safe_load(written.read_text(encoding="utf-8"))["blank_issues_enabled"] is False


def test_cli_all_mode_renders_first_party_repos(tmp_path: Path) -> None:
    """The supported --all dry-run form includes every first-party repo."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = cli.main(["--all", "--dry-run"])
    output = buf.getvalue()
    assert rc == 0
    # Every first-party repo's name must appear at least once in the
    # rendered preamble blocks
    for repo_id in (
        "hapax-council",
        "hapax-constitution",
        "hapax-officium",
        "hapax-watch",
        "hapax-phone",
        "hapax-mcp",
        "hapax-coord",
        "hapax-spine",
        "hapax-assets",
        "hapax-research-ledger",
        "agentgov",
        "reins",
    ):
        assert repo_id in output


def test_cli_file_mode_renders_only_one_artifact() -> None:
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = cli.main(
            [
                "--repo",
                "hapax-council",
                "--dry-run",
                "--file",
                "CITATION.cff",
            ]
        )
    output = buf.getvalue()
    assert rc == 0
    assert "# CITATION.cff" in output
    assert "# codemeta.json" not in output


def test_cli_skips_upstream_forks_silently() -> None:
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = cli.main(["--repo", "tabbyAPI", "--dry-run"])
    output = buf.getvalue()
    assert rc == 0
    # No artifact headers should be printed for forks
    assert "# CITATION.cff" not in output


def test_render_artifacts_returns_empty_for_upstream_fork() -> None:
    registry = load_registry()
    identity = load_operator_identity()
    artifacts = cli.render_artifacts(registry["tabbyAPI"], identity)
    assert artifacts == {}


# --- Constitutional invariants ---------------------------------------------


def test_no_emoji_in_any_rendered_body(council_repo: RepoSpec, identity: OperatorIdentity) -> None:
    """HARDM anti-anthropomorphization: no emoji anywhere in body text."""
    bodies = [
        notice_md.render(council_repo),
        contributing_md.render(council_repo),
        security_md.render(council_repo, identity),
        support_md.render(council_repo),
        governance_md.render(council_repo),
        issue_template_config_yml.render(council_repo),
        readme_section.render(council_repo),
    ]
    for body in bodies:
        for ch in body:
            assert not 0x1F300 <= ord(ch) <= 0x1FAFF, f"emoji {ch!r} found in rendered body"


def test_no_first_person_we_in_constitutional_disclosures(
    council_repo: RepoSpec, identity: OperatorIdentity
) -> None:
    """Constitutional non-negotiable: no 'we'/'our team' in templates
    (anti-anthropomorphization, scientific register).
    """
    bodies = [
        notice_md.render(council_repo),
        contributing_md.render(council_repo),
        security_md.render(council_repo, identity),
        support_md.render(council_repo),
        issue_template_config_yml.render(council_repo),
        readme_section.render(council_repo),
    ]
    banned = (" we ", " We ", "our team", "Our team")
    for body in bodies:
        for needle in banned:
            assert needle not in body, f"banned phrase {needle!r} present in rendered body"


def test_formal_metadata_uses_org_creator_not_legal_name(
    council_repo: RepoSpec, identity: OperatorIdentity
) -> None:
    """Public metadata uses Hapax Systems as creator; operator legal name
    must not be rendered by default in public repo metadata or body text.
    """
    legal_full = identity.full_name
    legal_parts = legal_full.split()
    citation_body = citation_cff.render(council_repo, identity)
    codemeta_body = codemeta_json.render(council_repo, identity)
    zenodo_body = zenodo_json.render(council_repo, identity)

    all_public_bodies = [
        citation_body,
        codemeta_body,
        zenodo_body,
        notice_md.render(council_repo),
        contributing_md.render(council_repo),
        security_md.render(council_repo, identity),
        support_md.render(council_repo),
        governance_md.render(council_repo),
        issue_template_config_yml.render(council_repo),
        readme_section.render(council_repo),
    ]
    for body in (citation_body, codemeta_body, zenodo_body):
        assert "Hapax Systems" in body
    for body in all_public_bodies:
        assert legal_full not in body
        for part in legal_parts:
            assert part not in body
