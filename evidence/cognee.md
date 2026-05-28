# Cognee — Evidence

> Every ✅ claim backed by public source code or documentation.
> Audit date: 2026-05-28. Source: GitHub `topoteretes/cognee` main branch, `docs.cognee.ai`.

## Architecture

### Web/TUI ✅
- `README.md` — "To open the local UI, run: `cognee-cli -ui`". Launches full-stack UI at http://localhost:3000.
- `CLAUDE.md` — "Launch full stack with UI: `cognee-cli -ui`". Graph visualization server at `http://localhost:3000`.
- `CLAUDE.md` — `cognee/api/v1/visualize/` — `start_visualization_server()`: Python API to launch visualization on custom port.

### Offline — ❌→✅ (was claimed absent, but Cognee can run fully offline)
- `CLAUDE.md` — Ollama provider: local model inference via `ollama pull llama3.1:8b`, endpoint `http://localhost:11434/v1`.
- `CLAUDE.md` — llama.cpp provider: "full offline inference" with GGUF models, supports in-process and server modes.
- `CLAUDE.md` — Default databases are all local: SQLite (relational), LanceDB (vector), Ladybug (graph). No external services needed.
- `docs.cognee.ai/setup-configuration/llm-providers` — Ollama/LM Studio/llama.cpp sections all documented as local providers.
- `docs.cognee.ai/guides/local-setup` — Dedicated local setup guide for zero-API-key operation.

### LLM providers — 11+ (claims 1 — **UNDERCOUNT** ✅→🔺)
- `docs.cognee.ai/setup-configuration/llm-providers` — Lists 11+ distinct providers: OpenAI, Azure OpenAI, Google Gemini, Anthropic, AWS Bedrock, Groq, Ollama, LM Studio, HuggingFace, llama.cpp, Custom (OpenAI-compatible). Custom covers DeepSeek, OpenRouter, vLLM, Moonshot/Kimi, DeepInfra, self-hosted — each with dedicated docs sections.
- `CLAUDE.md` — Same list with configuration for each provider.
- **Finding**: Current data.js claims `llmFlex: 1`, but Cognee supports at least 11 distinct provider backends. Should be updated to 11+.

---

## Data Model

### Entities ✅
- `CLAUDE.md` — "extract_graph_from_data (LLM extracts entities/relationships using Instructor)" in the cognify pipeline.
- `cognee/shared/data_models.py` — `Node` Pydantic model: `id`, `name`, `type`, `description`. `Edge` model: `source_node_id`, `target_node_id`, `relationship_name`. `KnowledgeGraph` container with `nodes` and `edges` lists.
- `cognee/infrastructure/engine/models/` — `DataPoint` base class for all graph nodes (versioned, with metadata). `Edge` — graph relationships. `Triplet` — subject-predicate-object representation.
- `docs.cognee.ai/core-concepts/overview` — "Graph store — Captures entities and relationships in a knowledge graph (nodes and edges that show connections between concepts)."
- `README.md` — "combines embeddings, graphs and cognitive science approaches to make your documents both searchable by meaning and connected by relationships."

### Schema fields — ~10 (claims 10 ✅)
- `cognee/shared/data_models.py` — Node has 4 fields: `id`, `name`, `type`, `description`. Edge has 3: `source_node_id`, `target_node_id`, `relationship_name`.
- `CLAUDE.md` — DataPoint is versioned, with metadata. Dataset model tracks: name, user, permissions (read/write/delete/share), pipeline_status, provenance. Chunks track: text, chunk_id, chunk_index, chunk_size, cut_type.
- Distinct structured fields per memory entry approximate: name, type, description, dataset, user, permissions, pipeline_status, chunk_index, embedding vector, relationships — ~10. The claim of 10 fields is consistent with the data model.

---

## Search & Retrieval

### Full-text ✅
- `cognee/modules/search/types/SearchType.py` — `CHUNKS_LEXICAL` search type: "lexical (keyword) search over chunks".
- `CLAUDE.md` — Search types: "CHUNKS_LEXICAL — Lexical (keyword) search over chunks".
- `docs.cognee.ai/core-concepts/main-operations/recall` — "Exact quoted phrases bias toward lexical chunk search" in auto-routing. CHUNKS_LEXICAL returns: "Ranked chunk-like results for lexical matching; may include scores in addition to chunk text/metadata."

### Semantic/vector ✅
- `cognee/modules/search/types/SearchType.py` — `CHUNKS` search type (vector similarity search over chunks). `RAG_COMPLETION` (traditional RAG with chunks).
- `CLAUDE.md` — "Vector: LanceDB (default), ChromaDB, PGVector via VectorDBInterface". "Embedding Engines — Factory pattern for embeddings." CHUNKS is "Vector similarity search over chunks."
- `README.md` — "combines embeddings, graphs and cognitive science approaches."

### Hybrid (BM25+Vec) — ✅→❌ (claimed true, but no explicit BM25+Vec RRF mode)
- `cognee/modules/search/types/SearchType.py` — Full SearchType enum (17 types): SUMMARIES, CHUNKS, RAG_COMPLETION, TRIPLET_COMPLETION, GRAPH_COMPLETION, GRAPH_COMPLETION_DECOMPOSITION, GRAPH_SUMMARY_COMPLETION, CYPHER, NATURAL_LANGUAGE, GRAPH_COMPLETION_COT, GRAPH_COMPLETION_CONTEXT_EXTENSION, FEELING_LUCKY, TEMPORAL, CODING_RULES, CHUNKS_LEXICAL, AGENTIC_COMPLETION.
- **No HYBRID or combined BM25+vector search type exists in the SearchType enum.** Cognee has separate lexical (CHUNKS_LEXICAL) and vector (CHUNKS) modes, but no explicit result fusion (RRF or equivalent) between them.
- `docs.cognee.ai/core-concepts/main-operations/recall` — Auto-routing picks ONE search type per query — it does not fuse multiple modes. "Exact quoted phrases bias toward lexical chunk search" vs "Summary-style prompts... bias toward summary retrieval."
- `README.md` — "combines embeddings, graphs and cognitive science approaches" refers to the dual-storage architecture (vector + graph), not a BM25+vector RRF search mode.
- **Finding**: Claimed as `hybrid: true`, but Cognee has no BM25+vector result fusion. Should be changed to `false`.

### Code graph — ❌→✅ (was claimed absent, but Cognee has tree-sitter-based code extraction)
- `pyproject.toml` — `codegraph` extra: includes `tree-sitter>=0.24.0,<0.25` and `tree-sitter-python>=0.23.6,<0.24`.
- `CLAUDE.md` — Installation extras: "codegraph — Code graph extraction." Documented as an installable extra.
- `CLAUDE.md` — Search types: `CODING_RULES` — "Code-specific search rules."
- `cognee/shared/data_models.py` — `SummarizedCode`, `SummarizedFunction`, `SummarizedClass` models: code structure extraction with high-level summary, key features, imports, constants, classes, functions, workflow_description.
- `CLAUDE.md` — Document loaders support code files in `cognee/infrastructure/files/`. `ChunkStrategy.CODE` exists for code chunking.
- **Finding**: Was claimed absent (`codeGraph: false`). Cognee has tree-sitter-based code parsing, code-specific search mode (CODING_RULES), and structured code models. Should be `true`.

### Search modes — 1 claimed, but at least 5+ distinct modes (UNDERCOUNT ✅→🔺)
- `cognee/modules/search/types/SearchType.py` — 17 search types, but many are graph-completion variants. Distinct search approaches: lexical (CHUNKS_LEXICAL), vector (CHUNKS), graph completion (GRAPH_COMPLETION family), RAG (RAG_COMPLETION), triplet (TRIPLET_COMPLETION), summaries (SUMMARIES), temporal (TEMPORAL), coding rules (CODING_RULES), Cypher (CYPHER), natural language (NATURAL_LANGUAGE), agentic (AGENTIC_COMPLETION), auto-route (FEELING_LUCKY). At minimum: lexical, vector, graph, RAG, temporal = 5+.
- `docs.cognee.ai/core-concepts/main-operations/recall` — Auto-routing with multiple strategies, explicit `query_type` override for all search types.
- **Finding**: Current claim says `searchModes: 1`, but cognee has at least 5 distinct retrieval strategies. Should be updated to at least 5.

### Data sources — at least 3 ✅
- `CLAUDE.md` — Three storage systems: relational (SQLite/Postgres), vector (LanceDB/ChromaDB/PGVector), graph (Ladybug/Neo4j/Neptune).
- `docs.cognee.ai/core-concepts/overview` — "Cognee uses three complementary storage systems."
- Searches can hit graph data, vector data, session cache. Data sources = 3 (learnings/graph, session/cache, relational metadata).

---

## Knowledge Lifecycle

### Explicit forget ✅
- `docs.cognee.ai/core-concepts/main-operations/forget` — Comprehensive forget operation with 5 modes: single item, dataset, everything, memory-only (dataset), memory-only (single file).
- `README.md` — `await cognee.forget(dataset="main_dataset")` and `cognee-cli forget --all`.
- `README.md` — "Four operations — remember, recall, forget, and improve."
- `CLAUDE.md` — `delete(data_id)` method. CLI: `cognee-cli delete --all`.

---

## Extraction Pipeline

### Auto-extraction ✅
- `CLAUDE.md` — "cognify() - Extract entities/relationships and build knowledge graph" — automatic pipeline.
- `README.md` — `await cognee.remember("Cognee turns documents into AI memory.")` — single call ingests, extracts entities, and stores in graph automatically.
- `CLAUDE.md` — `cognify()` pipeline: `classify_documents → extract_chunks_from_documents → extract_graph_from_data → summarize_text → add_data_points`. Fully automated extraction, no manual save calls required.
- `docs.cognee.ai/core-concepts/overview` — "Remember — Store new memory in one call, either as permanent graph-backed memory or as session memory." No separate extraction step needed.

---

## Platform Support

### Claude Code ✅
- `README.md` — "Available as a plugin for your Claude Code — claude-code-plugin." Links to `topoteretes/cognee-integrations`.
- `CLAUDE.md` — "Claude Code" section with full setup instructions: pip install cognee, clone plugin, `claude --plugin-dir`.
- `README.md` — Plugin hooks: "SessionStart initializes memory, PostToolUse captures actions, UserPromptSubmit injects relevant context, PreCompact preserves memory across context resets, SessionEnd bridges session data into the permanent graph."

### OpenClaw ✅
- `README.md` — "Available as a plugin for your OpenClaw — cognee-openclaw." Links to npm package `@cognee/cognee-openclaw`.

---

## Claims correctly absent (verified no public evidence)

The following features are correctly absent from Cognee's public documentation:

**Architecture:** proxy, multiAgent — no evidence in README, docs, or source.

**Data Model:** actions, keywords, anticipatedQueries, triggerRules, domainTag, taskType, context, source, originTrust, emotional, conflict, layeredMemory, timeTravel — all ❌ (Cognee has graph nodes with type/description but no structured metadata fields for these; TEMPORAL search type exists for time-aware graph queries but is not a memory-state browsing or time-travel feature per CRITERIA.md).

**Search:** deep (no thinking trace search), docsSearch (no dedicated doc index search), factQuery (no structured metadata queries), timeline (no chronological browsing tool) — all ❌.

**Lifecycle:** decay, supersede, contradiction, quarantine, autoResolve, trustModel — all ❌ (forget() is explicit deletion — no automatic decay, no version chains, no contradiction detection).

**Extraction:** contentPreproc, dedup, qualityRefine, narrative, clustering, recurrence, persona — all ❌ (cognify pipeline is a single automated extraction pass; no dedup, quality refinement, narrative generation, clustering, recurrence detection, or persona extraction documented).

---

## Audit Notes

1. **offline ❌→✅**: Cognee can run fully offline with Ollama/llama.cpp + local LanceDB/Ladybug/SQLite. The local setup guide (`docs.cognee.ai/guides/local-setup`) documents zero-API-key operation. Should be changed from `false` to `true`.

2. **codeGraph ❌→✅**: Cognee's `codegraph` extra includes tree-sitter + tree-sitter-python for AST-based code parsing. `SummarizedCode`/`SummarizedFunction`/`SummarizedClass` models extract code structure. `CODING_RULES` search type exists for code-specific queries. Should be changed from `false` to `true`.

3. **hybrid ✅→❌**: Cognee has no combined BM25+vector RRF search mode in the SearchType enum. The README's "combines embeddings, graphs" refers to dual-storage architecture, not result fusion. Should be changed from `true` to `false`.

4. **llmFlex undercount**: data.js claims 1, but Cognee supports 11+ distinct LLM providers (OpenAI, Azure, Gemini, Anthropic, Bedrock, Groq, Ollama, LM Studio, HuggingFace, llama.cpp, Custom/compatible). Should be updated to 11+.

5. **searchModes undercount**: data.js claims 1, but Cognee has at least 5 distinct search strategies (lexical, vector, graph completion, RAG, temporal, plus more). Should be updated to at least 5.

6. **schemaFields 10**: Approximately correct. Node has id/name/type/description, plus dataset tracking, chunk metadata, pipeline status, permissions, embeddings — around 10 distinct structured fields.
