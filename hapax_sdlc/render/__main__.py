"""Module entry point: ``python -m hapax_sdlc.render``."""

from __future__ import annotations

import sys

from sdlc.render.cli import main

if __name__ == "__main__":
    sys.exit(main())
