"""SECURITY.md renderer.

Per the operational checklist, the disclosure path is **not** an email
address — it is a Sigstore-signed disclosure path. Constitutional
requirement: operator does not publish email on repository surfaces.
"""

from __future__ import annotations

from sdlc.render.operator_referent import OperatorReferentPicker
from sdlc.render.repo_registry import OperatorIdentity, RepoSpec


def render(repo: RepoSpec, identity: OperatorIdentity) -> str:
    referent = OperatorReferentPicker.pick_for_artifact(repo.id)
    return (
        "# Security policy\n"
        "\n"
        f"This repository is operated by a single individual ({referent}). "
        f"It runs in a single-operator deployment with no external users, "
        f"no auth surface, and no third-party data residency.\n"
        "\n"
        "## Disclosure path\n"
        "\n"
        f"Submit security disclosures via the Sigstore-signed disclosure "
        f"channel at:\n"
        "\n"
        f"  {identity.contact_url}\n"
        "\n"
        f"Email is not published on repository surfaces by constitutional "
        f"choice. The Sigstore path verifies disclosure authorship via "
        f"OpenID Connect, eliminating the need for PGP key exchange or "
        f"private email correspondence.\n"
        "\n"
        "## Scope\n"
        "\n"
        f"Security reports about deployment hardening, architectural "
        f"choices, or features absent from a single-operator system "
        f"(multi-tenancy, RBAC, federated identity) are out of scope; the "
        f"single-operator axiom forecloses these.\n"
        "\n"
        "## Response time\n"
        "\n"
        "Best-effort, single-operator basis; no SLA. Critical disclosures "
        "(remote code execution, secret leak in published commits) are "
        "addressed in the next maintenance window.\n"
        "\n"
        "## Past advisories\n"
        "\n"
        "None to date.\n"
        "\n"
        "---\n"
        "\n"
        "This file is rendered from `hapax-constitution/sdlc/render/`. "
        "Edits are overwritten on next render.\n"
    )
