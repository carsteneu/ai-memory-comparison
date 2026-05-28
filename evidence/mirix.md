# MIRIX — Audit Report

> **Source:** `MIRIX-AI/MIRIX` (~3.6k stars, Python 96.6%, Apache 2.0)
> **Date:** 2026-05-28

## Vital Signs

| Field | Value |
|---|---|
| **Stars** | ~3.6k |
| **Language** | Python (96.6%), TypeScript (2.6%) |
| **License** | Apache 2.0 |
| **Deployment** | Docker (docker compose), PyPI `mirix-client` |
| **Integration** | REST API, Python client library (`MirixClient`) |
| **Storage** | PostgreSQL 17 (recommended) or SQLite |
| **Single binary** | No — requires Docker or Python runtime + PostgreSQL |
| **Foundation** | Built on Letta framework |

## Classification

MIRIX started as a desktop personal assistant agent but has since been **repositioned as a pure, dedicated memory system**. Per the docs: "Starting with 0.1.6, Mirix is a pure memory system that can be plugged into any existing agents." The desktop agent has been deprecated and moved to a separate `desktop-agent` branch. This is a dedicated memory backend, comparable to Mem0 or engram — not an agent framework with memory as a side feature.

## Feature Audit

### Architecture

| Feature | Status | Evidence |
|---|---|---|
| **webUi** | ✅ | Dashboard at `http://localhost:5173`. Memory visualization with tree/list views for all memory types. |
| **offline** | ✅ | "All long-term data stored locally with user-controlled privacy settings." "Local-first data storage." PostgreSQL/SQLite local DB. |
| **privacy** | ✅ | "Privacy-first design." "User-controlled privacy settings." "Enterprise-grade PostgreSQL security." "Encryption: Sensitive data encrypted at rest" (Knowledge Vault). |
| **export** | ❌ | No explicit export mechanism documented. Memory is in PostgreSQL/SQLite — accessible via DB tools but no user-facing export. |
| **multiAgent** | ✅ | "8 specialized agents working collaboratively": Meta Agent, Chat Agent, Core Memory Manager, Episodic Memory Manager, Semantic Memory Manager, Procedural Memory Manager, Resource Memory Manager, Knowledge Vault Manager. Plus reflexion_agent and background_agent in configuration. |
| **llmFlex** | ✅ | Supports OpenAI (GPT-4o-mini, GPT-4.1-mini), Anthropic (Claude 3.5 Sonnet), Google (Gemini 2.0 Flash). Configurable LLM endpoint, model, and context window. Separate topic extraction LLM config. |

### Data Model

| Feature | Status | Evidence |
|---|---|---|
| **entities** | ✅ | Semantic Memory stores named entities: `name`, `summary`, `details`, `source`. Core Memory has `human` and `persona` blocks with persistent user attributes. Knowledge Vault tracks `entry_type`, `source`, `caption`. |
| **actions** | ✅ | Episodic Memory tracks `event_type` (user_message, inferred_result, system_notification), `actor` (user/assistant). "Captures... what the user has done and is currently doing." |
| **keywords** | ✅ | Tag filtering system with `filter_tags` parameter. Supports hierarchical tags: "project:module:feature". Tags set during `add()` and filterable during `search()`. |
| **context** | ❌ | No explicit "why" or rationale field for why a memory was stored. Episodic `details` provides event context but not a dedicated storage rationale. |
| **source** | ✅ | Semantic Memory: `source` field (user_provided, Wikipedia, user_interaction, inferred). Knowledge Vault: `source` (github, user_provided, user_profile). Episodic: `actor` (user/assistant). |
| **emotional** | ❌ | No emotional or sentiment tracking documented in any memory component. |
| **conflict** | ❌ | No contradiction detection. Semantic memory "persist unless conceptually overwritten" — implicit replacement, no dual-track conflict surfacing. Semantic memory "Merges duplicate concepts" but this is dedup, not contradiction surfacing. |
| **layeredMemory** | ✅ | Six memory types form a layered architecture: Core (always-visible persona/prefs), Episodic (temporal events), Semantic (abstract concepts), Procedural (workflows), Resource (documents), Knowledge Vault (credentials). Each type has distinct structure and retrieval patterns. |
| **timeTravel** | ❌ | Temporal filtering exists (`start_date`/`end_date`, `list_episodic_memory_around_timestamp`) but no "query as of time T" capability. No version chains or snapshot history. |
| **schemaFields** | ~12 | Six distinct memory types, each with 3-5 structured fields: Core (human, persona), Episodic (event_type, summary, details, actor, timestamp), Semantic (name, summary, details, source), Procedural (entry_type, description, steps), Resource (title, summary, resource_type, content), Knowledge Vault (entry_type, source, sensitivity, secret_value, caption), plus filter_tags. Unique field names across all types: ~12-15. |

### Search & Retrieval

| Feature | Status | Evidence |
|---|---|---|
| **fulltext** | ✅ | PostgreSQL-native full-text search using `ts_rank_cd` (BM25-like). GIN-indexed. AND/OR query fallback logic. ILIKE fallback. "PostgreSQL-native BM25 full-text search." |
| **semantic** | ✅ | "Embedding Search (Semantic)" using vector similarity. Supports `search_method="embedding"` with configurable `similarity_threshold`. OpenAI (text-embedding-3-small, 1536d) and Google (text-embedding-004, 768d). |
| **hybrid** | ❌ | BM25 and embedding are separate search modes (`bm25` OR `embedding`). No combined/hybrid RRF ranking. Switch modes per query, not fused. |
| **deep** | ❌ | No deep search into raw conversation history or thinking content. |
| **codeGraph** | ❌ | No code graph or tree-sitter integration. |
| **docsSearch** | ❌ | No indexed documentation search. |
| **factQuery** | ❌ | No dedicated metadata/fact query API. Search is content-based via BM25 or embeddings. |
| **timeline** | ✅ | Temporal filtering on episodic memory: `start_date`/`end_date` (ISO 8601). `list_episodic_memory_around_timestamp()`. Automatic temporal extraction from natural language: "yesterday", "last week", "last 3 days", "this month". `retrieve_with_conversation()` extracts date ranges from queries. |
| **searchModes** | 6 | (1) `search()` BM25, (2) `search()` embedding, (3) `search()` string_match, (4) `retrieve_with_conversation()` (context-aware with auto topic extraction), (5) `retrieve_with_topic()` (topic-based), (6) `search_all_users()` (org-wide). |

### Knowledge Lifecycle

| Feature | Status | Evidence |
|---|---|---|
| **decay** | ✅ | Configurable decay: `fade_after_days: 30` (inactive, excluded from retrieval), `expire_after_days: 90` (permanently deleted). "Automatic Cleanup" per memory type: Core rewrites at 90% capacity, Episodic archives by relevance, Knowledge Vault expires outdated credentials. |
| **supersede** | ✅ | Semantic memory "persist unless conceptually overwritten" — implicit supersede on update. Core memory rewrites when exceeding 90% capacity. Semantic memory "Merges duplicate concepts." |
| **contradiction** | ❌ | No explicit contradiction detection mechanism. No dual-track preservation of conflicting facts. |
| **quarantine** | ❌ | No quarantine mechanism for suspicious or low-confidence memories. |
| **autoResolve** | ✅ | Decay system auto-resolves stale memories (`fade_after_days` for inactivity, `expire_after_days` for permanent deletion). Automatic cleanup across all memory types. Knowledge Vault: "Automatic Expiration" for credentials. |
| **trustModel** | ❌ | Knowledge Vault has sensitivity levels (low/medium/high) with access control, but this is a security classification, not a general trust/confidence model for memory quality. No origin-based trust scoring across memory types. |
| **explicitForget** | ❌ | No explicit user-facing forget/delete mechanism documented. Decay is automatic and time-based only. |

### Extraction Pipeline

| Feature | Status | Evidence |
|---|---|---|
| **autoExtract** | ✅ | Meta Agent auto-analyzes incoming content (text, images, voice) and routes to relevant Memory Managers. Screen capture every 1.5s with auto-dedup. "20 unique screenshots collected → memory update triggered." Six agents each auto-extract their domain data. |
| **contentPreproc** | ✅ | Screen capture dedup: "images visually similar (similarity > 0.99) are discarded." BM25 search preproc: text cleaning, punctuation removal, whitespace normalization, lowercase conversion, tokenization, special character escaping. |
| **dedup** | ✅ | Visual similarity dedup for screenshots (0.99 threshold). Semantic Memory: "Merges duplicate concepts." Core Memory: rewrites at 90% capacity to avoid bloat. Procedural Memory: "Updates workflows based on usage patterns." |
| **qualityRefine** | ✅ | Dedicated `reflexion_agent`: "Analyzes and improves memory quality." `background_agent`: "Handles asynchronous memory processing." Core memory rewrites compactly. Semantic merges duplicates. Procedural updates based on usage. |
| **narrative** | ✅ | Episodic memory entries are summaries + details generated from raw events. Paper mentions generating "consolidated events" from conversation history (e.g., "Caroline moved from her hometown, Sweden, 4 years ago"). LLM-driven consolidation during memory update workflow. |
| **clustering** | ✅ | Semantic Memory organized as tree structure with hierarchical categories (e.g., Favorites > Sports, Pets, Music). "Organized into a tree structure" shown in paper Figure 3. |
| **recurrence** | ✅ | Procedural Memory: "Recognizes recurring task patterns." "Updates workflows based on usage patterns." Episodic memory captures routines and recurring activities. |
| **persona** | ✅ | Core Memory explicit persona block: `{"label": "persona", "value": "I am a helpful assistant."}`. "persona block encodes the identity, tone, or behavior profile of the agent." Human block stores user identity and preferences. |

### Platform Support

| Feature | Status | Evidence |
|---|---|---|
| **p_claude** | ❌ | No native Claude Code integration. REST API accessible from any platform but no MCP server, hook, or plugin. |
| **p_codex** | ❌ | No Codex integration. |
| **p_opencode** | ❌ | No OpenCode integration. |
| **p_gemini** | ❌ | No Gemini CLI integration. |
| **p_copilot** | ❌ | No Copilot integration. |
| **p_cursor** | ❌ | No Cursor integration. |
| **p_windsurf** | ❌ | No Windsurf integration. |
| **p_openclaw** | ❌ | No OpenClaw integration. |
| **p_hermes** | ❌ | No Hermes integration. |
| **p_pi** | ❌ | No pi/omp integration. |
| **p_antigravity** | ❌ | No Antigravity integration. |

MIRIX is a **platform-agnostic memory backend** via REST API. Any agent framework can call it, but it has no first-class integrations into any specific IDE or agent platform.

### Benchmarks

| Feature | Status | Evidence |
|---|---|---|
| **b_locomo** | ✅ | **85.38%** overall LLM-as-Judge accuracy (SOTA). 85.11% single-hop, 83.70% multi-hop, 65.62% open-domain, 88.39% temporal. Outperforms all baselines (Zep 79.09%, LangMem 78.05%, Mem0 62.47%). Close to Full-Context upper bound (87.52%). |
| **b_longmemeval** | ❌ | Not evaluated. |
| **b_personamem** | ❌ | Not evaluated. |
| **b_token** | ✅ | ScreenshotVQA: 99.9% storage reduction vs RAG baselines, 93.3% vs long-context Gemini. From 15.07GB (SigLIP) / 236.70MB (Gemini) down to 15.89MB (MIRIX). Not measured as token cost but as storage efficiency. |
| **b_methodology** | ✅ | Full paper on arXiv (2507.07957). Code released on `public_evaluation` branch. Reproduction instructions with specific model versions and run counts. Baselines re-run with identical backbone models for fair comparison. |

## What MIRIX IS

- A **dedicated, pluggable memory system** for LLM agents (as of v0.1.6+)
- Six specialized memory types with dedicated agent-per-type architecture
- Multi-modal input support (text, images, voice, screen captures)
- Strongest LOCOMO benchmark results (85.38%, SOTA among memory systems)
- Configurable decay with fade and expire phases
- PostgreSQL-native BM25 + vector embedding search
- Quality refinement through reflexion_agent
- Built on Letta's memory framework (acknowledged in README)

## What MIRIX is NOT

- Not an IDE/agent platform plugin — pure REST API backend
- No hybrid (BM25+vector combined) search — modes are separate
- No time-travel querying (can't query "what did I know at time T")
- No contradiction detection or conflict surfacing
- No explicit user-facing forget mechanism
- No origin-based trust scoring across memory types
- No code graph or documentation search
- No export mechanism

## Architecture Summary

MIRIX uses a **multi-agent pipeline** on top of PostgreSQL/SQLite:

```
User Input → Meta Agent (routing) → Memory Managers (6x) → PostgreSQL/SQLite
                                      ↓
                              Chat Agent (retrieval)
```

1. **Meta Agent**: Analyzes incoming multimodal content, routes to relevant Memory Managers
2. **Six Memory Managers**: Each autonomously extracts and stores its domain data using LLM function calls
3. **Chat Agent**: Handles conversational retrieval via Active Retrieval (auto topic extraction → multi-component search → response synthesis)
4. **reflexion_agent + background_agent**: Quality improvement and async processing

Storage: PostgreSQL (production) or SQLite (lightweight). Docker deployment with Dashboard UI.

Search: `search_in_memory()` function with BM25, embedding, and string_match methods. Three retrieval APIs: `search()`, `retrieve_with_conversation()`, `retrieve_with_topic()`.

## Notable Strengths

- **Architectural ambition**: Six memory types is more than most competitors (Letta has 3, Mem0 has flat facts). MIRIX's type-specific agent-per-component architecture is genuinely differentiated.
- **Multi-modal**: One of very few memory systems that handles visual input natively (screenshots). 35% accuracy gain over RAG on ScreenshotVQA with 99.9% less storage.
- **LOCOMO SOTA**: 85.38% beats all published baselines including Zep (79.09%) and LangMem (78.05%).
- **Configurable decay**: `fade_after_days` + `expire_after_days` is a clean two-phase approach — more configurable than most systems.
- **Quality pipeline**: reflexion_agent + background_agent for continuous memory improvement.

## Notable Gaps (vs dedicated memory systems like YesMem)

- **No platform integrations**: MIRIX is a backend API. No MCP server, no Claude Code/Codex/Cursor plugin. Users must write integration code.
- **No hybrid search**: BM25 and embedding are separate modes, not combined RRF.
- **No contradiction handling**: No dual-track conflict surfacing. Overwrites replace old facts silently.
- **No time-travel**: Can filter by date range but can't query "what did the system know at time T."
- **No code graph**: No code-aware memory for development workflows.
- **No trust model**: Sensitivity is security classification, not confidence/trust scoring.

## Corrections / Notes from Prior Knowledge

1. **MIRIX is now a dedicated memory system, not an agent framework.** The desktop personal assistant was deprecated in v0.1.6. This is different from nanobot which remains an agent framework. MIRIX should be classified alongside Mem0, engram, and YesMem as a dedicated memory backend.
2. **Pluggable but platform-agnostic.** "Can be plugged into any existing agents" means via REST API — there are no IDE-specific plugins. All platform support flags are ❌.

---

`evidence: "https://github.com/carsteneu/ai-memory-comparison/blob/main/evidence/mirix.md"`
