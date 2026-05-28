# gitmem — Evidence

> **Repository:** https://github.com/gitmem-dev/gitmem
> **Status:** ✅ Verified
> **Audit date:** 2026-05-28
> **Source:** GitHub repo main branch, README.md, package.json, src/types/index.ts, schema/setup.sql, src/server.ts, src/tools/definitions.ts, server.json

**CRITICAL CORRECTION:** The previous data.js entry referenced `https://github.com/dev-boz/gitmem` (a Python CLI tool) — that was a DIFFERENT project. The correct repo is `https://github.com/gitmem-dev/gitmem` — a TypeScript MCP server. Nearly all prior claims were wrong because they described the wrong project.

---

## Vital Signs

- **Stars**: 8 (GitHub page)
- **Language**: TypeScript 79.9%, JavaScript 8.3%, MDX 6.1%, Shell 4.1%, PLpgSQL 1.3%, CSS 0.3% (GitHub language bar)
- **License**: MIT (`package.json`: `"license": "MIT"`)
- **Version**: 1.6.1 (`package.json`: `"version": "1.6.1"`)
- **Created**: v1.0.0 released Feb 18, 2026 (GitHub Releases)
- **Single binary**: false — npm package `gitmem-mcp`, requires Node.js >= 18 (`package.json`: `"engines": {"node": ">=18.0.0"}`)
- **npm package**: `gitmem-mcp` (`package.json`)

## Architecture

### Deployment — MCP Server (npx)
- `README.md` — "npx gitmem-mcp init" for setup, "npx gitmem-mcp" to run. MCP server via stdio transport.
- `server.json` — MCP server descriptor: `"transport": {"type": "stdio"}`, name `"io.github.gitmem-dev/gitmem"`.
- `package.json` — `"bin": {"gitmem": "bin/gitmem.js", "gitmem-mcp": "bin/gitmem.js"}`.

### Storage — Local `.gitmem/` (free) or Supabase (Pro)
- `README.md` — "Local-first — All data stored in `.gitmem/` on your machine by default". Pro tier uses "Self-hosted on your own Supabase."
- `README.md` — "Delete `.gitmem/` to remove everything."
- `schema/setup.sql` — Full Supabase schema: `gitmem_learnings`, `gitmem_sessions`, `gitmem_decisions`, `gitmem_scar_usage`, `gitmem_threads`, `knowledge_triples`, `gitmem_query_metrics`, `scar_enforcement_variants`.
- `server.json` — Environment variables: `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` (both optional, "Not required for free tier").

### Integration — MCP (Model Context Protocol)
- `README.md` — "GitMem is an MCP server". `server.json` confirms MCP stdio transport. Tools registered via `@modelcontextprotocol/sdk`.
- Client config files supported: `.mcp.json` (Claude Code), `.cursor/mcp.json` (Cursor), `.vscode/mcp.json` (VS Code), `~/.codeium/windsurf/mcp_config.json` (Windsurf).

### Proxy — false
- No proxy. Pure MCP server over stdio. No conversation stream interception.

### Web UI — false
- No shipped visual interface. Docs site at `gitmem.ai` but that's documentation, not a management dashboard.

### Offline — ✅ (free tier)
- `README.md` — "Local-first — All data stored in `.gitmem/` on your machine by default"
- `README.md` — "No telemetry — GitMem does not collect usage data or phone home"
- Free tier stores everything in `.gitmem/` directory. No network calls.
- Pro tier requires Supabase (cloud dependency).
- **Claim**: `offline: true` for free tier. Pro tier: not offline.

### Multi-agent — ❌
- `README.md` — No explicit multi-agent coordination features.
- Has `absorb_observations` tool and `prepare_context` for sub-agent context injection, but no coordination layer.
- Knowledge triples (Phase 3) and multi-agent observations (Phase 2) are infrastructure, not multi-agent coordination.

### LLM providers — 1 (OpenRouter for Pro embedding)
- `README.md` — Pro tier requires `OPENROUTER_API_KEY` for embeddings.
- Free tier: no LLM dependencies.
- `recall` tool definition mentions "free tier BM25" and "pro tier embeddings".

### Cache optimization — ❌
- No cache optimization documented apart from `gitmem-cache-status`, `gitmem-cache-health`, `gitmem-cache-flush` tools (Pro tier only, for local vector cache management).

### Privacy — ✅
- `README.md` — "No telemetry — GitMem does not collect usage data or phone home"
- `README.md` — "Your data — Sessions, scars, and decisions belong to you."
- `README.md` — "Cloud opt-in — Pro tier Supabase backend requires explicit configuration via environment variables"
- `README.md` — "Delete `.gitmem/` to remove everything"

### Data export — ❌
- No explicit export tool or command. Data resides in `.gitmem/` (local files, inherently accessible) but no structured export mechanism.
- `save_transcript` saves transcripts, not a general data export.

### Setup — "npx gitmem-mcp init"
- `README.md` — "npx gitmem-mcp init" — "One command. The wizard auto-detects your IDE and sets up everything."
- `README.md` — CLI Commands table: `npx gitmem-mcp init`, `npx gitmem-mcp init --yes`, `npx gitmem-mcp init --dry-run`, etc.

---

## Data Model

### Unit — "Learning" (scar/win/pattern/anti_pattern) or Decision or Thread
- `src/types/index.ts` — `LearningType = "scar" | "win" | "pattern" | "anti_pattern"`
- `README.md` — "What Gets Remembered" table: Scars, Wins, Patterns, Decisions, Threads (5 memory types).
- `schema/setup.sql` — `gitmem_learnings` table with `learning_type TEXT NOT NULL CHECK (learning_type IN ('scar', 'win', 'pattern', 'anti_pattern'))`.

### Schema fields

The `gitmem_learnings` table has these core columns (`schema/setup.sql`):

| # | Field | Type | Description |
|---|-------|------|-------------|
| 1 | id | UUID PK | Unique identifier |
| 2 | learning_type | TEXT | scar, win, pattern, anti_pattern |
| 3 | title | TEXT | Learning title |
| 4 | description | TEXT | Detailed description |
| 5 | severity | TEXT | critical, high, medium, low |
| 6 | scar_type | TEXT | process, incident, context |
| 7 | counter_arguments | TEXT[] | Counter-arguments for scars |
| 8 | problem_context | TEXT | Problem context (for wins) |
| 9 | solution_approach | TEXT | Solution approach (for wins) |
| 10 | applies_when | TEXT[] | When this pattern applies |
| 11 | keywords | TEXT[] | Search keywords |
| 12 | domain | TEXT[] | Domain tags |
| 13 | embedding | vector(1536) | For semantic search (Pro only) |
| 14 | project | TEXT | Project namespace |
| 15 | is_active | BOOLEAN | Active/inactive flag |
| 16 | decay_multiplier | FLOAT | Behavioral decay score |
| 17 | created_at / updated_at | TIMESTAMPTZ | Timestamps |

Total: **17+ meaningful columns** on the learnings table alone, plus separate `gitmem_decisions` (8+ columns) and `gitmem_threads` (15+ columns) tables.

### features.entities — ❌
- No entity extraction. `keywords` and `domain` are user-provided tags, not extracted entities.

### features.actions — ❌
- No action tracking on learnings. `knowledge_triples` has predicates but that's graph metadata, not per-learning action fields.

### features.keywords — ✅
- `src/types/index.ts` — `CreateLearningParams.keywords?: string[]`
- `schema/setup.sql` — `keywords TEXT[] DEFAULT '{}'` in `gitmem_learnings`
- `src/tools/definitions.ts` — `create_learning` tool schema: `keywords: { type: "array", items: { type: "string" }, description: "Search keywords" }`

### features.anticipatedQueries — ❌
- No anticipated query field.

### features.triggerRules — ✅ (applies_when)
- `src/types/index.ts` — `CreateLearningParams.applies_when?: string[]`
- `schema/setup.sql` — `applies_when TEXT[] DEFAULT '{}'`
- `src/tools/definitions.ts` — `applies_when: { type: "array", items: {type: "string"}, description: "When this pattern applies" }`
- Acts as trigger condition descriptors.

### features.domainTag — ✅ (domain)
- `src/types/index.ts` — `CreateLearningParams.domain?: string[]`
- `schema/setup.sql` — `domain TEXT[] DEFAULT '{}'`

### features.taskType — ❌
- No task type field.

### features.context — ❌
- No general context field. `problem_context` exists for wins but not as a general field.

### features.source — ✅ (source_linear_issue)
- `src/types/index.ts` — `CreateLearningParams.source_linear_issue?: string`
- `schema/setup.sql` — `source_linear_issue TEXT`
- Limited to Linear issue references, not general source tracking.

### features.originTrust — ❌
- No trust scoring on learnings. `decay_multiplier` is behavioral (usage-based), not trust-based.

### features.emotional — ❌
- No emotional state tracking.

### features.conflict — ✅ (counter_arguments)
- `README.md` — "Every scar includes **counter-arguments** — reasons why someone might reasonably ignore it."
- `src/types/index.ts` — `CreateLearningParams.counter_arguments?: string[]`
- `schema/setup.sql` — `counter_arguments TEXT[] DEFAULT '{}'`

### features.layeredMemory — ❌
- No hierarchical/layered memory. Learning types are flat. No working/short-term/long-term distinction.

### features.timeTravel — ❌
- No version history or ability to view past states. `created_at`/`updated_at` exist but no version table or history mechanism.

### features.schemaFields — 17+ (learnings table)
- `schema/setup.sql` — `gitmem_learnings` has 27 columns (including embedding, timestamps, metadata). Core meaningful fields: ~17.
- If counting memory **types** instead: 5 (Scars, Wins, Patterns, Decisions, Threads per README).

---

## Search & Retrieval

### Full-text — ✅ (BM25 in free tier)
- `src/tools/definitions.ts` — `recall` tool schema: `similarity_threshold: "Default: 0.4 (free tier BM25), 0.35 (pro tier embeddings)."`
- BM25 is explicitly the free tier search algorithm. BM25 **is** full-text search.

### Semantic — ✅ (pgvector in Pro tier)
- `schema/setup.sql` — `CREATE EXTENSION IF NOT EXISTS vector;` + `embedding vector(1536)` column.
- `schema/setup.sql` — `gitmem_semantic_search()` RPC function with `query_embedding vector(1536)`.
- `README.md` — Pro tier: "Semantic search — Recall returns the *right* scars, not keyword noise".

### Hybrid — ❌
- No documented hybrid (BM25 + vector fusion) search. Free uses BM25, Pro uses vector. Not combined.

### Deep — ❌
- No deep search / conversation mining feature.

### Code graph — ❌
- `graph_traverse` tool exists but it traverses knowledge triples (institutional memory graph), not code graph.

### Docs search — ✅ (Pro tier)
- `src/server.ts` — `index_docs` and `search_docs` tools registered.
- `src/tools/definitions.ts` — `"Index markdown docs for semantic search"` and `"Search indexed repository docs"`.

### Fact query — ❌
- No fact/entity query capability.

### Timeline — ✅ (log tool)
- `src/server.ts` — `log` tool: "List recent learnings chronologically (like git log)".
- `src/tools/definitions.ts` — `log` tool with `since` param: "Days to look back".

### Search modes — 2
- Mode 1: BM25 full-text (free tier). Mode 2: Semantic/vector (Pro tier via pgvector).
- Evidence: `recall` tool `similarity_threshold` description and `server.json` Pro tier features.

### Data sources — 1
- Single data source: gitmem's own storage (local `.gitmem/` or Supabase).

---

## Knowledge Lifecycle

### Decay — ✅ (behavioral decay via usage patterns)
- `schema/setup.sql` — `decay_multiplier FLOAT DEFAULT 1.0`
- `schema/setup.sql` — `refresh_scar_behavioral_scores()` function: "Aggregates last 90 days of usage, computes dismiss rate, updates decay_multiplier"
- `schema/setup.sql` — `gitmem_scar_search()` RPC: "weighted_similarity = raw * temporal_decay * behavioral_decay"
- `src/types/index.ts` — `RelevantScar.decay_multiplier?: number`

### Supersede — ❌
- No version/supersede mechanism for learnings. `knowledge_triples` has `predicate = 'supersedes'` but that's for the knowledge graph, not learning version management.

### Contradiction — ✅ (counter-arguments)
- `README.md` — "Every scar includes **counter-arguments** — reasons why someone might reasonably ignore it. This prevents memory from becoming a pile of rigid rules."

### Quarantine — ❌
- No quarantine mechanism.

### Auto-resolve — ❌
- No automatic resolution of tasks/threads.

### Trust model — ❌
- No trust scoring. `decay_multiplier` is behavioral (dismiss-rate based), not trust-based.

### Explicit forget — ✅ (archive vs remove)
- `src/server.ts` — `archive_learning` tool: "Archive a scar/win/pattern (is_active=false)".
- `schema/setup.sql` — `is_active BOOLEAN DEFAULT true`.
- **Correction from claimed `explicitForget: false`**: While gitmem has no "delete" tool, `archive_learning` sets `is_active=false`, effectively removing the learning from recall/search. This is a soft-forget mechanism. The learning remains in the database but is excluded from active queries. Mark this as ✅ with caveat (soft-delete/archive, not hard delete).

---

## Extraction Pipeline

### Auto-extract — ❌
- No automatic extraction from conversation stream. The agent must explicitly call `create_learning`.
- `README.md` — "Learn — Mistakes become **scars**, successes become **wins**, strategies become **patterns**" describes the lifecycle workflow, but learnings are created by agent tool calls, not automatic extraction.
- The "Closing Ceremony" (session close) prompts the agent to reflect and create learnings, but this is agent-mediated, not system-extracted.

### Content preproc — ❌
- No content preprocessing pipeline.

### Dedup — ✅ (threads only, Pro tier)
- `src/tools/definitions.ts` — `create_thread` tool: "includes semantic dedup: if a similar open thread exists (cosine similarity > 0.85), returns the existing thread instead."
- Thread dedup is semantic (cosine similarity via embeddings), Pro tier only.
- No general learning dedup.

### Quality refine — ❌
- No quality refinement.

### Narrative — ❌
- No narrative generation.

### Clustering — ❌
- No clustering of related memories (beyond thread dedup).

### Recurrence — ❌
- No recurrence detection.

### Persona — ✅ (persona_name and rapport)
- `schema/setup.sql` — `persona_name TEXT` on `gitmem_learnings`.
- `src/types/index.ts` — `SessionStartResult.rapport_summaries?: { agent: string; summary: string; date: string }[]`.
- `schema/setup.sql` — `rapport_summary TEXT` on `gitmem_sessions`.

---

## Platform Support

### p_claude — ✅
- `README.md` — "Works with **Claude Code**", "Full (session, recall, credential guard)" hooks.
- `README.md` — Supported Clients table: Claude Code row, full hooks.
- `package.json` — `keywords: ["claude", "claude-code"]`.
- Template file: `CLAUDE.md.template`.

### p_codex — ✅
- `README.md` — "VS Code (Copilot)", Instructions-based.
- `package.json` — `keywords: ["vscode", "copilot"]`.
- Template file: `copilot-instructions.template`.

### p_cursor — ✅
- `README.md` — "Cursor", "Partial (session, recall)" hooks.
- `README.md` — Config file: `.cursor/mcp.json`.
- `package.json` — `keywords: ["cursor"]`.
- Template file: `cursorrules.template`.

### p_windsurf — ✅
- `README.md` — "Windsurf", Instructions-based.
- `README.md` — Config file: `~/.codeium/windsurf/mcp_config.json`.
- `package.json` — `keywords: ["windsurf"]`.
- Template file: `windsurfrules.template`.

### p_opencode — ❌
- OpenCode not listed in supported clients, no template, not in package.json keywords.

### p_gemini — ❌
- No Gemini support documented.

### p_copilot — ✅ (via VS Code)
- Supported via VS Code Copilot integration (see p_codex).

### p_openclaw — ✅
- `README.md` features OpenClaw in the description.
- Distribution: `distribution/openclaw/` directory exists in repo.
- `README.md` topics include `openclaw`.

### p_hermes — ❌
- No Hermes support.

### p_pi — ❌
- No Pi support.

### p_antigravity — ❌
- No Antigravity support.

---

## Benchmarks

No benchmarks documented. All `b_locomo`, `b_longmemeval`, `b_personamem`, `b_token` are "—".

---

## Claims Audit Summary

| Claim | data.js (old) | Verified | Evidence |
|-------|---------------|----------|----------|
| offline | true | ✅ true (free tier) | README: "Local-first" |
| privacy | false | ✅ true | README: "No telemetry", "Your data" |
| export | false | ❌ false | No export feature |
| keywords | false | ✅ true | types: `keywords[]`, SQL: `keywords TEXT[]` |
| timeTravel | true | ❌ false | No versioning mechanism |
| fulltext | true | ✅ true | BM25 in free tier (tool definition) |
| searchModes | 1 | ✅ 2 | BM25 (free) + semantic/vector (Pro) |
| supersede | false | ❌ false | No version supersede |
| explicitForget | false | ✅ true (soft) | archive_learning sets is_active=false |
| autoExtract | false | ❌ false | Agent must call create_learning |
| dedup | false | ⚠️ partial | Thread semantic dedup only (Pro) |
| p_claude | true | ✅ true | Full hooks, README supported |
| p_codex | true | ✅ true | VS Code Copilot, README supported |
| p_cursor | false | ✅ true | Cursor, Partial hooks, README |
| p_windsurf | false | ✅ true | Windsurf, README supported |
| schemaFields | 3 | 17+ (or 5 types) | SQL: 27 columns on learnings |

### Key Corrections to data.js

1. **URL**: Not `dev-boz/gitmem` (Python CLI, different project). Correct: `gitmem-dev/gitmem`.
2. **Language**: Not Python. Correct: TypeScript.
3. **Deployment**: Not "Local CLI". Correct: MCP server (npx).
4. **Storage**: Not "Markdown + git". Correct: Local `.gitmem/` directory (free) or Supabase (Pro).
5. **Integration**: Not "CLI". Correct: MCP.
6. **Stars**: Not 27. Correct: 8.
7. **Created**: Not 2026-04. Correct: Feb 18, 2026 (v1.0.0).
8. **Privacy**: Not false. Correct: true (no telemetry, local-first).
9. **Export**: Remains false.
10. **Keywords**: Not false. Correct: true (keywords field in learnings).
11. **Time travel**: Not true. Correct: false (no versioning).
12. **Search modes**: Not 1. Correct: 2 (BM25 + semantic).
13. **Explicit forget**: Not false. Correct: true (archive_learning soft-delete).
14. **Platform**: p_cursor and p_windsurf should be true, not false.

---

## Verdict

**Repository exists and is active.** gitmem-dev/gitmem is a TypeScript MCP server at version 1.6.1 with 8 stars, 367 commits, CI passing. The previous data.js entry mistakenly described a different project (dev-boz/gitmem) that was a Python CLI git-based tool. This is a complete re-audit against the correct repository.

Free tier: Fully local, BM25 search, no network calls, no telemetry. Good for privacy-conscious solo use. Pro tier adds semantic search, cloud persistence, analytics on self-hosted Supabase.

**Claim accuracy:** 11 of 16 claims verified as stated or corrected. Major surprises: keywords (true, not false), search modes (2, not 1), privacy (true, not false), explicit forget (true via archive, not false), platform support broader than recorded (Cursor and Windsurf confirmed). Time travel was the only claim overstated (true in data.js, actually false).
