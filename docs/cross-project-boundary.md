# Cross-Project Boundary: Hapax System ↔ Logos

This document defines the relationship between the wider hapax system and the
containerized logos system. It must be byte-identical in both repos:

- `~/projects/hapaxromana/docs/cross-project-boundary.md`
- `~/projects/hapax-officium/docs/cross-project-boundary.md`

Any divergence is a high-severity drift item detected by the wider system's
drift-detector agent (weekly Sunday 03:00).

## Project Identities

**Wider Hapax System** (`hapaxromana` + `ai-agents`): A personal executive
function platform for a single operator. Covers all domains — management,
personal knowledge, health monitoring, audio capture, content sync, creative
production. 28+ agents across sync, RAG, analysis, and automation.

**Logos** (`hapax-officium`): A management-only decision
support system extracted from the wider system in March 2026. Purpose-built
for team leadership — 1:1 prep, coaching tracking, management self-awareness
profiling, actionable nudges. 15 agents, all management-scoped. Safety
principle: LLMs prepare, humans deliver.

## Shared Lineage

Both projects share the same origin codebase. The logos system was
extracted via a deliberate conversion that:

- Removed 22 agents outside management scope
- Renamed 5 agents for management clarity
- Added 1 management-specific agent (management_activity)
- Regrounded axioms from single-operator cognitive-ergonomics context to management decision theory
- Removed all single-operator personal context (executive-function offloading, single-operator ergonomics patterns)
- Rewrote the demo pipeline for management-only content

The extraction is documented in:
- `hapax-officium/docs/plans/2026-03-06-management-conversion-design.md`
- `hapax-officium/docs/plans/2026-03-06-management-conversion-plan.md`

## Axiom Correspondence

hapax-officium's axioms are a fork-with-rename of the wider system's axioms.
Same constitutional principles, different grounding language.

| Wider System (hapaxromana) | hapax-officium | Weight | Notes |
|---------------------------|------------------|--------|-------|
| single_operator | single_operator | 100 | Same semantics, role-generic language |
| decision_support | decision_support | 95 | Regrounded: single-operator cognitive ergonomics → decision-support theory |
| management_safety | management_safety | 95 | Elevated: domain axiom → constitutional scope |
| corporate_boundary | corporate_boundary | 90 | Unchanged, dormant in both |

All T0 blocking implications are preserved. Only the grounding text differs.

## Agent Roster Divergence

### Present in both (identical or renamed)

| Wider System | hapax-officium | Change |
|-------------|------------------|--------|
| management_prep | management_prep | Identical |
| meeting_lifecycle | meeting_lifecycle | Identical |
| briefing | management_briefing | Renamed, management-focused |
| profiler | management_profiler | Renamed, 13 → 6 dimensions |
| demo | demo | Ported with adaptation |
| health_monitor | system_check | Rewritten: 75 checks → 4, no auto-fix |
| digest | digest | Ported |
| scout | scout | Ported |
| drift_detector | drift_detector | Ported |
| knowledge_maint | knowledge_maint | Ported |
| introspect | introspect | Ported |
| ingest | ingest | Ported |

### Only in hapax-officium

| Agent | Purpose |
|-------|---------|
| management_activity | Management practice metrics from management data (no LLM) |
| status_update | Upward-facing status reports from management data |
| review_prep | Performance review evidence aggregation |

### Only in wider system (removed from hapax-officium)

Sync agents (7): gdrive_sync, gcalendar_sync, gmail_sync, youtube_sync,
chrome_sync, claude_code_sync, obsidian_sync.

Analysis agents (3): research, code_review, activity_analyzer.

Audio agents (3): audio_processor, hapax_daimonion, audio_recorder (systemd).

Other (3): query, profiler_sources, demo_eval.

## Shared Modules

18 modules in `shared/` exist in both repos. hapax-officium is a strict
subset — it has no unique shared modules.

Key shared modules: config.py, operator.py, profile_store.py,
management_bridge.py, notify.py, vault_writer.py, axiom_*.py,
context_tools.py, langfuse_client.py, langfuse_config.py.

The wider system has 18 additional shared modules not present in
hapax-officium (google_auth.py, calendar_context.py, health_*.py,
capacity.py, dimensions.py, email_utils.py, service_*.py, etc.).

## Infrastructure (Isolated)

Each system runs its own infrastructure stack. No shared services, databases,
collections, or traces.

| Service | Wider System | Logos |
|---------|-------------|-------------------|
| Qdrant | localhost:6333 | localhost:6433 |
| LiteLLM | localhost:4000 | localhost:4100 |
| Langfuse | localhost:3000 | localhost:3100 |
| PostgreSQL | localhost:5432 | localhost:5532 |
| Ollama | localhost:11434 | localhost:11434 (shared — single GPU) |

Ollama is the one shared service — stateless inference with auto-managed
model loading. Both stacks point at the same instance. Not a data store.

## Isolation Status

Infrastructure isolation completed March 2026. Each system has its own
Qdrant collections, LiteLLM proxy, Langfuse traces, and PostgreSQL databases.
Ollama remains shared (single GPU constraint, stateless inference).

Data source isolation in progress — the logos system's vault dependency
has been excised. VS Code + Qdrant integration is the planned replacement.

## Boundary Rules

Changes in one repo that may affect the other:

- **Shared module APIs**: Function signatures and class interfaces in shared/
  modules used by both repos. A breaking change in one breaks the other.
- **Axiom semantics**: Redefining what a constitutional axiom means affects
  both systems' governance.
- **Qdrant collection schemas**: Field names, vector dimensions, payload
  structure changes affect both readers.
- **Vault structure**: Path changes in data/ that
  management_bridge.py reads.
- **Profile dimensions**: The 6 management dimensions in profile_store.py
  are used by both systems' profilers.
- **Operator manifest**: operator.json structure changes affect both
  operator.py implementations.
