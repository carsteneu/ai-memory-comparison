# Cognee — Evidence

> Every ✅ claim backed by public source code or documentation.
> Audit date: 2026-08-24 (re-audit; previous audit 2026-05-28). Source: GitHub `topoteretes/cognee` main branch, `topoteretes/cognee-integrations` main branch, `docs.cognee.ai`.

## Architecture

### Web/TUI ✅
- `README.md` — "To open the local UI, run: `cognee-cli -ui`". Launches full-stack UI at http://localhost:3000.
- `cognee/api/v1/visualize/` — `start_visualization_server()`: Python API to launch visualization on custom port.

### Offline ✅
- Ollama provider: local model inference, endpoint `http://localhost:11434/v1`; llama.cpp provider: full offline inference with GGUF models.
- Default databases are all local: SQLite (relational), LanceDB (vector), Ladybug (graph). No external services needed.
- `docs.cognee.ai/setup-configuration/llm-providers` — Ollama/LM Studio/llama.cpp sections documented as local providers.

### Multi-agent — ❌→✅ (2026-08 re-audit)
- `cognee-mcp/README.md` — "By default, each MCP client gets its own auto-named dataset (e.g. Cursor → `cursor_vscode_memory`, Claude Code → `claude_code_memory`) so different agents don't share memory unintentionally." Per-agent memory scoping with opt-in sharing.
- `README.md` — "Multi-tenant deployments" section: shared relational database holds "users, permissions, registry"; datasets are shared across users/agents with read/write/delete/share permissions.
- `cognee/modules/agent_memory/` — agent-scoped memory runtime resolving per-agent permissioned datasets (`get_all_user_permission_datasets`).
- `cognee/modules/provenance/models/ProvenanceEntry.py` — `agent_id` / `agent_type` recorded per entry, distinguishing which agent authored each memory.

### LLM providers — 11+ ✅
- `docs.cognee.ai/setup-configuration/llm-providers` — 11+ distinct providers: OpenAI, Azure OpenAI, Google Gemini, Anthropic, AWS Bedrock, Groq, Ollama, LM Studio, HuggingFace, llama.cpp, Custom (OpenAI-compatible: DeepSeek, OpenRouter, vLLM, etc.).

### Cache optimization — ❌→✅ (2026-08 re-audit)
- `README.md` (Claude Code plugin section) — "`PreCompact` preserves memory across context resets" — explicit context-collapse prevention hook.
- `README.md` — session memory is a "fast cache, syncs to graph in background"; improve "self-tune[s] its memory. Reads get faster and cheaper".

### Privacy — ❌→✅ (2026-08 re-audit)
- `.env.template` line 481 — `TELEMETRY_DISABLED=1` documented telemetry opt-out.
- Default stack is fully local (SQLite + LanceDB + Ladybug, local LLM via Ollama/llama.cpp) — local-only storage per criterion.

### Data export — ❌→✅ (2026-08 re-audit)
- `cognee/api/v1/export/export.py` — "SDK entry point: export a dataset's memory to a portable format." Formats: `cogx`, `json`, `graphml`, `cypher` (plus in-memory `pydantic` GraphSnapshot).
- `cognee/api/v1/activity/routers/get_activity_router.py` — `export_dataset_markdown(dataset_id)` REST endpoint: Markdown export.

### Integration — MCP+API+Hooks
- `cognee-mcp/` — MCP server (stdio/SSE/HTTP transports), Docker image `cognee/cognee-mcp`.
- `README.md` — REST API + Python SDK; Claude Code plugin uses lifecycle hooks (SessionStart, UserPromptSubmit, PostToolUse, Stop, PreCompact, SessionEnd).

---

## Data Model

### Entities ✅
- `cognee/shared/data_models.py` — `Node` (id, name, type, description), `Edge`, `KnowledgeGraph`; `DataPoint` base class; `Triplet` subject-predicate-object.
- cognify pipeline: `extract_graph_from_data` — LLM extracts entities/relationships.

### Actions — ❌→✅ (2026-08 re-audit)
- `README.md` (Claude Code plugin) — "The plugin captures prompts, **tool traces**, and assistant responses into session memory" — tool calls stored as structured session entries via the `PostToolUse` hook ("`PostToolUse` captures tool traces").

### Keywords/tags — ❌→✅ (2026-08 re-audit)
- `node_set` tagging system: `cognee/api/v1/improve/improve.py` — entries "tagged with `node_set=\"user_sessions_from_cache\"`" and "`session_learnings`"; integrations stamp source tags (e.g. `node_set=["slack"]`). `node_set` is a first-class add/search filter across the API.

### Source attribution — ❌→✅ (2026-08 re-audit)
- `cognee/modules/provenance/models/ProvenanceEntry.py` — "W3C PROV-O flavored provenance entry": `agent_id`, `agent_type` (user vs `software_agent`), `is_automated`, `role`, plus audit-grade source fields `source_document`, `source_location`, `source_quote`, `source_ref_key`. ≥3 distinct source levels (user input / software agent / automated extraction).
- `cognee/tasks/provenance/record_provenance.py` — provenance recorded during the pipeline.

### Conflict surfacing — ❌→✅ (2026-08 re-audit)
- `cognee/tasks/graph/detect_contradictions.py` — "asks an LLM which pairs directly contradict each other. Each contradiction is surfaced twice instead of silently coexisting: a warning is logged, and a `contradicts` edge (carrying both facts, the reason, and a confidence) is written so the conflict is queryable next to the data it concerns." Opt-in cognify task (`contradiction_detection` config flag).

### Layered memory — ❌→✅ (2026-08 re-audit)
- `README.md` — L0: session memory ("fast cache, syncs to graph in background") vs permanent knowledge graph.
- `cognee/api/v1/improve/improve.py` — L1: session distillation ("gated active-guidance entries are curated into entity-anchored lessons", tagged `session_learnings`); L2: "Global context index — builds retrieval-ready bucket and root summaries over the graph's text summaries."

### Time-travel — ❌→✅ (2026-08 re-audit)
- `cognee/tasks/graph/resolve_temporal_contradictions.py` — "Nothing is deleted: a superseded edge stays in the graph with its provenance, tagged (`superseded`, `superseded_by`, `supersession_reason`)" — superseded versions remain queryable.
- `cognee/modules/search/types/SearchType.py` — `TEMPORAL` search type; `cognee/modules/retrieval/temporal_retriever.py` — `extract_time_from_query()` derives `time_from`/`time_to` and filters results by time interval.

### Schema fields — ~14
- Node core (id, name, type, description) + `node_set` tags + dataset + permissions (read/write/delete/share) + `feedback_weight` + importance/truth weights + provenance source fields (source_document/location/quote) + temporal validity (`valid_from`/`valid_until`) + chunk metadata (chunk_index, chunk_size, cut_type) + agent/session attribution (`agent_id`, `agent_type`).

### Correctly absent ❌
anticipatedQueries, triggerRules, domainTag, taskType, context(why), originTrust, emotional — no public evidence.

---

## Search & Retrieval

### Full-text ✅
- `cognee/modules/search/types/SearchType.py` — `CHUNKS_LEXICAL`: lexical (keyword) search over chunks.

### Semantic/vector ✅
- `SearchType.CHUNKS` — vector similarity search over chunks; LanceDB (default), ChromaDB, PGVector backends.

### Hybrid (BM25+Vec) — ❌ (still; note new HYBRID_COMPLETION is not BM25+Vec fusion)
- `SearchType.HYBRID_COMPLETION` was added since the last audit, but `cognee/modules/retrieval/hybrid_retriever.py` is a "Completion retriever using chunk, entity, and optional global-context channels" — it fuses vector-chunk, graph-entity, and facts lanes, not BM25 + vector with RRF. Per the strict criterion (full-text + vector result fusion), this remains ❌.

### Code graph ✅
- `pyproject.toml` — `codegraph` extra (tree-sitter). `SearchType.CODE` and `SearchType.CODING_RULES` search types. `SummarizedCode`/`SummarizedFunction`/`SummarizedClass` models.

### Fact metadata query — ❌→✅ (2026-08 re-audit)
- `SearchType.CYPHER` — direct structured graph queries; `SearchType.NATURAL_LANGUAGE` — natural-language-to-Cypher structured querying over memory. Combined with `node_set`/dataset filters this supports structured metadata queries.

### Timeline — ❌→✅ (2026-08 re-audit)
- `cognee/modules/retrieval/temporal_retriever.py` — `extract_time_from_query()` → `time_from` / `time_to` interval filtering (temporal search with since/before semantics), exposed via `SearchType.TEMPORAL`.

### Search modes — 8 (was 5)
- `SearchType.py` now has 19 enum values. Distinct strategies: lexical (CHUNKS_LEXICAL), vector (CHUNKS), hybrid multi-lane (HYBRID_COMPLETION), graph completion (GRAPH_COMPLETION family), RAG (RAG_COMPLETION), temporal (TEMPORAL), code (CODE / CODING_RULES), structured query (CYPHER / NATURAL_LANGUAGE) — plus summaries, triplet, agentic, graph-report variants. Conservative distinct count: 8.

### Data sources — 4 (was 1)
- Searchable data types: document chunks (CHUNKS/CHUNKS_LEXICAL), graph facts/entities (GRAPH_* / TRIPLET), session memory (`recall(..., session_id=...)` — README), code (CODE/CODING_RULES).

### Correctly absent ❌
deep (thinking-trace search), docsSearch (no dedicated framework-docs index) — no public evidence.

---

## Knowledge Lifecycle

### Decay/forgetting — ❌→✅ (2026-08 re-audit; feedback-signal based)
- `cognee/api/v1/improve/improve.py` — "**Apply feedback weights** — session entries with feedback scores update `feedback_weight` on the graph nodes/edges that were used to produce those answers. Higher-rated answers boost their source nodes; **lower-rated answers decrease them**." Relevance is automatically adjusted from engagement signals; runs as part of session sync (plugin `SessionEnd` triggers sync — README). Not time-based decay; feedback/engagement-signal based per the criterion ("time, disuse, **or engagement signals**").

### Supersede/replace — ❌→✅ (2026-08 re-audit)
- `cognee/tasks/graph/resolve_temporal_contradictions.py` — resolves temporal conflicts and "tags the older ones as superseded. Nothing is deleted: a superseded edge stays in the graph with its provenance, tagged (`superseded`, `superseded_by`, `supersession_reason`)" — explicit replacement with a traceable chain (`tag_superseded_edges` in `cognee/modules/graph/utils`).

### Contradiction detect — ❌→✅ (2026-08 re-audit)
- `cognee/tasks/graph/detect_contradictions.py` — opt-in cognify task; compares newly ingested facts against already-stored facts in the same entity neighbourhood, LLM flags contradicting pairs, writes `contradicts` edges with reason + confidence. "Cross-ingestion contradictions work because entity node ids are deterministic."

### Explicit forget ✅
- `docs.cognee.ai/core-concepts/main-operations/forget` — 5 modes: single item, dataset, everything, memory-only (dataset), memory-only (single file). `await cognee.forget(dataset="main_dataset")`, `cognee-cli forget --all`.

### Correctly absent ❌
quarantine, autoResolve, trustModel — no public evidence.

---

## Extraction Pipeline

### Auto-extraction ✅
- `README.md` — `await cognee.remember("...")` — single call runs add + cognify + improve automatically. cognify pipeline: `classify_documents → extract_chunks_from_documents → extract_graph_from_data → summarize_text → add_data_points`.

### Deduplication — ❌→✅ (2026-08 re-audit)
- `cognee/modules/ingestion/identify.py` — content-hash identity: `content_hash_predicates(content_hash, user, dataset_id)`; ingestion resolves each item by content hash per user+dataset, so re-ingested identical content is not duplicated.
- `cognee/tasks/ingestion/resolve_dlt_sources.py` — "Rows are deduplicated by identity (table, pk_value, content_hash)" for structured sources.

### Quality refinement — ❌→✅ (2026-08 re-audit)
- `cognee/api/v1/improve/improve.py` — `improve()` is an explicit LLM-based post-extraction pass: feedback-weight application, session distillation into curated lessons, triplet-embedding enrichment, optional global context index and truth subspace.
- `cognee/tasks/graph/detect_contradictions.py` — contradiction checking with confidence scores (criterion examples: "confidence scoring, contradiction checking").

### Narrative generation — ❌→✅ (2026-08 re-audit)
- `cognee/api/v1/improve/improve.py` — "**Distill sessions** — each session's gated active-guidance entries are curated into entity-anchored lessons" (session summaries/handover lessons, tagged `session_learnings`).
- cognify `summarize_text` task + `SearchType.SUMMARIES`; global context index builds "bucket and root summaries".

### Persona extraction — ❌→✅ (2026-08 re-audit)
- `cognee/modules/user_preferences/` — "Per-user preference storage inside a dataset's graph. One `UserPreference` node per (user, dataset) plus weighted `prefers` edges"; `load_preference_text` / `load_preference_weights` feed personalized retrieval (`hybrid_retriever.py`: "Personal prefers weights ride into the chunk-lane ranking").

### Correctly absent ❌
contentPreproc, clustering, recurrence — no public evidence (global-context bucket summaries are hierarchical summarization, not claimed as clustering).

---

## Platform Support

### Claude Code ✅
- `README.md` — "Available as a plugin for your Claude Code"; `claude plugin marketplace add topoteretes/cognee-integrations && claude plugin install cognee-memory@cognee`. Full lifecycle hooks documented.

### Codex — ❌→✅ (2026-08 re-audit)
- `topoteretes/cognee-integrations` — `integrations/codex/` directory: dedicated Codex CLI integration.

### OpenCode — ❌→✅ (2026-08 re-audit)
- `topoteretes/cognee-integrations` — `integrations/opencode/` directory: dedicated OpenCode integration.

### Cursor — ❌→✅ (2026-08 re-audit)
- `cognee-mcp/README.md` — dedicated Cursor setup sections: "**Cursor (`~/.cursor/mcp.json`)**" (two config variants), and "Call them from any MCP client (Cursor, Claude Desktop, Cline, Roo and more)"; auto-named `cursor_vscode_memory` dataset.

### OpenClaw ✅
- `README.md` — "Available as a plugin for your OpenClaw — cognee-openclaw" (npm `@cognee/cognee-openclaw`); `integrations/openclaw/` + `integrations/openclaw-skills/` in cognee-integrations.

### Hermes — ❌→✅ (2026-08 re-audit)
- `topoteretes/cognee-integrations` — `integrations/hermes-agent/` directory: dedicated Hermes agent integration.

### Correctly absent ❌
Gemini CLI (google-adk integration exists but is not Gemini CLI), Copilot CLI, Windsurf, pi/omp, Antigravity — no dedicated documented integration.

---

## Benchmarks

- No published LoCoMo / LongMemEval / PersonaMem scores in README/docs — all `—`. (An `eval_framework/` with benchmark harness exists in-repo, but no published scores on the listed benchmarks with methodology; leaving unchanged.)

---

## Audit Notes (2026-08-24 re-audit)

Since the 2026-05-28 audit, cognee shipped several features that flip previous ❌ claims. Every flip above cites the exact public source. Notable non-flips kept honest:

1. **hybrid stays ❌** — the new `HYBRID_COMPLETION` mode fuses vector-chunk + graph-entity + facts lanes, not BM25+vector RRF.
2. **decay ✅ is feedback-signal based**, not time-based — matches the criterion's "engagement signals" clause; flagged for maintainer judgment.
3. **clustering stays ❌** — global-context bucket/root summaries are hierarchical summarization; not claiming it as clustering.
4. **stars**: 30,227 as of 2026-08-24.
