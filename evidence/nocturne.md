# Nocturne — Evidence

> Every ✅ claim backed by public source code or documentation.
> Audit date: 2026-05-28. Source: GitHub `Dataojitori/nocturne_memory` main branch, README.md, docs/TOOLS.md, backend/db/models.py.

---

## Architecture

### WebUI ✅
- `README.md` — "可视化管理界面 (The Dashboard)" section with 4 screenshots: Memory Explorer (tree browsing), Memory Detail (edit content/metadata/triggers), Review & Audit (visual diff, one-click accept/reject), Brain Cleanup (version backup management).
- `README.md` — Dashboard components: Memory Explorer, Review & Audit, Brain Cleanup, Settings (server/port, API token, database, Boot URIs, valid domains).
- `README.md` — Tech stack: "React + Vite + TailwindCSS" for Human Interface.
- `backend/web_app.py` — FastAPI app serving the built frontend and REST API.

### Offline ✅
- `README.md` — "SQLite/PostgreSQL + URI Routing" architecture. "完全开源，可本地单机运行" (fully open-source, can run locally on a single machine).
- `README.md` — Storage: SQLite (default) or PostgreSQL. No cloud dependency.

### Multi-agent — ❌ (verified absent)
- No agent-to-agent communication, coordination, or swarm orchestration.
- `README.md` — Namespace isolation exists ("同时托管一到多个 Agent 的独立记忆空间"), but this is about hosting separate AI personalities with independent memory, not multi-agent collaboration.

### LLM providers — 1 ✅ (MCP-agnostic)
- Nocturne is an MCP server that stores data; it does not call LLMs itself. Any MCP-compatible LLM client can use it. The README emphasizes model independence: "不绑定任何 LLM". The count of 1 reflects that it is a storage backend, not an LLM caller. This is technically unlimited but the field measures the storage's direct LLM integration (none = 1 default).

---

## Data Model

### Storage unit: "Memory entry" ✅
- `backend/db/models.py` — `Memory` ORM model: `id`, `node_uuid`, `content`, `deprecated`, `migrated_to`, `created_at`. Content is the core payload.
- `README.md` — Architecture diagram shows Node → Memory → Edge → Path hierarchy.

### Entities — ❌ (verified absent)
- No structured entity extraction (Person, Organization, etc.). Nodes are conceptual anchors (UUIDs), not typed entities.
- `backend/db/models.py` — `Node` has only `uuid`, `created_at`, `last_accessed_at`. No type/label field.

### Actions — ❌ (verified absent)
- No action tracking or command logging.

### Keywords — ❌ (verified absent)
- Has glossary keywords (`GlossaryKeyword` table: keyword → node_uuid binding for auto-hyperlinking via Aho-Corasick) and `manage_triggers` (trigger words for cross-node recall). But these serve functional purposes (linking/retrieval triggers), not metadata tagging of memory entries. No keyword/tag field on the Memory or Edge models.
- `backend/db/models.py` — `GlossaryKeyword` for cross-linking. `SearchDocument.search_terms` for CJK tokenization. Neither is a user-facing keyword metadata system.

### Anticipated queries — ❌ (verified absent)
- No anticipated query pre-definition.

### Trigger rules ✅ (claims ❌ — **CORRECTION** ❌→✅)
- `docs/TOOLS.md` — `create_memory()` parameter `disclosure`: "触发条件：描述'在什么情况下该想起这条记忆'" (trigger condition: describes "in what situation should this memory be recalled"). Example: `"当我准备发 Bluesky 时"` (when I'm about to post on Bluesky).
- `docs/TOOLS.md` — `manage_triggers(uri, add?, remove?)`: "为记忆节点绑定触发词，为记忆增加超越父子层级的横向召回通道" (binds trigger words to memory nodes for lateral recall beyond parent-child hierarchy).
- `README.md` — "Disclosure Routing: 每条记忆绑定一个人类可读的触发条件（disclosure），如'当用户提到项目 X 时'。AI 按当前情境精准注入" (each memory binds a human-readable trigger condition, AI injects precisely based on current context).
- `backend/db/models.py` — `Edge.disclosure` field (Text, nullable): stores the trigger condition. `SearchDocument.disclosure` mirrors it for search.

### Domain tag — ❌ (verified absent)
- Domains exist as structural URI prefixes (`core://`, `writer://`, `game://`, etc.) — part of the addressing scheme, not arbitrary metadata tags on entries.
- `backend/db/models.py` — `Path.domain` is part of the composite primary key for URI routing, not a free-form metadata field.
- `README.md` — "Valid Domains" configurable in Settings as namespace buckets.

### Task type — ❌ (verified absent)
- No task/idea/blocked/stale classification.

### Context (why) — ❌ (verified absent)
- No separate "context" or "why this was created" field. The `disclosure` field describes when to recall, not why the memory was created.

### Source attribution — ❌ (verified absent)
- No source tracking on memories.

### Origin trust — ❌ (verified absent)
- No trust scoring model.

### Emotional — ❌ (verified absent)
- No emotional dimension or valence tracking.

### Conflict detection — ❌ (verified absent)
- No automatic conflict detection. The `system://diagnostic` feature finds "冗余、过时、矛盾的内容" (redundant, stale, contradictory content) but this is a diagnostic report, not automated contradiction resolution.

### Layered memory — ❌ (verified absent)
- Architecture has 4 structural layers (identity/content/relationship/routing), but these are database normalization layers, not cognitive memory layers (episodic/semantic/procedural).
- `backend/db/models.py` — Node (identity), Memory (content), Edge (relationship), Path (routing). All serve structural purposes, not memory type differentiation.

### Time-travel ✅
- `README.md` — "每次写入自动生成快照 (Snapshot), 人类 Owner 通过 Dashboard 一键审计、回滚或合并" (each write auto-generates snapshot, human owner audits/rolls back/merges via Dashboard one-click).
- `README.md` — "可视化 diff 对比变更，一键 Integrate（接受）或 Reject（回滚）" (visual diff comparison, one-click accept or reject/rollback).
- `README.md` — "版本安全网 — AI 每次操作自动备份，清理需人类确认" (version safety net — AI operation auto-backup, cleanup requires human confirmation).
- `backend/db/snapshot.py` — Full snapshot engine (13,999 bytes).
- `backend/db/models.py` — `Memory.deprecated` + `Memory.migrated_to`: version chain for tracking memory evolution across versions. `ChangeCollector` class records pre-mutation state for rollback.
- `backend/models/schemas.py` — `UriDiff`, `RollbackResponse`, `GroupRollbackResponse`: diff and rollback schemas for the review/audit dashboard.

### Schema fields — 5 ✅
- The core fields that define a memory entry:
  1. `content` (Text) — the memory text (Memory table)
  2. `priority` (Integer) — retrieval weight (Edge table, 0=highest)
  3. `disclosure` (Text) — trigger condition (Edge table)
  4. `domain` (String) — namespace in URI, e.g. "core" (Path table)
  5. `path` (String) — location within domain (Path table)
- `docs/TOOLS.md` — `create_memory(parent_uri, content, priority, disclosure, title?)`: content + priority + disclosure + parent_uri (domain+path) + optional title.
- `backend/db/models.py` — Memory: content. Edge: priority, disclosure. Path: domain, path. These 5 semantic fields define a user-facing memory entry. Bookkeeping fields (uuid, id, created_at, deprecated, migrated_to, namespace) excluded.

---

## Search & Retrieval

### Full-text ✅
- `docs/TOOLS.md` — `search_memory(query, domain?, limit?)`: "按关键词搜索记忆内容和路径。使用全文检索，不是语义搜索。" (keyword search on memory content and paths. Uses full-text search, not semantic search.)
- `backend/db/search.py` — Full-text search implementation (15,523 bytes). `SearchDocument` table with `content` and `search_terms` columns.
- `backend/db/search_terms.py` — Search term tokenization including CJK bigram splitting for Chinese/Japanese/Korean text.

### Semantic/vector — ❌ (verified absent)
- `README.md` — Explicitly argues AGAINST vector RAG: "为什么 Vector RAG 做不了 Agent 的记忆？" section lists 6 fatal flaws of vector RAG.
- `docs/TOOLS.md` — `search_memory` explicitly states: "全文检索，不是语义搜索" (full-text search, not semantic search).
- No embedding model, no vector index, no cosine similarity search anywhere in the codebase.

### Hybrid — ❌ (verified absent)
- Only fulltext. No vector component to hybridize with.

### Deep search — ❌ (verified absent)
- No deep search with conversation context.

### Code graph — ❌ (verified absent)
- No code symbol indexing or traversal.

### Docs search — ❌ (verified absent)
- No documentation indexing.

### Fact query — ❌ (verified absent)
- No fact/entity structured query.

### Timeline — ❌ (verified absent)
- Snapshots and `created_at` timestamps exist for versioning, but no dedicated timeline view or temporal query feature.

### Search modes — 1 ✅
- `search_memory` is the sole search tool. System URIs (`system://boot`, `system://index`, `system://recent`, `system://glossary`, `system://diagnostic`) are read operations, not separate search modes.

### Data sources — 1 ✅
- Single data source: the SQLite/PostgreSQL database. No multi-source federation.

---

## Knowledge Lifecycle

### Decay/forgetting — ❌ (verified absent)
- No time-based decay or relevance reduction.

### Supersede/replace — ❌ (verified absent)
- Has `Memory.deprecated` + `Memory.migrated_to` for version chains, and snapshots for manual review/rollback. But no automatic supersede where a new learning replaces an old one — version management is manual via the Dashboard review workflow.
- `backend/db/models.py` — `Memory` model has `deprecated` (Boolean) and `migrated_to` (Integer) fields. These enable version tracking but require human action to deprecate/migrate.

### Contradiction detection — ❌ (verified absent)
- No automatic contradiction resolution. `system://diagnostic` surfaces stale/redundant/contradictory content as a report, not an automated resolution.

### Quarantine — ❌ (verified absent)
- No quarantine or sandbox.

### Auto-resolve — ❌ (verified absent)
- No automatic task resolution.

### Trust model — ❌ (verified absent)
- No trust or confidence scoring.

### Explicit forget — ❌ (verified absent)
- `delete_memory` removes "一条访问路径（不删除记忆正文本体）" (one access path, does not delete the memory body). Soft path deletion only. Brain Cleanup exists for version cleanup but requires human confirmation.

---

## Extraction Pipeline

### Auto-extract — ❌ (verified absent)
- AI manually creates memories via MCP tools (`create_memory`, `update_memory`). No automatic extraction from conversations.
- `README.md` — "没有后台自动摘要的系统。每一条记忆都由 AI 自己决定创建" (no background auto-summarization. Every memory is created by the AI itself).

### Content preprocessing — ❌ (verified absent)
- No LLM-based content cleaning or preprocessing.

### Dedup — ❌ (verified absent)
- `system://diagnostic` finds "重复别名" (duplicate aliases), but this is a human-reviewed diagnostic, not automatic dedup.

### Quality refinement — ❌ (verified absent)
- No quality scoring or refinement.

### Narrative generation — ❌ (verified absent)
- No narrative/summary generation.

### Clustering — ❌ (verified absent)
- No automatic clustering of memories.

### Recurrence tracking — ❌ (verified absent)
- `MemoryAccessLog` table tracks access frequency (`backend/db/models.py`), but there is no recurrence detection or pattern recognition.

### Persona — ❌ (verified absent)
- System Boot URIs can encode AI identity/personality as content, but there is no structured persona trait system with predefined dimensions.

---

## Platform Support

### p_claude ✅
- `README.md` — Claude Desktop and Claude Code explicitly listed with configuration examples. "claude mcp add-json" command provided.

### p_opencode ✅ (claims ❌ — **CORRECTION** ❌→✅)
- `README.md` — OpenCode explicitly listed: "适用于任何支持 MCP 的客户端（OpenClaw / Cursor / Windsurf / GitHub Copilot / Cline / OpenCode / Gemini CLI / OpenAI Codex / Claude Code / Cherry Studio / Antigravity 等）"

### p_codex ✅ (claims ❌ — **CORRECTION** ❌→✅)
- `README.md` — OpenAI Codex explicitly listed with dedicated config example: "OpenAI Codex — 在 `.codex/config.toml` 中添加"
- `README.md` — Demo server: code block for `.codex/config.toml` configuration.

### p_gemini ✅ (claims ❌ — **CORRECTION** ❌→✅)
- `README.md` — Gemini CLI explicitly listed: "Gemini CLI" in the compatibility list.

### p_copilot ✅ (claims ❌ — **CORRECTION** ❌→✅)
- `README.md` — GitHub Copilot explicitly listed: "GitHub Copilot" in the compatibility list and in Step 2 config instructions.

### p_cursor ✅ (claims ❌ — **CORRECTION** ❌→✅)
- `README.md` — Cursor explicitly listed in the compatibility list.

### p_windsurf ✅ (claims ❌ — **CORRECTION** ❌→✅)
- `README.md` — Windsurf explicitly listed in the compatibility list.

### p_openclaw ✅ (claims ❌ — **CORRECTION** ❌→✅)
- `README.md` — OpenClaw mentioned multiple times: in the compatibility list at the top, and a dedicated "特别提醒 OpenClaw 用户" (special note for OpenClaw users) section at the bottom.
- `README.md` — "还在于 OpenClaw 原生简陋的记忆系统？将其替换为 Nocturne Memory" (still using OpenClaw's crude native memory system? Replace it with Nocturne Memory).

### p_antigravity ✅ (claims ❌ — **CORRECTION** ❌→✅)
- `README.md` — Antigravity mentioned multiple times with dedicated configuration: "Antigravity — 在 MCP 设置中添加" with JSON config snippet.
- `README.md` — Special Antigravity note: "如果是 Antigravity：args 必须指向 `backend/mcp_wrapper.py`（解决 Windows CRLF 问题）" (if using Antigravity: args must point to mcp_wrapper.py).
- `README.md` — Demo server: code block for Antigravity MCP configuration.

### p_hermes — ❌ (verified absent)
- No mention of Hermes.

### p_pi — ❌ (verified absent)
- No mention of Pi.

---

## Other

### Setup — "Easy" (claims "?" — **CORRECTION**)
- `README.md` — 2-step install: `git clone` + `pip install -r backend/requirements.txt`. Then add MCP client config JSON. "30 秒试用 MCP（无需安装）" for the demo server.

### Cache optimization — ❌ (verified absent)
- No caching optimization mentioned.

### Privacy/encryption — ❌ (verified absent)
- No encryption at rest or in transit. API Token available for remote access auth, but no content encryption.

### Data export — ❌ (verified absent)
- Migration scripts exist (`migrate_neo4j_to_sqlite`), but no general-purpose data export. Database backup on migration is for safety, not user-facing export.

---

## Summary of Corrections

| Feature | Claimed | Actual | Evidence |
|---------|---------|--------|----------|
| triggerRules | ❌ | ✅ | `disclosure` field + `manage_triggers` tool — conditional memory recall |
| p_opencode | ❌ | ✅ | Explicitly listed in compatible MCP clients |
| p_codex | ❌ | ✅ | Dedicated config example in README |
| p_gemini | ❌ | ✅ | Listed in compatible clients |
| p_copilot | ❌ | ✅ | Listed in compatible clients |
| p_cursor | ❌ | ✅ | Listed in compatible clients |
| p_windsurf | ❌ | ✅ | Listed in compatible clients |
| p_openclaw | ❌ | ✅ | Multiple mentions, dedicated section |
| p_antigravity | ❌ | ✅ | Multiple mentions, dedicated config + wrapper |
| setup | "?" | "Easy" | pip install + MCP JSON config |

**All other claims verified correct.** The 20+ absent features listed in the audit prompt are confirmed absent.
