"""Import-graph invariants enforced as a CI gate (converts the sibling/tier discipline
from convention to a test):

- commons is tier-0 PURE: it imports nothing from a lifecycle (sdlc/rdlc) or a model (ndcvb).
- rdlc never RUNTIME-imports sdlc (rdlc imports only commons).
- ndcvb is RUNTIME-imported only by rdlc/m_binding.py (so importing rdlc never requires
  the research repo; type-only imports under TYPE_CHECKING are allowed anywhere).
- sdlc never imports rdlc (siblings do not depend on each other).
"""

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _pkg_files(pkg: str) -> list[Path]:
    return sorted((ROOT / pkg).glob("*.py"))


def _runtime_imports(path: Path) -> set[str]:
    """Module names imported at RUNTIME (anywhere, incl. inside functions), excluding
    imports guarded by ``if TYPE_CHECKING:``."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found: set[str] = set()

    def visit(node: ast.AST, in_type_checking: bool) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.If):
                test = child.test
                is_tc = isinstance(test, ast.Name) and test.id == "TYPE_CHECKING"
                for n in child.body:
                    visit(n, in_type_checking or is_tc)
                for n in child.orelse:
                    visit(n, in_type_checking)
            elif isinstance(child, ast.ImportFrom):
                if not in_type_checking and child.module:
                    found.add(child.module)
            elif isinstance(child, ast.Import):
                if not in_type_checking:
                    for alias in child.names:
                        found.add(alias.name)
            else:
                visit(child, in_type_checking)

    visit(tree, False)
    return found


def _mentions(text: str, module: str) -> bool:
    return re.search(rf"(?m)^\s*(from|import)\s+{re.escape(module)}(\.|\s|$)", text) is not None


def test_commons_is_tier0_pure():
    for f in _pkg_files("commons"):
        text = f.read_text(encoding="utf-8")
        for forbidden in ("sdlc", "rdlc", "ndcvb"):
            assert not _mentions(text, forbidden), (
                f"commons/{f.name} imports {forbidden} — tier-0 must be pure"
            )


def test_rdlc_does_not_import_sdlc():
    for f in _pkg_files("rdlc"):
        sdlc_imports = {m for m in _runtime_imports(f) if m == "sdlc" or m.startswith("sdlc.")}
        assert not sdlc_imports, (
            f"rdlc/{f.name} runtime-imports {sdlc_imports}; rdlc imports only commons, never sdlc"
        )


def test_ndcvb_runtime_imported_only_by_m_binding():
    for f in _pkg_files("rdlc"):
        ndcvb_imports = {m for m in _runtime_imports(f) if m == "ndcvb" or m.startswith("ndcvb.")}
        if f.name == "m_binding.py":
            continue
        assert not ndcvb_imports, (
            f"rdlc/{f.name} runtime-imports {ndcvb_imports}; only m_binding may bind M"
        )


def test_sdlc_does_not_import_rdlc():
    for f in _pkg_files("sdlc"):
        text = f.read_text(encoding="utf-8")
        assert not _mentions(text, "rdlc"), (
            f"sdlc/{f.name} imports rdlc — siblings must not depend on each other"
        )
