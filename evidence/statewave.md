# Statewave — Evidence

**Repo:** `smaramwbc/statewave`
**Stars:** 313
**Language:** Python
**License:** Apache-2.0
**Created:** 2026-04-24
**Description:** Open-source memory runtime that compiles raw events into typed, provenance-tagged memories and assembles deterministic, token-bounded context bundles — instead of query-time retrieval.

> Sources: `github.com/smaramwbc/statewave` (core server, main branch), `github.com/smaramwbc/statewave-web` (marketing site incl. published benchmark numbers), `github.com/smaramwbc/statewave-admin` (operator console). Audit date: 2026-08-14.

---

## System Metadata

| Field | Value |
|-------|-------|
| **Deployment** | `Self-host (Docker Compose / Helm / bare-metal)` |
| **Storage** | `PostgreSQL 14+ with pgvector` |
| **Integration** | `REST API / SDKs (Python, TypeScript) / MCP (via statewave-connectors)` |
| **Single binary?** | `no` (API process + Postgres; separate desktop admin app ships as a single binary) |
| **Setup** | `docker compose up -d`, or `npx @statewavedev/statewave` / `curl \| sh` quick-start, or `pip install statewave` (SDK only) |
| **Pricing** | `free` (Apache-2.0, self-hosted; no hosted paid tier documented) |
| **Storage unit** | `Memory` — typed as `profile_fact` / `episode_summary` / `procedure` / `artifact_ref` |

---

## Architecture

### Proxy ❌

### Web/TUI ✅
- `statewave-admin` repo, `README.md` — ships a desktop operator console ("Statewave Admin") with macOS/Windows/Linux installers, described as a read-only console over the API.
- `statewave-admin` repo, `src/pages/` — React SPA source for the console.

### Offline ✅
- `README.md:69` — "The default heuristic compiler runs fully local; choose an LLM compiler or hosted embeddings if you want them."
- `README.md:171` — Embedding provider `stub` documented as "local heuristic, no API key".

### Multi-agent ✅
- `README.md:34` — "Everything is organised around **subjects** — a user, account, agent, repo, or any entity you track", i.e. any number of agents can read/write the same subject's memory via the shared API.
- `statewave-web` repo, `src/pages/MultiAgentSharedContextPage.tsx:610` — "One run, one subject_id. Every agent in the fleet reads and writes that same shared context, automatically."

### LLM providers (count: 100+) ✅
- `README.md:170` — "Any of 100+ LiteLLM-supported providers — OpenAI, Anthropic, Azure, Bedrock, Ollama, Cohere, Gemini, Mistral, Groq, …"

### Cache optimization ✅
- `server/services/embeddings/query_cache.py:1-34` — documents a two-layer query-embedding cache: L1 in-process LRU+TTL inside the LiteLLM provider, L2 a Postgres-backed cross-machine cache in front of it, to avoid repeat provider round-trips for identical task text.

### Procedural memory ❌
> `procedure` is a stored `MemoryKind` (`server/domain/models.py:21`) containing step-by-step text, but nothing in the compilers or context assembly executes it — it is returned to the caller as data, same as any other memory kind.

### Sandboxed execution ❌

### Scheduled/autonomous ✅
- `server/app.py:35-56,135` — an `asyncio` background task (`_cleanup_loop`, `asyncio.sleep(3600)`, "every hour") started at server boot, runs without any user/API request, and tombstones expired memories / purges old compile jobs.

### Privacy/encrypt ✅
- `README.md:69` — "You own the storage — self-hosted, open source, no vendor lock-in. Episodes and compiled memories live in your Postgres."
- `README.md:273` — `STATEWAVE_RECEIPT_SIGNING_KEYS` — HMAC-SHA256 keys for receipt signing, "Never persisted to the DB".

### Data export ✅
- `server/api/admin.py:2880-2881` — `GET /export/{subject_id}` — "Export all episodes and memories for a subject as a portable JSON document."
- `server/api/admin.py:3656-3657` — `POST /memory/export` — versioned export payload for one or more subjects.

---

## Data Model

### Entities ✅
- `server/services/entities.py:1-15` — `populate_entities_for_memories` / `backfill_entities_for_subject`: LLM-based named-entity extraction (`entity_extraction.extract_entities`) written into a dedicated `subject_entities` store with embeddings, distinct from the memory row itself.

### Actions ❌
> `MemoryKind` (`server/domain/models.py:18-22`) has no `action`/`tool_call` kind; no separate structured field for commands/operations was found.

### Keywords/tags ❌
> Per-memory `sensitivity` labels exist (`docs/capabilities.md` — "Per-memory sensitivity labels ... operator-supplied capability tags (`pii`, `financial`, `secret`, …)") but they're a fixed, policy-purpose vocabulary for redaction, not a general keyword/tag system for categorizing memory content.

### Anticipated queries ❌

### Trigger rules ❌

### Domain tag ❌

### Task type ❌

### Context (why) ❌

### Source attribution ✅
- `server/domain/models.py:47` — `Episode.source: str` — free-text origin field.
- `README.md:195-206` — connectors stamp distinct source identifiers per channel (`chat`, `github`, `markdown`, `slack`, `n8n`, `zapier`, `discord`, `notion`, `zendesk`/`intercom`/`freshdesk`, `gmail`) — well over 3 distinct authoring origins are distinguishable per memory's provenance chain.

### Origin + trust ❌
> Source is recorded (see above) but nothing in `server/services/context.py` ranking weights one source/origin above another.

### Emotional ❌
> `server/services/compilers/llm.py:89` instructs the extractor to preserve "sentiment/emotion words" verbatim in memory text — that's a wording-fidelity rule, not a structured sentiment/intensity field.

### Conflict surfacing ✅
- `server/services/conflicts.py:1-20` — claim-based path (canonical key + value, "wording-independent contradiction resolution") plus a legacy Jaccard token-overlap path; both detect and resolve conflicting memories at compile time.

### Layered memory ❌

### Time-travel ✅
- `README.md:151` — `GET /v1/timeline` — chronological subject timeline.
- `server/domain/models.py:25-34` — `MemoryStatus.tombstoned` — superseded memories are soft-deleted, not purged, so history stays queryable.
- `README.md:328` — `docs/replay.md` / `POST /v1/receipts/{id}/replay` — "re-run a historical retrieval against current memories + original policy."

### Schema fields (count: 11) ✅
- `server/domain/models.py:60-76` — `Memory` model fields excluding auto id/timestamps: `subject_id`, `kind`, `content`, `summary`, `confidence`, `valid_from`, `valid_to`, `source_episode_ids`, `metadata`, `status`, `embedding` = 11.

---

## Search & Retrieval

### Full-text ✅
- `alembic/versions/0027_memories_content_tsvector.py` — Postgres `tsvector` migration on memory content.
- `server/api/memories.py:396` — hybrid blend uses "Postgres BM25 (`ts_rank_cd`)".

### Semantic/vector ✅
- `server/services/context.py:219-233` — `repo.search_memories_by_embedding` — pgvector cosine-distance search, converted to a similarity score.

### Hybrid (BM25+Vec) ✅
- `server/api/memories.py:393-402` — `hybrid` search param: "Blend semantic cosine with Postgres BM25 (`ts_rank_cd`) and entity boost for hybrid retrieval... v10 bench validated this as a strict improvement across LoCoMo (+2.1), LongMemEval (+16.0 vs Phase-1 hybrid), and BEAM (+1.8)." Default `True` since 2026-06-19.

### Deep (incl. thinking) ❌

### Code graph ❌

### Docs search ❌
> The Markdown connector (`README.md:199`) ingests docs as ordinary "decision memory" through the same episode/memory pipeline; there is no dedicated docs-only search mode.

### Fact metadata query ✅
- `server/api/memories.py:390` — `GET /v1/memories/search` supports a `kind` filter.
- `README.md:154-155` — `GET /v1/resolutions` — structured query for a subject's resolution history.

### Timeline view ✅
- `README.md:151` — `GET /v1/timeline`.

### Search modes (count: 4) ✅
- `server/api/memories.py:387-444` — `GET /v1/memories/search` reports `search_mode` as `text` / `semantic` / `text_fallback`, and separately exposes `hybrid` (BM25+vector+entity blend) and `rerank` (LLM rerank of the hybrid candidate pool) query flags — 4 distinct retrieval modes in this one endpoint (text, semantic, hybrid, rerank).

### Data sources (count: 4) ✅
- `server/domain/models.py:18-22` — `MemoryKind`: `profile_fact`, `episode_summary`, `procedure`, `artifact_ref`.

---

## Knowledge Lifecycle

### Decay/forgetting ✅
- `server/services/memory_ttl.py:1-16` — per-kind, operator-configured TTL; expired active memories are tombstoned by the hourly `_cleanup_loop` in `server/app.py`.

### Supersede/replace ✅
- `server/services/conflicts.py:1-20` — newer claims/overlapping facts supersede older ones; `MemoryStatus.tombstoned` (`server/domain/models.py:25-34`) preserves the superseded row for traceability rather than deleting it.

### Contradiction detection ✅
- `server/services/claims.py:1-20` — canonical key+value claim envelope lets the resolver "detect contradictions independent of wording".
- `server/services/conflicts.py:1-9` — "a newer claim whose normalized value DIFFERS ... supersedes it — wording-independent contradiction resolution."

### Quarantine ❌
> No session-level "exclude without delete" mechanism found in `server/services/`. (The one repo hit for "quarantine" is `statewave-admin/README.md`'s unrelated macOS Gatekeeper `xattr -cr` instruction.)

### Auto-resolution ✅
- `server/services/memory_ttl.py:1-16` — stale memories are automatically tombstoned once their per-kind TTL window passes, no manual action required.

### Trust model ❌
> `caller_type`/`caller_id` exist (`docs/capabilities.md`, "Caller identity") but they drive the policy/redaction engine, not a multi-tier trust hierarchy over memory sources in retrieval ranking.

### Explicit forget ✅
- `README.md:153` — `DELETE /v1/subjects/{id}` — "Permanently delete all data for a subject."

---

## Extraction Pipeline

### Auto-extraction ✅
- `README.md:148` — `POST /v1/memories/compile` — "Compile memories from episodes (idempotent)"; no manual per-fact save call needed.

### Content-aware preprocessing ✅
- `server/services/compilers/llm.py:90-91` — extractor is explicitly instructed to skip values inside code blocks/JSON examples/curl output ("Those are illustrations of *shape*, not facts") while still extracting surrounding prose — code and text are filtered differently before extraction.

### Deduplication ✅
- `server/services/dedup.py:1-20` — compile-time near-duplicate collapse: an exact normalized-text pass followed by a semantic (embedding) pass over survivors.

### Quality refinement ✅
- `server/services/reconcile.py:1-25` — a single LLM call returns ADD/UPDATE/DELETE/NONE per candidate fact judged against the semantically nearest existing memories, run after the compiler and before insertion.

### Narrative generation ✅
- `docs/capabilities.md` (Support-agent stack) — "Handoff context packs — compact escalation briefs with health, SLA, and issue context."
- `README.md:156` — `POST /v1/handoff` — "Generate compact handoff context pack."

### Clustering ❌
> `server/services/dedup.py` groups near-duplicates in order to collapse them, not to surface general topic clusters; no separate clustering feature was found.

### Recurrence detection ✅
- `docs/capabilities.md` (Support-agent stack) — "Repeat-issue detection — surfaces prior resolutions when patterns recur."

### Persona extraction ❌

---

## Platform Support

> Connector code itself lives in a separate repo (`statewave-connectors`), not audited here; this section reflects only what the main README documents.

### Claude Code ✅
- `README.md:197` — MCP server connector row: "Copilot / Claude / Cursor / agent memory — ✅ shipped."

### Codex ❌
### OpenCode ❌
### Gemini CLI ❌

### Copilot ✅
- `README.md:197` — same MCP connector row as above.

### Cursor ✅
- `README.md:197` — same MCP connector row as above.

### Windsurf ❌
### OpenClaw ❌
### Hermes ❌
### pi/omp ❌
### Antigravity ❌

---

## Benchmarks

### LoCoMo ✅
- Score: `0.905`
- `statewave-web` repo, `src/pages/BenchmarksPage.tsx:52` — `{ key: 'statewave', ..., locomo: 0.905, lme: 0.967 }`, vs. `mem0-cloud` `0.899` and `mem0-oss` `0.866`.
- `BenchmarksPage.tsx:85` — n = 1,540, "Robust signal", run on mem0's own eval harness with a gpt-4o answerer/judge.

### LongMemEval ✅
- Score: `0.967`
- `BenchmarksPage.tsx:52,86` — n = 30 (matched subset), labeled "Directional" — the page itself flags this as a small-n, non-significance-test result.

### PersonaMem ❌

### Token reduction ❌
> No published token-reduction percentage vs. a defined baseline was found on the benchmarks page or in the docs.

### Methodology open ✅
- `BenchmarksPage.tsx:19,28` — harness is `statewave-memory-benchmarks`, "a fork of mem0's own eval harness."
- `BenchmarksPage.tsx:226` — "The harness is Apache-2.0 and copy-pasteable: clone it and re-run every number yourself."

---

## Notes

1. **Self-reported benchmark numbers.** LoCoMo/LongMemEval scores are published on Statewave's own marketing site, not an independent leaderboard — but the harness itself is public, Apache-2.0, and stated to be a fork of mem0's own eval harness (not authored by Statewave), and the same page discloses its own weak points (n=30 LongMemEval, no BEAM number claimed). This meets the CONTRIBUTING.md bar for "published benchmarks with methodology" but reviewers may want to independently re-run the harness.
2. **Platform Support is undercounted by design.** Statewave's connectors (including MCP) live in a separate `statewave-connectors` repo that wasn't available to audit alongside the core server; only the platforms named explicitly in the core README's connector table are marked ✅. It's likely — but unverified here — that Codex/OpenCode/Gemini CLI/etc. also work over the same generic MCP server.
3. **Scheduled/autonomous** is marked ✅ for a narrow, internal maintenance loop (hourly TTL tombstoning), not a user-facing scheduled-task feature — see the citation for exactly what it does.
