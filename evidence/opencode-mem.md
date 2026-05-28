# opencode-mem Audit

> **Evidence document** for ai-memory-comparison
>
> **Audit date:** 2026-05-28
> **Source:** [https://github.com/tickernelz/opencode-mem](https://github.com/tickernelz/opencode-mem)
> **Version:** 2.14.3 (257 commits, MIT license, TypeScript)
> **Evidence:** `"https://github.com/carsteneu/ai-memory-comparison/blob/main/evidence/opencode-mem.md"`

---

## Summary

opencode-mem is a mature, feature-rich OpenCode plugin for persistent AI agent memory. It uses local SQLite + USearch vector indexing with Xenova/Transformers embeddings. It is **substantially more capable** than the 3-field / 1-search-mode characterization suggests.

---

## 1. Verified Claims

| Claim | Status | Evidence |
|---|---|---|
| **offline** | ✅ Verified | Local SQLite storage (`shard-manager.ts`), no cloud dependency. All operations run locally. |
| **semantic** | ✅ Verified | Vector search via USearch (`usearch` v2.21.4 dep) + Xenova Transformers embeddings (`@xenova/transformers`). Cosine similarity scoring with content/tags weighted fusion (0.6/0.4). |
| **p_opencode** | ✅ Verified | OpenCode-native plugin via `@opencode-ai/plugin` v1.3.0, hooks: `chat.message` + `event`, tool: `memory`. |

---

## 2. Corrections to Claims

### schemaFields=3 → **At least 10 meaningful schema fields** (17 total columns)

The `memories` table has 17 columns:

| Column | Type | Purpose |
|---|---|---|
| id | TEXT | Unique memory ID |
| content | TEXT | Memory content |
| vector | BLOB | 384d embedding vector |
| tags_vector | BLOB | Tags embedding vector |
| container_tag | TEXT | Project/user scope identifier |
| tags | TEXT | Comma-separated tags |
| type | TEXT | Memory type (feature, bug-fix, etc.) |
| created_at | INTEGER | Unix timestamp |
| updated_at | INTEGER | Unix timestamp |
| metadata | TEXT | JSON blob (source, sessionID, reasoning, tool, captureTimestamp, promptId) |
| display_name | TEXT | Project display name |
| user_name | TEXT | Git user name |
| user_email | TEXT | Git user email |
| project_path | TEXT | Project path |
| project_name | TEXT | Project name |
| git_repo_url | TEXT | Git remote URL |
| is_pinned | INTEGER | Pin flag |

Plus the **metadata JSON** carries 6 additional fields: `source`, `tool`, `sessionID`, `reasoning`, `captureTimestamp`, `promptId`.

**Correction: schemaFields ≥ 10** (excluding vector blobs and timestamps as "structural"), or **17** if counting all columns.

---

### searchModes=1 → **At least 2 retrieval modes** (3 with session-ID lookup)

| Mode | How | In tool API |
|---|---|---|
| **Semantic/vector search** | USearch cosine similarity with content/tags fusion | `memory({ mode: "search", query: "..." })` |
| **Chronological listing** | SQL ORDER BY created_at DESC | `memory({ mode: "list", limit: N })` |
| **Session-ID lookup** | SQL WHERE metadata LIKE '%sessionID%' | Internal (compaction handler) |

The web UI adds tag-filtered browsing and paginated listing.

**Correction: searchModes ≥ 2.**

---

### webUi → **PRESENT** (claimed absent)

Full-featured web UI at `http://127.0.0.1:4747`:
- **Memory explorer** with search, pagination, tag filtering, pinning
- **Project Memory Timeline** visualization
- **User Profile Viewer** with preferences, patterns, workflows, changelog/snapshot history
- **API endpoints**: `/api/memories`, `/api/search`, `/api/stats`, `/api/cleanup`, `/api/deduplicate`, `/api/user-profile`, `/api/migration/*`
- Built-in web server with port takeover, health checks, multi-instance coordination
- Frontend: 40KB `app.js`, 24KB `styles.css`, i18n support (`i18n.js`)

**Correction: webUi IS present — full CRUD dashboard.**

---

### source attribution → **PRESENT** (claimed absent)

`MemoryMetadata.source` enum: `"manual"` | `"auto-capture"` | `"import"` | `"api"`. Stored in the metadata JSON blob on every memory. Injected by the tool handler or auto-capture pipeline.

**Correction: source IS present (4-tier).**

---

### explicitForget → **PRESENT** (claimed absent)

`memory({ mode: "forget", memoryId: "mem_..." })` → `memoryClient.deleteMemory()` → `DELETE FROM memories WHERE id = ?`. Also web UI bulk-delete at `/api/memories/bulk-delete`.

**Correction: explicitForget IS present.**

---

### dedup → **PRESENT** (claimed absent)

Web API endpoint `/api/deduplicate` + `handleRunDeduplication()` handler. README claims "smart deduplication." The exact dedup algorithm is in `api-handlers.ts` (not fetched in this audit — verified endpoint exists).

**Correction: dedup IS present.**

---

### persona → **PRESENT** (claimed absent)

- `performUserProfileLearning()` triggered on session idle
- `UserProfileManager` with create/update/merge/versioning
- Profile data: `preferences[]`, `patterns[]`, `workflows[]`
- Web UI: User Profile Viewer, changelog history, snapshot viewer, refresh
- `memory({ mode: "profile" })` for explicit preference writes
- LLM-powered extraction: "automatic user profile learning"
- User profile analysis interval configurable (`userProfileAnalysisInterval`)

**Correction: persona IS present (preferences + patterns + workflows).**

---

### timeline → **PRESENT (visual only)** (claimed absent)

The web UI has a "Project Memory Timeline" visualization (README screenshots). However, there is **no temporal search API** (since/before parameters, time-range queries). The timeline is display-only: memories sorted by `created_at` with no time-travel query capability.

**Correction: timeline IS present as visualization, absent as search capability.**

---

### context (why) → **PARTIAL** (claimed absent)

The `reasoning` field in metadata captures the LLM's reasoning during auto-capture. However, there is no structured "context/why" field in the schema like engram's dedicated "Why" field. It's stored as a free-text string inside the JSON metadata blob alongside other fields.

**Assessment: minimal context support (free-text reasoning in metadata JSON).**

---

## 3. Verified Absent (no correction needed)

### Data Model
- **entities** — No entity junction table. Tags are strings, not structured entities.
- **actions** — No action metadata.
- **keywords** — No keyword junction table (tags ≠ keyword metadata search).
- **anticipatedQueries** — Not present.
- **triggerRules** — Not present.
- **domainTag** — No domain classification (code/marketing/legal/finance/general).
- **taskType** — The `type` field is a free-form string, not a structured task-type enum (task/idea/blocked/stale).

### Search
- **fulltext** — SQLite is used but no FTS5 table configured. No BM25. The only text matching is exact substring matching on tags during vector search scoring.
- **hybrid** — No BM25 + vector fusion (RRF or otherwise). Pure vector search with optional tag-exact-match boost.
- **deep** — No deep search (no raw thinking/conversation content search).
- **codeGraph** — No Tree-sitter or code graph. No code navigation tools.
- **docsSearch** — No documentation indexing.
- **factQuery** — No metadata query API (entity=, action=, keyword=).

### Lifecycle
- **decay** — No Ebbinghaus or time-based forgetting.
- **supersede** — Add-only model. No update/replace/supersede chains.
- **contradiction** — No conflict detection.
- **quarantine** — No session quarantine.
- **autoResolve** — No TTL-based auto-resolution.
- **trustModel** — No trust tiering or origin-weighted scoring (source field exists but no trust multiplier applied).
- **layeredMemory** — Single flat memory table. No L0→L3 pyramid or temporal layers.
- **timeTravel** — No session replay, no version chains, no temporal search filters.

### Extraction
- **contentPreproc** — `stripPrivateContent` removes `<private>...</private>` tags only. Not content-aware quality preprocessing.
- **qualityRefine** — Single-pass LLM summary. No multi-phase refinement.
- **narrative** — No narrative generation.
- **clustering** — Not present.
- **recurrence** — Not present.

### Platform
- **multiAgent** — No multi-agent orchestration (spawn, heartbeat, messaging, crash recovery).

### Trust & Quality
- **originTrust** — No trust scoring tiers (source field exists but no multiplier applied to search).
- **emotional** — No emotional scoring dimension.
- **conflict** — No conflict detection or surfacing.

---

## 4. Additional Capabilities (not in claim list)

These were discovered during source audit and are worth noting for the comparison:

| Feature | Detail |
|---|---|
| **Compaction memory injection** | On `session.compacted` event, injects recent memories back into context. Configurable via `compaction.memoryLimit`. |
| **Chat message injection** | On `chat.message` hook, prepends project memories to first user message. Configurable: `injectOn: first/always`, `excludeCurrentSession`, `maxAgeDays`. |
| **Privacy scrubbing** | `<private>...</private>` tag stripping before storage. Fully-private content blocked. |
| **Language detection** | `franc-min` for auto language detection; `autoCaptureLanguage: auto`. Summary generated in detected language. |
| **Multi-provider AI** | Auto-capture supports opencode-native providers (Anthropic, OpenAI, GitHub Copilot via opencode session API) + manual API keys. Structured output via Zod schema. |
| **Sharding** | Per-project SQLite shards with scope-based partitioning (`user`/`project`). Cross-project search via `scope: all-projects`. |
| **Cleanup service** | Scheduled memory cleanup with configurable triggers. |
| **Migration tooling** | Schema migration detection + execution (fresh-start / re-embed strategies). Tag migration with batch progress. |
| **Pin system** | Pin/unpin memories for persistent prominence. |
| **USearch fallback** | Automatic ExactScan fallback when USearch is unavailable or fails. |
| **Embedding warmup** | Async model warmup to avoid blocking OpenCode startup. Global warmup key prevents double-initialization. |
| **Web server takeover** | Port conflict resolution with health-check loop. Jittered retry. Multi-instance coordination. |
| **i18n** | Web UI internationalization support (`i18n.js`, 11KB). |
| **Toasts** | OpenCode TUI toast notifications for auto-capture, profile learning, errors, compaction, web server events. |

---

## 5. What opencode-mem Actually Does

opencode-mem is a **local-first, SQLite-backed vector memory plugin for OpenCode** with:

1. **Storage**: SQLite memories table (17 columns) + USearch in-memory vector index (384d Xenova embeddings) + ExactScan CPU fallback
2. **Ingestion**: Manual `memory({ mode: "add" })` + automatic capture on session idle (LLM-generated summaries via opencode provider API)
3. **Retrieval**: Vector similarity search (content 0.6 + tags 0.4 fusion) + chronological listing + session-ID metadata lookup
4. **Organization**: Project-scoped sharding, user tags, pin system, user profiles
5. **Integration**: OpenCode `chat.message` hook (memory injection), `event` hook (idle → auto-capture, compacted → re-injection), `memory` tool (add/search/list/forget/profile)
6. **UI**: Full web dashboard at localhost:4747 (memory explorer, timeline, profiles, cleanup, dedup, migration)
7. **Pipeline**: Single-pass LLM extraction (open structured output), privacy scrubbing, language detection, no multi-phase refinement
8. **Lifecycle**: Add/delete only (no update, no decay, no conflict resolution)

---

## 6. Comparison-Ready Summary

```
opencode-mem
├── Vital:        TS, MIT, local binary ❌ (Bun plugin, not standalone)
├── Deployment:   Local plugin, SQLite+USearch+Transformers
├── Integration:  OpenCode plugin (tool + 2 hooks)
├── Web UI:       ✅ Full dashboard
├── Offline:      ✅
├── Schema:       17 columns, ~10 meaningful fields
├── Source:       4-tier (manual/auto-capture/import/api)
├── Search:       2 modes (vector + chronological), 1 source
├── Forget:       ✅ explicit delete
├── Auto-extract: ✅ LLM single-pass on idle
├── Dedup:        ✅ API endpoint
├── Persona:      ✅ preferences + patterns + workflows
├── Timeline:     ✅ visual (Web UI), ❌ query API
├── Fulltext:     ❌ no FTS5
├── Hybrid:       ❌ no BM25+vector fusion
├── Deep search:  ❌
├── Code graph:   ❌
├── Decay:        ❌
├── Supersede:    ❌ add-only
├── Contradiction:❌
├── Trust model:  ❌
└── Multi-agent:  ❌
```
