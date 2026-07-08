"""SECURITY.md renderer.

Per the operational checklist, the disclosure path is **not** an email
address — it is a Sigstore-signed disclosure path. Constitutional
requirement: operator does not publish email on repository surfaces.
"""

from __future__ import annotations

from sdlc.render.repo_registry import OperatorIdentity, RepoSpec


def render(repo: RepoSpec, identity: OperatorIdentity) -> str:
    return (
        "# Security policy\n"
        "\n"
        "A single individual operates this repository in a single-operator "
        "deployment. Public repository surfaces are not a multi-tenant "
        "product, customer-data processor, or public auth service. That "
        "boundary is a scope statement, not a warranty about every internal "
        "integration.\n"
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
        f"In scope: exposure of secrets or private material in public "
        f"commits/artifacts, public-egress bypasses, supply-chain or "
        f"workflow weaknesses, and concrete remotely exploitable defects. "
        f"Out of scope: feature requests for multi-tenancy, RBAC, federated "
        f"identity, general hardening consultations, or integration support.\n"
        "\n"
        "## Response time\n"
        "\n"
        "Best-effort, single-operator basis; no SLA. Critical disclosures "
        "such as remote code execution or leaked secrets in published "
        "commits are triaged out of band immediately; other reports wait "
        "for a maintenance window.\n"
        "\n"
        "## Advisory record\n"
        "\n"
        "This rendered policy does not maintain a complete dated advisory "
        "ledger. Current advisories, if any, belong in release notes, "
        "security notices, or publication-bus records with their own dates "
        "and receipts.\n"
        "\n"
        "---\n"
        "\n"
        "This file is rendered from `hapax-constitution/sdlc/render/`. "
        "Edits are overwritten on next render.\n"
    )
