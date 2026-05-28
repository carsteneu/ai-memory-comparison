# Memora — Evidence

> **GitHub**: https://github.com/agentic-box/memora
> **Version**: v0.2.29 (May 27, 2026), 30 releases since v0.1.0
> **Stars**: 407 | **Forks**: 50 | **License**: MIT
> **Language**: Python (69.9%), TypeScript (8.2%), HTML (19.8%)
> **Created**: 2025-11-11 (first release v0.1.0)
> **Deployment**: Local MCP server + optional cloud (S3/R2/D1)
> **Storage**: SQLite (local) with optional cloud sync (S3/R2) or Cloudflare D1
> **Integration**: MCP (standard stdio transport, optional streamable-http/sse)
> **Setup**: `pip install git+https://github.com/agentic-box/memora.git`
> **Docs**: README-only (https://github.com/agentic-box/memora#readme); no separate docs site
> **Description**: MCP memory layer for AI agents — structured storage, semantic retrieval, graph relations, source-backed cross-session context.

---

## Vital Signs

### Stars ✅
- `[README]` — 407 stars shown on repo header

### Language ✅
- `[repo language bar]` — Python 69.9%, HTML 19.8%, TypeScript 8.2%, Shell 1.8%, Lua 0.3%

### License ✅
- `[LICENSE]` — MIT license
- `[pyproject.toml]` — `license = "MIT"`

### Created ✅
- `[releases/page=3]` — v0.1.0 tagged 2025-11-11 (first public release)

---

## Architecture

### webUi ✅
- `[README Live Graph Server]` — Built-in HTTP server on port 8765 serving interactive knowledge graph visualization
- `[README Graph UI Features]` — Details Panel, Timeline Panel, History Panel, Chat Panel, Time Slider, Real-time SSE updates, Mermaid rendering, tag/section filters
- `[memora/graph/]` — Graph frontend (D3.js/vis-network)

### offline ✅
- `[README Install]` — Works with local SQLite (default: `~/.local/share/memora/memories.db`)
- `[README Embeddings]` — sentence-transformers backend runs fully offline, TF-IDF has zero deps
- `[README Config Local DB]` — Local DB config shown as first option, cloud optional

### privacy ✅
- `[README Config S3/R2]` — `MEMORA_CLOUD_ENCRYPT=true` to encrypt database before cloud upload
- `[storage.py]` — `_redact_secrets()` detects and redacts API keys, passwords, credit cards before storage
- Local-only mode: no cloud dependency, all data stays on disk

### export ✅
- `[server.py]` — `memory_export` tool exports all memories as structured data
- `[README Knowledge Graph Export]` — `memory_export_graph` exports static HTML graph visualization
- `[README Export/Import]` — Backup and restore with merge strategies

### multiAgent ✅
- `[README Event Notifications]` — "Poll-based system for inter-agent communication"
- `[schema.py]` — `memories_events` table (id, memory_id, tags, timestamp, consumed)
- `[server.py]` — `memory_poll_events` MCP tool for consuming events

### llmFlex ✅ (4+ providers)
- `[README Embeddings]` — Three embedding backends: OpenAI (default), sentence-transformers (local), TF-IDF (local)
- `[README Chat]` — Chat model defaults to `deepseek/deepseek-chat`, falls back to `MEMORA_LLM_MODEL`
- `[README LLM Dedup]` — Works with any OpenAI-compatible API (OpenAI, OpenRouter, Azure)
- `[env vars]` — `OPENAI_API_KEY`, `OPENAI_BASE_URL` for custom endpoints
- Count: OpenAI, OpenRouter, Azure, DeepSeek, plus any OpenAI-compatible = 4+ verified

### cacheOpt ✅
- `[schema.py]` — Per-backend schema cache: `ensure_schema()` runs once per process, not per tool call. D1 latency dropped from 10s+ to ~2s (v0.2.25 release notes)
- `[schema.py]` — Inode-based cache invalidation for `CloudSQLiteBackend`
- `[server.py]` — Tool cooldowns prevent repeated expensive operations (rebuild, dedup, export, import)
- `[storage.py]` — Cached LLM client instance for dedup comparison

---

## Data Model

### actions ✅
- `[schema.py]` — `memories_actions` table: id, memory_id, action, summary, timestamp
- `[storage.py]` — `_log_action()` logs create, update, delete, merge, boost, link operations
- `[README Action History]` — "Track all memory operations (create, update, delete, merge, boost, link) with grouped timeline view"

### keywords ✅ (tags)
- `[schema.py]` — `tags` TEXT column in memories table, stored as JSON array
- `[server.py]` — Tag filters: `tags_any` (OR), `tags_all` (AND), `tags_none` (NOT)
- `[storage.py]` — `_enforce_tag_whitelist()` validates tags against `MEMORA_TAGS` allowlist or `MEMORA_TAG_FILE`
- `[README env vars]` — `MEMORA_ALLOW_ANY_TAG=1` to skip allowlist, `MEMORA_TAGS`, `MEMORA_TAG_FILE`

### taskType ✅
- `[server.py]` — `_infer_type()` detects todo/issue/note/idea/question/warning from content prefixes
- `[server.py]` — `memory_create_todo` and `memory_create_issue` MCP tools with structured status/priority/severity fields
- `[storage.py]` — `_detect_memory_type()` auto-detects issue and TODO from keyword patterns
- `[README Memory Automation Tools]` — Structured tools for TODOs, issues, sections with status tracking

### source ✅
- `[server.py]` — `memory_absorb(facts, source="manual|session_end|post_tool|import", ...)` — explicit source attribution for absorbed facts
- `[storage.py]` — Metadata stores source alongside confidence in absorb flow

### timeTravel ✅
- `[server.py]` — Lineage `follow` parameter: `"full_history"` expands supersession chains, `"latest"` resolves to current version, `"active"` excludes superseded memories
- `[server.py]` — `_digest_memory_preview` + lineage chain expansion for time-travel context
- `[README v0.2.26]` — "Lineage-aware retrieval: `follow` parameter for supersession chain walking"

### schemaFields ✅ (25)
- `[schema.py]` — memories table: id, content, metadata, tags, created_at, updated_at, importance, last_accessed, access_count (9)
- `[schema.py]` — memories_embeddings: memory_id, embedding (2)
- `[schema.py]` — memories_crossrefs: memory_id, related (2)
- `[schema.py]` — memories_events: id, memory_id, tags, timestamp, consumed (5)
- `[schema.py]` — memories_actions: id, memory_id, action, summary, timestamp (5)
- `[schema.py]` — memories_meta: key, value (2)
- Total: 25 structural columns

---

## Search & Retrieval

### fulltext ✅
- `[schema.py]` — `_ensure_fts()` creates FTS5 virtual table on content, metadata, tags
- `[server.py]` — `memory_list(query=...)` uses FTS5 text search when available

### semantic ✅
- `[README Semantic Search]` — Three embedding backends: OpenAI (default), sentence-transformers (local, `pip install memora[local]`), TF-IDF (basic, included)
- `[schema.py]` — `memories_embeddings` table stores vector embeddings
- `[server.py]` — `memory_semantic_search` MCP tool with `top_k`, `min_score`, metadata filters

### hybrid ✅
- `[server.py]` — `memory_hybrid_search` with configurable `semantic_weight` (0.0–1.0)
- `[README v0.2.0]` — "Combines keyword (full-text) and semantic (vector) search using Reciprocal Rank Fusion (RRF)"
- `[storage.py]` — RRF fusion implementation for hybrid search

### timeline ✅
- `[README Graph UI]` — Timeline Panel browses memories chronologically, click to highlight in graph
- `[README Action History]` — Action log of all operations with grouped consecutive entries
- `[README Preview]` — GIF showing timeline panel with chronological memory browser

### searchModes ✅ (4)
- `[server.py]` — `memory_list` (full-text + filter) — FTS5 with tag/metadata/date filtering
- `[server.py]` — `memory_semantic_search` (vector) — embedding-based similarity search
- `[server.py]` — `memory_hybrid_search` (BM25+vector RRF) — hybrid search with tunable weight
- `[server.py]` — `memory_digest` (agent-friendly) — topic-based digest with related memories, TODOs, issues, lineage
- Note: `memory_list_compact` is deprecated, not counted as separate mode

### dataSources ✅ (1)
- Memory content is the single source of retrievable data (no external file indexing, no conversation log search)

---

## Knowledge Lifecycle

### supersede ✅
- `[server.py]` — `memory_absorb` classifies fact→memory relationships as `supersedes`/`superseded_by`
- `[server.py]` — `memory_detect_supersessions` retroactively scans existing memories for supersession pairs
- `[README v0.2.26]` — "6-way relation enum (a_supersedes_b, b_supersedes_a, duplicate, related, contradicts, neither)"
- `[README Memory Linking]` — Edge types include `supersedes`
- `[server.py]` — `follow="active"` excludes superseded memories from retrieval

### explicitForget ✅
- `[server.py]` — `memory_delete(memory_id)` deletes individual memories
- `[server.py]` — `memory_delete_batch(ids)` bulk deletion
- `[README Chat]` — LLM can delete memories from chat ("delete memory #42")

---

## Extraction Pipeline

### contentPreproc ✅
- `[storage.py]` — `_redact_secrets()`: 13 regex patterns detect and redact API keys (OpenAI, Anthropic, AWS), private keys, bearer tokens, GitHub PATs, Slack tokens, passwords, credit cards — applied before storage
- `[storage.py]` — `_validate_content()`: trims whitespace, normalizes newlines (max 2 consecutive), enforces min 3 / max 50000 chars
- `[storage.py]` — `_normalize_tags()`: auto-prefixes generic tags with detected project name
- `[server.py]` — `_infer_type()`: auto-detects todo/issue/note/idea from content prefixes

### dedup ✅
- `[README LLM Dedup]` — `memory_find_duplicates(min_similarity, max_similarity, use_llm=True)` with AI-powered comparison
- `[storage.py]` — `compare_memories_llm()` returns verdict (duplicate/similar/different), confidence, reasoning, suggested_action
- `[server.py]` — `DUPLICATE_THRESHOLD = 0.85` — warning on create when similar memory exists above threshold
- `[server.py]` — `memory_merge(source_id, target_id, merge_strategy="append|prepend|replace")`

### clustering ✅
- `[README Memory Linking]` — `memory_clusters(min_cluster_size=2, min_score=0.3)` "Detect clusters of related memories"
- `[server.py]` — `detect_clusters()` function imported from storage
- `[README Features]` — "cluster detection" listed as knowledge graph feature

---

## Platform Support

### p_claude ✅
- `[README Claude Code]` — Full `.mcp.json` configuration example for Claude Code
- `[README MCP]` — Standard MCP stdio transport
- `[CLAUDE.md]` — Project uses Memora as its own memory system ("Memora is the sole memory system for this project")

### p_codex ✅
- `[README Codex CLI]` — Full `~/.codex/config.toml` configuration example
- Codex is explicitly documented as supported platform

---

## Benchmarks

No published benchmarks found. All benchmark fields unverified.

---

## Features NOT present (verified absent)

The following features were checked and NOT found in code or documentation:

| Feature | Evidence of absence |
|---------|-------------------|
| **entities** | No entity extraction. Schema has no entity table; metadata is a flat JSON dict. |
| **anticipatedQueries** | No anticipated-query field or concept in schema. |
| **triggerRules** | Event system is tag-based polling (`memories_events`), not rule-based triggers. |
| **domainTag** | No domain classification (code/marketing/legal). Tags are freeform. |
| **context** | Metadata is flexible but no dedicated context/why field. Absorb has optional context param but it's not a first-class schema field. |
| **originTrust** | Source attribution exists (absorb's `source` param) but no trust hierarchy or trust scoring. |
| **emotional** | No emotional valence or sentiment tracking. |
| **conflict** | Contradiction classification exists in absorb's LLM path but is not surfaced as a persistent data model feature or retrieval-time conflict flag. |
| **layeredMemory** | No layered memory tiers (working/session/long-term). Single flat `memories` table. |
| **deep** | No raw conversation/thinking search. Only processed memory content is searchable. |
| **codeGraph** | No code graph or AST-aware search. |
| **docsSearch** | No documentation indexing or docs-specific search. |
| **factQuery** | No structured fact metadata query. Metadata filters exist but no dedicated fact query API. |
| **decay** | Importance score has recency-aware calculation for ranking, but no automatic forgetting/decay of memory content. Stale detection (`memory_insights`) flags stale items for review but does not decay them. |
| **contradiction** | Absorb can classify as "contradicts" but this is not a systemic contradiction detection or surfacing feature in retrieval. |
| **quarantine** | No quarantine concept or isolation of suspect data. |
| **autoResolve** | `memory_absorb` can auto-apply (merge, supersede) based on LLM classification, but this is tool-driven, not a background/automatic resolution process. |
| **trustModel** | No trust scoring hierarchy or provenance-weighted retrieval. |
| **autoExtract** | No automatic extraction from conversations or tool output. `memory_absorb` is the intended ingestion path but requires explicit tool invocation. |
| **qualityRefine** | No quality refinement pipeline. |
| **narrative** | `memory_insights` LLM analysis provides themes and summary but does not generate cross-session narratives. |
| **recurrence** | No recurrence pattern detection. |
| **persona** | No persona extraction or user profiling. |
| **singleBinary** | Python package distributed via pip, not a single binary. |
| **proxy** | Standard MCP server, not a transparent proxy. |
