# memU — Evidence File

> Audit date: 2026-05-28  
> Repository: https://github.com/NevaMind-AI/memU  
> Stars: 13,730 | License: Apache 2.0 | Created: 2025-07-29 | Language: Python 99.8% + Rust 0.2%

---

## Repository Metadata

| Field | Value | Evidence |
|-------|-------|----------|
| **URL** | https://github.com/NevaMind-AI/memU | GitHub |
| **Stars** | 13,730 | GitHub API: `stargazers_count: 13730` |
| **License** | Apache 2.0 | LICENSE.txt: "Apache License Version 2.0, Copyright 2024 MemU Team" |
| **Created** | 2025-07-29 | GitHub API: `created_at: "2025-07-29T01:54:40Z"` |
| **Latest Release** | v1.5.1 (2026-03-23) | CHANGELOG.md |
| **Commits** | 288 | GitHub repo header |
| **Language** | Python 99.8%, Rust 0.2% | GitHub languages + pyproject.toml: maturin build system for `memu._core` |
| **PyPI** | memu-py v1.5.1 | pyproject.toml |
| **Docs** | https://memu.pro/docs | README.md |
| **Homepage** | https://memu.pro | GitHub API |

---

## Architecture

### webUi: ✅ TRUE
- Separate repo: `github.com/NevaMind-AI/memU-ui` — "Visual memory dashboard with live memory evolution monitoring"
- Evidence: README.md Ecosystem section: "memU-ui — Visual memory dashboard, Live memory evolution monitoring"

### offline: ✅ TRUE
- Self-hosted with three storage backends: `inmemory`, `sqlite`, `postgres`
- No cloud dependency required. Cloud (memu.so) is optional.
- Evidence: `src/memu/app/settings.py` — `MetadataStoreConfig.provider: "inmemory" | "postgres" | "sqlite"`; `src/memu/database/` contains inmemory/, sqlite/, postgres/

### privacy: ✅ TRUE
- Self-hosted = fully local. Scope model filters per user/agent.
- Evidence: `UserConfig.model` in settings.py; `_normalize_where()` in retrieve.py validates scope fields

### export: ❌ FALSE
- README conceptually mentions "file system as memory: export, backup, and transfer memory like files" but no export/migration feature found in code
- No export API, no backup/restore commands, no format conversion
- Evidence: Absence in code — no export function in CRUDMixin, no export CLI command, no export workflow step

### multiAgent: ✅ TRUE
- `where={"agent_id__in": ["1", "2"]}` filter shown in README retrieve usage
- `UserConfig` model supports `user_id`, with `agent_id` and `session_id` fields in comments (infrastructure ready)
- Evidence: README.md Proactive Filtering; `DefaultUserModel` in settings.py with commented agent_id/session_id fields; scope model propagation via `build_scoped_models()`

### llmFlex: ✅ TRUE
- Multiple LLM backends: `sdk` (OpenAI SDK), `httpx` (provider-adapted HTTP for OpenAI/Doubao/Grok/OpenRouter), `lazyllm_backend` (LazyLLM adapter)
- Providers: OpenAI, Grok (xAI), OpenRouter, Volcano, Nebius, custom via base_url
- Evidence: `LLMConfig` in settings.py; `docs/providers/grok.md`; `docs/integrations/grok.md`; `examples/test_nebius_provider.py`; README Custom LLM and OpenRouter sections

---

## Data Model

### entities: ⚠️ PARTIAL
- MemoryItem has `memory_type` field with 6 types: `profile`, `event`, `knowledge`, `behavior`, `skill`, `tool`
- Categories auto-assigned (10 defaults: personal_info, preferences, relationships, activities, goals, experiences, knowledge, opinions, habits, work_life)
- No explicit "entity" extraction field (no named entity disambiguation)
- Evidence: `MemoryType = Literal["profile", "event", "knowledge", "behavior", "skill", "tool"]` in models.py; `_default_memory_categories()` in settings.py

### actions: ❌ FALSE
- No action field or action extraction in schema
- Evidence: Full model scan in models.py — no action field

### keywords: ❌ FALSE
- No keyword field or keyword extraction
- Evidence: Full model scan in models.py — no keyword field

### anticipatedQueries: ❌ FALSE
- No anticipated query mechanism or field
- Evidence: Absence in codebase

### triggerRules: ❌ FALSE
- No trigger rules or disclosure logic
- Evidence: Absence in codebase

### domainTag: ❌ FALSE
- No domain tagging field or mechanism
- Evidence: Absence in codebase

### taskType: ⚠️ PARTIAL
- "tool" memory type tracks tool invocations with `ToolCallResult` model (tool_name, input, output, success, time_cost, token_cost, score)
- No explicit task/idea/blocked/stale type system
- Evidence: `ToolCallResult` class in models.py with tool invocation tracking

### context: ✅ TRUE
- `MemoryItem.resource_id` links back to the original `Resource`
- `Resource` tracks source via `url`, `local_path`, `caption`
- Evidence: models.py foreign key relation

### source: ✅ TRUE
- `Resource.url` tracks origin (file path or URL)
- `Resource.modality` indicates type (conversation|document|image|video|audio)
- Evidence: Resource model in models.py

### originTrust: ❌ FALSE
- No trust scoring or provenance origin tracking
- Evidence: Absence in codebase

### emotional: ❌ FALSE
- No emotional analysis, sentiment tracking, or affect fields
- Evidence: Absence in codebase

### conflict: ❌ FALSE
- No contradiction or conflict detection
- Evidence: Absence in codebase

### layeredMemory: ✅ TRUE
- Three explicit layers: **Resource** (raw source artifacts) → **MemoryItem** (extracted atomic memories) → **MemoryCategory** (grouped topic summaries)
- Documented in architecture.md as the core design: "Implements the 'memory as file system' concept with three persistent layers"
- Evidence: architecture.md; models.py with Resource/MemoryItem/MemoryCategory/CategoryItem; README Hierarchical Memory Architecture section

### timeTravel: ❌ FALSE
- `happened_at` field exists on MemoryItem for temporal anchoring
- No historical state reconstruction, no point-in-time queries
- Evidence: Absence of temporal navigation APIs

### schemaFields: ✅ TRUE (13 base fields across 4 models)

**Resource** (6 fields): id, url, modality, local_path, caption, embedding → plus user scope fields

**MemoryItem** (7 base fields): id, resource_id, memory_type, summary, embedding, happened_at, extra (dict with: content_hash, reinforcement_count, last_reinforced_at, ref_id, when_to_use, metadata, tool_calls) → plus user scope fields

**MemoryCategory** (5 fields): id, name, description, embedding, summary → plus user scope fields

**CategoryItem** (3 fields): id, item_id, category_id → plus user scope fields

**ToolCallResult** (8 fields): tool_name, input, output, success, time_cost, token_cost, score, call_hash, created_at

Evidence: models.py (MemoryType, BaseRecord, Resource, MemoryItem, MemoryCategory, CategoryItem, ToolCallResult, build_scoped_models)

---

## Search

### fulltext: ❌ FALSE
- No BM25 or full-text search. All search is embedding-based vector similarity (cosine).
- Evidence: `cosine_topk()` in inmemory/vector.py used universally; pgvector backend uses vector distance operators; no text search index or BM25 implementation

### semantic: ✅ TRUE
- pgvector extension for PostgreSQL (vector similarity operators)
- Brute-force cosine similarity for inmemory and SQLite backends
- Evidence: `VectorIndexConfig.provider: "bruteforce" | "pgvector"` in settings.py; `cosine_topk()` in database/inmemory/vector.py; architecture.md: "SQLite/inmemory vector search is brute-force"

### hybrid: ❌ FALSE
- Only vector (cosine) or LLM-based ranking; no BM25+vector fusion
- Evidence: retrieve.py RAG pipeline uses exclusively embedding similarity; no keyword/text component

### deep: ❌ FALSE
- Three-tier cascading retrieval (category → item → resource) but no multi-hop reasoning or deep traversal
- Evidence: retrieve.py pipeline is sequential single-hop

### codeGraph: ❌ FALSE
- No code graph, symbol search, or AST analysis
- Evidence: Absence in codebase

### docsSearch: ❌ FALSE
- No documentation indexing or doc search
- Evidence: Absence in codebase

### factQuery: ❌ FALSE
- No fact/entity structured query system
- Evidence: Absence in codebase

### timeline: ⚠️ PARTIAL
- `happened_at` field exists on MemoryItem for temporal data
- No timeline query mode, no temporal search UI or API
- Evidence: `MemoryItem.happened_at: datetime | None` in models.py

### searchModes: ✅ TRUE (2 modes)
1. **rag** — Embedding-based vector similarity (cosine top-k). Fast, sub-second.
2. **llm** — LLM-driven ranking where the LLM scores and selects IDs from formatted context. Slower but deeper.

Evidence: `RetrieveConfig.method: "rag" | "llm"` in settings.py; two separate workflow pipelines in retrieve.py (`_build_rag_retrieve_workflow` and `_build_llm_retrieve_workflow`); README retrieve() Dual-Mode Intelligence section

---

## Lifecycle

### decay: ⚠️ PARTIAL
- `recency_decay_days` (default 30 days) for salience scoring in retrieval ranking
- Affects retrieval ordering only (salience = similarity weighted by reinforcement + recency), not automatic expiration/deletion
- Evidence: `RetrieveItemConfig.recency_decay_days: 30.0` and `ranking: "similarity" | "salience"` in settings.py

### supersede: ❌ FALSE
- No explicit supersede mechanism. Content hash (`compute_content_hash()`) exists but only for dedup, not replacement.
- Evidence: `dedupe_merge` step is a placeholder pass-through; no supersede API

### contradiction: ❌ FALSE
- No contradiction or conflict detection between memories
- Evidence: Absence in codebase

### quarantine: ❌ FALSE
- No quarantine mechanism for suspect/low-quality memories
- Evidence: Absence in codebase

### autoResolve: ❌ FALSE
- No automatic task resolution lifecycle
- Evidence: Absence in codebase

### trustModel: ❌ FALSE
- No trust scoring, provenance tracking, or confidence model
- Evidence: Absence in codebase

### explicitForget: ✅ TRUE
- CRUDMixin provides `delete` operations: list/clear/create/update/delete memory
- Evidence: architecture.md: "CRUDMixin: list/clear/create/update/delete memory operations"; `src/memu/app/crud.py`; CHANGELOG v1.2.0: "clear memory (#239)"

---

## Extraction

### autoExtract: ✅ TRUE
- `memorize()` pipeline automatically extracts memories from resources. 7-step pipeline: `ingest_resource → preprocess_multimodal → extract_items → dedupe_merge → categorize_items → persist_index → build_response`
- 6 configurable memory types extracted via LLM prompts (profile, event, knowledge, behavior, skill, tool)
- Evidence: `_build_memorize_workflow()` in memorize.py; `MemorizeConfig.memory_types` in settings.py

### contentPreproc: ✅ TRUE
- `preprocess_multimodal` step handles: conversation segmentation, image captioning (Vision API), video frame extraction + captioning, document condensation, audio transcription
- Modality-specific prompts for conversation, document, image, video, audio
- Evidence: `_preprocess_resource_url()` and modality dispatchers in memorize.py; `format_conversation_for_preprocess()`; `VideoFrameExtractor` class

### dedup: ⚠️ PARTIAL
- `dedupe_merge` workflow step exists but is a **placeholder pass-through** (docstring: "Placeholder for future dedup/merge logic")
- `compute_content_hash()` exists for generating content hashes from summary + memory type (SHA-256, 16-char hex)
- Evidence: `_memorize_dedupe_merge()` in memorize.py: comment "# Placeholder for future dedup/merge logic"; `compute_content_hash()` in models.py

### qualityRefine: ❌ FALSE
- No explicit quality filtering, confidence thresholding, or refinement pass
- LLM extraction quality depends entirely on prompt quality, no post-extraction validation
- Evidence: Absence in codebase

### narrative: ❌ FALSE
- No narrative generation, story extraction, or summarization beyond category summaries
- Evidence: Absence in codebase

### clustering: ⚠️ PARTIAL
- Items are auto-assigned to categories via LLM extraction (each memory type prompt includes category assignment)
- Categories are pre-defined (10 defaults), not dynamically discovered via ML clustering
- Category summaries are regenerated when new items are added
- Evidence: `_map_category_names_to_ids()` and `_update_category_summaries()` in memorize.py; `_default_memory_categories()` in settings.py

### recurrence: ✅ TRUE
- Optional reinforcement tracking: `enable_item_reinforcement` in MemorizeConfig
- Tracks `reinforcement_count` and `last_reinforced_at` in MemoryItem.extra
- Previously seen items get updated instead of duplicated (via content hash match)
- Evidence: CHANGELOG v1.4.0: "Add salience-aware memory with reinforcement tracking (#186)"; `MemorizeConfig.enable_item_reinforcement` in settings.py

### persona: ❌ FALSE
- No persona profiling, trait extraction, or user profile building (beyond "profile" memory type which is generic)
- Evidence: Absence in codebase

---

## Platforms

### p_claude: ⚠️ PARTIAL
- `claude-agent-sdk>=0.1.24` listed as optional dependency in pyproject.toml (`[project.optional-dependencies] claude`)
- No dedicated Claude desktop app plugin found in integrations or docs
- Evidence: pyproject.toml line: `claude = ["claude-agent-sdk>=0.1.24"]`

### p_claudeCode: ⚠️ PARTIAL
- Same evidence as p_claude — `claude-agent-sdk` optional dependency
- No dedicated Claude Code skill/MCP server/plugin found in the repository
- Evidence: pyproject.toml claude optional dep

### p_cursor: ❌ FALSE
- No Cursor integration found
- Evidence: Absence in codebase and docs

### p_opencode: ❌ FALSE
- No OpenCode integration
- Evidence: Absence in codebase and docs

### p_windsurf: ❌ FALSE
- No Windsurf integration
- Evidence: Absence in codebase and docs

### p_codex: ❌ FALSE
- No Codex integration
- Evidence: Absence in codebase and docs

### p_copilot: ❌ FALSE
- No GitHub Copilot integration
- Evidence: Absence in codebase and docs

### p_antigravity: ❌ FALSE
- No Antigravity integration
- Evidence: Absence in codebase and docs

### Other Integrations
- **LangGraph**: ✅ TRUE — `MemULangGraphTools` adapter exposing `save_memory` and `search_memory` as LangChain tools
  - Evidence: `src/memu/integrations/langgraph.py`; `docs/langgraph_integration.md`
- **OpenAI Wrapper**: ✅ TRUE — `memu.client.openai_wrapper` auto-retrieves and injects memories into system context
  - Evidence: `src/memu/client/openai_wrapper.py`; architecture.md: "opt-in OpenAI client wrapper that auto-retrieves memories"
- **OpenClaw/memUBot**: ✅ TRUE — Separate repo `github.com/NevaMind-AI/memUBot` as "enterprise-ready OpenClaw" with memU memory backend
  - Evidence: README.md memU Bot section; CHANGELOG v1.4.0

---

## Benchmarks

| Benchmark | Score | Evidence |
|-----------|-------|----------|
| **LoCoMo** | 92.09% average accuracy | README.md Performance section; linked experiment repo `github.com/NevaMind-AI/memU-experiment` |

---

## Deployment & Setup

| Field | Value | Evidence |
|-------|-------|----------|
| **Install** | `pip install -e .` or `uv sync` | README Installation; AGENTS.md |
| **Python** | 3.13+ | pyproject.toml: `requires-python = ">=3.13"` |
| **Build** | Maturin (Rust core) + uv | pyproject.toml: `build-backend = "maturin"` |
| **Storage** | inmemory, SQLite, PostgreSQL+pgvector | `MetadataStoreConfig` in settings.py |
| **Docker** | `pgvector/pgvector:pg16` for Postgres | README Quick Start |
| **Cloud** | https://memu.so hosted service | README Cloud Version |

---

## Summary: VERIFIED Features by Category

### Architecture
| Feature | Status |
|---------|--------|
| webUi | ✅ TRUE (separate repo: memU-ui) |
| offline | ✅ TRUE (inmemory/SQLite/PostgreSQL self-hosted) |
| privacy | ✅ TRUE (local self-hosted, scope filters) |
| export | ❌ FALSE |
| multiAgent | ✅ TRUE (agent_id__in filters, scope model) |
| llmFlex | ✅ TRUE (SDK/HTTP/LazyLLM, OpenRouter, Grok, custom) |

### Data Model
| Feature | Status |
|---------|--------|
| entities | ⚠️ PARTIAL (6 memory types + 10 categories, no named entity field) |
| actions | ❌ FALSE |
| keywords | ❌ FALSE |
| anticipatedQueries | ❌ FALSE |
| triggerRules | ❌ FALSE |
| domainTag | ❌ FALSE |
| taskType | ⚠️ PARTIAL (tool memory type only) |
| context | ✅ TRUE (resource_id linkage) |
| source | ✅ TRUE (Resource.url) |
| originTrust | ❌ FALSE |
| emotional | ❌ FALSE |
| conflict | ❌ FALSE |
| layeredMemory | ✅ TRUE (Resource → MemoryItem → MemoryCategory, 3 tiers) |
| timeTravel | ❌ FALSE |
| schemaFields | ✅ TRUE (13+ fields across 4 models) |

### Search
| Feature | Status |
|---------|--------|
| fulltext | ❌ FALSE |
| semantic | ✅ TRUE (pgvector + brute-force cosine) |
| hybrid | ❌ FALSE (vector-only, no BM25) |
| deep | ❌ FALSE |
| codeGraph | ❌ FALSE |
| docsSearch | ❌ FALSE |
| factQuery | ❌ FALSE |
| timeline | ⚠️ PARTIAL (happened_at field, no query mode) |
| searchModes | ✅ TRUE (rag + llm, 2 modes) |

### Lifecycle
| Feature | Status |
|---------|--------|
| decay | ⚠️ PARTIAL (recency_decay for ranking only) |
| supersede | ❌ FALSE |
| contradiction | ❌ FALSE |
| quarantine | ❌ FALSE |
| autoResolve | ❌ FALSE |
| trustModel | ❌ FALSE |
| explicitForget | ✅ TRUE (CRUD delete operations) |

### Extraction
| Feature | Status |
|---------|--------|
| autoExtract | ✅ TRUE (7-step memorize pipeline) |
| contentPreproc | ✅ TRUE (5 modalities: conversation/document/image/video/audio) |
| dedup | ⚠️ PARTIAL (placeholder step, hash computed but unused) |
| qualityRefine | ❌ FALSE |
| narrative | ❌ FALSE |
| clustering | ⚠️ PARTIAL (predefined category assignment, not ML) |
| recurrence | ✅ TRUE (optional reinforcement tracking) |
| persona | ❌ FALSE |

### Platforms
| Feature | Status |
|---------|--------|
| p_claude | ⚠️ PARTIAL (claude-agent-sdk optional dep) |
| p_claudeCode | ⚠️ PARTIAL (same) |
| p_cursor | ❌ FALSE |
| p_opencode | ❌ FALSE |
| p_windsurf | ❌ FALSE |
| p_codex | ❌ FALSE |
| p_copilot | ❌ FALSE |
| p_antigravity | ❌ FALSE |
| LangGraph | ✅ TRUE |
| OpenAI Wrapper | ✅ TRUE |
| OpenClaw/memUBot | ✅ TRUE (separate repo) |

### Benchmarks
| Benchmark | Score |
|-----------|-------|
| LoCoMo | 92.09% |
