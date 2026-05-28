# OpenMemory — Evidence

> Every ✅ claim backed by public source code or documentation.
> Audit date: 2026-05-28. Source: GitHub `CaviraOSS/OpenMemory` main branch, `openmemory.cavira.app`, ARCHITECTURE.md, Why.md.

## Metadata

- **Stars**: 4,164 (API), 4.2k (GitHub page)
- **Created**: 2025-10-19
- **License**: Apache 2.0
- **Docs**: https://openmemory.cavira.app/docs
- **Homepage**: https://openmemory.cavira.app
- **Status**: Currently being rewritten (notice on README; rewrite branch active)
- **Language**: TypeScript 72.5%, Python 24.5%
- **Description**: "Local persistent memory store for LLM applications including claude desktop, github copilot, codex, antigravity, etc."

---

## Architecture

### Web/TUI (webUi) ✅
- `README.md` — Docker compose supports dashboard: `docker compose --profile ui up --build -d`. Backend exposes "dashboard UI (when `ui` profile is enabled)".
- `openmemory.cavira.app` — Landing page shows Pulse/Retention dashboard with live stats (94.7% retention, 97% memory health, 23k factual, 18k emotional, 36ms latency). Browser-based UI with "Deploy in minutes" CTA.

### Offline ✅
- `README.md` — "Offline‑friendly", "Zero cloud config", "100% local storage". Local SQLite default, no cloud dependency.
- `Why.md` — "Runs fine on a $5/month VPS", "100% local and auditable".

### Privacy ✅
- `README.md` — "Self‑hosted, local‑first, you own the DB", "Your DB, your schema".
- `Why.md` — "100% local and auditable", "Zero vendor lock‑in; full data control", "Data ownership: 100% Yours".
- `ARCHITECTURE.md` — "100% local storage (no vendor lock-in)", "Optional content encryption at rest", "PII scrubbing hooks available", "Tenant isolation support".

### Export ❌
- No export feature mentioned in README, API docs, ARCHITECTURE.md, or Why.md. Migration tool imports FROM other systems, not export of OpenMemory data.

### Multi-Agent (multiAgent) ✅
- `README.md` — Integration with CrewAI and AutoGen: "Crew-style agents: use Memory as a shared long-term store", "AutoGen-style orchestrations: store dialog + tool calls as episodic memory".
- `ARCHITECTURE.md` — Server supports multi-user with `user_id` scoping, LangGraph mode with multi-agent context assembly.

### LLM Flexibility (llmFlex) ✅
- `ARCHITECTURE.md` — Embedding providers: OpenAI (`text-embedding-3-small`, `text-embedding-3-large`), Gemini (`embedding-001`), AWS (`amazon.titan-embed-text-v2:0`), Ollama (`nomic-embed-text`, `bge-small`, `bge-large`), local custom models, synthetic hash-based fallback. 6 providers confirmed.
- `Why.md` — "Works with any LLM (OpenAI, Gemini, AWS, Ollama, Claude)".

---

## Data Model

### Entities ❌
- No entity extraction or entity linking mentioned in README, ARCHITECTURE.md, or API docs. The data model has `user_id` scoping and `tags`, but no extracted named entities.

### Actions ❌
- No action/operation metadata in schema. The `memories` table has: id, content, primary_sector, tags, meta, created_at, updated_at, last_seen_at, salience, decay_lambda, version, mean_dim, mean_vec. No action field.

### Keywords ❌
- CLI supports `--tags` on `opm add`, but these are user-supplied tags, not extracted keywords. No automatic keyword extraction pipeline.

### Context ❌
- Not a structured schema field. The API accepts `metadata` (JSON) which could carry context, but there is no dedicated `context` field.

### Source ❌
- Not a dedicated schema field. `meta` (JSON metadata) can carry source information, but no `source` column exists in the memories table.

### Emotional (emotional) ✅
- `ARCHITECTURE.md` — Five memory sectors include "emotional": "Feelings and sentiments" with decay_lambda=0.020, weight=1.3, patterns=[/feel|happy|sad|angry/i,...].
- `README.md` — "Multi-sector memory: Episodic (events), semantic (facts), procedural (skills), emotional (feelings), reflective (insights)."
- `Why.md` — "Emotional: Feelings and tone". Example: "'feel productive' → stored across emotional sector".

### Conflict ❌
- No conflict detection or resolution mentioned anywhere. No contradiction handling in temporal KG (auto-evolution closes old facts but doesn't flag contradictions).

### Layered Memory (layeredMemory) ✅
- `ARCHITECTURE.md` — Five cognitive sectors as memory layers: episodic (events), semantic (facts), procedural (skills), emotional (feelings), reflective (insights). Each with independent decay rates and weights. Memories are classified into sectors on ingestion.
- `README.md` — "Multi‑sector memory (episodic, semantic, procedural, emotional, reflective)".

### Time Travel (timeTravel) ✅
- `README.md` — "Temporal knowledge graph: `valid_from` / `valid_to`, point‑in‑time truth, evolution over time."
- `README.md` — Concepts: "auto‑evolution – new facts close previous ones", "confidence decay – old facts fade gracefully", "point‑in‑time queries – 'what was true on X?'", "timelines – reconstruct an entity's history", "change detection – see when something flipped".
- `ARCHITECTURE.md` — Backend exposes `/api/temporal/*` endpoints for temporal knowledge graph operations.

### Schema Fields (schemaFields) — 13
- `ARCHITECTURE.md` — `memories` table: `id`, `content`, `primary_sector`, `tags`, `meta`, `created_at`, `updated_at`, `last_seen_at`, `salience`, `decay_lambda`, `version`, `mean_dim`, `mean_vec` = **13 fields**.
- Additional fields in `vectors` table (id, sector, v, dim) and `waypoints` table (src_id, dst_id, weight, created_at, updated_at) are separate tables, not core memory schema.

---

## Search & Retrieval

### Full-text (fulltext) ❌
- No BM25 or full-text search mentioned. All search is vector cosine similarity based. The composite scoring formula (0.6×similarity + 0.2×salience + 0.1×recency + 0.1×waypoint) has no keyword/BM25 component.

### Semantic/Vector (semantic) ✅
- `ARCHITECTURE.md` — Query flow: "embedForSector() → query vector → cosine similarity → top-K per sector → merge results". Uses 768-dim vectors stored as Float32 BLOBs in SQLite.
- `README.md` — Embeddings supported: OpenAI, Gemini, Ollama, AWS, synthetic fallback.

### Hybrid (hybrid) ✅
- `ARCHITECTURE.md` — Composite scoring fuses multiple signals: `score = 0.6×similarity + 0.2×salience + 0.1×recency + 0.1×waypoint`. Also: "expandViaWaypoints() → 1-hop graph traversal" for graph-enhanced retrieval.
- Note: Hybrid here means multi-signal fusion (semantic + salience + recency + graph), not BM25+vector. The fusion of 4 distinct signal types qualifies as hybrid retrieval.

### Deep Search (deep) ❌
- No deep search with expanded context or cross-session conversation history retrieval mentioned.

### Code Graph (codeGraph) ❌
- Not a code-aware tool. OpenMemory is for general memory, not code graph indexing.

### Documentation Search (docsSearch) ❌
- No documentation indexing or search feature.

### Fact Query (factQuery) ✅
- `README.md` — Temporal knowledge graph with subject-predicate-object fact model: `POST /api/temporal/fact {subject, predicate, object, valid_from}`. Queries like "what was true on X?" supported.
- `Why.md` — Ingestion table shows "✓Multi-format" for OpenMemory vs ✗ for others.

### Timeline (timeline) ✅
- `README.md` — Temporal KG: "timelines – reconstruct an entity's history", "change detection – see when something flipped".
- `ARCHITECTURE.md` — "Temporal KG" subgraph in architecture diagram includes "Facts → Timeline".

### Search Modes (searchModes) — 2
- Vector semantic search via `/memory/query` (primary mode)
- Temporal/fact queries via `/api/temporal/*` endpoints (secondary mode)
- Both are distinct retrieval interfaces with different query semantics.

---

## Knowledge Lifecycle

### Decay (decay) ✅
- `ARCHITECTURE.md` — "Decay System: Simulate memory fading over time". Formula: `salience × e^(-decay_lambda × days)`. Sector-specific decay rates: episodic (0.015), semantic (0.005), procedural (0.008), emotional (0.020), reflective (0.001).
- `README.md` — "Decay engine: Adaptive forgetting per sector instead of hard TTLs."
- `ARCHITECTURE.md` — Runs every 24 hours (previously "every 12h" on landing page). Configurable via `OM_DECAY_LAMBDA`.

### Supersede/Replace (supersede) ✅
- `README.md` — Temporal KG: "auto‑evolution – new facts close previous ones". When a new fact with same subject+predicate is added, the old one's `valid_to` is automatically set.
- Example in README: Adding "Bob has_CEO from 2024-04-10" auto-closes "Alice has_CEO from 2021-01-01".

### Contradiction ❌
- No contradiction detection mentioned. Temporal KG handles evolution (old facts auto-close) but doesn't detect or flag conflicting facts.

### Quarantine ❌
- No quarantine mechanism mentioned for low-quality or suspect memories.

### Auto-Resolve (autoResolve) ❌
- No automatic task/issue resolution mentioned. Unfinished tasks not part of the data model.

### Trust Model (trustModel) ❌
- No trust scoring or provenance-based trust model. The `meta` JSON field could store source info but there's no automated trust assessment.

### Explicit Forget (explicitForget) ✅
- `ARCHITECTURE.md` — REST API: `DELETE /memory/:id` endpoint for deleting specific memories.
- `README.md` — CLI: `opm delete <id>` command.
- `api-server.md` — Delete endpoint confirmed in API docs.
- Note: MCP tools listed (openmemory_query, openmemory_store, openmemory_list, openmemory_get, openmemory_reinforce) do NOT include a delete tool. But REST API and CLI both support explicit deletion.

---

## Extraction Pipeline

### Auto-Extraction (autoExtract) ✅
- `ARCHITECTURE.md` — Sector classification pipeline: `classifyContent()` automatically routes content to 1-3 sectors using regex pattern matching (e.g., `/today|yesterday|remember when/i` → episodic, `/feel|happy|sad|angry/i` → emotional).
- `README.md` — "Multi-sector memory" with automatic classification into 5 cognitive types.
- Roadmap item: "Learned sector classifier (trainable on your data)" — current is regex-based, future will use ML.

### Content Preprocessing (contentPreproc) ✅
- `ARCHITECTURE.md` — Ingestion Pipeline supports 8 formats: PDF (`pdf-parse`), DOCX (`mammoth` → markdown), TXT (native), MD (native), HTML (`turndown`), URL (`fetch` + `turndown`), Audio (OpenAI Whisper), Video (`fluent-ffmpeg` + Whisper).
- `ARCHITECTURE.md` — Chunking strategy: "For texts > 512 tokens: split into overlapping chunks (512 tokens, 50 overlap), embed each, aggregate via mean pooling".

### Deduplication (dedup) ❌
- No deduplication mentioned. Ingest flow document → chunk → store as separate memories with no dedup check.

### Quality Refinement (qualityRefine) ❌
- No quality scoring or refinement of extracted memories. Raw content is classified and embedded as-is.

### Narrative (narrative) ❌
- The "reflective" sector is for "meta-cognition and insights" but there is no narrative generation (summarization, storytelling) mentioned.

### Clustering ❌
- No clustering of related memories mentioned. The waypoint graph creates single-best-match links but does not cluster.

### Recurrence ❌
- The "reinforcement" system boosts salience on recall (+0.1 per access) and strengthens waypoints (+0.05 per traversal), which resembles recurrence-based importance tracking. However, this is simple access-count boosting, not explicit recurrence pattern detection. Marking as absent.

### Persona ❌
- No persona extraction or user profile building mentioned. User scoping is via `user_id` only, no automatic trait extraction.

---

## Platform Support

### Claude/Claude Code (p_claude) ✅
- `README.md` — "Claude / Claude Code" section with MCP setup: `claude mcp add --transport http openmemory http://localhost:8080/mcp`.
- `README.md` — MCP tools: `openmemory_query`, `openmemory_store`, `openmemory_list`, `openmemory_get`, `openmemory_reinforce`.
- Repo description: "including claude desktop".

### Codex (p_codex) ✅
- Repo description: "including ... codex".
- `README.md` — "Integrations: ... MCP, VS Code, IDEs". MCP server works with any MCP client.

### OpenCode (p_opencode) ❌
- Not mentioned in README, platform list, or documentation. The repo description lists "claude desktop, github copilot, codex, antigravity" — no OpenCode.

### Gemini (p_gemini) ❌
- Embeddings support Gemini models, but no Gemini IDE/CLI integration documented. Not listed as a platform target.

### GitHub Copilot (p_copilot) ✅
- Repo description: "including ... github copilot".
- `README.md` — MCP server works with any MCP-aware IDE. VS Code extension available on marketplace.

### Cursor (p_cursor) ✅
- `README.md` — "Cursor / Windsurf" section with `.mcp.json` configuration example. Explicitly documented.

### Windsurf (p_windsurf) ✅
- `README.md` — "Cursor / Windsurf" section with `.mcp.json` configuration. Explicitly documented.

### OpenClaw (p_openclaw) ❌
- Not mentioned in README, platform list, or documentation.

### Hermes (p_hermes) ❌
- Not mentioned in README, platform list, or documentation.

### Pi (p_pi) ❌
- Not mentioned in README, platform list, or documentation.

### Antigravity (p_antigravity) ✅
- Repo description: "including ... antigravity". Listed as a supported IDE/platform in the repo's own description.

---

## Benchmarks

### LoCoMo (b_locomo) ❌
- No LoCoMo benchmark scores published. Not mentioned in README, docs site, or repository.

### LongMemEval (b_longmemeval) ❌
- No LongMemEval benchmark scores published. Not mentioned in README, docs site, or repository.

### PersonaMem (b_personamem) ❌
- No PersonaMem benchmark scores published.

### Token Efficiency (b_token) ❌
- No token efficiency benchmark published.

### Open Methodology (b_methodology) ❌
- No open benchmark methodology or evaluation framework published. No benchmark repository or paper cited.

---

## Claims NOT present (marked ❌ above) — verification summary

The following features have no public evidence:

**Data Model:** entities, actions, keywords, context, source (as dedicated field), conflict — all ❌

**Search:** fulltext (BM25), deep, codeGraph, docsSearch — all ❌

**Lifecycle:** contradiction, quarantine, autoResolve, trustModel — all ❌

**Extraction:** dedup, qualityRefine, narrative, clustering, recurrence, persona — all ❌

**Architecture:** export — ❌

**Platform:** p_opencode, p_gemini, p_openclaw, p_hermes, p_pi — all ❌

**Benchmarks:** b_locomo, b_longmemeval, b_personamem, b_token, b_methodology — all ❌

---

## Audit Notes

1. **Active rewrite**: The README banner says "This project is currently being rewritten. Expect breaking changes and potential bugs." The `rewrite` branch describes a JS/Node-first cleanup focusing on "durable records with provenance, temporal correctness, explainable recall." The current `main` branch reflects the pre-rewrite state. Features may change significantly during the rewrite.

2. **Hybrid search nuance**: OpenMemory's "composite scoring" fuses semantic (vector), salience, recency, and waypoint graph signals — a genuine multi-signal hybrid. However, it lacks BM25/full-text, which many other systems include in their hybrid search. Marked as ✅ but with the caveat that it's graph+salience hybrid, not BM25+vector hybrid.

3. **MCP tools are limited**: Only 5 MCP tools documented (query, store, list, get, reinforce). Notably missing: delete, temporal queries, stats. The REST API and CLI have broader functionality (delete, temporal endpoints, stats, document ingestion) not exposed via MCP.

4. **LLM flexibility is embedding-only**: The 6 providers are embedding models, not chat/LLM providers for extraction. The sector classifier uses regex patterns, not LLM calls. There's no LLM-based memory extraction pipeline — classification is rule-based.

5. **Schema fields count (13)**: Derived from the `memories` table in ARCHITECTURE.md. This excludes the `vectors` table (3 fields) and `waypoints` table (5 fields), which are separate normalized tables, not core memory schema fields.

6. **Stars variance**: GitHub API returns 4,164; GitHub page shows 4.2k. Both are within typical rounding range.
