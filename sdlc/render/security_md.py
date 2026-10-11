"""SECURITY.md renderer.

The disclosure path names the network's public contact address (A16) and
links the contact page; disclosures attach Sigstore-signed artifacts when
applicable. The practice of not publishing an address on repository
surfaces comes from the "Operational checklist" of
hapax-council/docs/research/2026-04-25-github-repo-presentation.md —
agent-written research, not a constitutional rule — and the seat's ruling
does not apply it to the network's address.
"""

from __future__ import annotations

from urllib.parse import urldefrag

from sdlc.render.repo_registry import OperatorIdentity, RepoSpec


def _recheck(identity: OperatorIdentity) -> str:
    """Render the address-check line from identity.

    The page is ``contact_url`` without its fragment. The anchor half
    derives from the fragment; a URL without one renders the address half
    alone.
    """
    page, fragment = urldefrag(identity.contact_url)
    legs = []
    if fragment:
        legs.append(f"curl -fsSL {page} | grep -qF 'id=\"{fragment}\"'")
    legs.append(f"curl -fsSL {page} | grep -qF '{identity.contact_email}'")
    return " && ".join(legs)


def render(repo: RepoSpec, identity: OperatorIdentity) -> str:
    return (
        "# Security policy\n"
        "\n"
        "This repository is published by Hapax Research Lab. Public "
        "repository surfaces are not a multi-tenant product, "
        "customer-data processor, or public auth service. That boundary "
        "is a scope statement, not a warranty about every internal "
        "integration.\n"
        "\n"
        "## Disclosure path\n"
        "\n"
        f"Send security disclosures to {identity.contact_email}, the "
        f"address on the lab's contact page. Attach Sigstore-signed "
        f"disclosure artifacts when applicable. The commitment that "
        f"covers this address is on that page:\n"
        "\n"
        f"  {identity.contact_url}\n"
        "\n"
        "Sigstore's keyless signing associates each signature with an "
        "OpenID Connect identity through a short-lived certificate, and "
        "logs the signing event in Rekor, a signature transparency "
        "log.\n"
        "\n"
        "Address check (fails if the contact page no longer carries its "
        "contact section or this address):\n"
        "\n"
        "```bash\n"
        f"{_recheck(identity)}\n"
        "```\n"
        "\n"
        "## Scope\n"
        "\n"
        "In scope: exposure of secrets or private material in public "
        "commits/artifacts, public-egress bypasses, supply-chain or "
        "workflow weaknesses, and concrete remotely exploitable defects. "
        "Out of scope: feature requests for multi-tenancy, RBAC, "
        "federated identity, general hardening consultations, or "
        "integration support.\n"
        "\n"
        "## Response time\n"
        "\n"
        "Best effort; no SLA. Messages sent to this address fall under "
        'the commitment stated on the contact page: "The network commits '
        'to receipt, retention and published correction. It promises no '
        'response time." The page also says: "Today one person inside '
        'the network is the first reader of incoming mail, so a '
        'correction request currently reaches the network through that '
        'person." Critical disclosures, such as remote code execution '
        "or leaked secrets in published commits, are triaged out of "
        "band as soon as they are read, not deferred to a maintenance "
        "window. Other reports wait for one.\n"
        "\n"
        "## Advisory record\n"
        "\n"
        "This rendered policy does not maintain a complete dated "
        "advisory ledger. Current advisories, if any, belong in release "
        "notes, security notices, or publication-bus records with their "
        "own dates and receipts.\n"
        "\n"
        "---\n"
        "\n"
        "This file is rendered from `hapax-constitution/sdlc/render/`. "
        "Edits are overwritten on next render.\n"
    )
