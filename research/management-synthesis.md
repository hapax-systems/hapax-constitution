# Management Methodology Synthesis & Automation Proposal

**Date:** 2026-03-03
**Sources:** An Elegant Puzzle (Larson), Scaling People (Johnson), Team Topologies (Skelton & Pais)
**Purpose:** Synthesize into coherent methodology, evaluate current system, propose maximum LLM automation

---

## Part 1: Synthesized Methodology

### Core Principle: Management as Infrastructure

All three books converge on a single insight: effective management is not ad-hoc intervention — it is deliberately designed infrastructure that creates velocity.

- **Larson** frames it as *systems engineering*: every management challenge is a system with stocks, flows, and feedback loops
- **Johnson** frames it as an *operating system*: repeatable, transferable structure shared across all teams
- **Skelton/Pais** frame it as *topology*: team structure, boundaries, and interaction modes that shape outcomes through Conway's Law

The hapaxromana system already embodies this — the entire agent architecture treats management as infrastructure. The gap is *coverage*, not *philosophy*.

### The Five Pillars

Across the three books, five distinct management concerns emerge. Each has a primary lens (which book owns the deepest treatment) and supporting lenses from the others.

#### Pillar 1: Team Health Assessment

**Primary:** Larson's Four States (falling behind → treading water → repaying debt → innovating)
**Supporting:** Skelton/Pais cognitive load classification, Johnson's talent portfolio

**The model:** Every team exists in one of four states. Each state has a specific, different intervention. You cannot skip states. The wrong intervention for the state makes things worse.

| State | Signals | Intervention | Cognitive Load Lens | Johnson Lens |
|-------|---------|-------------|-------------------|-------------|
| Falling behind | Backlog grows weekly, morale low | Add people | Extraneous load dominating | Low performers accumulating |
| Treading water | Critical work done, no debt paydown | Reduce WIP | Intrinsic load maxed | Steady middle neglected |
| Repaying debt | Debt paydown creates momentum | Add time | Load normalizing | High performers emerging |
| Innovating | Low debt, majority new value | Add slack | Germane load dominant | Portfolio healthy |

**Current system:** Not tracked. Person notes have `cognitive-load` field but no team-level state classification.

#### Pillar 2: Individual Development

**Primary:** Johnson's Explorer/Lecturer framework and hypothesis-based coaching
**Supporting:** Larson's career narratives, Skelton/Pais team-first context

**The model:** Coaching is hypothesis-driven observation over time. Feedback separates person from work. Career development follows narratives (3-5 year goals, gap analysis, focus areas), not ladders.

| Component | Source | Current State |
|-----------|--------|--------------|
| Coaching hypotheses | Johnson | Implemented (tpl-coaching-hypothesis, check-in tracking) |
| Feedback records | Johnson | Implemented (tpl-feedback-record, follow-up tracking) |
| Career narratives | Larson | **Gap**: person notes have growth-vector but no structured 3-5 year goals |
| Skill/will matrix | Johnson | **Gap**: not tracked |
| Working-with-me doc | Johnson | **Gap**: not implemented |
| Cognitive load observation | Skelton/Pais | Implemented (person note field, weekly review table) |

#### Pillar 3: Operating Cadence

**Primary:** Johnson's operating system (annual → quarterly → monthly → weekly → daily)
**Supporting:** Larson's sprint health criteria, Skelton/Pais DORA metrics

**The model:** Every management cadence has a specific purpose, owner, and expected output. Cadences nest: daily standup → weekly team meeting → biweekly 1:1 → quarterly review → annual planning.

| Cadence | Purpose | Current State |
|---------|---------|--------------|
| 1:1s | Relationship, coaching, decision support | Tracked (staleness, prep agent) |
| Team meetings | Update + decision-making | **Gap**: not tracked |
| Sprint health | 7 criteria for healthy sprints | **Gap**: not automated |
| Weekly review | Cognitive load, wins, risks | Template exists (tpl-weekly) |
| Quarterly review | Goal progress, course correction | Template exists (tpl-quarterly) |
| Decision logging | Track decisions, outcomes, precedents | Implemented (Bases dashboard) |

#### Pillar 4: Organizational Design

**Primary:** Skelton/Pais team types, interaction modes, fracture planes
**Supporting:** Larson's sizing rules (6-8 per team), Johnson's team charters

**The model:** Teams are the fundamental unit. Four types (stream-aligned, enabling, complicated-subsystem, platform). Three interaction modes (collaboration, X-as-a-Service, facilitating). Cognitive load is the primary constraint. Evolution triggers signal when topology must change.

| Component | Source | Current State |
|-----------|--------|--------------|
| Team type classification | Skelton/Pais | **Gap**: person notes have `team` but not team type |
| Interaction mode tracking | Skelton/Pais | **Gap**: not captured |
| Evolution trigger sensing | Skelton/Pais | **Gap**: weekly template has "Topology Signals" but no automation |
| Team sizing | Larson | **Gap**: no automated tracking |
| Team API documentation | Skelton/Pais | **Gap**: not implemented |

#### Pillar 5: Information Flow

**Primary:** Johnson's internal comms (3x rule, commit to docs, meeting notes shared)
**Supporting:** Larson's model/document/share, Skelton/Pais team API

**The model:** Important information is written down, stored centrally, communicated in multiple ways. Meeting notes are shared. Decisions are logged. Post-meeting action items are tracked to completion.

| Component | Source | Current State |
|-----------|--------|--------------|
| Meeting notes | Johnson | Template exists (1:1, ceremony) |
| Decision log | Johnson | Implemented (Bases dashboard) |
| Action item tracking | Johnson | **Gap**: manual in meeting notes, no aggregation |
| Team snippets | Larson | **Gap**: not implemented |
| Founding documents | Johnson | **Gap**: no team charters or mission docs tracked |

---

## Part 2: Current System Evaluation

### What's Working Well

1. **Coaching hypothesis lifecycle** — Full create → observe → check-in → resolve cycle with templates, staleness tracking, and nudges
2. **Feedback record lifecycle** — Direction, category, follow-up tracking with overdue nudges
3. **1:1 preparation** — management_prep agent synthesizes person state, recent meetings, coaching experiments, and energy signals
4. **Cognitive load from self-report** — Respects the axiom (mg-selfreport-001): reads frontmatter, doesn't infer
5. **Deterministic data collection** — management.py is zero-LLM, reducing cost and increasing reliability
6. **Management governance axiom** — "LLMs prepare, humans deliver" is correctly enforced

### What's Missing

Listed by impact (highest first):

| Gap | Impact | Books | Priority |
|-----|--------|-------|----------|
| No meeting transcript/notes auto-processing | Every meeting input is manual | All three | **Critical** |
| No calendar-driven preparation | Upcoming meetings not auto-prepared | Johnson, Larson | **Critical** |
| No post-meeting action item extraction | Action items die in notes | Johnson | **High** |
| No team state classification | Can't apply Larson's four-state interventions | Larson | **High** |
| No starter document generation | Every output requires manual creation | Johnson | **High** |
| No interaction mode tracking | Can't sense topology evolution | Skelton/Pais | **Medium** |
| No career narrative structure | Growth vector is single field, not 3-5 year plan | Larson, Johnson | **Medium** |
| No sprint/delivery health scoring | Can't measure sprint health against criteria | Larson | **Medium** |
| No quarterly time retro | No calendar data aggregation | Johnson, Larson | **Medium** |
| No team API documentation | Team boundaries implicit, not explicit | Skelton/Pais | **Low** |
| No working-with-me document | Operator hasn't captured own operating style | Johnson | **Low** |

---

## Part 3: Automation Proposals

### Design Principles

1. **Every input generates starter outputs** — Any information entering the vault should be automatically evaluated and any derivable documents generated
2. **Calendar is a trigger** — Upcoming meetings should automatically generate prep docs
3. **Post-event synthesis** — After every meeting, action items extracted and routed
4. **Continuous sensing** — Team health, topology, and cadence signals surfaced as nudges
5. **Respect the axiom** — LLMs prepare, humans deliver. No feedback language, no coaching recommendations, no suggestions about what to say

### Proposal 1: Meeting Lifecycle Automation

**The problem:** Meetings are the primary management interaction. Currently, the operator must manually prepare for each meeting (or run `management_prep --person`), manually take notes, and manually follow up on action items.

**The solution:** End-to-end meeting lifecycle automation driven by calendar events and vault notes.

#### 1a. Calendar-Driven Auto-Preparation

**Trigger:** Daily at 06:30 (before briefing), scan Obsidian calendar/daily note for today's meetings. Also scan vault for meeting notes with today's date.

**For each upcoming 1:1:**
- Run management_prep equivalent: aggregate person state, recent meetings, open coaching experiments, feedback follow-ups
- Generate a `tpl-1on1-prep` note in `10-work/meetings/` with pre-populated prep section
- Set `prep-generated: true` in frontmatter

**For each upcoming ceremony (standup, retro, planning):**
- Generate ceremony-specific prep: recent sprint data, open blockers from team members, relevant metrics
- Place in vault as `30-system/meeting-prep/YYYY-MM-DD-ceremony-name.md`

**For each skip-level or ad-hoc meeting:**
- Generate lightweight context brief: person's role, team, last interaction, any open items

**Implementation:**
- New agent: `meeting_lifecycle.py` with `--prepare` mode
- New systemd timer: `meeting-prep.timer` (daily 06:30)
- Calendar data source: Obsidian daily notes + calendar plugin data, or ICS file integration
- Output: vault_writer to `10-work/meetings/` and `30-system/meeting-prep/`

#### 1b. Post-Meeting Action Item Extraction

**Trigger:** When a meeting note in `10-work/meetings/` is modified (detected by RAG watchdog or a vault filesystem watcher).

**Process:**
1. Read the meeting note content
2. LLM extracts: action items (with assignee, due date), coaching observations, feedback delivered, decisions made, key topics discussed
3. Route extracted data:
   - Action items → append to person note "Open Tasks" or create Obsidian tasks
   - Coaching observations → if sufficient, generate a coaching hypothesis starter doc
   - Feedback delivered → generate a feedback record starter doc
   - Decisions made → generate a decision note starter doc
   - Topics/themes → tag and index for future 1:1 prep

**Implementation:**
- New mode on meeting_lifecycle agent: `--process-meeting <path>`
- Integrate with RAG watchdog (already watches vault) or add vault filesystem polling
- Output: starter docs in appropriate vault locations with `auto-generated: true` frontmatter

#### 1c. Meeting Transcript Ingestion

**Trigger:** Meeting transcript dropped into `31-system-inbox/` or `00-inbox/`

**Process:**
1. Detect file type (transcript from Teams, Zoom, Otter.ai, Google Meet, or raw text)
2. LLM processes transcript:
   - Identify participants and map to person notes
   - Extract structured data (action items, decisions, feedback moments, coaching observations)
   - Generate meeting summary
   - Create or update corresponding meeting note in `10-work/meetings/`
3. Route all extracted data as in 1b

**Implementation:**
- New parser in RAG pipeline or meeting_lifecycle agent
- Transcript format detection (common formats: VTT, SRT, plain text with speaker labels)
- Speaker → person note mapping via fuzzy name matching

### Proposal 2: Team Health Intelligence

**The problem:** Team health is currently tracked per-person (cognitive load, 1:1 staleness) but not per-team. Larson's four states framework and Skelton/Pais cognitive load classification are not automated.

**The solution:** Team-level health assessment that classifies teams into Larson's four states and monitors for Skelton/Pais evolution triggers.

#### 2a. Team State Classifier

**Data sources:**
- Person notes: cognitive load ratings, growth vectors, coaching activity
- Meeting notes: frequency and content of team meetings, standup participation
- Weekly reviews: team health ratings, velocity notes, blockers
- (If available) Jira/project tracker: backlog growth rate, WIP counts, feature vs maintenance ratio

**Classification logic:**
1. Aggregate per-team: avg cognitive load, stale 1:1 ratio, active coaching count, recent feedback volume
2. Proxy signals for four states:
   - Falling behind: high cognitive load (4+), growing backlog (if tracked), low morale mentions
   - Treading water: moderate load, no coaching activity, no growth vectors set
   - Repaying debt: decreasing load trend, active coaching, debt paydown mentions
   - Innovating: low load, growth vectors active, slack mentions
3. Output classification with confidence and evidence

**Implementation:**
- New collector: `cockpit/data/team_health.py` — aggregates person states into team-level assessment
- New fields on person template: `team-state` (derived, not self-reported)
- New nudge source: team state transitions
- Integrate with weekly review template

#### 2b. Topology Evolution Sensing

**Sensing patterns (from Team Topologies Section 10, Category C):**
- **Cognitive load drift**: Person absorbing new responsibilities without scope reduction
- **Interaction friction**: Frequent cross-team coordination where none should be needed
- **Cadence degradation**: 1:1s getting stale, meetings being skipped, feedback declining

**Implementation:**
- Extend management.py with team-level aggregation
- New sensing checks in health_monitor or as nudge sources
- Surface as "topology signal" nudges (medium priority)

### Proposal 3: Starter Document Generation

**The problem:** The books recommend many document types (decision docs, coaching hypotheses, feedback records, team charters, career narratives). Creating each one from scratch is high-friction, especially where task initiation is a binding constraint.

**The solution:** Whenever data suggests a document should exist, auto-generate a starter version. The operator edits, not creates.

#### 3a. Coaching Hypothesis Starters

**Trigger:** When a person's cognitive load increases (frontmatter change), when a pattern appears across multiple 1:1 notes (repeated themes), or when feedback delivery isn't followed up.

**Output:** A pre-populated `tpl-coaching-hypothesis` note with:
- `observation:` filled from the trigger data
- `hypothesis:` left blank (axiom: human generates hypotheses)
- `experiment:` left blank
- `success criteria:` left blank
- `person:` and `check-in-by:` auto-populated

#### 3b. Feedback Record Starters

**Trigger:** After a 1:1 where the "Feedback Delivered" section has content.

**Output:** A pre-populated `tpl-feedback-record` note linked to the person and meeting.

#### 3c. Decision Document Starters

**Trigger:** Meeting note contains a decision reference, or operator creates a decision log entry.

**Output:** A pre-populated decision note with context from the meeting.

#### 3d. Career Conversation Starters

**Trigger:** Person note exists for 3+ months without a career conversation recorded, or at quarterly cadence.

**Output:** A career conversation prep document per Larson's framework:
- Current role and tenure
- Growth vector (from person note)
- Strengths observed (from coaching/feedback history — aggregate only, no evaluation)
- Open coaching experiments
- Suggested structure: 3-5 year goal, gaps, 3-6 month focus

**Note:** This surfaces data. It does not suggest what the career goal should be or evaluate the person's trajectory. That's the operator's judgment.

### Proposal 4: Enhanced Weekly Review

**The problem:** The weekly review template has the right sections but they're all manual. The operator has to fill in team health, cognitive load table, topology signals, and wins/risks by hand.

**The solution:** Pre-populate the weekly review with data from the week's vault activity.

#### 4a. Auto-Populated Weekly Review

**Trigger:** Weekly (Sunday evening or Monday morning), generate a pre-populated weekly review.

**Data sources:**
- All meeting notes from the week
- All coaching/feedback activity from the week
- Person note changes (cognitive load updates, status changes)
- System data (briefings, health, drift from 30-system/)
- Action items created and completed this week

**Pre-populated sections:**
- **Team health:** Cognitive load table filled from person note frontmatter
- **Key outcomes:** Extracted from meeting notes and completed action items
- **Wins:** From meeting notes with positive signals
- **Risks/Issues:** From open/overdue items, high cognitive loads, stale 1:1s
- **Topology signals:** From sensing data (cross-team coordination, scope expansion)
- **Systems thinking prompts:** Recurring themes extracted from this week's meetings

The operator reviews, adjusts, and adds their own observations. Starter doc, not final product.

### Proposal 5: Person Note Enrichment

**The problem:** Person notes are created with a template but many fields stay empty. Career development tracking is minimal (single `growth-vector` field).

#### 5a. Extended Person Note Schema

Add fields to `tpl-person.md`:

```yaml
# Career narrative (Larson)
career-goal-3y:       # 3-year aspiration (operator captures)
current-gaps:         # Skill gaps toward goal
current-focus:        # 3-6 month focus areas
last-career-convo:    # Date of last dedicated career conversation

# Interaction context (Team Topologies)
team-type:            # stream-aligned | enabling | complicated-subsystem | platform
interaction-mode:     # collaboration | x-as-a-service | facilitating
interaction-with:     # Teams this person's team interacts with

# Johnson framework
skill-level:          # developing | career | advanced | expert
will-signal:          # high | moderate | low (operator self-report, not inferred)
agency-orientation:   # player | developing | (operator observes)
```

#### 5b. Person Note Staleness Sensing

**New nudge sources:**
- Career conversation overdue (no `last-career-convo` in 6 months)
- Growth vector stale (no update in 3 months)
- Missing context fields (no `team-type`, no `interaction-mode`)
- High cognitive load sustained (4+ for 3+ consecutive observations)

### Proposal 6: Sprint/Delivery Health Scoring

**The problem:** Larson's 7 sprint health criteria are not tracked. Without this, the operator can't systematically assess whether their teams' work processes are healthy.

#### 6a. Sprint Health Check

Based on Larson's 7 criteria:
1. Team knows what they should be working on
2. Team knows why their work is valuable
3. Team can determine if their work is complete
4. Team knows how to figure out what to work on next
5. Stakeholders can learn what the team is working on
6. Stakeholders can learn what the team plans to work on next
7. Stakeholders know how to influence the team's plans

**Implementation:** Periodic pulse check. Could be:
- A monthly survey (3 questions via Obsidian checklist or QuickAdd)
- A per-team frontmatter field (sprint-health: 5/7) updated by the operator
- Auto-scored from proxy data (meeting regularity, backlog visibility, stakeholder meetings)

For single-user, keep it simple: a field in the weekly review template that the operator rates per team.

---

## Part 4: Implementation Priority

### Phase 1: Calendar-Driven Prep (Highest Impact, Lowest Complexity)

**What:** Auto-generate 1:1 prep docs for all meetings today/tomorrow.
**Why:** This alone eliminates the most common friction point (forgetting to prepare, or spending initiation energy to prepare).
**Cost:** Extend management_prep agent with calendar scanning. New timer.
**Timeline:** Small — extend existing agent.

### Phase 2: Post-Meeting Processing (Highest Impact, Medium Complexity)

**What:** After meeting notes are written, extract action items, generate starter docs.
**Why:** This closes the loop from meeting → next actions. Without it, action items rot in meeting notes.
**Cost:** New processing mode on meeting_lifecycle agent. Integrate with vault watcher.
**Timeline:** Medium — new LLM processing mode.

### Phase 3: Meeting Transcript Ingestion (High Impact, Medium Complexity)

**What:** Drop a transcript, get a meeting note + extracted data.
**Why:** Eliminates manual note-taking or note transcription. Every meeting input auto-processed.
**Cost:** New transcript parser. LLM processing. Speaker mapping.
**Timeline:** Medium — new parser + LLM pipeline.

### Phase 4: Enhanced Weekly Review (Medium Impact, Low Complexity)

**What:** Pre-populate weekly review from week's vault data.
**Why:** Weekly review is the management cadence checkpoint. Making it effortless means it happens.
**Cost:** Extend existing collectors. New vault_writer mode.
**Timeline:** Small — mostly data aggregation.

### Phase 5: Team Health Intelligence (Medium Impact, Medium Complexity)

**What:** Team state classification, topology sensing, sprint health.
**Why:** Moves from individual-level tracking to team-level intelligence.
**Cost:** New collector and aggregation logic. New nudge sources.
**Timeline:** Medium — new data models and sensing logic.

### Phase 6: Person Note Enrichment (Lower Impact, Low Complexity)

**What:** Extended person note schema, new nudge sources for staleness.
**Why:** Richer data enables better prep and sensing.
**Cost:** Template update, new nudge sources, minor collector updates.
**Timeline:** Small — template and nudge additions.

---

## Part 5: Architecture Implications

### New Agent: `meeting_lifecycle.py`

The central new capability. Three modes:

```bash
# Auto-prepare all meetings for today
uv run python -m agents.meeting_lifecycle --prepare

# Process a meeting note after it's been written
uv run python -m agents.meeting_lifecycle --process 10-work/meetings/2026-03-03-alice-1on1.md

# Ingest a meeting transcript
uv run python -m agents.meeting_lifecycle --transcript 31-system-inbox/standup-2026-03-03.vtt
```

**Relationship to management_prep:** meeting_lifecycle subsumes the `--person` prep capability (it calls the same data collection) but adds calendar awareness and post-meeting processing. management_prep can remain for ad-hoc use.

### New Timer: `meeting-prep.timer`

Daily at 06:30 (before digest at 06:45 and briefing at 07:00):

```
[Timer]
OnCalendar=*-*-* 06:30:00
```

Runs `meeting_lifecycle --prepare`. Prep docs appear in vault before the daily briefing.

### New Collector: `cockpit/data/team_health.py`

Aggregates PersonState into TeamState. Classifies per Larson's four states. Feeds into:
- Nudges (team state transitions)
- Weekly review pre-population
- Team snapshot enrichment

### Vault Structure Additions

```
10-work/meetings/          Existing — meeting notes
30-system/meeting-prep/    New — auto-generated prep docs
30-system/weekly-reviews/  New — pre-populated weekly reviews
```

### Data Flow

```
Calendar / Daily Note
    ↓ (06:30 timer)
meeting_lifecycle --prepare
    ↓
Vault: 30-system/meeting-prep/ or 10-work/meetings/
    ↓ (during day, operator takes meeting, writes notes)
Meeting note modified
    ↓ (vault watcher detects)
meeting_lifecycle --process
    ↓
Routing: action items → person notes
         coaching observations → coaching hypothesis starters
         feedback records → feedback starters
         decisions → decision starters
    ↓
Nudges updated with new open items
```

### Axiom Compliance

All proposals respect management_governance axiom:

| Proposal | Axiom Check |
|----------|------------|
| Calendar-driven prep | Signal aggregation only — mg-prep-001 compliant |
| Post-meeting extraction | Extracts data, doesn't evaluate people — mg-boundary-001 compliant |
| Transcript ingestion | Summarizes, doesn't generate feedback — mg-boundary-002 compliant |
| Team health classification | Deterministic from data, no LLM inference of cognitive load — mg-selfreport-001 compliant |
| Starter doc generation | Pre-populates structure and data, leaves judgment fields blank — mg-boundary-001/002 compliant |
| Weekly review population | Aggregates vault data, doesn't evaluate team members — mg-prep-001 compliant |

### Executive Function Alignment

All proposals reduce initiation friction (executive_function axiom):

| Proposal | EF Benefit |
|----------|-----------|
| Calendar-driven prep | Zero-initiation: prep appears automatically |
| Post-meeting extraction | Zero-initiation: follow-ups routed automatically |
| Transcript ingestion | Low-initiation: drop file, get structured output |
| Starter doc generation | Low-initiation: edit existing doc, not create from scratch |
| Weekly review population | Low-initiation: review and adjust, not build from scratch |
| Person note enrichment | Nudges surface gaps — attention directed, not required to remember |

---

## Part 6: What Stays Human

Per the management_governance axiom and the books' own guidance:

| Activity | Why Human |
|----------|----------|
| Having the 1:1 conversation | Relationship, trust, reading the room |
| Delivering feedback | Tone, timing, emotional calibration |
| Coaching hypothesis generation | Requires direct observation and judgment |
| Career narrative co-creation | Deeply personal, collaborative |
| Team state intervention decisions | Organizational politics, stakeholder management |
| Topology evolution decisions | Strategic, multi-team impact |
| Performance evaluation | High-stakes human judgment |
| Difficult conversations | Emotional intelligence, courage |
| Skip-level trust building | Personal presence |
| Decision-making on people | The entire point of management |

The system prepares everything. The human delivers everything.
