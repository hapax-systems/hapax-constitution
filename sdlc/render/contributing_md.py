"""CONTRIBUTING.md renderer (refuse-and-redirect mode).

CONTRIBUTING.md is positively asserted with explicit governance refusal and
redirect text rather than left absent (which would allow GitHub's default
contribution prompts to imply an open community patch queue).
"""

from __future__ import annotations

from sdlc.render.repo_registry import RepoSpec, SurfaceClass, github_repo_url


def render(repo: RepoSpec) -> str:
    return (
        "# Contributing\n"
        "\n"
        "This repository does not accept external contributions through GitHub. "
        "It is published by **Hapax Research Lab** (`hrl-han`, "
        "https://hapaxresearch.com) and governed as a single trust domain under "
        "`hapax-constitution`. Research and engineering staff are AI agents; one "
        "human, the lab's principal, holds constitutional authority inside "
        "`hrl-han`. Public repositories are published for inspection, citation, "
        "and use within their stated license, not for external contributor "
        "onboarding or community patch queues.\n"
        "\n"
        "## Why\n"
        "\n"
        f"{_why(repo)}\n"
        "\n"
        "## What this means in practice\n"
        "\n"
        "- Issues are redirect-only; `.github/ISSUE_TEMPLATE/config.yml` "
        "disables blank issues.\n"
        "- Pull requests from external forks are not an intake path for this "
        "repository.\n"
        "- Repositories disable Discussions, Projects, and Wiki across the "
        "`hapax-systems` organization.\n"
        "- Funding links, if present, are no-perk research support only.\n"
        "- This file is rendered from `hapax-constitution/sdlc/render/`; "
        "edits are overwritten on next render.\n"
        "\n"
        "## Security disclosures and factual corrections\n"
        "\n"
        f"{_bug_boundary(repo)}\n"
        "\n"
        "Send concrete security disclosures or factual correction proposals to "
        "`hrl-han@hapaxresearch.com` (see `SECURITY.md` and "
        "https://hapaxresearch.com/about/#contact). The network commits to "
        "receipt, retention and published correction. It promises no response "
        "time.\n"
        "\n"
        "## Citation\n"
        "\n"
        "If your research engages with this repository, cite via `CITATION.cff` "
        "(Citation File Format v1.2.0) and `.zenodo.json`.\n"
    )


def _why(repo: RepoSpec) -> str:
    if repo.archived or repo.surface_class is SurfaceClass.HISTORICAL_ARCHIVE:
        return (
            f"`{repo.name}` is an archived historical prototype superseded by "
            f"[reins]({github_repo_url('reins')}). It remains public for "
            "inspection and citation under its MIT license and is not under "
            "active development or community maintenance."
        )
    if repo.surface_class is SurfaceClass.ADOPTION_COMMONS:
        return (
            f"`{repo.name}` is a bounded adoption surface in the Hapax "
            "Research Lab portfolio. It is inspectable and usable under its "
            "stated license, while releases remain governed inside `hrl-han` "
            "rather than through community maintenance."
        )
    if repo.surface_class is SurfaceClass.PRODUCT_FRONT_DOOR:
        return (
            f"`{repo.name}` is the Hapax Research Lab product front door. GitHub is "
            "an inspection and source-available evaluation surface, not the "
            "support, roadmap, or commercial intake channel."
        )
    if repo.surface_class is SurfaceClass.RUNTIME_MECHANISM:
        return (
            f"`{repo.name}` is a source-available runtime mechanism. It is "
            "published for inspection and evaluation without turning the "
            "mechanism into a community-maintained framework."
        )
    return (
        "Hapax Research Lab operates its software and evidence repositories "
        "inside a single constitutional trust domain (`hrl-han`). Keeping "
        "GitHub read-and-verify prevents repository affordances from implying "
        "an unstaffed support queue, community governance body, or external "
        "patch-review obligation."
    )


def _bug_boundary(repo: RepoSpec) -> str:
    if repo.archived or repo.surface_class is SurfaceClass.HISTORICAL_ARCHIVE:
        return (
            f"This repository is archived and receives no feature or bug-fix "
            f"maintenance; evaluate [reins]({github_repo_url('reins')}) for "
            "active governed agent-delivery inspection."
        )
    if repo.surface_class is SurfaceClass.ADOPTION_COMMONS:
        return (
            "Use the published documentation and examples to evaluate the "
            "adoption surface. GitHub Issues remain redirect-only, not a "
            "staffed support queue."
        )
    if repo.surface_class is SurfaceClass.PRODUCT_FRONT_DOOR:
        return (
            "Use the published demo and evaluation path (`reins --demo`) to "
            "inspect shipped behavior. Operational support and commercial "
            "discussions do not happen through GitHub Issues."
        )
    if repo.surface_class is SurfaceClass.RUNTIME_MECHANISM:
        return (
            "Use the repository as a source-available inspection surface. "
            "Integration help and framework-style issue triage are out of "
            "scope for GitHub."
        )
    return (
        "Security disclosures and factual error reports remain in scope via "
        "`SECURITY.md`. Feature requests, integration troubleshooting, and "
        "community maintenance requests are out of scope for GitHub."
    )
