# Shodh-Memory Audit

**Date:** 2026-05-28
**Source:** https://github.com/varun29ankuS/shodh-memory
**Version:** v0.2.0 (latest as of audit)
**Language:** Rust (89.5%)
**Stars:** 215
**License:** Apache-2.0

## URL Correction

The claimed URL `https://github.com/debjitpurohit/shodh` returns **404** — the repository does not exist at that path. The actual repository is `https://github.com/varun29ankuS/shodh-memory`.

## Summary

Shodh-Memory is a Rust-based persistent cognitive memory system for AI agents and robots. Single ~17MB binary, runs fully offline. Implements neuroscience-inspired primitives: Hebbian learning, exponential activation decay, spreading activation, long-term potentiation, three-tier memory hierarchy (working → session → long-term). Exposed via MCP (37 tools), REST API (160+ endpoints), Python/Rust SDKs, and Zenoh transport for ROS2 robotics. Uses MiniLM-L6 embeddings via ONNX, Tantivy BM25 for full-text, RocksDB for storage, custom Vamana HNSW for vector search.

## Claim Audit

### Verified Claims

| Claim | Status | Evidence |
|-------|--------|----------|
| webUi | ✅ Verified | TUI dashboard via `shodh tui` command. Screenshots show semantic recall UI, projects/todos GTD view. Not a web UI but a terminal UI. |
| offline | ✅ Verified | "100% offline" in README. "Runs fully offline: Yes" in comparison table. "Works on air-gapped systems after initial model download." |
| privacy | ✅ Verified | "No API keys. No cloud. No external databases. One binary." Local embeddings, no LLM API calls. |
| fulltext | ✅ Verified | Tantivy 0.25 (BM25) in Cargo.toml. `HybridSearchEngine` with BM25 + Vector + RRF. "Tag search ~1ms." BM25 index backfill in init. |
| semantic | ✅ Verified | "Semantic search 34-58ms." MiniLM-L6 embeddings (384-dim) via ONNX. Three retrieval modes: semantic, associative, hybrid. |
| hybrid | ✅ Verified | `HybridSearchEngine` (BM25 + Vector + RRF + Reranking). "hybrid" retrieval mode in openapi.yaml. Hybrid search module in memory system. |
| decay | ✅ Verified | "activation decay" — "You stop using a memory → it fades over time." `decay.rs` module. Exponential decay: A(t) = A0 · e^(-λt). `Memory::decay_activation()`. |
| explicitForget | ✅ Verified | `forget` MCP tool with 7 criteria: ById, OlderThan, LowImportance, Pattern, ByTags, ByDateRange, All. REST endpoints: `/api/forget/tags`, `/api/forget/date`. |
| autoExtract | ✅ Verified | Claude Code hooks auto-capture context. Temporal fact extraction on `remember()`. Entity extraction (TinyBERT NER). Auto-extraction when `entities` is empty. Segmentation engine with dedup. |
| p_claude | ✅ Verified | "Claude Code" section in README. `claude mcp add shodh-memory -- npx -y @shodh/memory-mcp`. Claude Code hooks setup. |
| p_cursor | ✅ Verified | "Cursor Directory" badge. Config snippet for Cursor MCP. Link to cursor.directory listing. |
| schemaFields=6 | ⚠️ Misleading | API-level `RememberRequest` has 6 fields: `user_id`, `content`, `tags`, `memory_type`, `external_id`, `created_at`. However the internal `Experience` struct has 45+ fields (entities, metadata, embeddings, robotics fields, emotional context, source context, episode context, multimodal embeddings, decision fields, etc.). |

### Partially Verified

| Claim | Issue | Evidence |
|-------|-------|----------|
| p_codex | Not explicitly mentioned. MCP-compatible (works via stdio transport). | README says "available to Claude, Cursor, and other MCP clients" — Codex implied but not named. |
| p_opencode | Not explicitly mentioned. | Same as above — any MCP client works, but not listed. |
| p_gemini | Not explicitly mentioned. | Same — MCP-compatible, not explicitly listed. |
| p_copilot | Not explicitly mentioned. | Same — MCP-compatible, not explicitly listed. |
| p_windsurf | Not explicitly mentioned. | Same — MCP-compatible, not explicitly listed. |
| p_openclaw | Not explicitly mentioned. | Same — MCP-compatible, not explicitly listed. |
| p_hermes | Not explicitly mentioned. | Same — MCP-compatible, not explicitly listed. |
| p_pi | Not explicitly mentioned. | Same — MCP-compatible, not explicitly listed. |
| p_antigravity | Not explicitly mentioned. | Same — MCP-compatible, not explicitly listed. |

### Corrections — Claimed Absent, Actually Present

| Feature | User Claim | Reality |
|---------|-----------|---------|
| **multiAgent** | absent | **Present.** `remember_with_agent()` method with `agent_id` and `run_id` parameters. Memory struct has `agent_id`, `run_id`, `actor_id` fields. Multi-tenant enterprise support. |
| **entities** | absent | **Present.** Entity extraction (TinyBERT NER) on `remember()`. `Experience.entities: Vec<String>`, `Experience.ner_entities: Vec<NerEntityRecord>`. Performance table: "Entity lookup 763ns." Knowledge graph with entity nodes. |
| **context** | absent | **Present.** `Experience.context: Option<RichContext>` — massive multi-dimensional context with 9 sub-contexts: Conversation, User, Project, Temporal, Semantic, Code, Document, Environment, Emotional, Source, Episode. |
| **source** | absent | **Present.** `SourceContext` within `RichContext` — tracks `source_type` (User, System, ExternalApi, File, Web, AiGenerated, Inferred), `source_id`, `credibility`, `verified`, `source_chain`. |
| **emotional** | absent | **Present.** `EmotionalContext` within `RichContext` — `valence`, `arousal`, `dominant_emotion`, `content_sentiment`, `confidence`. |
| **layeredMemory** | absent | **Present.** Core architecture: "Working Memory (100 items) → Session Memory (100 MB) → Long-Term Memory (RocksDB)." Three-tier Cowan's model with tier promotion/demotion. |
| **dedup** | absent | **Present.** "Content-hash dedup (SHA-256) ensures identical memories are never stored twice." `get_by_content_hash()` O(1) RocksDB index lookup. `DeduplicationEngine` in segmentation module. |
| **factQuery** | absent | **Present.** `SemanticFactStore`, `FactQueryResponse`, `FactStats`. Semantic fact extraction from episodic memories with `fact_extraction_needed` flag. |
| **supersede** | absent | **Partial.** `external_id` enables upsert semantics (same external_id = update existing). `MemoryRevision` history with `update_content()`. Not a named "supersede" primitive though. |
| **contradiction** | absent | **Partial.** Interference detector (SHO-106) handles retroactive/proactive interference between contradictory memories. Not named "contradiction" but functionally present. |
| **trustModel** | absent | **Partial.** `SourceContext.credibility` (0.0-1.0). `SourceContext.verified` boolean. Not a full trust model but credibility-weighted source tracking exists. |
| **taskType** | absent | **Partial.** `ExperienceType::Task` exists as enum variant. No separate `task_type` metadata field, but experience_type covers this. |

### Actually Absent (confirmed not in codebase or README)

The following features are genuinely not mentioned anywhere in the README, openapi.yaml, or source code:

**actions, keywords** (tags serve this function but no dedicated keyword field), **anticipatedQueries, triggerRules, domainTag, originTrust** (separate from credibility), **conflict** (interference detection is related but different concept), **timeTravel, deep, codeGraph** (has knowledge graph NOT code graph), **docsSearch, timeline, quarantine, autoResolve, contentPreproc, qualityRefine, narrative, clustering, recurrence, persona.**

### Special: layeredMemory Correction

User flagged this as absent. This is a major correction — the three-tier memory architecture (Working → Session → Long-Term) is the **central architectural claim** of the README, derived from Cowan's working memory model and Wixted's memory decay research. It's the second thing described after the pitch paragraph.

## Feature Inventory (from README and source)

### MCP Tools (37)
**Memory:** `remember`, `recall`, `proactive_context`, `context_summary`, `list_memories`, `read_memory`, `forget`
**Todos (GTD):** `add_todo`, `list_todos`, `update_todo`, `complete_todo`, `delete_todo`, `reorder_todo`, `list_subtasks`, `add_todo_comment`, `list_todo_comments`, `update_todo_comment`, `delete_todo_comment`, `todo_stats`
**Projects:** `add_project`, `list_projects`, `archive_project`, `delete_project`
**Reminders:** `set_reminder`, `list_reminders`, `dismiss_reminder`
**System:** `memory_stats`, `verify_index`, `repair_index`, `token_status`, `reset_token_session`, `consolidation_report`, `backup_create`, `backup_list`, `backup_verify`, `backup_restore`, `backup_purge`

### REST API
160+ endpoints on `localhost:3030`. Auth via `X-API-Key` header.

### Retrieval Modes (3)
`semantic` (pure vector similarity), `associative` (graph traversal with Hebbian edges), `hybrid` (combined + RRF reranking)

### Cognitive Primitives
- Hebbian learning: co-activation strengthens connections
- Exponential activation decay: A(t) = A0 · e^(-λt)
- Spreading activation retrieval
- Long-term potentiation (permanent connections after threshold)
- Memory replay during maintenance
- Retroactive/proactive interference detection
- Pattern-triggered consolidation (not fixed-interval)

### Data Model (Experience struct — 45+ fields)
Core: `content`, `experience_type`, `context`, `entities`, `metadata`, `embeddings`, `tags`, `temporal_refs`
Multimodal: `image_embeddings`, `audio_embeddings`, `video_embeddings`, `media_refs`
Robotics: `robot_id`, `mission_id`, `geo_location`, `local_position`, `heading`, `action_type`, `reward`, `sensor_data`
Decision: `decision_context`, `action_params`, `outcome_type`, `confidence`, `alternatives_considered`
Environmental: `weather`, `terrain_type`, `lighting`, `nearby_agents`
Failure: `is_failure`, `is_anomaly`, `severity`, `recovery_action`, `root_cause`
Prediction: `pattern_id`, `predicted_outcome`, `prediction_accurate`
Relation: `related_memories`, `causal_chain`, `outcomes`, `cooccurrence_pairs`, `ner_entities`

### RichContext (12 sub-contexts)
Conversation, User, Project, Temporal, Semantic, Code, Document, Environment, Emotional, Source, Episode, parent

### Platform Support
Linux x86_64, Linux ARM64, macOS Apple Silicon, macOS Intel, Windows x86_64

### MCP Compatibility
Any MCP client (stdio transport). Explicitly documented: Claude Code, Cursor. Implicit: all MCP-compatible clients.

### Robotics / ROS2
Zenoh transport (pub/sub + request/reply). ROS2 Kilted via rmw_zenoh or zenoh-bridge-ros2dds. Spatial recall (haversine). 26 robotics-specific fields per Experience. Fleet discovery via Zenoh liveliness tokens.

## Architecture Notes

- ~17MB single binary (ONNX model ~37MB downloaded on first run)
- Embedding: MiniLM-L6-v2 (384-dim)
- Full-text: Tantivy BM25
- Vector search: Custom Vamana HNSW
- Storage: RocksDB with jemalloc
- Graph: petgraph for entity relationships / knowledge graph
- Reranker: Reciprocal Rank Fusion (RRF)
- Dedup: SHA-256 content hash with O(1) RocksDB index lookup
- MCP transport: rmcp 0.12 with stdio transport
- HTTP server: Axum + Tokio
- Optional: Zenoh transport (robotics), Python bindings (PyO3), telemetry, LLM-parser

## Notable Design Decisions

1. **No LLM in the loop.** All intelligence is algorithmic — local embeddings, mathematical decay, learned associations. This is the core differentiator from mem0/Cognee/Zep. Store latency: 55ms vs 20+ seconds.

2. **Neuroscience-grounded.** Hebbian learning, exponential decay, spreading activation, long-term potentiation — all modeled on cognitive science research with academic citations (Cowan 2010, Wixted 2004, Magee & Grienberger 2020).

3. **Robotics as first-class use case.** Zenoh transport, 26 robotics-specific fields, spatial recall, fleet discovery. Not just for chat agents.

4. **GTD task management bundled.** Todos, projects, reminders are part of the memory system, not separate tools. Causal lineage between decisions and outcomes.

5. **MCP-native, agent-neutral.** Default transport is stdio MCP. Any MCP client can use it.

6. **Apache 2.0 license.** Permissive, no copyleft constraints.

## Evidence

`evidence: "https://github.com/carsteneu/ai-memory-comparison/blob/main/evidence/shodh.md"`
