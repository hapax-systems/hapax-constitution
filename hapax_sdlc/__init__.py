"""hapax_sdlc — published-package import path for hapax-sdlc.

The published `hapax-sdlc` distribution exposes its modules under the
`hapax_sdlc.*` import path. Internally, the source layout uses `sdlc/`
because that path predates the package rename. This module re-exports
the relevant subpackages so downstream consumers see the canonical
`hapax_sdlc.render` API while local code keeps using `sdlc.render`.
"""

from sdlc import render

__all__ = ["render"]
