"""Tier-0 commons: the shared governance-case spine.

Every governed lifecycle's case model is a ``BaseGovernanceCase`` — ``AuthorityCase``
for SDLC (the code-mutation plant), ``ResearchCase`` for RDLC (the claim-assertion
plant), and any future sibling (MPDLC, Life-DLC, ...). The base carries ONLY
plant-agnostic identity fields plus the byte-identical YAML-frontmatter mechanics
pulled up from ``AuthorityCase``.

The base deliberately has **no authorization fields**. A lifecycle's plant-specific
no-go fields (e.g. SDLC's ``source_mutation_authorized``, RDLC's
``assertion_authorized``) live only on the subclass, so the category error of one
lifecycle's verbs leaking into another's case is *type-impossible by inheritance*,
not merely discouraged. ``parsed_stage``/``no_go_violations`` are abstract and raise
``NotImplementedError`` — never defaulted to a fabricated pass (that would be a
silent green, the honest-dark rule's type-illegal move at the case layer).

Tier-0 purity: imports nothing from any lifecycle (``sdlc``/``rdlc``) or model
(``ndcvb``).
"""

from __future__ import annotations

from datetime import datetime
from enum import IntEnum
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel


class BaseGovernanceCase(BaseModel):
    """Plant-agnostic governance-case spine (see module docstring)."""

    case_id: str
    version: int = 0
    stage: str
    status: str
    created_utc: datetime
    originator: str
    methodology: str | None = None
    risk_tier: str | None = None

    model_config = {"extra": "allow"}

    @classmethod
    def from_yaml(cls, text: str) -> BaseGovernanceCase:
        """Parse a case from a markdown document's YAML frontmatter."""
        frontmatter = _extract_frontmatter(text)
        if frontmatter is None:
            raise ValueError("No YAML frontmatter found")
        return cls.model_validate(frontmatter)

    @classmethod
    def from_file(cls, path: str) -> BaseGovernanceCase:
        """Load a case from a file path."""
        return cls.from_yaml(Path(path).read_text(encoding="utf-8"))

    def parsed_stage(self) -> IntEnum:
        """Return the case's stage as the subclass's ladder member."""
        raise NotImplementedError("each lifecycle binds its own stage ladder")

    def no_go_violations(self) -> list[str]:
        """Return authorization fields dangerously set for the current stage."""
        raise NotImplementedError("each lifecycle binds its own no-go semantics")


def _extract_frontmatter(text: str) -> dict[str, Any] | None:
    """Extract YAML frontmatter from a markdown document."""
    text = text.strip()
    if not text.startswith("---"):
        return None
    end = text.find("---", 3)
    if end == -1:
        return None
    data = yaml.safe_load(text[3:end].strip())
    return data if isinstance(data, dict) else None
