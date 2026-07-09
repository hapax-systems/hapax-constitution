# Axiom Governance Gap Analysis: Viable Solutions

Research conducted 2026-03-05. Evaluates the 4 primary gaps identified in `axiom-governance-evaluation.md` with concrete, implementable solutions grounded in the research literature.

---

## Gap 1: No Formal Recovery Mechanisms

**Problem:** When the PreToolUse hook blocks a violation (exit 2), the agent gets a terse error message. It knows what it *can't* do but not what it *should* do instead. ABC's research shows that detection without recovery (γ > α drift bound) leads to frustrated workarounds — the agent rewrites the same intent through an unmonitored path.

**Evidence from ABC (arXiv:2602.22302):**
- Contracted agents detect 5.2-6.8 soft violations per session that baselines miss
- Recovery rate γ > α bounds cumulative drift — without structured recovery, violations accumulate
- Fallback chain: automated fix → human-in-loop → graceful termination
- (p,δ,k)-satisfaction: probability p of staying within δ deviation over k steps — impossible without recovery paths

**Current state:** `axiom-scan.sh` outputs to stderr:
```
Axiom violation (T0/single_user): pattern matched in path/to/file
Matched: class Auth_Service(Base_Model):  # [pattern escaped for axiom scan]
This introduces multi-user scaffolding prohibited by axiom governance.
Relevant T0 implications: su-auth-001, su-feature-001, su-privacy-001, su-security-001, su-admin-001
```

This tells the agent *what* was blocked and *which* implications apply, but not *how* to proceed.

### Proposed Solution: Recovery Hints per Axiom Domain

Add a `RECOVERY` message to hook stderr output, keyed by axiom domain and pattern category.

**Implementation:** Extend `axiom-scan.sh` and `axiom-commit-scan.sh` with a recovery hint lookup:

```bash
# After domain detection, add recovery guidance
case "$DOMAIN" in
  single_user)
    case "$pattern" in
      *[Aa]uth*|*[Pp]ermission*|*[Rr]ole*)
        RECOVERY="Remove auth/permission/role code entirely. The single user is always authorized. If protecting a dangerous operation, use a confirmation prompt instead."
        ;;
      *[Uu]ser*|*[Tt]enant*|*[Mm]ulti*)
        RECOVERY="Remove user/tenant abstraction. Reference the operator directly or use config values. There is exactly one user."
        ;;
      *[Ss]haring*|*[Cc]ollab*)
        RECOVERY="Remove sharing/collaboration features. If the goal is data export, implement direct file export instead."
        ;;
      *)
        RECOVERY="Remove the multi-user scaffolding. If the underlying goal is valid, reimplement it assuming a single operator with full access."
        ;;
    esac
    ;;
  management_governance)
    RECOVERY="Keep the data aggregation but remove generated language. Surface patterns and open loops; let the operator formulate their own words. Replace any 'suggest saying X' with 'notable pattern: X'."
    ;;
esac

echo "Recovery: $RECOVERY" >&2
```

**Complexity:** Low. ~30 lines added to each scan script. No new dependencies.

**Risk:** Recovery hints could become stale if axiom implications evolve. Mitigate by keeping hints generic (per-domain, not per-implication) and reviewing them when implications change.

**ABC alignment:** This implements the first tier of ABC's fallback chain (automated guidance). The existing operator review (Layer 6) serves as the second tier (human-in-loop). Session termination isn't needed — blocked writes are non-destructive.

---

## Gap 2: Stateless Per-Action Enforcement

**Problem:** The PreToolUse hook checks each file write in isolation. Multi-action violations — where no single write is problematic but the combination is — go undetected until the weekly drift detector runs. PCAS's dependency graph research shows this is a significant blind spot.

**Evidence from PCAS:**
- Models tool interactions as a DAG with `tool_call`, `tool_result`, and `message` nodes
- Dependency edges capture data flow between actions
- Reference monitor evaluates policy against the full graph, not individual nodes
- Result: 48% → 93% compliance when graph-aware enforcement is added
- Zero violations in instrumented runs (vs. stateless baseline that missed composition violations)

**Current state:** `axiom-audit.sh` (PostToolUse) logs every file modification to `~/.cache/axiom-audit/YYYY-MM-DD.jsonl` with timestamp, tool, file path, and snippet. This data *exists* but is never analyzed within a session.

### Proposed Solution: Lightweight Session Accumulator with Periodic Cross-Check

**Architecture:** Two components working together:

1. **Session accumulator** (extend PostToolUse `axiom-audit.sh`): Track files written in the current session in a session-scoped temp file. When the count exceeds a threshold (e.g., 10 writes), set a flag.

2. **Periodic semantic cross-check** (new, triggered by accumulator): When the threshold flag is set, run a lightweight LLM check across the session's written files. This happens in the *next* PostToolUse invocation (piggyback, not a separate process).

**Implementation — Session accumulator (axiom-audit.sh extension):**

```bash
# Session-scoped accumulator
SESSION_FILE="/tmp/axiom-session-$$"
# Append current file to session tracker
echo "$FILE_PATH" >> "$SESSION_FILE"
WRITE_COUNT=$(wc -l < "$SESSION_FILE" 2>/dev/null || echo 0)

# Every 10 writes, check for cross-file patterns
if [ "$WRITE_COUNT" -gt 0 ] && [ $((WRITE_COUNT % 10)) -eq 0 ]; then
  # Collect first 50 lines of each file written this session
  CONTEXT=""
  while IFS= read -r f; do
    if [ -f "$f" ]; then
      CONTEXT+="--- $f ---\n$(head -50 "$f")\n\n"
    fi
  done < "$SESSION_FILE"

  # Quick semantic check via local model (fast, private, no API cost)
  echo "$CONTEXT" | aichat -m local-fast \
    "Do these files, taken together, introduce multi-user scaffolding, auth systems, or collaboration features? Answer only YES or NO with a one-line reason." \
    2>/dev/null | grep -qi "^YES" && {
      echo "WARNING: Session cross-check detected possible multi-action axiom violation across $(wc -l < "$SESSION_FILE") files." >&2
      echo "Files: $(cat "$SESSION_FILE" | tr '\n' ' ')" >&2
  }
fi
```

**Why local model, not cloud:** This runs on every 10th file write. Using a cloud model would add latency and cost. The local `qwen-7b` (aliased as `local-fast`) is sufficient for a binary yes/no classification and runs in ~1 second on the RTX 3090. False positives are acceptable — this is advisory, not blocking.

**Complexity:** Medium. Adds session state via temp file, introduces an LLM call in the hot path (but only every 10th write and only via local model). The temp file is cleaned up when the shell session ends.

**Risk:**
- **Performance:** The LLM call adds ~1-2s every 10th write. Acceptable since PostToolUse doesn't block the agent.
- **False positives:** Local model may flag benign combinations. Mitigate with clear "WARNING" framing (not blocking).
- **Session boundary:** `$$` PID may not correctly scope to Claude Code sessions. Alternative: use `CLAUDE_SESSION_ID` env var if available, or derive from the audit log's session field.

**PCAS alignment:** This is a simplified version of PCAS's dependency graph. Full DAG construction is overkill for this system — the session accumulator captures the key insight (cross-action awareness) without the graph infrastructure.

---

## Gap 3: Pull-Based Upper Layers vs. Executive Function Axiom

**Problem:** Layers 5-7 (agent tools, operator review, precedent database) require the operator to *check* things — `check_axiom_compliance()` must be called by the agent, cockpit precedent review requires manual navigation, and the precedent database is only consulted on lookup. This contradicts the `executive_function` axiom: task initiation is a binding constraint, and pull-based systems fail when initiation is the bottleneck.

**Evidence from push governance research:**
- Taiwan's digital governance reform (2019-2023): Shifted from "citizens must apply" to "government proactively delivers." Result: 40% increase in service utilization among populations with access barriers.
- ADHD executive function research consistently shows that *prompting* (external cues to initiate) is more effective than *expecting* (assuming the person will remember to check). The literature calls this "environmental scaffolding" — restructuring the environment so the desired action is the default path.

**Current state:**
- `check_axiom_compliance()` is registered on 10 agents but called at agent discretion (Langfuse data suggested low usage)
- Cockpit precedent review at `/axiom-review` requires operator to remember to run it
- Precedent database is passive — only queried when an agent explicitly looks up prior decisions

### Proposed Solution: Convert to Push-Based Delivery

Three changes, ordered by impact-to-effort ratio:

**A. SessionStart axiom nudge (highest impact, lowest effort):**

The existing `session-context.sh` SessionStart hook already outputs system context. Extend it to surface pending axiom items:

```bash
# In session-context.sh, after existing context output
PENDING_PRECEDENTS=$(find ~/.cache/cockpit/precedents/ -name "*.json" -newer ~/.cache/cockpit/.last-reviewed 2>/dev/null | wc -l)
if [ "$PENDING_PRECEDENTS" -gt 0 ]; then
  echo "Axioms: $PENDING_PRECEDENTS precedent(s) pending review (run /axiom-review)"
fi

LAST_SWEEP=$(stat -c %Y ~/.cache/axiom-audit/baseline-*.json 2>/dev/null | sort -rn | head -1)
NOW=$(date +%s)
if [ -n "$LAST_SWEEP" ] && [ $((NOW - LAST_SWEEP)) -gt 604800 ]; then
  echo "Axioms: Last compliance sweep was $(( (NOW - LAST_SWEEP) / 86400 )) days ago"
fi
```

This surfaces axiom status *every session* without requiring the operator to remember.

**B. Daily briefing integration (medium impact, low effort):**

The daily briefing agent already runs at 07:00 via systemd timer. Add an axiom summary section:

```python
# In agents/briefing.py, add to data collection
from shared.sufficiency_probes import run_all_probes

def collect_axiom_status() -> dict:
    probe_results = run_all_probes()
    failures = [p for p in probe_results if not p["passed"]]
    return {
        "probe_failures": len(failures),
        "failed_probes": [p["name"] for p in failures],
        "pending_precedents": count_pending_precedents(),
    }
```

This puts axiom health into the daily push notification the operator already receives. Zero additional cognitive load — it's in the briefing they already read.

**C. Instrument Layer 5-7 usage (medium impact, medium effort):**

Add lightweight telemetry to `check_axiom_compliance()` and `record_axiom_decision()`:

```python
# In shared/axiom_tools.py
import time, json
from pathlib import Path

USAGE_LOG = Path.home() / ".cache" / "axiom-audit" / "tool-usage.jsonl"

def _log_usage(tool_name: str, agent: str):
    USAGE_LOG.parent.mkdir(parents=True, exist_ok=True)
    with USAGE_LOG.open("a") as f:
        f.write(json.dumps({
            "ts": time.time(),
            "tool": tool_name,
            "agent": agent,
        }) + "\n")
```

After 30 days, review the usage log. If Layers 5-7 show <5 calls total, mark them as dormant in the architecture docs and stop maintaining them. This follows ArbiterOS's progressive governance principle: don't maintain layers that aren't earning their keep.

**Complexity:** A is trivial (~10 lines of bash). B is low (one new data collector in an existing agent). C is medium (instrumentation + review process).

**Executive function alignment:** All three changes convert pull → push. The operator never has to *remember* to check axiom status — it's surfaced in every session (A) and every morning (B). Layer usage data (C) prevents maintenance of unused infrastructure, which is itself a cognitive load issue.

---

## Gap 4: Incomplete Action Coverage

**Problem:** PreToolUse hooks only fire on Write, Edit, MultiEdit, and Bash (for git operations). An agent can bypass axiom enforcement by:
1. Using `Bash` to write files (`sed`, `python -c`, `echo >`)
2. Using MCP tools (`mcp__filesystem__write_file`)
3. Making API calls via `curl` that violate `corporate_boundary`

**Evidence from Claude Code ecosystem:**
- GitHub issue #29709 confirms this is a known limitation: PreToolUse hooks for Edit/Write are bypassable via Bash
- MCP tools can be matched in hooks as `mcp__<server>__<tool>` (e.g., `mcp__filesystem__write_file`)
- The hook system supports regex matching on tool names, enabling broad coverage

**Current state:**
- `axiom-scan.sh` fires on `Write`, `Edit`, `MultiEdit` — covers Claude Code native file ops
- `axiom-commit-scan.sh` fires on `Bash` — but only checks for `git commit` and `git push` commands
- MCP filesystem tools (`mcp__filesystem__write_file`, `mcp__filesystem__edit_file`) are completely uncovered
- Bash file-writing commands (`sed -i`, `tee`, `python -c "open(...).write()"`, `echo >`) are uncovered
- `curl`/`wget` to external URLs are uncovered (relevant to `corporate_boundary`)

### Proposed Solution: Layered Coverage Extension

**A. Cover MCP filesystem tools (highest priority, trivial):**

Add MCP filesystem tools to the existing axiom-scan hook trigger:

In `~/.claude/settings.json`, the current PreToolUse matcher for axiom-scan:
```json
{"tool_name": "Write|Edit|MultiEdit"}
```

Change to:
```json
{"tool_name": "Write|Edit|MultiEdit|mcp__filesystem__write_file|mcp__filesystem__edit_file"}
```

The hook script already extracts content from `.tool_input.content` — MCP filesystem tools use the same field name. Zero code changes needed in the scan script itself.

**B. Cover Bash file-writing bypass (high priority, low effort):**

Extend `axiom-commit-scan.sh` (already fires on all Bash commands) to detect file-writing patterns:

```bash
# After git commit/push detection, before the else/exit 0

# Detect Bash file-writing commands
elif echo "$COMMAND" | grep -qE '(sed\s+-i|tee\s|>\s|python\s+-c|perl\s+-[ip])'; then
  # Extract target file from command (heuristic)
  TARGET_FILE=$(echo "$COMMAND" | grep -oE '[^\s]+\.(py|js|ts|sh|yaml|yml|json|toml|md)' | head -1)
  if [ -z "$TARGET_FILE" ]; then
    exit 0  # Can't determine target, skip
  fi
  # For sed/tee/redirect, scan the command arguments for axiom patterns
  DIFF="$COMMAND"
```

This is deliberately heuristic — it won't catch every possible Bash file write, but it catches the common bypass patterns (`sed -i`, `tee`, `echo >`, `python -c`). The goal is coverage of the 80% case, not perfection.

**C. Cover external API calls (medium priority, medium effort):**

Add `corporate_boundary` checks to the Bash hook for `curl`/`wget`:

```bash
# Detect curl/wget to non-localhost
elif echo "$COMMAND" | grep -qE '\b(curl|wget)\b'; then
  # Extract URL
  URL=$(echo "$COMMAND" | grep -oE 'https?://[^\s"'"'"']+' | head -1)
  if [ -z "$URL" ]; then
    exit 0
  fi
  # Allow localhost/127.0.0.1
  if echo "$URL" | grep -qE '^https?://(localhost|127\.0\.0\.1)'; then
    exit 0
  fi
  # In projects governed by corporate_boundary, flag external API calls
  # Check if current repo has corporate_boundary relevance
  if [ -f ".corporate-boundary" ] || echo "$FILE_PATH" | grep -q "obsidian-hapax"; then
    echo "Axiom advisory (T1/corporate_boundary): External API call detected" >&2
    echo "URL: $URL" >&2
    echo "Corporate boundary axiom requires sanctioned providers only (OpenAI, Anthropic)." >&2
    echo "If this is intentional, ensure the endpoint is employer-approved." >&2
    # Advisory only (exit 0), not blocking — external calls have legitimate uses
    exit 0
  fi
fi
```

Note: This is **advisory** (exit 0), not blocking (exit 2). External API calls are often legitimate. The goal is awareness, not prevention. The operator sees the warning and can decide.

**D. Accept the residual gap (important framing):**

Complete coverage is neither achievable nor desirable:
- An agent could write a Python script that, when later executed, creates violating code. No hook can catch this without executing the script.
- An agent could encode violating content in base64 and decode it later. Pattern matching can't catch arbitrary encoding.
- The weekly drift detector (Layer 4) catches what runtime hooks miss. This is the correct fallback.

The goal is **raising the cost of accidental violations**, not preventing intentional circumvention. The agent isn't adversarial — it's a well-meaning system that sometimes generates prohibited patterns by default. Making the common paths covered is sufficient.

**Complexity:** A is trivial (config change). B is low (~15 lines of bash). C is medium (~20 lines + per-project marker file). D is a documentation/framing decision.

**Known limitation (#29709):** Even with these extensions, the Bash tool can theoretically bypass any file-write hook by using exotic methods. This is a Claude Code platform limitation, not an axiom system limitation. The mitigation is defense-in-depth: the drift detector catches what hooks miss.

---

## Implementation Priority

| Solution | Gap | Effort | Impact | Priority |
|----------|-----|--------|--------|----------|
| A4: MCP tool coverage | 4 | Trivial | High | **Do first** |
| A1: Recovery hints | 1 | Low | High | **Do first** |
| A3: SessionStart nudge | 3 | Low | High | **Do first** |
| B3: Briefing integration | 3 | Low | Medium | **Do second** |
| B4: Bash bypass detection | 4 | Low | Medium | **Do second** |
| C2: Session accumulator | 2 | Medium | Medium | **Do third** |
| C3: Layer 5-7 instrumentation | 3 | Medium | Medium | **Do third** |
| C4: External API advisory | 4 | Medium | Low | **Do third** |
| D3: Usage review process | 3 | Low | Low | **Defer 30 days** |

The "do first" items are all <30 lines of code each and address the highest-impact gaps. They could be implemented in a single session.

---

## Sources

- **ABC:** arXiv:2602.22302 — Agent Behavioral Contracts (Feb 2026)
- **PCAS:** arXiv:2502.11999 — Policy-Compiled Agent Security (Feb 2025)
- **ArbiterOS:** arXiv:2504.13359 — Multi-Agent OS Governance (Apr 2025)
- **GaaS:** arXiv:2504.10560 — Governance-as-a-Service (Apr 2025)
- **Constitutional AI:** arXiv:2212.08073 — Bai et al. (Dec 2022)
- **From Craft to Constitution:** arXiv:2503.07608 (Mar 2025)
- **Claude Code hooks:** GitHub anthropics/claude-code issue #29709
- **Taiwan digital governance:** NDC proactive service delivery reform (2019-2023)
- **ADHD environmental scaffolding:** Barkley (2015), executive function compensation strategies
