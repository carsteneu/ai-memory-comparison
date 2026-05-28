# TencentDB-AM — Evidence

> Every ✅ claim backed by public source code or documentation.
> Audit date: 2026-05-28. Source: GitHub `Tencent/TencentDB-Agent-Memory` main branch, README, `openclaw.plugin.json`, `src/` source.

## Architecture

### Layered memory (L0→L3) ✅
- `README.md` — "Memory Layering: Progressive Disclosure with Heterogeneous Storage." Explicit L0→L1→L2→L3 semantic pyramid:
  - L0 Conversation: raw dialogue
  - L1 Atom: atomic facts extracted from conversation
  - L2 Scenario: scene blocks grouping related atoms
  - L3 Persona: user profile derived from scenarios
- `README.md` — Architecture diagram shows pyramid with L0→L3 levels. "Lower layers preserve evidence; upper layers preserve structure."
- `src/core/tdai-core.ts` — 4-layer system: L0 conversation recording, L1 memory extraction, L2 scene block management, L3 persona generation.
- `SKILL-DIAGNOSTIC-EXPORT.md` — Memory plugin data structure confirms: `conversations/` (L0), `records/` (L1), `scene_blocks/` (L2), `persona.md` (L3).

### Offline ✅
- `README.md` — "TencentDB Agent Memory delivers fully local long-term memory for AI Agents via a 4-tier progressive pipeline, with zero external API dependencies."
- `README.md` — "Local backend: SQLite + sqlite-vec, ready to use out of the box."
- `src/config.ts` — `storeBackend: "sqlite"` is the default, with `sqlite-vec` for vectors. No cloud dependency required.

---

## Data Model

### Entities — **FALSE CLAIM** ✅→❌
- The `MemoryRecord` type (`src/core/record/l1-reader.ts`) has these fields: `id`, `content`, `type`, `priority`, `scene_name`, `source_message_ids`, `metadata`, `timestamps`, `createdAt`, `updatedAt`, `sessionKey`, `sessionId` = 12 fields.
  - The `type` field is memory *classification*: `persona`, `episodic`, `instruction` — not entity/NER extraction.
- No evidence of NER, entity extraction, or a separate entity table anywhere in the codebase. Search across `src/` reveals no `entity`, `NER`, `spacy`, or `extract_entities` references.
- Per CRITERIA.md: "Extracts or stores named entities (files, people, systems, packages) as separate structured fields or database tables, not just free-text mentions." — TencentDB-AM does NOT do this.
- **Recommendation: change `entities: true` to `entities: false`.**

### Schema fields — 12 ✅
- `MemoryRecord` interface in `src/core/record/l1-reader.ts`: `id`, `content`, `type`, `priority`, `scene_name`, `source_message_ids`, `metadata`, `timestamps`, `createdAt`, `updatedAt`, `sessionKey`, `sessionId` = exactly 12 fields.
- `L1SearchResult` in `src/core/store/types.ts`: `record_id`, `content`, `type`, `priority`, `scene_name`, `score`, `timestamp_str`, `timestamp_start`, `timestamp_end`, `session_key`, `session_id`, `metadata_json` = 12 fields (mirrors MemoryRecord with snake_case).
- **12 fields verified.** Not counting auto-generated DB internal columns.

---

## Search & Retrieval

### Full-text (BM25/FTS5) ✅
- `README.md` — "Hybrid retrieval: BM25 + vector + RRF — supports both keyword and semantic recall."
- `src/config.ts` — BM25 config with `language: "zh" | "en"` and `enabled: true` default.
- `src/core/hooks/auto-recall.ts` — `searchByKeyword()` uses FTS5 BM25: `vectorStore.isFtsAvailable()`, `vectorStore.searchL1Fts()`, `buildFtsQuery()`. FTS5 is used for keyword search with BM25 ranking.
- `src/core/store/types.ts` — `IMemoryStore` interface includes `searchL1Fts(ftsQuery, limit)` with `L1FtsResult` type that has BM25-derived score.
- `src/config.ts` — BM25 uses `@tencentdb-agent-memory/tcvdb-text` for local sparse vector encoding.

### Semantic/vector ✅
- `README.md` — Embedding-based vector search. Config supports OpenAI-compatible remote embedding providers.
- `src/core/hooks/auto-recall.ts` — `searchByEmbedding()`: Vector similarity search via `embeddingService.embed()` + `vectorStore.searchL1Vector()`.
- `src/core/store/types.ts` — `searchL1Vector(queryEmbedding, topK)` with `L1SearchResult.score` (cosine similarity, 0-1).
- `src/config.ts` — `embedding` config group with `provider`, `baseUrl`, `apiKey`, `model`, `dimensions` for OpenAI-compatible remote embedding.

### Hybrid (BM25+Vector+RRF) — **FALSE CLAIM** ❌→✅
- The data.js says `hybrid: false`, but the evidence is overwhelming:
- `README.md` — "Hybrid retrieval: BM25 + vector + RRF — supports both keyword and semantic recall."
- `src/config.ts` — `recall.strategy` default is `"hybrid"` with enum: `"keyword" | "embedding" | "hybrid"`. Description: "hybrid(RRF融合，推荐)" = "hybrid (RRF fusion, recommended)."
- `src/core/hooks/auto-recall.ts` — `searchHybrid()`: runs FTS5 keyword + embedding in parallel, merges with Reciprocal Rank Fusion (RRF): `rrfScore = 1 / (RRF_K + rank + 1)` where `RRF_K = 60`. Results from both strategies are merged and ranked by combined RRF score.
- `src/core/store/types.ts` — `IMemoryStore.searchL1Hybrid()` declared as optional native hybrid search method for backends that support it (TCVDB).
- **Recommendation: change `hybrid: false` to `hybrid: true`.**

---

## Extraction Pipeline

### Auto-extraction ✅
- `README.md` — "Once enabled, TencentDB Agent Memory automatically handles conversation capture, memory extraction, scene aggregation, persona generation, and recall before the next turn."
- `src/core/tdai-core.ts` — `performAutoCapture()` and `performAutoRecall()` are the two core capabilities. Auto-capture runs on `handleTurnCommitted()` (mapped to OpenClaw `agent_end` / Hermes `sync_turn()`).
- `index.ts` — Full pipeline: `before_prompt_build` hook for auto-recall, `agent_end` hook for auto-capture, pipeline scheduler for L1→L2→L3 progression.
- `src/config.ts` — `pipeline.everyNConversations` (default 5): triggers L1 every N turns. `enableWarmup: true`: starts at 1 turn, doubles to N.

### Deduplication — **FALSE CLAIM** ❌→✅
- The data.js says `dedup: false`, but:
- `src/config.ts` — `extraction.enableDedup` (default `true`): "L1 smart dedup (based on vector similarity or keywords for conflict detection)."
- `openclaw.plugin.json` — `extraction.enableDedup` schema: "L1 智能去重（基于向量相似度或关键词进行冲突检测）" = "L1 smart dedup (conflict detection based on vector similarity or keywords)."
- `index.ts` — Config logging confirms: `extraction(dedup=${cfg.extraction.enableDedup})`. Feature is enabled by default.
- **Recommendation: change `dedup: false` to `dedup: true`.**

### Persona extraction ✅
- `README.md` — L3 Persona: "distills fragmented conversations into structured personas and scenes." "PersonaMem accuracy from 48% to 76%."
- `src/config.ts` — `persona` config group: `triggerEveryN` (default 50), `maxScenes`, `backupCount`.
- `src/core/tdai-core.ts` — `createL3Runner()`: dedicated L3 persona runner for persona synthesis.
- `SKILL-DIAGNOSTIC-EXPORT.md` — `persona.md` is the persisted L3 user profile file.

---

## Platform Support

### OpenClaw ✅
- `README.md` — Install command: `openclaw plugins install @tencentdb-agent-memory/memory-tencentdb`.
- `openclaw.plugin.json` — Full OpenClaw plugin manifest with configSchema, contracts.tools, commandAliases.
- `index.ts` — Complete OpenClaw plugin registration: `registerTool()`, `registerCli()`, `api.on("before_prompt_build")`, `api.on("agent_end")`, `api.on("before_message_write")`, `api.on("gateway_stop")`.
- npm badge in README shows published package `@tencentdb-agent-memory/memory-tencentdb`.

### Hermes ✅
- `README.md` — Hermes section with Docker build/run instructions. "Hermes (Docker, requires version ≥ 0.3.4)."
- `hermes-plugin/memory/memory_tencentdb/` — Full Hermes provider directory with `__init__.py`, `client.py`, `supervisor.py`, `plugin.yaml`, `README.md`.
- `hermes-plugin/memory/memory_tencentdb/README.md` — Comprehensive Hermes provider documentation: architecture diagram, setup instructions, lifecycle hooks (`prefetch`, `sync_turn`, `shutdown`, `on_session_end`), LLM tools (`memory_tencentdb_memory_search`, `memory_tencentdb_conversation_search`).

---

## Benchmarks

### PersonaMem — 76% ✅
- `README.md` — Memory benchmark table: PersonaMem "OpenClaw Success" = 48%, "With Plugin" = 76%, "Relative Δ" = "+59%".
- The 76% figure is the accuracy WITH the TencentDB-AM plugin enabled, and represents a published score claim.

### Token reduction — 61% ✅
- `README.md` — WideSearch benchmark: "OpenClaw Tokens" = 221.31M, "With Plugin Tokens" = 85.64M, "Relative Δ" = "−61.38%".
- The 61% figure is the token reduction achieved on the WideSearch benchmark when using the plugin.

### Methodology open — **FALSE CLAIM** ✅→❌
- The README shows a benchmark results table but does NOT publish:
  - A link to a benchmark repository or evaluation framework
  - Reproduction scripts or commands
  - Dataset details or links
  - Configuration for reproducing the results
  - Any external paper, report, or methodology document
- Per CRITERIA.md: "Benchmark methodology is publicly documented and reproducible (scripts, dataset links, configuration). Claims without reproduction steps are not considered 'methodology open'."
- While the README notes that "SWE-bench runs 50 consecutive tasks per session," this is a brief methodology note, not a published reproduction framework.
- No benchmark repo analogous to `mem0ai/memory-benchmarks` exists for TencentDB-AM.
- **Recommendation: change `b_methodology: true` to `b_methodology: false`.**

---

## Claims NOT present (marked false in data.js) — verified correct

The following features are correctly marked `false` in data.js. No public evidence found:

**Data Model:** actions, keywords, anticipatedQueries, triggerRules, domainTag, taskType, context, source, originTrust, emotional, conflict, timeTravel — all ❌ (MemoryRecord has 12 fields but none match these structured metadata categories)

**Search:** deep, codeGraph, docsSearch, factQuery, timeline — all ❌ (FTS5 + vector + RRF hybrid covers keyword/embedding, but no deep search, code graph, doc search, fact query, or timeline view)

**Lifecycle:** decay, supersede, contradiction, quarantine, autoResolve, trustModel, explicitForget — all ❌ (no forgetting mechanism, no memory versioning/supersede, no conflict detection beyond dedup, no quarantine, no auto-resolution, no explicit delete tool)

**Extraction:** contentPreproc, qualityRefine, narrative, clustering, recurrence — all ❌ (extraction is LLM-based atom extraction; no content-type-aware preprocessing, no quality refinement pass, no narrative generation, no clustering, no recurrence detection)

**Architecture:** proxy, webUi, multiAgent — all ❌ (plugin-based integration, no proxy layer; no visual UI/TUI; single-agent design)

**Platforms:** p_claude, p_codex, p_opencode, p_gemini, p_copilot, p_cursor, p_windsurf, p_pi, p_antigravity — all ❌ (only OpenClaw and Hermes supported)

---

## Audit Notes

1. **entities: true → false**: No entity/extraction NER pipeline exists. The `type` field on MemoryRecord classifies memories as persona/episodic/instruction — this is memory categorization, not entity extraction per CRITERIA.md.

2. **hybrid: false → true**: Substantial correction. The system's default recall strategy IS hybrid (RRF fusion of FTS5 BM25 + embedding). This is the recommended mode with dedicated implementation in `searchHybrid()`. The config enum and documentation consistently present hybrid as the primary strategy.

3. **dedup: false → true**: Config has `enableDedup: true` by default with description of vector-similarity-based deduplication. This is a first-class configuration option in the OpenClaw plugin schema.

4. **b_methodology: true → false**: No published benchmark repository, scripts, or reproduction methodology. Results are stated in the README table but without verifiable reproduction steps. This doesn't meet the CRITERIA.md threshold for "methodology open."

5. **b_personamem: "76%"** and **b_token: "61%"**: These are percentage improvement claims (% accuracy with plugin, % token reduction), not absolute benchmark scores. The README presents them as comparative metrics ("OpenClaw Success" vs "With Plugin"). The data.js format represents them correctly as percentage strings.
