# mem9 — Evidence

> Audit date: 2026-05-28. Source: GitHub `mem9-ai/mem9` main branch, `mem9.ai`, API docs, DESIGN.md.
> Repo URL: `https://github.com/mem9-ai/mem9` (note: org is `mem9-ai`, NOT `mem9co`)

## Description

"Unlimited memory for AI agents" — mem9 gives coding agents one shared persistent memory layer with hybrid recall (vector + keyword), a visual dashboard, and support across OpenClaw, Hermes Agent, Claude Code, OpenCode, Codex, and Dify. Built by PingCAP (TiDB creators) on TiDB Cloud Starter.

- **Stars**: 1,114 (1.1k on GitHub badge, 1.1k star count on page)
- **Language**: TypeScript (47.2%), Go (30.5%), JavaScript, Shell, Python, Astro
- **License**: Apache 2.0
- **Single binary**: No — Go server (`mnemo-server`) + TypeScript plugins + dashboard frontend
- **Created**: ~2026-02 (estimated — March 20, 2026 tweet says "shipped ~3 weeks ago"; tutorial from 2026-03-15; 433 commits on main)
- **Deployment**: Cloud (hosted API) / Self-hosted (Go binary or Docker, TiDB/Postgres/db9 backend)
- **Storage**: TiDB Cloud (MySQL-compatible with VECTOR type) — also supports PostgreSQL and db9 backends
- **Integration**: REST API (v1alpha2 + v1alpha1) + Plugins (OpenClaw, Claude Code, OpenCode, Codex) + Hooks + Skills
- **Setup**: OpenClaw paste-command (`Read https://mem9.ai/SKILL.md`), `curl | bash` provisioning, `go run`, Docker
- **Pricing**: Freemium — Free tier (13K add, 1.3K retrieval/mo). Starter $9, Pro $120 planned but currently free.
- **Docs**: `https://mem9.ai/docs` / `https://github.com/mem9-ai/mem9/tree/main/docs`

---

## Evidence by Feature

### Architecture

#### webUi ✅
- `README.md` — Repository has `dashboard/` directory: "Dashboard product frontend and supporting product docs."
- `mem9.ai` — "Your Memory" dashboard at `/your-memory/`: "Visualize, manage, analyze, import, and export your memories from the official mem9.ai interface."
- `mem9.ai` — "Visible in a dashboard: Review, analyze, import, and export memory from the hosted mem9.ai interface."

#### offline ✅
- `README.md` — Self-hosting section: "mem9 server supports multiple storage backends. Set `MNEMO_DB_BACKEND` to `tidb`, `postgres`, or `db9`, point `MNEMO_DSN` at that backend."
- `docs/DESIGN.md` — Server Mode: "Self-host `mnemo-server` (Go binary or Docker)" with "TiDB / MySQL" backend.
- Self-hosted server mode can run entirely on local infrastructure without internet dependency.

#### privacy ✅
- `mem9.ai` — Security section: "Encryption in transit and at rest", "Access controls", "Isolated data handling boundaries."
- `README.md` — `MNEMO_ENCRYPT_TYPE` env var: `plain`, `md5`, or `kms` encryption for tenant DB passwords.
- Self-hostable for full data control: "Run it on our cloud or bring it home. Your agent's memory, your infrastructure."

#### export ✅
- `mem9.ai` — Dashboard features: "import and export memory from the hosted mem9.ai interface."
- `README.md` — API includes import endpoints (`POST /v1alpha2/mem9s/imports` for memory/session file import).
- Self-hosted data is in TiDB/Postgres/db9 — standard DB export tools apply.

#### multiAgent ✅
- `README.md` — "Shared memory across agents and workflow platforms: OpenClaw, Hermes Agent, Claude Code, OpenCode, Codex, Dify apps, and custom clients can recall the same facts."
- `docs/DESIGN.md` — Spaces section: "A space is a shared memory pool. All agents in a space can read/write all memories." Space tokens support multiple agents with distinct identities per space.
- `README.md` — Space management API: `POST /api/spaces/:space_id/tokens` — add agents to space.

#### llmFlex — 3 providers
- `README.md` — Embedding: OpenAI (`text-embedding-3-small` default), Ollama via `MNEMO_EMBED_BASE_URL`, any OpenAI-compatible endpoint. LM Studio mentioned in DESIGN.md.
- `README.md` — LLM ingest: `MNEMO_LLM_MODEL` (default `gpt-4o-mini`), `MNEMO_LLM_BASE_URL` for any OpenAI-compatible chat endpoint.
- `docs/DESIGN.md` — "Embedding Provider Configuration: OpenAI, Ollama, LM Studio, any OpenAI-compatible endpoint."
- Count: OpenAI, Ollama, and any OpenAI-compatible (generic category, count as 3 distinct provider categories).

#### proxy — No evidence
- No proxy architecture. Plugins talk directly to the API server. Direct mode talks directly to TiDB HTTP Data API.

#### cacheOpt — No evidence
- No cache optimization described.

---

### Data Model

#### unit: "Memory with content, key, tags, source, metadata, embedding, version, score"
- `docs/DESIGN.md` — Core model: `{ content, key, tags, source, metadata, embedding, version, score }`.
- `README.md` — API response: `id`, `content`, `memory_type` (insight/pinned/session), `state` (active/archived), `version`, `created_at`, `updated_at`.

#### entities — No evidence
- No entity extraction or entity linking functionality described anywhere.

#### actions — No evidence
- No action tracking or action metadata.

#### keywords ✅
- `docs/DESIGN.md` — `tags` field: JSON array of strings, filterable in search via `?tags=tag1,tag2`.
- `README.md` — API: `GET /memories?tags=tech&source=openclaw-main&limit=10`.
- `docs/DESIGN.md` — Schema: `tags JSON` column, `memory_store(content, key?, tags?, metadata?)` tool signature.

#### anticipatedQueries — No evidence
- No anticipated queries or trigger fields.

#### triggerRules — No evidence
- No trigger rule configuration.

#### domainTag — No evidence
- No domain classification or domain metadata.

#### taskType — No evidence
- No task type classification.

#### context — No evidence
- No context/why field. The memory model has `content` as the primary text but no separate context/why field.

#### source ✅
- `docs/DESIGN.md` — `source` field: "who wrote it", auto-filled from agent_name in server mode. Filterable: `?source=sj-openclaw`.
- `README.md` — Schema: `source VARCHAR(100)`, indexed by `(space_id, source)`.

#### originTrust — No evidence
- No trust scoring for sources. Source is just an identifier, no trust model.

#### emotional — No evidence
- No emotional state tracking.

#### conflict ✅
- `docs/DESIGN.md` — "Conflict Resolution: LWW (Last Writer Wins) — Both Modes. The `version` field is tracked on every write."
- `README.md` — `If-Match` header for optimistic concurrency: "`If-Match` matches current version → write, version++; `If-Match` mismatch → server auto-resolves (MVP: LWW)."
- `docs/DESIGN.md` — "LLM Merge — Server Mode, Phase 2" for automatic conflict merging planned.

#### layeredMemory — No evidence
- No explicit memory layers (working memory, session, long-term, etc.). Memory type `insight|pinned|session` is a categorization, not a layered architecture.

#### timeTravel — No evidence
- `version` field tracks versions but no snapshot rollback or time-travel query capability described.

#### schemaFields — 14
- Database schema columns (`docs/DESIGN.md`): `id`, `space_id`, `content`, `key_name`, `source`, `tags`, `metadata`, `embedding`, `version`, `updated_by`, `created_at`, `updated_at` = 12
- API additional fields (`README.md` API ref): `memory_type` (insight/pinned/session), `state` (active/archived) = +2
- Search-only: `score` (not counted in schema — transient)
- Total unique schema fields: 14

---

### Search & Retrieval

#### fulltext ✅
- `README.md` — `MNEMO_FTS_ENABLED`: "Enable TiDB full-text search path."
- `docs/DESIGN.md` — Keyword-only mode: "Keyword search works immediately" using `content LIKE CONCAT('%', ?, '%')`.
- `docs/DESIGN.md` — Graceful degradation: "No embedding config → keyword search works immediately."

#### semantic ✅
- `docs/DESIGN.md` — Vector search: "`SELECT *, VEC_COSINE_DISTANCE(embedding, ?) AS distance FROM memories WHERE ... ORDER BY VEC_COSINE_DISTANCE(embedding, ?)`". Uses TiDB native VECTOR type with ANN cosine distance.
- `README.md` — Embedding support: OpenAI (`text-embedding-3-small`, 1536 dims), Ollama, custom endpoints.
- `README.md` — Server-side auto-embedding: `MNEMO_EMBED_AUTO_MODEL` env var for TiDB's `EMBED_TEXT()` server-side embedding.

#### hybrid ✅
- `mem9.ai` — Hero text: "Hybrid search, zero config — Keyword search works out of the box. Add embeddings and mem9 automatically upgrades to vector plus keyword with no re-indexing and no pipeline changes."
- `docs/DESIGN.md` — Hybrid Search Algorithm (step-by-step):
  1. Embed query → vector search (ANN) with `limit × 3`
  2. Keyword search with `limit × 3`
  3. Merge & de-duplicate: vector scores (1 − distance), keyword-only gets 0.5, vector score wins on overlap
  4. Sort & paginate after merge
- `README.md` — "Hybrid recall and a visual dashboard: Semantic search, keyword search, and inspection workflows stay in one system."

#### deep — No evidence
- No deep search (searching through thinking/context/raw conversation). Session messages are stored but only listing, not deep search.

#### codeGraph — No evidence
- No code graph or symbol-level search.

#### docsSearch — No evidence
- No documentation search capability.

#### factQuery — No evidence
- No fact metadata query. Search filters by tags, source, agent_id, session_id, state, memory_type — but no structured fact query (entity/action/keyword metadata search).

#### timeline — No evidence
- `created_at` and `updated_at` timestamps exist but no timeline view or chronological browsing interface described.

#### searchModes — 3
1. **Keyword-only** search (no embedding configured, LIKE-based)
2. **Hybrid search** (vector ANN + keyword, merged and ranked)
3. **Space Chain Recall** (`MNEMO_CHAIN_RECALL_STOP_SCORE`) — multi-space chained recall with confidence thresholds

Plus non-search access: filtered list (GET without `q`), filtered by tags/source/agent/state/memory_type.

#### dataSources — 2
1. **Memories** — primary CRUD/search
2. **Session Messages** — raw captured conversation (`/v1alpha2/mem9s/session-messages`)

Plus imports (memory files, session files) but those are ingested into the above two sources.

---

### Knowledge Lifecycle

#### decay — No evidence
- No decay/forgetting mechanism described.

#### supersede ✅
- `docs/DESIGN.md` — "If `key` is provided and already exists in the space → upsert (update existing)."
- `docs/DESIGN.md` — Version tracking: "`version` field is tracked on every write", "Atomic `version = version + 1` in SQL."
- `README.md` — `PUT` endpoint supports `If-Match` for optimistic concurrency.

#### contradiction ✅ — LWW resolution, LLM merge planned
- `docs/DESIGN.md` — "Conflicts result in overwrite. Simple, predictable, sufficient for most cases."
- `docs/DESIGN.md` — Phase 2: "LLM conflict merge (configurable per space): 'Two agents updated the same memory. Merge into one coherent version.'"
- But: no automatic contradiction detection (flagging conflicting facts). Conflict detection is mechanical (version mismatch), not semantic. Marking as **true** because LWW is a form of contradiction handling, and LLM merge is explicitly planned.

#### quarantine — No evidence
- No quarantine mechanism for sessions or learnings.

#### autoResolve — No evidence (planned, not implemented)
- `docs/DESIGN.md` — "LLM Merge — Server Mode, Phase 2" — planned future feature.
- Current behavior: LWW overwrite on version conflict. No automatic LLM-based resolution. Mark as **false** since it's not implemented.

#### trustModel — No evidence
- Source field exists but no trust scoring. No trust model for prioritizing reliable sources.

#### explicitForget ✅
- `README.md` — `DELETE /v1alpha2/mem9s/memories/{id}`: "Delete one memory. Deletes the selected memory row and returns 204 No Content on success."
- `docs/DESIGN.md` — `memory_delete(id)` tool in all plugins.

---

### Extraction Pipeline

#### autoExtract ✅
- `docs/DESIGN.md` — Claude Code hooks: `SessionStart` loads recent memories, `Stop` hook "Summarize last turn (via haiku), save as new memory."
- `opencode-plugin/README.md` — Hook flow: `chat.message` captures user prompts, `experimental.chat.system.transform` searches and injects memories, `session.idle` and `session.compacting` trigger background smart ingest.
- `docs/DESIGN.md` — "Automatic memory capture and recall via agent plugins."

#### contentPreproc — No evidence
- No content-aware preprocessing pipeline described. Messages are stripped of injected memory blocks in OpenCode plugin but no general preprocessing.

#### dedup — Partial (ingest dedup only, not memory dedup)
- `opencode-plugin/README.md` — "Identical transcripts are deduped per in-memory session state" — only prevents duplicate uploads of the same transcript within a 15-minute window.
- No cross-memory deduplication (duplicate facts across different memories not detected or merged). Mark as **false**.

#### qualityRefine — No evidence
- No quality scoring or refinement of extracted memories.

#### narrative — No evidence
- No narrative generation or summarization pipeline beyond hook-based capture.

#### clustering — No evidence
- No clustering of related memories.

#### recurrence — No evidence
- No recurrence or pattern detection.

#### persona — No evidence
- No persona extraction or user profile modeling.

---

### Platform Support

#### p_claude (Claude Code) ✅
- `README.md` — "Claude Code: Marketplace plugin with hooks and skills."
- `claude-plugin/` directory with hooks (`session-start.sh`, `stop.sh`, etc.) and `memory-recall` skill.
- `docs/DESIGN.md` — Full Claude Code plugin architecture: Hooks (SessionStart, UserPromptSubmit, Stop, SessionEnd) + Skills (memory-recall on fork context).

#### p_codex (Codex) ✅
- `README.md` — "Codex: Marketplace plugin with managed hooks and project overrides."
- `codex-plugin/` directory in repo.
- `mem9.ai` — Codex listed under "Works with your agent stack."

#### p_opencode (OpenCode) ✅
- `README.md` — "OpenCode: Plugin SDK integration loaded from `opencode.json`."
- `opencode-plugin/README.md` — Full plugin with TUI setup (`/mem9-setup`), server hooks, tools (memory_store/search/get/update/delete), recall injection, auto-ingest.
- Installation: `opencode plugin --global @mem9/opencode`.

#### p_gemini (Gemini CLI) — No evidence
- Not listed on website or README.

#### p_copilot (Copilot) — No evidence
- Not listed on website or README.

#### p_cursor (Cursor) — No evidence
- Not listed on website or README.

#### p_windsurf (Windsurf) — No evidence
- Not listed on website or README.

#### p_openclaw (OpenClaw) ✅
- `README.md` — "OpenClaw: `kind: 'memory'` plugin for server-backed shared memory" — primary target platform.
- `openclaw-plugin/` directory. `mem9.ai` — "Install for OpenClaw" with paste command.
- `docs/DESIGN.md` — Plugin replaces OpenClaw's built-in memory slot. Framework calls memory automatically at lifecycle points.

#### p_hermes (Hermes Agent) ✅
- `README.md` — "Hermes Agent: Memory provider plugin with setup and activation flow."
- Separate repo: `mem9-ai/mem9-hermes-plugin`.
- `mem9.ai` — Hermes Agent listed under "Works with your agent stack."

#### p_pi (pi/omp) — No evidence
- Not listed.

#### p_antigravity (Antigravity) — No evidence
- Not listed.

Additional platform: **Dify** — Dify tool plugin with `mem9-ai/mem9-dify-plugin` repo, supports Agent apps and Workflow apps.

---

### Benchmarks

#### b_locomo ✅
- `mem9.ai` — "LoCoMo Benchmark Results" section with full results:
  - **F1 Score**: 58.84%
  - **LLM Score**: 71.95%
  - **Evidence Recall**: 53.76%
  - Model: qwen3.5-plus
  - Category breakdown: Multi-hop (22.60% F1), Single-hop (58.18%), Temporal (13.79%), Open-domain QA (56.57%), Adversarial (96.19%).
- `benchmark/` directory: locomo harness, scripts (`drive-session.py`, `report.py`), results output.
- `docs/BENCHMARK.md` — Pipeline documented: seven-phase A/B benchmark comparing baseline (without mem9) vs treatment (with mem9).

#### b_longmemeval — No evidence
- Not mentioned on website or in docs.

#### b_personamem — No evidence
- Not mentioned.

#### b_token — No evidence
- No token reduction percentage published.

#### b_methodology ✅
- `benchmark/README.md` — Full benchmark harness open-sourced: "The harness compares an agent without mem9 memory (Profile A / baseline) vs. with mem9 memory (Profile B / treatment)."
- `docs/BENCHMARK.md` — Seven-phase pipeline documented: cleanup, configure space, create profiles, workspace setup, start gateways, run benchmark, summary.
- `benchmark/` directory contains scripts, prompts, workspace, MR-NIAH bridge, locomo harness.
- Benchmark results published on mem9.ai with methodology explanation.

---

## Summary Feature Matrix

| Category | Feature | Present | Evidence |
|----------|---------|---------|----------|
| Architecture | webUi | ✅ | Dashboard (`dashboard/` dir, `/your-memory/`) |
| Architecture | offline | ✅ | Self-hosted server mode (Go binary/Docker) |
| Architecture | privacy | ✅ | Encryption at rest, self-hostable |
| Architecture | export | ✅ | Dashboard export, DB export tools |
| Architecture | multiAgent | ✅ | Spaces with multi-token, shared memory pools |
| Architecture | llmFlex | ✅ (3) | OpenAI, Ollama, OpenAI-compatible endpoints |
| Architecture | proxy | ❌ | Direct API/client architecture |
| Architecture | cacheOpt | ❌ | No evidence |
| Data Model | entities | ❌ | No entity extraction |
| Data Model | actions | ❌ | No action tracking |
| Data Model | keywords | ✅ | Tags (JSON array), filterable |
| Data Model | context | ❌ | No context/why field |
| Data Model | source | ✅ | Source field, auto-populated from agent name |
| Data Model | emotional | ❌ | No emotional state |
| Data Model | conflict | ✅ | LWW + version tracking, If-Match, LLM merge planned |
| Data Model | layeredMemory | ❌ | Memory type is categorization, not architecture |
| Data Model | timeTravel | ❌ | Version tracking only, no rollback |
| Data Model | schemaFields | ✅ (14) | 12 DB columns + memory_type + state |
| Search | fulltext | ✅ | TiDB FTS + LIKE-based keyword search |
| Search | semantic | ✅ | TiDB native VECTOR + ANN cosine |
| Search | hybrid | ✅ | Vector + keyword merged with scoring |
| Search | deep | ❌ | No thinking/context search |
| Search | codeGraph | ❌ | No code graph |
| Search | docsSearch | ❌ | No docs search |
| Search | factQuery | ❌ | No structured metadata query |
| Search | timeline | ❌ | No timeline view |
| Search | searchModes | ✅ (3) | Keyword, hybrid, space chain recall |
| Search | dataSources | ✅ (2) | Memories + Session Messages |
| Lifecycle | decay | ❌ | No decay/forgetting |
| Lifecycle | supersede | ✅ | Upsert by key, version tracking |
| Lifecycle | contradiction | ✅ | LWW resolution, LLM merge planned |
| Lifecycle | quarantine | ❌ | No quarantine |
| Lifecycle | autoResolve | ❌ | LLM merge planned, not implemented |
| Lifecycle | trustModel | ❌ | Source field only, no trust scoring |
| Lifecycle | explicitForget | ✅ | DELETE endpoint |
| Extraction | autoExtract | ✅ | Hooks auto-capture, summarize & save |
| Extraction | contentPreproc | ❌ | No preprocessing |
| Extraction | dedup | ❌ | Ingest dedup only (in-memory, not storage) |
| Extraction | qualityRefine | ❌ | No quality refinement |
| Extraction | narrative | ❌ | No narrative generation |
| Extraction | clustering | ❌ | No clustering |
| Extraction | recurrence | ❌ | No recurrence detection |
| Extraction | persona | ❌ | No persona extraction |
| Platform | p_claude | ✅ | Claude Code plugin (hooks + skills) |
| Platform | p_codex | ✅ | Codex marketplace plugin |
| Platform | p_opencode | ✅ | OpenCode plugin (@mem9/opencode) |
| Platform | p_gemini | ❌ | Not supported |
| Platform | p_copilot | ❌ | Not supported |
| Platform | p_cursor | ❌ | Not supported |
| Platform | p_windsurf | ❌ | Not supported |
| Platform | p_openclaw | ✅ | Primary platform (kind: "memory" plugin) |
| Platform | p_hermes | ✅ | Hermes Agent provider plugin |
| Platform | p_pi | ❌ | Not supported |
| Platform | p_antigravity | ❌ | Not supported |
| Benchmarks | b_locomo | ✅ (58.84% F1) | Published on mem9.ai |
| Benchmarks | b_longmemeval | ❌ | Not published |
| Benchmarks | b_personamem | ❌ | Not published |
| Benchmarks | b_token | ❌ | Not published |
| Benchmarks | b_methodology | ✅ | Open-source benchmark harness |
