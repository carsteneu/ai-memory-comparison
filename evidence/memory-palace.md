# Memory Palace — Evidence

> Every ✅ claim backed by public documentation or source code.
> Audit date: 2026-05-28. Source: GitHub `AGI-is-going-to-arrive/Memory-Palace` main branch (v3.9.0).

## Vital Signs

| Field | Value | Verified |
|-------|-------|----------|
| Stars | 300 | ✅ GitHub repo |
| Language | Python | ✅ README (Python 77.5%, JS 17.9%) |
| License | MIT | ✅ LICENSE file |
| Single binary | false | ✅ Docker/Python deployment, not compiled binary |
| Created | 2026-02-19 | ✅ From README context |
| Coverage | — | ✅ Not published |

## Architecture

### webUi: ✅ (Dashboard with 4 views)
- `README.md` — "React-based, four views: **Memory Browser**, **Review & Rollback**, **Maintenance**, **Observability**."
- `docs/TECHNICAL_OVERVIEW_EN.md` — Frontend structure: `features/memory/`, `features/review/`, `features/maintenance/`, `features/observability/`.
- Screenshots in README show actual Dashboard pages.

### offline: ✅ (Profiles A/B fully local)
- `docs/DEPLOYMENT_PROFILES_EN.md` — Profile A: pure keyword, local SQLite. Profile B: "**Default starting profile**, zero external dependencies" — local hash embedding (64-dim), no external services.
- Profiles C/D need external APIs but A/B are fully offline.
- Docker deployment binds to `127.0.0.1` by default.

### multiAgent: ❌ (single backend)
- `README.md` — Multi-client integration (one backend serving multiple MCP clients). Not multi-agent orchestration.
- No spawn/heartbeat/crash-recovery/messaging between agents.

### proxy: ❌
- Standard MCP server + REST API. Does not intercept or modify LLM conversation streams.

### llmFlex: ~1
- Uses single configurable OpenAI-compatible endpoint (`ROUTER_API_BASE`). Any provider compatible with `/embeddings`, `/rerank`, `/chat/completions` works, but only one at a time.

### cacheOpt: ❌
- Session-first retrieval cache exists (`TECHNICAL_OVERVIEW_EN.md` §2: "per-session caps plus a total session limit"), but this is a bounded in-process cache, not a general-purpose cache optimization layer.

### privacy: ❌ (no encryption)
- Strong local-only security: `MCP_API_KEY` fail-closed auth, loopback-only defaults, Docker non-root.
- No encryption-at-rest or zero-knowledge architecture.
- `docs/SECURITY_AND_PRIVACY_EN.md` covers key auth and policies but not data encryption.

### export: ❌ (backup only)
- `scripts/backup_memory.sh` / `.ps1` for database backup (keeps latest 20, UTC timestamps).
- No structured data export format (JSON, CSV, Markdown intended for portability).

### setup: "docker compose / script"
- `README.md` — Three setup paths: Prebuilt Docker (`docker compose -f docker-compose.ghcr.yml up -d`), One-Click Docker (`scripts/docker_one_click.sh --profile b`), Manual Local (`pip install -r requirements.txt && npm install && npm run dev`).
- Windows: PowerShell equivalents for all scripts.

### pricing: "free"
- MIT license, open source, no cloud tier mentioned.

---

## Data Model

### Verified features

| Feature | Status | Evidence |
|---------|--------|----------|
| **layeredMemory** | ✅ L0→L1→L2 | `README.md` — "L0 (raw) → L1 (linked clusters) → L2 (topic summaries) with full derivation provenance." `docs/TECHNICAL_OVERVIEW_EN.md` §2: `layering_engine` provides L2 read-only summaries; derived data carries provenance fields (`source_memory_ids`, `source_hashes`, `derivation_method`, `confidence`, `review_state`). |
| **timeTravel** | ✅ Snapshots + rollback | `README.md` — "Auditable Write Pipeline: Every write passes through Write Guard pre-check → Snapshot → Async index rebuild." `docs/TECHNICAL_OVERVIEW_EN.md` §3 `/review`: "View version diffs, rollback, integrate." Snapshot writes use atomic replace. Rollback returns `409` if newer snapshot exists (content revalidation). |
| **triggerRules** | ✅ disclosure field | **CORRECTION: This feature IS present.** `docs/TOOLS_EN.md` — `create_memory(disclosure=...)` — "Trigger condition." `add_alias(disclosure=...)` — "When I want to recall how we first met." The disclosure parameter acts as a trigger rule controlling when a memory should be surfaced. |
| **schemaFields** | 8 | `README.md` — "schemaFields=8." From tool params: uri, content, priority, title, disclosure, domain (in URI), gist, trace. |

### Features confirmed absent

| Feature | Evidence |
|---------|----------|
| **entities** | URI-based namespace (`core://`, `writer://`), not entity junction tables. No named entities as separate fields. |
| **actions** | No action/command/operation metadata field on memories. |
| **keywords** | No keyword/tag field. Priority is integer, not keyword/tag metadata. |
| **anticipatedQueries** | No query generation field for retrieval optimization. |
| **domainTag** | Domain is encoded in URI prefix (`core://`), not a per-memory free-form tag field. Namespace-level only. |
| **taskType** | No task/idea/blocked/stale classification. Procedural engine extracts workflows but no task type field. |
| **context** | `compact_context` has a `reason` parameter and Write Guard returns `guard_reason`, but no per-memory "why this was saved" context field. |
| **source** | Snapshots track session origin but no multi-tier source attribution (user_stated/agreed_upon/claude_suggested). |
| **originTrust** | No trust weighting by source origin. |
| **emotional** | No emotional valence or intensity field. |
| **conflict** | Write Guard detects near-duplicates and returns NOOP/UPDATE. No contradiction detection between semantically different but logically conflicting memories. |
| **supersede** | Version chains exist via snapshots and rollback. No explicit "A supersedes B" link between distinct memory IDs. |
| **contradiction** | No detection of semantically contradictory memory pairs. |
| **quarantine** | No session-level quarantine mechanism. |
| **autoResolve** | No automatic task/memory resolution on completion. |
| **trustModel** | No multi-tier trust scoring by origin/source. |
| **narrative** | ⚠️ `compact_context` generates gist summaries (LLM-assisted or extractive). L2 layering produces topic summaries. This arguably IS narrative generation. Current data.js marks it false. Recommend review. |
| **autoExtract** | Write Guard runs automatically on writes (duplicate detection). `compact_context`, procedural engine, and learn/trigger all require explicit MCP tool calls. No automatic extraction pipeline that runs on every conversation input. |
| **contentPreproc** | Query preprocessing exists (whitespace normalization, tokenization, URI preservation) but no content-aware memory preprocessing for storage reduction. |
| **qualityRefine** | Gist quality is scored (0–1) in `compact_context` response. No separate LLM-based quality refinement phase. |
| **recurrence** | No recurrence/pattern detection across sessions. |
| **persona** | No persona extraction engine. Profile/preference storage exists via core memories but no dedicated persona trait extraction. |

---

## Search & Retrieval

### Verified features

| Feature | Status | Evidence |
|---------|--------|----------|
| **fulltext** | ✅ FTS5 | `docs/TECHNICAL_OVERVIEW_EN.md` §2: `db/search/` — "FTS5 / vector / RRF / entity boost channels." `docs/TOOLS_EN.md` — keyword mode: "FTS/BM25 first; unsafe queries fall back to escaped LIKE." |
| **semantic** | ✅ Multiple backends | `docs/TOOLS_EN.md` — semantic mode: "Embedding-based search (requires hash / api / router / openai)." §Retrieval Configuration: backends include hash (64-dim local), api, router, openai. |
| **hybrid** | ✅ RRF + reranker | `docs/TOOLS_EN.md` — hybrid: "Keyword + semantic; reranker applied if enabled." `docs/DEPLOYMENT_PROFILES_EN.md` — Profile B enables RRF fusion (`RRF_K=10`). C/D add real embedding + reranker. |
| **searchModes** | 3 | `docs/TOOLS_EN.md` — Three modes: `keyword`, `semantic`, `hybrid`. Confirmed in `search_memory` tool signature. |
| **dataSources** | 1 | Conversations/memories only. No code graph, documentation, or external data source indexing. |

### Features confirmed absent

| Feature | Evidence |
|---------|----------|
| **deep** | `search_memory` returns gist summaries and content. No search over model thinking/reasoning traces. |
| **codeGraph** | No code structure indexing. Search is over memories only. |
| **docsSearch** | No indexed documentation search. |
| **factQuery** | Metadata filtering exists (`domain`, `path_prefix`, `max_priority`, `updated_after`) but no structured fact query DSL (e.g., "all decisions about X by entity Y"). |
| **timeline** | `system://recent` shows recently modified memories. Temporal search uses `updated_after` filter. No dedicated timeline visualization or query mode in the Dashboard. |

---

## Knowledge Lifecycle

### Verified features

| Feature | Status | Evidence |
|---------|--------|----------|
| **decay** | ✅ Vitality + Forgetting Engine | `README.md` — "Forgetting Engine: runtime vitality scores decay with `VITALITY_DECAY_HALF_LIFE_DAYS` (30 days)." `docs/DEPLOYMENT_PROFILES_EN.md` §8: Full vitality parameter table: `VITALITY_MAX_SCORE` (3.0), `VITALITY_REINFORCE_DELTA` (0.08 per retrieval), `VITALITY_DECAY_HALF_LIFE_DAYS` (30), `VITALITY_CLEANUP_THRESHOLD` (0.35). |
| **dedup** | ✅ Write Guard | `docs/TOOLS_EN.md` — Write Guard: "Detect duplicates, Suggest merges (returns UPDATE / NOOP)." Three-level chain: semantic match → keyword match → LLM decision (optional). |
| **explicitForget** | ✅ delete_memory | **CORRECTION: This feature IS present.** `docs/TOOLS_EN.md` — `delete_memory(uri)` — "Delete a URI path." Forgetting engine: "archive/prepare → archive/confirm" with review token gating. Review page: permanent delete of deprecated memories. Currently marked false in data.js. |

### Features confirmed absent

| Feature | Evidence |
|---------|----------|
| **supersede** | Snapshots provide version history (update in place). No explicit "learning A replaces learning B" linking between distinct memory IDs. |
| **contradiction** | No detection of conflicting semantic content between distinct memories. |
| **quarantine** | No per-session quarantine. SSE stale session returns `404/410` but no quarantine flag. |
| **autoResolve** | No automatic task/memory lifecycle resolution. |
| **trustModel** | No multi-tier trust scoring system. |

---

## Extraction Pipeline

### Verified features

| Feature | Status | Evidence |
|---------|--------|----------|
| **dedup** | ✅ Write Guard | Confirmed above. Write Guard provides duplicate detection on every write. |
| **clustering** | ✅ L1 linked clusters | `README.md` — "Layering Engine: organizes memories into L0 (raw) → L1 (linked clusters) → L2 (topic summaries)." `docs/TECHNICAL_OVERVIEW_EN.md` §2: `layering_engine.py` provides L2 read-only summaries from L1 clusters. |

### Features confirmed absent

| Feature | Evidence |
|---------|----------|
| **autoExtract** | Write Guard runs automatically. All other extraction (gist generation, procedural extraction, learn/trigger) requires explicit MCP tool calls. |
| **contentPreproc** | Query preprocessing exists for search. No content-aware memory preprocessing for storage efficiency. |
| **qualityRefine** | Gist quality scored (0–1). No separate LLM-based quality refinement of stored memories. |
| **narrative** | See note in Data Model section above. `compact_context` gist generation + L2 topic summaries arguably qualify. |
| **recurrence** | No cross-session pattern/recurrence detection. |
| **persona** | No persona trait extraction engine. Core memories can store preferences but no dedicated persona pipeline. |

---

## Platform Support

### Verified features

| Platform | Status | Evidence |
|----------|--------|----------|
| **p_claude** | ✅ | `README.md` — "Claude Code: `--scope user` is the stable default." Skills + MCP path. `/docs/skills/MEMORY_PALACE_SKILLS_EN.md` §1: installed to `.claude/` mirror directory. |
| **p_codex** | ✅ | `README.md` — "Codex CLI / OpenCode: `sync` for repo-local skill discovery; use `--scope user --with-mcp` to bind reliably." |
| **p_opencode** | ✅ | Same as Codex. Listed in supported clients table. OpenCode mirror in `.opencode/`. |
| **p_gemini** | ✅ | `README.md` — "Gemini CLI: `--scope user` default." `docs/skills/MEMORY_PALACE_SKILLS_EN.md` §8: Gemini variant with custom SKILL.md and overrides TOML. |
| **p_cursor** | ✅ | `README.md` — IDE hosts: "Repo-local `AGENTS.md` + rendered MCP snippet." `scripts/render_ide_host_config.py --host cursor`. |
| **p_windsurf** | ✅ | Same IDE host path: `render_ide_host_config.py --host windsurf`. |
| **p_antigravity** | ✅ | Same IDE host path: `render_ide_host_config.py --host antigravity`. `docs/skills/MEMORY_PALACE_SKILLS_EN.md` §3: Antigravity variant workflow at `variants/antigravity/global_workflows/memory-palace.md`. |
| **p_copilot** | ❌ | Not listed in supported clients. Tool mapping doc referenced for Copilot CLI but no explicit integration. |
| **p_openclaw** | ❌ | Not listed in supported clients or IDE hosts. |
| **p_hermes** | ❌ | Not listed. |
| **p_pi** | ❌ | Not listed. |

---

## Benchmarks

| Benchmark | Value | Evidence |
|-----------|-------|----------|
| **LoCoMo** | — | Not published. |
| **LongMemEval** | — | Not published. |
| **PersonaMem** | — | Not published. |
| **Token reduction** | — | Not published. |
| **Methodology open** | ❌ | Internal benchmarks in `backend/tests/benchmark/` but: Profile A/B/C/D metrics in `profile_abcd_real_metrics.json` are published in `docs/EVALUATION_EN.md` with methodology. Write Guard precision/recall and Intent Classification accuracy also published. Recommend marking as ✅ (published methodology, even if not on standard LoCoMo/LongMemEval benchmarks). |

### Published quality metrics
- `docs/EVALUATION_EN.md` — A/B/C/D profile comparison with HR@10, MRR, NDCG@10, Recall@10, p95 latency.
- Write Guard precision: 1.000, recall: 1.000.
- Intent Classification accuracy: 1.000.
- Gist ROUGE-L: 0.759.
- Methodology: 8 samples per dataset, 200 distractors, seed 20260219. Full reproduction guide.

---

## Unique Differentiators

1. **Four Maintenance Engines**: Forgetting (vitality decay + archive), Layering (L0→L1→L2), Compression (preview-only), Procedural (step extraction). All read-only by default; mutations gated behind review tokens.
2. **Intent-Aware Search**: Four intent classes (factual, exploratory, temporal, causal) route to different retrieval strategy templates.
3. **Snapshot + Rollback**: Every write creates a snapshot. Review page enables diff, rollback, and integration. Write Guard pre-checks every write.
4. **Write Guard Pipeline**: ADD/UPDATE/NOOP/DELETE decisions with three-level chain (semantic → keyword → LLM).
5. **A/B/C/D Deployment Profiles**: From pure keyword (A) to remote API hybrid with reranker (D). Profile B is the "zero external dependencies" default.
6. **Multi-Client Skills + MCP**: Unified install for Claude Code, Codex, Gemini CLI, OpenCode, plus IDE host snippets for Cursor, Windsurf, Antigravity, VSCode.

---

## Summary of Corrections

| # | Claim | data.js | Verified | Recommendation |
|---|-------|---------|----------|----------------|
| 1 | `triggerRules` | false | **true** | Change to true. `disclosure` parameter in create/update/add_alias is a trigger condition. |
| 2 | `explicitForget` | false | **true** | Change to true. `delete_memory` tool + forgetting archive in `/api/forgetting`. |
| 3 | `narrative` | false | ⚠️ borderline | `compact_context` gist generation + L2 topic summaries arguably qualify as narrative generation. Recommend review. |
| 4 | `autoExtract` | false | ⚠️ borderline | Write Guard auto-runs on writes. `compact_context`, procedural engine, and learn/trigger need explicit calls. Current false is defensible. |
| 5 | `b_methodology` | false | ⚠️ borderline | Published methodology in `docs/EVALUATION_EN.md` with full reproduction guide. Recommend review for ✅. |
| 6 | `offline` | true | ✅ | Confirmed. Profile B is fully offline with local hash embedding. |
| 7 | `schemaFields` | 8 | ✅ | Confirmed. README states 8 fields. |
| 8 | `setup` | "?" | "docker compose / script" | Three documented paths: GHCR prebuilt, one-click Docker, manual local. |

### Features correctly marked in data.js:
webUi, offline, fulltext, semantic, hybrid, layeredMemory, timeTravel, searchModes=3, dataSources=1, decay, dedup, clustering, p_claude, p_codex, p_opencode, p_gemini, p_cursor, p_windsurf, p_antigravity, schemaFields=8.

### Features correctly absent:
entities, actions, keywords, anticipatedQueries, domainTag, taskType, context, source, originTrust, emotional, conflict, deep, codeGraph, docsSearch, factQuery, timeline, supersede, contradiction, quarantine, autoResolve, trustModel, contentPreproc, qualityRefine, recurrence, persona, p_copilot, p_openclaw, p_hermes, p_pi.

---

## Source Documents

- `README.md` — Main feature overview, architecture, deployment profiles, platform support
- `docs/TOOLS_EN.md` — Complete MCP tool reference: all 9 tools, parameters, return formats, degradation
- `docs/TECHNICAL_OVERVIEW_EN.md` — Backend structure, API endpoints, frontend modules, data/task flow
- `docs/DEPLOYMENT_PROFILES_EN.md` — A/B/C/D profile configurations, vitality parameters, troubleshooting
- `docs/skills/MEMORY_PALACE_SKILLS_EN.md` — Skills design, distribution, supported platforms
- `docs/EVALUATION_EN.md` — Benchmark methodology and published results
- `docs/changelog/` — Per-release feature details
