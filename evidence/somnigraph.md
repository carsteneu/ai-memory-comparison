# Somnigraph — Evidence

> Every ✅ claim is backed by a public source (code file + line, or docs). Citations are pinned to
> commit [`d56b769`](https://github.com/AlexisOlson/somnigraph/tree/d56b769) so line numbers do not drift.
> Somnigraph is a single-user research artifact; the value lives in its documentation. It deliberately
> does **not** implement multi-agent, IDE-GUI, code-graph, or autonomous-daemon features, so many cells
> are honest ❌ with negative evidence. See the "Borderline" and "Absent Features (Verified)" sections.

**Repo:** `github.com/AlexisOlson/somnigraph`
**Stars:** 2
**Language:** Python
**License:** `Apache-2.0 WITH Commons-Clause`
**Created:** 2026-03-07
**Description:** Research-driven persistent memory for Claude Code — SQLite + sqlite-vec + FTS5 hybrid retrieval with RRF fusion, a learned LightGBM reranker, biological decay, sleep-based (NREM/REM) consolidation, and a retrieval feedback loop.

---

## System Metadata

| Field | Value |
|-------|-------|
| **Deployment** | Self-host / Local library (MCP server) |
| **Storage** | SQLite + sqlite-vec + FTS5 |
| **Integration** | MCP (FastMCP); optional `UserPromptSubmit` hook |
| **Single binary?** | no |
| **Setup** | `pip install` / `uv` (Python ≥3.11) |
| **Pricing** | free (open source) |
| **Storage unit** | Memory (text row) |

---

## Architecture

### Proxy ❌
- No conversation-stream interception; delivery is MCP tools + an optional prompt hook, not an in-flight proxy layer.

### Web/TUI ❌
- No web framework or TUI library in the codebase; the only interface is MCP tools accessed through the host agent.

### Offline ✅
- [`src/memory/embeddings.py#L121`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/embeddings.py#L121) — an optional `fastembed` backend (`BAAI/bge-small-en-v1.5`, 384-d, local) runs the full retrieval path without network; SQLite/FTS5/sqlite-vec are all local. Default backend is the OpenAI API, so offline requires setting `SOMNIGRAPH_EMBEDDING_BACKEND=fastembed`.

### Multi-agent ❌
- Single-user, single-session design; no agent registry, shared store, or inter-agent messaging.

### LLM providers (count: 2) ✅
- [`src/memory/embeddings.py#L121`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/embeddings.py#L121) — two embedding backends: OpenAI `text-embedding-3-small` (1536-d) and `fastembed` `BAAI/bge-small-en-v1.5` (384-d).

### Cache optimization ✅
- [`src/memory/scoring.py`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/scoring.py) — a Personalized-PageRank cache is reused across candidates (documented ~100× speedup in `docs/sessions/`); write-path embedding dedup skips re-embedding near-duplicates (cosine > 0.9). Token-efficient recall is controlled by the `limit` parameter rather than fixed context dumps.

### Procedural memory ❌
- A `procedural` memory *category* exists ([`src/memory/tools.py`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/tools.py)), but it stores text *about* procedures — there is no storage/execution of user-defined tools, workflows, or skills. See Borderline.

### Sandboxed execution ❌
- No code execution path of any kind; the system stores and retrieves text.

### Scheduled/autonomous ❌
- [`scripts/sleep.py`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/scripts/sleep.py) — the sleep/consolidation pipeline is manually invoked (`uv run scripts/sleep.py`); there is no cron, timer, or background daemon in the repo.

### Privacy/encrypt ✅
- [`src/memory/privacy.py`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/privacy.py) — regex PII/secret redaction (API keys, JWTs, passwords, GitHub/Slack tokens) at the write path; storage is local-only SQLite (`~/.somnigraph/`), no telemetry. (No encryption at rest.)

### Data export ❌
- No dedicated structured-export tool. `consolidate()` archives old events to a sidecar DB, but there is no JSON/Markdown/archive export API for the memory set.

---

## Data Model

### Entities ❌
- Entities are stored as ordinary memories with `category='entity'`, not as a dedicated entity table or extracted structured fields.

### Actions ❌
- No structured field for commands/operations/tool-calls; such content lives inline in `content`.

### Keywords/tags ✅
- [`src/memory/db.py#L114`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/db.py#L114) — `themes TEXT DEFAULT '[]'` JSON array, normalized by [`src/memory/themes.py`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/themes.py) (`normalize_themes()`), and used as a first-class retrieval channel.

### Anticipated queries ❌
- No generation of predicted search queries per entry. Bridge-theme injection exists but is *reactive* (added after retrieval-failure feedback), not a predictive query-generation step at ingest.
- Nearest mechanism: the sleep pass **intentionally writes summary vocabulary to be query-anticipatory** — REM summaries are deliberately phrased in the terms future searches are expected to use ([`scripts/sleep_rem.py#L1182`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/scripts/sleep_rem.py#L1182)). Same goal as this criterion (match likely future queries), but it shapes stored *content* rather than generating and storing predicted query strings, so still ❌.

### Trigger rules ❌
- No condition-based activation (file-open triggers, deadlines); relevance is scored, not rule-gated.

### Domain tag ❌
- `category` uses cognitive types (`episodic`, `semantic`, `procedural`, `reflection`, `meta`, `entity`), not domain labels (code/legal/finance/…).

### Task type ❌
- No task/idea/blocked/stale classification field.

### Context (why) ❌
- No dedicated "why is this relevant" field. A generic `metadata` JSON blob and edge `linking_context` exist but are not a structured rationale field. See Borderline.

### Source attribution ✅
- [`src/memory/db.py#L125`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/db.py#L125) — `source TEXT` with ≥3 distinct levels in use: `session`, `correction`, `reflect`, `extraction`, `sleep`, `probe`, `benchmark`, `live-feedback`, and more.

### Origin + trust ✅
- [`src/memory/graph.py#L14`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/graph.py#L14) — `_source_confidence_modifier()` assigns trust weights by capture method: `manual`=1.0, `correction`=0.95, `session`/`journal`=0.9, `auto`=0.7, applied to consolidation confidence.

### Emotional ❌
- No sentiment/emotional-intensity field anywhere in the schema.

### Conflict surfacing ✅
- [`src/memory/tools.py#L744`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/tools.py#L744) — recall output surfaces edges flagged `contradiction`; edges are created by NREM classification ([`scripts/sleep_nrem.py#L86`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/scripts/sleep_nrem.py#L86)).

### Layered memory ✅
- [`src/memory/db.py#L126`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/db.py#L126) — a `layer` field with a deliberate detail-layer → summary-layer architecture; the REM pass consolidates detail clusters into summary memories ([`scripts/sleep_rem.py#L16`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/scripts/sleep_rem.py#L16)).

### Time-travel ❌
- `valid_from`/`valid_until` columns exist ([`src/memory/db.py#L129`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/db.py#L129)) and temporal-evolution edges set validity bounds, but **no retrieval tool queries by validity window** and superseded memories are hard-deleted (`status='deleted'`), so historical state is not browsable. (`recall(since/before)` filters `created_at`, not validity — that is the Timeline-view feature below, a different criterion.)

### Schema fields (count: ~20) ✅
- [`src/memory/db.py#L109`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/db.py#L109) — distinct structured fields per memory (excluding auto ID and pure timestamps/counters): `content`, `summary`, `category`, `themes`, `base_priority`, `token_count`, `status`, `superseded_by`, `source`, `layer`, `metadata`, `valid_from`, `valid_until`, `generated_from`, `topic_id`, `decay_rate`, `shadow_load`, `flags`, `confidence`, `session_id`.

---

## Search & Retrieval

### Full-text ✅
- [`src/memory/tools.py#L487`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/tools.py#L487) — FTS5 keyword search via `bm25(memory_fts, BM25_SUMMARY_WT, BM25_THEMES_WT)` over a `memory_fts` virtual table, with tuned column weights (summary 13.278, themes 5.731 — [`constants.py#L44`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/constants.py#L44)). Query strings are sanitized for FTS5 in [`fts.py#L34`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/fts.py#L34).

### Semantic/vector ✅
- [`src/memory/vectors.py#L8`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/vectors.py#L8) — embeddings serialized to sqlite-vec; KNN by cosine distance in [`src/memory/tools.py#L460`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/tools.py#L460).

### Hybrid (BM25+Vec) ✅
- [`src/memory/scoring.py#L88`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/scoring.py#L88) — Reciprocal Rank Fusion over FTS + vector + theme channels, **then** a learned 31-feature LightGBM pointwise reranker ([`src/memory/reranker.py#L366`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/reranker.py#L366)) as the production scoring path (RRF kept as a fallback). The comparison's single ✅ cannot express the reranker/feedback layer — noted here for the record, not for extra credit.

### Deep (incl. thinking) ❌
- No indexing of model thinking/reasoning traces.

### Code graph ❌
- No Tree-sitter/AST indexing; the system is content-agnostic text memory, not a code index.

### Docs search ❌
- No ingested framework/API documentation corpus.

### Fact metadata query ✅
- [`src/memory/tools.py#L414`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/tools.py#L414) — `recall()` supports structured metadata filters (`category`, `since`, `before`). This is filter-level metadata querying, not a free-form attribute query language (no "all blocked tasks in project X"). See Borderline.

### Timeline view ✅
- [`src/memory/tools.py#L434`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/tools.py#L434) — `recall()` accepts `since`/`before` (relative like `"7d"` or ISO dates), filtering `created_at` for temporal/chronological search.

### Search modes (count: 3) ✅
- [`src/memory/tools.py#L460`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/tools.py#L460) — three fused retrieval channels: vector KNN, FTS/BM25, theme-overlap.

### Data sources (count: 1) ✅
- One searchable data type — user/agent memories (spanning detail and summary layers). No separate code, docs, or message corpora.

---

## Knowledge Lifecycle

### Decay/forgetting ✅
- [`src/memory/decay.py#L9`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/decay.py#L9) — exponential decay `base * exp(-decay_rate * days_since)` with per-category defaults, per-memory override, and pinned/keep immunity.

### Supersede/replace ✅
- [`src/memory/tools.py#L362`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/tools.py#L362) — duplicate `remember()` sets `superseded_by`; [`src/memory/graph.py#L243`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/graph.py#L243) records a revision-flagged edge with validity bounds (a traceable chain).

### Contradiction detection ✅
- [`scripts/sleep_nrem.py#L86`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/scripts/sleep_nrem.py#L86) — the NREM pass LLM-classifies memory pairs into `hard_contradiction`/`soft_contradiction` and flags the edge.

### Quarantine ❌
- Exclude-without-delete *does* exist at the **memory level**: `dormant` retires a memory from retrieval while retaining the row ([`scripts/sleep_rem.py#L1658`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/scripts/sleep_rem.py#L1658)), and `deleted` is a reversible soft-delete flag, not a hard row removal ([`src/memory/tools.py#L1407`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/tools.py#L1407)). What's absent is the **session-scoped** form the criterion asks for — no status or tool excludes *a whole session's* memories, and no retrieval path filters by `session_id`. ❌ is on the session-level requirement. See Borderline.

### Auto-resolution ✅
- [`scripts/sleep_rem.py#L1658`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/scripts/sleep_rem.py#L1658) — dormancy: low-access, aged detail memories move to `status='dormant'`; stale `pending` items auto-discard after a TTL ([`src/memory/tools.py#L1615`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/tools.py#L1615)).

### Trust model ✅
- [`src/memory/graph.py#L14`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/graph.py#L14) — a multi-tier source hierarchy (`manual` > `correction` > `session`/`journal` > `auto`) weights how much a source's classification is trusted.

### Explicit forget ✅
- [`src/memory/tools.py#L1391`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/tools.py#L1391) — `forget()` sets `status='deleted'` and cleans the vec/fts/rowid-map rows.

---

## Extraction Pipeline

### Auto-extraction ❌ *(borderline — see below)*
- Somnigraph runs **no extraction pipeline of its own** — no process watches the session and extracts memories. Capture happens only when the host agent calls `remember()` on its own judgment, guided by the shipped snippet ([`README.md#L72`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/README.md#L72)), with an auto-capture → `pending` → [`review_pending()`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory/tools.py#L1461) queue for confirmation. Two concrete triggers exist in the shipped guidance: mid-session, when the agent judges a lesson worth keeping; and a **session-end review, where the agent re-reads the session and calls `remember()` for anything unstored** ([`README.md#L72`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/README.md#L72)). So capture is autonomous in normal operation (no *user* save command), but it's delegated to the agent's judgment rather than system-owned, and even that session-end review is invoked manually today. Marked ❌ because the criterion certifies a *system* capability; the autonomous-in-practice behavior is documented in Borderline. See Borderline.

### Content-aware preprocessing ❌
- No type-specific truncation/filtering (code vs. prose). Theme normalization exists but is not content-type preprocessing. See Borderline.

### Deduplication ✅
- [`scripts/sleep_nrem.py#L526`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/scripts/sleep_nrem.py#L526) — duplicate-typed edges merge the weaker/older memory into the winner (by priority, then age); the write path also runs a near-duplicate embedding check before insert.

### Quality refinement ✅
- [`scripts/sleep_nrem.py#L519`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/scripts/sleep_nrem.py#L519) — a post-classification pass applies source-weighted confidence, filters low-confidence pairs (< 0.3), and boosts/penalizes by edge type.

### Narrative generation ✅
- [`scripts/sleep_rem.py#L745`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/scripts/sleep_rem.py#L745) — `generate_summaries()` produces dense summary-layer memories (with vocabulary bridging) from detail clusters.

### Clustering ✅
- [`scripts/sleep_rem.py#L577`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/scripts/sleep_rem.py#L577) — `detect_clusters()` groups detail memories by taxonomy `topic_id`; an LLM assigns unassigned memories and proposes taxonomy add/merge/split/reparent operations.

### Recurrence detection ❌
- No cross-session recurring-pattern detection (same bug / repeated question); no such code path exists.

### Persona extraction ❌
- No persistent user-trait/preference/working-style model. (Note: `personalized_pagerank()` is a graph algorithm, not persona extraction.)

---

## Platform Support

Somnigraph is a standard MCP server, so any MCP-capable host *could* connect, but the only documented, tested integration is Claude Code.

### Claude Code ✅
- [`src/memory_server.py`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/src/memory_server.py) — FastMCP server; the README documents installation into Claude Code, and the project is built and dogfooded against it.

### Codex ❌
### OpenCode ❌
### Gemini CLI ❌
### Copilot ❌
### Cursor ❌
### Windsurf ❌
### OpenClaw ❌
### Hermes ❌
### pi/omp ❌
### Antigravity ❌
- No documented integration for any of the above.

---

## Benchmarks

### LoCoMo ✅
- Score: **85.1** (overall accuracy, LLM-as-judge)
- [`docs/locomo-benchmark.md`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/docs/locomo-benchmark.md) — end-to-end QA, turn-level granularity, GPT-4.1-mini reader, **Opus 4.6 judge** (a strict judge; 3.2pp stricter than GPT-4.1-mini as judge, measured in-doc). 85.1 is the conservative headline (Level-3 retrieval); a later run with graph-augmented (L5b) retrieval and corrected ground truth reaches 87.2 on the same harness. Self-run harness (not third-party-verified) — as with every score in this table.

### LongMemEval ❌
- Not run. Score: —

### PersonaMem ❌
- Not run. Score: —

### Token reduction ❌
- Not measured against a defined baseline. Score: —

### Methodology open ✅
- [`docs/locomo-benchmark.md`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/docs/locomo-benchmark.md) documents datasets, reader/judge models, metrics, and per-category breakdowns; the harness scripts are public under [`scripts/locomo_bench/`](https://github.com/AlexisOlson/somnigraph/blob/d56b769/scripts/locomo_bench) (`run.py`, `eval_retrieval.py`, `train_locomo_reranker.py`).

---

## Borderline / Judgment Calls

Documented here rather than silently deciding, following the evidence-file rigor of `byterover.md`.

- **Offline → ✅.** Core retrieval runs fully local via the `fastembed` backend, but the *default* is the OpenAI embedding API. Marked ✅ because offline operation is supported and documented (a config change), consistent with how other index rows treating a local-model option are marked.
- **Procedural memory → ❌.** A `procedural` memory category exists, but the criterion requires *executable* tools/workflows/skills that persist and run. Somnigraph stores text describing procedures; it executes nothing. ❌ is the honest call.
- **Context (why) → ❌.** A generic `metadata` JSON field and edge `linking_context` could hold a rationale, but there is no dedicated, structured "why relevant" field, so ❌.
- **Fact metadata query → ✅.** `recall()` exposes structured `category`/`since`/`before` filters over memory metadata — real, implemented filtering — but not a free-form attribute query language. Marked ✅ for the implemented filters, with the limitation stated inline.
- **Content-aware preprocessing → ❌.** Theme normalization runs at write time, but there is no type-specific truncation/filtering (code vs. prose), which is what the criterion asks for.
- **Auto-extraction → ❌ (borderline).** Real and autonomous in practice: in-session the agent calls `remember()` on its own judgment per the shipped snippet (no *user* save command), and auto-captured items land in a `pending` queue for `review_pending()`. That much meets a behavioral reading of "without manual save calls." But Somnigraph runs no *system-owned* extraction pipeline (unlike byterover's post-session extraction) — the trigger is the host agent's judgment, not Somnigraph's code; it is miss-prone (the agent can simply not capture a lesson); and the systematic session-end review — where the agent re-reads the session and calls `remember()` for lessons worth keeping — is invoked manually (a shutdown hook could automate it, but none ships). Marked ❌ because the criterion certifies a system capability, and under "code beats docs" there is no extraction code — but the autonomous-capture reality is real enough that a reviewer could defensibly call it borderline ✅.
- **Quarantine → ❌.** The criterion is specifically session-scoped exclude-without-delete. Somnigraph *has* exclude-without-delete at the memory level (`dormant` hides a memory from retrieval while keeping it; `deleted` is a reversible soft-delete) — but no mechanism operates on a whole session, and nothing filters retrieval by `session_id`. ❌ on the session-level reading; the memory-level primitives are real and noted so a reviewer sees the partial capability.
- **Coverage note.** Several cells that a surface read might mark ✅ resolve to ❌ once the code is read (Scheduled/autonomous, Procedural memory, Data export, Time-travel, and Auto-extraction — the last three are documented borderlines above). Verified coverage is **~41% of boolean features** — and the coverage % is not a quality signal for this system anyway (a learned reranker + feedback loop are invisible to a binary feature grid).

---

## Absent Features (Verified)

Negative evidence for the ❌ features, so a reviewer can confirm without re-deriving.

| Feature | Evidence of absence |
|---|---|
| Proxy | MCP tools + optional hook only; no stream interception layer |
| Web/TUI | No web/TUI framework in the dependency set or code |
| Multi-agent | No agent registry, shared store, or inter-agent messaging |
| Procedural memory | `procedural` is a text category, not executable tool/skill storage |
| Sandboxed execution | No code-execution path of any kind |
| Scheduled/autonomous | Sleep pipeline is manually invoked; no cron/timer/daemon |
| Data export | No structured export tool (archive-to-sidecar is not export) |
| Entities | Entities are `category='entity'` memories, not structured fields/table |
| Actions | No structured command/operation field |
| Anticipated queries | Bridge themes are reactive (post-feedback), not predicted queries at ingest |
| Trigger rules | No condition-based activation |
| Domain tag | `category` is cognitive-type, not domain-labeled |
| Task type | No task/idea/blocked/stale field |
| Context (why) | No dedicated rationale field (generic metadata only) |
| Emotional | No sentiment/intensity field |
| Time-travel | Validity columns exist but no history-query tool; superseded rows deleted |
| Deep (incl. thinking) | No reasoning-trace indexing |
| Code graph | No Tree-sitter/AST indexing |
| Docs search | No ingested docs corpus |
| Quarantine | Memory-level exclude-without-delete exists (`dormant`, soft-`deleted`), but no session-scoped quarantine and no retrieval filter by `session_id` |
| Auto-extraction | No system-owned extraction pipeline; capture is host-agent `remember()` calls, autonomous in practice but delegated and miss-prone (borderline — see above) |
| Content-aware preprocessing | No type-specific truncation/filtering |
| Recurrence detection | No cross-session recurring-pattern detection |
| Persona extraction | No user-trait/preference model |
| LongMemEval / PersonaMem / Token reduction | Not run / not measured |
| Platforms (Codex … Antigravity) | Only Claude Code integration is documented |
