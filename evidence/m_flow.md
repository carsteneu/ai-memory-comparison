# M-flow — Evidence

> Every ✅ claim backed by public source code or documentation.
> Audit date: 2026-05-28. Source: GitHub `FlowElement-ai/m_flow` main branch, `docs.m-flow.ai`, `mflow-benchmarks` repo.

## Metadata

- **Description**: Bio-inspired cognitive memory engine — a new paradigm for Graph RAG. Graph-routed bundle search with path-cost propagation through a four-layer inverted cone knowledge graph (Episode → Facet → FacetPoint → Entity).
- **Deployment**: Docker Compose (with profiles for neo4j, postgres, ui, playground, mcp), pip install (`mflow-ai`), source install (`pip install -e .`), Helm charts (`deployment/helm/`).
- **Storage**: SQLite/PostgreSQL (relational), LanceDB/ChromaDB/PGVector/Qdrant/Weaviate/Milvus/Pinecone (vector), KuzuDB/KuzuDB-remote/Neo4j (graph). Defaults to all-local (SQLite + LanceDB + KuzuDB).
- **Integration**: MCP server (stdio/sse/http), Python library (`import m_flow`), REST API (FastAPI), CLI (`mflow`), OpenClaw skill.
- **Setup**: `./quickstart.sh` (Docker), `pip install mflow-ai`, or source clone.
- **License**: Apache 2.0
- **Created**: ~Feb 2026 (v0.3.0 first documented release, 204 commits on main)
- **Docs URL**: https://docs.m-flow.ai

---

## Architecture

### webUi ✅
- `README.md` — "CLI & Web UI: Interactive console, knowledge graph visualization, config wizard". `mflow -ui` launches backend + frontend + MCP at `http://localhost:3000`.
- `m_flow-frontend/` — Next.js web console (pnpm).
- `AGENTS.md` — Frontend console (Next.js / pnpm), `pnpm dev` at `http://localhost:3000`.

### offline ✅
- `README.md` — "LLM-agnostic: OpenAI, Anthropic, Mistral, Groq, Ollama, LLaMA-Index, LangChain". Ollama enables local inference.
- `.env.template` — "All defaults are file-based; no external services required for local dev." SQLite (relational), LanceDB (vector), Kuzu (graph) all local.
- `.env.template` — `TELEMETRY_DISABLED=1` opt-out for anonymous telemetry.
- `AGENTS.md` — Docker Compose runs everything locally.

### privacy ✅
- `.env.template` — `TELEMETRY_DISABLED=1` to opt out of anonymous telemetry.
- `.env.template` — All storage local by default (SQLite/LanceDB/Kuzu), no data leaves machine unless S3 configured.
- `.env.template` — `ALLOW_HTTP_REQUESTS=True` can be set False to block outbound HTTP (SSRF protection).

### export ❌
- No evidence of data export functionality found.

### multiAgent ✅
- `.env.template` — Multi-user access control: `REQUIRE_AUTHENTICATION`, `ENABLE_BACKEND_ACCESS_CONTROL=True`, per-user+dataset DB isolation (SQLite, Postgres, LanceDB, KuzuDB).
- `AGENTS.md` — `auth/` module: "Authentication & multi-tenancy".
- `.env.template` — JWT secrets, user management via FastAPI Users.
- Face-aware memory partitioning: each recognized person gets their own dataset partition.

### llmFlex ✅
- `README.md` — "LLM-agnostic: OpenAI, Anthropic, Mistral, Groq, Ollama, LLaMA-Index, LangChain".
- `.env.template` — Explicit provider configs for: OpenAI, Ollama, DeepSeek, Qwen, Doubao, Cohere, MiniMax, plus generic "custom" OpenAI-compatible provider. At least 9+ distinct providers.
- `AGENTS.md` — Extension point: "New LLM provider → extend `llm/LLMGateway.py`".

---

## Data Model

### entities ✅
- `README.md` — "Entity: A named thing — person, tool, metric — linked across all Episodes". Entities bridge multiple Episodes through the same Entity node.
- `AGENTS.md` — `core/` contains domain models including Entity.
- `docs/RETRIEVAL_ARCHITECTURE.md` — "Entity direct path: Entity → Episode" in bundle search. "Cross-document entity bridging" example (MIT linking two documents).

### actions ❌
- No evidence of action tracking in the data model.

### keywords ❌
- No evidence of keyword/tag metadata on memory entries.

### context ✅
- `docs/RETRIEVAL_ARCHITECTURE.md` — Context stored implicitly via the cone graph structure: FacetPoints belong to Facets, Facets belong to Episodes. Full conversation context preserved within Episode bundles.
- `README.md` — "Each returned bundle is one Episode, scored by its strongest path of evidence." Bundle contains the Episode together with its Facets and FacetPoints.

### source ❌
- No evidence of explicit source tracking field in the data model.

### emotional ❌
- No evidence of emotional markers or sentiment tracking.

### conflict ❌
- No evidence of contradiction/conflict detection between memories.

### layeredMemory ✅
- `README.md` — Four-layer inverted cone graph: Episode (bounded semantic focus) → Facet (cross-sectional dimension) → FacetPoint (atomic assertion) → Entity (named thing bridging Episodes).
- `docs/RETRIEVAL_ARCHITECTURE.md` — Full specification of the four-level hierarchy with search entering at the tip (FacetPoint/Entity) and targeting Episodes at the base.
- `AGENTS.md` — `core/` domain models: Episode, Facet, FacetPoint.

### timeTravel ❌
- No evidence of version history, historical state querying, or time-travel retrieval.

### schemaFields: ~8
- Episode: summary, content, metadata (at least 3 fields)
- Facet: name, summary (at least 2 fields)
- FacetPoint: assertion/text, vector embedding (at least 2 fields)
- Entity: name, type (at least 2 fields)
- Edge: source_node_id, target_node_id, relationship_name, edge_text (at least 4 fields)
- Conservatively ~8 schema fields per stored memory unit depending on the level.

---

## Search & Retrieval

### fulltext ✅
- `m_flow-mcp/README.md` — `CHUNKS_LEXICAL` RecallMode: "Lexical search — precise text matching."
- `docs/RETRIEVAL_ARCHITECTURE.md` — Retrieval modes include Lexical as one of 5 modes.

### semantic ✅
- `README.md` — "Vector search casts a wide net across multiple granularities to find entry points."
- `docs/RETRIEVAL_ARCHITECTURE.md` — Query embedded and searched against seven vector collections covering every layer.

### hybrid ✅
- `m_flow-mcp/README.md` — `search` tool has `enable_hybrid_search` parameter.
- `docs/RETRIEVAL_ARCHITECTURE.md` — Phase 1: vector search across all collections. Phase 2: project into graph. Phase 3: propagate cost from tip to base combining vector distances and graph edge costs. This is vector+graph hybrid retrieval.
- `README.md` — "Retrieval is graph-routed: the system casts a wide net across all levels, projects the hits into the knowledge graph, propagates cost along supported evidence paths."

### deep ✅
- `docs/RETRIEVAL_ARCHITECTURE.md` — Graph-routed Bundle Search with multi-hop path-cost propagation. Paths like: FacetPoint → Facet → Episode (2 hops), Entity → Facet → Episode (2 hops), Entity → Episode (1 hop). Each hop accumulates cost: starting vector distance + edge vector distance + hop penalty. "The system performs multi-hop reasoning within 2-3 hops through cost arithmetic, without invoking an LLM at retrieval time."
- `README.md` — "Retrieval through reasoning and association — M-flow operates like a cognitive memory system."

### codeGraph ❌
- No evidence of code-specific graph analysis or symbol extraction. M-flow is a memory system, not a codebase tool.

### docsSearch ❌
- No evidence of documentation search/indexing feature.

### factQuery ✅
- `m_flow-mcp/README.md` — `TRIPLET_COMPLETION` RecallMode: "Triplet completion + LLM answer — general knowledge queries."
- `README.md` — "Triplet Completion is a simpler vector-based mode suited for customization and secondary development." Also: 5 retrieval modes including Triplet Completion.

### timeline ❌
- No evidence of temporal/timeline search or chronological querying. No TEMPORAL search mode listed among the 5 modes.

### searchModes: 5
- `m_flow-mcp/README.md` — RecallMode enum: `TRIPLET_COMPLETION`, `CHUNKS_LEXICAL`, `EPISODIC`, `PROCEDURAL`, `CYPHER`. Exactly 5 distinct search modes.
- `README.md` — "5 retrieval modes: Episodic, Procedural, Triplet Completion, Lexical, Cypher."

---

## Knowledge Lifecycle

### decay ❌
- No evidence of time-based decay, expiry, or forgetting curves. The system does apply "penalties" to broad/direct matches in retrieval but this is relevance scoring, not knowledge decay.

### supersede ❌
- No evidence of learning superseding or version replacement. The `update_data` MCP tool updates existing data entries but there's no evidence of a formal supersede mechanism with old-version preservation.

### contradiction ❌
- No evidence of contradiction detection between memories or conflict resolution.

### quarantine ❌
- No evidence of session or data quarantine mechanism.

### autoResolve ❌
- No evidence of automatic task/issue resolution.

### trustModel ❌
- No evidence of trust scoring, source credibility weighting, or confidence decay per source.

### explicitForget ✅
- `m_flow-mcp/README.md` — `delete` tool: "Delete data" with params `data_id`, `dataset_id`, `mode`. `prune` tool: "Selectively clear knowledge graph" with params `graph`, `vector`, `metadata`, `cache`.
- `AGENTS.md` — `api/` routers include `delete`.

---

## Extraction Pipeline

### autoExtract ✅
- `README.md` — Pipeline: Data Input → Extract (chunking, parsing) → Memorize (KG build, embeddings). LLM-based extraction via Instructor or BAML structured output framework.
- `.env.template` — `STRUCTURED_OUTPUT_FRAMEWORK="instructor"` (instructor | baml). Procedural memory extraction (`MFLOW_PROCEDURAL_ENABLED`).
- `CHANGELOG.md` — v0.3.1: "Procedural memory extraction and retrieval."

### contentPreproc ✅
- `coreference/README.md` — Dedicated coreference resolution module: resolves pronouns (he/she/it/their) to concrete antecedents before indexing. Supports Chinese (11 pronoun types, semantic role analysis) and English. Stream-level session processing across conversation turns.
- `README.md` — "Coreference resolution at ingestion: Pronouns are resolved into concrete antecedents before indexing. The graph stores actual names and entities, not pronouns."

### dedup ✅
- `CHANGELOG.md` — v0.3.4: "Fix dedup `_build_modern_id` tenant_id normalization"; v0.3.2: "KuzuDB adapter: entry-level deduplication."
- `CHANGELOG.md` — v0.3.4: "Fix graph relationship ledger UUID collision on batch insert" (dedup-related fix).
- Evidence of `deduplicate_nodes_and_edges` function.

### qualityRefine ❌
- No evidence of explicit quality scoring, filtering, or refinement pipeline step.

### narrative ❌
- No evidence of narrative extraction or story generation.

### clustering ❌
- No evidence of memory clustering or topic grouping beyond what the cone graph structure provides (Facets are topical cross-sections but generated per-Episode, not via clustering).

### recurrence ❌
- No evidence of recurring pattern detection or recurrence analysis.

### persona ❌
- No evidence of persona/profile extraction from conversation data. Face-aware partitioning is identity-based routing, not cognitive persona modeling.

---

## Platform Support

### p_claude ✅
- `m_flow-mcp/README.md` — Dedicated "Claude Desktop" section with exact config JSON for `claude_desktop_config.json`.
- `m_flow-mcp/README.md` — "M-flow MCP Server exposes M-flow knowledge graph functionality to AI assistants (such as Cursor, Claude Desktop, VS Code + Continue)."

### p_codex ❌
- No evidence of Codex-specific integration.

### p_opencode ❌
- No evidence of OpenCode-specific integration.

### p_gemini ❌
- No evidence of Gemini CLI-specific integration.

### p_copilot ❌
- `AGENTS.md` — "This file is intended for AI coding assistants (Cursor, Copilot, etc.)" — this is about the AGENTS file being readable, not about M-flow integration as a memory backend for Copilot. No MCP config for GitHub Copilot shown.

### p_cursor ✅
- `m_flow-mcp/README.md` — Dedicated "Cursor" section with exact MCP config JSON using SSE transport at `http://localhost:8001/sse`.

### p_windsurf ❌
- No evidence of Windsurf-specific integration.

### p_openclaw ✅
- `openclaw-skill/mflow-memory/README.md` — Dedicated OpenClaw skill: "clawhub install mflow-memory". "Your agent automatically gains memory tools via MCP." 11 MCP tools available.
- `README.md` — Links to OpenClaw Skill on clawhub.ai.

### p_hermes ❌
- No evidence of Hermes-specific integration.

### p_pi ❌
- No evidence of Pi-specific integration.

### p_antigravity ❌
- No evidence of Antigravity-specific integration.

---

## Benchmarks

### b_locomo ✅
- `README.md` — LoCoMo-10: M-flow scores **81.8%** (LLM-Judge, gpt-5-mini answer + gpt-4o-mini judge, top-k=10). Best among all tested systems (Cognee 79.4%, Zep 73.4%, Supermemory 64.4%, Mem0 50.4%).
- `mflow-benchmarks/README.md` — Full benchmark data: 1,540 questions, Category 5 (adversarial) excluded per standard methodology.

### b_longmemeval ✅
- `README.md` — LongMemEval: M-flow scores **89%** overall (93% temporal, 82% multi-session). Best among all tested systems (Supermemory 74%, Mem0 71%, Zep 61%, Cognee 57%).
- `mflow-benchmarks/README.md` — First 100 questions, all systems using gpt-5-mini + gpt-4o-mini judge + top-k=10.

### Evolving Events (additional benchmark) ✅
- `mflow-benchmarks/README.md` — Evolving Events (multi-hop reasoning): M-flow scores **97.7%** human-like correctness (k=10, gpt-5.4). Cognee 93.0%, Graphiti 68.4%.

### b_personamem ❌
- No evidence of PersonaMem benchmark testing.

### b_token ❌
- No evidence of token efficiency/cost benchmarking.

### b_methodology ✅
- `mflow-benchmarks/README.md` — Full methodology disclosed: LLM-Judge (binary CORRECT/WRONG with GPT-4 class models), Human-like Correctness (DirectLLM judge for semantic accuracy), BLEU-1/F1 token-level metrics. Identical prompts, metrics, and judge models across all systems.
- `mflow-benchmarks/README.md` — Reproduction scripts, raw data, and per-category breakdowns available for all benchmarks.
