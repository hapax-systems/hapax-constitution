"""Generic ordinal-ladder helper shared by every lifecycle's stage enum.

Tier-0 commons: imports nothing from any lifecycle (``sdlc``/``rdlc``) or model
(``ndcvb``). A lifecycle's stage ladder is an ``IntEnum`` whose members are named
``<PREFIX><n>_NAME`` (e.g. ``S5_AUTHORIZATION_PACKET``, ``R2_PREREGISTER``); this
helper parses a YAML label to a member by name or by ``<PREFIX><n>`` shorthand.

It is the one shared piece of the stage machinery; each lifecycle keeps its own
*plant predicates* (``allows_source_mutation`` for SDLC, ``allows_public_claim``
for RDLC) in its own module — those are plant content, not commons.
"""

from __future__ import annotations

from enum import IntEnum
from typing import TypeVar

E = TypeVar("E", bound=IntEnum)


def stage_from_label(enum_cls: type[E], label: str, *, prefix: str) -> E:
    """Parse a stage label to a member of ``enum_cls``.

    Accepts the member name (``"R2_preregister"``) or the ``<PREFIX><n>``
    shorthand (``"R2"``), case-insensitively, with ``-`` normalized to ``_``.
    """
    normalized = label.upper().replace("-", "_")
    for member in enum_cls:
        if member.name == normalized:
            return member
        if normalized == f"{prefix}{member.value}":
            return member
    raise ValueError(f"Unknown {enum_cls.__name__} stage: {label!r}")
