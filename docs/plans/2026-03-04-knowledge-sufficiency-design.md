# Knowledge Sufficiency Engine — Design

**Date:** 2026-03-04
**Status:** Approved
**Repos affected:** `hapaxromana`, `ai-agents`, `obsidian-hapax`

## Problem

The management system infrastructure exists (person templates, nudge sources, prep agents, team health classification, Larson states) but the vault is empty. The system silently degrades when data is missing — it can detect "stale 1:1" but not "you have no person notes at all." Missing cadence means a person never triggers a nudge. Missing cognitive-load makes a person invisible to team health. The system assumes absence means "fine" when it actually means "unknown."

There is no mechanism to:
1. Know what data the system needs to function (derived from Team Topologies, Scaling People, An Elegant Puzzle)
2. Detect that required data is missing
3. Proactively acquire missing data from the operator
4. Prioritize acquisition (critical-path data first)

## Approach: Knowledge Sufficiency Engine

A YAML knowledge model defines what the system should know. A deterministic audit scans vault state against the model and produces a prioritized gap list. The Obsidian plugin conducts guided interviews to acquire missing data, writing vault notes directly via the Obsidian API. Interview state persists across sessions.

## Knowledge Model

Lives at `hapaxromana/knowledge/management-sufficiency.yaml`. Each requirement has:

```yaml
- id: direct-reports
  category: foundational       # foundational | structural | enrichment
  description: >
    Person notes for all direct reports with type, role, team, status.
    Every management feature depends on these existing.
  source: "All 3 books"
  check:
    type: min_count             # file_exists | min_count | field_populated | field_coverage | any_content
    path: "10-work/people"
    filter: { type: person, status: active }
    min: 1
  acquisition:
    method: interview           # interview | nudge | external
    question: >
      Let's set up your team. Who are your direct reports?
      For each person, I need their name, role, and which team they're on.
    extraction_schema:
      type: array
      items: { name: string, role: string, team: string }
    output: person_note         # person_note | reference_doc | frontmatter_update
  priority: 100
  depends_on: []
```

### Categories and Requirements

**Foundational (priority 90-100 in nudge system)** — system is non-functional without these:

| ID | Description | Source | Check | Acquisition |
|---|---|---|---|---|
| `direct-reports` | Person notes for all direct reports | All 3 | `min_count >= 1` on `10-work/people/*.md` | Interview: list names, roles, teams |
| `team-assignment` | Every person note has `team` field | TT | `field_populated: team` on all active people | Interview: "What team is [name] on?" |
| `1on1-cadence` | Every person note has `cadence` set | SP, EP | `field_populated: cadence` | Interview: "How often do you meet with [name]?" |
| `manager-context` | Operator's manager is documented | SP | `file_exists` or person note with manager role | Interview: "Who is your manager?" |
| `company-mission` | Company mission documented | SP | `file_exists: 10-work/references/company-mission.md` | Interview: "What's your company's mission?" |

**Structural (priority 60 in nudge system)** — major features degrade:

| ID | Description | Source | Check |
|---|---|---|---|
| `operating-principles` | Company/team values documented | SP | `file_exists: 10-work/references/operating-principles.md` |
| `org-structure` | Org hierarchy documented (spans, reporting) | EP | `file_exists: 10-work/references/org-chart.md` |
| `team-topology-type` | Team type set for each team | TT | `field_coverage >= 80%: team-type` |
| `team-interaction-modes` | Interaction modes between team pairs | TT | `file_exists: 10-work/references/team-interactions.md` |
| `operating-cadence` | Meeting cadences documented | SP | `file_exists: 10-work/references/operating-cadence.md` |
| `meeting-ceremonies` | At least one meeting note per ceremony type | All 3 | `min_count >= 1` on `10-work/meetings/*.md` |
| `key-stakeholders` | Person notes for non-report stakeholders | SP | `min_count >= 1` with non-direct-report filter |
| `decision-approach` | Decision framework documented | SP | `file_exists: 10-work/references/decision-framework.md` |
| `team-charters` | Per-team mission and scope | SP | `file_exists: 10-work/references/team-charters.md` |
| `team-sizing` | Team sizes documented and in range | EP | Derived from person count per team (6-8 target) |

**Enrichment (priority 35 in nudge system)** — improves output quality:

| ID | Description | Source | Check |
|---|---|---|---|
| `career-goals` | Person notes have `career-goal-3y` | SP, EP | `field_coverage >= 50%` |
| `skill-will` | Person notes have `skill-level` + `will-signal` | SP | `field_coverage >= 50%` |
| `cognitive-load` | Person notes have numeric `cognitive-load` | TT, EP | `field_coverage >= 80%` |
| `coaching-hypotheses` | Active coaching docs for coaching-active people | SP | coaching notes exist for `coaching-active: true` people |
| `working-with-me` | Operator management style doc | SP | `file_exists: 10-work/references/working-with-me.md` |
| `feedback-style` | Per-person feedback preferences | SP | `field_coverage >= 50%: feedback-style` |
| `growth-vectors` | Per-person development areas | EP | `field_coverage >= 50%: growth-vector` |
| `cross-team-deps` | Cross-team interaction patterns | TT | `file_exists: 10-work/references/cross-team-deps.md` |
| `notable-individuals` | Skip-levels, executives, key collaborators | SP | Person notes with non-direct-report roles |
| `team-api` | Team boundaries and interfaces | TT | `file_exists: 10-work/references/team-api.md` |
| `evolution-triggers` | Topology change signals | TT | Reference doc or team-state tracking |
| `performance-framework` | Career ladder, performance designations | SP, EP | `file_exists: 10-work/references/career-ladder.md` |

**External Data (not interview-acquirable):**

| ID | Description | Source | Check |
|---|---|---|---|
| `dora-metrics` | Deployment frequency, MTTR, lead time, change failure | EP | Interview: "Do you track DORA metrics? Where?" |
| `backlog-health` | WIP count, backlog growth rate | EP | Interview: "What project management tool do you use?" |
| `sprint-velocity` | Team throughput trends | EP | Derived from project tool data |

## Sufficiency Audit

**Module:** `cockpit/data/knowledge_sufficiency.py`

Zero LLM. Reads knowledge model, scans vault, produces gap list.

```python
@dataclass
class KnowledgeGap:
    requirement_id: str
    category: str           # foundational | structural | enrichment
    priority: int           # nudge priority (90, 60, or 35)
    description: str
    acquisition_method: str # interview | nudge | external
    interview_question: str | None
    depends_on: list[str]
    satisfied: bool

@dataclass
class SufficiencyReport:
    gaps: list[KnowledgeGap]
    total_requirements: int
    satisfied_count: int
    foundational_complete: bool
    structural_complete: bool
    sufficiency_score: float  # 0.0 - 1.0
```

**Check implementations:**

| Type | Logic |
|---|---|
| `file_exists` | `Path(vault / path).exists()` and file has >50 chars body |
| `min_count` | Glob path, parse frontmatter, apply filter, count >= min |
| `field_populated` | All matching notes have non-empty field value |
| `field_coverage` | >= threshold% of matching notes have non-empty field |
| `any_content` | File exists with substantive content |

**Nudge integration:** New source in `cockpit/data/nudges.py`:

```python
def _collect_sufficiency_nudges(report: SufficiencyReport) -> list[Nudge]:
    nudges = []
    for gap in report.gaps:
        if gap.satisfied:
            continue
        # Check dependencies
        if any(dep not in satisfied_ids for dep in gap.depends_on):
            continue
        nudges.append(Nudge(
            source="knowledge-sufficiency",
            priority=gap.priority,  # 90, 60, or 35
            urgency="high" if gap.category == "foundational" else "medium" if gap.category == "structural" else "low",
            text=f"Missing: {gap.description}",
            action=f"/setup {gap.requirement_id}" if gap.acquisition_method == "interview" else f"Create {gap.description}",
        ))
    return nudges
```

**Scheduling:** Runs in cockpit 5-minute slow refresh cycle. Also runs on-demand when interview system checks progress.

## Interview Engine (Obsidian Plugin)

**New files in `obsidian-hapax/src/interview/`:**

### `engine.ts` — State Machine

```typescript
interface InterviewState {
    active: boolean;
    current_requirement: string | null;
    completed: string[];      // requirement IDs satisfied
    skipped: string[];        // user chose to skip
    pending: string[];        // remaining gaps in priority order
    last_updated: string;     // ISO timestamp
}
```

State persists in `data.json` (syncs across an institutional compartment boundary).

Interview flow:
1. Load knowledge model (bundled as JSON in plugin build)
2. Run local sufficiency check (scan vault via Obsidian API)
3. Sort unsatisfied requirements by priority (foundational first, then by dependency order)
4. Present next question in chat
5. Send answer to LLM with extraction prompt
6. Write extracted data to vault
7. Re-check requirement, mark satisfied if met
8. Show progress, advance to next gap

### `questions.ts` — Question Templates

Each requirement has a question template with:
- Conversational question text (not form-like)
- Follow-up prompts if answer is incomplete
- Extraction schema (JSON format for LLM to produce)
- Output type: `person_note`, `reference_doc`, `frontmatter_update`

### `extractor.ts` — LLM Structured Extraction

Sends user answer + extraction prompt to current provider. Extraction prompt:

```
Extract structured data from this answer. The user was asked: [question].
Return valid JSON matching this schema: [schema].
Only extract what was explicitly stated. Do not infer, guess, or add information.
If the answer is incomplete, return what you can and set "incomplete": true.
```

Respects mg-boundary-001/002 — LLM does structured extraction only, never generates management advice.

### `vault-writer.ts` — Note Creation

Uses Obsidian API (`app.vault.create`, `app.vault.modify`):
- `person_note`: Creates `10-work/people/{name}.md` with frontmatter from tpl-person schema
- `reference_doc`: Creates `10-work/references/{id}.md` with appropriate content
- `frontmatter_update`: Modifies existing note frontmatter via Obsidian's `processFrontMatter`

### UI Integration

- **Banner:** When foundational gaps exist, chat view shows a persistent banner: "Your management system needs setup data" with "Start Setup" button
- **Progress:** During interview, shows "Foundational: 3/5 | Structural: 2/10 | Enrichment: 0/12"
- **Slash command:** `/setup` starts or resumes interview. `/setup skip` skips current question. `/setup status` shows progress
- **Normal chat:** When interview is not active, chat works normally. Nudges for structural/enrichment gaps appear in the existing nudge display

### Corporate Boundary Compliance

- Works on both home (LiteLLM) and work (OpenAI/Anthropic) devices
- Vault writing via Obsidian API — no server dependency
- Knowledge model bundled in plugin build — no external fetch
- Interview state in data.json — syncs across an institutional compartment boundary

## Ongoing Maintenance

### Gap detection after bootstrap

1. **New hire detection:** Operator mentions unfamiliar name in chat → LLM notes it → optional nudge "Create person note for [name]?"
2. **Enrichment decay:** `field_coverage` checks have staleness component — `last-career-convo` >6 months generates enrichment nudge
3. **Org changes:** Manual trigger via `/setup refresh` re-runs full audit
4. **New requirements:** Adding entries to knowledge model YAML → next audit detects new gaps automatically

### Interview vs Nudge routing

- **>3 gaps in a category:** Offer interview mode
- **1-2 gaps:** Generate nudges only (operator fills via templates/QuickAdd)
- **Foundational gaps always route to interview** regardless of count

### Completeness signal

When all foundational requirements are met, system transitions from "bootstrapping" to "operational":
- Banner changes from "needs setup data" to normal nudge display
- One-time notification: "Management system is operational. All foundational data is in place."
- Structural and enrichment gaps continue as normal nudges

## File Changes

| File | Change |
|---|---|
| `hapaxromana/knowledge/management-sufficiency.yaml` | New — knowledge model |
| `ai-agents/cockpit/data/knowledge_sufficiency.py` | New — sufficiency audit |
| `ai-agents/cockpit/data/nudges.py` | Add sufficiency nudge source |
| `obsidian-hapax/src/interview/engine.ts` | New — interview state machine |
| `obsidian-hapax/src/interview/questions.ts` | New — question templates |
| `obsidian-hapax/src/interview/extractor.ts` | New — LLM extraction |
| `obsidian-hapax/src/interview/vault-writer.ts` | New — Obsidian API vault writing |
| `obsidian-hapax/src/chat-view.ts` | Interview banner, `/setup` command, progress display |
| `obsidian-hapax/src/slash-commands.ts` | Add `/setup` command |
| `obsidian-hapax/styles.css` | Interview UI styles |

## Axiom Compliance

| Axiom | Status |
|---|---|
| `single_user` | No multi-user anything |
| `executive_function` | Persistent interview state (stop/resume), one question at a time, progress visibility, completeness signal |
| `management_governance` | LLM does structured extraction only, never generates feedback/coaching language |
| `corporate_boundary` | Works on both devices via provider abstraction, no server dependency for vault writes |

## Methodology Sources

Knowledge model requirements derived from:
- **Team Topologies** (Skelton & Pais): team types, interaction modes, cognitive load, evolution triggers, fracture planes, team API
- **Scaling People** (Claire Hughes Johnson): founding documents, operating cadence, skill/will matrix, explorer feedback, hypothesis coaching, career conversations, working-with-me, decision frameworks
- **An Elegant Puzzle** (Will Larson): four team states, career narratives, team sizing, systems thinking, DORA metrics, migration playbook, sprint health criteria
