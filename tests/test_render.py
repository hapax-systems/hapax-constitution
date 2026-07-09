"""Tests for ``sdlc.render`` (published as ``hapax_sdlc.render``).

Per workspace conventions: ``unittest.mock`` only, file is self-contained,
no shared conftest fixtures.
"""

from __future__ import annotations

import io
import json
from contextlib import redirect_stdout
from pathlib import Path

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
    assert registry["agentgov"].value_partition is ValuePartition.ADOPTION_COMMONS
    assert registry["agentgov"].license_posture.startswith("Permissive adoption surface")

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
    assert registry["agentgov"].surface_class is SurfaceClass.ADOPTION_COMMONS
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
    assert "bounded adoption surface" in body
    assert "staffed support channel" in body
    assert "Blank issues are disabled" in body
    assert "no-perk research support only" in body
    assert "does not create an SLA" in body


def test_product_and_adoption_preambles_do_not_use_generic_research_artifact_copy() -> None:
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
    assert "adoption-commons" in agentgov_body
    assert "governance-hook surface" in agentgov_body
    assert "Permissive adoption surface" in agentgov_body
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
    assert "bounded adoption surface" in agentgov_contributing
    assert "community maintenance" in agentgov_contributing
    assert "not a product" not in agentgov_contributing


def test_org_profile_readme_orients_public_portfolio_without_private_repo_table() -> None:
    registry = load_registry()
    body = org_profile_readme.render(registry)
    assert body.startswith("# Hapax Systems")
    assert "authority before action" in body
    assert "receipts before claims" in body
    assert "unsupported automation claims" in body
    assert "Reader value" in body
    assert "what evidence would have to exist" in body

    assert "[reins](https://github.com/hapax-systems/reins)" in body
    assert "[agentgov](https://github.com/hapax-systems/agentgov)" in body
    assert "[hapax-council](https://github.com/hapax-systems/hapax-council)" in body
    assert "[hapax-constitution](https://github.com/hapax-systems/hapax-constitution)" in body
    assert "[hapax-mcp](https://github.com/hapax-systems/hapax-mcp)" in body
    assert "[hapax-phone](https://github.com/hapax-systems/hapax-phone)" in body
    assert "[hapax-watch](https://github.com/hapax-systems/hapax-watch)" in body
    assert "Supporting Public Surfaces" in body
    assert "Hapax Logos MCP Bridge" in body
    assert "Mobile Context Source" in body
    assert "Wrist Biometric Source" in body

    assert "hapax-spine](https://github.com/hapax-systems/hapax-spine)" not in body
    assert "hapax-coord](https://github.com/hapax-systems/hapax-coord)" not in body


def test_org_profile_readme_pins_claim_ceiling_and_license_boundaries() -> None:
    body = org_profile_readme.render(load_registry())
    assert "open adoption commons" in body
    assert "source-available commercial core" in body
    assert "source-visible research apparatus" in body
    assert "remains a read/preview surface" in body
    assert "not a general-purpose lifecycle kernel" in body
    # Spine went public 2026-07-09 (Part-4 decision): the profile states the
    # source-available posture; visibility-vs-copy mismatch never returns in
    # either direction.
    assert "spine is the source-available BSL 1.1 runtime mechanism" in body
    assert "private during restructure" not in body
    # Capability Frontier embargo: scores are registry-asserted today;
    # "measured capability" is claimable only once the measurement loop runs.
    assert "registry-asserted today; measured calibration is planned" in body
    assert "describe measured capability" not in body
    assert "not as a supported framework" in body
    assert "not claim autonomous write authority" in body
    assert "full general lifecycle coverage" in body
    assert "staffed community support" in body
    assert "publication-bus channels" in body
    assert "must not imply direct public" in body
    assert "Hapax is open source" not in body
    assert "generic agent OS" not in body
    assert "guaranteed safe" not in body


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
    """``--all`` renders every first-party repo. Each gets its own
    target subdirectory under ``--target-root`` is not yet supported —
    here we just verify the dry-run path handles --all without error.
    """
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
