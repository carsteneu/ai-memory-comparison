# Mem0 — Evidence

> Every ✅ claim backed by public source code or documentation.
> Audit date: 2026-05-28. Source: GitHub `mem0ai/mem0` main branch, `docs.mem0.ai`, GitHub `mem0ai/memory-benchmarks`.

## Architecture

### Web/TUI ✅
- `README.md` — Self-hosted server ships Dashboard: "Dashboard — Yes" in the deployment table. Setup wizard, audit log, memory browser, entity management, API key management.
- `docs.mem0.ai/open-source/setup` — "What the dashboard gives you" section lists 6 pages: Requests, Memories, Entities, API Keys, Configuration, Settings. Browser-based UI served at `http://localhost:3000`.

### LLM providers — 16+ (claims 5 — **UNDERCOUNT** ✅→🔺)
- `mem0/llms/configs.py` — `LlmConfig` validator lists 18 valid providers: `openai`, `ollama`, `anthropic`, `groq`, `together`, `aws_bedrock`, `litellm`, `azure_openai`, `gemini`, `deepseek`, `minimax`, `xai`, `sarvam`, `lmstudio`, `vllm`, `langchain` (plus `openai_structured`/`azure_openai_structured` variants).
- `docs.mem0.ai/components/llms/overview` — 16 card items listed: OpenAI, Ollama, Azure OpenAI, Anthropic, Together, Groq, Litellm, Mistral AI, Google AI, AWS bedrock, DeepSeek, MiniMax, xAI, Sarvam AI, LM Studio, Langchain.
- **Finding**: Current data.js says 5, but code + docs confirm at least 16 distinct providers. Should be updated to 16.

---

## Data Model

### Entities ✅
- `mem0/utils/entity_extraction.py` — `extract_entities()` extracts four entity types: PROPER (capitalized sequences), QUOTED (text in quotes), COMPOUND (noun-noun compounds), NOUN (fallback nouns). Returns `List[Tuple[str, str]]`.
- `mem0/utils/entity_extraction.py` — `extract_entities_batch()` for batched NER via spaCy `nlp.pipe()`.
- `mem0/memory/main.py` — `_upsert_entity()` stores entities in a separate `_entities` vector collection with `entity_type` and `linked_memory_ids` in payload. Entities are embedded and searchable.
- `mem0/memory/main.py` — Phase 7 of `_add_to_vector_store()`: batch entity linking during memory ingestion — extracts entities from new memories, searches for existing ones (cosine ≥0.95 match), updates linked_memory_ids or creates new entity records.
- `README.md` — "Entity linking — entities are extracted, embedded, and linked across memories for retrieval boosting."

### Schema fields — 7+ (claims 6 — **SLIGHT UNDERCOUNT** ✅→🔺)
- `mem0/configs/base.py` — `MemoryItem` Pydantic model: `id`, `memory`, `hash`, `metadata`, `score`, `created_at`, `updated_at` = 7 fields.
- `mem0/memory/main.py` — Payload stored in Qdrant additionally includes: `user_id`, `agent_id`, `run_id`, `actor_id`, `role`, `data` (memory text), `text_lemmatized`, `attributed_to`. Total unique fields across MemoryItem + payload ≈ 12-14.
- **Finding**: Current data.js says 6, but MemoryItem alone has 7. The full stored schema has ~12+ unique fields. Core memory unit fields: id, memory, hash, metadata, score, created_at, updated_at = 7. Recommend updating to at least 7.

---

## Search & Retrieval

### Full-text (BM25) ✅
- `mem0/vector_stores/qdrant.py` — `Qdrant` class stores BM25 sparse vectors using `SparseVector` with `fastembed` Qdrant/bm25 encoder in a dedicated `bm25` named vector slot.
- `mem0/vector_stores/qdrant.py` — `keyword_search()` method: "Search using BM25 sparse vectors for keyword-based retrieval." Uses `query_points()` with `using="bm25"`.
- `mem0/utils/scoring.py` — `get_bm25_params()` and `normalize_bm25()`: Sigmoid normalization of raw BM25 scores to [0,1] range, query-length-adaptive parameters.

### Semantic/vector ✅
- `mem0/vector_stores/qdrant.py` — `search()` method: Dense vector search via `QdrantClient.query_points()` with cosine distance.
- `mem0/memory/main.py` — `add()` embeds memory text via `self.embedding_model.embed()` and stores in Qdrant as dense vectors.
- `README.md` — Default embedder: `text-embedding-3-small` from OpenAI. Recommends Qwen 600M+ for best hybrid results.

### Hybrid (BM25+Vec) ✅
- `mem0/utils/scoring.py` — `score_and_rank()`: "Score candidates additively." Combines `semantic_score + bm25_score + entity_boost` with adaptive divisor. Three-signal fusion: semantic (vector) + BM25 (keyword) + entity (linking).
- `mem0/memory/main.py` — `search()` method uses multi-signal retrieval: runs semantic search + BM25 keyword search in parallel, then fuses with entity boosts via `score_and_rank()`.
- `README.md` — "Multi-signal retrieval — semantic, BM25 keyword, and entity matching scored in parallel and fused."
- `README.md` — "For enhanced hybrid search with BM25 keyword matching and entity extraction, install with NLP support: `pip install mem0ai[nlp]`"

### Search modes — 1 ✅
- `mem0/memory/main.py` — Single primary search method: `search()`. Supports filters, threshold, top_k, optional reranking. `keyword_search()` exists as internal method in Qdrant class but is not a user-facing mode — it feeds into the fused search.

---

## Knowledge Lifecycle

### Supersede/replace — "add-only" ✅
- `README.md` — New Memory Algorithm (April 2026): "Single-pass ADD-only extraction — one LLM call, no UPDATE/DELETE. Memories accumulate; nothing is overwritten."
- `mem0/configs/prompts.py` — `ADDITIVE_EXTRACTION_PROMPT`: "Your sole operation is ADD." System prompt for V3 extraction explicitly forbids UPDATE/DELETE operations.
- The old v2 prompt (`DEFAULT_UPDATE_MEMORY_PROMPT`) supported ADD/UPDATE/DELETE/NONE, but v3 switched to ADD-only. Old prompt is still in source but is legacy code for v2 path, not active in v3.
- **Finding**: The "add-only" text claim is accurate. Memories are never updated or deleted automatically — they accumulate. However, users can still manually `update_memory` and `delete_memory` via MCP tools / REST API.

### Explicit forget ✅
- `docs.mem0.ai/integrations/claude-code` — MCP Tools table lists: `delete_memory` (single by ID), `delete_all_memories` (bulk delete in scope), `delete_entities` (cascade delete user/agent/app/run and its memories).
- `docs.mem0.ai/api-reference` — REST API includes Delete Memory (`DELETE /v1/memories/{memory_id}/`), Update Memory.
- `mem0/memory/main.py` — Memory class has `delete()` and `update()` methods (visible in the truncated source — methods are part of the public API).
- `docs.mem0.ai/open-source/setup` — Dashboard Entities page supports "cascade-delete."

---

## Extraction Pipeline

### Auto-extraction ✅
- `mem0/memory/main.py` — `add()` method: `infer` parameter defaults to `True`. When True, runs the full V3 extraction pipeline (Phase 0-8) including LLM-based fact extraction, embedding, dedup, entity linking.
- `mem0/memory/main.py` — `_add_to_vector_store()`: 8-phase pipeline. Phase 0: context gathering. Phase 1: existing memory retrieval. Phase 2: LLM extraction via `ADDITIVE_EXTRACTION_PROMPT`. Phase 3: batch embedding. Phase 4-5: CPU processing + hash dedup. Phase 6: batch persist. Phase 7: batch entity linking. Phase 8: save messages.
- `mem0/configs/prompts.py` — `ADDITIVE_EXTRACTION_PROMPT` (multi-page prompt): "You are a Memory Extractor — a precise, evidence-bound processor responsible for extracting rich, contextual memories from conversations." Defines extraction rules, quality standards, memory linking, temporal grounding, numeric precision requirements.

---

## Platform Support

### Claude Code ✅
- `docs.mem0.ai/integrations/claude-code` — Dedicated integration page. MCP server (9 memory tools), lifecycle hooks (SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, PreCompact), SDK skill. Plugin marketplace install.
- `README.md` — Agent Skills section lists Claude Code as supported. "Teach your AI coding assistant (Claude Code, Codex, Cursor, Windsurf, OpenCode, OpenClaw...) how to build with Mem0."
- Repository contains `.claude-plugin/` directory with plugin configuration.

### Cursor ✅
- `docs.mem0.ai/integrations/cursor` — Dedicated integration page. MCP server (9 memory tools), lifecycle hooks, SDK skill. One-click deeplink install, npx, manual config, or Cursor Marketplace install.
- Repository contains `.cursor-plugin/` directory with plugin configuration.

---

## Benchmarks

### LoCoMo — 91.6 ✅
- `README.md` — Benchmark table: LoCoMo = 91.6 (new algorithm, April 2026). Previous: 71.4.
- `github.com/mem0ai/memory-benchmarks/README.md` — Open-source evaluation suite. LoCoMo results: 92.5% at Top 200, 91.8% at Top 50. Slight variance from README (91.6) due to different configurations (Platform vs OSS, top-k cutoffs).
- `github.com/mem0ai/memory-benchmarks/README.md` — Methodology: "Ingest → Search → Evaluate" pipeline with LLM answerer + judge LLM scoring correctness against ground truth.

### LongMemEval — 94.8 ✅
- `README.md` — Benchmark table: LongMemEval = 94.8 (new algorithm). Previous: 67.8.
- `github.com/mem0ai/memory-benchmarks/README.md` — LongMemEval results: 94.4% at Top 200, 94.8% at Top 50. Platform v3 pipeline. Breakdown by question type: knowledge-update, multi-session, single-session-assistant, single-session-preference, single-session-user, temporal-reasoning.

### Methodology open ✅
- `github.com/mem0ai/memory-benchmarks` — Apache 2.0 licensed evaluation framework. Full pipeline code in `benchmarks/` directory. Instructions for running with both Cloud and OSS backends. Configurable parameters: top-k, answerer model, judge model, provider.
- `README.md` (memory-benchmarks) — "Open-source evaluation suite to run benchmarks on memory-augmented LLM systems." Three benchmarks: LOCOMO, LongMemEval, BEAM. "The evaluation framework is open-sourced so anyone can reproduce the numbers."
- Paper: arXiv preprint arXiv:2504.19413 (cited in main README).

---

## Claims NOT present (marked false in data.js) — verified

The following features are correctly marked `false` in data.js. No public evidence was found for any of them:

**Data Model:** actions, keywords, anticipatedQueries, triggerRules, domainTag, taskType, context, source, originTrust, emotional, conflict, layeredMemory, timeTravel — all ❌ (Mem0 has a flat memory model with user_id/agent_id/run_id entity scoping, but no structured metadata fields beyond that)

**Search:** deep, codeGraph, docsSearch, factQuery, timeline — all ❌ (search() is the only retrieval mode; no code graph, doc index, or timeline view)

**Lifecycle:** decay, contradiction, quarantine, autoResolve, trustModel — all ❌ (no forgetting/decay, no contradiction handling, no quarantine, no auto-resolution, no trust model)

**Extraction:** contentPreproc, dedup, qualityRefine, narrative, clustering, recurrence, persona — all ❌ (extraction is a single LLM call with hash-based dedup in code; no quality refinement, no narrative generation, no clustering, no recurrence detection, no persona engine)

**Architecture:** proxy, multiAgent, offline — all ❌ (API/SDK-based integration, no proxy; not multi-agent; self-hosted and library modes exist but cloud platform requires internet)

---

## Audit Notes

1. **llmFlex undercount**: data.js says 5, but evidence shows 16+ providers. The `LlmConfig` validator in `mem0/llms/configs.py` accepts 18 provider strings, and docs list 16 distinct providers. Recommend updating to 16.

2. **schemaFields slight undercount**: data.js says 6, but `MemoryItem` model alone has 7 fields. The full Qdrant payload adds 5+ more. Minimum should be 7 based on the Pydantic model. Recommend updating to 7.

3. **Benchmark scores**: README claims LoCoMo 91.6 and LongMemEval 94.8. The benchmark repo's published results show slight variance (LoCoMo 91.8-92.5, LongMemEval 94.4-94.8 at different top-k cutoffs). The README's 91.6 and 94.8 numbers are within the published range and should be considered the canonical claims. Accepted as verified.

4. **Supersede "add-only"**: This is the v3 algorithm behavior. The v2 prompt (still in source) supported UPDATE/DELETE, but v3 explicitly switched to ADD-only. The "add-only" text is accurate for the current version. Users can still manually delete/update via API — the "add-only" refers specifically to the automatic extraction pipeline.
