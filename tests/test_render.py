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
    notice_md,
    readme_section,
    security_md,
    zenodo_json,
)
from sdlc.render.operator_referent import REFERENTS, OperatorReferentPicker
from sdlc.render.repo_registry import (
    LicenseClass,
    OperatorIdentity,
    RepoSpec,
    load_operator_identity,
    load_registry,
)


# --- Registry --------------------------------------------------------------


def test_registry_has_seven_first_party_repos() -> None:
    registry = load_registry()
    first_party = [s for s in registry.values() if s.is_first_party]
    assert len(first_party) == 7
    ids = sorted(s.id for s in first_party)
    assert ids == [
        "hapax-assets",
        "hapax-constitution",
        "hapax-council",
        "hapax-mcp",
        "hapax-officium",
        "hapax-phone",
        "hapax-watch",
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
    assert parsed["authors"][0]["family-names"] == "Zarbacaster"
    assert parsed["authors"][0]["given-names"] == "Quentin"
    assert parsed["authors"][0]["orcid"] == identity.orcid
    assert parsed["license"] == "PolyForm-Strict-1.0.0"
    assert "research-software" in parsed["keywords"]


def test_codemeta_json_parses_and_aligns_to_v3_jsonld(
    council_repo: RepoSpec, identity: OperatorIdentity
) -> None:
    body = codemeta_json.render(council_repo, identity)
    parsed = json.loads(body)
    assert parsed["@context"] == "https://w3id.org/codemeta/3.0"
    assert parsed["@type"] == "SoftwareSourceCode"
    assert parsed["author"][0]["@id"] == identity.orcid
    assert parsed["license"] == ("https://polyformproject.org/licenses/strict/1.0.0/")
    assert parsed["codeRepository"] == "https://github.com/ryanklee/hapax-council"


def test_zenodo_json_carries_related_identifier_graph(
    council_repo: RepoSpec, identity: OperatorIdentity
) -> None:
    body = zenodo_json.render(council_repo, identity)
    parsed = json.loads(body)
    assert parsed["upload_type"] == "software"
    assert parsed["access_right"] == "open"
    # ORCID stripped of URL prefix per Zenodo schema
    assert parsed["creators"][0]["orcid"] == "0000-0000-0000-0001"
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
    referent = OperatorReferentPicker.pick_for_artifact(council_repo.id)
    assert referent in body
    assert "Single-operator" in body
    assert "https://github.com/ryanklee/hapax-constitution" in body


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


def test_governance_md_anchor_vs_redirect(
    council_repo: RepoSpec, constitution_repo: RepoSpec
) -> None:
    anchor_body = governance_md.render(constitution_repo)
    redirect_body = governance_md.render(council_repo)
    assert "canonical axiom registry" in anchor_body
    assert "Governance for this repository is centralised" in redirect_body
    assert "https://github.com/ryanklee/hapax-constitution" in redirect_body


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
        "GOVERNANCE.md",
        "README.md",
    ):
        assert f"# {filename}" in output


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
    assert rc == 1  # all 8 files drifted


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


def test_cli_all_mode_renders_seven_first_party_repos(tmp_path: Path) -> None:
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
        "hapax-assets",
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
        governance_md.render(council_repo),
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
        readme_section.render(council_repo),
    ]
    banned = (" we ", " We ", "our team", "Our team")
    for body in bodies:
        for needle in banned:
            assert needle not in body, f"banned phrase {needle!r} present in rendered body"


def test_legal_name_only_appears_in_formal_contexts(
    council_repo: RepoSpec, identity: OperatorIdentity
) -> None:
    """Operator-referent policy: legal name in CITATION/codemeta/.zenodo
    only. NEVER in body text of NOTICE/CONTRIBUTING/SECURITY/GOVERNANCE/
    README preamble.
    """
    # Legal-name parts (CITATION.cff splits given/family; codemeta uses
    # givenName/familyName; .zenodo.json uses joined form).
    legal_full = identity.full_name
    legal_parts = legal_full.split()
    citation_body = citation_cff.render(council_repo, identity)
    codemeta_body = codemeta_json.render(council_repo, identity)
    zenodo_body = zenodo_json.render(council_repo, identity)
    # Joined form must appear in zenodo.json creators name field.
    assert legal_full in zenodo_body
    # Both parts must appear in citation + codemeta (split form).
    for part in legal_parts:
        assert part in citation_body
        assert part in codemeta_body

    forbidden = [
        notice_md.render(council_repo),
        contributing_md.render(council_repo),
        security_md.render(council_repo, identity),
        governance_md.render(council_repo),
        readme_section.render(council_repo),
    ]
    for body in forbidden:
        assert legal_full not in body
        for part in legal_parts:
            assert part not in body
