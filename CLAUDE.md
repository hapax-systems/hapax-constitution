# CLAUDE.md

Governance architecture for LLM agent systems — constitutional axioms, derived implications, interpretive canon, sufficiency probes, and precedent store. **Specification repo**: YAML definitions, deterministic `hapax-sdlc` render/check tooling, and markdown documentation, not runtime application code.

Shared conventions (uv, ruff, testing, git workflow) are in the workspace `CLAUDE.md` — this file covers constitution-specific details only.

**Consumers of this spec:** Private runtime estates (`hapax-council` and `hapax-officium`) consume this specification via the `hapax-sdlc` package alongside public surfaces documented at [hapaxresearch.com](https://hapaxresearch.com). Changes to `axioms/registry.yaml` propagate to downstream consumers on dependency bump.

## Key Files

- **`axioms/registry.yaml`** — Canonical axiom definitions (IDs, weights, scope, text)
- **`axioms/implications/`** — Per-axiom derived implications with tier (T0/T1/T2/T3), enforcement mode, sufficiency levels
- **`domains/`** — Domain-scoped axiom extensions (infrastructure, management)
- **`knowledge/`** — Sufficiency probes per domain (management, music, personal, technical)
- **`sdlc/render/`** — Deterministic constellation registry (`repos.yaml`), presentation renderers, and GitHub settings policy (`repo_settings.py`)
- **`pattern-guide.md`** — Guide for implementing the governance pattern

## Conventions

Workspace-wide conventions (worktree discipline, PR completion rules, ownership) are in the workspace `CLAUDE.md`. This file covers constitution-specific conventions only.

- **This is a spec repo.** Changes to `axioms/registry.yaml` are always high-complexity and require human review.
- **YAML is the source of truth** for axiom definitions and implications. Markdown documents describe; YAML defines.
- **Weight ordering matters.** Higher weight = higher precedence. Constitutional axioms always outweigh domain axioms (supremacy clause).
- **Tier semantics are strict.** T0 = block (existential violation), T1 = review (requires awareness), T2 = warn (quality preference), T3 = lint (advisory style/documentation guidance, enforcement: linter).

## Local Validation

```bash
uv sync
uv run ruff check .              # Lint Python (SDLC scripts)
uv run ruff format --check .     # Format check
yamllint -d relaxed axioms/ domains/ knowledge/  # YAML lint
python sdlc/consistency_check.py --json --check-resolutions
```

CI runs deterministic YAML linting, deontic consistency checks, sufficiency scope validation, and capability coverage automatically via `yaml-lint.yml` alongside `ci.yml` and `semgrep.yml`.

## Public Workflow Surface

Public GitHub Actions on this repository are restricted to deterministic validation and settings-drift gates (`yaml-lint.yml`, `ci.yml`, `semgrep.yml`, `repo-settings-drift-check.yml`, `dependabot-auto-merge.yml`, and `sdlc-axiom-gate.yml`). LLM-invoking or untrusted-issue-triggered workflows do not run on this public repository.
