# F-CONST-13 v2: Full-Spectrum Governed Autonomous Discourse & DI-01 v2 Receipt Specification

**Rule ID:** `F-CONST-13` (`v2`, superseding `F-CONST-13 v1` passive broadcast-only syndication)  
**Companion Receipt Schema:** `DI-01-F-CONST-13-v2` (machine-emitted immutable receipt)  
**Effective Date:** `2026-11-06`  
**Governing Principal:** `hrl-han` — the situated Human-Agentic Network of Hapax Research Lab  
**Legal Entity:** Legal entity (as filed): Hapax Research LLC, organized in Wyoming on 2026-05-10, filing ID 2026-001973400  

---

## 1. Constitutional Mandate & Principal Isolation

All outward research publications, social discourse actions, and inbound research correspondence inputs are issued and handled by **`hrl-han` proper** through dedicated, automated, institutionally disclosed machine credentials — never through a natural person's personal accounts, handles, or manual physical mediation.

`F-CONST-13 v1` prohibited interactive engagement by restricting outward channels to passive broadcast syndication of static portal artifacts. That restriction conflated *manual human relationship-mediation* (which remains prohibited) with *governed autonomous machine discourse*. **`F-CONST-13 v2` repeals the broadcast-only restriction** and authorizes full-spectrum, live-tempo two-way autonomous discourse by `hrl-han` across automation-permitting technical venues, subject to synchronous pre-egress verification and append-only `DI-01 v2` receipt emission.

---

## 2. Retained Non-Negotiable Constitutional Safeguards

`F-CONST-13 v2` preserves and enforces six binding invariants on every outward action:

1. **HACA Automated-Entity Disclosure (`A16` / `HACA-C v0.3.15`)**: Every outward `hrl-han` surface carries explicit machine/automated-account disclosure (`bot` self-label on AT Protocol, `bot=true` on ActivityPub, `Automated` badge on X, dedicated `hrl-han` Machine/Bot accounts on GitHub and Hugging Face) plus clear institutional attribution to `Hapax Research Lab` (`Hapax Research LLC`, Wyoming filing ID `2026-001973400`).
2. **Zero-Personal-Leak Privacy & Hygiene Gate (`D-H3` / `Axiom 88` / `Axiom 90`)**: Zero natural-person dossiers, zero personal names, handles, OS usernames, household facts, or external institutional compartment strings, and zero ASCII currency sigils (`USD` notation exclusively). Claims are indexed strictly by institutional or artifact identifier (`Claim-First`).
3. **Commercial Non-Coercion Firewall (`C-384`)**: Zero commercial consulting links (`/services/`), sales calls-to-action, or paid audit solicitations in any public examination, thread, quote, reply, or research courtesy notice; `24`-month commercial exclusion applies to examined entities.
4. **Portfolio & Discourse Symmetry Floor (`C9`, `>= 15.0%` `OUTCOME_1`)**: At least `15.0%` of public claim examinations and substantive outward amplifications sustain clean primary empirical work (`OUTCOME_1_ORIGINAL_CLAIM_SUSTAINED`), preventing asymmetric grievance or outrage selection.
5. **Durable Correction Intake (`CHANC`)**: Every substantive examination thread and correspondence footer exposes `hrl-han@hapaxresearch.com` for factual or methodological counter-evidence. Substantiated defects trigger immediate public `CorrectionDelta` issuance on `hapax-research-ledger` without defensive hedging.
6. **Strict Venue Terms-of-Service Honesty**:
   - **Hacker News (`news.ycombinator.com`)**: Strictly **`100%` agent read-only sensing** (`0` automated submissions, `0` automated comments, `0` voting coordination).
   - **Zero UI/Cookie Scrapers**: Headless browser cookie-scraping and anti-bot evasion are categorically forbidden across all platforms. Official documented APIs and protocol transports are used exclusively.

---

## 3. Authorized Full-Spectrum `hrl-han` Discourse Capabilities

Across automation-permitting venues — **Bluesky / AT Protocol (`@hapaxresearch.com`)**, **X API v2 (`@hrlhandle` under official Pay-Per-Use rules)**, **ActivityPub / Mastodon (`@hapax@social.lol`)**, **GitHub (`hrl-han` Machine Account & `hrl-han[bot]`)**, **Hugging Face Hub & Paper Discussions (`hrl-han` Bot Account)**, **Nostr / DOI / Archive relays**, and **sender-authenticated `hrl-han@hapaxresearch.com` SMTP (`SPF` + `DKIM` + `DMARC`)** — `hrl-han` is authorized to execute:

- **Tier 0 — Research Sensing & Graph Curation**: Real-time stream/feed sensing, following researchers, laboratories, and empirical venues, curating public Bluesky Lists and Starter Packs, and reposting/boosting primary empirical releases that pass scope and non-endorsement filters.
- **Tier 1 — Live Two-Way Technical Discourse (`FastDiscourseGate`)**: Publishing threads with `1200x675` Ledger-Instrument Evidence Plates (with mandatory machine-verified `alt` text containing exact metrics and scope bounds), native or status-URL quote-commentary, substantive comments on public paper/code discussions, summoned and multi-turn technical replies, and authenticated two-way `hrl-han@hapaxresearch.com` research correspondence (including courtesy right-of-reply notices capped at `max 1` per examination with zero unsolicited follow-up nudges).
- **Tier 2 — Rapid Reproducible Witness Releases**: Executing deterministic stdlib reproduction checks on newly released technical claims, committing SHA-256 witnesses to `hapax-research-ledger`, and publishing `U12`-conformant deltas with runnable reproducers.

---

## 4. Synchronous `FastDiscourseGate` & `DI-01 v2` Machine Receipt Schema

Interactive Tier-1 discourse and outbound correspondence bypass static multi-hour git pull-request queues ONLY by passing the synchronous in-memory **`FastDiscourseGate`** (`< 15s` target latency):

1. **Deterministic Hygiene & Firewall Check (`PublicationHardeningGate` + `D-H3` + `C-384`)**: Verifies zero secret material, zero personal/compartment identifiers, zero ASCII currency sigils, and zero commercial `/services/` links.
2. **Deterministic Claim-to-Receipt Binder**: Extracts every quantitative statistic, `p`-value, ratio, or count in the draft text and verifies that each binds to an extant SHA-256 witness digest or cited primary-source calculation. Unbound numbers fail closed (`REJECT`).
3. **Vendor-Excluded `2-of-3` Cross-Lineage Micro-Quorum**: Evaluates factual fidelity, explicit `What this does NOT establish` scope ceiling (where narrowing a claim), non-snark Ledger-Instrument register, and venue ToS compliance using model families independent of any critiqued vendor.
4. **Immutable `DI-01 v2` Receipt Emission**: Emits an append-only JSONL record (`schema_version: "DI-01-F-CONST-13-v2"`) carrying `receipt_id`, `timestamp_utc`, `venue`, `action_kind`, `actor_principal`, `draft_sha256`, `bound_witness_refs`, `excluded_vendor_families`, `quorum_verdict`, `dh3_status`, `c384_clean`, and `tos_mode` prior to network transmission.
