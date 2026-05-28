# ClawMem — Evidence

> Every ✅ claim backed by public README, CLAUDE.md, or source.
> Repo: [yoloshii/ClawMem](https://github.com/yoloshii/ClawMem) (177 stars, TypeScript on Bun, MIT)
> **URL correction:** User provided `AiderOnClaw/clawmem` which returns 404. Actual repo is `yoloshii/ClawMem`.

---

## Corrections to Claimed Data

### Repository URL — CORRECTION
- Claimed: `https://github.com/AiderOnClaw/clawmem`
- Actual: `https://github.com/yoloshii/ClawMem` (yoloshii/ClawMem, case-sensitive)

The org "AiderOnClaw" does not exist on GitHub. The project lives under `yoloshii/ClawMem`.

### singleBinary — CORRECTION: NOT PRESENT ✅→❌
- `package.json` — `"bin": { "clawmem": "./bin/clawmem" }` — the entry point is a bash wrapper script
- `package.json` — `"engines": { "bun": ">=1.0.0" }` — requires Bun runtime
- `package.json` — `"type": "module"` — TypeScript source, interpreted, not compiled to a standalone binary
- This is an npm package requiring a JavaScript runtime (Bun) — NOT a single compiled Go/Rust binary
- Install requires `npm install -g clawmem` or `bun add -g clawmem`, not a single binary download

### hybrid — CORRECTION: PRESENT ❌→✅
- README.md — "hybrid architecture combines QMD-derived multi-signal retrieval (BM25 + vector search + reciprocal rank fusion + query expansion + cross-encoder reranking)"
- CLAUDE.md — `query` pipeline: "Full hybrid: BM25 + vector + query expansion + deep reranking (4000 char)"
- CLAUDE.md — RRF fusion: "Original query lists get positional 2× weight in RRF; expanded get 1×"
- HTTP API: `/search` endpoint accepts `mode: hybrid`
- This is a full BM25+vector hybrid search with RRF fusion — definitively present

### conflict — CORRECTION: PRESENT ❌→✅
- README.md — "Detects contradictions between new and prior decisions, auto-decaying superseded ones (with an additional merge-time contradiction gate in the consolidation worker that blocks cross-observation contradictions before they land, v0.7.1)"
- CLAUDE.md — `CLAWMEM_CONTRADICTION_POLICY`: `link` (keeps both rows active + `contradicts` edge) or `supersede` (marks old row inactive)
- CLAUDE.md — `CLAWMEM_CONTRADICTION_MIN_CONFIDENCE`: minimum combined confidence before contradiction gate blocks a merge
- CLAUDE.md — Phase 3 deductive synthesis: "Contradictory dedupe matches are linked via `contradicts` edges"
- Contradiction detection operates at merge-time and during decision extraction — definitively present

### timeline — CORRECTION: PRESENT ❌→✅
- README.md — "Navigates temporal neighborhoods around any document via the `timeline` tool — progressive disclosure from search to chronological context to full content"
- CLAUDE.md — MCP tool: `timeline(docid, before=5, after=5, same_collection=false)` — "Shows what was created/modified before and after a document"
- HTTP API: `GET /timeline/:docid` — "Temporal neighborhood (before/after)"
- CLAUDE.md — Temporal extraction from queries: "regex date range from query: 'last week', 'March 2026' → WHERE modified_at BETWEEN filters"
- Meets CRITERIA.md definition: "Historical state querying with since/before parameters"

### dedup — CORRECTION: PRESENT ❌→✅
- README.md — "Deduplicates hook-generated observations within a 30-minute window using normalized content hashing, preventing memory bloat from repeated hook output"
- CLAUDE.md — A-MEM link generation includes deduplication; conversation synthesis uses dedup-aware `saveMemory`
- README.md — "Cleans stale embeddings automatically before embed runs, removing orphans from deleted/changed documents"
- Dedup is present at the hook-output level (30-min window) and during fact extraction

### searchModes — CORRECTION: UNDERCOUNT (claimed 3, actual 5+)
- Claimed: 3 search modes
- Actual modes documented in README/CLAUDE.md:
  1. BM25 keyword (`search`) — FTS5 full-text
  2. Vector semantic (`vsearch`) — embedding-based
  3. Hybrid (`query`) — BM25 + vector + RRF + rerank
  4. Intent-aware (`intent_search`) — intent classification + graph traversal
  5. Query plan decomposition (`query_plan`) — multi-clause parallel
  6. Auto-routing (`memory_retrieve`) — classifies and dispatches
- Plus `timeline` (temporal), `find_similar` (k-NN), `find_causal_links` (causal graph), `session_log` (session history)
- Minimum verifiable count: **5** distinct retrieval modes, vs claimed 3

### dataSources — CORRECTION: UNDERCOUNT (claimed 2, actual 3+)
- Claimed: 2 data sources
- Actual sources:
  1. Markdown documents (indexed from collections)
  2. Session transcripts (observer model auto-captures decisions/preferences/milestones/problems)
  3. Conversation exports (mine: Claude Code, ChatGPT, Claude.ai, Slack, plain text)
  4. Beads issue tracker sync (bd CLI → SPO triples)
  5. Diary entries (diary_write in non-hooked environments)
- Minimum verifiable count: **3** distinct data sources, likely 4-5

### schemaFields — CORRECTION: UNDERCOUNT (claimed 8, actual 12+)
- Claimed: 8 schema fields
- Document fields from README/CLAUDE.md evidence:
  1. `id` / `docid` (6-char hash prefix identifier)
  2. `path` (file path within collection)
  3. `title` (document title)
  4. `content` / `body` (full text)
  5. `collection` (collection name)
  6. `content_type` (decision/preference/milestone/problem/deductive/handoff/conversation/note/research/project/antipattern/hub)
  7. `confidence` (0.0–1.0, used in composite scoring)
  8. `quality_score` (0.0–1.0, structure/keywords/metadata richness)
  9. `keywords` (A-MEM enriched)
  10. `tags` (A-MEM enriched)
  11. `status` (active/inactive/invalidated)
  12. `created_at` / `modified_at` (temporal metadata)
  13. `last_recalled_at` / `last_accessed_at` (for lifecycle)
  14. `revisions` (revision count for durability signal)
  15. `pinned` (boolean, +0.3 composite boost)
  16. `snoozed_until` (date for temporary suppression)
  17. `invalidated_at` / `superseded_by` (soft deletion chain)
  18. `source_doc_ids` (provenance for deductive observations)
- Minimum verifiable count: **12+** distinct semantic fields (excluding auto-generated timestamps)

---

## Verified Present Features

### Data Model

#### entities ✅
- README.md — "Injects knowledge-graph facts as structured triples" via SPO (subject-predicate-object) graph
- CLAUDE.md — `entity_mentions` + `entity_cooccurrences` tables: "LLM entity extraction → quality filters → type-agnostic canonical resolution within compatibility buckets (person, org, location, tech=project/service/tool/concept)"
- CLAUDE.md — `kg_query` tool: "query the SPO knowledge graph for an entity's relationships. Returns temporal triples with validity windows"
- CLAUDE.md — "Guards against cross-entity merges during consolidation — name-aware dual-threshold merge safety compares entity anchors"
- Entity resolution includes canonical IDs in `vault:type:slug` form

#### actions ✅
- README.md — "Captures decisions, preferences, milestones, and problems from session transcripts using a local GGUF observer model"
- CLAUDE.md — Eligible observation types: decision, preference, milestone, problem, discovery, feature
- CLAUDE.md — Tight predicate vocabulary for SPO triples: adopted, migrated_to, deployed_to, runs_on, replaced, depends_on, integrates_with, uses, prefers, avoids, caused_by, resolved_by, owned_by
- These content types and predicates represent structured actions/operations — actions are captured as typed observations with rich metadata

#### keywords ✅
- README.md — "A-MEM self-evolving memory notes that enrich documents with keywords, tags, and causal links between entries"
- CLAUDE.md — Keywords field in document metadata, enriched during A-MEM indexing
- CLAUDE.md — Quality scoring uses "keywords signal" as one component

#### taskType ✅
- CLAUDE.md — `content_type` field with explicit type taxonomy: decision, preference, milestone, problem, deductive, handoff, conversation, note, research, project, antipattern, hub
- CLAUDE.md — Decision-extractor assigns content_type during observation capture
- This maps to task/idea/blocked classification, though ClawMem uses a content-first taxonomy rather than task-status taxonomy

#### context ✅
- README.md — "Surfaces relevant context on every prompt (context-surfacing hook)"
- CLAUDE.md — Context-surfacing injects `<vault-context>` with `<instruction>` + `<facts>` + `<relationships>` + `<vault-facts>` blocks
- CLAUDE.md — Multi-turn query construction: "current prompt + up to 2 recent same-session priors"
- Context (the "why" and surrounding relationships) is explicitly captured and surfaced

#### source ✅
- CLAUDE.md — Source attribution through `source_doc_ids` on deductive observations
- README.md — Multiple ingestion paths with provenance: observer model (session transcripts), mine (Claude Code/ChatGPT/Claude.ai/Slack/text), beads (issue tracker)
- CLAUDE.md — Conversation synthesis saves extracted facts with `sourceDocId` provenance
- While not a formal 5-tier trust hierarchy like YesMem, source attribution is present and trackable

### Search & Retrieval

#### fulltext ✅
- README.md — "BM25 keyword search" via `search` tool
- CLAUDE.md — "BM25 only, 0 GPU" — "BM25 AND's all terms as prefix matches"
- README.md — SQLite with FTS5 as prerequisite
- CLAUDE.md — "BM25 Probe → Strong Signal Check (skip expansion if top hit ≥ 0.85 with gap ≥ 0.15)"

#### semantic ✅
- README.md — "Vector semantic search" via `vsearch` tool
- README.md — Embedding models: zembed-1 (2560d) or EmbeddingGemma-300M (768d) via llama.cpp
- CLAUDE.md — "Vector only, 1 GPU call. Conceptual/fuzzy, don't know vocabulary"
- HTTP API: `POST /search` with `mode: semantic`

#### timeTravel ✅
- README.md — "Navigates temporal neighborhoods around any document via the `timeline` tool"
- CLAUDE.md — `timeline(docid, before=5, after=5, same_collection=false)` — "Shows what was created/modified before and after a document"
- CLAUDE.md — Temporal extraction from queries parses "last week", "March 2026" into date-range filters
- HTTP API: `GET /timeline/:docid` with before/after parameters
- While not git-like version control, this qualifies as time-travel per CRITERIA.md (temporal neighborhood navigation)

### Knowledge Lifecycle

#### decay ✅
- README.md — "SAME-inspired composite scoring (recency decay, confidence, content-type half-lives, co-activation reinforcement)"
- CLAUDE.md — Content-type half-life table: handoff (30 days), conversation/progress (45 days), problem/milestone/note (60 days), research (90 days), project (120 days), decision/deductive/preference/hub/antipattern (∞)
- CLAUDE.md — "Attention decay: non-durable types lose 5% confidence per week without access"
- CLAUDE.md — Access reinforcement extends half-lives up to 3×
- Recency-weighted composite scoring: `0.25 × recencyScore` (normal), `0.70 × recencyScore` (recency intent)

#### supersede ✅
- README.md — "Detects contradictions between new and prior decisions, auto-decaying superseded ones"
- CLAUDE.md — `CLAWMEM_CONTRADICTION_POLICY=supersede` marks old row `status='inactive'`, new row replaces
- CLAUDE.md — `superseded_by` and `invalidated_at` columns for soft invalidation chains
- CLAUDE.md — Observation invalidation: "Documents with `invalidated_at` set are excluded from search results"

#### explicitForget ✅
- README.md — MCP tool `memory_forget`: "Search → deactivate closest match (with audit trail)"
- README.md — HTTP API: `POST /documents/:docid/forget` — "Deactivate"
- CLAUDE.md — "Forget is for genuinely wrong or permanently obsolete memories"

### Extraction Pipeline

#### autoExtract ✅
- README.md — "Captures decisions, preferences, milestones, and problems from session transcripts using a local GGUF observer model"
- CLAUDE.md — `decision-extractor` hook: "LLM extracts observations → `_clawmem/agent/observations/`, infers causal links, detects contradictions, persists observer-emitted SPO triples"
- CLAUDE.md — `handoff-generator` hook: "LLM summarizes session → `_clawmem/agent/handoffs/`"
- CLAUDE.md — Consolidation worker: "Background worker backfills unenriched docs and runs Phase 2/3 consolidation + deductive synthesis"
- Multiple automated extraction paths, not a single-pass pipeline

### Platform Support

#### p_claude ✅
- README.md — "Claude Code integration via hooks (settings.json) and an MCP stdio server"
- README.md — `clawmem setup hooks` installs lifecycle hooks (SessionStart, UserPromptSubmit, Stop, PreCompact)
- README.md — `clawmem setup mcp` registers 31 MCP tools in `~/.claude.json`
- README.md — Hooks handle 90% of retrieval automatically (context-surfacing, postcompact-inject, decision-extractor, handoff-generator, feedback-loop)

#### privacy ✅
- README.md — "On-device memory... No API keys, no cloud dependencies"
- README.md — "Runs fully local with no API keys and no cloud services"
- README.md — "All paths write to the same local SQLite vault"
- Cloud embedding is optional, not required — local mode is the default and fully functional

#### offline ✅
- README.md — "Runs fully local with no API keys and no cloud services"
- README.md — GPU services can run locally via llama.cpp; in-process fallback via node-llama-cpp
- CLAUDE.md — "ClawMem always works either way" (with or without GPU servers)
- Cloud embedding is optional — default is local models

#### export ✅
- README.md — HTTP API: `GET /export` — "Full vault export as JSON"
- All data stored in local SQLite, directly accessible

---

## Absent Features (Verified)

The following features from the "verify absent" list are confirmed as genuinely absent:

| Feature | Evidence of Absence |
|---|---|
| webUi | No web dashboard, TUI, or GUI mentioned. REST API exists but no browser-based management interface. |
| multiAgent | Multi-framework operation (shared SQLite vault across Claude Code/OpenClaw/Hermes) but no inter-agent communication, orchestration, or swarm coordination. No spawn/relay/messaging primitives. |
| anticipatedQueries | Query expansion generates search variants dynamically but no "anticipated queries" stored as document metadata for proactive surfacing. |
| triggerRules | No condition-based activation rules for automatic memory surfacing based on context triggers (beyond the standard context-surfacing hook which is query-driven, not rule-driven). |
| domainTag | No domain category tag (code/marketing/legal/finance/general). Content types classify by format (decision, handoff, etc.) not by domain. |
| originTrust | Has source provenance (observer, mine, beads, diary) but no trust weight hierarchy based on capture method. Confidence scoring exists but is not origin-weighted. |
| emotional | No sentiment or emotional intensity tracking. |
| layeredMemory | No L0→L1→L2 semantic layering. A-MEM enrichment adds metadata to documents but does not create tiered summaries (raw → summary → persona). Content-type half-lives are decay management, not layered memory architecture. |
| deep | No search of model thinking/reasoning traces. Observer model captures session transcripts but not the internal reasoning chains. |
| codeGraph | No Tree-sitter/AST-based code indexing. A-MEM links are LLM-generated, not structural code analysis. |
| docsSearch | No dedicated documentation search index separate from the vault. The vault indexes markdown docs but has no separate docs search with section/heading awareness. |
| factQuery | `kg_query` exists for SPO entity graph but is entity-centric (single entity lookup), not a general fact metadata query tool (no query by entity+action+keyword across all learnings). |
| quarantine | No session quarantine/exclusion from search. No mechanism to mark an entire session as untrusted and exclude its learnings. |
| autoResolve | Contradictions auto-decayed via confidence lowering but no general auto-resolution with configurable TTL for stale tasks/ideas. Consolidation worker handles dedup, not task lifecycle. |
| trustModel | Has confidence scoring (0.0–1.0) on observations but no multi-tier trust hierarchy with origin-based multipliers. |
| contentPreproc | No explicit content-aware preprocessing pipeline. Documents are indexed as-is; validation exists (max size, format checks) but no structured reduction/transformation before storage. |
| qualityRefine | No explicit second-pass quality refinement with LLM re-evaluation. LLM extraction is single-pass. Confidence scoring is compositional (keywords + structure + metadata) but not a separate refinement stage. |
| narrative | Handoffs are single-session summaries, not cross-session narrative generation or project profiles. No narrative pipeline that synthesizes multi-session arcs. |
| clustering | No embedding-based clustering of related memories. k-NN similarity exists (`find_similar`) but not cluster formation. Consolidation merges observations by semantic similarity but does not form persistent clusters. |
| recurrence | No recurrence/pattern detection across sessions. Deductive synthesis combines related recent observations but does not detect cyclical patterns. |
| persona | Static + dynamic user profile exists (`profile` command, session bootstrap) but this is user-defined configuration, not automatic persona trait extraction from conversations. No detected trait persistence. |

---

## Borderline / Judgement Call

### kg_query as factQuery — BORDERLINE ⚠️
- CLAUDE.md documents `kg_query(entity, as_of?, direction?)` — "query the SPO knowledge graph for an entity's relationships"
- Returns structured (subject, predicate, object) triples with temporal validity windows
- However, this is entity-centric (query one entity's facts), not a general metadata search across all learnings by entity/action/keyword
- Criteria for factQuery is: "Structured metadata query tool" — kg_query qualifies in the narrow sense but lacks the breadth of YesMem's query_facts (search by entity/action/keyword/category/domain)
- Judgement: technically present as a structured fact query mechanism, but narrower in scope than the criterion implies

---

## Architecture

### Language: TypeScript ✅ (not in claims but verified)
- `package.json` — `"type": "module"`, TypeScript on Bun
- README.md — "TypeScript on Bun. MIT License."

### License: MIT ✅ (not in claims but verified)
- `package.json` — `"license": "MIT"`
- README.md — "TypeScript on Bun. MIT License."

### Stars: ~177 (verified)
- GitHub repo page shows 177 stars as of audit date

### Storage: SQLite + sqlite-vec ✅
- `package.json` — dependencies include `sqlite-vec`
- README.md — "SQLite with FTS5"
- CLAUDE.md — vault at `~/.cache/clawmem/index.sqlite`

### Integration: Hooks + MCP + Native Plugins ✅
- README.md — Claude Code hooks (SessionStart, UserPromptSubmit, Stop, PreCompact)
- README.md — MCP server (31 tools, stdio transport)
- README.md — Native OpenClaw plugin (kind: memory)
- README.md — Hermes Agent MemoryProvider plugin

### Deployment: Local binary/package ✅
- `package.json` — npm global install (`bin/clawmem`), also works with bun
- README.md — "Runs fully local"

---

## Score Correction Summary

| Feature | Claimed | Actual | Evidence |
|---|---|---|---|
| singleBinary | ✅ | ❌ | Requires Bun runtime, bash wrapper, not compiled |
| hybrid | ❌ | ✅ | BM25 + vector + RRF + rerank pipeline |
| conflict | ❌ | ✅ | Contradiction detection + merge-time gate |
| timeline | ❌ | ✅ | Timeline tool + temporal query extraction |
| dedup | ❌ | ✅ | 30-min hook dedup + fact extraction dedup |
| searchModes | 3 | 5+ | search, vsearch, query, intent_search, query_plan, memory_retrieve |
| dataSources | 2 | 3+ | Markdown, transcripts, conversation exports, beads, diary |
| schemaFields | 8 | 12+ | Content type, confidence, quality, keywords, tags, status, half-life, revisions, pin/snooze, invalidation chain |
