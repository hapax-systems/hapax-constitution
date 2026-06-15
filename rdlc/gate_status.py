"""GateStatus — the honest-dark trichotomy.

NEVER ``bool()``-coerced; always compared by identity. A truthiness coercion would let a
DARK gate read as falsy-but-present or a PARTIAL as "good enough" — exactly the silent
shortcut honest-dark forbids.
"""

from __future__ import annotations

from enum import Enum


class GateStatus(Enum):
    LIT = "lit"  # the gate exists and ran — carries a Verdict
    PARTIAL = "partial"  # machinery exists (at M) but no RDLC-level enforcement yet
    DARK = "dark"  # no model/gate exists here — a forced terminal stalk {*}
