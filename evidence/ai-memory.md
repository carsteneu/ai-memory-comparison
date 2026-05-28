# ai-memory — Evidence

> Every ✅ claim backed by public source code or documentation.
> Audit date: 2026-05-28. Source: GitHub `akitaonrails/ai-memory` main branch (v0.5.1).

## Vital Signs

### Single binary ✅
- `README.md` — "One Rust binary runs an MCP/HTTP server." Project is 92.4% Rust with `Cargo.toml` workspace.
- `README.md` — Docker image published for `linux/amd64` and `linux/arm64`. Ships as single executable via `cargo build --release --workspace`.
- `ARCHITECTURE.md` — "ai-memory is a single Rust binary that gives AI coding agents long-term memory."
- `Cargo.toml` — Workspace crate with 8 sub-crates; builds a single `ai-memory` binary entrypoint.

---

## Architecture

### Web/TUI ✅
- `README.md` — "Built-in `/web` browser. Read-only HTML UI for the wiki - project list, folder tree, FTS5 search, markdown rendering, dark mode. Mounted on the same axum server as MCP."
- `README.md` — "Browse the wiki at `http://<server>:49374/web` - HTTP Basic dialog if auth is on, paste the token as password. Per-project tree view, rendered markdown, supersession chain visible per page."

### Offline ✅
- `README.md` — "Zero-LLM mode still gives you FTS5 search + rule-based summarisation. Add a provider when you want consolidated pages and lint contradictions."
- `ARCHITECTURE.md` — "Zero-LLM default path. LLM has opt-in via env. The system works without any provider configured."
- `ARCHITECTURE.md` — "ai-memory runs without an LLM: hooks still capture sessions, search uses FTS5, and summaries fall back to rule-based output."

### Deployment ✅
- `README.md#quick-start` — Docker quick start with `docker run`, AUR packages (`ai-memory-bin`, `ai-memory`), source build via `cargo build --release`.
- `README.md` — "The published Docker image includes `linux/amd64` and `linux/arm64` variants."
- `docs/install.md` — Full installation cookbook covering Docker, Docker Compose, Arch Linux native (AUR), source build, Windows/WSL2, curl-based hook install.

### Storage ✅
- `ARCHITECTURE.md` — Storage is `<data_dir>/wiki/` (markdown source of truth, git-versioned) + `<data_dir>/db/memory.sqlite` (SQLite derived index, WAL mode, FTS5) + `<data_dir>/raw/` (session log archives) + `<data_dir>/logs/` (rolling tracing output).
- `README.md` — "The wiki is plain markdown in a git repo - `grep`-able, openable in Obsidian, backed up with `rsync`. No vector database to babysit."

---

## Data Model

### Time-travel ✅
- `README.md` — "Supersession chain + git-versioned markdown means you can time-travel with `git log`."
- `ARCHITECTURE.md` — "Pages are versioned in place via supersession" and "supersession chain" + "git-versioned tree of markdown pages on disk."
- `ARCHITECTURE.md` — "pages" table: "Versioned wiki pages with `is_latest` + `supersedes` chain."

### Schema fields — ~6 ✅ (UNDERCOUNT — actual 10+)
- **Finding**: The pages table has at minimum: `title`, `body`, `is_latest`, `supersedes`, `pinned` (frontmatter), `access_count`, `last_accessed_at`, `superseded_at`, `embedding_provider`, `embedding_model`, `embedding_dim`, plus foreign keys `project_id`/`workspace_id`. That's 10+ structured fields per page entry, not 6.
- `ARCHITECTURE.md` — Schema description of `pages` table: "Versioned wiki pages with `is_latest` + `supersedes` chain. M8 columns: `last_accessed_at`, `access_count`, `superseded_at`. M9 cols: `embedding_provider`, `embedding_model`, `embedding_dim`."
- **Recommendation**: Update schemaFields claim from 6 to 10.

### Layered memory — SHOULD BE ✅ (FALSELY ABSENT)
- `ARCHITECTURE.md` — "Memory tiers (M8 policy)" explicitly defines: Working (current session), Episodic (30d hot → 180d cold → evict), Semantic (indefinite), Procedural (indefinite), Pinned (exempt from all decay). This is a clear hierarchical memory structure (L0 raw → L1 episodic → L2 semantic/procedural/pinned).
- `ARCHITECTURE.md` — M8 decay policy has distinct retention rules per tier: Working hard-drops on session end; Episodic decays via `salience · exp(−λΔt) + σ · log(1+access_count) · exp(−μ · days_since_access)`; Semantic only supersedeable via LLM rewrite; Procedural frequency-decays if not re-observed.
- **Recommendation**: Add `layeredMemory: true` to data.js.

---

## Search & Retrieval

### Full-text (FTS5) ✅
- `ARCHITECTURE.md` — "pages_fts: FTS5 virtual table over `(title, body)`, auto-synced by triggers."
- `ARCHITECTURE.md` — "observations_fts: FTS5 virtual table over raw observation `(title, body)`, used only as bounded fallback."
- `README.md` — "FTS5 search still works without any keys" (zero-LLM mode).
- `README.md` — "Type `memory_query X` from the agent (or `ai-memory search X` from a terminal) - FTS5 over the wiki."

### Semantic/vector ✅ (SHOULD BE CLAIMED — currently absent)
- `ARCHITECTURE.md` — "when an embedder is configured, vector cosine over `page_embeddings` joins the same RRF."
- `README.md` — "Embedding providers: Supported — OpenAI, Voyage, and Google Gemini."
- `ARCHITECTURE.md` — `page_embeddings` table: "Optional vector rows for latest pages, with `(provider, model, dim)` denormalised."
- `ARCHITECTURE.md` — "`memory_query` answers via FTS5 + link-neighbour RRF; when an embedder is configured, vector cosine over `page_embeddings` joins the same RRF."
- **Note**: Semantic/vector search is opt-in (requires embedder config) but is a documented, implemented feature. Should be moved from absent list to claimed features.

### Search modes — 3+ (UNDERCOUNT — claimed 2)
- `README.md` — `memory_query` from agent: "FTS5 over the wiki." Interactive MCP tool.
- `README.md` — `ai-memory search X` from terminal: CLI subcommand for wiki search. Listed in CLI subcommand surface.
- `README.md` — `/web` browser: "FTS5 search, markdown rendering" in the read-only HTML UI.
- `ARCHITECTURE.md` — `memory_recent`: "Most-recently-updated `is_latest=1` pages." Additional retrieval mode.
- **Count**: At least 3 distinct search modes (MCP tool, CLI subcommand, web UI), possibly 4 with `memory_recent`.
- **Recommendation**: Update searchModes claim from 2 to 3.

### Data sources — 3+ ✅
- `ARCHITECTURE.md` — Searchable data: wiki pages (FTS5), raw observations (bounded FTS5 fallback), page_embeddings (optional vector).
- **Finding**: At least 3 distinct data source types.

---

## Knowledge Lifecycle

### Supersede/replace ✅
- `ARCHITECTURE.md` — "Pages are versioned in place via supersession." Pages table has `is_latest` + `supersedes` columns for version chains.
- `README.md` — "Pages are compiled from observations at session-end (or PreCompact), not retrieved over raw logs. Supersession chain + git-versioned markdown."
- `ARCHITECTURE.md` — `memory_consolidate` tool: "LLM-driven page rewrite. `multi_page=true` for atomic fan-out." This rewrites existing pages, creating new versions that supersede old ones.

### Decay/forgetting — SHOULD BE ✅ (FALSELY ABSENT)
- `ARCHITECTURE.md` — Explicit decay parameters: `lambda = 0.02`, `sigma = 0.6`, `mu = 0.04`, `cold_threshold = 0.20`, `hard_delete_after_days = 180`. Configurable in `config.toml`.
- `ARCHITECTURE.md` — "The forget sweep runs on demand and on the server's `[maintenance]` schedule" — this is AUTOMATIC scheduled decay.
- `ARCHITECTURE.md` — Decay formula: "`salience · exp(−λΔt) + σ · log(1+access_count) · exp(−μ · days_since_access)`". Based on time, disuse, and engagement signals.
- `ARCHITECTURE.md` — M8 policy: "pages with `retention < cold_threshold` are soft-deleted; soft-deletions older than `hard_delete_after_days` with no subsequent access get purged."
- `ARCHITECTURE.md` — `memory_forget_sweep` tool: "M8 retention pass. `dry_run=true` for preview."
- **Recommendation**: Add `decay: true` to data.js.

### Explicit forget — absent ✅
- No `delete_memory` or `forget_memory` MCP tool for individual memory deletion. The `forget-sweep` is batch/automatic. `purge-project` drops entire projects atomically but not individual pages.
- **Finding**: Verified absent. No explicit per-memory forget mechanism.

### Contradiction detection — BORDERLINE
- `ARCHITECTURE.md` — `memory_lint` tool: "Rule-based + LLM contradiction findings → `wiki/_lint/`." Detects contradictions but is manually triggered, not automatic.
- **Finding**: Contradiction detection exists as a manual tool, not automatic. The absent claim is technically correct since CRITERIA.md doesn't specify automatic vs manual, but the system does have contradiction surfacing capability.

---

## Extraction Pipeline

### Auto-extraction ✅
- `README.md` — "Zero-friction capture. Lifecycle hooks fire-and-forget every prompt + tool call + session boundary. You never type `write_note`."
- `ARCHITECTURE.md` — Hook event vocabulary: `session-start`, `user-prompt`, `pre-tool-use`, `post-tool-use`, `pre-compact`, `notification`, `stop`, `session-end`. All captured automatically via lifecycle hooks.
- `ARCHITECTURE.md` — "Hooks POST observations to the server. The server serializes writes through one SQLite writer, compiles session observations into markdown pages."

### Narrative generation ✅
- `README.md` — "when the next agent starts (Claude Code, Codex, OpenCode, …) it sees a handoff with 'where you left off' already prepended."
- `ARCHITECTURE.md` — "On true `SessionEnd` events, the server synthesises a `sessions/<id>.md` summary page (rule-based, no LLM) and opens a `Handoff` row for the next agent."
- `ARCHITECTURE.md` — `memory_consolidate`: "LLM-driven page rewrite" that "rewrites that summary into a richer durable page or fans out into a multi-page batch under `concepts/`, `decisions/`, `gotchas/`."
- `ARCHITECTURE.md` — `memory_explore`: "LLM prose digest over the briefing snapshot, degrading to JSON without a provider."
- `ARCHITECTURE.md` — `memory_briefing`: "Structured counts/activity/rules/slots/recent snapshot."

---

## Platform Support

### Claude Code ✅
- `README.md` — Support Matrix: "Supported — MCP config + lifecycle hooks."
- `README.md` — Quick start uses `ai-memory install-mcp --client claude-code --apply` and `ai-memory install-hooks --agent claude-code --apply`.
- `docs/install.md` — "Claude Code: Supported. MCP + hooks, multiple providers supported."

### Codex ✅
- `README.md` — Support Matrix: "Supported — MCP config + lifecycle hooks."
- `docs/install.md` — Dedicated Codex section with MCP snippet (`~/.codex/config.toml`) and hook installation commands (`ai-memory install-hooks --agent codex --apply`).

### OpenCode ✅
- `README.md` — Support Matrix: "Supported — Remote MCP config + generated TypeScript plugin."
- `docs/install.md` — OpenCode section: "Plugin — write to `~/.config/opencode/plugins/ai-memory.ts`." "Restart OpenCode after installing or changing the plugin; plugins are loaded at startup."

### Gemini CLI ✅
- `README.md` — Support Matrix: "Supported — MCP config + lifecycle hooks."
- `docs/mcp-install.md` — Dedicated Gemini CLI section: MCP config at `~/.gemini/settings.json`, hook install via `ai-memory install-hooks --agent gemini-cli --apply`. Maps `SessionStart`, `SessionEnd`, `BeforeTool`, `AfterTool`, `PreCompress` events.
- `docs/install.md` — Gemini CLI install commands with `--client gemini-cli` and `--agent gemini-cli`.

### Cursor ✅
- `README.md` — Support Matrix: "Supported — MCP config + lifecycle hooks."
- `docs/mcp-install.md` — Dedicated Cursor section: MCP config at `.cursor/mcp.json`, hooks at `~/.cursor/hooks.json`. Maps `sessionStart`, `sessionEnd`, `beforeSubmitPrompt`, `preToolUse`, `postToolUse`, `postToolUseFailure`, `preCompact`, `stop`.

### OpenClaw ✅
- `README.md` — Support Matrix: "Supported — MCP config + native plugin lifecycle hooks."
- `docs/mcp-install.md` — Dedicated OpenClaw section: MCP config at `~/.openclaw/config.json` with `transport: streamable-http`. Native plugin with `session_start`, `session_end`, `before_prompt_build`, `before_tool_call`, `after_tool_call`, `before_compaction`, `agent_end` hooks.
- `docs/install.md` — OpenClaw install commands.

### Oh My Pi / OMP ✅
- `README.md` — Support Matrix: "Supported — `pi` / `omp` aliases for MCP config + TypeScript extension."
- `docs/mcp-install.md` — Dedicated OMP section: MCP config at `~/.omp/agent/mcp.json`, TypeScript extension at `~/.omp/agent/extensions/ai-memory.ts`. Maps OMP lifecycle events + `before_agent_start` for handoff injection.
- `docs/install.md` — OMP install commands with `--client pi`/`--client omp` and `--agent omp`/`--agent pi` aliases.

### Antigravity CLI ✅
- `README.md` — Support Matrix: "Supported — MCP config (`serverUrl`) + lifecycle hooks (`agy` alias)."
- `docs/mcp-install.md` — Dedicated Antigravity CLI section: MCP config at `~/.gemini/antigravity-cli/mcp_config.json` with `serverUrl` key. Hooks at `~/.gemini/config/hooks.json` in named-groups format. Maps `PreInvocation`, `PreToolUse`, `PostToolUse`, `Stop` events.
- `docs/install.md` — Antigravity CLI install commands with `--client antigravity-cli` and `--agent antigravity-cli`.

---

## Absent features verified (confirmed —)

All below confirmed absent from public README, ARCHITECTURE.md, install.md, and mcp-install.md:

- **proxy**: Hooks POST observations to server; no in-flight LLM conversation stream interception.
- **multiAgent**: System supports multi-agent use (different CLIs) but no agent orchestration/swarm.
- **entities**: No entity extraction or structured entity storage.
- **actions**: No structured action/command extraction fields.
- **keywords/tags**: No explicit keyword or tag system. Wiki pages use frontmatter (`pinned`) but no keyword/tag taxonomy.
- **anticipatedQueries**: No predicted search query generation.
- **triggerRules**: No condition-based memory activation triggers.
- **domainTag**: No domain category tagging (code/marketing/legal etc).
- **taskType**: No task type classification (task/idea/blocked/stale).
- **context (why)**: No explicit "why this memory matters" field.
- **source attribution**: `ObservationKind` enum exists but no multi-level source attribution (user/agent/extraction).
- **originTrust**: No trust weighting by memory origin.
- **emotional**: No sentiment or emotional intensity tracking.
- **deep**: No search across model thinking/reasoning traces.
- **codeGraph**: No Tree-sitter/AST code structure indexing.
- **docsSearch**: No dedicated framework/API documentation search.
- **factQuery**: No structured metadata query tool.
- **timeline**: Audit log exists but no dedicated chronological search/browse tool with `since`/`before`.
- **quarantine**: No session quarantine mechanism.
- **autoResolve**: No automatic stale task resolution.
- **trustModel**: No multi-tier trust hierarchy.
- **contentPreproc**: No content-aware truncation before extraction.
- **dedup**: No duplicate memory detection/merging.
- **qualityRefine**: No LLM-based post-extraction quality pass.
- **clustering**: No semantic clustering of memories.
- **recurrence**: No recurrence detection across sessions.
- **persona**: No user persona/trait extraction.

---

## Summary of corrections needed in data.js

| Feature | Current | Correct | Evidence |
|---------|---------|---------|----------|
| `schemaFields` | 6 | **10** | pages table has title, body, is_latest, supersedes, pinned, access_count, last_accessed_at, superseded_at, embedding_provider, embedding_model, embedding_dim (10+) |
| `searchModes` | 2 | **3** | memory_query (MCP), ai-memory search (CLI), /web browser search |
| `layeredMemory` | — (absent) | **✅** | M8 policy: Working/Episodic/Semantic/Procedural/Pinned tiers |
| `decay` | — (absent) | **✅** | M8 scheduled forget sweep with configurable decay formula |
| `semantic` | — (absent) | **✅** | Optional vector search via page_embeddings + embedder config |

**Additional note**: `conflict` (contradiction detection via `memory_lint`) is borderline — the tool exists but is manual, not automatic.
