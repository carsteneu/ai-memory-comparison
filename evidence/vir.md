# VIR — Evidence

> **GitHub**: https://github.com/djolex999/vir
> **Version**: v0.8.0 (May 2026), 22 releases since initial
> **Stars**: 14 | **Forks**: 2 | **License**: MIT
> **Language**: TypeScript (83.1%), JavaScript (12.1%), HTML (4.8%)
> **Created**: 2026-04 (Karpathy's LLM Wiki pattern published April 2026; repo active by then)
> **Deployment**: Local CLI (`npm install -g @djolex999/vir-cli`)
> **Storage**: SQLite (`~/.vir/vir.db`) + Markdown vault (Obsidian)
> **Integration**: MCP (5 tools over stdio) + CLI daemon (launchd/systemd/cron) + CLAUDE.md sync
> **Setup**: `npm install -g @djolex999/vir-cli && vir init`
> **Docs**: README-only; no separate docs site
> **Description**: Obsidian-native LLM Wiki that reads Claude Code session transcripts retroactively, distills durable knowledge into typed markdown notes, and feeds them back into CLAUDE.md. Optional Ollama embeddings for semantic search, MMR-diverse retrieval, confidence scoring, human verification workflow, web article ingestion pipeline.

---

## Vital Signs

### Stars ✅
- `[GitHub repo header]` — 14 stars

### Language ✅
- `[repo language bar]` — TypeScript 83.1%, JavaScript 12.1%, HTML 4.8%

### License ✅
- `[LICENSE]` — MIT license
- `[package.json]` — `"license": "MIT"`
- `[README badge]` — `license-MIT-22d3ee`

### Created ✅
- `[README]` — Karpathy's LLM Wiki pattern published April 2026; vir is a direct implementation
- `[package.json]` — earliest release tag suggests ~2026-04

### singleBinary ❌
- Distributed via npm, not a single binary. Requires Node.js 20+.

---

## Architecture

### deployment ✅
- `[README Install]` — `npm install -g @djolex999/vir-cli` — local CLI tool
- `[README]` — "local-first" badge; runs entirely on the user's machine

### storage ✅
- `[src/state/db.ts:1-50]` — `better-sqlite3` database at `~/.vir/vir.db` (STATE_PATH)
- `[README State & logs]` — `~/.vir/vir.db` — SQLite (hashes, embeddings, content)
- `[README Vault structure]` — Markdown files in Obsidian vault: `vault/vir/patterns/`, `gotchas/`, `decisions/`, `tools/`, `articles/`
- Dual storage: SQLite for processing state + Markdown vault for knowledge artifacts

### integration ✅
- `[README MCP server]` — "Vir runs as an MCP server, letting Claude Code consult your vault mid-session"
- `[src/mcp/server.ts:1-650]` — Full MCP server over stdio with 5 tools (vir_query, vir_status, vir_recent_notes, vir_recent_articles, vir_project_summary)
- `[README Commands]` — vir sync-claude injects knowledge into CLAUDE.md
- `[README]` — CLI daemon runs on schedule (launchd/systemd/cron)

### proxy ❌
- Standard CLI tool and MCP server. No transparent proxy architecture.

### webUi ❌
- `[README]` — Obsidian plugin "sidebar, command palette, canvas integration" — planned, not yet released
- `[README Prerequisites]` — Obsidian vault required as external frontend
- No built-in web UI or TUI dashboard (CLI commands with chalk formatting only)

### offline ✅
- `[README]` — "local-first" badge; all processing is local
- `[src/state/db.ts]` — SQLite database, no network dependency for storage
- `[README Semantic search]` — Ollama for embeddings is optional; TF-IDF works offline by default
- `[README Cost]` — API calls only for LLM distillation (Haiku+Sonnet); optional for search

### multiAgent ❌
- `[README What's coming]` — "Multi-agent support — Codex CLI, Cursor, Aider, Cline (one per release)" — planned, not yet implemented
- `[src/cli.ts]` — Single-user design, no agent-to-agent communication

### llmFlex ✅ (2)
- `[README Prerequisites]` — "Anthropic API key OR Kie.ai API key (~72% cheaper, same models)"
- `[src/pipeline/distiller.ts]` — Distiller class supports Anthropic direct and Kie.ai endpoints
- `[README Cost controls]` — `--force-model haiku|sonnet` to switch distill model
- Count: Anthropic direct + Kie.ai = 2 distinct providers (same models, different gateways)

### cacheOpt ✅
- `[README How it works]` — "content hashes make reruns idempotent" — SHA-256 hash of session content, skip if unchanged
- `[src/state/db.ts:isProcessed]` — `hash` column checked before reprocessing
- `[README]` — "per-schema cache" mentioned for performance optimization
- `[src/pipeline/toolCallFilter.ts]` — `filterToolCalls` strips large embedded content to reduce token cost

### proceduralMemory ✅
- `[README]` — "feeds the best of it back into your CLAUDE.md files — so every future session starts sharper than the last"
- `[src/cli.ts:sync-claude]` — `vir sync-claude` injects top knowledge into CLAUDE.md
- `[src/claude/updater.ts]` — `applyPlan()` writes Vir blocks into CLAUDE.md with confidence-gated entries
- This is procedural memory: knowledge that changes *how* the agent works in future sessions

### sandboxedExec ❌
- No sandboxed execution capability. Tool runs directly on the user's machine.

### scheduledExec ✅
- `[README Platform support]` — Daemon support: macOS (launchd), Linux (systemd user timer), Linux (crontab)
- `[README Quick start]` — `vir schedule install` registers the daemon, runs every 3h by default
- `[src/daemon/index.ts]` — install/uninstall/status implementation for all platforms
- `[README Cadence]` — Configurable `cadenceHours` (default 3)

### privacy ❌
- `[README]` — No encryption mentioned. Uses Kie.ai which routes through third-party API.
- Local files are plain markdown. No at-rest encryption.
- `[README config]` — API keys stored in `~/.vir/config.json` (plaintext)

### export ✅
- `[README]` — "Plain markdown output. Every note is a file in your Obsidian vault. Read it, edit it, delete it. Nothing is hidden in a compressed database you can't inspect."
- `[src/cli.ts:query --json]` — `--json` flag emits machine-readable results
- `[src/cli.ts:doctor --json]` — `--json` flag for diagnostics
- Markdown vault is inherently portable and exportable

### setup ✅
- `[README Install]` — `npm install -g @djolex999/vir-cli`
- `[README Quick start]` — `vir init` (guided wizard) then `vir run`

### pricing ✅
- `[README]` — MIT license, free. API costs are out-of-pocket (Anthropic/Kie.ai), not a vir fee.

---

## Data Model

### unit ✅
- `[README Vault structure]` — Typed markdown notes: patterns, gotchas, decisions, tools
- `[src/pipeline/types.ts:47]` — `Category = "pattern" | "gotcha" | "decision" | "tool"`
- `[src/mcp/server.ts:38-41]` — Article categories: concept, technique, reference, opinion
- Storage unit is a typed Markdown note with YAML frontmatter, backed by SQLite sessions + articles tables

### entities ❌
- `[src/pipeline/types.ts]` — No entity type in the classification system
- `[src/mcp/server.ts]` — No entity extraction referenced
- `[src/state/db.ts]` — No entity table; sessions table has project field for grouping but no entity graph
- No NER, entity resolution, or entity graph

### actions ❌
- `[src/state/db.ts]` — No actions table; no action tracking
- `[src/pipeline/types.ts]` — No action type in pipeline
- `[src/cli.ts]` — No action logging beyond processing records

### keywords ❌
- `[src/pipeline/types.ts:47]` — Classification is category-exclusive (pattern/gotcha/decision/tool), not keyword-based
- `[src/mcp/server.ts]` — Category filter on vir_query, project filter on vir_recent_notes; no tag/keyword dimension
- `[src/state/db.ts]` — No tags column in sessions or articles tables
- Categories serve a similar role but are taxonomic (4-8 fixed types), not freeform keywords

### anticipatedQueries ❌
- No anticipated-queries field in frontmatter or schema
- `[src/pipeline/types.ts]` — Classification has category, topic, project, confidence only

### triggerRules ❌
- `[src/daemon/index.ts]` — Daemon is time-based (every N hours), not trigger/event-based
- No hook system or event-driven triggers

### domainTag ❌
- `[src/pipeline/types.ts:47]` — Category is project-knowledge type (pattern/gotcha/decision/tool), not domain (code/marketing/legal)
- No domain classification

### taskType ❌
- `[src/pipeline/types.ts:47]` — Category types are knowledge types, not task types (todo/issue/note)
- `[README Vault structure]` — patterns/gotchas/decisions/tools/projects/articles — all knowledge, no tasks

### context ❌
- `[src/pipeline/types.ts:47]` — Classification has category, topic, project, confidence. No context/why field.
- `[README How it works]` — "distills durable knowledge with Sonnet" — knowledge extraction, not context preservation
- Notes capture *what* was learned, not explicit *why* context

### source ✅
- `[src/mcp/server.ts:96-104]` — `hitMeta()` parses frontmatter for `source_url`, `source_title`, `source_author` on article notes
- `[src/pipeline/writer.ts]` — Notes carry session attribution in frontmatter (project, session ID, date)
- `[README How it works]` — "Articles always keep their source URL in frontmatter for backlinks"
- `[README Vault structure]` — index.md catalogs every note with its origin

### originTrust ✅
- `[README Quality controls]` — "Confidence scores on every note, written into the frontmatter (`confidence: 0.xx`)"
- `[src/mcp/server.ts:116-119]` — `isVerifiedContent()` checks `verified: true` in frontmatter
- `[src/search/retriever.ts:VERIFIED_BOOST]` — Verified notes get +0.2 ranking boost
- `[src/mcp/server.ts:vir_query schema]` — `verified_only` parameter to filter to human-verified notes
- `[README Active learning]` — "Verified notes get retrieval priority over unverified ones"

### emotional ❌
- `[src/pipeline/types.ts]` — No emotional/sentiment field
- `[src/state/db.ts]` — No sentiment column
- No emotional analysis mentioned in README

### conflict ✅
- `[README Quality controls]` — "`vir lint` flags contradictions and stale notes"
- `[src/cli.ts:lint --contradictions]` — "Run only the contradiction check (Haiku tokens)"
- `[src/lint/linter.ts]` — `contradictionCheck()` uses Haiku to compare note pairs
- Contradictions are detected and reported, though resolution is manual

### layeredMemory ❌
- `[README Vault structure]` — Flat directory: patterns/, gotchas/, decisions/, tools/, articles/, projects/
- `[src/state/db.ts]` — Single sessions table, no tier or layer column
- No L0/L1/L2 or working/session/long-term differentiation

### timeTravel ❌
- `[src/state/db.ts]` — Sessions table has `processed_at` and `started_at` but no version history
- `[src/cli.ts]` — No as-of query or historical state recovery
- Notes are current-state only; dedupe moves old versions to archived/ but no time-travel query interface

### schemaFields ✅ (~8)
- Sessions table (`src/state/db.ts:115-130`): path, hash, processed_at, skipped, note_paths, error, content, category, topic, project, confidence, started_at, archived, embedding (14 columns)
- Articles table (`src/state/db.ts:132-146`): path, hash, processed_at, skipped, note_path, error, content, category, title, url, author, published, confidence, distilled_at, embedding (15 columns)
- Topics table (`src/state/db.ts:148-158`): id, topic_text, title, content, source_note_ids, confidence, model, created_at, updated_at, embedding (10 columns)
- Knowledge-bearing fields in the core memory model (sessions + note frontmatter): content, category, topic, project, confidence, started_at, verified (7-8 semantic fields)

---

## Search & Retrieval

### fulltext ✅
- `[src/search/retriever.ts:searchTfIdf]` — Full TF-IDF implementation over the vault's markdown files
- `[src/search/retriever.ts:stripMarkdown]` — Strips YAML frontmatter, code blocks, images, links, headings before tokenization
- `[README Semantic search]` — "Vir uses TF-IDF by default" (when Ollama not running)
- `[src/cli.ts:query]` — Falls back to TF-IDF automatically when Ollama is unavailable

### semantic ✅
- `[src/search/embedder.ts]` — Ollama-based embedding with nomic-embed-text
- `[src/search/retriever.ts:embed]` — `embed()` function calls Ollama API, returns vector
- `[src/search/retriever.ts:cosineSimilarity]` — Cosine similarity scoring
- `[README Semantic search]` — `ollama pull nomic-embed-text` and `vir embed` for generation
- `[src/state/db.ts:storeEmbedding]` — Stores embeddings as JSON in sessions.embedding column

### hybrid ❌
- `[src/search/retriever.ts:search]` — `search()` function: tries embeddings first, falls back to TF-IDF if Ollama unavailable or no results
- This is sequential fallback, NOT hybrid fusion. No RRF, no score combination, no weighted merge.
- Embedding and TF-IDF never combine scores on the same query

### deep ❌
- `[src/search/retriever.ts:search]` — Only searches distilled note content (markdown files), not raw conversation transcripts
- `[src/pipeline/parser.ts]` — Transcripts are parsed for distillation input, but not indexed for retrieval
- No "deep search" over raw thinking/tool-call content

### codeGraph ❌
- `[src/search/retriever.ts]` — Search is purely text-based (TF-IDF + embeddings over markdown)
- No AST parsing, no code graph, no Tree-sitter integration
- `[src/pipeline/parser.ts]` — Tracks `filesTouched` from transcripts but stores as metadata, not for code search

### docsSearch ❌
- `[src/search/retriever.ts]` — Single vault index; no separate documentation search mode
- No documentation indexing or docs-specific retrieval path

### factQuery ❌
- `[src/mcp/server.ts:vir_query]` — Has category, project, type, verified_only filters, but these are query-time filters, not a structured fact metadata query engine
- `[src/state/db.ts]` — No fact-query specific index or API

### timeline ✅
- `[src/mcp/server.ts:vir_recent_notes]` — Returns most recently distilled notes, sorted by `started_at`
- `[src/mcp/server.ts:vir_recent_articles]` — Returns most recently distilled articles, sorted by `published`/`distilled_at`
- `[src/mcp/server.ts:vir_status]` — Returns `dateRange: { oldest, newest }` for the knowledge base
- `[src/cli.ts:status]` — Shows oldest/newest note dates, chronological project breakdown

### searchModes ✅ (3)
- `[src/search/retriever.ts:search]` — Unified semantic/lexical search: embedding (Ollama cosine) with TF-IDF fallback
- `[src/mcp/server.ts:vir_recent_notes]` — Chronological retrieval by date, with category/project/since_days filters
- `[src/mcp/server.ts:vir_project_summary]` — Pre-synthesized project knowledge summary retrieval
- Note: `vir_recent_articles` and `vir_status` are informational/MCP tools, not distinct search modes in the comparison taxonomy

### dataSources ✅ (2)
- `[README How it works]` — Claude Code sessions (`~/.claude/projects/**/*.jsonl`) — primary source
- `[README How it works]` — Web articles via Obsidian Web Clipper (`raw/` directory) — secondary source
- `[src/pipeline/scanner.ts]` — Scans both session JSONL files and article markdown files
- More sources planned (PDFs, code repos, images) but not yet implemented

---

## Knowledge Lifecycle

### decay ❌
- `[src/state/db.ts]` — No decay mechanism. Notes persist indefinitely once written.
- `[README]` — No Ebbinghaus curve, no time-based forgetting, no importance decay
- Staleness is detected by lint (`vir lint --stale`) but is advisory only — notes are never automatically pruned

### supersede ✅
- `[README Quality controls]` — "`vir dedupe` merges similar notes that have drifted apart"
- `[src/dedupe/detector.ts]` — `detectDuplicates()` finds near-duplicate note pairs
- `[src/dedupe/merger.ts]` — `mergeNotes()` merges or archives one of the pair
- `[src/cli.ts:dedupe]` — Interactive merge with keep/swap/merge/skip options
- `[README Vault structure]` — Archived notes moved to `archived/` (kept, never deleted)
- Note: This is deduplication (= supersession by identity), not version-based supersession chains

### contradiction ✅
- `[README Quality controls]` — "`vir lint` flags contradictions"
- `[src/cli.ts:lint --contradictions]` — Dedicated contradiction check command
- `[src/lint/linter.ts:contradictionCheck]` — Uses Haiku to compare note pairs for contradictions
- Returns contradiction pairs with reasoning strings

### quarantine ❌
- `[README Vault structure]` — `archived/` directory for deduplicated notes; `.rejected/` for human-rejected notes via `vir review`
- Neither is an automatic quarantine — both are explicit human actions
- No automatic isolation of suspect/low-confidence data

### autoResolve ❌
- `[src/cli.ts:dedupe]` — Deduplication is interactive (user chooses keep/swap/merge/skip)
- `[README Active learning]` — `vir review` is manual (approve/edit/reject)
- No background auto-resolution of conflicts or duplicates

### trustModel ✅
- `[README Quality controls]` — "Confidence scores on every note" (0.0–1.0)
- `[src/search/retriever.ts:VERIFIED_BOOST]` — Verified notes get +0.2 ranking boost
- `[src/mcp/server.ts:vir_query]` — `verified_only` parameter restricts to human-verified notes
- `[README Quality controls]` — Heuristic pre-filter drops low-signal sessions before LLM; classification confidence ≤0.6 is dropped before distill
- `[README Cost controls]` — Hybrid Haiku/Sonnet routing planned for cost-quality tradeoff
- Two-tier trust: confidence score (LLM-generated) + verified flag (human-approved)

### explicitForget ✅
- `[README Active learning]` — `vir review` → "Rejected notes are moved to `.rejected/` — recoverable, not deleted"
- `[README Quality controls]` — "Every note is a file in your Obsidian vault. Read it, edit it, delete it."
- `[src/cli.ts:dedupe]` — dedupe archives notes (moves to archived/)
- Users can delete .md files directly from the vault
- No explicit MCP delete tool, but file-system-level deletion is inherently supported

---

## Extraction Pipeline

### autoExtract ✅
- `[README How it works]` — "Vir reads your transcripts from `~/.claude/projects/**/*.jsonl`, runs each session through a cheap heuristic filter, classifies the survivors with Haiku, and distills durable knowledge with Sonnet"
- `[src/pipeline/run.ts]` — Full automated pipeline: scan → filter → classify → distill → write
- `[src/pipeline/scanner.ts]` — Scans JSONL files for new/updated sessions
- `[src/pipeline/filter.ts]` — Heuristic pre-filter with configurable threshold
- `[src/pipeline/distiller.ts]` — classify() + distill() two-stage LLM extraction
- `[src/daemon/index.ts]` — Scheduled daemon runs this automatically every N hours
- Retroactive: processes existing sessions, not just new ones

### contentPreproc ✅
- `[README How it works]` — "Before distillation it filters tool calls — preserving intent (file paths, commands, search patterns, errors, short results) while truncating large embedded content (file writes, long bash logs, big grep dumps) to keep token cost bounded"
- `[src/pipeline/toolCallFilter.ts]` — `filterToolCalls()` with three modes: aggressive, moderate, off
- `[src/pipeline/scrubber.ts]` — `scrub()` function for content cleaning
- `[src/search/retriever.ts:stripMarkdown]` — Strips YAML frontmatter, code blocks, images, links for indexing
- `[README Config reference]` — `filterToolCalls` configurable: aggressive | moderate | off
- Content-aware: understands tool call structure (preserves intent, drops noise)

### dedup ✅
- `[README Quality controls]` — "`vir dedupe` merges similar notes that have drifted apart"
- `[src/dedupe/detector.ts]` — `detectDuplicates()` uses Haiku to compare note content
- `[src/dedupe/merger.ts]` — `mergeNotes()` handles keep/merge/swap
- `[src/state/db.ts:isProcessed]` — SHA-256 hash-based idempotency: same session content won't be reprocessed
- `[README How it works]` — "content hashes make reruns idempotent"

### qualityRefine ✅
- `[README Quality controls]` — Three quality layers:
  1. Heuristic pre-filter drops low-signal sessions before any LLM call
  2. Classification scores ≤0.6 dropped before distill step
  3. Confidence scores on every note written into frontmatter
- `[README Active learning]` — `vir review` for human verification (approve/edit/reject)
- `[src/search/retriever.ts:VERIFIED_BOOST]` — Verified notes ranked higher
- `[README Quality controls]` — `vir lint` flags contradictions and stale notes
- Multi-stage quality pipeline: pre-filter → classify → threshold → distill → score → human review → lint

### narrative ✅
- `[README Commands]` — `vir compose "<topic>"` — "Synthesize a topic page from related notes" — embedding-searches the vault, synthesizes into a topic page with wikilinked sources
- `[README Commands]` — `vir summarize <project>` — "Cross-session project synthesis"
- `[src/pipeline/composer.ts]` — `composeFromSources()` — LLM synthesis from gathered vault sources
- `[src/pipeline/summarizer.ts]` — `summarizeProject()` / `summarizeAll()` — per-project knowledge summaries
- `[src/search/synthesizer.ts]` — `synthesize()` — LLM answer synthesis from top-K search hits (used in vir_query)
- `[README]` — Notes are cross-linked with wikilinks

### clustering ❌
- `[src/cli.ts]` — No clustering command or subsystem
- `[src/pipeline/types.ts]` — No cluster type
- `[README]` — No cluster detection mentioned
- Topic composition (`vir compose`) synthesizes around user-provided topics, but doesn't auto-discover clusters

### recurrence ❌
- `[src/cli.ts:lint]` — Orphans and staleness, no recurrence pattern detection
- `[src/pipeline]` — No recurrence analysis
- `[README]` — No recurrence detection mentioned

### persona ❌
- `[src/pipeline/types.ts]` — No persona type in extraction pipeline
- `[src/state/db.ts]` — No persona table or field
- `[README]` — No persona extraction or user profiling mentioned
- Knowledge is project-scoped, not user-scoped

---

## Platform Support

### p_claude ✅
- `[README]` — "An LLM Wiki for Claude Code, in your Obsidian vault" — tagline
- `[src/mcp/server.ts:1-15]` — Full MCP server with Claude Code registration instructions in header comment
- `[src/cli.ts:mcp install]` — `vir mcp install` registers with Claude Code
- `[src/claude/updater.ts]` — `vir sync-claude` writes knowledge blocks into CLAUDE.md
- `[README MCP server]` — Five MCP tools: vir_query, vir_status, vir_recent_notes, vir_recent_articles, vir_project_summary
- `[README How it works]` — Reads from `~/.claude/projects/**/*.jsonl`
- Claude Code is the primary and only currently supported platform

### p_codex ❌
- `[README What's coming]` — "Multi-agent support — Codex CLI, Cursor, Aider, Cline (one per release)" — planned

### p_opencode ❌
- Not mentioned anywhere in README or source

### p_gemini ❌
- Not mentioned anywhere in README or source

### p_copilot ❌
- Not mentioned anywhere in README or source

### p_cursor ❌
- `[README What's coming]` — "Multi-agent support — Codex CLI, Cursor, Aider, Cline (one per release)" — planned

### p_windsurf ❌
- Not mentioned anywhere in README or source

### p_openclaw ❌
- Not mentioned anywhere in README or source

### p_hermes ❌
- Not mentioned anywhere in README or source

### p_pi ❌
- Not mentioned anywhere in README or source

### p_antigravity ❌
- Not mentioned anywhere in README or source

---

## Benchmarks

### b_locomo ❌
- No published LoCoMo benchmark. No benchmark infrastructure.

### b_longmemeval ❌
- No published LongMemEval benchmark.

### b_personamem ❌
- No published PersonaMem benchmark. No persona extraction.

### b_token ❌
- `[README Cost controls]` — Claims 60-70% token cost reduction via tool-call filtering in v0.7.0, but this is production cost measurement, not a published/standardized benchmark
- No published token reduction vs. baseline benchmark

### b_methodology ❌
- No benchmark methodology documented. Cost claims are informal (production measurements), not rigorous benchmarks.

---

## Features NOT present (verified absent)

| Feature | Evidence of absence |
|---------|-------------------|
| **entities** | No entity extraction pipeline, no entity table in schema, no NER. Classification is category-based (pattern/gotcha/decision/tool), not entity-based. |
| **actions** | No action tracking table. Session processing is tracked but user/agent actions are not modeled. |
| **keywords** | Four fixed categories (pattern/gotcha/decision/tool) + four article categories (concept/technique/reference/opinion). No freeform keyword/tag system. |
| **anticipatedQueries** | No anticipated-query field. Search is reactive (user types query, system retrieves). |
| **triggerRules** | Daemon is purely time-based (every N hours). No event-driven or rule-based triggering. |
| **domainTag** | No domain classification (code/marketing/legal). Category is knowledge type, not domain. |
| **taskType** | No task detection (todo/issue/idea). Knowledge-focused, not task-focused. |
| **context** | No dedicated context/why field. Notes capture distilled knowledge, not situational context. |
| **emotional** | No sentiment or emotional valence tracking. |
| **layeredMemory** | Flat vault structure (directories by category). No L0/L1/L2 or working/session/long-term tiers. |
| **timeTravel** | No version history or as-of querying. Notes are current-state; archived notes exist in archived/ but no time-travel query interface. |
| **hybrid** | Sequential fallback (embedding → TF-IDF), not true hybrid fusion. No RRF, no score combination. |
| **deep** | Only distilled notes are searchable. Raw conversation transcripts not indexed for retrieval. |
| **codeGraph** | No AST or code graph search. No Tree-sitter integration. |
| **docsSearch** | No separate documentation indexing or search path. |
| **factQuery** | Category/project/verified_only filters exist on vir_query MCP tool but are query-time filters, not a dedicated fact metadata query engine. |
| **decay** | No automatic forgetting. Staleness detection (vir lint) is advisory, not automatic. |
| **quarantine** | .rejected/ and archived/ are human-driven, not automatic quarantine of suspect data. |
| **autoResolve** | Deduplication is interactive (user choice required). No automatic conflict/duplicate resolution. |
| **clustering** | No automatic topic clustering. Topic synthesis is user-initiated via `vir compose <topic>`. |
| **recurrence** | No recurrence pattern detection across sessions. |
| **persona** | No persona extraction or user profiling. Knowledge is project-scoped, not user-scoped. |
| **singleBinary** | npm package, not a standalone binary. Requires Node.js 20+. |
| **proxy** | Standard MCP server + CLI, not a transparent proxy. |
| **webUi** | No built-in web UI. Relies on Obsidian as external frontend. Obsidian plugin planned but not yet released. |
| **multiAgent** | Single-user design. Multi-agent support planned for future releases. |
| **sandboxedExec** | No sandboxed execution capability. |
| **privacy** | No encryption. API keys in plaintext config. Data sent to external LLM APIs. |
| **All non-Claude platforms** | Only Claude Code is currently supported. All other platforms (Codex, OpenCode, Gemini, Copilot, Cursor, Windsurf, OpenClaw, Hermes, pi, Antigravity) are either planned or not mentioned. |
| **All benchmarks** | No published benchmarks (LoCoMo, LongMemEval, PersonaMem). No benchmark infrastructure. Token reduction claim is informal, not standardized. |
