# Domain 1: Shared Foundation — Audit v2 Findings

**Audited:** 2026-03-03
**Auditor:** Claude Code (v2 full re-read)
**Prior findings (v1):** 17 (6 completeness, 4 correctness, 7 robustness)
**Fixes to verify:** 18, 19, 20, 21, 22, 52, 75, 76, 77

---

## Inventory

| File | v1 LOC | v2 LOC | Delta | Test File | Test LOC |
|------|--------|--------|-------|-----------|----------|
| `shared/config.py` | 116 | 149 | +33 | `tests/test_config.py` | 82 |
| | | | | `tests/test_embed_batch.py` (new) | 125 |
| `shared/operator.py` | 178 | 202 | +24 | `tests/test_operator.py` | 238 |
| `shared/notify.py` | 173 | 173 | 0 | `tests/test_notify.py` | 224 |
| `shared/vault_writer.py` | 284 | 283 | -1 | `tests/test_vault_writer.py` | 223 |
| `shared/vault_utils.py` | 35 | 35 | 0 | (indirect) | 0 |
| `shared/langfuse_client.py` | 58 | 59 | +1 | `tests/test_langfuse_client.py` (new) | 221 |
| `shared/langfuse_config.py` | 25 | 25 | 0 | (none) | 0 |
| `shared/email_utils.py` | 108 | 108 | 0 | (indirect via test_proton) | 0 |

**Total source:** 1,034 LOC (was 977, +57)
**Total test:** 1,113 LOC (was 657, +456)
**Test:source ratio:** 1.08 (was 0.67) — significant improvement from two new test files

---

## Fix Verification

### Fix 18: Add tests for langfuse_client.py — VERIFIED
**v1 finding:** C-1.1 (medium)
**Status:** ✅ Complete and correct.
`tests/test_langfuse_client.py` exists (221 LOC, 11 tests). Covers: auth header construction, URL encoding of params (ISO timestamps with `+00:00`), empty credentials, HTTP failure, JSON decode failure, `is_available()` (3 scenarios: no keys, has traces, no traces), no-params URL, custom timeout passthrough.
**Quality note:** Every test uses `importlib.reload(mod)` after patching env vars, which is correct but creates a fragile pattern — test ordering could matter if a test fails to reload. No issue observed in practice.

### Fix 19: Add tests for embed_batch() — VERIFIED
**v1 finding:** C-1.6 (medium)
**Status:** ✅ Complete and correct.
`tests/test_embed_batch.py` exists (125 LOC, 13 tests). Covers: empty input early return, single/batch results, prefix application (default/custom/empty), model selection (default/custom), timeout passthrough, error wrapping with cause chain, dimension validation (wrong size, mixed dimensions in batch).
**Quality note:** Thorough. Tests the right things. Mock patterns are clean.

### Fix 20: Add schema validation for operator.json — VERIFIED
**v1 finding:** R-1.1 (medium)
**Status:** ✅ Complete and correct.
`OperatorSchema(BaseModel, extra="allow")` at `operator.py:30-33`. Validates `version` (int|str) and `operator` (dict). `_load_operator()` now calls `OperatorSchema.model_validate(raw)` and catches `(json.JSONDecodeError, ValidationError)`, falling back to empty dict with a warning log. Tests: `test_operator_schema_valid`, `test_operator_schema_extra_fields_allowed`, `test_operator_schema_wrong_type_rejects`, `test_load_operator_corrupt_json`, `test_load_operator_invalid_schema`.
**Residual gap:** Schema uses `extra="allow"` — secondary fields (`axioms`, `constraints`, `patterns`, `cognitive-ergonomics`) are not validated. A `constraints: "string"` instead of `constraints: {}` would pass validation but silently break `get_constraints()`. Acceptable tradeoff for a single-operator system but noted.

### Fix 21: Add timeout to embed() and embed_batch() — VERIFIED
**v1 finding:** B-1.1 (medium)
**Status:** ✅ Complete and correct.
Both `embed()` (line 90) and `embed_batch()` (line 126) pass `request_timeout=30` to `ollama.embed()`. Test `test_timeout_passed_through` in `test_embed_batch.py` verifies the parameter. `test_embed_error_handling` in `test_config.py` implicitly covers the timeout error path (wrapping to RuntimeError).

### Fix 22: Differentiate Langfuse failure modes — PARTIALLY APPLIED
**v1 finding:** B-1.2 (medium)
**Status:** ⚠️ Incomplete. The fix plan specified returning a structured result (named tuple or dataclass with `data`, `error`, `available` fields). What was actually done: `langfuse_get()` now logs at `warning` level (line 50) for HTTP/JSON errors — this is correct and an improvement. However, the function still returns `{}` for all failure modes (missing credentials at line 36, HTTP errors at line 51, JSON errors at line 51). Callers cannot distinguish "Langfuse returned no data" from "Langfuse is unreachable" from "credentials are misconfigured."
**Impact:** Activity analyzer and profiler sources silently produce incomplete data when Langfuse is down. The `is_available()` guard (line 54-59) partially mitigates for callers that check it first, but `langfuse_get()` callers directly still get undifferentiated empty results.

### Fix 52: Consolidate PROFILES_DIR imports — VERIFIED
**v1 finding:** H-2.2 (medium)
**Status:** ✅ Complete and correct.
`cockpit/accommodations.py:17` now imports `from shared.config import PROFILES_DIR`. `shared/management_bridge.py:17` now imports `from shared.config import PROFILES_DIR, VAULT_PATH as _DEFAULT_VAULT_PATH`. All PROFILES_DIR references in the codebase trace back to the single definition in `shared/config.py:26`.

### Fix 75: Add operator cache invalidation API — VERIFIED
**v1 finding:** R-1.2 (low)
**Status:** ✅ Complete and correct.
`reload_operator()` at `operator.py:76-79` sets `_operator_cache = None`. Test `test_reload_operator_clears_cache` verifies: populates cache → injects fake data → confirms fake data returned → calls `reload_operator()` → confirms cache is None → confirms real data re-read from disk.

### Fix 76: Singleton Qdrant client — VERIFIED
**v1 finding:** R-1.3 (low)
**Status:** ✅ Complete and correct.
`_qdrant_client` module-level variable at `config.py:60`. `get_qdrant()` checks and caches at lines 65-68. No longer creates a new client per call.

### Fix 77: Add embed() dimension validation — VERIFIED
**v1 finding:** B-1.7 (low)
**Status:** ✅ Complete and correct.
`embed()` checks `len(vec) != EXPECTED_EMBED_DIMENSIONS` at lines 94-97 and raises `RuntimeError`. `embed_batch()` checks per-item at lines 130-134. Tests: `test_embed_dimension_validation` (wrong dims), `test_embed_dimension_validation_correct` (correct dims), `test_dimension_validation_rejects_wrong_size`, `test_dimension_validation_catches_mixed_dimensions`.

### Additional v1 fixes applied (outside fix plan scope for D1)

**B-1.4 (vault write return values):** Both `agents/briefing.py:396` and `agents/digest.py:393` now check the return value of their vault write calls, logging a warning on `None`. Fixed as part of Fix 91.

**R-1.4 (DIGESTS_DIR test fixture):** The `fake_vault` fixture in `test_vault_writer.py:35` now patches `DIGESTS_DIR` alongside the other four constants. Fixed as part of Fix 74.

**C-1.5 (write_digest_to_vault untested):** `TestWriteDigestToVault` class with 2 tests now exists in `test_vault_writer.py:89-104`. Fixed as part of Fix 74.

---

## Completeness Findings

### C2-1.1: `validate_embed_dimensions()` is defined but never called
**File:** `shared/config.py:138-149`
**Severity:** low
**Finding:** `validate_embed_dimensions()` was added as part of Fix 77 as a startup validation utility. Its docstring says "Call on startup from agents that depend on correct embedding dimensions." However, no agent, service, or startup path calls it. The function exists as dead code. The per-call dimension check in `embed()` and `embed_batch()` provides runtime protection, making this function redundant in practice.
**Impact:** Minimal. The per-call checks are the real protection. This is a "defense in depth" function that was written but not wired in.

### C2-1.2: `get_qdrant()` singleton has no reset/invalidation mechanism
**File:** `shared/config.py:60-68`
**Severity:** low
**Finding:** The `_qdrant_client` singleton (Fix 76) has no public reset function, unlike `reload_operator()` (Fix 75) which provides `_operator_cache` invalidation. Tests that need to mock `get_qdrant()` must patch it at the caller site (e.g., `@patch("agents.knowledge_maint.get_qdrant")`), which works correctly. But if the Qdrant URL changes at runtime (unlikely but possible via `direnv` reload), the singleton serves the old connection.
**Impact:** Minimal for current architecture (agents are per-invocation). The cockpit TUI is long-running but connects to a fixed localhost URL.

### C2-1.3: `langfuse_config.py` still has no dedicated test file
**File:** `shared/langfuse_config.py` (25 lines)
**Severity:** low (unchanged from v1 C-1.2)
**Finding:** No test file created. This was P3/Fix 74 which was only partially applied (vault_writer and embed tests addressed, but not langfuse_config, email_utils, or vault_utils dedicated test files).
**Impact:** Low. The module is 25 lines of `os.environ.setdefault()` calls guarded by a credential check.

### C2-1.4: `vault_utils.py` and `email_utils.py` still only indirectly tested
**File:** `shared/vault_utils.py` (35 lines), `shared/email_utils.py` (108 lines)
**Severity:** low (unchanged from v1 C-1.3, C-1.4)
**Finding:** No dedicated test files created. These were P3/Fix 74 items. `email_utils.py` has solid indirect coverage (12 tests in `test_proton.py::TestEmailUtils`). `vault_utils.py` is tested via `test_management_bridge.py`.
**Impact:** Low. Coverage exists but is non-obvious for maintainers.

---

## Correctness Findings

### R2-1.1: `OperatorSchema` validates structure minimally — secondary fields unprotected
**File:** `shared/operator.py:30-33`
**Severity:** low
**Finding:** `OperatorSchema(BaseModel, extra="allow")` validates that `version` is int|str and `operator` is a dict. But `axioms`, `constraints`, `patterns`, `cognitive-ergonomics`, `goals`, and `agent_context_map` are all accessed via `.get()` with no structural validation. If `axioms` were a string instead of a dict, `get_axioms()` would return the string, and callers iterating over it would get individual characters. Similarly, if `goals.primary` were a dict instead of a list, `get_goals()` would crash with `TypeError` in the `+` operation.
**Impact:** Low. `operator.json` is authored by the profiler agent, not edited by hand. The risk is a profiler bug producing malformed output. The `.get()` fallbacks prevent most crashes but could produce subtly wrong data.
**Operator impact:** None direct — this is a defense-in-depth gap.

### R2-1.2: `langfuse_client` module-level constants frozen at import time
**File:** `shared/langfuse_client.py:18-20`
**Severity:** low
**Finding:** `LANGFUSE_HOST`, `LANGFUSE_PK`, `LANGFUSE_SK` are computed once at import from `os.environ`. This is standard Python practice, but means env var changes (e.g., from `direnv` reload in a shell) are not reflected. The test file works around this with `importlib.reload(mod)` in every test — a correct but heavy-handed pattern that's necessary because of this design.
**Impact:** Negligible in production (env vars are set before any agent runs). Mildly annoying for tests.

### R2-1.3: `vault_writer.write_to_vault()` still uses non-atomic writes
**File:** `shared/vault_writer.py:72`
**Severity:** low (unchanged from v1 B-1.5)
**Finding:** `target.write_text("\n".join(parts))` is not atomic. Fix 41 added atomic writes to `accommodations.py` and `chat_agent.py` but not to `vault_writer.py`. If two agents write the same file simultaneously (e.g., nudges.md during a cockpit refresh while briefing agent triggers nudge update), the file could be partially written.
**Impact:** Low. In practice, writes are sequential. The briefing/digest timer ordering (Fix 51) reduces overlap risk. Vault replication would re-sync on the next full write anyway.

### R2-1.4: `VAULT_PATH` in `config.py` uses `Path.home()` at module load — not patchable cleanly
**File:** `shared/config.py:27`
**Severity:** low
**Finding:** `VAULT_PATH: Path = Path(os.environ.get("OBSIDIAN_VAULT_PATH", Path.home() / "Documents" / "Personal"))` computes the default at import time. Tests must patch `VAULT_PATH` at every import site (`shared.vault_writer.VAULT_PATH`, etc.). This is the same category as R2-1.2 (module-level constant freeze) but affects more downstream modules.
**Impact:** Manageable. Tests handle this with fixture patching. No production issue.

---

## Robustness Findings

### B2-1.1: `langfuse_get()` still returns undifferentiated `{}` on all failure modes
**File:** `shared/langfuse_client.py:34-51`
**Severity:** medium
**Finding:** Fix 22 was only partially applied. The warning-level logging (line 50) was added, but the return type is still `dict` returning `{}` for:
- Missing credentials (line 36, logged at `debug`)
- HTTP errors (line 51, logged at `warning`)
- JSON decode errors (line 51, logged at `warning`)
- Timeout (line 51, logged at `warning`)

Callers have no programmatic way to distinguish these. `is_available()` helps for pre-flight checks but doesn't help callers that get `{}` back from a data query.
**Impact:** Medium. The activity analyzer and profiler sources produce silently incomplete data when Langfuse is misconfigured or down. The operator sees a normal-looking briefing that's actually missing LLM usage data. The health monitor could detect Langfuse being down, but the data consumers don't correlate this.
**Operator impact:** Degraded briefing quality without explanation. The operator might not notice missing Langfuse data unless specifically looking for it.

### B2-1.2: `validate_embed_dimensions()` exists but is not wired into any startup path
**File:** `shared/config.py:138-149`
**Severity:** low
**Finding:** The function is correctly implemented — it calls `embed("dimension check")` and validates the result. But no agent calls it on startup. If the embedding model changes or is misconfigured, the error surfaces only on the first actual embed call, which may be deep in a processing pipeline.
**Impact:** Low. The per-call validation in `embed()` and `embed_batch()` catches this anyway. The startup check would provide earlier, clearer error messages but is not functionally necessary.

### B2-1.3: `_qdrant_client` singleton is not thread-safe
**File:** `shared/config.py:60-68`
**Severity:** low
**Finding:** If two threads call `get_qdrant()` simultaneously when `_qdrant_client is None`, both will execute the `if` block, both will create a `QdrantClient`, and the second assignment wins. The first client is leaked. Python's GIL largely prevents this in CPython, but the web API (FastAPI/uvicorn) uses async, and `asyncio.to_thread()` calls (Fix 13) could theoretically create a race.
**Impact:** Low. In practice, `get_qdrant()` is called during module import or early in agent startup, before any concurrency. A leaked extra QdrantClient instance would be garbage collected.

### B2-1.4: `notify.py` outer exception catch logs at `debug` only
**File:** `shared/notify.py:79-80`
**Severity:** low (unchanged from v1 B-1.3)
**Finding:** `send_notification()` wraps `_send_ntfy()` in `except Exception as exc: _log.debug("ntfy failed: %s", exc)`. This means unexpected errors (not the `URLError/OSError` caught inside `_send_ntfy`) are logged at debug level. A `ValueError` from a malformed URL or a `TypeError` from an incorrect parameter type would be invisible without debug logging enabled.
**Impact:** Low. The function correctly returns `False` for the failed channel and tries the desktop fallback. The risk is diagnostic difficulty, not functional failure.

---

## Test Coverage Assessment

| File | Status | v1→v2 Change | Notes |
|------|--------|-------------|-------|
| `shared/config.py` | **well tested** | Significant improvement | `test_config.py` (10 tests) + `test_embed_batch.py` (13 tests, new). All public functions tested. `validate_embed_dimensions()` untested (dead code). |
| `shared/operator.py` | **well tested** | Significant improvement | 27 tests (was ~19). Schema validation, corrupt JSON, reload_operator all covered. |
| `shared/notify.py` | **well tested** | Unchanged | 22 tests. Comprehensive. No gaps. |
| `shared/vault_writer.py` | **well tested** | Improved | 19 tests (was 17). Digest tests added. DIGESTS_DIR fixture fixed. Error path (PermissionError) still untested. |
| `shared/vault_utils.py` | **indirectly tested** | Unchanged | Still no dedicated file. P3. |
| `shared/langfuse_client.py` | **well tested** | New coverage | 11 tests (was 0). Auth, URL encoding, failures, availability. Good. |
| `shared/langfuse_config.py` | **untested** | Unchanged | Still no test file. P3. |
| `shared/email_utils.py` | **indirectly tested** | Unchanged | 12 tests in test_proton.py. P3. |

---

## Summary

### Fix Verification Scorecard

| Fix | Status | Quality |
|-----|--------|---------|
| 18 (langfuse tests) | ✅ Complete | Good: 11 tests, all critical paths |
| 19 (embed_batch tests) | ✅ Complete | Good: 13 tests, thorough |
| 20 (operator schema) | ✅ Complete | Good: Pydantic validation with graceful fallback |
| 21 (embed timeout) | ✅ Complete | Good: 30s timeout, tested |
| 22 (langfuse failure modes) | ⚠️ Partial | Warning logging added but return type unchanged |
| 52 (PROFILES_DIR consolidation) | ✅ Complete | Good: single source of truth |
| 75 (operator reload) | ✅ Complete | Good: clean API with test |
| 76 (Qdrant singleton) | ✅ Complete | Good: standard pattern |
| 77 (embed dimension check) | ✅ Complete | Good: per-call + per-batch validation |

**7 of 9 fixes fully verified. 1 partial (Fix 22). 0 failed.**

### New Findings

| ID | Severity | Category | Summary |
|----|----------|----------|---------|
| C2-1.1 | low | completeness | `validate_embed_dimensions()` defined but never called |
| C2-1.2 | low | completeness | `get_qdrant()` singleton has no reset API |
| C2-1.3 | low | completeness | `langfuse_config.py` still untested (P3 carry-forward) |
| C2-1.4 | low | completeness | `vault_utils.py` + `email_utils.py` still indirect-only (P3 carry-forward) |
| R2-1.1 | low | correctness | `OperatorSchema` validates minimally — secondary fields unprotected |
| R2-1.2 | low | correctness | `langfuse_client` module-level constants frozen at import |
| R2-1.3 | low | correctness | `vault_writer` still uses non-atomic writes (carry-forward) |
| R2-1.4 | low | correctness | `VAULT_PATH` computed at import — not cleanly patchable |
| B2-1.1 | **medium** | robustness | `langfuse_get()` still returns undifferentiated `{}` on all failures |
| B2-1.2 | low | robustness | `validate_embed_dimensions()` not wired into startup |
| B2-1.3 | low | robustness | `_qdrant_client` singleton not thread-safe |
| B2-1.4 | low | robustness | `notify.py` outer exception catch at debug level (carry-forward) |

### Overall Assessment

The shared foundation improved substantially between v1 and v2:

- **Test coverage** nearly doubled (0.67 → 1.08 test:source ratio). The two new test files (`test_langfuse_client.py`, `test_embed_batch.py`) address the two highest-priority v1 gaps.
- **Defensive coding** improved: embedding calls now have timeouts (30s) and dimension validation. Operator config has schema validation with graceful fallback. Qdrant client is singleton. Operator cache has invalidation API.
- **PROFILES_DIR consolidation** eliminates a structural fragility across 3 modules.
- **Vault write return values** are now checked by callers (briefing, digest).

**Remaining concern:** The only medium-severity finding (B2-1.1) is the incomplete Fix 22 — `langfuse_get()` still conflates all failure modes into `{}`. This is the same issue identified in v1 but now with evidence that the fix was attempted and only partially completed. The logging improvement helps diagnostics but doesn't help programmatic consumers.

**Fix quality assessment:** The v1→v2 fixes for D1 were applied carefully and correctly. No regressions introduced. The embed timeout, dimension validation, and schema validation are all clean implementations with appropriate tests. The partial Fix 22 appears to be a conscious scope reduction (logging was simpler than changing the return type and updating all callers) rather than an error.

**Operator impact:** The foundation serves the operator well. Notification dispatch has proper dual-channel fallback. Profile data degrades gracefully on missing files. The only operator-facing gap is B2-1.1 — silently degraded Langfuse data could produce briefings that look complete but aren't.
