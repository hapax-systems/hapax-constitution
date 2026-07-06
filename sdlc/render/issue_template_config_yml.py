"""GitHub issue-template chooser config renderer."""

from __future__ import annotations

import yaml

from sdlc.render.repo_registry import RepoSpec, github_repo_url


def render(repo: RepoSpec) -> str:
    """Return ``.github/ISSUE_TEMPLATE/config.yml`` for redirect-only issues."""
    config = {
        "blank_issues_enabled": False,
        "contact_links": [
            {
                "name": "Read the repository overview",
                "url": f"{repo.github_url}#readme",
                "about": "Start with the rendered README and repository body.",
            },
            {
                "name": "Read the support boundary",
                "url": f"{repo.github_url}/blob/main/SUPPORT.md",
                "about": "GitHub Issues are not a staffed support queue.",
            },
            {
                "name": "Report a security issue",
                "url": f"{repo.github_url}/security/policy",
                "about": "Use the repository security policy for disclosures.",
            },
            {
                "name": "Read Hapax governance",
                "url": github_repo_url("hapax-constitution"),
                "about": "Repository governance is centralized in hapax-constitution.",
            },
        ],
    }
    return yaml.safe_dump(config, sort_keys=False)
