# MarsNMe — Evidence

> Every ✅ claim backed by public README, source code (server.mjs), migrations, or CHANGELOG.
> Repo: [marsmanleo/MarsNMe](https://github.com/marsmanleo/MarsNMe) (5 stars, JS/Python/Shell/PLpgSQL, Apache 2.0, created 2026-05-14)
> Version: 0.1.8

---

## Repository Metadata

- **description**: "Agent-agnostic AI memory MCP — never forget a conversation again"
- **deployment**: MCP gateway (streamable HTTP/SSE), Docker Compose, self-hosted Supabase, Cloudflare tunnel demo
- **storage**: Supabase (PostgreSQL + pgvector), two-tier: short-term (`memories`) + long-term (`marsvault_chunks`)
- **integration**: MCP (13 tools, `streamable-http` transport), OAuth 2.1 bearer auth, REST API via Supabase
- **setup**: `curl -fsSL https://marsnme.com/install.sh | bash` or `npx @marsnme/mcp-gateway`
- **license**: Apache-2.0
- **created**: 2026-05-14 (first public release v1.0.0)
- **docs**: https://marsnme.com, https://github.com/marsmanleo/MarsNMe/tree/main/docs
- **package**: `@marsnme/mcp-gateway` on npm, registered in MCP Registry, Glama, LobeHub

---

## Architecture

### webUi ❌
- No evidence of a built-in web dashboard or memory browser UI.
- `marsnme.com` is a landing page with install instructions and demo GIFs — not a memory management interface.
- No admin panel, search UI, or visual graph mentioned in README or source.

### offline ❌
- Requires Supabase (external or Docker-hosted Postgres) for storage.
- Requires Jina API key for embeddings — no local embedding model option. `JINA_API_KEY` is marked as required in `server.json`.
- Docker Compose runs Postgres + pgvector locally but Jina API calls still go external.
- Evidence: `server.json` → `JINA_API_KEY` is `isRequired: true`. `server.mjs` → `JINA_EMBEDDING_API_URL = 'https://api.jina.ai/v1/embeddings'`.

### privacy ✅
- `README.md` — "Data ownership: Your own Supabase — zero vendor lock-in"
- `README.md` — "Self-hostable: Full control", "Your own Supabase project"
- All data stays in the user's Supabase instance. No telemetry to MarsNMe servers.
- `SECURITY.md` present in repo.

### export ❌
- No built-in export functionality.
- Data resides in user-owned Supabase, so standard Postgres tools (`pg_dump`, Supabase dashboard) can export — but no first-class export feature.
- No markdown export, JSON dump, or data portability tool mentioned.

### multiAgent ❌
- Multi-profile via `MCP_PROFILE` isolates schemas (coco/toto/arbitrary profile IDs) — but this is memory isolation, not agent-to-agent collaboration.
- No cross-agent memory sharing, agent directory, pub/sub events, or federated memory.
- Multiple MCP clients can connect to the same profile, but there's no agent-aware routing or inter-agent communication.

### llmFlex ❌
- Single embedding provider: Jina AI (`jina-embeddings-v3`, 1024 dimensions).
- `server.json` → `JINA_API_KEY` required. `server.mjs` → hardcoded `JINA_EMBEDDING_MODEL = 'jina-embeddings-v3'`.
- No support for alternative embedding backends (OpenAI, Voyage, local, etc.).
- The system is "LLM-agnostic" only in the sense of being agent-platform-agnostic, not embedding-model-agnostic.
- Other LLM calls (none by the gateway itself) are delegated to the connected agent.

---

## Data Model

### entities ❌
- No entity extraction pipeline. No `entities` table or entity tracking.
- No named-entity recognition, entity linking, or entity graph.

### actions ❌
- No action/relationship tracking. No typed edges or relationship table.
- No `works_at`, `founded`, `attended` or similar link verbs.

### keywords ✅
- `tags` field on both `memories` (text[]) and `marsvault_chunks` (text[]).
- Source: migration `20260504052744` → `tags text[] not null default '{}'` on both tables.
- `server.mjs` → `normalizeTags()` function validates and limits tags (max 30, trimmed, non-empty).
- `memory_ingest` tool accepts user-supplied tags. Fixed tags applied: `[profile, 'insight']` for ingest.
- `health_check` aggregates tag frequencies for topic richness analysis.

### context ✅
- Rich contextual metadata on every memory/chunk entry.
- Short-term (`memories`): `session_id`, `source`, `tags`, `agent_body`, `environment`, `promoted`, `expires_at`.
- Long-term (`marsvault_chunks`): `body`, `visibility`, `type`, `date`, `origin`, `source_file`, `section`, `source_session_id`, `source_tool`, `source_user_note`.
- Source: migrations `20260504052744`, `20260513213800`, `20260517183000`, `20260517194000`.

### source ✅
- Strong source attribution model.
- `source` field on memories (validated against whitelist: `perplexity`, `cursor`, `warp`, `openclaw`, `hermes` for `coco` profile).
- Source registry table (`source_registry`) for runtime whitelist management via `MCP_SOURCE_MODE=registry`.
- `origin` field on chunks tracking the ingestion pipeline source.
- `source_tool`, `source_session_id` on chunks for provenance chain.
- `server.mjs` → `validateMemorySource()`, `MEMORY_SOURCE_WHITELIST`, `SOURCE_REGISTRY_TABLE`.

### emotional ❌
- `mood` field on `session_boot`/`session_close` as optional free-text string — no emotional analysis, sentiment scoring, or emotion tagging.
- No emotional state model.

### conflict ✅
- `health_check` tool includes `detect_conflicts` with configurable parameters:
  - `conflict_similarity_threshold` (default 0.85)
  - `conflict_window_days` (default 14)
  - `conflict_match_count`, `conflict_scan_limit`, `conflict_neighbor_limit`
- `detect_marsvault_conflicts()` PostgreSQL function in migration `20260513222500`:
  - Uses vector similarity with LATERAL JOIN neighbor search
  - Returns paired chunks with similarity scores, content, tags for manual review
- Conflict classification: within `conflict_window_days` → CONFLICT, beyond → SUPERSEDED.

### layeredMemory ✅
- Two-tier memory architecture:
  - **Short-term**: `memories` table, ~30 day TTL (`expires_at = now() + interval '30 days'`)
  - **Long-term**: `marsvault_chunks` table, persistent with upsert dedup via content_hash
- Visibility layers: `private`, `shared`, `global` on chunks
- Profile isolation: separate Postgres schemas per `MCP_PROFILE`
- Memory promotion: `promoted` flag on short-term memories, `source_memory_id` FK linking chunks back to parent memory
- `recall` tool supports filtered retrieval by `body`, `visibility`, `type`
- README: "Short-term (TTL) + long-term (semantic)"

### timeTravel ❌
- No timeline view, temporal query, or time-travel capability.
- `created_at` and `date` timestamps exist but no narrative timeline or event-sequencing feature.

### schemaFields (count: 28) ✅
**memories table (12 fields)**:
`id`, `body`, `source`, `session_id`, `tags`, `promoted`, `promoted_at`, `created_at`, `expires_at`, `embedding`, `agent_body`, `environment`

**marsvault_chunks table (23 fields)**:
`id`, `content`, `embedding`, `source_file`, `section`, `body`, `visibility`, `tags`, `type`, `date`, `content_hash`, `origin`, `created_at`, `updated_at`, `source_memory_id`, `source_session_id`, `source_tool`, `source_user_note`, `deprecated_at`, `deprecated_reason`, `superseded_by`, `agent_body`, `environment`

**Additional tables** (not counted in schemaFields): `memory_tool_usage` (telemetry), `source_registry` (source management), `memory_daily_lifecycle` (session rhythm).

Unique field names: 28 (id, embedding, tags, agent_body, environment, created_at appear in both tables).
Count: 12 + 23 - 7 overlapping = 28 unique fields.

Sources: migrations `20260504052744`, `20260513213800`, `20260517183000`, `20260517194000`, `20260517200500`.

---

## Search & Retrieval

### fulltext ❌
- No full-text search. No BM25, FTS5, tsvector, or lexical search.
- All search is semantic/vector via Jina embeddings.

### semantic ✅
- Jina embeddings v3, 1024 dimensions, stored as `pgvector` `vector(1024)`.
- `search_memories`: semantic search over short-term memories via `search_memories_semantic()` PostgreSQL function.
- `recall`: semantic search over long-term chunks via `search_marsvault_chunks_semantic()` PostgreSQL function.
- HNSW index on `memories.embedding` for millisecond retrieval.
- IVFFlat index (100 lists) on `marsvault_chunks.embedding`.
- Filtering by `min_similarity`, `scope` (this_body/all_bodies), `agent_body`, `environment`, `source`, `type`, `visibility`, `body`.
- Source: migration `20260504052744` → embedding column + HNSW/IVFFlat indexes + search functions.

### hybrid ❌
- No BM25 + vector hybrid search. No reciprocal-rank fusion.
- Search is purely semantic/vector-based. No keyword component.

### deep ❌
- No deep search, multi-hop reasoning, gap analysis, or LLM-synthesized answers.
- No "think" or "synthesize" mode.

### codeGraph ❌
- No code-symbol graph, AST traversal, or source-code-parsing graph.

### docsSearch ❌
- No indexed documentation search.
- `docs/` directory exists but no searchable documentation index.

### factQuery ❌
- No structured fact queries. No graph traversal or expert routing.

### timeline ❌
- No timeline view, temporal query, or chronological event tracking.

### searchModes (count: 2) ✅
Two distinct search surfaces with different schemas:
1. `search_memories` — semantic search over short-term `memories` with source/scope/time filters
2. `recall` — semantic search over long-term `marsvault_chunks` with body/visibility/type/scope filters

Plus listing: `list_memories` returns recent entries by time (not search, a listing operation).

All use the same underlying mechanism (Jina embedding → pgvector cosine similarity) but target different tables with different filter schemas.

### dataSources (count: 5) ✅
Five built-in source types with whitelist validation:
- `perplexity`, `cursor`, `warp`, `openclaw`, `hermes` (for `coco` profile)
- `toto` profile: `perplexity`, `cursor`, `warp`, `openclaw`
- Source registry table supports dynamic extension (`MCP_SOURCE_MODE=registry`, `MCP_EXTRA_SOURCES` env var)
- Source-to-agent-body mapping: `SOURCE_TO_AGENT_BODY_MAP` in server.mjs
- Source whitelist enforced by PostgreSQL CHECK constraint and server-side validation

---

## Knowledge Lifecycle

### decay ✅
- TTL-based expiry on short-term memories: default `expires_at = now() + interval '30 days'`
- `search_memories` and `list_memories` support `unexpired_only: true` filter
- `health_check` includes `alert_window_hours` for proactive expiry warning
- `expires_at` overridable per-memory via `insert_memory`
- Source: migration `20260504052744` → `expires_at timestamptz not null default (now() + interval '30 days')`

### supersede ✅
- `superseded_by` foreign key on `marsvault_chunks` pointing to replacement chunk
- `deprecated_at` timestamp and `deprecated_reason` text for deprecation tracking
- `demote_memory` MCP tool: marks chunk as deprecated with optional `superseded_by` link
- Source: migration `20260517200500` → `superseded_by uuid` with FK constraint, `deprecated_at`, `deprecated_reason`

### contradiction ✅
- `detect_marsvault_conflicts()` PostgreSQL function:
  - Cross-chunk vector similarity comparison
  - Exclusion of same-content-hash pairs
  - Configurable threshold (default 0.85), neighbor limit, scan limit
- Integrated into `health_check` tool with `conflict_similarity_threshold`, `conflict_window_days` parameters
- Classification: within window → CONFLICT, beyond window → SUPERSEDED
- Source: migration `20260513222500` → full conflict detection implementation

### quarantine ✅
- `deprecated_at` timestamp acts as soft-delete marker on chunks
- `soft_forget` MCP tool: expires short-term memory rows early without hard delete
- Deprecated chunks excluded from recall by default behavior (though not explicitly filtered in current search functions — filtering is application-level)
- Source: migrations `20260517200500`, `20260517231000`

### autoResolve ❌
- No automatic conflict resolution or memory consolidation pipeline.
- Conflict detection identifies issues but does not auto-resolve them.
- Dream cycle (`dream_runner.py`) generates digests and ingests them — but this is scheduled ingestion, not autonomous conflict resolution.
- The "dream" is content generation + ingestion, not a reflection/repair loop.

### trustModel ❌
- Source whitelist is binary (allowed/blocked), not tiered trust.
- No source-tier ranking, confidence scoring, or trust-weighted retrieval.
- No differentiation between user-authored and agent-generated memory.

### explicitForget ✅
- `soft_forget` tool: batch-expire short-term memories by UUID list, with optional `reason` and `forgotten_at`
- `demote_memory` tool: mark long-term chunks as deprecated with `deprecated_reason` and optional `superseded_by`
- `soft_forget` supports up to 50 IDs per call
- Source: migration `20260517200500` → `deprecated_at`, `deprecated_reason`, `superseded_by` columns. `server.mjs` → `soft_forget` handler.

---

## Extraction Pipeline

### autoExtract ❌
- No automatic extraction on memory insert.
- No entity extraction, fact extraction, or LLM-based synthesis pipeline.
- Content is stored verbatim (short-term) or paragraph-chunked (long-term).

### contentPreproc ❌
- Basic chunking: paragraph-boundary-aware splitting with configurable `max_chunk_chars` (300-3000).
- Tag normalization: trimming, validation, dedup.
- Source name normalization to lowercase alphanumeric pattern.
- No markdown parsing, content sanitization, quality gating, or format detection.
- Not a substantive preprocessing pipeline.

### dedup ✅
- Content-hash deduplication on long-term chunks.
- `content_hash text not null` on `marsvault_chunks`.
- Unique index on `(source_file, section, content_hash, body)` — prevents duplicate chunk inserts.
- Upsert behavior in the `memory_ingest`/`dream_ingest` flow.
- Source: migration `20260504052744` → unique index `coco_marsvault_chunks_upsert_key`.

### qualityRefine ❌
- No reranking, relevance scoring beyond cosine similarity, or multi-query expansion.
- No citation verification or quality scoring.

### narrative ❌
- No narrative synthesis. Dream runner generates markdown digests but these are structured reports, not narrative memory summaries.
- No prose synthesis from memory contents.

### clustering ❌
- No clustering or topic modeling.
- `health_check` aggregates tag frequencies for "rich/sparse/volatile" topic classification, but this is counting, not clustering.

### recurrence ✅
- Dream runner (`soul-memory/scripts/dream_runner.py`) is designed for recurring execution:
  - Configurable via `DREAM_MODE` (lite/standard/pro)
  - Modular providers: recent_memory, semantic_memory, issue_signals, repo_scan, soul_context
  - Generates digests and ingests them back via `dream_ingest` MCP tool
  - Designed to run via cron/systemd timer
- README: "Dream Runner is public-friendly and can run without Hermes private environment"
- `DREAM_ENABLED=true DREAM_MODE=lite python3 soul-memory/scripts/dream_runner.py`

### persona ❌
- Profile-based isolation (coco/toto) resembles persona separation but is not persona extraction.
- `session_boot` has identity/workflow/status recall patterns — a daily rhythm with persona-aware queries.
- No automatic persona extraction, trait learning, or personality modeling from conversations.
- The "soul" concept (SOUL.md files for dream context) is static configuration, not extracted persona.

---

## Platform Support

### p_claude ✅
- `README.md` — "Claude Desktop" MCP connection guide with `claude_desktop_config.json` config
- `AGENTS.md` — "This repository is the public edition of MarsNMe"
- Claude Desktop HTTP MCP integration documented and tested

### p_codex ❌
- No mention of OpenAI Codex in README, AGENTS.md, or any file.

### p_opencode ❌
- No mention of OpenCode.

### p_gemini ❌
- No mention of Gemini CLI.

### p_copilot ❌
- No mention of GitHub Copilot.

### p_cursor ✅
- `README.md` — "Cursor" MCP connection guide with step-by-step setup
- `skills/cursor/memory-daily-boot/rule.mdc` — Cursor-specific skill template
- Explicitly documented and supported

### p_windsurf ❌
- No mention of Windsurf.

### p_openclaw ✅
- `server.mjs` — `openclaw` in `PROFILE_CONFIGS.coco.sourceWhitelist`
- `SOURCE_TO_AGENT_BODY_MAP` maps `openclaw` → `desktop`
- Source type `openclaw` is a first-class citizen with body routing

### p_hermes ✅
- `server.mjs` — `hermes` in `PROFILE_CONFIGS.coco.sourceWhitelist`
- `hermes_digest_runner.py` — optional Hermes digest runner
- `HERMES_*` environment variables throughout dream runner
- README: "Hermes digest runner" referenced

### p_warp ✅
- `README.md` — "Warp" MCP connection guide
- `skills/warp/memory-daily-boot/prompt.md` — Warp-specific skill template
- Source type `warp` in whitelist, mapped to `warp` agent body

### p_perplexity ✅
- `README.md` — "Perplexity" MCP connection guide with Space Settings instructions
- `skills/perplexity/memory-daily-boot/SKILL.md` — Perplexity-specific skill template
- Source type `perplexity` in whitelist, mapped to `perplexity-web` agent body

### p_pi ❌
- No mention of pi.ai.

### p_antigravity ❌
- No mention of Antigravity.

---

## Benchmarks

### b_locomo ❌
- No mention of LoCoMo benchmark.

### b_longmemeval ❌
- No mention of LongMemEval benchmark.

### b_personamem ❌
- No mention of PersonaMem benchmark.

### b_token ❌
- No mention of TokenBench.
- Usage telemetry exists (`memory_tool_usage` table + `writeToolUsageTelemetry()` in server.mjs) but no published token benchmarks.

### b_methodology ❌
- No evaluation methodology or benchmark framework.
- `README.md` mentions "3 months of daily use across 4 AI tools" as a user story — anecdotal, not a structured evaluation.
- No metric glossary, reproducibility commitment, or public evaluation dataset.

---

## Feature Totals (quick reference)

| Category | Present / Total | Details |
|---|---|---|
| Architecture | 1/6 | privacy only |
| Data Model | 6/10 | keywords, context, source, conflict, layeredMemory, schemaFields(28) |
| Search | 3/10 | semantic, searchModes(2), dataSources(5) |
| Lifecycle | 5/7 | decay, supersede, contradiction, quarantine, explicitForget |
| Extraction | 1/8 | dedup only |
| Platform | 6/13 | p_claude, p_cursor, p_openclaw, p_hermes, p_warp, p_perplexity |
| Benchmarks | 0/5 | — |

**Total: 22/59 features present (37%)**

---

## Key Differentiators

1. **Two-tier memory with promotion**: Short-term memories (30-day TTL) can be promoted to long-term persistent chunks via `memory_ingest` with FK backlinks (`source_memory_id`). The promotion is explicit (agent-driven), not automatic.

2. **Cross-platform, not cross-agent**: MarsNMe's strength is making the same memory layer accessible from 5+ different AI tools (Claude, Cursor, Warp, Perplexity, OpenClaw/Hermes). Each tool connects via standard MCP HTTP transport. The vision is continuity across tools, not agent-to-agent collaboration.

3. **Data sovereignty by construction**: All data lives in the user's own Supabase project. Zero vendor lock-in. The gateway is stateless — Supabase is the source of truth.

4. **Profile isolation via Postgres schemas**: `MCP_PROFILE` creates a new schema for each agent/use case. Legacy profiles `coco`/`toto` demonstrate the two-agent pattern. This is schema-level multi-tenancy, not row-level.

5. **Source validation with registry**: Memory writes are validated against a source whitelist with PostgreSQL CHECK constraints. The `source_registry` table + `MCP_SOURCE_MODE=registry` allows runtime whitelist management without restart.

6. **Dream cycle as scheduled ingestion**: The dream runner collects recent memories, semantic context, repo scans, and issue signals → generates structured digests → ingests them back as long-term chunks. This is content generation for continuity, not autonomous memory refinement.

---

## Notable Gaps

- **No entity model**: No entities, relationships, or knowledge graph. Pure flat vector storage.
- **Search is vector-only**: No BM25, hybrid RRF, or multi-modal search. Jina embeddings are the sole retrieval mechanism.
- **No auto-extraction**: No LLM-based extraction pipeline. All structuring is explicit (manual promotion, manual tagging).
- **No benchmarks**: No evaluation framework, no published scores. User story is anecdotal (3 months daily use).
- **Single embedding provider**: Locked to Jina AI. No local embedding model option, no provider flexibility.
- **No web dashboard**: No built-in memory browser, admin UI, or visualization.
- **No export tooling**: No first-class data portability beyond Supabase's native pg_dump.
- **No narrative synthesis**: No gap analysis, contradiction narrative, or memory summary generation from stored data.
