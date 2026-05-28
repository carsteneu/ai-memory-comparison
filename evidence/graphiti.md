# Graphiti — Evidence

> Every ✅ claim backed by public source code or documentation.
> Audit date: 2026-05-28. Source: GitHub `getzep/graphiti` main branch, `help.getzep.com/graphiti`, ArXiv 2501.13956.

---

## Data Model

### Entities ✅
- `graphiti_core/nodes.py` — `EntityNode` class: structured node with `uuid`, `name`, `name_embedding`, `group_id`, `labels`, `created_at`, `summary`, `attributes` fields. Entities are the core building block of the temporal knowledge graph.
- `README.md` — "Entities (nodes): People, products, policies, concepts — with summaries that evolve over time"
- `graphiti_core/graphiti.py` — `_extract_and_resolve_nodes()`: LLM-based entity extraction from episodes + deduplication against existing graph entities.
- `mcp_server/README.md` — Built-in entity types: Preference, Requirement, Procedure, Location, Event, Organization, Document, Topic, Object. "Graphiti MCP Server includes built-in entity types for structured knowledge extraction."

### Layered memory ✅
- `graphiti_core/nodes.py` — Hierarchical node types: `EpisodicNode` (L0: raw data with content/valid_at), `EntityNode` (L1: extracted entities with summaries), `CommunityNode` (L2: regional groupings of entities), `SagaNode` (L2+: incremental summaries of episode sequences).
- `README.md` — Component table: Episodes (provenance) → Entities/Facts (extracted nodes/edges) → Communities (derived groupings). "A context graph is a temporal graph of entities, relationships, and facts... Everything traces back to episodes — the raw data that produced it."
- `README.md` — "Build context graphs that evolve with every interaction — tracking what's true now and what was true before."
- ArXiv 2501.13956 — "Zep: A Temporal Knowledge Graph Architecture for Agent Memory" describes the hierarchical memory model.

### Time-travel ✅
- `graphiti_core/edges.py` — `EntityEdge` model: `valid_at`, `invalid_at`, `expired_at` datetime fields. Every fact carries a temporal validity window showing when it became true and when it stopped being true.
- `README.md` — "Temporal Fact Management: Facts have validity windows. When information changes, old facts are invalidated — not deleted. Query what's true now, or what was true at any point in time."
- `README.md` — "Unlike traditional knowledge graphs, each fact in a context graph has a validity window: when it became true, and when (if ever) it was superseded."
- `graphiti_core/utils/maintenance/edge_operations.py` — `resolve_edge_contradictions()`: Temporal comparison logic comparing `valid_at`/`invalid_at` between conflicting facts.
- ArXiv 2501.13956 — "explicit bi-temporal tracking with automatic fact invalidation"

### Schema fields — 8+ ✅
- `graphiti_core/nodes.py` — `EntityNode` Pydantic model: `uuid`, `name`, `name_embedding`, `group_id`, `labels`, `created_at`, `summary`, `attributes` = 8 fields.
- `graphiti_core/edges.py` — `EntityEdge` Pydantic model: `uuid`, `source_node_uuid`, `target_node_uuid`, `name`, `fact`, `fact_embedding`, `episodes`, `created_at`, `expired_at`, `valid_at`, `invalid_at`, `reference_time`, `attributes`, `group_id` = 14 fields.
- `graphiti_core/nodes.py` — `EpisodicNode`: `uuid`, `name`, `group_id`, `labels`, `created_at`, `source`, `source_description`, `content`, `valid_at`, `entity_edges`, `episode_metadata` = 11 fields.
- Combined unique fields across EntityNode + EntityEdge ≈ 18+. The 8 claim is conservative (EntityNode alone has 8); the actual full schema has 14+ per edge.

---

## Search & Retrieval

### Full-text (BM25) ✅
- `graphiti_core/graph_queries.py` — `get_fulltext_indices()`: Creates fulltext indexes on Episodic (`content`, `source`, `source_description`, `group_id`), Entity (`name`, `summary`, `group_id`), Community (`name`, `group_id`), and RELATES_TO edges (`name`, `fact`, `group_id`). Supports Neo4j, FalkorDB, and Kuzu backends.
- `graphiti_core/search/search.py` — `EdgeSearchMethod.bm25` triggers `edge_fulltext_search()`. `NodeSearchMethod.bm25` triggers `node_fulltext_search()`. `EpisodeSearchMethod.bm25` triggers `episode_fulltext_search()`.
- `README.md` — "Hybrid Retrieval: Combines semantic embeddings, keyword (BM25), and graph traversal."

### Semantic/vector ✅
- `graphiti_core/search/search.py` — `EdgeSearchMethod.cosine_similarity` triggers `edge_similarity_search()`. `NodeSearchMethod.cosine_similarity` triggers `node_similarity_search()`. Both use `query_vector` against stored embeddings.
- `graphiti_core/nodes.py` — `EntityNode.name_embedding` stores embedding vector, generated via `embedder.create()` on the entity name.
- `graphiti_core/edges.py` — `EntityEdge.fact_embedding` stores embedding vector, generated via `embedder.create()` on the fact text.
- `graphiti_core/graphiti.py` — Default embedder: `OpenAIEmbedder`. Supports OpenAI, Voyage, Sentence Transformers, Gemini embeddings.

### Hybrid (BM25+Vec) ✅
- `graphiti_core/search/search_config_recipes.py` — `EDGE_HYBRID_SEARCH_RRF`: Combines `[EdgeSearchMethod.bm25, EdgeSearchMethod.cosine_similarity]` with `EdgeReranker.rrf` (Reciprocal Rank Fusion). Same pattern for nodes, communities, and combined search.
- `graphiti_core/search/search.py` — `edge_search()`: Executes BM25 and cosine similarity in parallel via `semaphore_gather`, then fuses results with the configured reranker (RRF, MMR, cross-encoder, or node-distance).
- `README.md` — "Hybrid Retrieval: Combines semantic embeddings, keyword (BM25), and graph traversal for low-latency, high-precision queries."
- Pre-built search recipes: `COMBINED_HYBRID_SEARCH_RRF`, `COMBINED_HYBRID_SEARCH_MMR`, `COMBINED_HYBRID_SEARCH_CROSS_ENCODER` — each combining BM25 + vector + optional BFS with different fusion methods.

### Search modes — 2+ (claims 1 — **UNDERCOUNT** ✅→🔺)
- `graphiti_core/search/search.py` — Core `search()` dispatches to four distinct search scopes: `edge_search()`, `node_search()`, `episode_search()`, `community_search()`.
- `mcp_server/README.md` — MCP tools table lists separate `search_nodes` and `search_facts` as distinct user-facing tools. Also `get_entity_edge`, `get_episodes`.
- Pre-built search configs: 15+ named recipes (COMBINED_HYBRID_SEARCH_RRF, EDGE_HYBRID_SEARCH_RRF, NODE_HYBRID_SEARCH_MMR, etc.) supporting different search method + reranker combinations.
- **Finding**: Current data.js says 1, but MCP server exposes at least 2 distinct search tools (`search_nodes`, `search_facts`), and the core library supports 4 search scopes with configurable methods and rerankers. Should be at least 2.

---

## Knowledge Lifecycle

### Decay/forgetting — ❌ (claims ✅ — **CORRECTION** ✅→❌)
- No evidence of automatic time-based decay or relevance reduction. The `expired_at` field on `EntityEdge` is set only when facts are actively contradicted by new information during ingestion, not based on elapsed time or disuse.
- `graphiti_core/utils/maintenance/edge_operations.py` — `resolve_edge_contradictions()`: `expired_at` is set to `utc_now()` when a new fact invalidates an old one. This is a supersede mechanism, not decay.
- `README.md` — No mention of forgetting, decay, staleness, or time-based relevance reduction.
- **Finding**: Graphiti has temporal fact management (valid_at/invalid_at windows) and supersede via contradiction, but no automatic decay based on time or disuse. The "decay" claim should be changed to `false`.

### Supersede/replace ✅
- `graphiti_core/utils/maintenance/edge_operations.py` — `resolve_edge_contradictions()`: Explicitly sets `edge.expired_at` and `edge.invalid_at` on conflicting edges when a newer fact arrives. The superseded edge remains in the graph with its temporal end marked, creating a traceable chain.
- `graphiti_core/edges.py` — `EntityEdge.expired_at` field: "datetime of when the node was invalidated." `EntityEdge.invalid_at`: "datetime of when the fact stopped being true."
- `README.md` — "When information changes, old facts are invalidated — not deleted." and "Automatic fact invalidation with temporal history preserved."
- `README.md` — "Facts have validity windows. When information changes, old facts are invalidated — not deleted. Query what's true now, or what was true at any point in time."

### Explicit forget — ✅ (claims ❌ — **DISCOVERY** ❌→✅)
- `graphiti_core/nodes.py` — `Node.delete()` method on all node types. `Node.delete_by_uuids()` for batch deletion. `Node.delete_by_group_id()` for bulk cleanup.
- `graphiti_core/edges.py` — `Edge.delete()` and `Edge.delete_by_uuids()` methods on all edge types.
- `mcp_server/README.md` — MCP tools: `delete_entity_edge` ("Delete an entity edge from the knowledge graph"), `delete_episode` ("Delete an episode from the knowledge graph"), `clear_graph` ("Clear all data from the knowledge graph and rebuild indices").
- **Finding**: Graphiti supports explicit deletion at the API, MCP, and library levels. Should be marked `true`.

---

## Extraction Pipeline

### Auto-extraction ✅
- `graphiti_core/graphiti.py` — `add_episode()` method: Full automatic pipeline — episode ingestion → node extraction → node resolution → edge extraction → edge resolution (with dedup + invalidation) → attribute extraction → persistence. No manual `save` calls needed.
- `graphiti_core/graphiti.py` — Pipeline steps: `extract_nodes()` (LLM-based), `resolve_extracted_nodes()` (dedup against graph), `extract_edges()` (LLM-based), `resolve_extracted_edges()` (dedup + contradiction + invalidation), `extract_attributes_from_nodes()`.
- `README.md` — "Graphiti continuously integrates user interactions, structured and unstructured enterprise data, and external information into a coherent, queryable graph."
- `README.md` — "Incremental Graph Construction: New data integrates immediately without batch recomputation. The graph evolves in real-time as episodes are ingested."

### Deduplication — ✅ (claims ❌ — **DISCOVERY** ❌→✅)
- `graphiti_core/utils/maintenance/edge_operations.py` — `resolve_extracted_edges()`: Exact-match dedup using `_normalize_string_exact()`. Fast path: "if the fact text and endpoints already exist verbatim, reuse the matching edge."
- `graphiti_core/utils/maintenance/edge_operations.py` — `resolve_extracted_edge()`: LLM-based dedup via `EdgeDuplicate` response model. The LLM evaluates whether new facts match existing ones semantically.
- `graphiti_core/utils/maintenance/edge_operations.py` — In-extraction dedup: `seen: dict[tuple[str, str, str], EntityEdge]` to catch exact duplicates within a single extraction batch before parallel processing.
- `graphiti_core/graphiti.py` — `_extract_and_dedupe_nodes_bulk()`: `dedupe_nodes_bulk()` function for batch node deduplication.

### Narrative generation — ✅ (claims ❌ — **DISCOVERY** ❌→✅)
- `graphiti_core/nodes.py` — `SagaNode` class: stores `summary`, `first_episode_uuid`, `last_episode_uuid`, `last_summarized_at` fields. Represents an ongoing narrative thread.
- `graphiti_core/graphiti.py` — `summarize_saga()` method: Incrementally summarizes a saga using only new episodes since the last summary. Maintains two watermarks: `last_summarized_at` (wall-clock filter) and `last_summarized_episode_valid_at` (temporal). Uses LLM to generate narrative summaries from episode sequences.
- `README.md` — (in the code, sagas are documented in graphiti.py docstrings and the SagaNode model)

### Clustering — ✅ (claims ❌ — **DISCOVERY** ❌→✅)
- `graphiti_core/nodes.py` — `CommunityNode` class: Groups related entities into semantic communities with `name` and `summary` fields. `CommunityEdge` connects communities to member entities.
- `graphiti_core/graphiti.py` — `update_communities` parameter on `add_episode()`: When True, triggers `update_community()` for each node, which groups related entities by their relationships.
- `graphiti_core/graphiti.py` — `build_communities()` and `remove_communities()` functions in `community_operations`.
- `README.md` — "Communities" listed as a graph component alongside entities, facts, and episodes.

---

## Platform Support

### Claude Code — ✅ (claims ❌ — **DISCOVERY** ❌→✅)
- `mcp_server/README.md` — "Integrating with Claude Desktop" section with full configuration instructions. Uses `mcp-remote` gateway for HTTP transport. Includes `stdio` transport option for Claude Desktop.
- `README.md` — MCP server announcement: "Check out the new MCP server for Graphiti! Give Claude, Cursor, and other MCP clients powerful context graph-based memory with temporal awareness."
- Repository contains `CLAUDE.md` and `AGENTS.md` files for AI coding assistants.

### Cursor — ✅ (claims ❌ — **DISCOVERY** ❌→✅)
- `mcp_server/README.md` — "Integrating with the Cursor IDE" section with step-by-step instructions. "The integration enables AI assistants in Cursor to maintain persistent memory through Graphiti's knowledge graph capabilities."
- `mcp_server/README.md` — Cursor configuration JSON example: `{"mcpServers": {"graphiti-memory": {"url": "http://localhost:8000/mcp/"}}}`
- `mcp_server/README.md` — References `cursor_rules.md` for Cursor's User Rules integration.

---

## Claims correctly marked false — verified

The following features are correctly marked `false` in data.js. No public evidence was found:

**Architecture:** proxy — ❌ (Graphiti is a library, not a proxy)
**Data Model:** actions, keywords, anticipatedQueries, triggerRules, domainTag, taskType, context, source (has EpisodeType but no 3-level attribution), originTrust, emotional — all ❌
**Search:** deep (no thinking trace search), codeGraph, docsSearch, factQuery, timeline — all ❌
**Lifecycle:** quarantine, autoResolve, trustModel — all ❌
**Extraction:** contentPreproc, qualityRefine, recurrence, persona — all ❌
**Platform:** OpenCode, Gemini CLI, Copilot CLI (MCP mentions VS Code Copilot but not Copilot CLI specifically), Windsurf, OpenClaw, Hermes, pi/omp, Antigravity — all ❌

### Contradiction detection — borderline (kept ❌)
- `graphiti_core/utils/maintenance/edge_operations.py` — `resolve_edge_contradictions()` + LLM-based `contradicted_facts` detection. Graphiti detects when new facts contradict existing ones and auto-resolves by invalidating old edges. However, this is an internal auto-resolution mechanism, not user-facing "conflict surfacing." The detection happens but conflicts are automatically resolved rather than surfaced for review. Kept as ❌ per CRITERIA's "detects AND surfaces" requirement.

---

## Audit Notes

1. **decay → ❌**: The `expired_at` mechanism is contradiction-driven supersede, not time/disuse-based decay. Change from `true` to `false`.

2. **explicitForget → ✅**: Delete methods exist on nodes, edges, and via MCP tools (`delete_entity_edge`, `delete_episode`, `clear_graph`). Change from `false` to `true`.

3. **dedup → ✅**: Exact-match and LLM-based deduplication during edge/entity resolution. Change from `false` to `true`.

4. **narrative → ✅**: `SagaNode` with `summarize_saga()` provides incremental narrative summaries from episode sequences. Change from `false` to `true`.

5. **clustering → ✅**: `CommunityNode` groups related entities by semantic relationship. Change from `false` to `true`.

6. **searchModes → 🔺**: At least 2 distinct search tools (`search_nodes`, `search_facts`) via MCP, plus 4 core search scopes. Current value `1` is an undercount. Should be `2`.

7. **Platform additions**: `p_claude` and `p_cursor` should both be `true` — the MCP server is explicitly documented for both.

8. **schemaFields confirmed**: EntityNode alone has 8 fields (uuid, name, name_embedding, group_id, labels, created_at, summary, attributes). EntityEdge adds 14 more. The 8 claim is a minimum; actual model is richer.
