# Comparable Projects to hapaxromana

Research conducted 2026-03-05. Projects grouped by which dimension of hapaxromana they most closely match.

## How to read this

hapaxromana is unusual because it spans several categories simultaneously:
- **Specification layer** (axioms, governance, architecture docs — not runnable code)
- **Personal multi-agent infrastructure** (13 agents, 3 tiers, systemd timers)
- **Self-hosted AI stack** (Docker services, LiteLLM routing, Langfuse observability)
- **Executive function prosthetic** (automation and cognitive offloading optimized for executive-function support)
- **Personal knowledge management** (RAG pipeline, Obsidian plugin, vector DB)

No single project covers all of these. The closest matches are composites.

---

## Tier 1: Closest Architectural Matches

### agent-second-brain (smixs)
**GitHub:** smixs/agent-second-brain | **License:** MIT | **Stars:** ~new (2025-2026)

The single most structurally similar project found. A Claude Code-powered personal assistant that:
- Uses a vault structure (goals, projects, CRM, reflections) with `.claude/skills/`
- Has MEMORY.md for persistent agent context across sessions
- Runs daily 3-phase processing: Capture → Execute → Reflect
- Integrates Telegram (voice input via Deepgram), Todoist, Obsidian
- Pipeline: `Telegram → Deepgram → Claude Code → Todoist + Obsidian vault → Telegram report`

**What hapaxromana can learn:**
- The daily capture→execute→reflect cycle is elegant and maps well to the briefing agent pattern
- Using Claude Code skills as the agent runtime (instead of custom Python) is radically simpler
- The `MEMORY.md` pattern for cross-session persistence is exactly what hapaxromana already does
- Voice capture → structured output pipeline is more mature than our faster-whisper script

**Key differences:**
- No governance/axiom layer
- No observability (no Langfuse equivalent)
- Single agent (Claude Code) rather than multiple specialized agents
- No local model support — fully dependent on Anthropic API
- No hardware/GPU integration

### COG (huytieu/COG-second-brain)
**GitHub:** huytieu/COG-second-brain | **License:** MIT | **Stars:** ~186

"Claude + Obsidian + Git" — a self-organizing second brain where AI does all filing and cross-referencing.

- 10 built-in skills (braindump, consolidate-knowledge, review, etc.)
- Works across multiple AI agents (Claude Code, Kiro, Gemini CLI, Codex)
- Pure markdown — no database, no vendor lock-in
- Auto-generates Maps of Content and cross-references
- Weekly consolidation pattern

**What hapaxromana can learn:**
- Agent-agnostic design (skills as markdown files portable across Claude/Gemini/Codex) is clever future-proofing
- The "humans capture, AI organizes" philosophy matches our executive_function axiom perfectly
- Weekly consolidation as a first-class operation (vs our weekly drift-detector)
- Obsidian-native workflow without requiring a custom plugin

**Key differences:**
- No infrastructure layer at all — purely a note organization system
- No agents beyond the AI coding assistant itself
- No hardware, services, or monitoring
- No axiom governance

### linuz90/claude-telegram-bot (Personal Assistant Pattern)
**GitHub:** linuz90/claude-telegram-bot | **Notable:** docs/personal-assistant-guide.md

Not a product — a documented pattern for using Claude Code as a full personal assistant. Interesting because:
- Uses `.claude/skills/` for gmail, research, workout planning, etc.
- Runs subagents for daily "pulse" digests and health summaries
- Structures personal data in `~/Documents/Notes/` with domain folders
- Has an explicit "About [Your Name]" section in CLAUDE.md (similar to our operator profile)
- Daily digest format: TL;DR → Now → For You → Top of Mind → Health → Next

**What hapaxromana can learn:**
- The digest format is more actionable than our current briefing format
- Using Telegram as the mobile capture interface is pragmatic
- The pattern of Claude Code as the runtime for ALL personal automation (not just coding) is where the ecosystem is headed
- Skills-based decomposition vs our agent-per-task decomposition

---

## Tier 2: Strong Partial Matches

### Khoj (khoj-ai/khoj)
**GitHub:** khoj-ai/khoj | **License:** AGPL-3.0 | **Stars:** 32.8k

The most polished self-hosted "second brain" app. Indexes PDFs, markdown, Notion, images. Semantic search + chat over personal documents. Supports Ollama for local inference.

**Relevant to hapaxromana:** PKM + RAG dimension. Their document indexing pipeline is more mature than our rag-pipeline. Obsidian plugin available. Desktop + web + WhatsApp interfaces.

**Differences:** Multi-user architecture (cloud-first, self-host optional). No agent orchestration. No governance layer. No executive function focus.

**Potential learning:** Their Obsidian integration approach could inform obsidian-hapax. Their semantic search UX is polished.

### Mirix (Mirix-AI/MIRIX)
**GitHub:** Mirix-AI/MIRIX | **Stars:** 3.5k

Multi-agent personal assistant with named memory agents (core, episodic, semantic, procedural, resource, knowledge, reflexion). YAML-configured agent layout. Screen capture for personal memory. Docker Compose deployment.

**Relevant to hapaxromana:** Multi-agent architecture most similar to our Tier 2 agents. Memory agent taxonomy is more sophisticated than our flat agent list. Background agent concept similar to our Tier 3 timers.

**Differences:** Memory-capture focused (screenshots, activity), not task/executive-function focused. No axiom governance. Agent taxonomy is cognitive-science inspired (episodic, semantic, procedural) vs our task-inspired (briefing, health, scout).

**Potential learning:** The memory agent taxonomy (episodic vs semantic vs procedural) is a more principled decomposition than ours. Worth studying whether our agents map to these categories.

### arifOS (ariffazil/arifOS)
**GitHub:** ariffazil/arifOS | **License:** AGPL-3.0 | **Stars:** 34

Constitutional AI governance framework using MCP. Implements governance "floors" and tools as MCP endpoints (/mcp, /health, /metrics). Designed to sit beneath agents as a constraint layer.

**Relevant to hapaxromana:** Closest match to our axiom governance system. Both implement constitutional constraints on agent behavior.

**Differences:** arifOS is a runtime enforcement layer (MCP server). Our axioms are design-time constraints (documentation + drift-detector audit). arifOS is generic; our axioms are deeply personal (single_user, executive_function).

**Potential learning:** Runtime enforcement via MCP is compelling. Our drift-detector currently checks docs post-hoc; arifOS prevents violations in real-time. Could we expose axiom checks as MCP tools?

### danielrosehill/My-AI-Stack
**GitHub:** danielrosehill/My-AI-Stack, danielrosehill/AI-Stack-Oct-2025

A documented personal AI infrastructure with CLAUDE.md, stack.json, and budget breakdowns. Not code — documentation of one person's AI tool choices and architecture.

**Relevant to hapaxromana:** Same "single-user infrastructure documentation" impulse. Also uses Open WebUI, Qdrant, PostgreSQL.

**Differences:** Pure documentation, no agents, no governance. API-first (OpenRouter, cloud LLMs) rather than self-hosted-first. No automation layer.

**Potential learning:** The practice of documenting your stack as a versioned artifact (with point-in-time snapshots) is something we do in hapaxromana but could do more systematically.

---

## Tier 3: Infrastructure Templates (Ingredient Overlap)

### n8n Self-Hosted AI Starter Kit
**GitHub:** n8n-io/self-hosted-ai-starter-kit | **Stars:** 14.1k

Docker Compose bundle: Ollama + Qdrant + PostgreSQL + n8n. Almost identical service list to our llm-stack/, minus LiteLLM and Langfuse.

**Learning:** Their Compose patterns are well-tested. Compare healthcheck and resource limit configs.

### coleam00/local-ai-packaged
Docker Compose bundling Ollama, Supabase, n8n, Open WebUI, Flowise, Neo4j, Langfuse, SearXNG, Caddy. Superset of our stack.

**Learning:** They include SearXNG (private search) and Neo4j (knowledge graph) — two services we don't have. SearXNG could be useful for the research agent.

### kossakovsky/n8n-install
**Stars:** 743. Production-oriented self-hosted stack with Grafana + Prometheus monitoring, Langfuse, Letta agent server, Caddy reverse proxy.

**Learning:** Their monitoring stack (Grafana + Prometheus) is more mature than our health_monitor agent. Could complement rather than replace.

---

## Tier 4: Adjacent Concepts (Different Approach, Same Problem)

### alfred_ (get-alfred.ai)
Commercial ($25/mo). AI executive assistant specifically for ADHD professionals. Auto-triages email, extracts tasks, tracks follow-ups, generates daily priorities. No manual input required.

**Relevant to hapaxromana:** Most explicit ADHD/executive-function product found. Their design principles ("if I had the executive function to manually prioritize every task, I wouldn't need the app") mirror our executive_function axiom.

**Learning:** Their "zero-initiation" design principle (the system works without you doing anything) is more radical than ours. Our agents require `uv run python -m agents.X` invocation for Tier 2. Only Tier 3 timers are truly zero-initiation. Push more toward zero-initiation.

### Goblin Tools (goblin.tools)
Free, web-based. AI tools for executive function: Magic To-Do (breaks tasks into steps), Formalizer (rewrites text), Judge (estimates emotional tone), Estimator (time estimates).

**Learning:** Task decomposition as a first-class tool. Our system doesn't have an explicit "break this down for me" capability. Could be a useful Claude Code skill.

### Saner.AI
Commercial. AI PKM for ADHD. Voice capture → auto-transcription → auto-organization → smart search. All-in-one, no context switching.

**Learning:** The all-in-one, zero-configuration approach. Their insight: "the constant need to jump between tabs" is the enemy. Resonates with our executive_function axiom.

---

## Synthesis: What hapaxromana Does That Nobody Else Does

1. **Axiom-driven governance with T0 blocking violations.** arifOS is the only project attempting constitutional AI governance, and it's runtime enforcement — nobody else does design-time axioms with formal blocking implications.

2. **Operator profile as structured context.** agent-second-brain has `about.md`, COG has onboarding, but nobody builds a multi-dimensional cognitive/professional/creative profile that's injected into every agent's system prompt.

3. **Three-tier architecture with systemd autonomy.** Most projects are either fully interactive (Claude Code skills) or fully autonomous (AutoGPT). The interactive → on-demand → autonomous tier separation is unique.

4. **Cross-boundary operation (corporate_boundary axiom).** The Obsidian plugin operating across employer/personal network boundaries with graceful degradation is a constraint nobody else faces.

5. **Observability mandate.** Langfuse tracing of all LLM calls is standard in production systems but rare in personal tools.

## Synthesis: What hapaxromana Should Learn From Others

1. **Claude Code as universal agent runtime.** agent-second-brain, COG, and linuz90's pattern all use Claude Code skills instead of custom Python agents. This is dramatically simpler than maintaining 13 Pydantic AI agents. Worth evaluating: could some Tier 2 agents be replaced with Claude Code skills?

2. **Zero-initiation design.** alfred_'s principle that the system should never require the user to start it. Our Tier 2 agents still require manual invocation. Push more toward Tier 3 (autonomous) or Tier 1 (triggered by existing interaction patterns).

3. **Memory agent taxonomy.** Mirix's decomposition into episodic/semantic/procedural memory is more principled than our flat agent list. Could inform how we think about profile, documents, and knowledge_maint.

4. **Daily digest format.** linuz90's TL;DR → Now → For You → Top of Mind → Health → Next format is more actionable than raw briefings.

5. **Voice capture pipeline.** agent-second-brain's Telegram → Deepgram → structured output pipeline is more practical for daily use than our standalone voice-to-text.py script.

6. **Runtime axiom enforcement.** arifOS's MCP-based governance could make our axioms enforceable at runtime rather than only at audit time.

7. **Private search (SearXNG).** The research agent currently has no private search backend. SearXNG in Docker would be a natural addition to llm-stack.
