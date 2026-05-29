# Continuity v2 — Evidence

> Audit date: 2026-05-29
> URL: https://github.com/Haustorium12/continuity-v2
> Stars: 32 · Language: Python · License: MIT · Created: 2026-05-01
> Repo: 24 commits, 11 source files + 4 hooks
> Verified: README + all 11 source files + 4 hook files reviewed in full.

## Vital Signs

### Stars ✅
- GitHub API: `stargazers_count: 32`, `forks_count: 6`, `created_at: 2026-05-01T01:51:29Z`

### Language ✅ (`data.js` metadata)
- GitHub API: `"language": "Python"` — 100% Python

### License ✅
- GitHub API: `"license": { "spdx_id": "MIT" }`
- `LICENSE` file present in repo root

### Single binary ❌
- Requires Python runtime (`python index.py`, `python mcp_server.py`, etc.). Not a compiled binary.

---

## Architecture

### Deployment ✅ — MCP server (Python)
- `README.md`: "Add to `~/.claude.json`: `"command": "python", "args": ["/path/to/continuity-v2/mcp_server.py"]`"
- `mcp_server.py`: stdio MCP server via `FastMCP("continuity-v2")`

### Storage ✅ — SQLite + FTS5 (+ vec)
- `index.py:29-57`: `SCHEMA` — creates `sessions`, `turns` tables, `turns_fts` FTS5 virtual table, triggers for auto-sync
- `embed.py:20-25`: `turn_vecs` virtual table via `vec0` (sqlite-vec)

### Integration ✅ — MCP + Hooks
- MCP: `mcp_server.py` exposes 8 tools (search_sessions, recall_session, recent_sessions, index_stats, thread_recall, find_similar, reindex, fts_integrity_check, fts_rebuild)
- Hooks: 4 hook files in `hooks/`: `precompact_save.py`, `session_start_inject.py`, `stop_hook_checkpoint.py`, `sse_proxy.py`

### Proxy ✅ — SSE proxy for token pressure detection
- `hooks/sse_proxy.py`: Proxies Claude Code ↔ Anthropic API on port 9099. Watches SSE stream for context window usage.
- `hooks/sse_proxy.py:48-51`: `THRESHOLDS = [70, 85, 95]` — writes signal files at each threshold
- `hooks/sse_proxy.py:80-88`: `write_signal()` writes `bell_{level}.signal` files with token counts
- `hooks/stop_hook_checkpoint.py:8`: "Fires on every Stop event (end of turn). Reads bell signal files written by sse_proxy.py."
- This is a genuine proxy (inspects and relays the API stream), not just hooks or MCP.

### Web/TUI ❌
- No visual interface. README mentions no browser, terminal UI, or dashboard.

### Offline ✅
- Core operations (indexing, FTS5 search, SQLite storage) run fully locally. Sentence transformer model downloads once but the core pipeline works offline. No cloud dependency.

### Multi-agent ❌
- No multi-agent coordination. Single-user, single-session design.

### LLM flexibility ❌ (1 model)
- Hardcoded to Claude Code + Anthropic API. No model-agnostic abstraction. The SSE proxy specifically parses Anthropic SSE format.

### Cache optimization ❌
- No token caching, prompt caching, or cache-aware mechanisms. The proxy monitors usage but doesn't optimize it.

### Procedural memory ❌
- No procedural/capability system. No REPL, no sandboxed execution, no workflow automation.

### Sandboxed execution ❌
- No sandbox. Python scripts run directly on the host.

### Scheduled execution ❌
- No scheduling, cron, or periodic jobs.

### Privacy/export ✅
- `chat_index.py` imports Anthropic data export (`conversations.json`). Data lives locally in user-controlled SQLite DB. Schema is fully open (SQLite, no proprietary format).

### Setup ✅
- `README.md`: Install hooks with `cp hooks/*.py ~/.claude/hooks/`, add MCP config to `~/.claude.json`. Package on PyPI: `pip install continuity-v2`.

### Pricing ✅
- MIT license, free.

---

## Data Model

**Unit:** Session turn (episodic record)

### Schema
```
sessions(id, project, ai_title, cwd, started_at, ended_at, turn_count, file_path, file_mtime, indexed_at, source)
turns(id, session_id, turn_idx, ts, role, text)
turns_fts (FTS5 mirror of turns.text)
edges(id, src_turn_id, dst_turn_id, edge_type, weight)
turn_vecs(turn_id, embedding float[384])
```

### Entities ❌
- No entity extraction. System indexes raw turn text from JSONL. No named entity recognition, no structured entity fields, no entity_upsert equivalent.
- `index.py` extracts user/assistant/tool use blocks but stores them as flat `role` + `text`, not structured entities.

### Actions ❌
- No structured action extraction. Tool calls parsed in `extract_text()` as `[tool:{name}]` annotations embedded in text, not as separate structured fields.

### Keywords ❌
- No keyword/tag system. The comparison can filter by project name (string match) but there is no user- or auto-assigned tagging.

### Anticipated queries ❌
- No generated queries. No semantic cross-referencing between stored items and predicted retrieval paths.

### Trigger rules ❌
- `hooks/stop_hook_checkpoint.py:24-31`: `CLOSE_TRIGGERS` list — hardcoded English words ("save", "goodnight", "bye", etc.) that trigger a sticky-note prompt. These are NOT user-configurable trigger rules. They are hardcoded session-close detectors.
- The bell signals (70/85/95%) are context pressure thresholds, not user-configured memory triggers.

### Domain tag ❌
- No domain categorization. The only classification is `source` field ('code' vs 'chat').

### Task type ❌
- No task classification. Session/turn data is indexed as-is with no completion/blocking/idea classification.

### Context (why) ❌
- No "why" field. Sessions have `ai_title` and raw text but no explicit context/reason storage alongside memories.

### Source attribution ❌
- `index.py:100`: `source TEXT DEFAULT 'code'` on sessions table.
- Only 2 source levels: 'code' (Claude Code) and 'chat' (claude.ai). CRITERIA.md requires ≥3 distinct source levels for ✅.
- `chat_index.py:78`: chat sessions tagged `source='chat'`.

### Origin + trust ❌
- No trust hierarchy. Source differentiation is flat (code/chat) with no weighting or trust levels.

### Emotional ❌
- No sentiment tracking, no emotional intensity fields.

### Conflict surfacing ❌
- No contradiction detection. No mechanism for flagging when new information conflicts with old.

### Layered memory ❌
- Flat chronological model. Raw turns indexed directly. No hierarchical summarization (L0 raw → L1 summary → L2 persona).

### Time-travel ✅
- `mcp_server.py:328-380`: `recall_session(session_id, range)` — full session replay by session ID or prefix
- `mcp_server.py:383-414`: `recent_sessions(n=10)` — chronological session browsing
- `stats.py`: Earliest/latest session timestamps
- `wire_edges.py`: `TEMPORAL` edges between sequential turns maintain temporal topology
- `mcp_server.py:437-502`: `thread_recall()` — BFS over TEMPORAL edges, walks backward and forward from seed turns

### Schema fields
- **13** distinct structured fields (non-ID, non-timestamp): project, ai_title, cwd, turn_count, file_path, source, session_id, turn_idx, role, text, edge_type, weight, embedding (384-dim)
- Excluded: id (auto), ts (timestamp), started_at/ended_at (timestamp), indexed_at (timestamp), file_mtime (timestamp), turn_id (foreign key)

---

## Search & Retrieval

### Full-text ✅
- `index.py:46-56`: `turns_fts` virtual table via SQLite FTS5 — full content index of all turn text
- `mcp_server.py:92-130`: `search_sessions()` — FTS5 `MATCH` query with AND/OR/NOT, quoted phrases, prefix* matching
- `search.py`: CLI wrapper around same FTS5 queries
- FTS5 triggers (`turns_ai`, `turns_ad`) keep index in sync with turns table
- `fts_integrity_check()` and `fts_rebuild()` maintenance tools available

### Semantic/Vector ✅
- `embed.py:12-16`: Uses `all-MiniLM-L6-v2` (384-dim), L2-normalized vectors stored via sqlite-vec `vec0` virtual table
- `mcp_server.py:596-660`: `find_similar()` — semantic similarity via ANN query on `turn_vecs`

### Hybrid (BM25+Vec) ❌
- System has both FTS5 (`search_sessions`) and semantic search (`find_similar`) as separate tools, but no single tool fuses BM25+vector results with Reciprocal Rank Fusion or similar.
- `mcp_server.py:596-660`: `find_similar()` hybrid scoring (0.7*sem + 0.2*recency + 0.1*complexity) combines semantic + temporal + complexity signals, but this is re-ranking of ANN results — not fusion of full-text and vector search.
- `thread_recall` uses FTS5 for seed discovery + BFS graph traversal, which is a different retrieval pattern (seeded graph walk), not BM25+vector fusion.

### Deep (incl. thinking) ❌
- No indexing of thinking/reasoning traces. `embed.py` filters with `is_embeddable()` which excludes `[tool:*]` and `[result]*` prefixes only. Claude Code's `<thinking>` blocks are not specifically captured or indexed.
- The JSONL parsing in `extract_text()` processes "text" and "tool_use" block types. There is no handling for thinking/reasoning content blocks.

### Code graph ❌
- No AST parsing, no Tree-sitter, no code structure indexing. Pure text search over conversation turns.

### Docs search ❌
- No documentation ingestion. No indexed API docs or framework references.

### Fact metadata query ❌
- No structured metadata query tool. `search_sessions` and `recent_sessions` support project/source string filters, but there's no dedicated query-by-metadata (e.g., "all turns about X", "all sessions edited file Y").
- `index_stats()` provides aggregate counts only.

### Timeline ✅
- `recall_session`: chronological replay of all turns in a session
- `recent_sessions`: reverse-chronological session listing
- `thread_recall`: BFS expansion from seed turns following TEMPORAL edges both directions
- `sessions.started_at` + `sessions.ended_at` timestamps on every session
- `turns.ts` timestamp on every turn
- `wire_edges.py`: TEMPORAL edge graph preserves chronological topology

### Search modes
- **5**: `search_sessions` (FTS5), `find_similar` (semantic/hybrid), `thread_recall` (BFS graph traversal), `recall_session` (session replay), `recent_sessions` (chronological browsing)

### Data sources
- **2**: Claude Code JSONL sessions (`~/.claude/projects/`) + claude.ai chat export (`conversations.json` via `chat_index.py`)

---

## Knowledge Lifecycle

### Decay/forgetting ✅
- `mcp_server.py:44-50`: `_W_RECENCY = 0.2` in hybrid scoring. Linear decay from 1.0 (now) to 0.0 at 365 days.
- `mcp_server.py:55-64`: `_recency_score()` function computes days-since-session-started, linearly maps to [0, 1].
- This is retrieval-level decay (reduces relevance of old results), not storage-level pruning. Qualifies under CRITERIA.md definition: "Automatically reduces relevance or removes memories based on time, disuse, or engagement signals."

### Supersede/replace ❌
- No version chain for turns or sessions. Turns are immutable once indexed. Re-indexing replaces entire session but there's no traceable update chain tracking "memory B replaces memory A".
- `index.py` reindex: `DELETE FROM turns WHERE session_id = ?` + `DELETE FROM sessions WHERE id = ?` — full replacement, not tracked supersede.

### Contradiction detect ❌
- No contradiction detection between memories.

### Quarantine ❌
- No mechanism to exclude a session's memories from retrieval without deleting.

### Auto-resolution ❌
- No automatic resolution or archival of stale items.

### Trust model ❌
- Flat source differentiation (code/chat) with no trust weighting hierarchy.

### Explicit forget ❌
- No delete/forget tool exposed via MCP. `index.py` reindex logic does DELETE+INSERT but this is rebuild, not selective forget. No `delete_session`, `delete_turn`, or `forget` tool.

---

## Extraction Pipeline

### Auto-extraction ✅
- `index.py`: Walks `~/.claude/projects/`, parses every JSONL file, extracts turns automatically — no manual save step required
- `mcp_server.py:650-790`: `reindex()` tool — re-indexes all sessions from within the MCP server, incremental (mtime check)
- `hooks/precompact_save.py`: Parses transcript on every compaction event, extracts user messages, assistant responses, files touched, bash operations
- `hooks/stop_hook_checkpoint.py`: Periodic checkpoint writes on every Stop event (end of turn)
- System automatically extracts from the JSONL record without user action

### Content-aware preproc ✅
- `embed.py:30-35`: `is_embeddable()` — filters out tool calls (`[tool:*]`), tool results (`[result]*`), text under 30 chars
- `embed.py:72`: Text truncated to 512 chars before embedding
- `index.py:extract_text()`: Tool results truncated to 500 chars, structured into `[tool:{name}]` and `[result]` prefixed annotations
- Different handling for conversational text (full capture) vs tool output (500 char cap)

### Deduplication ❌
- No deduplication. Re-indexing updates entire sessions by mtime comparison, but there's no turn-level dedup or near-duplicate merge.

### Quality refinement ❌
- No LLM-based or rule-based quality pass after extraction. No confidence scoring on extracted turns.

### Narrative generation ✅
- `mcp_server.py:437-502`: `thread_recall(query)` — BFS over TEMPORAL edges outward from FTS5 seed matches. Walks up to `max_hops=8` in both directions, groups results by session chronologically. Returns a "narrative thread, not just rows."
- Output marks seed turns with `[MATCH]`, shows surrounding context as a coherent narrative chain
- This is narrative assembly (not generation), but the thread reconstruction from seed+edges qualifies as narrative feedback

### Clustering ✅
- `wire_similar.py`: Wires `SIMILAR_TO` edges between semantically similar turns (cosine similarity ≥ 0.85 via ANN search on embeddings)
- Creates implicit clusters through the edge graph — turns within cosine 0.85 radius become connected components
- `mcp_server.py:597`: `find_similar()` returns nearest-neighbor clusters around query embedding
- Edge type `SIMILAR_TO` in edges table with weight = cosine similarity

### Recurrence detection ❌
- No cross-session pattern detection. No "you asked this before" or recurring topic identification.

### Persona extraction ❌
- No user trait extraction. No persistent persona model.

---

## Platform Support

### Claude Code ✅
- Primary integration target. README documents `~/.claude.json` MCP config + hook installation. All four hooks target Claude Code events (PreCompact, SessionStart, Stop).
- `sse_proxy.py` proxies Claude Code → Anthropic API on port 9099.

### Codex ❌
- No documentation or integration.

### OpenCode ❌
- No documentation or integration.

### Gemini CLI ❌
- No documentation or integration.

### Copilot ❌
- No documentation or integration.

### Cursor ❌
- No documentation or integration.

### Windsurf ❌
- No documentation or integration.

### OpenClaw ❌
- No documentation or integration.

### Hermes ❌
- No documentation or integration.

### pi/omp ❌
- No documentation or integration.

### Antigravity ❌
- No documentation or integration.

---

## Benchmarks

### LoCoMo ❌
- No published score.

### LongMemEval ❌
- No published score.

### PersonaMem ❌
- No published score.

### Token reduction ❌
- The system reduces context loss via compaction checkpoints, but no quantitative token savings benchmark is published.
- README references ~50 MB DB start, not token savings.

### Methodology open ❌
- No benchmark methodology published.

---

## Summary

| Category | ✅ Present | ❌ Absent |
|---|---|---|
| Architecture (11) | 4 (proxy, offline, privacy, export) | 7 |
| Data Model (14 booleans) | 1 (timeTravel) | 13 |
| Search (8 booleans) | 3 (fulltext, semantic, timeline) | 5 |
| Lifecycle (7) | 1 (decay) | 6 |
| Extraction (8) | 4 (autoExtract, contentPreproc, narrative, clustering) | 4 |
| Platform (11) | 1 (p_claude) | 10 |
| Benchmarks (5) | 0 | 5 |
| **Total (64 booleans)** | **14** | **50** |

Coverage: **14 / 64 ≈ 21.9%**

Numeric highlights: schemaFields=13, searchModes=5, dataSources=2, llmFlex=1

### Key strengths
- Genuine **SSE proxy** (rare in the comparison — monitors API stream at 70/85/95% thresholds)
- **Multi-signal semantic search** with 3-component scoring (cosine sim + recency decay + complexity bonus)
- **Thread recall** via BFS graph traversal (narrative reconstruction from seed turns, showing what led to and followed a topic)
- **Dual-source indexing** (Claude Code + claude.ai) in unified DB
- Robust **compaction resilience** via PreCompact/Stop/SessionStart hook pipeline

### Key limitations
- No structured knowledge model — everything is raw turn text, no entities/actions/tags
- No lifecycle management beyond recency decay in search scoring
- Claude Code only — no cross-platform support
- No benchmarks published
- No person-level features (persona, emotional tracking, user preferences)
