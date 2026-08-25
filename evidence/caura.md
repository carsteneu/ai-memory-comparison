# Caura — Evidence

**Repo:** `caura-ai/caura`
**Stars:** 448
**Language:** Python
**License:** Apache-2.0
**Created:** 2026-04-27
**Description:** Governed shared memory for multi-tenant, multi-agent AI fleets — LLM-enriched memories with visibility scopes, trust tiers, keystone policies, an auto-extracted knowledge graph, and outcome-based retrieval tuning, exposed over MCP and REST.

> Sources: `github.com/caura-ai/caura` (main branch, commit `8ccf2ef`). Formerly MemClaw — the repo, packages, env vars and tool names were renamed to `caura_*` with permanent `memclaw_*` aliases. Audit date: 2026-08-25.

---

## System Metadata

| Field | Value |
|-------|-------|
| **Deployment** | `Self-host (Docker Compose / bare ASGI) + managed cloud (caura.ai)` |
| **Storage** | `PostgreSQL 16 + pgvector` (Redis for cache/STM) |
| **Integration** | `MCP (Streamable HTTP, 12 tools) / REST / Python + TypeScript SDKs / OpenClaw plugin / Claude Code + Codex skill` |
| **Single binary?** | `no` (core-api + core-storage-api + Postgres + Redis; four containers) |
| **Setup** | `docker compose up -d` (self-host), `pip install caura-client` / `npm install @caura/client` (clients) |
| **Pricing** | `freemium` — engine Apache-2.0 and self-hostable forever; managed platform at caura.ai is paid |
| **Storage unit** | `Memory` (14 typed kinds: fact / episode / decision / preference / task / plan / action / outcome / rule / insight / …) plus `Document` (JSONB collections) |

---

## Architecture

### Proxy ❌
> No in-flight interception of the LLM conversation stream. The OpenClaw plugin's `context-engine.ts` hooks turn boundaries (afterTurn auto-write), which is a hook, not a proxy.

### Web/TUI ✅
- `static/docs/integration-guide.md:29` — "Web UI | Served at `/ui` | Manage, Prism (with Graph button), Playground, Fleet, MCP Test, Ingest, Admin Dashboard".
- `static/docs/integration-guide.md:291,345` — Fleet page `/ui/fleet.html` and Manage page `/ui/tenant-admin.html` (agents, trust levels, home fleets, last-seen).

### Offline ✅
- `README.md:285` — "Pair Standalone mode with `--profile embed-local` … for a fully self-contained deployment: no admin keys, no external API calls, all embeddings computed locally. Useful for offline / air-gapped environments".
- `README.md:180-185` — documented offline / air-gapped compose operation (`--no-pull`, `pull_policy: never`).
- `README.md:1223` — "the application makes zero outbound calls unless you configure a Sentry DSN or an LLM/embedding provider".

### Multi-agent ✅
- `README.md:392` — visibility scopes stamped per memory: `scope_agent` (private), `scope_team` (fleet-wide, default), `scope_org` (cross-fleet).
- `README.md:393` — "Agent trust tiers — four levels control cross-fleet reads, writes, and deletes."
- `README.md:956-959` / `plugin/src/heartbeat.ts` — fleet nodes register and heartbeat; `POST /fleet/heartbeat`, `GET /fleet/nodes`, `POST /fleet/commands` coordinate a fleet of agents.
- `core-api/src/core_api/services/trust_service.py:39` — `require_trust` gates every cross-agent/cross-fleet operation on the agent's tier.

### LLM providers (count: 5) ✅
- `README.md:413` — "Multi-provider LLM — primary + fallback provider chain per tenant (OpenAI, Gemini, Anthropic, OpenRouter) with platform defaults".
- `README.md:1023,1034` — `ENTITY_EXTRACTION_PROVIDER` accepts `openai`, `gemini`, `anthropic`, `openrouter`; `PLATFORM_LLM_PROVIDER` adds `vertex` → 5 LLM backends.
- Embeddings are separately selectable: `EMBEDDING_PROVIDER=openai | local | fake`, plus a self-hosted TEI (`BAAI/bge-m3`) profile (`README.md:1022`, `README.md:160-165`, `docs/local-embedder.md`).

### Cache optimization ✅
- `core-api/src/core_api/services/memory_service.py:3875-3896` — `_get_or_cache_embedding`: Redis-backed query-embedding cache keyed on `VECTOR_DIM` + query instruction with TTL, plus in-flight coalescing so concurrent cold-cache callers share one provider round-trip ("measured 3-second tail spread on 5 parallel novel-query recalls pre-fix").
- `core-api/src/core_api/cache.py:1` — "Redis cache client with graceful fallback to in-memory."
- `BENCHMARKS.md:16-18` — published token savings vs full-context baseline: 96.6% (LoCoMo) / 98.2% (LongMemEval).

### Procedural memory ✅
- `README.md:522-558` — Skill Factory: agents author `SKILL.md` skills into the `skills` document collection; Forge mines memory + outcome signals and distills repeated successful procedures into skill candidates; a `candidate → staged → active` lifecycle gates promotion.
- `README.md:545-552` — delivery: agents pull active skills over MCP (`caura_doc op=search|read`), or the OpenClaw plugin reconciler fetches `POST /api/v1/skills/installable` and writes each skill to the node's skill directory / OpenClaw load path.
- `core-api/src/core_api/services/skill_lifecycle.py`, `core-api/src/core_api/routes/skills_inbox.py:13` — lifecycle transitions and operator inbox (`approve` / `edit` / `defer` / `quarantine` / `reject`).

### Sandboxed execution ❌
> Skills are delivered to the agent's harness to run there; nothing in this repo executes user-supplied code under resource limits. (The only "sandbox" hits are a GCP staging-project name and the read-only demo tenant, `core-api/src/core_api/auth.py:145`.)

### Scheduled/autonomous ✅
- `core-operations/src/core_operations/app.py:104-170` — a scheduler service registering recurring ticks that run without any user request: `lifecycle-archive-expired`, `lifecycle-archive-stale`, `lifecycle-purge-soft-deleted`, `lifecycle-crystallize`, `lifecycle-entity-link`, `lifecycle-insights`, `agent-digest` (daily), `agent-digest-weekly`, `interviewer-schedule` (hourly), `embedding-coverage`.
- `README.md:395` — daily/weekly per-agent activity digests "generated server-side", driven by the `agent-digest` / `agent-digest-weekly` cron ticks.
- `docs/operator-forge-cron.md` — scheduling the Forge resident.

### Privacy/encrypt ✅
- `README.md:1032` — `SETTINGS_ENCRYPTION_KEY`: "Fernet key for encrypting tenant settings. Required in production."
- `README.md:391` — "row-level database separation per tenant; PII auto-detected and flagged on every write (surfaced in memory metadata as `contains_pii`/`pii_types`)"; the classifier prompt is at `common/enrichment/_prompts.py:148-154`.
- `README.md:1219-1223,1240-1244` — "Caura **does not phone home** by default. No usage data, analytics, or tracking of any kind." Sentry is opt-in via `SENTRY_DSN`.
- `README.md:596-600` — Interviewer disk-parser is default-deny and scrubs credential-shaped strings locally before submit, masking again server-side.

### Data export ✅
- `scripts/backup-db.sh:1-4` — "Database backup: pg_dump → gzip → optional GCS upload".
- `README.md:883-885,1141` — `GET /memories` (filter by type/status/agent, paginate) and `GET /memories/{id}` return full memory JSON; `caura_list` is the same surface over MCP, so the corpus is exportable as structured JSON without direct DB access.

---

## Data Model

### Entities ✅
- `README.md:401` — "Live knowledge graph — people, orgs, locations, and concepts extracted into entities and relations on every write. Semantic entity resolution (>0.85 cosine) auto-merges duplicates."
- `common/models/entity.py`, `core-api/src/core_api/services/entity_extraction.py` — dedicated `entities` / `relations` tables with their own embeddings, separate from the memory row.
- `common/models/memory.py:75-80` — each memory additionally links `subject_entity_id` → `entities.id`.

### Actions ✅
- `common/enrichment/constants.py:34` — `ACTION = "action"` is a first-class member of the 14-value `MemoryType` enum; `common/enrichment/_prompts.py:58-60` defines it as "the ACTOR did a DEED. Verbs of doing (deployed, merged, sent, completed, created, filed, staged, confirmed, approved, paused, cancelled)".
- `common/models/memory.py:74-80` — every memory is additionally stored as an RDF triple in dedicated columns (`subject_entity_id`, `predicate`, `object_value`), so the operation itself is a structured field, not free text.

### Keywords/tags ✅
- `common/enrichment/_prompts.py:114-120` — enrichment emits `"tags": array of 1-5 lowercase keyword tags for search and filtering`, kebab-case, singular.
- `README.md:399` — tags are generated on every write from a single `content` field; `caura_list` filters on them.

### Anticipated queries ✅
- `common/enrichment/_prompts.py:156-173` — `retrieval_hint`: "short clause … capturing the memory's SEMANTIC ESSENCE in vocabulary a reader would use when asking about it LATER. Used to augment the embedding so queries that reference the significance/category of the memory can find it, not just ones that share surface vocabulary with the content."
- `core-api/src/core_api/pipeline/steps/write/parallel_embed_enrich.py:30` — the stored vector is computed from `compose_embedding_text(content, retrieval_hint)`; the hint is persisted at `core-api/src/core_api/services/memory_service.py:3008-3011`.

### Trigger rules ❌
> Memories carry temporal validity bounds (`ts_valid_start` / `ts_valid_end`, `expires_at`) that feed ranking and the archive-expired tick (`core-storage-api/src/core_storage_api/services/postgres_service.py:1728-1737`), but there is no condition-based activation ("show this when file X is opened"). Keystones are always-on governance rules for a scope, not conditional triggers.

### Domain tag ❌
> The enrichment schema has `business_relevance: "business" | "personal"` (`common/enrichment/_prompts.py:195-200`) — a two-value governance gate, not a domain taxonomy (code / marketing / legal / finance / general). Free-form `tags` carry topical categorization instead.

### Task type ✅
- `common/enrichment/constants.py:29,32,34` — `task` ("pending work"), `plan` (ordered steps), `action` (completed deed) are distinct enum values; `common/enrichment/_prompts.py:100-101` shows the classification rules.
- `common/enrichment/constants.py:235-244` — an 8-value status vocabulary (`active`, `pending`, `confirmed`, `cancelled`, `outdated`, `conflicted`, `archived`, `deleted`) classifies where unfinished work stands; `common/constants.py:23` defines which of those are live.

### Context (why) ❌
> No dedicated "why this matters" field. `retrieval_hint` (counted above under anticipated queries) is a retrieval-vocabulary augmentation, and the reasoning behind a `decision` lives in its content text, not a separate column.

### Source attribution ✅
- `common/models/memory.py:30-38` — every row carries `tenant_id`, `fleet_id`, `agent_id`, `source_uri`, and `run_id`.
- `common/enrichment/constants.py:170` — `SERVER_RESERVED_MEMORY_TYPES = {"outcome", "rule", "insight"}`: types only the server's own flows may author, distinguishing machine-generated memories from agent writes at the boundary.
- Distinct authoring origins are separated in code: agent MCP/REST writes; Interviewer transcript synthesis (`README.md:574-580`); Forge (`core-api/src/core_api/services/forge/forge_service.py:679` — `"source": "forge"`); STM promotion (`core-api/src/core_api/pipeline/steps/search/inject_stm_context.py:91` — `"source": "stm"`); Broker installs, attributed under the `broker:<install>` ownership namespace (`README.md:614-621`, `core-api/src/core_api/mcp_server.py:297-300`).

### Origin + trust ✅
- `README.md:393` — four agent trust tiers control cross-fleet reads, writes and deletes.
- `core-api/src/core_api/services/trust_service.py:39-52` — `require_trust(tenant_id, agent_id, min_level)` is the shared gate for MCP and REST; unregistered callers fall back to `DEFAULT_TRUST_LEVEL`.
- `static/docs/integration-guide.md:47-48` — keystone authoring is tiered by origin: trust ≥ 1 to author your own `scope=agent` rule, ≥ 2 for `scope=fleet` / `scope=tenant` or another agent's.
- `common/models/memory.py:122-125` — `confidence` per claim, and `is_inferred` so a system-inferred memory "never silently overrides an explicit fact".

### Emotional ❌
> `sentiment` / `sentiment_score` appear only as candidate RDF predicates in `common/constants.py:250-251` (single-value predicate list). No sentiment or intensity field is extracted or stored per memory.

### Conflict surfacing ✅
- `README.md:402` — "Contradiction detection — RDF triple comparison + LLM semantic analysis detects conflicting memories and automatically supersedes them, with full contradiction chain tracking."
- `core-api/src/core_api/services/contradiction_detector.py` + `core-api/src/core_api/services/contradiction/` — the detector; `common/constants.py:52-58` sets `CONTRADICTION_SIMILARITY_THRESHOLD = 0.70` and an 8-candidate LLM check.
- `README.md:888` — `GET /memories/{id}/contradictions` surfaces the chain; `caura_insights` has a dedicated `contradictions` focus mode (`core-api/src/core_api/services/insights_service.py:325`).

### Layered memory ✅
- `core-api/src/core_api/routes/stm.py:1` + `core-api/src/core_api/providers/redis_stm.py:19-30` — a short-term memory tier (notes / bulletin, capped and TTL'd) distinct from long-term storage, with a documented "promote door" from STM into durable memories (`core-api/src/core_api/routes/stm.py:21-27`).
- `README.md:407` — Crystallization: "LLM merges near-duplicate memories into canonical atomic facts with full provenance", i.e. a derived layer above raw writes.
- `common/enrichment/_prompts.py:175-193` — `atomic_facts` fan-out: a composite write materialises child memories, each with its own embedding, under the parent.

### Time-travel ✅
- `common/models/memory.py:82-84,110-113` — `ts_valid_start` / `ts_valid_end` temporal windows and `supersedes_id` chains.
- `README.md:509,1122` / `static/docs/integration-guide.md:39` — `caura_manage op=lineage` walks a memory's supersession lineage; `common/models/memory_derivation.py:1-7` records which upstream memory produced each inferred memory, "enabling revalidation".
- `core-storage-api/src/core_storage_api/services/postgres_service.py:1834-1845` — search accepts a `valid_at` point in time and de-weights memories whose validity window has closed.
- `static/docs/integration-guide.md:40` — `caura_list` supports `include_deleted` at trust 3, so soft-deleted history stays queryable.

### Schema fields (count: ~28) ✅
- `common/models/memory.py:30-128` — column-level fields excluding auto IDs/timestamps: `tenant_id`, `fleet_id`, `agent_id`, `memory_type`, `content`, `embedding`, `weight`, `source_uri`, `run_id`, `metadata`, `title`, `content_hash`, `embedded_content_hash`, `expires_at`, `subject_entity_id`, `predicate`, `object_value`, `ts_valid_start`, `ts_valid_end`, `status`, `visibility`, `recall_count`, `confidence`, `is_inferred`, `scope` (25).
- `common/enrichment/_prompts.py:104-203` — enrichment additionally persists `summary`, `tags`, `contains_pii`, `pii_types`, `retrieval_hint`, `business_relevance` into `metadata` (6 more, of which `tags`/`summary` overlap no column) → ~28-31 distinct structured fields per entry.

---

## Search & Retrieval

### Full-text ✅
- `core-storage-api/src/core_storage_api/services/postgres_service.py:1679-1692` — PostgreSQL FTS: `plainto_tsquery('english', query)` scored with `ts_rank_cd(Memory.search_vector, …)`, scaled by a tunable `fts_weight`.
- `common/models/memory.py:72` — `search_vector` TSVECTOR column, title-weighted by migration `034_memories_search_vector_title_weighting`.

### Semantic/vector ✅
- `common/models/memory.py:35` — `embedding = mapped_column(Vector(VECTOR_DIM))` (pgvector, 1024-dim since v2.0).
- `README.md:400` — pgvector semantic similarity as the first-stage retrieval.

### Hybrid (BM25+Vec) ✅
- `README.md:400` — "Hybrid search — pgvector semantic similarity + full-text keyword matching + knowledge graph expansion (up to 2 hops), ranked by composite score of similarity, importance, freshness, and graph boost".
- `core-storage-api/src/core_storage_api/services/postgres_service.py:1642-1745` — the composite blend (vector cosine, scaled FTS rank, weight, per-type freshness decay via `TYPE_DECAY_DAYS`, graph boost) with per-agent tunable weights.
- `common/ranking/__init__.py:1-8` — optional second-stage reranking (`RANK_PROVIDER`: noop / local cross-encoder / remote) over the fused candidate pool.

### Deep (incl. thinking) ❌
> The Interviewer synthesizes an agent's transcript/event trail into typed memories (`README.md:560-600`), but reasoning traces themselves are not stored or searchable — only the synthesized memories are.

### Code graph ❌
> No Tree-sitter/AST indexing anywhere in the repo. The knowledge graph is an entity/relation graph over people, orgs, locations and concepts (`README.md:401`), not code structure.

### Docs search ❌
> `POST /ingest/preview|commit` ingests URLs and documents into atomic-fact memories (`core-api/src/core_api/services/ingest_service.py:1`), and `caura_doc op=search` does semantic search over JSON document collections — but there is no dedicated framework/API-documentation index separate from ordinary memory/document search.

### Fact metadata query ✅
- `core-api/src/core_api/mcp_server.py:2211-2216` — `caura_list` filters on `memory_type`, `status`, `agent_id`, `min_weight`, `created_after`, `created_before`, with sort and cursor pagination.
- `README.md:510` — "`caura_list` | Filter by type/status/agent/weight/date, sort, cursor-paginate".
- `README.md:949` — `POST /documents/query` does field-equality queries over JSONB document collections.

### Timeline view ✅
- `core-api/src/core_api/mcp_server.py:2215-2216` — `created_after` / `created_before` ISO-8601 bounds, sortable by `created_at` (`static/docs/integration-guide.md:40`).
- `core-storage-api/src/core_storage_api/services/postgres_service.py:1834-1845` — point-in-time `valid_at` retrieval against each memory's validity window.

### Search modes (count: 6) ✅
- `README.md:1120-1127` / `static/docs/integration-guide.md:36-48` — (1) `caura_recall` hybrid semantic + keyword + graph recall, (2) `caura_recall include_brief=true` / `POST /recall` LLM-summarised brief, (3) `caura_list` non-semantic filtered enumeration, (4) `caura_doc op=search` semantic search over document collections, (5) `caura_doc op=query` field-equality document query, (6) `caura_entity_get` / `GET /graph` knowledge-graph lookup and traversal.

### Data sources (count: 5) ✅
- Searchable stores: memories (`POST /search`), documents incl. the `skills` collection (`caura_doc`), knowledge-graph entities + relations (`GET /entities`, `GET /graph`), STM notes/bulletin (`core-api/src/core_api/routes/stm.py`), and keystone governance rules (`GET /keystones`). See `README.md:1141-1149`.

---

## Knowledge Lifecycle

### Decay/forgetting ✅
- `common/constants.py:62-79` — `TYPE_DECAY_DAYS`, a per-type freshness half-life (preference 365d, decision 180d, fact 120d, episode 45d, task/action 30d, …).
- `core-storage-api/src/core_storage_api/services/postgres_service.py:1721` — those windows are applied as a freshness factor in the ranking expression on every search.
- `core-operations/src/core_operations/app.py:110-121` — `lifecycle-archive-stale` and `lifecycle-purge-soft-deleted` daily ticks remove or archive automatically.

### Supersede/replace ✅
- `common/models/memory.py:110-113` — `supersedes_id` self-FK; `README.md:402` — contradictions "automatically supersede" the losing memory "with full contradiction chain tracking".
- `README.md:509,1122` — `caura_manage op=lineage`; `common/models/memory_derivation.py:1-7` — per-edge derivation rows for inferred memories.

### Contradiction detection ✅
- `README.md:402` and `core-api/src/core_api/services/contradiction_detector.py` — RDF triple comparison plus LLM semantic analysis, triggered above `CONTRADICTION_SIMILARITY_THRESHOLD = 0.70` (`common/constants.py:52-54`).

### Quarantine ✅
- `common/constants.py:14-23` — `LIVE_MEMORY_STATUSES = ("active", "confirmed", "pending")`: a memory transitioned to `archived` / `outdated` / `conflicted` stays stored but drops out of retrieval.
- `README.md:509,887` — `caura_manage op=transition` (and `PATCH /memories/{id}/status`) performs the transition. Note this is per-memory / bulk rather than a single "quarantine this session" switch.
- `core-api/src/core_api/routes/skills_inbox.py:13` — skills have an explicit `quarantined` state (`staged → quarantined`, security review) that keeps the row but blocks delivery.

### Auto-resolution ✅
- `core-operations/src/core_operations/app.py:104-121` — daily `lifecycle-archive-expired` (past `expires_at` / `ts_valid_end`) and `lifecycle-archive-stale` ticks, plus `lifecycle-purge-soft-deleted`.
- `README.md:407` — "8-status lifecycle automation retires stale data".

### Trust model ✅
- `README.md:393` — four trust tiers gating cross-fleet reads/writes/deletes; `core-api/src/core_api/services/trust_service.py` enforces it on both surfaces.
- `common/models/memory.py:115-125` — `confidence` and `is_inferred` so "weak evidence must not delete strong" and an inferred memory "never silently overrides an explicit fact".
- `static/docs/integration-guide.md:326-341` — the 4-tier table, auto-registration at trust 1, admin key bypass.

### Explicit forget ✅
- `README.md:886,889` — `DELETE /memories/{id}` (soft delete) and bulk soft-delete; `README.md:509` — `caura_manage op=delete | bulk_delete`.
- `core-operations/src/core_operations/app.py:116-121` — `lifecycle-purge-soft-deleted` hard-deletes afterwards.

---

## Extraction Pipeline

### Auto-extraction ✅
- `README.md:560-601` — The Interviewer: on a schedule it reads an agent's durable work trail (Claude Code `~/.claude/projects`, Cursor agent transcripts, or the plugin's node-local buffer) and synthesizes typed memories — `worked_on → episode`, `decisions → decision`, `outcomes → outcome`, `blockers → task`, `open_questions → fact`, `preferences_learned → preference` — with no `save` call from the agent.
- `plugin/src/context-engine.ts:1292-1294` — the OpenClaw plugin's `afterTurn` hook auto-writes turn summaries by default (`CAURA_AUTO_WRITE_TURNS`, `README.md:1166`).
- `README.md:399` — every write is auto-classified and enriched (type, title, summary, tags, weight, PII flags, entities) from a single `content` field.

### Content-aware preprocessing ✅
- `core-api/src/core_api/services/ingest_chunking.py:1-45` — "Block-based structure-aware chunker": replaces "the first 50k chars of any document as one big blob" with a typed-block parse per format (markdown AST via markdown-it-py, plaintext paragraph split, tag-stripped HTML), greedy-packed into heading-bounded sections at `SECTION_SOFT_TOKENS = 2_000` / `SECTION_HARD_TOKENS = 3_000`, with a `DOC_HARD_TOKEN_LIMIT = 100_000` refuse threshold.

### Deduplication ✅
- `common/models/memory.py:151-160` — a partial unique index enforcing "one LIVE row per (tenant, fleet, agent, content_hash)".
- `README.md:407` — Crystallization "merges near-duplicate memories into canonical atomic facts with full provenance"; `core-api/src/core_api/services/crystallizer_service.py` with `CRYSTALLIZER_DEDUP_THRESHOLD` / `_NEIGHBORS` / `_BATCH_SIZE`, plus `core-api/src/core_api/services/dedup_judge.py` as the LLM adjudicator.
- `README.md:401` — entity resolution auto-merges duplicate entities above 0.85 cosine.
- `core-api/src/core_api/config.py:53` — a `CheckSemanticDuplicate` write-path step.

### Quality refinement ✅
- `common/enrichment/service.py:145-175` + `common/enrichment/constants.py:164-199` — `_validate_enrichment` post-pass: clamps/normalises LLM output, truncates `retrieval_hint`, and demotes server-reserved or deprecated types back to `fact`.
- `common/models/memory.py:116-122` — per-claim `confidence` scoring.
- `README.md:402` — contradiction check runs as part of the write pipeline.

### Narrative generation ✅
- `README.md:508,1120` — `caura_recall` with `include_brief` returns an LLM-summarised brief; `README.md:892` — `POST /recall` "Search + LLM summarization — returns context paragraph + source memories".
- `README.md:395` — daily and weekly per-agent activity digests, read back via `GET /api/v1/reports/agent-activity`; `core-api/src/core_api/services/agent_digest.py`.
- `README.md:940-941` — crystallization reports (`GET /crystallize/reports`, `/crystallize/latest`).

### Clustering ✅
- `README.md:531-537` — Forge "mines memory + outcome signals, clusters repeated successful procedures, and distills them into skill candidates".
- `core-api/src/core_api/services/session_trace.py:1-20` — session traces are the input to Forge's "cluster + fingerprint step (SF-103)".
- `core-api/src/core_api/services/insights_service.py:36,53` — the `discover` focus mode returns clusters of related memories.

### Recurrence detection ✅
- `README.md:531-537` — Forge detects *repeated* successful procedures across sessions and promotes them into skills.
- `README.md:924` — `caura_insights` focus modes include `patterns` (emerging themes) and `failures` (failure patterns); `core-api/src/core_api/services/insights_service.py:3-4` — "surface contradictions, failure patterns, stale knowledge, cross-agent divergence, emerging themes".
- `README.md:406` — the Karpathy Loop "auto-generates preventive `rule`-type memories on failure" so a repeat mistake is caught fleet-wide.

### Persona extraction ❌
> `preference` is a first-class memory type with a 365-day decay window (`common/enrichment/constants.py:28`, `common/constants.py:64`) and the Interviewer writes a `preferences_learned → preference` section (`README.md:576-580`), but those stay individual memories — there is no aggregated, persistent persona/profile model per user or agent.

---

## Platform Support

### Claude Code ✅
- `README.md:495-499` — `claude mcp add --transport http -s user caura http://localhost:8000/mcp --header "X-API-Key: standalone"`.
- `README.md:627-648` — an installable usage skill: `curl -s "http://localhost:8000/api/v1/install-skill" | bash` → `~/.claude/skills/memclaw/SKILL.md`.
- `README.md:584-590` — the `caura-interviewer` CLI ships a Claude Code transcript parser (`~/.claude/projects`).

### Codex ✅
- `README.md:668` — `?agent=codex` installs the skill to `~/.agents/skills/<skill>/SKILL.md`; `static/docs/integration-guide.md:99-111`.

### OpenCode ❌

### Gemini CLI ✅
- `README.md:605-609` — the Caura Broker daemon "connects coding agents — Claude Code, Codex, Cursor, Gemini — to Caura". (Broker ships from a separate repo; its server-side identity plumbing lives here — `README.md:614-621`.)

### Copilot ❌

### Cursor ✅
- `README.md:501` — "**Cursor** — Settings > MCP Servers > Add Server"; `static/docs/integration-guide.md:85` gives the exact server config.
- `README.md:584-590` — Interviewer disk-parser ships for Cursor (`~/.cursor/…/agent-transcripts`).

### Windsurf ✅
- `README.md:412` — "Connect Claude Desktop, Claude Code, Cursor, Windsurf, or any MCP client with a URL and API key"; `README.md:1277` repeats it in the FAQ.

### OpenClaw ✅
- `README.md:320-338` — one-line plugin install against managed or self-hosted Caura; "The plugin claims the OpenClaw `memory` slot (replacing `memory-core`) and exposes the same 12 MCP tools."
- `plugin/src/` — the TypeScript plugin (tools, agent auth, context engine, 60s heartbeat, skill reconciler).

### Hermes ❌
> `README.md:587-588` lists Hermes as *planned* for the Interviewer disk-parser, not shipped.

### pi/omp ❌

### Antigravity ❌

---

## Benchmarks

### LoCoMo ✅
- Score: `77.6%` accuracy (LLM-judge)
- `BENCHMARKS.md:13-16` and `README.md:448-451` — published table; last run 2026-04-19.

### LongMemEval ✅
- Score: `72.5%` accuracy (LLM-judge)
- `BENCHMARKS.md:13-16` and `README.md:448-451`.

### PersonaMem ❌
- Score: `—`

### Token reduction ✅
- Score: `96.6%` (LoCoMo) / `98.2%` (LongMemEval) vs full-context baseline
- `BENCHMARKS.md:17` and `README.md:451` — "Token savings vs full context"; `BENCHMARKS.md:33-36` defines the baseline as "the same prompt with the full prior conversation inlined".

### Methodology open ✅
- `BENCHMARKS.md:28-42` — what is measured and how (LLM judge over the retrieval-then-answer pipeline, token ratio vs full-context baseline, warm-cache p50/p95 of `POST /api/v1/search`).
- `BENCHMARKS.md:60-79` — six-step reproduction against the public LoCoMo / LongMemEval datasets, with the caveat that the end-to-end accuracy harness is not yet bundled.
- `scripts/benchmark_rerank_locomo.py` — the bundled reranking benchmark; `scripts/latency_test.py` — the latency harness (`README.md:1088-1101`).
