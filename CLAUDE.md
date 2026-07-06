# CLAUDE.md

Governance architecture for LLM agent systems — constitutional axioms, derived implications, interpretive canon, sufficiency probes, and precedent store. **Specification repo**: YAML definitions and markdown documentation, not application code.

Shared conventions (uv, ruff, testing, git workflow) are in the workspace `CLAUDE.md` — this file covers constitution-specific details only.

**Consumers of this spec:** [`hapax-council`](https://github.com/hapax-systems/hapax-council) (extends the constitutional axiom set with single_user, executive_function, etc.) and [`hapax-officium`](https://github.com/hapax-systems/hapax-officium) (extends with management_safety, management_governance) both depend on this repo via the published `hapax-sdlc` package. Changes to `axioms/registry.yaml` here propagate to both consumers on next dependency bump.

## Key Files

- **`axioms/registry.yaml`** — Canonical axiom definitions (IDs, weights, scope, text)
- **`axioms/implications/`** — Per-axiom derived implications with tier (T0/T1/T2), enforcement mode, sufficiency levels
- **`domains/`** — Domain-scoped axiom extensions (infrastructure, management)
- **`knowledge/`** — Sufficiency probes per domain (management, music, personal, technical)
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
yamllint axioms/ domains/ knowledge/  # YAML lint (if yamllint installed)
```

CI runs YAML linting automatically via `yaml-lint.yml` workflow.

## SDLC Pipeline

Spec-focused: no implement workflow. Triage → Review → Axiom Gate (structural only) → Auto-merge. Changes touching `axioms/registry.yaml` always classified as L complexity. Scripts in `scripts/`, workflows in `.github/workflows/`.

> Subject to the workspace CLAUDE.md rotation policy: `hapax-council/docs/superpowers/specs/2026-04-13-claude-md-excellence-design.md`.
