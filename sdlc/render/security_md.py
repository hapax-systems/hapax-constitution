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
        f"A single individual ({referent}) operates this repository. It runs "
        f"in a single-operator deployment with no external users, no auth "
        f"surface, and no third-party data residency.\n"
        "\n"
        "## Disclosure path\n"
        "\n"
        f"Submit security disclosures through the contact page. Attach "
        f"Sigstore-signed disclosure artifacts when applicable:\n"
        "\n"
        f"  {identity.contact_url}\n"
        "\n"
        f"Repository surfaces do not publish email by constitutional choice. "
        f"Sigstore signatures let the operator verify authorship via OpenID "
        f"Connect without publishing an email address.\n"
        "\n"
        "Endpoint recheck:\n"
        "\n"
        "```bash\n"
        f"curl -fsSIL {identity.contact_url}\n"
        "```\n"
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
        "Best-effort, single-operator basis; no SLA. The next maintenance "
        "window handles critical disclosures such as remote code execution "
        "or secret leaks in published commits.\n"
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
