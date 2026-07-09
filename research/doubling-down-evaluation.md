# Should We Double Down on What Nobody Else Does?

Evaluation of hapaxromana's 5 unique differentiators. For each: what it actually is today, whether it's genuinely valuable, whether to double down, and what that would look like.

---

## 1. Axiom-Driven Governance with T0 Blocking Violations

### What it actually is

Far more sophisticated than the comparable-projects report suggested. This is a 7-layer enforcement system:

- **Layer 1** (Static injection): Axiom text in CLAUDE.md and agent system prompts
- **Layer 2** (Health checks): 4 deterministic checks every 15 minutes
- **Layer 3** (Derivation): LLM generates concrete implications from axiom text (68+ implications across 4 axioms)
- **Layer 4** (Drift detector): Weekly codebase scan — 15 regex patterns + LLM semantic audit across 6 repos
- **Layer 5** (Agent tools): `check_axiom_compliance()` and `record_axiom_decision()` registered on all agents
- **Layer 6** (Operator review): Cockpit precedent review with promote/reject
- **Layer 7** (Precedent database): Qdrant collection with authority hierarchy (operator > agent > derived)
- **Hook**: PreToolUse blocks Write/Edit if content matches T0 patterns (multi-user code, feedback language)
- **Audit trail**: PostToolUse logs every file modification to JSONL

Plus interpretive canon (textualist, purposivist, absurdity, omitted-case) and a supremacy clause for constitutional vs domain axiom conflicts.

*Note: while writing this document, the PreToolUse hook fired a false positive on a prose example discussing prohibited patterns. This demonstrates the enforcement is active — but also that the regex patterns don't distinguish code from prose. Worth noting for the "sharpen hooks" recommendation below.*

### Is it genuinely valuable?

**Yes, but with an important caveat.**

The value isn't in preventing you from accidentally writing prohibited class names — that's the least interesting layer. The real value is in three things:

1. **Decision coherence over time.** The precedent database means an architectural decision made 6 months ago informs today's decision. Without this, you'd re-litigate the same tradeoffs constantly. Where working memory and attention are binding constraints, this is enormous — it externalizes the "wait, didn't we already decide this?" function.

2. **Executive function protection.** The executive_function axiom's sufficiency requirements (zero-config agents, errors with next actions, recurring tasks automated) actively push the system toward low cognitive load. Without enforcement, entropy would erode these properties over time.

3. **Preventing scope creep.** The single_user axiom blocks the most common source of accidental complexity in software: building for hypothetical users. Every "just in case" permission check is complexity that serves nobody.

**The caveat:** 7 layers is a lot of machinery. The marginal value of layers 3 (derivation), 6 (operator review), and 7 (precedent DB) over layers 1 (static docs), 4 (drift detector), and the PreToolUse hook is unclear. Are you actually reviewing precedents in the cockpit? If not, layers 5-7 are dead weight.

### Should you double down?

**Selectively yes.** Double down on the layers that fire automatically and protect executive function. Don't invest more in layers that require operator attention (which is exactly the resource the system is designed to conserve).

### What doubling down looks like

- **Sharpen the PreToolUse hook.** Highest-value enforcement point — fires on every write, costs nothing, prevents violations before they happen. Current improvements: distinguish code from prose/comments (the false positive on this document is a concrete example). Expand patterns to cover executive_function violations (e.g., agent code that requires manual config files, error messages without remediation steps).
- **Make drift detector findings more actionable.** Currently reports violations in a DriftReport. Could it auto-generate fix suggestions? Or send a notification with the specific file + line + fix?
- **Don't invest more in the precedent database** unless you're actively using cockpit review. If you are, great — it's a unique and powerful pattern. If not, it's architectural beauty that serves no one.
- **Surface pending axiom work as a nudge.** A SessionStart hook that says "you have 3 pending axiom precedents to review" would convert a pull-based workflow (check cockpit) to a push-based one (aligned with executive_function axiom).

### What doubling down does NOT look like

- More axioms. Four is the right number. Each additional axiom multiplies enforcement complexity.
- More implications. 68+ is already comprehensive. Diminishing returns.
- Runtime MCP enforcement a la arifOS. Your PreToolUse hook already does this more simply.

---

## 2. Operator Profile as Structured Context

### What it actually is

Genuinely industrial-grade. 16 source types (config files, shell history, git commits, Langfuse traces, Google Takeout, Proton Mail, Obsidian vault, interview transcripts). Dual-path extraction (LLM + deterministic bridges). 24 profile dimensions. 2.2MB profile in `ryan.json`. Authority-aware fact merging (interview > config > observation). Intention-practice gap detection. On-demand context tools for agents (`search_profile()`, `lookup_constraints()`). Updates every 6 hours via systemd timer.

The fact merge logic is particularly sophisticated: if you SAY you prefer X (config/interview) but DO Y (langfuse/shell history), the system flags it as a gap rather than overwriting — classifying it as executive_function (wants to but can't initiate), knowledge, context_dependent, or preference_shift.

### Is it genuinely valuable?

**Yes, and it's the most underappreciated differentiator.**

Every agent in the system knows who you are — not generically, but specifically. Your neurocognitive patterns, your energy cycles, your communication style, your decision patterns. This means:

- The briefing agent knows what time of day you're most receptive
- The management_prep agent knows your leadership style and what context you need before 1:1s
- The research agent knows your knowledge domains and can calibrate depth
- The health_monitor's enriched notifications can be phrased in ways that match your communication preferences

No other project does this. agent-second-brain has a flat `about.md`. COG has an onboarding interview. Neither has 24 dimensions with authority-aware fact merging, intention-practice gap detection, or semantic search over the profile.

**The question is whether agents actually use it well.** The context tools exist. But are agents calling `search_profile()` in practice, or just using the static system prompt fragment? If the latter, the sophisticated profile infrastructure is overbuilt for its actual consumption pattern.

### Should you double down?

**Yes — but on consumption, not extraction.**

The extraction pipeline is mature. 16 sources, dual-path, incremental updates every 6 hours. This doesn't need more work.

What needs work is making agents USE the profile more effectively.

### What doubling down looks like

- **Audit agent profile consumption.** Which agents actually call `search_profile()` or `lookup_constraints()` during execution? Check Langfuse traces for tool-call patterns. If most agents just use the static 400-word system prompt fragment, the on-demand tools are underutilized.
- **Profile-informed agent behavior, not just prompts.** Could the briefing agent adjust its output format based on `neurocognitive_profile.energy_cycles`? Could the health_monitor adjust notification priority based on time-of-day energy patterns?
- **Intention-practice gap as a first-class feature.** The gap detection is brilliant but currently just flags contradictions during curation. These gaps are exactly the executive_function signals that should surface as nudges. "You keep saying you want to do X but your behavior shows you don't — here's a low-friction way to start."
- **Profile digest in the daily briefing.** The digest exists (28KB) but does the briefing agent reference it? A "profile health" section (dimensions with low confidence, stale facts, intention-practice gaps) could be part of the morning briefing.

### What doubling down does NOT look like

- More source types. 16 is comprehensive.
- More dimensions. 24 (13 canonical + 11 discovered) is already broad.
- More frequent updates. Every 6 hours is fine.
- A profile UI. The cockpit already has profile routes.

---

## 3. Three-Tier Architecture with Systemd Autonomy

### What it actually is

Clean, well-separated, and working:
- **Tier 1** (Interactive): Claude Code + Cockpit web + LLM hotkeys
- **Tier 2** (On-demand): 13 Python agents, invoked via `uv run python -m agents.<name>`
- **Tier 3** (Autonomous): 10 systemd user timers, all active, all reliable, using watchdog wrapper scripts

No cross-tier violations. Agents import functions from each other (library pattern) but never invoke each other as processes. Timers are Persistent=true with randomized delay. All firing reliably.

### Is it genuinely valuable?

**The tier separation itself: yes. The implementation as standalone Python agents: also yes.**

The comparable-projects research surfaced projects (agent-second-brain, COG, linuz90) that accomplish similar outcomes using Claude Code skills. Initial analysis suggested some hapaxromana agents could migrate to skills. **This analysis was wrong** — it assumed Claude Code is the primary interface. It isn't.

Claude Code is one of several Tier 1 surfaces (alongside Cockpit web, CLI hotkeys, Open WebUI). Tier 2 agents are called by systemd timers, by the Cockpit API, by direct CLI invocation, and by Claude Code. A Claude Code skill only exists inside a Claude Code session — it can't be called by a timer, a web API, or any other surface.

This means standalone agents with a stable invocation interface (`uv run python -m agents.<name>`) are the correct implementation for virtually the entire roster. They are surface-independent: any caller that can run a shell command can use them.

**Additional advantages of standalone agents over skills:**
- Run without human presence (Tier 3 timers)
- Access Qdrant programmatically with precise queries
- Run deterministic checks with no LLM needed (health_monitor, introspect, knowledge_maint)
- Execute complex multi-step pipelines with structured Pydantic output
- Run cheaply on claude-haiku rather than requiring opus-level models
- Traced individually in Langfuse (per-agent cost and performance tracking)
- Testable (1524 pytest tests provide regression safety)

The maintenance cost (~10,000+ lines of Python) is real, but it's the cost of surface independence. The comparable projects that use skills instead have accepted a hard dependency on Claude Code as their sole runtime — fine for a personal note-taking system, not fine for an infrastructure that runs 24/7 on timers.

### Should you double down?

**Yes. The implementation is correct for the architecture.**

### What doubling down looks like

- **Keep the tier model and the agent implementation.** Both are the right choice given the multi-surface architecture.
- **Invest in agent quality over agent quantity.** Don't add agent #14 unless it genuinely needs to be surface-independent. If something only makes sense inside Claude Code (e.g., a one-off research task), a skill or direct interaction is fine.
- **Reduce per-agent maintenance cost** where possible: shared infrastructure (context tools, axiom tools, operator prompt) already does this well. Keep pushing toward agents as thin wrappers around shared libraries + a system prompt + tool registrations.
- **Consider whether any agents are underused.** If an agent hasn't been invoked (manually or by timer) in 30+ days, it's either unnecessary or its schedule needs adjustment. Langfuse traces could surface this.

### What doubling down does NOT look like

- Migrating agents to Claude Code skills. Skills are session-bound; agents must be surface-independent.
- Adding an orchestration layer. The flat topology is a feature, not a limitation.
- Making agents invoke each other as processes. The current function-import pattern is correct.

---

## 4. Cross-Boundary Operation (corporate_boundary axiom)

### What it actually is

The Obsidian plugin runs on an employer-managed device. It must use only employer-sanctioned LLM providers (Anthropic, OpenAI), sync data only via Obsidian Sync (E2E encrypted), degrade gracefully when home services are unreachable, and store API credentials in plugin data.json.

### Is it genuinely valuable?

**Valuable for you, but not a differentiator worth investing in.**

This is a constraint, not a capability. It exists because of your specific employment situation. It's well-handled by the corporate_boundary axiom and its T0 implications. The Obsidian plugin already respects it.

### Should you double down?

**No.** Maintain the axiom. Enforce via existing drift-detector. Don't invest engineering effort unless something breaks. If your employment situation changes, this axiom can be softcoded out.

---

## 5. Observability Mandate (Langfuse tracing)

### What it actually is

All LLM calls route through LiteLLM at :4000, which traces to Langfuse at :3000. Every agent call, every model selection, every token count is logged. The activity_analyzer reads traces to build usage patterns. The profiler reads traces for behavioral patterns.

### Is it genuinely valuable?

**Yes, but it's table stakes for production systems — not a unique differentiator.**

The unique part is that traces feed back into the operator profile and activity analysis — but that's differentiator #2, not #5.

### Should you double down?

**Maintain, don't invest.** The current setup works. LiteLLM + Langfuse is mature and well-supported.

One low-effort addition worth considering: **cost tracking in the daily briefing** ("you spent $X on LLM calls this week, 60% was briefing agent"). Langfuse already has this data.

---

## Summary Matrix

| Differentiator | Maturity | Genuine Value | Double Down? | Priority |
|---|---|---|---|---|
| 1. Axiom governance | Very high (7 layers) | High — decision coherence + scope control | Selectively — sharpen auto-enforcement | Medium |
| 2. Operator profile | Very high (16 sources, 24 dims) | Highest — unique, underexploited | Yes — improve consumption, surface gaps | **High** |
| 3. Three-tier architecture | High (clean, reliable) | High — model + implementation both correct | Yes — invest in agent quality, reduce per-agent cost | Medium |
| 4. Corporate boundary | Adequate | Constraint, not capability | No — maintain only | Low |
| 5. Observability mandate | High (LiteLLM + Langfuse) | Medium — table stakes | Maintain — add cost tracking | Low |

## Recommendation

**The operator profile (#2) is the highest-priority investment.** It's the most unique differentiator, the most aligned with the executive_function axiom, and the most underexploited. The extraction infrastructure is mature and impressive; the consumption side needs attention. Making agents actually adapt their behavior based on the profile — not just mention it in their prompts — would be genuinely novel.

**The axiom governance (#1) is mature and working.** Sharpen the PreToolUse hook (distinguish code from prose — this doc triggered a false positive). Make drift findings more actionable. Don't add more layers.

**The three-tier model AND its implementation (#3) are correct.** Claude Code skills are session-bound — they can't be called by timers, the Cockpit API, or any other surface. Since agents must be surface-independent, standalone Python with a stable CLI interface is the right implementation. Invest in agent quality and reducing per-agent maintenance cost (shared libraries, thin wrappers), not in migrating to skills.

**The other two (#4, #5) are maintenance-mode.** They work. Don't touch them.
