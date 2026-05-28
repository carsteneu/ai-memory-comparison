# Fullerenes — Evidence

> Every ✅ claim backed by public README, npm registry, or GitHub repo.
> Audit date: 2026-05-28. Source: GitHub `codebreaker77/Fullerenes` main branch, npm `fullerenes@0.1.4`.

## Vitals

### Stars ✅ — 19
- GitHub repo shows 19 stars, 4 forks, 1 watcher.

### Language ✅ — TypeScript (98.7%)
- GitHub language breakdown: TypeScript 98.7%, JavaScript 1.3%.
- `package.json`: monorepo with `turbo`, `typescript`, workspaces in `packages/*`.

### License ✅ — MIT
- `README.md`: "License — MIT".
- `package.json`: `"license": "MIT"`.

### Single binary — ❌
- npm package with 3 sub-packages (`fullerenes`, `fullerenes-core`, `fullerenes-daemon`). Not a single binary.

### Created — ~2026-04-25
- npm registry `_npmOperationalInternal` timestamp: `1777300264997` (epoch ms) → approximately April 2026.
- GitHub: 11 commits on main, no releases published.

---

## Architecture

### Deployment ✅ — Local CLI + MCP
- `README.md`: "Local-first CLI, MCP server, and agent-context file generation".
- CLI commands: `init`, `index`, `query`, `stats`, `mcp`, `watch`.
- `npx fullerenes mcp .` starts local MCP server.

### Storage ✅ — SQLite (graph.db)
- `README.md`: `fullerenes init` creates `.fullerenes/graph.db`.
- `fullerenes-core` description: "Parser engine, SQLite graph storage, incremental indexer, and query layer".

### Integration ✅ — MCP + generated agent files
- MCP tools: `query_codebase`, `get_function`, `find_entry_points`, `get_file_context`, `search_code`, `get_callers`, `predict_impact`, `get_stats`, `get_subgraph`.
- `README.md`: "For Claude Code: `claude mcp add fullerenes -- npx fullerenes mcp .`"
- `README.md`: "For Codex Desktop or another MCP client, register a stdio MCP server"
- `fullerenes init` generates: `CLAUDE.md`, `AGENTS.md`, `.cursor/rules/fullerenes.mdc`.

### Proxy — ❌
- No proxy architecture mentioned. Direct MCP stdio connection.

### Web/TUI — ❌
- No web UI or TUI mentioned.

### Offline ✅
- `README.md` comparison table: "Works offline: Yes", "Zero hosted infra required: Yes".
- "fully local-first generated summaries with no external LLM dependency".
- Tree-sitter parses locally, SQLite stores locally. No API calls needed.

### Multi-agent — ❌
- No multi-agent coordination, cross-session sharing, or agent-to-agent communication mentioned.

### LLM providers ✅ — 0 (no LLM dependency)
- `README.md` "What's New": "fully local-first generated summaries with no external LLM dependency".
- The system uses Tree-sitter for code parsing and rule-based summary generation. No LLM provider configuration exists. This is a deliberate architectural choice — deterministic, offline, no API keys.

### Cache optimization — ❌
- No token caching or context optimization beyond targeted retrieval via graph queries.

### Privacy/encryption ✅
- Fully local. No cloud, no hosted infra. "Zero hosted infra required". All data stays on disk as `.fullerenes/graph.db`.

### Data export — ❌
- No export/import functionality mentioned.

### Setup ✅ — `npm install -g`
- `README.md`: `npm install -g fullerenes` or `npx fullerenes init`.

### Pricing ✅ — free
- MIT license, OSS. No pricing tiers, no cloud service.

---

## Data Model

### Storage unit — Code symbol (func/class/import)
- `README.md`: "turns a source tree into a local knowledge graph". Tree-sitter parses source into functions, classes, imports, and call relationships stored in SQLite.

### Entities ✅
- Tree-sitter parses functions, classes, imports as graph nodes. Tools: `get_function`, `find_entry_points`, `get_callers`, `get_subgraph`. Graph has typed nodes (function, class, module).

### Actions — ❌
- No action/operation tracking. System indexes static code structure, not runtime behavior.

### Keywords/tags — ❌
- No manual tagging or keyword assignment.

### Anticipated queries — ❌
- No anticipated-query metadata field.

### Trigger rules — ❌
- No conditional retrieval triggers.

### Domain tag — ❌
- No domain categorization.

### Task type — ❌
- No task tracking.

### Context (why) — ❌
- No "why" or rationale field. Stores code structure, not developer intent.

### Source attribution — ❌
- No provenance tracking for graph entries.

### Origin + trust — ❌
- No trust scoring or origin metadata.

### Emotional — ❌
- Not applicable.

### Conflict surfacing — ❌
- No conflict detection between knowledge entries.

### Layered memory — ❌
- Single-layer code graph. No working/session/long-term layers.

### Time-travel — ❌
- No historical versioning. Watch mode keeps graph current; old state is overwritten.

### Schema fields — ~8
- Per symbol: name, kind (function/class/import), file path, start line, end line, signature/prototype, callers list, callees/dependents. ~8 structured fields in the graph schema.

---

## Search & Retrieval

### Full-text ✅
- Inferred from `query_codebase` tool accepting natural language questions ("how does authentication work", "where is watch mode implemented"). Graph stores symbol names, doc comments, signatures — searchable via SQLite.

### Semantic/vector — ❌
- No embedding or vector storage mentioned. "fully local-first generated summaries with no external LLM dependency" — no embeddings model. "Natural-language retrieval" likely uses text matching against symbol names and doc comments in SQLite, not vector similarity.

### Hybrid (BM25+Vec) — ❌
- No vector DB, no BM25+vector fusion mentioned.

### Deep (incl. thinking) — ❌
- No thinking trace or chain-of-thought storage.

### Code graph ✅ — PRIMARY FEATURE
- `README.md`: "turns a source tree into a local knowledge graph". Tree-sitter parses repo into SQLite with functions, classes, imports, call relationships.
- MCP tools: `query_codebase`, `get_function`, `find_entry_points`, `get_file_context`, `search_code`, `get_callers`, `predict_impact`, `get_stats`, `get_subgraph`.
- `README.md`: `predict_impact({ functionName: "resetCache" })` — blast radius analysis from call graph.
- CLI: `npx fullerenes query "how does authentication work"` — NL codebase queries.
- CLI: `npx fullerenes query "where is watch mode implemented" --budget 1200` — token-budgeted queries.
- Comparison table: "Caller and impact inspection: Yes", "Token-budgeted query output: Yes", "Local SQLite graph: Yes".
- Comparison column: "Raw file prompting" gets "No" on caller/impact inspection and SQLite graph; "Generic graph tooling" gets "Varies".
- Files generated: `CLAUDE.md`, `AGENTS.md`, `.cursor/rules/fullerenes.mdc` — inject graph context into agent instructions.

### Docs search — ❌
- No external documentation indexing. Only source code is indexed.

### Fact metadata query — ❌
- No structured metadata query layer beyond code graph traversal.

### Timeline view — ❌
- No chronological or historical browsing.

### Search modes — 9
- MCP tools (9): `query_codebase`, `get_function`, `find_entry_points`, `get_file_context`, `search_code`, `get_callers`, `predict_impact`, `get_stats`, `get_subgraph`.
- CLI also has `query` with `--budget` and `--json`, `stats`.

### Data sources — 1
- Single data source: the SQLite code graph (`.fullerenes/graph.db`). No external docs, no web, no conversation logs.

---

## Knowledge Lifecycle

### All lifecycle features — ❌
- **Decay/forgetting**: ❌ — No forgetting mechanism. Graph is statelessly regenerated from source.
- **Supersede/replace**: ❌ — Incremental reindexing replaces old graph state. No version chains.
- **Contradiction detect**: ❌ — No contradiction detection.
- **Quarantine**: ❌ — No quarantine mechanism.
- **Auto-resolution**: ❌ — No automatic conflict resolution.
- **Trust model**: ❌ — No trust scoring.
- **Explicit forget**: ❌ — No delete/forget API. Graph is regenerated on reindex; no selective removal.

Fullerenes is a code index, not a memory system with knowledge lifecycle management. The graph is always a live reflection of the current source tree.

---

## Extraction Pipeline

### Auto-extraction ✅
- `fullerenes init` auto-parses entire repo via Tree-sitter into SQLite graph. No manual tagging.
- `fullerenes watch` auto-reindexes on file changes.
- `fullerenes index` triggers manual reindex.

### Content-aware preprocessing — ❌
- Tree-sitter does AST parsing (content-aware in the parsing sense), but the "content-aware preproc" feature in CRITERIA.md refers to LLM-driven content categorization/structuring before storage (e.g., ByteRover's context tree). Fullerenes uses deterministic parsing, not LLM-based preprocessing.

### Deduplication — ❌
- No deduplication mentioned. Each reindex regenerates graph from scratch.

### Quality refinement — ❌
- "fully local-first generated summaries with no external LLM dependency". Summaries are rule-based from AST, no quality refinement pass.

### Narrative generation — ❌
- No narrative summaries. Code structure only.

### Clustering — ❌
- No entity clustering.

### Recurrence detection — ❌
- No pattern recurrence detection.

### Persona extraction — ❌
- No user persona modeling.

---

## Platform Support

### Claude Code ✅
- `README.md`: "For Claude Code: `claude mcp add fullerenes -- npx fullerenes mcp .`"
- Generates `CLAUDE.md` with graph usage instructions.

### Codex ✅
- `README.md`: "For Codex Desktop or another MCP client, register a stdio MCP server with: `npx fullerenes mcp /absolute/path/to/project`"

### Cursor ✅
- Generates `.cursor/rules/fullerenes.mdc` on `fullerenes init`.

### Other platforms — ❌
- No explicit mention of OpenCode, Gemini CLI, Copilot, Windsurf, OpenClaw, Hermes, pi/omp, or Antigravity integrations.
- Note: as a generic MCP stdio server, Fullerenes technically works with any MCP-compatible client, but only Claude Code and Codex are explicitly documented.

---

## Benchmarks

### Token reduction ✅ — "64% (SWE-bench), 94.4% (local)"
- `README.md` "SWE-bench Verified smoke comparison": 91,949 tokens (baseline) → 32,945 tokens (Fullerenes) = 64.2% reduction on a single SWE-bench instance (`sympy__sympy-20590`). Same fix, same files touched.
- `README.md` "Local repo context compression": 2,452 tokens (raw files) → 137 tokens (Fullerenes query) = 94.4% reduction on local benchmark.
- Methodology caveat from README: token estimate uses heuristic `1 token ~= 4 characters`. Benchmark artifacts are "preliminary and intended as transparent early validation". Not enough data for broad SWE-bench claims.

### Methodology open ✅
- `README.md` explicitly describes token estimation heuristic (`1 token ~= 4 characters`), benchmark methodology, and notes preliminary nature of results. No hidden methodology.

### Other benchmarks — all ❌
- No LoCoMo, LongMemEval, PersonaMem results.

---

## Claims correctly absent (verified no public evidence)

**Architecture:** proxy, webUi, multiAgent, cacheOpt, export — all ❌.

**Data Model:** actions, keywords, anticipatedQueries, triggerRules, domainTag, taskType, context, source, originTrust, emotional, conflict, layeredMemory, timeTravel — all ❌ (Fullerenes is a code index, not a general memory system — these structured metadata fields have no analog in a code graph).

**Search:** semantic, hybrid, deep, docsSearch, factQuery, timeline — all ❌.

**Lifecycle:** ALL false — Fullerenes has no knowledge lifecycle management. It's a live code index, not a memory system.

**Extraction:** contentPreproc, dedup, qualityRefine, narrative, clustering, recurrence, persona — all ❌.

**Platform:** OpenCode, Gemini CLI, Copilot, Windsurf, OpenClaw, Hermes, pi/omp, Antigravity — all ❌ (no explicit docs, though MCP technically works with any client).

**Benchmarks:** b_locomo, b_longmemeval, b_personamem — all "—".

---

## Audit Notes

1. **Not a general memory system**: Fullerenes is a specialized code-indexing tool, not a general-purpose agent memory system. It indexes static code structure (functions, classes, imports, call graphs) via Tree-sitter, and has zero conversation memory, session tracking, or knowledge lifecycle features. This explains why nearly all Data Model, Lifecycle, and Extraction Pipeline features are absent.

2. **llmFlex = 0 is a design choice**: Fullerenes deliberately uses no LLM. Summary generation is rule-based from Tree-sitter ASTs. This makes it deterministic, fully offline, and API-key-free — a differentiating characteristic compared to every other system in the comparison.

3. **codeGraph is the primary strength**: 9 MCP tools for graph queries (symbol lookup, call tracing, impact analysis, subgraph traversal). The 64% SWE-bench token reduction comes from replacing raw file reading with targeted graph queries.

4. **searchModes = 9**: All 9 listed MCP tools are distinct code-graph retrieval operations. While all fall under "code graph" conceptually, they represent different query shapes (NL search, symbol lookup, caller tracing, impact prediction, entry point discovery, etc.).

5. **Platform reach via MCP**: As a generic MCP stdio server, Fullerenes technically works with any MCP client. Only Claude Code and Codex are explicitly documented. Cursor integration is via generated `.cursor/rules/fullerenes.mdc` file, not MCP.

6. **No releases published**: GitHub shows no releases, only npm packages. The repo has 11 commits and is actively being developed.

7. **Token reduction benchmark caveat**: The 64% SWE-bench number is from a single instance (`sympy__sympy-20590`), not a full benchmark run. The README explicitly notes "not enough data yet to claim broad SWE-bench improvements". b_token entry should note "64% (1 instance)".
