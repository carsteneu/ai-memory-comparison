# Wax — Evidence

> **Repo:** https://github.com/christopherkarani/Wax (Swift, Apache 2.0, ~744 stars)
> **Audit date:** 2026-05-28
> **Source:** README.md + Resources/docs/wax-mcp-setup.md
> **URL CORRECTION:** The provided URL `https://github.com/tom-doerr/wax` does **not exist** (404). The correct repo is `christopherkarani/Wax`. tom-doerr has 294 repos but none named "wax".

---

## Vital Signs

| Field | Value |
|-------|-------|
| **Stars** | ~744 |
| **Language** | Swift |
| **License** | Apache 2.0 |
| **Single binary** | ✅ wax-cli (build from source) |
| **Deployment** | Local binary / Swift Package / npx launcher |
| **Storage** | Single `.wax` file (SQLite FTS5 + Metal HNSW + LZ4 frames) |
| **Integration** | MCP server + Swift library + CLI daemon (JSON-line) |

---

## Claim Verification

### ✅ CONFIRMED

| Claim | Evidence |
|-------|----------|
| **offline** | README: "100% on-device", "No servers. No API keys. No Docker." FAQ: "Do I need an internet connection? No." |
| **fulltext** | README: SQLite FTS5 for text search. CLI: `wax-cli search "query" --mode text`. Architecture: "SQLite FTS5 Blob (Text Search + EAV Facts)". |
| **semantic** | README: "Metal HNSW Index (Vector Search)". CLI: `--mode hybrid`. Comparison table: "Hybrid (Text + Vector)". Apple Silicon Metal-accelerated embeddings. |
| **p_claude** | README: "Claude Code" mentioned multiple times. MCP server with `claude install-skill` command. Dedicated CLAUDE.md prompt included. |
| **p_cursor** | README: "Your AI assistant (Claude Code, Cursor, etc.)". Agent Quick Start lists Cursor alongside Claude Code and Windsurf. |
| **p_windsurf** | README: Agent Quick Start section explicitly lists "Windsurf" as a target platform. |

### ⚠️ PARTIAL / BORDERLINE

| Claim | Verdict | Evidence |
|-------|---------|----------|
| **p_codex** | ⚠️ partial | Not in README's platform list. But wax-mcp-setup.md mentions "steady-state Claude/Codex sessions". The npx launcher supports Codex-style MCP. Present but not prominently supported. |

### ❌ NOT CONFIRMED (claimed but absent from README/docs)

| Claim | Evidence of absence |
|-------|---------------------|
| **layeredMemory** | No layered memory architecture described. Distinction exists between session-scoped vs broker-managed long-term memory, and EAV structured facts vs raw documents, but this is not a "layered" model (no L0→L3 pyramid, no progressive disclosure, no tier hierarchy). |
| **decay** | No decay or time-based forgetting mechanism. `session_synthesize` and promotion thresholds exist but are about promoting from ephemeral to persistent, not decay over time. |
| **supersede** | No supersede/replace mechanism documented. `memory_promote` moves ephemeral → persistent but doesn't replace old versions. No version chain tracking. |
| **explicitForget** | No general `forget` or `delete` tool. `fact_retract` exists for structured facts only — not general memory deletion. The starter prompt explicitly says "Do not manage SESSION_STORE, --store-path, or flush in normal agent flows." |
| **autoExtract** | All memory writing is manual: `remember`, `save`, `handoff`. No automatic extraction pipeline from conversation/context. The agent must explicitly call `remember`. |
| **p_opencode** | Not mentioned anywhere in README or MCP setup docs. Platforms listed: Claude Code, Cursor, Windsurf. |
| **p_gemini** | Not mentioned anywhere in README or MCP setup docs. |
| **schemaFields=6** | Approximate — varies by tool. `remember` takes content + metadata + session_id (3 fields). `handoff` adds project + pending_tasks (4–5 fields). Structured memory has entity/attribute/value (3 EAV fields). The user's ~6 estimate is reasonable but not precisely documentable from public docs. |

---

## Absent Feature Verification

### CORRECTIONS: Features claimed absent that ARE present

| Feature | Discovery | Evidence |
|---------|-----------|----------|
| **entities** | ✋ PRESENT (claimed absent) | MCP tools: `entity_upsert`, `entity_resolve`. Architecture: "EAV (Entity-Attribute-Value) storage handles durable facts and long-term reasoning." Feature flag: `WAX_MCP_FEATURE_STRUCTURED_MEMORY` enables "graph/entity/fact tools". |
| **hybrid** | ✋ PRESENT (claimed absent) | Primary search feature. README comparison table: "Hybrid (Text + Vector)". CLI: `--mode hybrid`. Architecture: "Hybrid Search Indices" with SQLite FTS5 + Metal HNSW. Search modes: text, hybrid, vector. |
| **factQuery** | ✋ PRESENT (claimed absent) | `facts_query` is an explicit MCP tool. The starter prompt lists it alongside `entity_resolve`. Feature flag doc confirms graph/entity/fact tools. |

### ✅ CONFIRMED ABSENT

All other "absent" claims are verified absent from public README and docs:

webUi, multiAgent, actions, keywords, anticipatedQueries, triggerRules, domainTag, taskType, context, source, originTrust, emotional, conflict, timeTravel, deep, codeGraph, docsSearch, timeline, contradiction, quarantine, autoResolve, trustModel, contentPreproc, dedup, qualityRefine, narrative, clustering, recurrence, persona

---

## Notable Features Not Claimed

| Feature | Notes |
|---------|-------|
| **Session lifecycle** | `session_start` / `session_end` with explicit session_id scoping on reads and writes. |
| **Handoff continuity** | `handoff` / `handoff_latest` for cross-session context passing with content, project, and pending_tasks. |
| **Corpus search** | `corpus_search` for cross-session retrieval across broker-managed session history with provenance metadata. |
| **Structured memory** | EAV (Entity-Attribute-Value) model with `entity_upsert`, `fact_assert`, `fact_retract`, `facts_query`, `entity_resolve`. |
| **Single-file architecture** | Frame-based container with dual headers, WAL, LZ4 compression, TOC — similar concept to Memvid's .mv2. |
| **Apple Silicon native** | Metal-accelerated HNSW. ~6ms p95 hybrid recall, ~9ms cold open. |
| **Markdown sync** | `markdown_export` / `markdown_sync` for MEMORY.md round-trips (comparable to ai-memory's markdown wiki). |
| **WaxRepo TUI** | Semantic search TUI for git history — `wax-repo index` / `wax-repo search`. |

---

## Summary

| Category | Count |
|----------|-------|
| **Confirmed claims** | 6 of 14 |
| **Partial/borderline** | 1 (p_codex) |
| **NOT confirmed** | 7 (layeredMemory, decay, supersede, explicitForget, autoExtract, p_opencode, p_gemini) |
| **Absent claims corrected to PRESENT** | 3 (entities, hybrid, factQuery) |
| **Absent confirmed** | 32 features |
| **URL correct?** | ❌ — `tom-doerr/wax` → 404. Correct: `christopherkarani/Wax` |
| **Est. schema fields** | ~6 (varies by tool; core memory unit: content + metadata + session_id = 3) |

---

`evidence: "https://github.com/carsteneu/ai-memory-comparison/blob/main/evidence/wax.md"`
