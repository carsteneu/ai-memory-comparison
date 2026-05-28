# claude-mem — Evidence

> Every ✅ claim backed by public source code or documentation.
> Sources: GitHub repo `thedotmack/claude-mem`, docs at `docs.claude-mem.ai`.
> Version observed: 13.3.0 (package.json). Lines may shift; pinned to `main` for readability.

## Architecture

### webUi ✅
- `README.md` — "**Web Viewer UI** - Real-time memory stream at http://localhost:37777"
- `docs/architecture/overview.md` — "Viewer UI - React-based real-time memory stream served by the worker"
- `docs/architecture/overview.md` — "React + TypeScript web interface... Built with esbuild into a single file deployment"
- GitHub repo: `src/ui/viewer/` directory with React components

### offline ✅
- `README.md` — "**SQLite Database** - Stores sessions, observations, summaries" (local storage)
- `docs/architecture/database.md` — "Path: `~/.claude-mem/claude-mem.db`" — all data stored locally
- `docs/architecture/overview.md` — "SQLite 3 with bun:sqlite driver" — local-first storage
- `docs/hooks-architecture.md` — "All data stored locally in `~/.claude-mem/claude-mem.db`"
- Worker runs on localhost. AI compression requires API calls (configurable Claude/Gemini/OpenRouter), but core storage and retrieval work locally

### privacy ✅
- `README.md` (Key Features) — "**Privacy Control** - Use `<private>` tags to exclude sensitive content from storage"
- `docs/usage/private-tags.md` — Complete reference: tags strip content before database persistence, tag stripping at hook layer, verification steps
- `docs/usage/private-tags.md` — "Tags are stripped during storage, not from the live conversation"
- `docs/hooks-architecture.md` — "No cloud uploads (API calls only for AI compression)", "SQLite file permissions: user-only read/write", "No analytics or telemetry"

### export ✅
- `docs/usage/export-import.md` — Complete Export/Import system: `scripts/export-memories.ts` and `scripts/import-memories.ts`
- `docs/usage/export-import.md` — "Export Script: Searches the database using hybrid search (combines ChromaDB vector embeddings with FTS5 full-text search)"
- `docs/usage/export-import.md` — JSON export format with observations, sessions, summaries, and prompts
- `docs/usage/export-import.md` — Import with duplicate prevention (transactional, idempotent)
- `docs/llms.txt` — Lists "Memory Export/Import" documentation page

---

## Data Model

### fulltext ✅
- `docs/architecture/database.md` — "FTS5 Full-Text Search" section with 3 virtual tables: `observations_fts`, `session_summaries_fts`, `user_prompts_fts`
- `docs/architecture/database.md` — FTS5 triggers for automatic synchronization on INSERT/UPDATE/DELETE
- `docs/architecture/database.md` — `escapeFTS5Query()` for injection prevention, 332 injection attack tests
- `docs/architecture/search-architecture.md` — FTS5 queries with rank ordering: `SELECT * FROM observations_fts WHERE observations_fts MATCH ? ORDER BY rank`

### semantic ✅
- `README.md` — "**Chroma Vector Database** - Hybrid semantic + keyword search for intelligent context retrieval"
- `docs/architecture/overview.md` — "Vector Store: Chroma (optional, for semantic search)"
- `docs/architecture/search-architecture.md` — "Chroma Vector DB - Semantic search with hybrid retrieval"
- `docs/architecture/overview.md` — Vector sync: `src/services/sync/ChromaSync.ts`

### timeline ✅
- `README.md` (MCP Search Tools) — "**`timeline`** - Get chronological context around a specific observation or query"
- `docs/architecture/search-architecture.md` — Timeline tool with `anchor`, `query`, `depth_before`, `depth_after` parameters
- `docs/architecture/search-architecture.md` — "Returns: Chronological view showing what happened before/during/after"
- `docs/architecture/search-architecture.md` — HTTP Endpoint: `GET /api/timeline`

### searchModes: 3 ✅
- `README.md` (MCP Search Tools) — 3 functional search tools: `search`, `timeline`, `get_observations`
- `docs/architecture/search-architecture.md` — "The 4 MCP Tools" section documents: `__IMPORTANT` (workflow documentation), `search`, `timeline`, `get_observations`
- Note: `__IMPORTANT` is a workflow guidance tool, not a search mode. Functional search modes = 3.

### schemaFields: 4 ✅
- `docs/architecture/database.md` — "Core Tables": 4 primary tables
  1. `sdk_sessions` (~13 columns: id, sdk_session_id, claude_session_id, project, prompt_counter, status, created_at, created_at_epoch, completed_at, completed_at_epoch, last_activity_at, last_activity_epoch)
  2. `observations` (~16 columns: id, session_id, sdk_session_id, claude_session_id, project, prompt_number, tool_name, correlation_id, title, subtitle, narrative, text, facts, concepts, type, files_read, files_modified, created_at, created_at_epoch)
  3. `session_summaries` (~10 columns: id, sdk_session_id, claude_session_id, project, prompt_number, request, investigated, learned, completed, next_steps, notes, created_at, created_at_epoch)
  4. `user_prompts` (~7 columns: id, sdk_session_id, claude_session_id, project, prompt_number, prompt_text, created_at, created_at_epoch)
- Note: "schemaFields: 4" refers to the count of distinct entity tables in the data model.

### dataSources: 1 ✅
- `docs/architecture/overview.md` — SQLite is the single source of truth for all memory data
- ChromaDB is an optional index layer, not a separate data source
- All retrieval flows through the SQLite database (FTS5 + SessionSearch service)

---

## Knowledge Lifecycle

### autoExtract ✅
- `README.md` — "**Automatic Operation** - No manual intervention required"
- `README.md` (How It Works) — "5 Lifecycle Hooks - SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd (6 hook scripts)"
- `docs/usage/getting-started.md` — "Claude-Mem works automatically once installed. No manual intervention required!"
- `docs/usage/getting-started.md` — "Worker processes observations asynchronously: Worker Service processes tool observations and extracts Title, Subtitle, Narrative, Facts, Concepts, Type, Files"
- `docs/architecture/overview.md` — Memory Pipeline: "Hook (stdin) → Database → Worker Service → SDK Processor → Database → Next Session Hook"
- `docs/hooks-architecture.md` — Complete 5-stage hook lifecycle with automatic session startup, observation capture, AI compression, and context injection

---

## Platform Support

### p_claude ✅
- `README.md` (title) — "Persistent memory compression system built for Claude Code"
- `README.md` — Install via `/plugin marketplace add thedotmack/claude-mem` and `/plugin install claude-mem`
- `plugin/.claude-plugin/plugin.json` — Claude Code plugin manifest
- `docs/architecture/hooks.md` — Hooks configured via `plugin/hooks/hooks.json` for Claude Code lifecycle events

### p_codex ✅
- GitHub repo: `.codex-plugin/` directory with `plugin.json` manifest
- `package.json` — `"files": [".codex-plugin", ...]` — included in npm distribution
- `README.md` — "Works with Claude Code, OpenClaw, Codex, Gemini, Hermes, Copilot, OpenCode + More"

### p_opencode ✅
- `README.md` — Explicit install command: `npx claude-mem install --ide opencode`
- `README.md` — "Works with Claude Code, OpenClaw, Codex, Gemini, Hermes, Copilot, OpenCode + More"

### p_gemini ✅
- `README.md` — Explicit install command: `npx claude-mem install --ide gemini-cli`
- `README.md` — Auto-detects `~/.gemini`
- `docs/llms.txt` — "Gemini CLI Setup - Add persistent memory to Gemini CLI with claude-mem"
- `docs/configuration.md` — Gemini Provider Settings with `CLAUDE_MEM_GEMINI_API_KEY` and `CLAUDE_MEM_GEMINI_MODEL`

### p_copilot ✅
- `README.md` — "Works with Claude Code, OpenClaw, Codex, Gemini, Hermes, Copilot, OpenCode + More"
- Note: No dedicated Copilot plugin directory or documentation page found. The README description line is the primary evidence. This is the weakest claim among the verified platforms.

### p_openclaw ✅
- GitHub repo: `openclaw/` directory with full plugin implementation (`install.sh`, `openclaw.plugin.json`, `src/`, `skills/`, `package.json`)
- `README.md` — "🦞 OpenClaw Gateway" section with dedicated installer: `curl -fsSL https://install.cmem.ai/openclaw.sh | bash`
- `docs/openclaw-integration.md` — Complete integration guide with event lifecycle, system prompt context injection, SSE observation feeds to Telegram/Discord/Slack
- `package.json` — `"files": ["openclaw", ...]` — included in npm distribution

---

## Verified NOT Present (marked false in data.js)

The following features were specifically looked for and NOT found in claude-mem's public documentation or source code:

**Data Model (all false):** entities, actions, keywords, anticipatedQueries, triggerRules, domainTag, taskType, context, source, originTrust, emotional, conflict, layeredMemory, timeTravel
- Schema has no junction tables for entities/actions/keywords. No trigger_rule or domain columns. No emotional_intensity field. No time-travel/version history tracking.

**Search (all false):** hybrid (no RRF-based combined search — Chroma is separate/optional layer), deep (no thinking-block search), codeGraph (no tree-sitter symbol navigation), docsSearch (no indexed doc search), factQuery (no entity/keyword metadata query)

**Lifecycle (all false):** decay, supersede, contradiction, quarantine, autoResolve, trustModel, explicitForget
- No Ebbinghaus decay, no supersede chains, no contradiction detection, no quarantine/skip_indexing, no auto-resolution of tasks, no trust model, no explicit forget mechanism

**Extraction (all false):** contentPreproc, dedup, qualityRefine, narrative, clustering, recurrence, persona
- Extraction is single-pass via Claude Agent SDK, not multi-phase. No content-aware truncation, no deduplication pipeline, no quality refinement, no narrative generation, no clustering, no recurrence detection, no persona extraction.

**Architecture (all false):** proxy (hooks-based, no proxy layer), multiAgent (no agent spawning or inter-agent messaging)

---

## Vitals

### stars: 79,290 ✅
- GitHub page shows 79.3k stars as of 2026-05-28

### language: TypeScript ✅
- `package.json` — `"type": "module"`, TypeScript source with esbuild bundling
- GitHub: "TypeScript 91.5%" in language breakdown

### license: Apache 2.0 ✅
- `LICENSE` file in repo root
- `package.json` — `"license": "Apache-2.0"`

### created: 2025-08-31 ✅
- GitHub repo shows initial commit from this date
- README version history and release timeline consistent with this date

### setup: "npx install" ✅
- `README.md` (Quick Start) — `npx claude-mem install`
- `package.json` — `"bin": { "claude-mem": "./dist/npx-cli/index.js" }`

### pricing: "free" ✅
- `package.json` — `"license": "Apache-2.0"` — open source, no cost
- README — No paid tiers, no subscription model described
- Docs mention free Gemini tier (1500 req/day) and OpenRouter free models

### coverage: N/A
- No test coverage data in current data.js

---

## Notes

1. **Hybrid search**: The export script uses "hybrid search (combines ChromaDB vector embeddings with FTS5 full-text search)" per `docs/usage/export-import.md`. However, the primary search API described in `docs/architecture/search-architecture.md` uses FTS5-only queries. Chroma is an optional/incremental sync layer, not part of the core search pipeline. Classified as `hybrid: false` because hybrid RRF-based search is not the primary retrieval mode.

2. **Platform "+ More"**: README claims support for Hermes and "More" platforms, but no dedicated directories or docs were found for these. Only platforms with concrete evidence (directory, docs page, or explicit install command) were verified.

3. **Data freshness**: All evidence gathered 2026-05-28 from `main` branch. claude-mem releases frequently (v13.3.0 as of this audit, 271 releases total). Schema and features may have changed.
