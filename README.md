# hapax-constitution

Governance specification for a research project implementing Clark & Brennan's (1991) conversational grounding theory in a production voice AI system, evaluated via Single Case Experimental Design (SCED) with Bayesian analysis. See [hapax-council](https://github.com/hapax-systems/hapax-council) for the primary research artifact and experiment design.

## Role in the workspace

This repository is a specification, not application code. YAML files define the constitutional axiom set; markdown describes the architecture. The `hapax-sdlc` package (published from this repo) provides enforcement tooling that consumers run.

Two consumers extend the spec via the published package:

| Consumer | Domain extensions | Package |
|---------|-------------------|---------|
| [hapax-council](https://github.com/hapax-systems/hapax-council) | `single_user`, `executive_function`, `corporate_boundary`, `interpersonal_transparency`, `management_governance` | `hapax-sdlc` |
| [hapax-officium](https://github.com/hapax-systems/hapax-officium) | `single_operator`, `decision_support`, `management_safety` | `hapax-sdlc[demo]` |

Changes to `axioms/registry.yaml` propagate to both consumers on the next dependency bump.

## Governance architecture

The architecture follows constitutional law in structure: weighted axioms, derived implications at graduated enforcement tiers, interpretive canons for unanticipated cases, and a precedent store for accumulated rulings.

### Axioms and implications

Axioms are weighted constraints defined in `axioms/registry.yaml`. Each axiom produces derived implications.

| Axiom | Weight | Core constraint |
|-------|--------|-----------------|
| `single_user` | 100 | One operator. No auth, no roles, no multi-user features. |
| `executive_function` | 95 | Compensates for executive-function challenges. Zero-config agents, actionable errors, automated routines. |
| `corporate_boundary` | 90 | Work data stays in employer systems. Graceful degradation across network boundaries. |
| `interpersonal_transparency` | 88 | No persistent state about non-operator persons without an active consent contract. |
| `management_governance` | 85 | LLMs prepare context; humans deliver words. No generated feedback language or coaching recommendations about individuals. |

~90 implications across four enforcement tiers: T0 (block at commit), T1 (require review), T2 (warn), T3 (lint). Tier graduation follows the logic of levels of scrutiny in constitutional law. Each implication carries an enforcement mode (`compatibility`, `blocking`, `monitoring`) and applies at one of three levels (capability, subsystem, operator).

### Interpretive canons

Four canons handle unanticipated cases:

| Canon | Use |
|-------|-----|
| `textualist` | Literal axiom text, strict application; primary canon for T0 blocks |
| `purposivist` | Axiom intent, contextual reasoning when literal reading is too narrow |
| `absurdity` | Reject literal applications producing absurd results |
| `omitted-case` | Apply nearest precedent; escalate when no precedent exists |

### Precedent store

Operator rulings on edge cases are recorded under `axioms/precedents/` with situation, reasoning, resolution, and scope. Precedents carry authority weights (operator 1.0, agent 0.7, derived 0.5) and are append-only with supersession tracking. Future evaluations query the precedent store semantically (Qdrant) before escalating.

### Sufficiency probes

Implications carry a mode: prohibition (must not do) or sufficiency (must do). The enforcement engine runs both. The `executive_function` axiom requires that every error message contains a concrete next action; a system that never generates feedback language but also never includes next actions passes prohibition checks while failing sufficiency.

### Deliberative process (Publius/Brutus)

For contentious governance events — supremacy tensions, dissent thresholds (3+ dissents), new implications, weight changes, precedent supersession, canon challenges — the deliberation pipeline runs two opposed agents (Publius and Brutus) and produces a structured deliberation record (YAML) with both arguments, supporting precedents, and proposed resolution. The operator decides; neither agent decides. Spec: [`docs/design/deliberative-governance.md`](docs/design/deliberative-governance.md).

## Structural patterns

Two patterns are specified alongside axiom governance:

**Filesystem-as-bus.** Coordination state as markdown files with YAML frontmatter on disk. No message broker, no database, no RPC. Trades transactional consistency for human-readable state, git-native history, and tool-agnostic interoperability. At single-operator scale, the consistency trade-off has no practical cost. Independently described by "From Everything-is-a-File to Files-Are-All-You-Need" (arXiv:2601.11672) and "Everything is Context" (arXiv:2512.05470).

**Three-tier agent architecture.** Tier 1 (interactive: Claude Code, dashboards), Tier 2 (on-demand: pydantic-ai agents), Tier 3 (autonomous: systemd timers). Agents communicate through filesystem artifacts; no orchestrator or workflow engine.

## Related work

Several independent formalizations of agent governance appeared in late 2025 and early 2026: ArbiterOS (arXiv:2510.13857), Agent Behavioral Contracts (arXiv:2602.22302), PCAS (arXiv:2602.16708), Governance-as-a-Service (arXiv:2508.18765). This architecture converges on similar structural conclusions and adds interpretive canons, sufficiency probes, and personal axioms (governance tailored to a specific operator's cognitive constraints).

Active research currents (`research/`):

| Document | Scope |
|----------|-------|
| [`research/landscape-analysis-2026.md`](research/landscape-analysis-2026.md) | Competitive landscape audit (Apple Intelligence, Google Gemini, CrewAI, Humane/Rabbit/Limitless collapse) |
| [`research/axiom-governance-evaluation.md`](research/axiom-governance-evaluation.md) | 7-layer enforcement stack mapped to ABC, PCAS, Constitutional AI, GaaS |
| [`research/axiom-gap-analysis.md`](research/axiom-gap-analysis.md) | Four concrete proposals: recovery hints, session accumulator, precedent weights, sufficiency probes |
| [`research/axiom-enforcement.md`](research/axiom-enforcement.md) | Layer 1–7 taxonomy with cost / coverage / strength matrix |

## Repo presentation pipeline

The `hapax-sdlc` package (published from `sdlc/` and `hapax_sdlc/` shim) renders public metadata artifacts for first-party registry repos:

| Artifact | Render mode | Source |
|----------|-------------|--------|
| `CITATION.cff` | Full overwrite | `sdlc/render/citation_cff.py` |
| `codemeta.json` | Full overwrite | `sdlc/render/codemeta_json.py` |
| `.zenodo.json` | Full overwrite | `sdlc/render/zenodo_json.py` |
| `NOTICE.md` | Full overwrite | `sdlc/render/notice_md.py` |
| `CONTRIBUTING.md` | Full overwrite | `sdlc/render/contributing_md.py` |
| `SECURITY.md` | Full overwrite | `sdlc/render/security_md.py` |
| `GOVERNANCE.md` | Full overwrite | `sdlc/render/governance_md.py` |
| `README.md` preamble | Section replacement between `<!-- hapax-sdlc:preamble:begin/end -->` markers | `sdlc/render/readme_section.py` |

The README preamble preserves the per-repo body. The `OperatorReferentPicker` selects one of four equally-weighted non-formal referents (`The Operator`, `Oudepode`, `Oudepode The Operator`, `OTO`) per artifact deterministically from the repo id.

### CLI

```bash
python -m hapax_sdlc.render --all                  # Render all 7 first-party repos
python -m hapax_sdlc.render --repo hapax-council   # Render one repo
python -m hapax_sdlc.render --all --check          # Drift mode; exit 1 on diff (CI)
python -m hapax_sdlc.render --all --dry-run        # Print to stdout
python -m hapax_sdlc.render --repo X --file CITATION.cff  # Render one artifact
```

The render entrypoint is defined in `sdlc/render/cli.py`. Operator identity is loaded from `sdlc/operator.yaml` (or `sdlc/operator.local.yaml` if present, gitignored).

## CI

| Workflow | Trigger | Effect |
|----------|---------|--------|
| `yaml-lint.yml` | push main, PR | yamllint over `axioms/`, `domains/`, `knowledge/`; consistency checks E-1 (sufficiency), E-2 (capability coverage), E-3 (deontic conflicts) |
| `repo-settings-drift-check.yml` | cron 13:37 UTC, manual dispatch | Detects drift in GitHub Settings (`has_wiki`, `has_projects`, `has_discussions`) across 7 first-party repos via `python -m sdlc.render.repo_settings --check`. Requires `HAPAX_CROSS_REPO_PAT` (fine-grained, Metadata read-only on siblings); no-ops with a warning if unset. |
| `claude-review.yml` | PR open / sync | Claude Code review of axiom weight consistency, implication tier validity, cross-reference integrity, precedent quality |
| `sdlc-triage.yml` | issue labeled `agent-eligible` | Classify type and complexity (XS/S/M/L); reject L-complexity or missing context; dispatch to plan |
| `sdlc-implement.yml` | dispatch / PR review changes_requested on `agent/*` | LLM agent edits YAML, implications, precedents, docs; runs yamllint + pytest |
| `sdlc-review.yml` | PR open / sync on `agent/*` (agent-authored label) | Adversarial review (3 rounds, then needs-human label) |
| `sdlc-axiom-gate.yml` | PR review approved on `agent/*` | Axiom compliance gate; auto-merge on pass |
| `auto-fix.yml` | CI failure on non-main branch | Auto-fix attempts (3-attempt circuit breaker) |
| `dependabot-auto-merge.yml` | Dependabot PR | Auto-merge minor/patch bumps |

Pre-commit: `ruff` + `yamllint` (relaxed mode).

## Local validation

```bash
uv sync
uv run ruff check .
uv run ruff format --check .
yamllint -d relaxed axioms/ domains/ knowledge/
python sdlc/consistency_check.py --json --check-resolutions   # E-3 deontic consistency
uv run pytest                                                 # 27 assertions in tests/test_render.py
```

## Contents

| Path | Contents |
|------|----------|
| [`axioms/registry.yaml`](axioms/registry.yaml) | Axiom definitions (5 axioms, weights, scopes) |
| [`axioms/implications/`](axioms/implications/) | Derived implications per axiom (~90 total) |
| [`axioms/precedents/`](axioms/precedents/) | Precedent seeds (8 files) |
| [`knowledge/`](knowledge/) | Sufficiency probes per domain (management, music, personal, technical) |
| [`research/`](research/) | Governance research (axiom evaluation, gap analysis, landscape analysis) |
| [`pattern-guide.md`](pattern-guide.md) | Architectural pattern with code examples |
| [`agent-architecture.md`](agent-architecture.md) | Three-tier agent system design |
| [`docs/design/deliberative-governance.md`](docs/design/deliberative-governance.md) | Publius/Brutus deliberation pipeline |
| [`docs/cross-project-boundary.md`](docs/cross-project-boundary.md) | Inter-repo boundary specification |
| [`sdlc/`](sdlc/) | SDLC enforcement + render tools (published as `hapax-sdlc`) |
| [`hapax_sdlc/`](hapax_sdlc/) | Re-export shim for the published package |
| [`demo/`](demo/) | Demo pipeline (audio, video, charts, slides, dossier renderers) |

CODEOWNERS protects `axioms/`, `domains/`, `knowledge/`, `.github/`. Operator review required for any change in those paths.

## Ecosystem

| Repository | Role |
|-----------|------|
| [hapax-council](https://github.com/hapax-systems/hapax-council) | Primary research artifact — voice daemon, grounding system, experiment infrastructure |
| **hapax-constitution** (this repo) | Governance specification — axioms, implications, canons, precedents |
| [hapax-officium](https://github.com/hapax-systems/hapax-officium) | Supporting software — management decision support |
| [hapax-watch](https://github.com/hapax-systems/hapax-watch) | Wear OS biometric companion |
| [hapax-phone](https://github.com/hapax-systems/hapax-phone) | Android health + context companion |
| [hapax-mcp](https://github.com/hapax-systems/hapax-mcp) | MCP server bridging the logos APIs to Claude Code |

## Citation

If you cite this specification, see the [CITATION.cff](CITATION.cff) file (rendered).

## License

License posture is split by surface:

- `hapax-sdlc` package/tooling code: Apache 2.0 — see [LICENSE](LICENSE).
- Specification, citation, and publication metadata: CC BY-NC-ND 4.0, as declared in
  [NOTICE.md](NOTICE.md), [CITATION.cff](CITATION.cff), `.zenodo.json`, and `codemeta.json`.

Do not describe the whole repository as simply "Apache-licensed" or "open source" in public
copy; distinguish runnable tooling from specification/publication material.
