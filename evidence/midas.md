# Midas — Evidence

> Every ✅ claim is backed by public source code or documentation.
> Sources: GitHub repo `vornicx/Midas` (PyPI package `midas-memory`). Line numbers pinned to `main`; they may shift.

**Repo:** `github.com/vornicx/Midas`
**Stars:** 6
**Language:** Python
**License:** MIT
**Created:** 2026-06-04
**Description:** Local-first, eval-first memory for long-horizon AI agents — semantic recall + budgeted context assembly with **no LLM at ingest or query** (local embeddings only), and source-traceable retrieval.

---

## System Metadata

| Field | Value |
|-------|-------|
| **Deployment** | `Library + local MCP server` |
| **Storage** | `SQLite` |
| **Integration** | `MCP / SDK / LangGraph` |
| **Single binary?** | `no` (Python package; core has zero third-party deps) |
| **Setup** | `pip install midas-memory` (or `uv tool install "midas-memory[mcp,local]"`) |
| **Pricing** | `free` (MIT; $0 API — no LLM at ingest/query) |
| **Storage unit** | `Memory (text record)` |

---

## Architecture

### Proxy ❌

### Web/TUI ❌

### Offline ✅
> Core memory functionality works without internet connection.
- Source: `midas/embeddings.py:38-56` (`HashingEmbedder`, dependency-free offline default) and `:251-285` (`LocalEmbedder`, fastembed/ONNX bge-base — no API key, no torch) — `README.md` "works **fully offline**. No API key, ever."

### Multi-agent ✅
> Cross-agent memory sharing: several MCP clients/processes share one DB file **live** — each store detects other connections' writes (SQLite `PRAGMA data_version`) and refreshes, so an agent sees another agent's captures without restarting. Writes are stamped with `actor`; `namespace` scopes agents/projects/users inside the shared store.
- Source: `midas/sqlite_store.py:96-110` (`_refresh_if_stale`; module docstring "across processes — multiple MCP clients… can point at the same DB file"); `README.md` "One memory, many clients" (with demo GIF of a real two-process run); `midas/mcp_server.py:44-61` (`MIDAS_MCP_NAMESPACE` + per-call `namespace` on every tool); `midas/types.py:40` (`actor`).

### LLM providers (count: 3) ✅
> Distinct embedding backends behind the `Embedder` protocol.
- Source: `midas/embeddings.py` — `HashingEmbedder` (offline, `:38`), `LocalEmbedder` (fastembed/bge ONNX, `:251`), `OpenAIEmbedder` (`:58`). (No LLM is used at ingest/query; these are embedding providers.)

### Cache optimization ✅
> Caches embeddings for performance.
- Source: `midas/embeddings.py:106-217` (`DiskCachedEmbedder` — persistent SQLite embedding cache keyed by namespace + text hash, with hit/miss counters); `midas/store.py` in-memory store keeps a cached numpy cosine matrix.

### Procedural memory ❌

### Sandboxed execution ❌

### Scheduled/autonomous ❌

### Privacy/encrypt ✅
> Self-hosting, zero-telemetry, no data egress.
- Source: `README.md` — "**$0 API spend, zero data egress**", "no cloud, no per-message AI bill", "every Midas mechanism is local, $0, zero-egress"; all storage is a local SQLite file (`midas/sqlite_store.py`). No network call at ingest or query.

### Data export ❌

---

## Data Model

### Entities ❌

### Actions ❌

### Keywords/tags ❌

### Anticipated queries ❌

### Trigger rules ❌

### Domain tag ❌

### Task type ❌

### Context (why) ❌

### Source attribution ✅
> Every record carries `actor` (which agent/user/process authored it), a 4-level `provenance` (`planning` / `action` / `observation` / `user_confirmation`), and a free-form `source` pointer; recall returns them verbatim.
- Source: `midas/types.py:23-29` (`MemoryProvenance`), `:38-41` (`source`, `provenance`, `actor` on `MemoryRecord`); `midas/mcp_server.py` `_serialize_record` (recall/inspect return provenance+actor+source).

### Origin + trust ✅
> Trust is ordered by capture method — `user_confirmation > action > observation > planning` — and a re-captured duplicate can only *upgrade* a memory's provenance, never downgrade it.
- Source: `midas/memory.py:128-133` (`_PROVENANCE_RANK`), `:406-425` (`_upgrade_provenance`).

### Emotional ❌

### Conflict surfacing ❌

### Layered memory ❌

### Time-travel ❌

### Schema fields (count: 8) ✅
> Distinct structured fields per memory entry (excluding auto id/timestamps).
- Source: `midas/types.py:32-45` (`MemoryRecord`): `content`, `kind`, `importance` (1-5), `source`, `provenance`, `actor`, `metadata` (dict), `superseded_by`. (Excludes `id`, `created_at`, `updated_at`, and the derived `embedding`.)

---

## Search & Retrieval

### Full-text ✅
> Keyword-based BM25 ranking.
- Source: `midas/bm25.py:19-32` (pure-Python Okapi BM25 with non-negative IDF), invoked from `midas/memory.py:487-492`.

### Semantic/vector ✅
> Embedding-based semantic search (cosine).
- Source: `midas/memory.py:402-468` (`recall`, vector prefilter + cosine scoring), `midas/store.py` cosine search; `midas/embeddings.py:325-335` (`cosine`).

### Hybrid (BM25+Vec) ✅
> Combines full-text and vector with RRF fusion.
- Source: `midas/memory.py:470-518` (`_hybrid_candidates` — unions semantic top-k with BM25 top-k and fuses with reciprocal-rank fusion, `fusion="rrf"`). Enabled via `recall(hybrid=True)`.

### Deep (incl. thinking) ❌

### Code graph ❌

### Docs search ❌

### Fact metadata query ✅
> Structured predicate filtering on memory fields.
- Source: `midas/memory.py:421-426` (`recall(kind=..., min_importance=...)` builds a predicate filtering candidates by the structured `kind` and `importance` fields).

### Timeline view ✅
> Chronological assembly + event-time temporal retrieval.
- Source: `midas/memory.py:682-686` (`build_context(context_order="chronological" | "recency")`); `recall(now=...)` and per-record event time (`created_at`) drive recency-aware temporal retrieval (`:416-419`, `:992-1004`).

### Search modes (count: 3) ✅
> Distinct retrieval modes.
- Source: `midas/memory.py` — semantic/bi-encoder (`:451-452`), hybrid lexical+vector RRF (`:442-446`), cross-encoder reranked (`:447-450`, `midas/embeddings.py:288-322` `LocalReranker`).

### Data sources (count: 1) ✅
> Unified memory records (typed by `kind`: note / chat / fact / preference / constraint / mission).
- Source: `midas/types.py:13-21` (`MEMORY_KINDS`); a single record store is the searchable corpus.

---

## Knowledge Lifecycle

### Decay/forgetting ✅
> Selective forgetting by decay value (importance × recency).
- Source: `midas/memory.py:836-902` (`forget_decayed` evicts lowest-`memory_value` records; `memory_value` at `:808-821`). Exposed as the `maintain` MCP tool (`midas/mcp_server.py:156-188`) and auto-runs over `MIDAS_MCP_MAX_RECORDS`.

### Supersede/replace ✅
> Belief revision via a traceable supersession chain.
- Source: `midas/types.py:35` (`superseded_by`), `midas/memory.py:539-622` (`_maybe_supersede`, `_resolve_head`) — a query phrased like the old value resolves to the current head.

### Contradiction detection ✅
> Local NLI contradiction gate on revision.
- Source: `midas/nli.py:85-90` (`LocalNLI.contradiction`, int8 ONNX MNLI), gating supersession at `midas/memory.py:608-611`.

### Quarantine ❌

### Auto-resolution ❌

### Trust model ✅
> Multi-tier trust hierarchy with enforcement: memory-justified **external/destructive actions are allowed only on `user_confirmation`-provenance memories**; lower-trust memory (planning/observation/action) can inform planning but cannot authorize them.
- Source: `midas/guard.py:20-27` (allowed provenance per intended use), `:116` (`decide_memory_use`); MCP tool `check_memory_use`; `README.md` "Guard boundary".

### Explicit forget ✅
> Delete a single memory (supersession-chain-safe), erase a whole **topic** with a dry-run preview + deletion audit, or clear all.
- Source: `midas/memory.py:1055-1106` (`forget` with chain relinking, `forget_matching` — relevance-matched erasure, dry-run, returns matched records as the audit trail); `midas/mcp_server.py:385` (`forget_matching` MCP tool, dry-run by default), `forget`, `forget_all`.

---

## Extraction Pipeline

### Auto-extraction ❌
> (By design: Midas stores turns verbatim with **no LLM extraction** at ingest. `capture` auto-*decides whether to keep* a turn, but does not synthesize structured facts.)

### Content-aware preprocessing ❌

### Deduplication ✅
> Near-duplicate detection + collapse.
- Source: `midas/memory.py:904-950` (`consolidate` — extractive collapse of cosine ≥ threshold duplicates, keeps highest-value copy); `capture` dedup gate at `:331-343` and `midas/policy.py:34-36` (`dedup_threshold`).

### Quality refinement ✅
> No-LLM importance scoring + confidence/abstention pass.
- Source: `midas/importance.py` (`ContentImportance`/`StructuralImportance` — rule-based per-turn salience 1-5); `midas/memory.py:520-537` (`recall_confidence`) and `:707-732` (abstention via NLI entailment / calibration reranker).

### Narrative generation ❌

### Clustering ❌

### Recurrence detection ✅
> Restatement detection reinforces a memory (repetition ⇒ salience).
- Source: `midas/memory.py:360-375` (`_reinforce_existing` / `_reinforce_record` — a new turn with cosine ≥ `reinforce_threshold` to an existing memory is treated as a restatement and boosts its importance + recency).

### Persona extraction ❌

---

## Platform Support

### Claude Code ✅
- Source: `README.md` "Claude Code" section — `claude mcp add midas -s user … -- midas-mcp`.

### Codex ✅
- Source: `README.md` "Codex CLI" section — `codex mcp add midas -- midas-mcp` / `~/.codex/config.toml`.

### OpenCode ❌

### Gemini CLI ❌

### Copilot ❌

### Cursor ✅
- Source: `README.md` "Cursor" section — `~/.cursor/mcp.json` config block.

### Windsurf ✅
- Source: `README.md` "Windsurf" section — `~/.codeium/windsurf/mcp_config.json` config block.

### OpenClaw ❌

### Hermes ❌

### pi/omp ❌

### Antigravity ❌

---

## Benchmarks

### LoCoMo ✅
- Score: `recall@k 0.73` (FULL public set: 10 conversations, n=1,540 answerable questions, bge-base, no rerank, seed 0; baseline-raw 0.05)
- Source: `BENCHMARKS.md` §1 "Retrieval quality — recall@k" — with reproduce command and a dated correction notice: the previously published 0.85 (n=50) did not reproduce against the public `locomo10.json`; the full-set number replaces it.

### LongMemEval ✅
- Score: `recall@k 0.92` (LongMemEval-s, FULL set: all 500 questions, 246,750 turns ingested; baseline-raw 0.01); answer `0.84` with gpt-4o at n=40 (ties the LLM-ingest SOTA at $0 ingest)
- Source: `BENCHMARKS.md` §1 and §6 — with reproduce commands.

### PersonaMem ❌
- Score: `—`

### Token reduction ✅
- Score: `30–40% fewer context tokens` (deterministic A/B vs the parsimony-off baseline: synthetic 102→87, conflicts 207→121, multiday 174→126 avg tokens, recall@k unchanged); plus −42%/line lean record format and a 442→198-token (−55%) injected MCP policy.
- Source: `BENCHMARKS.md` §1 "Context parsimony — a scale-free relevance floor" (table + reproduce command); `CHANGELOG.md` "Token-lean by default".

### Methodology open ✅
> Publicly documented, reproducible methodology.
- Source: `BENCHMARKS.md` (every number has a reproduce command + "Methodology — why reader-independent metrics"); `eval/` harness in-repo (datasets, adapters, metrics, runner, retention).
