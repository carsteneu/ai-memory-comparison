# memorix — Evidence

> Every ✅ claim backed by public source code or documentation.
> Audit date: 2026-05-28. Source: GitHub `memorix-ai/memorix-sdk` main branch, `memorix-ai/memorix-docs`. PyPI: `memorix-ai`.

**IMPORTANT**: Memorix is a Python SDK/library — NOT an agent memory system. It wraps vector stores (FAISS, Qdrant) and embedding models (OpenAI, Gemini, Sentence Transformers) behind a clean API (`store`/`retrieve`/`update`/`delete`). It has zero agent platform integrations (no MCP server, no Claude Code plugin, no Cursor integration). This fundamentally differs from systems like engram, Mem0, or YesMem that are purpose-built for AI coding agent memory.

The GitHub org (`memorix-ai`) was created ~July 2025. All repos have 0 stars, 0 issues, 0 forks. The project is early-stage, with most features on the roadmap rather than implemented.

---

## Architecture

### Web UI ⚠️ (claims ✅ — CORRECTION: demo apps, not built-in)
- `memorix-ai/memorix-sdk/README.md` — "Streamlit Web App: Interactive memory management interface" and "Gradio Demo: Quick prototyping interface" — listed under `/memorix-examples` repo, not part of the SDK itself.
- These are external example applications, not a built-in Web UI or dashboard. Compare to Mem0's built-in Dashboard or engram's TUI — those ship with the product.
- **Correction**: Should be ⚠️ (demo only) or ❌ (not built-in). The project itself has no web UI; demo apps are in a separate examples repo.

### Offline ⚠️ (claims ✅ — CORRECTION: depends on embedder)
- `memorix-ai/memorix-sdk/README.md` — Embedder options: "Sentence Transformers: all-MiniLM-L6-v2, all-mpnet-base-v2" (local), "OpenAI: text-embedding-ada-002" (API), "Google Gemini: models/embedding-001" (API).
- With Sentence Transformers embedder + FAISS vector store + SQLite metadata, the system is fully offline. With OpenAI or Gemini embedders, it requires internet.
- **Correction**: Should be ⚠️ (partial — only fully offline with local embedders; default config uses OpenAI which needs API key).

---

## Data Model

### Schema fields — 5-6 ✅ (claims 6 — VERIFIED, borderline)
- `memorix-ai/memorix-docs/docs/api/memory_api.md` — `MemoryResult` object has 5 attributes: `id` (str), `text` (str), `metadata` (Dict), `score` (float), `embedding` (Optional[np.ndarray]).
- `memorix-ai/memorix-sdk/README.md` — `store()` takes `content` + `metadata` + implicit `id`; `retrieve()` returns `content`, `similarity`, `metadata`.
- Core fields: id, text/content, metadata, score/similarity, embedding = 5. The README mentions optional `hash` in some contexts. 5-6 is accurate.

### Keywords ❌ (claims ✅ — CORRECTION)
- `memorix-ai/memorix-docs/docs/api/memory_api.md` — `store()` accepts `metadata: Optional[Dict]`. Metadata is a free-form dictionary with no structure enforcement. Any key-value pairs can be stored, including user-defined tags.
- There is no keyword extraction, no keyword indexing, no structured tag system. Users must manually provide keywords inside the metadata dict.
- `memorix-ai/memorix-docs/docs/usage/memory.md` — Example shows `"tags": tags or []` in metadata. These are user-defined, not system-extracted.
- **Correction**: Should be ❌. Memorix has no keyword/tag extraction. Compare to engram's `type` tag or YesMem's junction table keyword system.

---

## Search & Retrieval

### Semantic/vector ✅
- `memorix-ai/memorix-docs/docs/api/memory_api.md` — `retrieve(query, top_k, filter, score_threshold)` performs vector similarity search. Returns `List[MemoryResult]` with `score` (similarity) and `embedding`.
- `memorix-ai/memorix-sdk/README.md` — "Retrieve relevant memories based on query" via `retrieve()`.
- Multiple embedding backends: OpenAI `text-embedding-ada-002`, Google Gemini, Sentence Transformers.

### Full-text ❌ (claims ✅ — CORRECTION)
- `memorix-ai/memorix-docs/docs/api/memory_api.md` — The API has no full-text search method. `retrieve()` is purely vector/semantic. `filter` parameter on `retrieve()` does metadata filtering, not text search.
- `memorix-ai/memorix-sdk/README.md` — Metadata store supports SQLite, but no FTS5 or text search API is exposed. SQLite is used only for structured metadata storage.
- **Correction**: Should be ❌. No BM25, no FTS5, no keyword search API exists.

### Search modes — 2 ✅ (claims 2 — VERIFIED)
- `memorix-ai/memorix-sdk/README.md` — API reference table lists two retrieval methods: `retrieve(query, top_k=5)` (semantic search) and `list_memories(limit=100)` (listing).
- `memorix-ai/memorix-docs/docs/api/memory_api.md` — Full API adds `get_by_id()` (direct ID lookup) but this is not a search mode. Core search modes: (1) vector similarity via `retrieve()`, (2) listing via `list_memories()` or `count()` with optional metadata filters.

---

## Knowledge Lifecycle

### Supersede ✅
- `memorix-ai/memorix-docs/docs/api/memory_api.md` — `update(id, text=None, metadata=None)` replaces existing memory content/metadata by ID. Returns `bool`.
- `memorix-ai/memorix-docs/docs/api/memory_api.md` — `update_by_filter(filter, text=None, metadata=None)` bulk-updates memories matching metadata filter.

### Explicit forget ✅
- `memorix-ai/memorix-docs/docs/api/memory_api.md` — `delete(id)` deletes by ID, `delete_by_filter(filter)` bulk-deletes by metadata filter, `clear()` removes all memories in a collection.

### Decay ❌ (claims ✅ — CORRECTION)
- `memorix-ai/memorix-sdk/README.md` — Roadmap: "Add memory expiration" is listed as a future feature, not yet implemented.
- `memorix-ai/memorix-docs/docs/usage/memory.md` — "Memory Retention Policies" section shows manual cleanup (`cleanup_old_memories()` with `delete_by_filter()`), not automatic decay. This is user-implemented application code, not a system feature.
- **Correction**: Should be ❌. No built-in decay, forgetting curve, or memory expiration exists.

### Auto-extraction ❌ (claims ✅ — CORRECTION)
- `memorix-ai/memorix-docs/docs/api/memory_api.md` — All memory operations are explicit: `store()`, `store_batch()`, `update()`, `delete()`. No hooks, no event listeners, no automatic extraction from conversations.
- `memorix-ai/memorix-docs/docs/usage/memory.md` — Usage patterns show manual `store()` calls in user code (`add_message()`, `add_knowledge()`, `store_episode()`). No automatic extraction pipeline.
- **Correction**: Should be ❌. Memorix is a passive store — you call `store()` yourself. Compare to Mem0's `add()` with `infer=True` or YesMem's 6-phase extraction pipeline.

---

## Platform Support

### ALL platform claims ❌ (claims 9 ✅ — CORRECTION: all false)

Memorix has **zero agent platform integrations**. It is a pure Python library with no MCP server, no Claude Code plugin, no Cursor extension, no Codex integration, no Gemini CLI integration, no Windsurf support, no OpenClaw plugin, no pi support, no Antigravity support.

Evidence of absence:
- `memorix-ai/memorix-sdk/README.md` — No mention of any agent platform. The "Integration" section does not exist. No MCP tools, no hooks, no platform-specific setup instructions.
- `memorix-ai/memorix-docs` — Documentation covers only: install, quickstart, basic usage, memory management, vector stores, embeddings, API reference. No integration guides for any coding agent platform.
- GitHub org `memorix-ai` — 6 repos total, none related to agent platform integration:
  - `memorix-sdk` (core SDK)
  - `memorix-docs` (MkDocs documentation)
  - `memorix-examples` (demo scripts)
  - `memorix-embedders` (empty stub)
  - `memorix-vectorstores` (empty stub)
  - `memorix-meta` (empty stub)

**Correction**: All 9 platform claims (p_claude, p_codex, p_opencode, p_gemini, p_cursor, p_windsurf, p_openclaw, p_pi, p_antigravity) should be ❌.

---

## Claims NOT present (marked absent) — VERIFIED

The following features are correctly identified as absent. No public evidence was found for any of them:

**Data Model:** entities, actions, anticipatedQueries, triggerRules, domainTag, taskType, context (why), source (attribution), originTrust, emotional, conflict, layeredMemory, timeTravel — all ❌ (free-form metadata dict only; no structured schema beyond id/text/metadata/score/embedding)

**Search:** hybrid, deep, codeGraph, docsSearch, factQuery, timeline — all ❌ (single vector search mode only; no BM25+Vec fusion, no code graph, no doc index, no fact metadata query, no timeline)

**Lifecycle:** contradiction, quarantine, autoResolve, trustModel — all ❌ (no contradiction detection, no quarantine, no auto-resolution, no trust weighting)

**Extraction:** contentPreproc, dedup, qualityRefine, narrative, clustering, recurrence, persona — all ❌ (no extraction pipeline at all — manual `store()` only; no preprocessing, no dedup, no quality refinement, no narrative generation, no clustering, no recurrence detection, no persona engine)

**Architecture:** multiAgent, proxy — all ❌ (single-user library; no proxy architecture; no multi-agent orchestration)

---

## Audit Notes

1. **Category error**: Memorix is a generic vector-store SDK, not an agent memory system. It's analogous to calling `chromadb` or `faiss` an "AI memory system." While you can build agent memory on top of it, the SDK itself provides no agent-specific features (no auto-extraction, no decay, no conflict resolution, no multi-agent support, no platform integrations).

2. **Platform claims are fabrications**: All 9 platform support claims (Claude Code, Codex, OpenCode, Gemini CLI, Cursor, Windsurf, OpenClaw, pi, Antigravity) have zero evidence. The SDK has no integrations with any coding agent platform whatsoever.

3. **decay is on roadmap, not implemented**: "Add memory expiration" appears on the README roadmap as a future feature. The usage docs show manual cleanup patterns (`delete_by_filter` with date filters), not automatic decay.

4. **webUi is external demo apps**: The Streamlit and Gradio apps live in a separate `memorix-examples` repo. They are demonstration applications, not a built-in UI that ships with the product. Compare to Mem0's Dashboard or engram's TUI which are part of the core product.

5. **offline requires local embedders**: While FAISS + SQLite run locally, the default configuration uses OpenAI embeddings which require internet. Only `sentence-transformers` mode is fully offline.

6. **fulltext absent**: Despite using SQLite for metadata, no full-text search (FTS5) is exposed. Search is vector-only via `retrieve()`. Metadata filtering is exact-match, not text search.

7. **Project maturity**: 0 stars across all repos, no issues filed, no community activity. The org was created ~July 2025. Most features (compression, summarization, versioning, expiration, categories, tags, search filters, export/import, analytics) are roadmap items, not implemented.

---

## Evidence URLs

- SDK README: `https://github.com/memorix-ai/memorix-sdk/blob/main/README.md`
- API Reference: `https://github.com/memorix-ai/memorix-docs/blob/main/docs/api/memory_api.md`
- Memory Usage Guide: `https://github.com/memorix-ai/memorix-docs/blob/main/docs/usage/memory.md`
- Vision: `https://github.com/memorix-ai/memorix-sdk/blob/main/docs/VISION.md`
- Docs README: `https://github.com/memorix-ai/memorix-docs/blob/main/README.md`
- GitHub Org: `https://github.com/memorix-ai`
- PyPI: `https://pypi.org/project/memorix-ai/`

---

## Summary of Corrections

| Claim | Claimed | Actual | Correction |
|-------|---------|--------|------------|
| webUi | ✅ | ⚠️ demo apps only | ❌ (not built-in) |
| offline | ✅ | ⚠️ local embedders only | ⚠️ (partial) |
| keywords | ✅ | ❌ free-form metadata only | ❌ |
| fulltext | ✅ | ❌ vector-only | ❌ |
| semantic | ✅ | ✅ vector similarity | ✅ |
| searchModes | 2 | 2 (retrieve + list) | ✅ |
| decay | ✅ | ❌ roadmap item | ❌ |
| supersede | ✅ | ✅ update() | ✅ |
| explicitForget | ✅ | ✅ delete() | ✅ |
| autoExtract | ✅ | ❌ manual store() only | ❌ |
| schemaFields | 6 | 5-6 | ✅ borderline |
| p_claude | ✅ | ❌ no integration | ❌ |
| p_codex | ✅ | ❌ no integration | ❌ |
| p_opencode | ✅ | ❌ no integration | ❌ |
| p_gemini | ✅ | ❌ no integration | ❌ |
| p_cursor | ✅ | ❌ no integration | ❌ |
| p_windsurf | ✅ | ❌ no integration | ❌ |
| p_openclaw | ✅ | ❌ no integration | ❌ |
| p_pi | ✅ | ❌ no integration | ❌ |
| p_antigravity | ✅ | ❌ no integration | ❌ |
