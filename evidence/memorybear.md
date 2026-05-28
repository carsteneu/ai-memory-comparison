# MemoryBear — Evidence

> Every ✅ claim backed by public README, source code (schemas), or documentation.
> Audit date: 2026-05-28. Source: GitHub `SuanmoSuanyangTechnology/MemoryBear` main branch.
> Stars: 4,200. 3,640 commits. 17 releases (latest: v0.3.4, May 22, 2026).

## Meta

- **Description:** Next-generation AI memory system by RedBear AI. Inspired by biological brain mechanisms: perception → extraction → association → forgetting. Emulates hippocampus encoding, neocortex consolidation, and synaptic pruning.
- **Deployment:** Self-hosted Docker Compose + manual start. Requires PostgreSQL, Neo4j, Redis, Elasticsearch.
- **Storage:** PostgreSQL 13+ (primary), Neo4j 4.4+ (knowledge graph), Elasticsearch 8.x (hybrid search), Redis 6.0+ (cache/queue).
- **Integration:** MCP via fastmcp + langchain-mcp-adapters. REST API (FastAPI). JWT + API Key auth.
- **Setup:** Clone → start 4 Docker services → configure .env → alembic upgrade → uv run → npm run dev.
- **License:** Apache 2.0
- **Created:** Earliest release data not captured, but 17 releases total as of May 2026.
- **Docs URL:** https://memorybear.ai/ (SPA, requires JS), https://github.com/SuanmoSuanyangTechnology/MemoryBear

---

## Architecture

### Web/TUI ✅
- `README.md` — Frontend: React 18 + TypeScript + Vite + Ant Design 5.x. Served at `http://localhost:3000`.
- `README.md` — Knowledge graph visualization with AntV X6 + ECharts + D3.js.
- `README.md` — "Interactive graph visualization with 'machine-generated + human-optimized' collaborative management."

### Offline ✅
- `README.md` — All services run locally: PostgreSQL, Neo4j, Redis, Elasticsearch. Self-hosted. No cloud dependency.
- `README.md` — Docker Compose setup for local development.

### Privacy ✅
- `api/app/schemas/memory_storage_schema.py` — `MemoryVerifySchema`: `has_privacy: bool`, `privacy_types: List[str]`, `summary: str`. Detects privacy information in memories.
- `README.md` — Self-hosted, data never leaves user's infrastructure.

### Export ✅
- `api/app/schemas/ontology_schemas.py` — `ExportBySceneRequest`/`ExportBySceneResponse`: OWL export in RDF/XML or Turtle format.
- `api/app/schemas/knowledgeshare_schema.py` / `release_share_schema.py` — Knowledge base sharing and export schemas.

### Multi-Agent ✅
- `api/app/schemas/multi_agent_schema.py` — Full multi-agent orchestration: `MasterAgentConfig`, `SubAgentConfig` (agent_id, name, role, priority, capabilities), `RoutingRule` (condition, target_agent_id), `ExecutionConfig` (routing_mode, sub_agent_execution_mode=parallel|sequential, result_merge_mode=smart|master).
- `api/app/schemas/multi_agent_schema.py` — `HandoffHistoryItem`, `HandoffChatResponse`, `HandoffStateResponse` — agent handoff system with history tracking.
- `api/app/schemas/multi_agent_schema.py` — `aggregation_strategy`: merge, vote, priority, custom.

### LLM Flexibility ✅
- `README.md` — Tech stack: LangChain / OpenAI / DashScope / AWS Bedrock.
- `api/app/schemas/memory_storage_schema.py` — ConfigParamsCreate has: `llm_id`, `embedding_id`, `rerank_id`, `reflection_model_id`, `emotion_model_id`, `audio_id`, `vision_id`, `video_id`. Each model can be independently configured.
- `README.md` — MCP integration: fastmcp + langchain-mcp-adapters.

---

## Data Model

### Entities ✅
- `api/app/schemas/memory_storage_schema.py` — `BaseDataSchema`: `entity1_name`, `entity2_name`, `entity2: Optional[Dict[str, Any]]` fields.
- `api/app/schemas/ontology_schemas.py` — Full ontology class system: `SceneCreateRequest`, `ClassCreateRequest`, `ClassResponse`. Entity types organized by domain scene.

### Actions ❌
- No dedicated "actions" field found in schemas. README mentions "subject-action-object logic" for statement extraction but no stored action type.

### Keywords ✅
- `api/app/schemas/emotion_schema.py` — `EmotionWordcloudRequest`: extracts keywords from emotional content.
- `api/app/schemas/memory_api_schema.py` — `EmotionConfigUpdateRequest`: `emotion_extract_keywords: bool`.
- `api/app/schemas/multi_agent_schema.py` — Routing via `enable_rule_fast_path`: "high confidence keywords directly return."

### Context ✅
- `api/app/schemas/memory_api_schema.py` — `ConfigUpdateExtractedRequest`: `include_dialogue_context: bool`, `max_context: int` (dialogue context length).
- `api/app/schemas/memory_storage_schema.py` — `BaseDataSchema`: `description`, `statement` fields capture surrounding context.

### Source ✅
- `api/app/schemas/knowledge_schema.py` — `created_by: uuid.UUID` on knowledge bases.
- `api/app/schemas/memory_api_schema.py` — `end_user_id` tracks source user for all memory operations.
- `api/app/schemas/retrieval_info_schema.py` — `Host` schema with host tracking.

### Emotional ✅
- `api/app/schemas/emotion_schema.py` — Full emotion analysis: `EmotionTagsRequest` with types joy/sadness/anger/fear/surprise/neutral, `EmotionWordcloudRequest`, `EmotionHealthRequest` (7d/30d/90d ranges), `EmotionSuggestionsRequest`, `EmotionGenerateSuggestionsRequest`.
- `api/app/schemas/memory_api_schema.py` — `EmotionConfigUpdateRequest`: `emotion_enabled`, `emotion_min_intensity` (0.0-1.0), `emotion_enable_subject`.

### Conflict ✅
- `api/app/schemas/memory_storage_schema.py` — `ConflictResultSchema`: `conflict: bool`, `data: List[BaseDataSchema]`. `ConflictSchema` with conflict_memory tracking, `ReflexionSchema` with reason+solution, `ResolvedSchema` with original_memory_id + resolved_memory + change records.
- `README.md` — Self-Reflection Engine: "Consistency checks: Detects logical conflicts across related knowledge."

### Layered Memory ✅
- `api/app/schemas/memory_explicit_schema.py` — `ExplicitMemoryDetailsRequest`: distinguishes "情景记忆或语义记忆" (episodic or semantic memory).
- `api/app/schemas/implicit_memory_schema.py` — Full implicit memory: preferences, personality dimensions (creativity/aesthetic/technology/literature), interest areas (tech/lifestyle/music/art), behavior habits with frequency patterns.
- `api/app/schemas/memory_perceptual_schema.py` — Perceptual memory schema exists in schemas directory.
- `api/app/schemas/memory_episodic_schema.py` — Episodic memory schema exists.

### Time Travel ✅
- `README.md` — Memory Extraction Engine: "Temporal anchoring: Automatically extracts and tags timestamps, enabling time-based knowledge tracing."
- `api/app/schemas/implicit_memory_schema.py` — `TimeRange`, `DateRange` for temporal analysis. Historical trends tracking. `BehaviorHabitResponse.first_observed`/`last_observed`.

### Schema Fields — 12+
- `api/app/schemas/memory_storage_schema.py` — `BaseDataSchema` fields: id, statement, created_at, expired_at, description, entity1_name, entity2_name, statement_id, predicate, relationship_statement_id, relationship, entity2 = **12 fields**.
- Plus implicit memory schemas add: tag_name, confidence_score, supporting_evidence, context_details, dimension_name, percentage, evidence, reasoning, habit_description, frequency_pattern, time_context, etc.

---

## Search & Retrieval

### Full-text ✅
- `README.md` — "Keyword search powered by Elasticsearch for millisecond-level exact matching of structured information."
- `README.md` — Tech stack lists Elasticsearch 8.x as search engine.

### Semantic ✅
- `README.md` — "Semantic vector search via BERT embeddings, recognizing synonyms, near-synonyms, and implicit intent."
- `README.md` — Elasticsearch handles both keyword and semantic vector search.

### Hybrid ✅
- `README.md` — "Keyword retrieval + semantic vector retrieval dual-engine fusion." "Semantic retrieval expands the candidate space; keyword retrieval then performs precise filtering." Retrieval accuracy: 92%, +35% over single-mode.
- `README.md` — Tech stack: "Elasticsearch 8.x (keyword + semantic vector hybrid)."

### Deep Retrieval ✅
- `api/app/schemas/memory_api_schema.py` — `ConfigUpdateExtractedRequest`: `deep_retrieval: Optional[bool]` with description "Deep retrieval toggle".
- `api/app/schemas/memory_storage_schema.py` — `ConfigParams`: `deep_retrieval: bool = True` with description "深度检索开关".

### Code Graph ❌
- No evidence. MemoryBear is an AI memory system, not a codebase analysis tool.

### Docs Search ❌
- No evidence of documentation indexing/search.

### Fact Query ✅
- `api/app/schemas/memory_api_schema.py` — `MemoryReadRequest.search_switch`: "0=verify, 1=direct, 2=context". Three query modes for fact verification.
- `README.md` — "Structured triples: Automatically extracts entity relationships as atomic units for graph storage." Fact-based querying via Neo4j graph.

### Timeline ✅
- `README.md` — "Temporal anchoring: Automatically extracts and tags timestamps, enabling time-based knowledge tracing."
- `api/app/schemas/implicit_memory_schema.py` — `TimeRange`, `DateRange` filtering for analysis.

### Search Modes — 3
- `api/app/schemas/memory_api_schema.py` — `search_switch` enum: 0=verify, 1=direct, 2=context = **3 modes**.
- Plus hybrid search combines vector + keyword as a fourth mode (internal).

---

## Knowledge Lifecycle

### Decay ✅
- `README.md` — Memory Forgetting Engine: "dual-dimension model of memory strength and time decay." "Each knowledge item is assigned an initial memory strength, updated dynamically by usage frequency and association activity."
- `api/app/schemas/memory_storage_schema.py` — `ForgettingConfigUpdateRequest`: `decay_constant`, `lambda_time`, `lambda_mem`, `offset`, `forgetting_threshold`, `min_days_since_access`, `forgetting_interval_hours`.
- `api/app/schemas/memory_storage_schema.py` — `ForgettingCurveRequest`/`ForgettingCurveResponse`: Ebbinghaus curve simulation with activation values over days.
- `README.md` — Three-stage lifecycle: "dormancy → decay → clearance."

### Supersede ✅
- `api/app/schemas/memory_storage_schema.py` — `ResolvedSchema`: `original_memory_id` + `resolved_memory` + `change: List[ChangeRecordSchema]`. Old memories resolved into updated versions with change tracking.
- `api/app/schemas/memory_storage_schema.py` — `ChangeRecordSchema`: tracks "field: [{original_memory_id}, {field_name: [old_value, new_value]}]".

### Contradiction ✅
- `README.md` — Self-Reflection Engine: "Consistency checks: Detects logical conflicts across related knowledge, flags suspicious records for human review."
- `api/app/schemas/memory_storage_schema.py` — `ConflictResultSchema`: `conflict: bool`. `ConflictSchema`: `conflict_memory`. `ReflexionSchema`: `reason` + `solution`. `SingleReflexionResultSchema`: groups conflict + reflexion + resolved.

### Quarantine ❌
- No explicit quarantine/isolation feature detected in schemas or README.

### Auto-Resolve ✅
- `api/app/schemas/memory_storage_schema.py` — `ResolvedSchema` + `ChangeRecordSchema`: AI auto-generates resolved versions with detailed change records.
- `README.md` — Self-Reflection Engine: automated daily reflection with "Value assessment: reinforces high-value knowledge, accelerates decay of low-value knowledge."
- `api/app/schemas/memory_api_schema.py` — `ReflectionConfigUpdateRequest`: `reflection_enabled`, `reflection_period_in_hours`, `baseline: TIME/FACT/TIME-FACT`.

### Trust Model ✅
- `api/app/schemas/memory_storage_schema.py` — `QualityAssessmentSchema`: `score: int (0-100)`, `summary: str`.
- `api/app/schemas/memory_api_schema.py` — `ReflectionConfigUpdateRequest`: `memory_verify: bool`, `quality_assessment: bool`. Both LLM-powered.
- `api/app/schemas/implicit_memory_schema.py` — `confidence_score`, `confidence_level` on preferences, behaviors, personality.

### Explicit Forget ✅
- `api/app/schemas/memory_storage_schema.py` — `ForgettingTriggerRequest`: manual trigger with `end_user_id`, `max_merge_batch_size`, `min_days_since_access`.
- `README.md` — Forgetting engine: "Redundant knowledge maintained below 8%, reducing waste by over 60%."
- `api/app/schemas/memory_storage_schema.py` — `ForgettingConfigResponse`/`ForgettingConfigUpdateRequest`: full configurable forgetting parameters.

---

## Extraction Pipeline

### Auto-Extract ✅
- `README.md` — Memory Extraction Engine: "Performs semantic-level parsing of unstructured conversations and documents." Extracts: core declarative info, structured triples (entity relationships), temporal anchoring, intelligent summarization (50-500 words).
- `README.md` — "Generates concise summaries of 10-page documents in under 3 seconds."
- `api/app/schemas/ontology_schemas.py` — `ExtractionRequest`: LLM-powered ontology extraction from scenario text.

### Content Preprocessing ✅
- `api/app/schemas/memory_storage_schema.py` — `ChunkerStrategy` enum: RecursiveChunker, TokenChunker, SemanticChunker, NeuralChunker, HybridChunker, LLMChunker, SentenceChunker, LateChunker = **8 chunking strategies**.
- `api/app/schemas/memory_api_schema.py` — `ConfigUpdateExtractedRequest`: `statement_granularity` (1-3), `include_dialogue_context`, `max_context`.
- `api/app/schemas/ontology_schemas.py` — Ontology scene-based content preprocessing.

### Dedup ✅
- `api/app/schemas/memory_api_schema.py` — `ConfigUpdateExtractedRequest`: `enable_llm_dedup_blockwise: Optional[bool]` — LLM-based blockwise deduplication.
- `api/app/schemas/memory_storage_schema.py` — `ConfigParams`: `enable_llm_dedup_blockwise: bool = True`.

### Quality Refinement ✅
- `api/app/schemas/memory_api_schema.py` — `ConfigUpdateExtractedRequest`: `enable_llm_disambiguation: Optional[bool]` — LLM-based disambiguation.
- `api/app/schemas/memory_api_schema.py` — `ConfigUpdateExtractedRequest`: `pruning_enabled`, `pruning_scene`, `pruning_threshold` (0-0.9) — semantic pruning for quality.
- `api/app/schemas/memory_storage_schema.py` — `QualityAssessmentSchema`: LLM-graded quality score.

### Narrative ✅
- `README.md` — "Intelligent summarization: Customizable length (50-500 words) and focus."
- `api/app/schemas/implicit_memory_schema.py` — `MemorySummary`, `UserMemorySummary`, `SummaryAnalysisResult` — structured memory summaries.

### Clustering ✅
- `api/app/schemas/memory_storage_schema.py` — `ForgettingTriggerRequest`: `max_merge_batch_size` — node fusion during forgetting.
- `api/app/schemas/memory_storage_schema.py` — `ForgettingReportResponse`: `merged_count`, `nodes_before`, `nodes_after` — clustering/merging metrics.
- `api/app/schemas/memory_storage_schema.py` — `ConfigParams`: `enable_llm_dedup_blockwise` — LLM-aided dedup clustering.

### Recurrence ❌
- No explicit recurrence pattern detection found. Forgetting engine tracks access frequency but no recurrence detection.

### Persona ✅
- `api/app/schemas/implicit_memory_schema.py` — `UserProfileResponse`: comprehensive user profile with preference_tags, dimension_portrait (creativity/aesthetic/technology/literature), interest_area_distribution (tech/lifestyle/music/art), behavior_habits (daily/weekly/monthly/seasonal/occasional/event_triggered).
- `api/app/schemas/implicit_memory_schema.py` — `CompleteProfileResponse`: full cached profile with preferences + portrait + interest + habits.
- `api/app/schemas/implicit_memory_schema.py` — `DimensionPortraitResponse`: 4-dimension personality with evidence + reasoning.

---

## Platform Support

All platform checks: MemoryBear is a general-purpose AI memory system exposed via REST API + MCP. No platform-specific plugins found in the repository.

### p_claude ❌ — No Claude Code plugin found.
### p_codex ❌ — No Codex plugin found.
### p_opencode ❌ — No OpenCode plugin found.
### p_gemini ❌ — No Gemini plugin found.
### p_copilot ❌ — No Copilot plugin found.
### p_cursor ❌ — No Cursor plugin found.
### p_windsurf ❌ — No Windsurf plugin found.
### p_openclaw ❌ — No OpenClaw plugin found.
### p_hermes ❌ — No Hermes plugin found.
### p_pi ❌ — No Pi plugin found.
### p_antigravity ❌ — No Antigravity plugin found.

Note: MemoryBear exposes MCP (Model Context Protocol) via fastmcp + langchain-mcp-adapters (README Tech Stack). Any MCP-compatible client could theoretically integrate, but no pre-built platform-specific plugins exist in the repo.

---

## Benchmarks

### b_locomo ✅
- `README.md` — "MemoryBear consistently outperforms competing systems including Mem0, Zep, and LangMem across all four task categories."
- `README.md` — Benchmark graphs show F1, BLEU-1, LLM-as-Judge scores. Vector version: 72.90 ± 0.19% overall accuracy. Graph version: 75.00 ± 0.20%.
- Repository includes `redbear-mem-benchmark` submodule.

### b_longmemeval ❌ — Not mentioned.
### b_personamem ❌ — Not mentioned.
### b_token ❌ — Not mentioned.
### b_methodology ✅
- `README.md` — Three papers: core technical report (memorybear.ai/pdf/memoryBear), multimodal affective intelligence (arxiv 2603.22306), A-MBER benchmark (arxiv 2604.07017).
- `README.md` — Evaluation methodology: F1, BLEU-1, LLM-as-Judge. Four task categories. Vector vs graph comparison. Latency benchmarks (p50, p95).
