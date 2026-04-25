"""Module entry point: ``python -m sdlc.render`` and (via shim package)
``python -m hapax_sdlc.render``.

Implementation lives in ``sdlc.render.cli``; this is a thin dispatcher.
"""

from __future__ import annotations

import sys

from sdlc.render.cli import main

if __name__ == "__main__":
    sys.exit(main())
