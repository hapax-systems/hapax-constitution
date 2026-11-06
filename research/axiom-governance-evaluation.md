# Axiom / Constitutional Governance: Design Choice Evaluation

> **[2026-11 Architectural Supersession Note]:** This early-2026 note documents a pre-hardening baseline (such as prompt-level "trusted agent" assumptions, dormant Layer 5-7 audit hooks, or single-family deliberation prototypes). Those baselines were superseded in the Hapax Research Lab architecture by unprivileged structural confinement (`reins` + container/microVM execution boundaries and `hapax-spine` append-only receipt ledgers) and live heterogeneous multi-family cross-examination published at [https://hapaxresearch.com](https://hapaxresearch.com). Retained for historical design lineage.

Research conducted 2026-03-05. Evaluates the hapaxromana axiom system as a design choice by comparing it against the emerging academic literature, production frameworks, and comparable personal projects.

---

## What the Hapaxromana System Actually Does

The system enforces 4 axioms (single_user, executive_function, management_governance, corporate_boundary) through a 7-layer stack:

| Layer | Mechanism | When | Enforcement |
|-------|-----------|------|-------------|
| 1. Static injection | Axiom text in CLAUDE.md + agent system prompts | Every session/invocation | Passive — LLM reads but can ignore |
| 2. Health checks | 15 sufficiency probes (deterministic) | Every 15 min | Active — flags gaps, doesn't block |
| 3. Derivation | LLM generates concrete implications | On demand | Interpretive — expands axiom surface |
| 4. Drift detector | Weekly regex + LLM semantic audit across repos | Weekly | Retroactive — finds violations post-hoc |
| 5. Agent tools | `check_axiom_compliance()`, `record_axiom_decision()` | During agent runs | On-demand — agent must choose to call |
| 6. Operator review | Cockpit precedent review | Manual | Pull-based — requires operator attention |
| 7. Precedent database | Qdrant with authority hierarchy | On decision lookup | Reference — informs future decisions |
| Hook | PreToolUse regex scan blocks Write/Edit | Every file write | **Blocking** — prevents violation pre-commit |
| Audit | PostToolUse logs file modifications | Every file write | Passive — observability only |

The system also has an interpretive canon (textualist, purposivist, absurdity, omitted-case) and a supremacy clause for constitutional vs domain axiom conflicts.

---

## The Research Landscape (2022-2026)

The axiom system was built largely in isolation. Since then, a body of research has converged on remarkably similar problems and solutions. Here's what exists:

### 1. Anthropic's Constitutional AI (2022)

**Paper:** Bai et al., "Constitutional AI: Harmlessness from AI Feedback" (arXiv:2212.08073)

**What it is:** A training-time technique. The model is given a "constitution" (a list of principles), generates self-critiques of its own outputs against those principles, revises them, then is fine-tuned on the revised outputs. A second phase uses RL from AI Feedback (RLAIF) — the model evaluates paired responses against the constitution and a preference model is trained on those evaluations.

**Key insight:** The constitution is baked into model weights through training. It doesn't enforce anything at runtime — it shapes the distribution of outputs.

**Comparison to hapaxromana:** Fundamentally different mechanism. Anthropic's CAI operates at training time on model weights. Hapaxromana's axioms operate at deployment time on a specific model instance. CAI produces a generally-aligned model; hapaxromana's axioms produce a specifically-constrained system. CAI is about what the model *tends to do*; axioms are about what *this system must not do*.

**What this means:** The approaches are complementary, not competing. Claude already has CAI in its weights. The axiom system adds deployment-specific constraints that no training process could anticipate (single_user, corporate_boundary, management_governance are all deeply personal).

### 2. Agent Behavioral Contracts (ABC) — February 2026

**Paper:** arXiv:2602.22302

**What it is:** Extends Bertrand Meyer's Design by Contract to AI agents. A contract C = (P, I, G, R) specifies Preconditions, Invariants, Governance policies, and Recovery mechanisms. Implemented as AgentAssert, a runtime enforcement library. Evaluated on 200 scenarios across 7 models.

**Key results:**
- Contracted agents detect 5.2-6.8 soft violations per session that uncontracted baselines miss entirely
- Hard constraint compliance: 88-100%
- Recovery rates: 100% for frontier models
- Establishes the **Drift Bounds Theorem**: with recovery rate γ > natural drift rate α, behavioral drift is bounded to D* = α/γ

**Comparison to hapaxromana:** ABC is the closest academic analog to the axiom system. Both specify invariants that must hold across an agent's execution. Key differences:

| Dimension | ABC | Hapaxromana |
|-----------|-----|-------------|
| Specification | Formal contract language | Natural language axioms + regex patterns |
| Enforcement | Runtime library (AgentAssert) | PreToolUse hook + drift detector |
| Recovery | Formal recovery mechanisms (R) | No explicit recovery — block or flag |
| Scope | Per-session contracts | System-wide permanent axioms |
| Violations | Hard vs soft distinction | T0 (blocking) vs T1 (warning) |
| Mathematical guarantees | Drift Bounds Theorem | None |

**What this means:** The axiom system intuitively arrived at the same architectural pattern that ABC formalizes. The main gap is that hapaxromana lacks formal recovery mechanisms — when a violation is detected, it blocks but doesn't help the agent recover. ABC's recovery rate concept (γ > α ensures bounded drift) is a useful framework for thinking about whether the system actually *converges* toward compliance or just *detects* violations.

### 3. Policy Compiler for Secure Agentic Systems (PCAS) — February 2026

**Paper:** arXiv:2602.16708

**What it is:** A compiler that takes an existing agent implementation + a policy specification (in a Datalog-derived language) and produces an instrumented system that is policy-compliant by construction. A reference monitor intercepts all actions and blocks violations before execution.

**Key results:** Improves policy compliance from 48% to 93% across frontier models, with zero policy violations in instrumented runs.

**Comparison to hapaxromana:** PCAS's reference monitor is architecturally identical to the PreToolUse hook — both intercept actions before execution and block on violation. The key difference is that PCAS models system state as a dependency graph (tracking causal relationships across tool calls), while the axiom hook is stateless — it checks each write independently with no memory of prior actions.

**What this means:** The axiom hook is a correct but minimal implementation of the reference monitor pattern. The statelessness is both a strength (simple, no failure modes from stale state) and a limitation (can't detect violations that span multiple actions, like "the agent wrote a config file and then a code file that together constitute multi-user scaffolding").

### 4. Governance-as-a-Service (GaaS) — August 2025

**Paper:** arXiv:2508.18765

**What it is:** A modular, policy-driven enforcement layer that sits outside agent architectures. Operates at runtime without modifying model internals. Uses a Trust Factor that scores agents based on compliance and severity-weighted violations. Supports coercive (block), normative (guide), and adaptive (dynamic trust) interventions.

**Comparison to hapaxromana:** GaaS is designed for multi-agent ecosystems where agents may be untrusted or adversarial. Hapaxromana's single-user axiom makes this unnecessary — all agents are authored by the operator and run in a trusted environment. The Trust Factor concept is interesting but irrelevant here: there's no concept of an agent becoming "less trusted" over time.

**What this means:** GaaS solves the wrong problem for this system. Multi-agent trust scoring adds complexity without value in a single-operator context. However, the graduated enforcement model (coercive → normative → adaptive) maps onto the existing T0/T1 distinction and suggests a possible T2 level: advisory constraints that inform but don't flag.

### 5. ArbiterOS / "From Craft to Constitution" — October 2025

**Paper:** arXiv:2510.13857

**What it is:** A governance-first paradigm that treats the LLM as a "Probabilistic CPU" and builds an OS-level kernel (ArbiterOS) around it. The Agent Constitution Framework (ACF) has 5 operational cores: Cognitive (reasoning), Memory (context), Execution (tools), Normative (rules), and Metacognitive (self-evaluation). Every instruction passes through a non-bypassable "Arbiter Loop" for validation.

**Key argument:** Current frameworks (OpenAI's AgentKit, Microsoft's Agent Framework) treat governance as "a configurable feature of the application's logic, placing the burden on the developer." ArbiterOS makes governance non-bypassable by placing it in the OS kernel, ensuring "the governor is separate from the governed."

**Comparison to hapaxromana:** This is the most philosophically aligned with the axiom system. Both argue that governance should be architectural, not application-level. The Claude Code hook mechanism achieves the "non-bypassable" property for file writes — the hook fires before the write tool executes, and the agent cannot bypass it. ArbiterOS's 5-core decomposition is more comprehensive but also more complex.

| Principle | ArbiterOS | Hapaxromana |
|-----------|-----------|-------------|
| Governor ≠ governed | Kernel-level separation | Hook-level separation |
| Non-bypassable | Arbiter Loop intercepts all instructions | PreToolUse intercepts all writes |
| Audit trail | Flight Recorder | PostToolUse JSONL logging |
| Progressive adoption | 3 stages (audit → resilience → robustness) | Organically evolved (hooks → probes → drift) |

**What this means:** The axiom system accidentally implemented the core ArbiterOS principle (governor separated from governed via non-bypassable enforcement) using Claude Code's hook mechanism. The main architectural gap is that hooks only intercept *file writes*, not *all agent actions*. An agent could violate axioms through tool calls that don't involve writing (e.g., sending a notification with feedback language, or making an API call that assumes multi-user context).

### 6. NVIDIA NeMo Guardrails

**What it is:** An open-source Python library for adding programmable guardrails to LLM conversations. Uses an event-driven runtime that intercepts inputs and outputs, applying configurable safety checks. Supports topic control, PII detection, RAG grounding, and jailbreak prevention.

**Comparison to hapaxromana:** NeMo Guardrails is designed for conversational AI products serving many users. It solves content safety and topic drift — problems that don't exist in a single-user system. The event-driven architecture is cleaner than the hook-based approach, but it requires the application to be built around the guardrails framework. The axiom system's hook-based approach is more retrofittable — it wraps an existing tool (Claude Code) without modifying it.

### 7. arifOS

**GitHub:** ariffazil/arifOS

**What it is:** A "constitutional metabolizer" that enforces 13 "immutable floors" before any AI output ships. Uses an MCP-based runtime with a three-stage governance pipeline (Ignition → Mind/Heart/Soul). Claims mathematical provability and cryptographic auditability.

**Comparison to hapaxromana:** arifOS is more ambitious in scope (13 floors vs 4 axioms, claims mathematical provability) but much less mature in implementation. The axiom system has 15 deterministic probes, a working PreToolUse hook, weekly drift detection, and 150+ tests. arifOS has 34 GitHub stars and ambitious documentation. The approaches share the "constitutional" metaphor but diverge sharply in engineering rigor.

---

## Design Pattern Analysis

Across all these systems, a taxonomy of enforcement strategies emerges:

### Enforcement Timing

| Strategy | When | Examples |
|----------|------|---------|
| Training-time | Model weights | Anthropic CAI, RLHF |
| Design-time | Architecture docs, specifications | Hapax Layer 1 (CLAUDE.md), Layer 3 (derivation) |
| Build-time | Code analysis, compilation | PCAS policy compiler, hapax Layer 4 (drift detector) |
| Runtime pre-action | Before execution | Hapax PreToolUse hook, PCAS reference monitor, ArbiterOS Arbiter Loop, NeMo input rails |
| Runtime post-action | After execution | Hapax PostToolUse audit, ABC violation detection, NeMo output rails |
| Periodic audit | Scheduled | Hapax drift detector (weekly), sufficiency probes (15-min) |

**Hapaxromana covers 5 of 6 timing categories** (all except training-time, which requires model access). This is more comprehensive than any single research system, which typically focuses on one or two categories.

### Enforcement Strength

| Level | Mechanism | Hapax equivalent |
|-------|-----------|------------------|
| Informational | Context injection, documentation | Layer 1 (CLAUDE.md), Layer 5 (agent tools) |
| Advisory | Warnings, suggestions | T1 implications, sufficiency probe failures |
| Blocking | Prevent action from executing | T0 PreToolUse hook (exit 2) |
| Corrective | Fix violation and proceed | **Gap — no auto-correction** |
| Adaptive | Adjust trust/behavior dynamically | **Gap — no trust scoring** |

### Statefulness

| Approach | State model | Hapax equivalent |
|----------|-------------|------------------|
| Stateless per-action | Check each action independently | PreToolUse hook (regex per write) |
| Session-stateful | Track within one execution | **Gap — hooks are stateless** |
| Cross-session persistent | Track across time | Precedent database (Layer 7), drift detector history |

---

## Evaluation: What the Axiom System Gets Right

### 1. The constitutional metaphor is validated by research

The "From Craft to Constitution" paper (2025) independently argues for exactly this paradigm: treating agent governance as constitutional law rather than application logic. The axiom system arrived at this independently and earlier. The interpretive canon (textualist, purposivist, absurdity, omitted-case) and supremacy clause are genuine innovations that no research system has — they address how to *interpret* axioms when cases are ambiguous, which is a real problem that formal contract languages don't solve.

### 2. Governor-governed separation via hooks is architecturally sound

The PreToolUse hook achieves the same "non-bypassable enforcement" that ArbiterOS's Arbiter Loop provides, using a simpler mechanism (shell script + exit code). The agent cannot bypass the hook because it's enforced by the Claude Code runtime, not by the agent's own code. This is the correct architectural pattern — the literature confirms it.

### 3. Multi-layer defense-in-depth is correct

No single enforcement mechanism is sufficient. Training (CAI) shapes tendencies but can't prevent specific violations. Runtime blocking (hooks) catches pattern matches but misses semantic violations. Periodic audits (drift detector) catch what runtime checks miss. The axiom system's 7 layers map onto a defense-in-depth strategy that the literature increasingly advocates.

### 4. Domain-specific axioms are genuinely novel

No research system has axioms like `single_user` or `executive_function`. These are deeply personal constraints that no general framework could provide. The research focuses on general safety properties (harm prevention, policy compliance). The axiom system adds *architectural* constraints (no multi-user code) and *cognitive* constraints (reduce decision load). This combination is unique.

### 5. Sufficiency probes are a novel inversion

Most systems check for *violations* — things the system should NOT do. The sufficiency probes check for *sufficiency* — things the system MUST do (agents must have zero-config, errors must have remediation, recurring tasks must be automated). This is the contract-theory distinction between "obligations" and "prohibitions." ABC formalizes this as invariants, but hapaxromana's probes are more concrete and deterministic.

---

## Evaluation: What the Axiom System Gets Wrong (or Could Improve)

### 1. No formal recovery mechanisms

ABC's key insight is that detection without recovery is insufficient. The axiom system blocks violations (PreToolUse exit 2) but gives the agent no structured path to recover. The error message says "this is prohibited" but doesn't say "here's how to accomplish what you were trying to do within the axioms." ABC's recovery rate concept (γ > α) suggests that a system with high detection but low recovery just frustrates the agent into finding workarounds.

**Concrete improvement:** When the PreToolUse hook blocks, it could suggest an axiom-compliant alternative. For `single_user` violations, this is often "just remove the auth/permission code." For `management_governance` violations, it's "aggregate the data but don't generate the language."

### 2. Stateless enforcement misses multi-action violations

PCAS's dependency graph insight is important: some violations only become visible across multiple actions. The PreToolUse hook checks each file write independently. An agent could write a config file that assumes multi-user context, then write code that reads from it — neither write individually matches a regex pattern, but together they constitute a violation.

**Concrete improvement:** A lightweight session-level accumulator in the PostToolUse hook that tracks files written in the current session and periodically runs a semantic check across them. Not every session — just when the accumulated writes exceed some threshold.

### 3. Regex patterns are the weakest enforcement layer

The literature consistently shows that pattern matching catches syntactic violations but misses semantic ones. A class named `AccessController` doesn't match `class Auth(Manager|Service|Handler)` but might still be multi-user scaffolding. The drift detector's LLM semantic audit catches these, but only weekly.

**Concrete improvement:** This is the right tradeoff for now. Regex is fast, deterministic, and zero-cost. The LLM semantic audit is expensive and slow. The current architecture (fast regex blocks obvious violations, slow LLM catches subtle ones) is a valid two-speed enforcement design. The main improvement would be running the semantic audit more frequently on high-change-velocity repos.

### 4. Layers 5-7 may not justify their complexity

The earlier doubling-down evaluation flagged this: agent tools (Layer 5), operator review (Layer 6), and the precedent database (Layer 7) require operator attention, which is the resource the system is designed to conserve. The research supports this concern — ArbiterOS explicitly argues for progressive governance adoption (audit → resilience → robustness) rather than deploying all layers at once. GaaS's adaptive enforcement mode suggests that some constraints should only activate when violations are detected, not preemptively.

**Concrete improvement:** Instrument Layers 5-7 for usage. If `check_axiom_compliance()` is never called (as the Langfuse data suggested), and cockpit precedent review hasn't been used in 30+ days, these layers should be marked as dormant rather than maintained.

### 5. No coverage of non-write actions

The PreToolUse hook only fires on Write and Edit tools. Agent actions through Bash, MCP tools, or API calls are uncovered. An agent could `curl` an external service in a way that violates `corporate_boundary`, or `git push` code that violates `single_user`, without triggering the hook. The axiom-commit-scan partially addresses git operations, but other tools remain unguarded.

**Concrete improvement:** Add pattern matching to the Bash PreToolUse hook for high-risk commands (e.g., `curl` to non-localhost URLs when the corporate_boundary axiom applies). Don't try to cover everything — focus on the highest-risk tool/axiom combinations.

---

## Summary Assessment

The axiom system is a well-engineered instance of a design pattern that the research community is just beginning to formalize. It predates the key papers (ABC, PCAS, ArbiterOS all published 2025-2026) and independently arrived at many of the same architectural principles:

- Governor separated from governed (ArbiterOS's core principle)
- Non-bypassable pre-action enforcement (PCAS's reference monitor)
- Formal specification of behavioral invariants (ABC's contracts)
- Multi-layer defense-in-depth (common across all frameworks)
- Domain-specific constraints (unique to hapaxromana)

The main gaps relative to the literature are:

1. **No formal recovery mechanisms** (ABC's key contribution)
2. **Stateless per-action enforcement** (PCAS's dependency graph solves this)
3. **Pull-based upper layers** that contradict the executive_function axiom
4. **Incomplete action coverage** (only file writes, not all tool calls)

None of these gaps are urgent. The system works, catches real violations (the false positive on this project's plan document proves enforcement is active), and the architecture is extensible enough to address these gaps incrementally. The 4-axiom count is right — the research confirms that constitutional systems with fewer, more fundamental principles outperform those with many specific rules.

**Bottom line:** The axiom system is a strong design choice that the literature validates. It should be maintained and sharpened (as Phase 2 of the improvement plan does), not expanded or replaced. The main investment should be in making the existing layers more effective (recovery hints, inline comment handling, non-write tool coverage) rather than adding new layers.

---

## Sources

- [Constitutional AI: Harmlessness from AI Feedback — Anthropic (2022)](https://arxiv.org/abs/2212.08073)
- [Agent Behavioral Contracts: Formal Specification and Runtime Enforcement (2026)](https://arxiv.org/abs/2602.22302)
- [Policy Compiler for Secure Agentic Systems (2026)](https://arxiv.org/abs/2602.16708)
- [Governance-as-a-Service: Multi-Agent Compliance and Policy Enforcement (2025)](https://arxiv.org/abs/2508.18765)
- [From Craft to Constitution: A Governance-First Paradigm for Principled Agent Engineering (2025)](https://arxiv.org/abs/2510.13857)
- [NVIDIA NeMo Guardrails](https://developer.nvidia.com/nemo-guardrails)
- [arifOS — GitHub](https://github.com/ariffazil/arifOS)
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks)
- [Agentic AI Governance Frameworks 2026](https://certmage.com/agentic-ai-governance-frameworks/)
- [Public Constitutional AI — Georgia Law Review](https://digitalcommons.law.uga.edu/glr/vol59/iss2/5/)
- [Weights & Biases: Guardrails for AI Agents](https://wandb.ai/site/articles/guardrails-for-ai-agents/)
- [Agent Contracts: A Formal Framework for Resource-Bounded Autonomous AI Systems (2026)](https://arxiv.org/abs/2601.08815)
