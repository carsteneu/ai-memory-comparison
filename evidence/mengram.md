# Mengram — Evidence

> **GitHub**: https://github.com/alibaizhanov/mengram
> **Stars**: 171 | **Forks**: 26 | **License**: Apache 2.0
> **Language**: Python (primary, + JavaScript/TypeScript SDK)
> **Created**: 2026-02-10
> **Deployment**: Cloud (mengram.io API) + Self-hosted (Ollama/Docker)
> **Storage**: PostgreSQL+pgvector (cloud) / SQLite+vectors (self-hosted)
> **Integration**: API/SDK/MCP/Hooks/LangChain/CrewAI/OpenClaw
> **Setup**: `pip install mengram-ai` or `mengram setup` (interactive)
> **Pricing**: Freemium (free tier, Pro/Growth/Business plans)
> **Docs**: https://mengram.io/docs
> **Description**: Human-like memory for AI agents — semantic, episodic & procedural. Experience-driven procedures that learn from failures. Free API, Python & JS SDKs, LangChain, CrewAI & OpenClaw integrations.

---

## Vital Signs

### Stars ✅
- `[GitHub API]` — stargazers_count: 171

### Language ✅
- `[GitHub API]` — language: "Python"
- `[repo topics]` — "python"

### License ✅
- `[GitHub API]` — license.key: "apache-2.0", spdx_id: "Apache-2.0"
- `[LICENSE]` — Full Apache 2.0 text in repo

### Created ✅
- `[GitHub API]` — created_at: "2026-02-10T19:20:33Z"

---

## Architecture

### Deployment ✅
- `[README Deploy Section]` — Cloud mode via mengram.io API + self-hosted mode (Ollama/Docker)
- `[ARCHITECTURE.md]` — "Two Modes: Cloud Mode (Production — mengram.io), Local Mode (Self-hosted)"
- `[cloud/Dockerfile]` — Docker deployment
- `[cloud/docker-compose.yml]` — Docker Compose config for cloud self-hosting

### Storage ✅
- `[ARCHITECTURE.md]` — "PostgreSQL + pgvector" (cloud), "SQLite vectors + knowledge graph" (local)
- `[cloud/schema.sql]` — Full PostgreSQL schema with pgvector extensions
- `[schema.sql:CREATE EXTENSION]` — `vector` and `uuid-ossp` extensions
- `[engine/vector/vector_store.py]` — SQLite vector store for local mode

### Web/TUI ✅
- `[README]` — "Console" link to mengram.io/dashboard
- `[cloud/dashboard.html]` — 261KB dashboard HTML file
- `[cloud/landing.html]` — 202KB landing page

### Offline ✅
- `[ARCHITECTURE.md Local Mode]` — Self-hosted mode: "SQLite vectors + knowledge graph" works fully offline
- `[README Self-Hosted (Ollama)]` — "When running locally with Ollama" — supports llama3.1, mistral, gemma2

### LLM providers ✅ (5+)
- `[ARCHITECTURE.md]` — "Claude Sonnet / GPT-4o-mini" for extraction, "Ollama (llama3.1, mistral, gemma2)" for self-hosted, Cohere for embeddings
- `[engine/extractor/llm_client.py]` — Multi-provider LLM client
- `[cloud/embedder.py]` — OpenAI embeddings (API-based)
- `[engine/vector/embedder.py]` — Local embeddings

### Procedural memory ✅
- `[README]` — "3 types of memory: Semantic, Episodic, Procedural"
- `[README]` — "Procedural — workflows that evolve"
- `[cloud/schema.sql:procedures table]` — Full procedures table: steps JSONB, version INT, parent_version_id, evolved_from_episode
- `[cloud/evolution.py]` — EvolutionEngine: evolve_on_failure, detect_and_create_from_episodes
- `[cloud/schema.sql:procedure_evolution table]` — Evolution log: change_type, diff, version_before, version_after

---

## Data Model

### Entities ✅
- `[cloud/schema.sql:entities table]` — entities: id, name, type, metadata, created_at, updated_at
- `[ARCHITECTURE.md]` — "ConversationExtractor → LLM → entities, facts, relations"

### Actions ✅
- `[cloud/schema.sql:procedures]` — procedures.steps JSONB — each step has action + detail
- `[cloud/schema.sql:procedure_evolution]` — Tracks actions: step_added, step_removed, step_modified, step_reordered
- `[cloud/evolution.py:FAILURE_INDICATORS]` — Detects actions from failure keywords
- `[api/cloud_mcp_server.py:checkpoint tool]` — Checkpoint tool captures decisions and learnings as structured actions

### Keywords/tags ✅
- `[cloud/schema.sql:procedures.entity_names]` — Entity names as tags on procedures
- `[cloud/schema.sql:episodes.participants]` — Participants array on episodes
- `[README Metadata Filters]` — `m.search("config", filters={"agent_id": "support-bot", "app_id": "prod"})`

### Trigger rules ✅
- `[cloud/schema.sql:memory_triggers table]` — trigger_type (reminder, contradiction, pattern), fire_at, source_type, source_id
- `[cloud/schema.sql:procedures.trigger_condition]` — When to use this procedure
- `[README API Reference]` — `GET /v1/triggers` — "Smart Triggers (reminders, contradictions, patterns)"

### Context (why) ✅
- `[cloud/schema.sql:episodes.context]` — Explicit context field on episodes
- `[cloud/schema.sql:episodes.outcome]` — Outcome tracking alongside summary
- `[README]` — Episodes store "events, decisions, outcomes"
- `[cloud/schema.sql:knowledge]` — Knowledge has scope field: entity, cross, temporal, insight

### Source attribution ✅
- `[cloud/schema.sql:memory_triggers.source_type + source_id]` — Tracks source of triggers
- `[cloud/schema.sql:episodes.participants]` — Who was involved
- `[cloud/schema.sql:procedures.source_episode_ids]` — Which episodes generated the procedure
- `[cloud/schema.sql:procedures.evolved_from_episode]` — Which episode triggered evolution

### Emotional ✅
- `[cloud/schema.sql:episodes.emotional_valence]` — VARCHAR(20): positive, negative, neutral, mixed
- `[cloud/evolution.py:is_failure_episode]` — Logic checking emotional_valence for failure classification

### Conflict surfacing ✅
- `[cloud/schema.sql:memory_triggers]` — trigger_type = 'contradiction' explicitly
- `[ARCHITECTURE.md Smart Triggers]` — "Contradictions" as a trigger category
- `[cloud/schema.sql:facts]` — archived + superseded_by fields for contradiction resolution

### Layered memory ✅
- `[ARCHITECTURE.md]` — "3 types of memory — like a human brain": Semantic (entities/facts/knowledge) → Episodic (events) → Procedural (workflows)
- `[cloud/schema.sql]` — Separate tables: entities + facts + knowledge (semantic), episodes (episodic), procedures (procedural)
- `[README Comparison Table]` — Mengram has all 3 types marked "Yes"

### Time-travel ✅
- `[cloud/schema.sql:procedure_evolution]` — Full version history with diffs
- `[cloud/schema.sql:procedures.parent_version_id + version + is_current]` — Version chain
- `[cloud/schema.sql:facts.superseded_by]` — Tracks replacement chain
- `[README API Reference]` — `GET /v1/procedures/{id}/history` — "Version history + evolution log"
- `[api/cloud_mcp_server.py:procedure_history tool]` — "Show how a procedure evolved over time — all versions and what changed"

### Schema fields ✅ (26)
- entities: name, type, metadata (3)
- facts: content, event_date, archived, superseded_by, importance, access_count, expires_at (7)
- relations: type, description (2)
- knowledge: type, title, content, artifact, scope, confidence, based_on_facts (7)
- episodes: summary, context, outcome, participants, emotional_valence, importance, linked_procedure_id, failed_at_step, happened_at, metadata (7 meaningful — linked_procedure_id/failed_at_step/importance are internal)
- procedures: name, trigger_condition, steps, source_episode_ids, entity_names, success_count, fail_count, version, parent_version_id, evolved_from_episode, is_current, metadata (7 meaningful)
- memory_triggers: trigger_type, title, detail, source_type, source_id, fire_at (5)
- embeddings: embedding vector(1536), tsv tsvector, chunk_text (2 — shared across entity/episode/procedure embeds)

Approximately 26 distinct structured fields across the data model (excluding auto-generated IDs and timestamps).

---

## Search & Retrieval

### Full-text ✅
- `[cloud/schema.sql]` — tsvector columns with GIN indexes on: embeddings, episode_embeddings, procedure_embeddings, chunk_embeddings
- `[ARCHITECTURE.md]` — "BM25 hybrid search" (cloud mode)
- `[schema.sql:CREATE INDEX idx_embeddings_tsv]` — GIN index for fast BM25 text search

### Semantic/vector ✅
- `[cloud/schema.sql]` — pgvector HNSW: `CREATE INDEX idx_embeddings_hnsw ON embeddings USING hnsw (embedding vector_cosine_ops)`
- `[ARCHITECTURE.md]` — "HNSW index · BM25 hybrid search · LLM re-ranking · Matryoshka 1536D"
- `[README]` — "Cohere multilingual embeddings + rerank"

### Hybrid (BM25+Vec) ✅
- `[ARCHITECTURE.md Cloud Mode]` — "PostgreSQL + pgvector ... HNSW index · BM25 hybrid search · LLM re-ranking"
- `[cloud/schema.sql]` — Each embedding table has both vector(1536) column and tsvector column with GIN index
- `[engine/retrieval/hybrid_search.py]` — Local hybrid: "Vector Search + Graph Traversal"

### Fact metadata query ✅
- `[api/cloud_mcp_server.py:list_episodes]` — Query episodes by search terms
- `[api/cloud_mcp_server.py:list_procedures]` — Query procedures by name, trigger, step content
- `[api/cloud_mcp_server.py:get_triggers]` — Filter by type (reminder, contradiction, pattern)
- `[api/cloud_mcp_server.py:get_reflections]` — Filter by scope (entity, cross, temporal)
- `[api/cloud_mcp_server.py:list_memories]` — List all entities with types and fact counts

### Timeline view ✅
- `[api/cloud_mcp_server.py:timeline tool]` — "Search memory by time" with after/before ISO datetime params
- `[cloud/schema.sql:episodes.happened_at]` — Extracted event date
- `[cloud/schema.sql:facts.event_date]` — Event date on facts
- `[README SDK]` — `m.episodes(query="deployment")` returns date-ordered events

### Search modes ✅ (14)
API-level distinct retrieval endpoints + MCP tools:
1. `/v1/search` — Semantic search
2. `/v1/search/all` — Unified search (semantic + episodic + procedural)
3. `/v1/episodes/search` — Episode search
4. `/v1/procedures/search` — Procedure search
5. `m.ask()` / `/v1/ask` — RAG with citations
6. `/v1/profile` — Cognitive Profile
7. `/v1/triggers` — Smart Triggers
8. `/v1/agents/run` — Memory agents (curator, connector, digest)
9. `timeline` MCP tool — Time-based search
10. `context_for` MCP tool — Task-specific context retrieval
11. `get_graph` MCP tool — Knowledge graph retrieval
12. `get_insights` MCP tool — AI-generated insight retrieval
13. `get_reflections` MCP tool — Reflection retrieval by scope
14. `get_feed` MCP tool — Activity feed / recent changes

### Data sources ✅ (4)
1. Semantic (entities + facts + knowledge)
2. Episodic (events, interactions, outcomes)
3. Procedural (workflows, skills, evolution history)
4. Conversation chunks (raw conversation fallback)
- `[cloud/schema.sql:conversation_chunks table + chunk_embeddings]` — Raw text fallback

---

## Knowledge Lifecycle

### Decay/forgetting ✅
- `[cloud/schema.sql:facts.expires_at]` — TTL expiry on facts
- `[cloud/schema.sql:episodes.expires_at]` — TTL expiry on episodes
- `[cloud/schema.sql:procedures.expires_at]` — TTL expiry on procedures

### Supersede/replace ✅
- `[cloud/schema.sql:facts.superseded_by]` — "tracks what replaced this fact"
- `[cloud/schema.sql:procedures.parent_version_id + is_current]` — Version chain: "only latest version is current"
- `[cloud/schema.sql:procedure_evolution]` — Full evolution log: version_before, version_after, diffs
- `[cloud/evolution.py:evolve_on_failure]` — Creates new procedure version on failure

### Contradiction detect ✅
- `[cloud/schema.sql:memory_triggers]` — trigger_type = 'contradiction'
- `[ARCHITECTURE.md Smart Triggers]` — "Contradictions" explicitly listed
- `[cloud/schema.sql:facts]` — archived + superseded_by for contradiction resolution workflow

### Explicit forget ✅
- `[api/cloud_mcp_server.py:delete_entity tool]` — "Delete an entity and all its data (facts, relations, knowledge)"
- `[api/cloud_mcp_server.py:archive_fact tool]` — "Archive a specific fact on an entity — soft-delete without removing the entity"
- `[cloud/schema.sql:webhooks.event_types]` — Includes "memory_delete" as webhook event

---

## Extraction Pipeline

### Auto-extraction ✅
- `[ARCHITECTURE.md]` — "You chat with any AI... The system automatically extracts knowledge from conversations"
- `[engine/extractor/conversation_extractor.py]` — 41KB conversation extractor
- `[README Claude Code Hooks]` — "Every Prompt → Searches past sessions... After Response → Saves new knowledge in background (auto-save)"
- `[cloud/evolution.py:detect_and_create_from_episodes]` — Auto-creates procedures from 3+ similar episodes

### Deduplication ✅
- `[cloud/schema.sql:idx_entities_user_sub_lname]` — Case-insensitive unique index: `LOWER(name)` prevents "Python"+"python" duplicates
- `[cloud/schema.sql:idx_procedures_user_sub_lname_ver]` — Case-insensitive unique on procedure names
- `[api/cloud_mcp_server.py:dedup tool]` — "Find and automatically merge duplicate entities"
- `[api/cloud_mcp_server.py:merge_entities tool]` — "Merge two entities into one — combines facts, relations, and knowledge"

### Narrative generation ✅
- `[README Cognitive Profile]` — "One API call generates a system prompt from all memories"
- `[api/cloud_mcp_server.py:checkpoint tool]` — Session checkpoint with summary, decisions, learnings, next steps
- `[api/cloud_mcp_server.py:run_agents digest]` — Weekly digest with headline and recommendation
- `[api/cloud_mcp_server.py:generate_rules_file]` — Auto-generates CLAUDE.md/.cursorrules/.windsurfrules from memory

### Clustering ✅
- `[cloud/evolution.py:_cluster_episodes_by_embedding]` — Embedding similarity clustering (greedy, similarity_threshold=0.65)
- `[cloud/evolution.py:detect_and_create_from_episodes]` — Clusters unlinked episodes by embedding → extracts common procedure
- `[cloud/evolution.py:compute_link_score]` — 3-signal entity+keyword+vector linking for episode↔procedure

### Recurrence detection ✅
- `[cloud/evolution.py:detect_and_create_from_episodes]` — Detects patterns from 2+ similar episodes; auto-creates at 3+
- `[cloud/schema.sql:memory_triggers]` — trigger_type = 'pattern'
- `[api/cloud_mcp_server.py:run_agents connector]` — Finds hidden patterns and insights across memories

### Persona extraction ✅
- `[README Cognitive Profile]` — "One API call generates a system prompt from all memories" — extracts user traits, preferences, working style
- `[api/cloud_mcp_server.py:get_insights tool]` — "AI-generated insights about the user — patterns, connections, reflections"
- `[api/cloud_mcp_server.py:get_reflections tool]` — Cross-entity and temporal insights
- `[api/cloud_mcp_server.py:generate_rules_file]` — Generates personalized AI coding assistant rules from memory

---

## Platform Support

### Claude Code ✅
- `[README]` — "Claude Code — Zero-Config Memory": `mengram hook install` with 3 hooks (profile on start, recall on prompt, save after response)
- `[README MCP]` — Standard MCP server config for Claude Desktop: `"mengram": { "command": "mengram", "args": ["server", "--cloud"] }`
- `[api/cloud_mcp_server.py]` — Full MCP server implementation for Claude Desktop
- `[README Claude Managed Agents]` — MCP URL for hosted Claude agents

### Codex ✅
- `[README Install Section]` — "Paste this into Claude Desktop, Cursor, Codex, Claude Code, or Windsurf"
- `[README MCP Section]` — "MCP Server — Claude Desktop, Cursor, Codex, Windsurf, Cline"

### Cursor ✅
- `[README Install Section]` — "Paste this into Claude Desktop, Cursor, Codex, Claude Code, or Windsurf"
- `[README MCP Section]` — "MCP Server — Claude Desktop, Cursor, Codex, Windsurf, Cline"
- `[api/cloud_mcp_server.py:generate_rules_file]` — Supports .cursorrules output format
- `[vscode-mengram/]` — VS Code extension directory (Cline is VS Code-based)

### Windsurf ✅
- `[README Install Section]` — "Paste this into Claude Desktop, Cursor, Codex, Claude Code, or Windsurf"
- `[README MCP Section]` — "MCP Server — Claude Desktop, Cursor, Codex, Windsurf, Cline"
- `[api/cloud_mcp_server.py:generate_rules_file]` — Supports .windsurfrules output format

### Cline ✅
- `[README MCP Section]` — "MCP Server — Claude Desktop, Cursor, Codex, Windsurf, **Cline**" (explicitly named)
- `[vscode-mengram/src/SessionTracker.ts]` — VS Code session tracking extension (Cline-compatible since Cline runs in VS Code)

### OpenClaw ✅
- `[README OpenClaw]` — Explicit section: `openclaw plugins install openclaw-mengram`
- `[integrations/openclaw/]` — Full OpenClaw skill: SKILL.md, bash scripts (mengram-add, mengram-search, mengram-profile, mengram-setup, mengram-workflow)
- `[README OpenClaw Features]` — "Auto-recall before every turn, auto-capture after. 12 tools, slash commands, Graph RAG."
- `[ARCHITECTURE.md]` — OpenClaw listed as integration target

---

## Benchmarks

### LoCoMo ✅
- `[benchmarks/locomo_bench.py]` — Full benchmark implementation: ingestion, retrieval, answer generation, scoring pipeline
- `[benchmarks/locomo_bench.py]` — Reference scores: "Mem0 ~68% | Zep ~75% | Backboard ~90%"
- `[benchmarks/locomo_metrics.py]` — Metric computation: F1 scoring, LLM-as-judge, aggregate scores
- **Score**: No published Mengram score yet — benchmark infrastructure exists but results not published
- NOTE: Benchmarks directory and code exist but no specific Mengram score is claimed in the README. The README comparison table makes no benchmark claims.

### Methodology open ✅
- `[benchmarks/locomo_bench.py]` — Full benchmark scripts are open-source and reproducible
- `[benchmarks/locomo_metrics.py]` — Scoring methodology is transparent
- Manual reproduction: `python benchmarks/locomo_bench.py --api-key om-...` with public LoCoMo dataset
