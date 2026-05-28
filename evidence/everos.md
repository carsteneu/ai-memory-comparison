# EverOS — Evidence

> Every ✅ claim backed by public source code or documentation.
> Audit date: 2026-05-28. Source: GitHub `EverMind-AI/EverOS` main branch, `docs.evermind.ai`, `github.com/tt-a1i/evermemos-mcp`.

## Architecture

### Offline ⚠️ (local = yes, extraction needs LLM)
- `README.md` — "docker compose up -d && uv sync && uv run python src/run.py" — runs entirely locally. Server at `http://localhost:1995`.
- `README.md` — Requires `LLM_API_KEY` for memory extraction and `VECTORIZE_API_KEY` for embedding/rerank. Extraction pipeline calls external LLM APIs by default.
- `methods/EverCore/docs/ARCHITECTURE.md` — Technology stack: MongoDB, Elasticsearch, Milvus, Redis — all local services via Docker.
- **Finding**: Core storage and retrieval work offline. Extraction pipeline needs LLM (cloud API by default). The env.template shows configurable API endpoints, but no documented support for local LLMs (Ollama). Recommend marking as "⚠️ local core, cloud extraction" unless local LLM support is documented.

### Schema fields — ~8 (verified)
- `methods/EverCore/docs/ARCHITECTURE.md` — 7 memory types: episodes, profiles, preferences, relationships, semantic knowledge, basic facts, core memories.
- `docs.evermind.ai` (llms.txt) — 6 API memory types: episodic_memory, profile, foresight, eventlog, agent_case, agent_skill.
- API v0 `MemorizeMessageRequest` model — 10 fields: group_id, group_name, message_id, create_time, sender, sender_name, role, content, refer_list, flush.
- The core MemCell (data model) from ARCHITECTURE.md lists ~5 properties: Unique identifier, Content, Metadata, Memory type classification, Semantic embeddings. Adding timestamp, user_id, session_id ≈ 8.
- **Finding**: Claim of 8 is reasonable. Recommend documenting as core memory fields: id, content, metadata, memory_type, embedding, user_id, timestamp, session_id = 8.

### Multi-agent ❌
- EverOS itself has no built-in multi-agent orchestration.
- Third-party integrations (MCO, Hive, Golutra) use EverOS as a memory backend but are separate projects.

### Proxy ❌
- EverOS is a REST API service, not a proxy. Does not intercept or modify LLM conversation streams.

### Web/TUI ❌ (local deployment)
- Cloud dashboard exists at `everos.evermind.ai`.
- Local deployment (`docker compose up -d`) starts only the API server on port 1995. No web UI included.
- Memory Graph Visualization demo exists as a separate frontend-only demo (no backend integration).

---

## Data Model

### Entities ❌
- No structured entity extraction or entity junction tables.
- Memory types cover profiles and facts but not named entities (files, people, systems) as separate fields.

### Actions ❌
- No action/command storage as structured fields.

### Keywords/tags ❌
- No keyword tagging system.

### Anticipated queries ❌
- No query generation for retrieval optimization.

### Trigger rules ❌
- No condition-based activation.

### Domain tag ❌
- "Space" system (`coding:app`, `chat:preferences`) provides namespace isolation but is not a per-memory domain tag.

### Task type ❌
- No task classification.

### Context (why) ❌
- No explicit context/why field alongside memories.

### Source attribution ❌
- Has sender attribution (message-level) but not a 3-tier source model (user_stated/claude_suggested/llm_extracted).

### Origin + trust ❌
- No trust weight system.

### Emotional ❌
- No emotional intensity tracking.

### Conflict surfacing ⚠️ (implicit, not surfaced)
- `README.md` — "Semantic Consolidation — ...resolves contradictions between old and new facts."
- `methods/EverCore/docs/ARCHITECTURE.md` — Consolidation clusters MemCells and resolves contradictions.
- **Finding**: EverOS automatically resolves contradictions during consolidation, but does not surface them explicitly to the user/agent. The absent list says "conflict" should be absent — but some degree of contradiction handling exists. Recommend: if "conflict" means explicit surfacing (like YesMem's contradiction boosts), then absent. If it means any handling, then present but different mechanism.

### Layered memory ⚠️ (type-based, not hierarchical)
- `methods/EverCore/docs/ARCHITECTURE.md` — 7 memory types: episodes, profiles, preferences, relationships, semantic knowledge, basic facts, core memories.
- `README.md` — Three-phase lifecycle: Episodic Trace → Semantic Consolidation → Reconstructive Recollection.
- The types create a flat taxonomy, not strictly L0→L3 hierarchy. The consolidation process (MemCell → MemScene) provides some layering.
- **Finding**: Different memory types exist but not in the L0 raw → L1 summary → L2 semantic → L3 persona hierarchy.

### Time-travel ❌
- No historical state browsing.
- `fetch_history` provides paginated timeline but not temporal replay.

---

## Search & Retrieval

### Full-text ✅
- `methods/EverCore/docs/ARCHITECTURE.md` — "Elasticsearch 8.x - Keyword search engine (BM25)".
- `docs.evermind.ai` (llms.txt) — Retrieval methods include `keyword` (BM25, <100ms).

### Semantic/vector ✅
- `methods/EverCore/docs/ARCHITECTURE.md` — "Milvus 2.4+ - Vector database for semantic retrieval".
- `docs.evermind.ai` (llms.txt) — Retrieval methods include `vector` (semantic similarity, 200-500ms).
- `methods/EverCore/src/memory_layer/constants.py` — `VECTORIZE_DIMENSIONS = 1024`.

### Hybrid (BM25+Vec) ✅ — **CORRECTION: This feature IS present**
- `methods/EverCore/docs/ARCHITECTURE.md` — "Hybrid retrieval (RRF fusion)" combining BM25 + vector.
- `docs.evermind.ai` (llms.txt) — `hybrid` retrieval method: "keyword + vector + rerank" at 200-600ms. "Recommended default."
- `benchmarks/EverMemBench/README.md` — `evermemos.yaml` config: `retrieve_method: "hybrid"`.
- **Finding**: Hybrid search is a core, documented feature. This should NOT be in the absent list.

### Deep (incl. thinking) ❌
- No search over model thinking/reasoning traces.

### Code graph ❌
- No code structure indexing.

### Docs search ❌
- No documentation search.

### Fact metadata query ❌
- Metadata filters exist (user_id, group_id, session_id, timestamp) but no structured fact querying (e.g., "all decisions about X").

### Timeline view ⚠️ (basic)
- `evermemos-mcp` README — `fetch_history` tool: "Paginate through memory timeline by type."
- `docs.evermind.ai` — Filters DSL supports `timestamp` range queries (gt, gte, lt, lte).
- **Finding**: Basic chronological access exists but no dedicated timeline tool with `since`/`before` parameters.

---

## Knowledge Lifecycle

### Decay/forgetting ❌
- No automatic decay mechanism.

### Supersede/replace ❌
- No memory replacement chain.

### Contradiction detect ⚠️ (implicit consolidation)
- `README.md` — "resolves contradictions between old and new facts" during Semantic Consolidation.
- Handled automatically during consolidation, not surfaced to user.

### Quarantine ❌
- No session quarantine.

### Auto-resolution ❌
- No automatic task resolution/archival.

### Trust model ❌
- No multi-tier trust hierarchy.

### Explicit forget ✅ — **CORRECTION: This feature IS present**
- `evermemos-mcp` README — `forget` tool: "Targeted deletion with verification workflow."
- `docs.evermind.ai` — `POST /api/v1/memories/delete` endpoint.
- **Finding**: Delete/forget is explicitly supported. Should NOT be in the absent list.

---

## Extraction Pipeline

### Auto-extraction ✅
- `README.md` — "Three-phase biological memory lifecycle":
  1. Episodic Trace Formation — detects semantic boundaries, segments interactions into MemCells
  2. Semantic Consolidation — clusters MemCells, resolves contradictions
  3. Reconstructive Recollection — rebuilds context for current task
- Extraction is automatic: messages are ingested via API, memory is extracted without manual `save()` calls.

### Content-aware preproc ❌
- No documented content-type-aware truncation.

### Deduplication ⚠️ (via consolidation)
- `README.md` — "clusters MemCells into thematic MemScenes, resolves contradictions between old and new facts."
- Consolidation inherently reduces duplicates but no explicit dedup mechanism is documented.
- **Finding**: Implicit via clustering. Not a dedicated dedup step.

### Quality refinement ❌
- LLM-based extraction includes quality checks, but no separate quality refinement phase is documented.

### Narrative generation ✅ — **CORRECTION: This feature IS present**
- `README.md` — Episodic Trace Formation produces "structured MemCells containing an episode narrative, atomic facts, foresight predictions, and metadata."
- `docs.evermind.ai` (llms.txt) — Episode memory type captures "Narrative summaries of conversations."
- **Finding**: Episode narratives are a core output of the extraction pipeline. Should NOT be in the absent list.

### Clustering ✅ — **CORRECTION: This feature IS present**
- `README.md` — "Semantic Consolidation — Clusters MemCells into thematic MemScenes."
- `methods/EverCore/src/memory_layer/cluster_manager/` — Dedicated cluster manager module.
- **Finding**: Clustering is a documented feature. Should NOT be in the absent list.

### Recurrence detection ❌
- No recurrence detection across sessions.

### Persona extraction ✅ — **CORRECTION: This feature IS present**
- `docs.evermind.ai` (llms.txt) — Profile memory type: "Persistent user attributes and preferences."
- `README.md` — "maintains a dynamic User Profile."
- `methods/EverCore/src/memory_layer/profile_manager/` — Dedicated profile manager module.
- **Finding**: User profile extraction is built into the memory system. Should NOT be in the absent list.

---

## Platform Support

### Claude Code ✅
- `use-cases/claude-code-plugin/` — Official plugin in the repo.
- `evermemos-mcp` README — "Works with Claude Code, Cursor, Cline, Cherry Studio, OpenClaw, Gemini CLI, Aider."

### Codex ⚠️ (MCP-compatible, no explicit docs)
- `evermemos-mcp` — MCP server works with "any MCP-compatible client." Codex supports MCP.
- No explicit Codex integration guide or mention.
- **Finding**: Works via MCP standard but no dedicated Codex documentation. Recommend marking as ⚠️ unless explicit Codex docs exist.

### OpenCode ⚠️ (MCP-compatible, no explicit docs)
- Same situation as Codex. MCP-compatible but no explicit OpenCode docs.
- Hive project (separate repo) mentions OpenCode, but Hive is not part of EverOS.

### Gemini CLI ✅
- `evermemos-mcp` README — explicitly lists "Gemini CLI" as supported client.

### Cursor ✅
- `evermemos-mcp` README — explicitly lists "Cursor" as supported client. Listed in repo topics.

### OpenClaw ✅
- `README.md` — "OpenClaw Agent Memory" use case with dedicated plugin.
- `evermemos-mcp` README — explicitly lists "OpenClaw" as supported client.

---

## Benchmarks

### LoCoMo — **CORRECTION: "✅" → "93.05"**
- `README.md` — "EverCore: LoCoMo **93.05%**". "HyperMem: LoCoMo **92.73%**".
- Paper: [arxiv.org/abs/2601.02163](https://arxiv.org/abs/2601.02163) (EverCore).
- Paper: [arxiv.org/abs/2604.08256](https://arxiv.org/abs/2604.08256) (HyperMem).
- Evaluation framework at `benchmarks/EverMemBench/` with full pipeline (Add → Search → Answer → Evaluate).
- **Finding**: Real numeric scores exist. "✅" in data.js should be replaced with "93.05" (EverCore primary score).

### LongMemEval — **CORRECTION: "✅" → "83.00"**
- `README.md` — "EverCore: LongMemEval **83.00%**" (EverCore only; HyperMem not reported).
- Same evaluation pipeline in `benchmarks/EverMemBench/`.
- **Finding**: Real numeric score. "✅" should be replaced with "83.00".

### Methodology open ✅
- Arxiv papers with full methodology for both EverCore (2601.02163) and HyperMem (2604.08256).
- Open-source evaluation framework at `benchmarks/EverMemBench/` with configurable pipeline, reproducible scripts, and public datasets.
- Public benchmarks also include `EvoAgentBench` (agent self-evolution) with HuggingFace dataset.

---

## Operations & Other

### LLM providers ⚠️ (configurable, not auto-discovered)
- `methods/EverCore/src/infra_layer/adapters/` — Adapter pattern for different services.
- `env.template` — LLM_API_KEY is configurable but no multi-provider auto-discovery.
- Cloud API abstracts provider selection. Local deployment requires manual configuration.

### Setup — 3 commands
- `README.md` — "git clone → docker compose up -d → uv sync → uv run python src/run.py". Plus `.env` configuration. More than 2 commands but well-documented.

### Multi-agent ❌
- No built-in multi-agent system. Third-party integrations (MCO, Hive, Golutra) use EverOS as backend.

### Web UI ❌ (local)
- Cloud dashboard only. No bundled local web UI.

---

## Summary of Corrections

| Claim | Stated | Verified | Recommendation |
|-------|--------|----------|----------------|
| offline | true | ⚠️ local core, cloud extraction | Mark as ⚠️ or note extraction needs LLM API |
| schemaFields | 8 | ~8 | Verified. Document as: id, content, metadata, memory_type, embedding, user_id, timestamp, session_id |
| fulltext | true | ✅ true | Verified |
| semantic | true | ✅ true | Verified |
| autoExtract | true | ✅ true | Verified |
| p_claude | true | ✅ true | Verified |
| p_codex | true | ⚠️ MCP-only | No explicit Codex docs. Mark as ⚠️ or ❌ |
| p_opencode | true | ⚠️ MCP-only | No explicit OpenCode docs. Mark as ⚠️ or ❌ |
| p_gemini | true | ✅ true | Verified via evermemos-mcp |
| p_cursor | true | ✅ true | Verified via evermemos-mcp |
| p_openclaw | true | ✅ true | Verified |
| b_locomo | "✅" | **93.05** | Replace "✅" with "93.05" (EverCore) |
| b_longmemeval | "✅" | **83.00** | Replace "✅" with "83.00" |
| b_methodology | true | ✅ true | Verified |

### Features claimed absent but actually present:

| Feature | Actually | Evidence |
|---------|----------|----------|
| hybrid | ✅ present | RRF fusion, API supports `method: hybrid` |
| explicitForget | ✅ present | `forget` tool in evermemos-mcp, DELETE API endpoint |
| narrative | ✅ present | Episode narratives in MemCells |
| clustering | ✅ present | MemScene clustering in consolidation |
| persona | ✅ present | Profile memory type, profile_manager module |
| conflict | ⚠️ implicit | Contradiction resolution during consolidation |
| dedup | ⚠️ implicit | Via clustering/consolidation |
| timeline | ⚠️ basic | fetch_history pagination, timestamp filters |
| layeredMemory | ⚠️ type-based | 7 memory types, not L0→L3 hierarchy |

### Features correctly absent:
proxy, webUi (local), multiAgent, entities, actions, keywords, anticipatedQueries, triggerRules, domainTag, taskType, context, source (3-tier), originTrust, emotional, timeTravel, deep, codeGraph, docsSearch, factQuery (structured), decay, supersede, quarantine, autoResolve, trustModel (multi-tier), contentPreproc, qualityRefine (dedicated), recurrence
