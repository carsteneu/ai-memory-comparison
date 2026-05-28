# LangMem — Evidence

> Every claim backed by public source code or documentation.
> Audit date: 2026-05-28. Source: GitHub `langchain-ai/langmem` main branch, `langchain-ai.github.io/langmem/` docs.

## Vital Signs

- **Stars**: 1,474 (GitHub API, `stargazers_count`)
- **Language**: Python (GitHub API, `language`)
- **License**: MIT (GitHub API, `license.spdx_id = "MIT"`)
- **Created**: 2025-01-21 (GitHub API, `created_at`)
- **Single binary**: false — Python library, pip install. No standalone executable.

## Architecture

### Deployment — Library (pip)
- `README.md` — "pip install -U langmem"
- `pyproject.toml` — Standard Python package, no binary distribution.
- Works as a Python library integrated into LangGraph agents.

### Storage — LangGraph BaseStore (vector-backed)
- `README.md` — `InMemoryStore` for dev, `AsyncPostgresStore` for production. Configured with embedding dimensions: `index={"dims": 1536, "embed": "openai:text-embedding-3-small"}`.
- `docs/concepts/conceptual_guide.md` — "Storage system is built on LangGraph's storage primitives." Supports semantic search, direct access, metadata filtering.
- Storage is delegated to LangGraph's `BaseStore` interface. No custom storage engine.

### Integration — LangGraph tools/library
- `README.md` — Tools (`create_manage_memory_tool`, `create_search_memory_tool`) integrate into LangGraph agents via `create_react_agent`. Also provides `create_memory_store_manager` for background extraction.
- `docs/guides/use_tools_in_crewai.md` — Also works with CrewAI.
- Integration is purely programmatic (Python library). No MCP server, no hooks, no proxy.

### Proxy — false
- No proxy. LangMem is a library, not a middleware. No conversation stream interception.

### Web/TUI — false
- No shipped visual interface. Purely a Python library.

### Offline — ❌ (claimed true, actually false)
- `README.md` — "Configure your environment with an API key for your favorite LLM provider: `export ANTHROPIC_API_KEY="sk-..."`"
- `docs/hot_path_quickstart.md` — Same: requires Anthropic API key. Embeddings use `"openai:text-embedding-3-small"` (OpenAI API).
- `docs/concepts/conceptual_guide.md` — "Prompt an LLM to determine how to expand or consolidate the memory state." Every memory operation calls an external LLM.
- **Correction**: Core memory functionality (extraction, search) depends on external LLM API calls (Anthropic for extraction, OpenAI for embeddings). No local/offline mode documented. Mark as **false**.

### Multi-agent — false
- No documented multi-agent coordination. Single-agent memory per LangGraph agent.

### LLM providers — 1+ (Anthropic shown; LangChain `init_chat_model` compatible)
- `README.md` — Shows `"anthropic:claude-3-5-sonnet-latest"`. Uses LangChain's `init_chat_model`, which supports many providers, but langmem itself does not enumerate or test them. Counting as 1 (documented Anthropic path).

### Cache optimization — false
- No cache optimization documented.

### Privacy/encrypt — false
- No encryption or privacy controls documented.

### Data export — false
- No data export functionality documented. Memories live in LangGraph's store; export would require using LangGraph store APIs directly.

### Setup — "pip install -U langmem"
- `README.md` — "pip install -U langmem" plus LLM API key configuration.

### Pricing — free (MIT)
- `LICENSE` — MIT License. No paid tiers.

---

## Data Model

### Storage unit — Memory (text, with optional Pydantic schema)
- `README.md` — Memories stored as text content with `kind` tags. Example: `{"kind": "Memory", "content": {"content": "User likes dogs as pets"}}`.
- `docs/concepts/conceptual_guide.md` — Three memory types: Semantic (facts), Episodic (experiences), Procedural (prompts). Semantic supports both Collection (document records) and Profile (single document with Pydantic schema).
- Profile example: `UserProfile(BaseModel)` with `name`, `preferred_name`, `response_style_preference`, `special_skills`, `other_preferences`.

### Entities — false
- No structured entity extraction or entity tables. Content is unstructured text.

### Actions — false
- No action/command extraction as structured fields.

### Keywords/tags — false
- No keyword or tag system. Content is plain text with optional `kind` label.

### Anticipated queries — false
- No query prediction or anticipated-query generation.

### Trigger rules — false
- No conditional activation or trigger-based recall.

### Domain tag — false
- No domain categorization (code, marketing, legal, etc.).

### Task type — false
- No task-type classification (task, idea, blocked, stale).

### Context (why) — false
- No separate "why" field. Memories are flat text.

### Source attribution — false
- No source tracking. Memories are LLM-extracted with no attribution to session/agent/user.

### Origin + trust — false
- No trust-weight model.

### Emotional — false
- No sentiment or emotional tracking.

### Conflict surfacing — false
- No contradiction detection or conflict surfacing.

### Layered memory — false
- Flat memory model. No hierarchical layers (L0→L3 etc.).

### Time-travel — false
- No historical browsing or temporal search. `created_at`/`updated_at` timestamps exist on store items but no time-travel query tool.

### Schema fields — ~4 (claimed 4 ✅)
- LangGraph `Item` object: `namespace`, `key` (UUID), `value` (dict with `kind` + `content`), `created_at`, `updated_at`, `score` = 6 fields total.
- Excluding auto-generated (`key`/uuid, `created_at`, `updated_at`, `score`): `namespace`, `kind`, `content` = 3 structured fields.
- With user-defined Pydantic profiles, fields are unlimited but user-defined; the base memory schema is minimal.
- Counting 4 is reasonable if `kind` and `content` are both counted, plus namespace and the content's internal structure. Verified as approximately correct.

---

## Search & Retrieval

### Full-text — false
- No BM25, FTS5, or keyword-based search. Only semantic vector search via LangGraph's `store.search()`.

### Semantic/vector ✅
- `README.md` — Embedding-based search: `store.search(namespace, query=...)` uses `"openai:text-embedding-3-small"` (1536 dims).
- `docs/concepts/conceptual_guide.md` — "Semantic Search: Find memories by semantic similarity."
- `docs/background_quickstart.md` — `store.search(("memories",))` returns semantically ranked results.
- **Verdict: true ✅**

### Hybrid (BM25+Vec) — false
- No hybrid search. No BM25 or keyword component. Pure vector similarity.

### Deep (incl. thinking) — false
- No search over reasoning traces or thinking blocks.

### Code graph — false
- No code structure indexing.

### Docs search — false
- No documentation search or ingestion.

### Fact metadata query — false
- No structured metadata query. Search is semantic only.

### Timeline view — false
- No chronological browsing or temporal search tool, though `created_at` exists on store items.

### Search modes — 1 ✅
- Single search method: `store.search()` (semantic vector similarity). Also `store.get()` for direct key lookup, but that's not a search mode.
- **Verdict: 1 ✅**

### Data sources — 1
- Memories only. One data source (the memory store). No code, docs, or multi-source search.

---

## Knowledge Lifecycle

### Decay/forgetting — false
- No automatic relevance decay or forgetting mechanism.

### Supersede/replace — false
- `docs/concepts/conceptual_guide.md` — Collection memories: "The system must reconcile new information with previous beliefs, either *deleting*/*invalidating* or *updating*/*consolidating* existing memories." This is LLM-prompted during extraction, not a structured supersede chain.
- No explicit `supersedes` field or replacement tracking.

### Contradiction detect — false
- No automatic contradiction detection.

### Quarantine — false
- No session quarantine capability.

### Auto-resolution — false
- No automatic resolution of stale items.

### Trust model — false
- No multi-tier trust hierarchy.

### Explicit forget — false
- `create_manage_memory_tool` supports delete operations (agent can delete memories by ID), but no explicit user-facing "forget" command or API documented in README/quickstarts. The tool allows deletion as part of normal memory management.

---

## Extraction Pipeline

### Auto-extraction ✅
- `README.md` — "Background memory manager that automatically extracts, consolidates, and updates agent knowledge."
- `docs/background_quickstart.md` — `create_memory_store_manager` extracts memories automatically from conversations in the background.
- `docs/concepts/conceptual_guide.md` — "Subconscious Formation": "prompting an LLM to reflect on a conversation after it occurs...finding patterns and extracting insights without slowing down the immediate interaction."
- Hot-path also supports conscious (agent-initiated) extraction via `create_manage_memory_tool`.
- **Verdict: true ✅**

### Content-aware preproc — false
- No content-type-aware preprocessing documented.

### Deduplication — false
- No deduplication documented. The background manager can "consolidate" memories via LLM prompting (updating/deleting redundant ones), but no algorithmic dedup.

### Quality refinement — false
- No quality scoring or refinement pass beyond the initial LLM extraction.

### Narrative generation — false
- No session summaries or project profiles. The focus is on individual memory extraction.

### Clustering — false
- No topic clustering documented.

### Recurrence detection — false
- No recurring pattern detection.

### Persona extraction — false
- Profiles can capture user preferences (`UserProfile` schema), but this is schema-driven extraction, not a dedicated persona engine. No automatic persona model.

---

## Platform Support

### Claude Code — ❌ (claimed true, actually false)
- No documented Claude Code integration. No MCP server, no hooks, no plugin, no skill for Claude Code.
- The README shows `"anthropic:claude-3-5-sonnet-latest"` as the LLM model via LangChain's chat model — this is using Claude as an API model, not Claude Code CLI integration.
- **Correction**: Mark as **false**. Integration is via LangGraph agents using Claude API, not Claude Code CLI.

### Codex — false
- No Codex integration documented.

### OpenCode — false
- No OpenCode integration documented.

### Gemini CLI — false
- No Gemini CLI integration documented.

### Copilot — false
- No Copilot integration documented.

### Cursor — false
- No Cursor integration documented.

### Windsurf — false
- No Windsurf integration documented.

### OpenClaw — false
- No OpenClaw integration documented.

### Hermes — false
- No Hermes integration documented.

### pi/omp — false
- No pi/omp integration documented.

### Antigravity — false
- No Antigravity integration documented.

---

## Benchmarks

### LoCoMo — —
- No published LoCoMo score.

### LongMemEval — —
- No published LongMemEval score.

### PersonaMem — —
- No published PersonaMem score.

### Token reduction — —
- No published token reduction metrics.

### Methodology open — false
- No benchmark methodology published.

---

## Claims NOT present (verified)

The following are correctly NOT claimed and verified absent:

**Data Model:** entities, actions, keywords, anticipatedQueries, triggerRules, domainTag, taskType, context, source, originTrust, emotional, conflict, layeredMemory, timeTravel — all ❌ (flat text memory model with optional Pydantic profile schema)

**Search:** fulltext, hybrid, deep, codeGraph, docsSearch, factQuery, timeline — all ❌ (semantic vector search only)

**Lifecycle:** decay, supersede, contradiction, quarantine, autoResolve, trustModel — all ❌ (no lifecycle management beyond agent-initiated delete via manage_memory_tool)

**Extraction:** contentPreproc, dedup, qualityRefine, narrative, clustering, recurrence, persona — all ❌ (auto-extraction is single LLM call; no pipeline stages beyond initial extraction)

**Architecture:** proxy, webUi, multiAgent, cacheOpt, privacy, export — all ❌ (library, not a service)

---

## Audit Corrections

1. **offline: true → false**: LangMem requires external LLM API calls for all core memory functionality. Every quickstart begins with `export ANTHROPIC_API_KEY="sk-..."` and embeddings use OpenAI API. No local/offline mode documented.

2. **p_claude: true → false**: No Claude Code CLI integration. Uses Claude as an API model via LangChain, not as a Claude Code MCP/hook/plugin integration. The CRITERIA.md requires "Documented integration with Claude Code (MCP, hooks, plugin, or skill)" — none exist.
