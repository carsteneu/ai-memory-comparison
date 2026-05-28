# GBrain — Evidence

> Every ✅ claim backed by public README, DESIGN.md, RETRIEVAL.md, AGENTS.md, or source references.
> Repo: [garrytan/gbrain](https://github.com/garrytan/gbrain) (19,553 stars, TypeScript on Bun, MIT, created 2026-04-05)
> Version: 0.41.26.1

---

## Repository Metadata

- **description**: "Garry's Opinionated OpenClaw/Hermes Agent Brain"
- **deployment**: CLI daemon (`gbrain serve`), MCP server (stdio + HTTP), standalone binary or npm package
- **storage**: PGLite (PostgreSQL 17 via WASM, zero-config, default) or Postgres + pgvector (Supabase/self-hosted for scale)
- **integration**: MCP (30+ tools, stdio + HTTP + OAuth 2.1), CLI, HTTP webhooks, SDK exports
- **setup**: `bun install -g github:garrytan/gbrain` or agent-driven install via `INSTALL_FOR_AGENTS.md`
- **license**: MIT (Garry Tan, 2026)
- **created**: 2026-04-05
- **docs**: https://github.com/garrytan/gbrain/tree/master/docs

---

## Architecture

### webUi ✅
- `README.md` — "HTTP MCP with OAuth 2.1 + admin dashboard at /admin"
- `DESIGN.md` — "admin/src/index.css", "admin SPA", admin dashboard with sidebar, calibration tab, request log
- `package.json` — `"build:admin": "cd admin && bun run build..."`

### offline ✅
- `README.md` — "PGLite (Postgres 17 via WASM, zero-config, default) for personal brains"
- `README.md` — "Database ready in 2 seconds (PGLite, no server)"
- `DESIGN.md` — "Dark theme is the only theme. No light mode toggle planned — admin is an operator tool"
- System operates fully locally with no external dependencies beyond API keys for LLM calls. PGLite runs entirely in-process.

### privacy ✅
- `README.md` — "Both run on your hardware, your DB, your keys"
- `README.md` — "Your knowledge lives in a regular git repo (your 'brain repo') as markdown files"
- `AGENTS.md` — "Privacy rule: Never commit real names of people, companies, or funds into public artifacts"
- Team-brain mode scopes data by login with "fuzz-tested across every way you can read the brain... got zero leaks"
- `README.md` — "Each person on the team gets their own slice of the brain, scoped by login. When you query, you only see what you're allowed to see"

### export ✅
- `README.md` — "Your knowledge lives in a regular git repo (your 'brain repo') as markdown files. GBrain syncs the repo into Postgres for retrieval"
- `README.md` — "deletes in git become soft-deletes in DB. You can publish public subsets, share team mounts"
- All data stored as markdown files on disk, synced bidirectionally — full filesystem export by construction

### multiAgent ✅
- `README.md` — "Set up GBrain as your company brain — federated, multi-user, OAuth-scoped institutional memory for a 10-50 person team"
- `README.md` — "Each person on the team gets their own slice of the brain, scoped by login"
- `README.md` — "gbrain mounts add lets you stack additional brains alongside your personal one"
- `AGENTS.md` — "cross-brain federation works (latent-space only; the agent decides)"
- Multi-brain mounting, team scoping, OAuth-based access control

### llmFlex ✅
- `README.md` — "16 recipes covering OpenAI (default fallback), OpenRouter, Voyage, ZeroEntropy (default), Google Gemini, Azure OpenAI, MiniMax, Alibaba DashScope, Zhipu, Ollama (local), llama.cpp llama-server (local), LiteLLM proxy"
- `README.md` — Reranker: ZeroEntropy zerank-2 + local llama-server-reranker via llama.cpp
- `package.json` — `@ai-sdk/anthropic`, `@ai-sdk/google`, `@ai-sdk/openai`, `@ai-sdk/openai-compatible` dependencies
- Three-tier model selection (Haiku/Sonnet/Opus) with cost-aware mode-matching
- `docs/integrations/embedding-providers.md` — full provider matrix + decision tree

---

## Data Model

### entities ✅
- `README.md` — "Auto-link fires on every page write. No LLM calls; pure pattern matching on `[[wiki/people/bob]]` style references"
- `README.md` — "Every put_page extracts entity refs from markdown/wikilinks/typed-link syntax and writes edges with zero LLM calls"
- `RETRIEVAL.md` — "extractEntityRefs on the markdown body" matches wikilinks, markdown links, typed-link blockquotes
- Entities tracked as first-class pages (`person`, `company`, `media`, `tweet`, etc.) with typed graph edges

### actions ✅
- `README.md` — "Typed edges (`attended`, `works_at`, `invested_in`, `founded`, `advises`, `mentions`, …)"
- `docs/what-schemas-unlock.md` — Schema packs declare link verbs: "add-link-type invested-in --page-type investor --target-type portco"
- Actions are typed graph edges derived from page content and schema pack declarations

### keywords ❌
- No explicit keyword/tag junction table found. Tags exist as frontmatter via schema packs but not as a first-class keyword extraction system.
- CLOSE CALL: Schema packs define `type` classification, but this is entity typing, not keyword tagging. Mark as absent.

### context ✅
- `README.md` — "Subtypes/format/origin pushed to frontmatter"
- `README.md` — Frontmatter carries `subtype`, `legacy_type`, `format`, `kind`, `period`, `domain`
- `RETRIEVAL.md` — "source-aware ranking" with source-factor CASE expression
- `docs/what-schemas-unlock.md` — "Every retyped page stamps frontmatter.legacy_type for rollback"
- Rich contextual metadata in frontmatter: type, subtype, source, created date, author, salience

### source ✅
- `README.md` — "source-aware ranking: curated content like originals/, concepts/, writing/ outranks bulk content"
- `RETRIEVAL.md` — "Source-aware ranking applies a source-factor CASE expression at the SQL layer"
- `README.md` — "Two organizational axes (brain ⊥ source). A brain is a database. A source is a repo inside that brain"
- Source attribution via frontmatter, path prefixes, and source-tier boost in ranking

### emotional ❌
- No emotional_intensity field, sentiment tracking, or emotional state model found in evidence.
- The "voice" calibration system exists but is about output tone, not emotional memory tagging.

### conflict ✅
- `README.md` — "gbrain eval suspected-contradictions samples retrieval pairs... Surfaces conflicts between takes + facts the agent has written"
- `README.md` — "Brain consistency. Wired into the daily dream cycle"
- `CHANGELOG.md` v0.36.4.0 — "contradictions trend, takes scorecard"
- Contradiction detection between stored facts/takes, surfaced in dream cycle and eval framework

### layeredMemory ✅
- `README.md` — "Two organizational axes (brain ⊥ source)" — multiple databases, multiple repos per DB
- `README.md` — "gbrain mounts add lets you stack additional brains alongside your personal one. Each mounted brain has its OWN schema pack"
- `AGENTS.md` — "cross-brain federation works (latent-space only)"
- Multiple memory layers: personal brain, mounted team brains, per-source routing, brain-first lookup hierarchy

### timeTravel ✅
- `README.md` — "find_trajectory" for "how have the company's metrics changed AND what does the team look like right now"
- `RETRIEVAL.md` — "Temporal queries ('what happened last week?') bypass source-boost so chat/daily pages surface"
- `RETRIEVAL.md` — "Event queries ('Acme AI Series A') engage the timeline index"
- `README.md` — "chronological history with regressions auto-flagged"
- `CHANGELOG.md` — `find_trajectory` operation with `since`/`before` semantics, event timelines
- Timeline index, temporal query routing, trajectory over entity history

### schemaFields (count: 15+) ✅
- `README.md` — "15-type DRY/MECE canonical taxonomy" (gbrain-base-v2): `person`, `company`, `media`, `tweet`, `social-digest`, `analysis`, `atom`, `concept`, `source`, `deal`, `email`, `slack`, `writing`, `project`, `note`
- `README.md` — Frontmatter fields: `type`, `subtype`, `format`, `origin`, `legacy_type`, `tags`
- `README.md` — "## Facts" fence with typed metric claims: `metric: mrr`, `value: 50000`, `unit: USD`, `period: monthly`
- `docs/what-schemas-unlock.md` — "22 page types covering the universal shapes" in legacy `gbrain-base`
- Far exceeds the typical 8-12 field count; minimum verifiable count is 15 canonical types plus frontmatter fields

---

## Search & Retrieval

### fulltext ✅
- `README.md` — "BM25 keyword search" as a core retrieval strategy
- `RETRIEVAL.md` — "BM25 keyword — lexical match. Catches names, exact phrases, code identifiers"
- `RETRIEVAL.md` — "BM25 via tsvector" (PostgreSQL full-text search)

### semantic ✅
- `README.md` — "Vector (HNSW on pgvector)" as a core retrieval strategy
- `RETRIEVAL.md` — "Vector (HNSW on chunk embeddings) — semantic similarity"
- `package.json` — `"pgvector": "^0.2.0"` dependency

### hybrid ✅
- `README.md` — "Hybrid search. Vector (HNSW on pgvector) + BM25 keyword + reciprocal-rank fusion + source-tier boost + intent-aware query rewriting"
- `RETRIEVAL.md` — Full pipeline: vector + keyword + RRF fusion + graph augment + reranker
- `RETRIEVAL.md` — "Hybrid search pulls from both; auto-linking on every write keeps the graph fresh"
- `llms.txt` — "Postgres-native personal knowledge brain with hybrid RAG search"

### deep ✅
- `README.md` — "gbrain think" — "synthesized answer across the results with explicit citations to the source pages AND an honest note on what the brain doesn't know yet"
- `README.md` — "Brain layer: synthesized answer with citations and gap analysis"
- `README.md` — "The gap analysis is the differentiator: the answer tells you when a page is stale, when a claim is uncited, when two pages contradict each other, when there's a hole you should fill"
- Multi-hop reasoning, gap analysis, cross-page synthesis with citations

### codeGraph ❌
- No code-symbol graph, AST traversal, or source-code-parsing graph found. The knowledge graph operates over markdown pages and entities, not codebases.
- CLOSE CALL: Knowledge graph exists with typed edges, but it's a knowledge/entity graph, not a code/symbol graph.

### docsSearch ✅
- `llms.txt` — "docs/INSTALL.md, docs/ENGINES.md, docs/GBRAIN_VERIFY.md" — full documentation tree
- `README.md` — Extensive docs/ directory with architecture, guides, integrations, eval, mcp, ethos
- `docs/eval/SEARCH_MODE_METHODOLOGY.md` — indexed evaluation documentation
- Search across indexed documentation and operational guides

### factQuery ✅
- `README.md` — "find_trajectory" operation, "whoknows" expert routing, "find_experts"
- `README.md` — "gbrain graph-query" for multi-hop traversal
- `README.md` — "gbrain founder scorecard <entity-slug> for a four-signal JSON rollup"
- `AGENTS.md` — "MCP op find_trajectory exposes the same data"
- Typed fact queries via graph traversal, expert routing, and scored fact rollups

### timeline ✅
- `RETRIEVAL.md` — "Temporal queries ('what happened last week?') bypass source-boost so chat/daily pages surface"
- `RETRIEVAL.md` — "Event queries ('Acme AI Series A') engage the timeline index"
- `README.md` — "chronological history with regressions auto-flagged" via `gbrain eval trajectory <entity-slug>`
- `AGENTS.md` — `find_trajectory` with `kind: 'event'` or `'all'` for event timelines
- Timeline index, temporal query routing, entity trajectory over time

### searchModes (count: 5+) ✅
- `README.md` — Three named search modes: `conservative`, `balanced`, `tokenmax`
- `README.md` — Two retrieval surfaces: `gbrain search` (raw retrieval) vs `gbrain think` (synthesis + gap analysis)
- `README.md` — `gbrain graph-query` (graph traversal queries)
- `RETRIEVAL.md` — "intent classify" routing: `entity`, `temporal`, `event`, `general`
- `RETRIEVAL.md` — "Multi-query expansion" via Haiku LLM for `tokenmax` mode
- Minimum count: 5 distinct search modes (3 named + synthesis + graph-query + intent-classified + query-expanded)

---

## Knowledge Lifecycle

### decay ✅
- `RETRIEVAL.md` — "source-aware ranking: curated content outranks bulk content" via source-factor CASE at SQL layer
- `README.md` — "0.3x source-boost demote" for extract receipts vs user content
- `RETRIEVAL.md` — "Hard-exclude prefixes filter at retrieval" for archive/test content
- Time-source-tier-based ranking decay: content from chat/daily gets lower boost than curated content. Configurable via `GBRAIN_SOURCE_BOOST`.

### supersede ✅
- `README.md` — "deletes in git become soft-deletes in DB"
- `CHANGELOG.md` — v105 `slug_aliases` table for redirect/canonical resolution
- `docs/what-schemas-unlock.md` — 72h soft-delete TTL on alias/link pages during pack migration
- `docs/what-schemas-unlock.md` — `frontmatter.legacy_type` preservation on retyped pages for rollback
- Soft-delete semantics, alias resolution, and rollback-preserving supersede via migration system

### contradiction ✅
- `README.md` — "gbrain eval suspected-contradictions samples retrieval pairs, layered date pre-filter, query-conditioned LLM judge, persistent cache. Surfaces conflicts between takes + facts"
- `README.md` — "Brain consistency. Wired into the daily dream cycle"
- `CHANGELOG.md` — contradiction detection wired as a dream cycle phase
- Contradiction detection between stored takes/facts, surfaced in dream cycle, with persistent cache

### quarantine ✅
- `README.md` — "deletes in git become soft-deletes in DB"
- `docs/what-schemas-unlock.md` — "72h soft-delete TTL on alias/link pages"
- `CHANGELOG.md` — "archived source" state with `restore` command
- Soft-delete and archival mechanisms for content isolation

### autoResolve ✅
- `README.md` — "Cron-driven enrichment runs while you sleep: dedup people pages, fix citations, score salience, find contradictions, prep tomorrow's tasks"
- `README.md` — "66 cron jobs running autonomously"
- `README.md` — "24/7 dream cycle — ingest, enrich, consolidate"
- `README.md` — "A synthesis layer that gives you the actual answer... with citations and an explicit note on what the brain doesn't know yet"
- Fully autonomous overnight enrichment cycle: dedup, citation fixing, salience scoring, contradiction detection, task prep

### trustModel ✅
- `RETRIEVAL.md` — "source-aware ranking: curated content like originals/, concepts/, writing/ outranks bulk content like your-openclaw/chat/, daily/, media/x/"
- `README.md` — Source-tier boost in ranking: "0.3x source-boost demote" for extract receipts
- `AGENTS.md` — "GBrain distinguishes trusted local CLI callers... from untrusted agent-facing callers"
- `docs/what-schemas-unlock.md` — "expert_routing: true" types get priority in whoknows/find_experts
- Tiered trust: source-factor ranking, local-vs-remote trust boundary, expert-routing promotion

### explicitForget ✅
- `README.md` — "deletes in git become soft-deletes in DB"
- `RETRIEVAL.md` — "Hard-exclude prefixes (test/, archive/, attachments/, .raw/) filter at retrieval, not post-rank"
- `CHANGELOG.md` — soft-delete with TTL, archived sources with restore
- Explicit content removal via git-based deletion cascading to soft-deletes, plus archive/exclude prefixes

---

## Extraction Pipeline

### autoExtract ✅
- `README.md` — "Auto-link fires on every page write. No LLM calls; pure pattern matching"
- `README.md` — "Signal detector runs on every message. Captures ideas, entity mentions, time-sensitive todos, names, links"
- `README.md` — "extract_entity_refs from markdown/wikilinks/typed-link syntax"
- `README.md` — "extract-facts runs only on extractable: true types" from page ## Facts fences
- `CHANGELOG.md` — extract_facts pipeline: facts.conversation (deterministic), atoms, concepts, takes (LLM-backed)
- Entity extraction on every write (zero LLM), auto-linking, facts extraction from structured fences, LLM extraction phases

### contentPreproc ✅
- `README.md` — "parseMarkdown infers page type from the pack's path prefixes"
- `README.md` — "frontmatter" parsing with type/subtype/format/origin fields
- `CHANGELOG.md` — "content-sanity gate" for scraper junk, error pages, Cloudflare challenge pages
- `CHANGELOG.md` v0.41.24.0 — conversation parser reformatting (Circleback meetings)
- Markdown parsing, frontmatter extraction, content sanity filtering, conversation format detection

### dedup ✅
- `RETRIEVAL.md` — "deduplication (same slug, different chunks → keep best)" in search pipeline
- `README.md` — "consolidate memory overnight", "dedup people pages" in dream cycle
- `README.md` — "retype: from_type → to_type" mapping rules collapse 94 redundant types to 15 canonical
- `CHANGELOG.md` — content hash short-circuit for already-imported files during sync
- Dedup at search results, import, and dream-cycle consolidation levels

### qualityRefine ✅
- `RETRIEVAL.md` — "ZeroEntropy zerank-2 as reranker: 60% top-1 reshuffle"
- `RETRIEVAL.md` — "multi-query expansion" via Haiku LLM producing 2-3 query variants
- `README.md` — "citation fixing" in dream cycle
- `README.md` — "score salience" in dream cycle
- Cross-encoder reranking, query expansion, citation repair, salience scoring

### narrative ✅
- `README.md` — "gbrain think composes a synthesized answer across the results with explicit citations"
- `README.md` — "voice calibration" in DESIGN.md: "smart friend who knows your past"
- `README.md` — Example output: prose synthesis with "Three things are still open", gap analysis ("nothing's been added to the brain about Alice or Acme since April 22")
- Full narrative synthesis with citations, gap analysis, and calibrated voice

### clustering ✅
- `README.md` — "gbrain schema detect clusters your actual filesystem into proposed types"
- `README.md` — "gbrain schema suggest runs an LLM pass over them"
- `CHANGELOG.md` — "collapse 94 redundant types to 15 canonical types" — type proliferation detection and collapsing
- Filesystem clustering for type detection, LLM-refined schema proposals, type proliferation analysis

### recurrence ✅
- `README.md` — "66 cron jobs running autonomously"
- `README.md` — "Cron-driven enrichment runs while you sleep"
- `README.md` — "24/7 dream cycle" with recurring phases: sync, embed, consolidate, extract
- `CHANGELOG.md` — recurring job scheduling with `gbrain schedule`
- Cron-based recurring enrichment, autonomous dream cycle, scheduled jobs system

### persona ✅
- `README.md` — "43 curated skills" in markdown covering signal capture, enrichment, querying, brain ops, voice
- `DESIGN.md` — "Voice: GBrain talks like a smart friend who knows your past" with 5-surface voice calibration
- `README.md` — "gbrain persona" traits via schema packs, voice gate calibration
- `DESIGN.md` — "gateVoice()" with mode-specific rubrics and Haiku judge for output tone
- Persona-awareness through voice calibration, skill-based behavior, and schema-pack personality

---

## Platform Support

### p_claude ✅
- `README.md` — "Claude Code" MCP setup: `claude mcp add gbrain -- gbrain serve`
- `README.md` — "CLAUDE.md — entry point for Claude Code (deep operating context)"
- `AGENTS.md` — "Claude Code reads ./CLAUDE.md automatically"
- Claude Code has first-class MCP integration and dedicated operating context file

### p_codex ✅
- `README.md` — "Already running Codex... paste the same instruction in", "Tested with Codex"
- `AGENTS.md` — "Everyone else (Codex, Cursor, OpenClaw, Aider, Continue, or an LLM fetching via URL): start here"
- Codex explicitly tested and supported via AGENTS.md entry point

### p_opencode ❌
- No mention of OpenCode found in README, AGENTS.md, or any documentation

### p_gemini ❌
- No mention of Gemini CLI found. Google Gemini is supported as an LLM provider (embeddings), but not as an agent platform.

### p_copilot ❌
- No mention of GitHub Copilot CLI found in docs

### p_cursor ✅
- `README.md` — "Cursor / Windsurf / any stdio MCP client" MCP setup documented
- `README.md` — "Tested with Codex, Claude Code, Claude Cowork, Cursor, and AlphaClaw"
- `AGENTS.md` — "Everyone else (Codex, Cursor, OpenClaw, Aider, Continue...): start here"
- Cursor MCP integration documented and tested

### p_windsurf ✅
- `README.md` — "Cursor / Windsurf / any stdio MCP client" MCP setup
- MCP integration path documented for Windsurf

### p_openclaw ✅
- `README.md` — "The production brain behind my OpenClaw and Hermes deployments"
- `README.md` — "Garry Tan's Opinionated OpenClaw/Hermes Agent Brain" (project subtitle)
- `README.md` — "OpenClaw" as recommended agent platform, AlphaClaw deployment
- `package.json` — `"openclaw": { "compat": { "pluginApi": ">=2026.4.0" }, "extensions": [...] }`
- Native OpenClaw plugin support via context-engine extension

### p_hermes ✅
- `README.md` — "The production brain behind my OpenClaw and Hermes deployments"
- `README.md` — "Hermes" as recommended agent platform with Railway deployment
- Built as first-class citizen for Hermes agent platform

### p_pi ❌
- No mention of pi/pi-ai found. Perplexity is mentioned as an MCP client but not as `p_pi`.

### p_antigravity ❌
- No mention of Antigravity found in documentation

---

## Benchmarks

### b_locomo ❌
- No mention of LoCoMo benchmark in documented eval framework

### b_longmemeval ✅
- `README.md` — "gbrain eval longmemeval runs the public LongMemEval benchmark against your hybrid retrieval"
- `RETRIEVAL.md` — "Run the public LongMemEval benchmark: `gbrain eval longmemeval datasets/longmemeval_s.jsonl`"
- `docs/eval/SEARCH_MODE_METHODOLOGY.md` — "LongMemEval — public split, n=500 questions. Downloaded from Hugging Face"

### b_personamem ❌
- No mention of PersonaMem benchmark found

### b_token ❌
- No mention of TokenBench found. Cost analysis exists in SEARCH_MODE_METHODOLOGY.md but it's per-query cost estimation, not TokenBench specifically.

### b_methodology ✅
- `docs/eval/SEARCH_MODE_METHODOLOGY.md` — full 8-section methodology: "What this measures", "Datasets and sizes", "Sample selection", "Run procedure", "Threats to validity", "Per-question raw outputs", "Pre-registered expectations", "Re-run cadence", "Statistical-significance discipline", "Cost anchors", "Reproducibility footer"
- `README.md` — "every claim is reproducible from the committed dataset + raw outputs"
- `docs/eval/METRIC_GLOSSARY.md` — auto-generated metric glossary via CI guard
- BrainBench (custom, in sibling gbrain-evals repo): P@5, R@5, MRR, nDCG@5 on 240-page corpus
- Self-reported BrainBench scores: P@5 49.1%, R@5 97.9%, +31.4 P@5 lift from graph+extract

---

## Feature Totals (quick reference)

| Category | Present / Total | Details |
|---|---|---|
| Architecture | 6/6 | webUi, offline, privacy, export, multiAgent, llmFlex |
| Data Model | 8/11 | entities, actions, context, source, conflict, layeredMemory, timeTravel, schemaFields(15+) |
| Search | 8/9 | fulltext, semantic, hybrid, deep, docsSearch, factQuery, timeline, searchModes(5+) |
| Lifecycle | 7/7 | decay, supersede, contradiction, quarantine, autoResolve, trustModel, explicitForget |
| Extraction | 8/8 | autoExtract, contentPreproc, dedup, qualityRefine, narrative, clustering, recurrence, persona |
| Platform | 6/12 | p_claude, p_codex, p_cursor, p_windsurf, p_openclaw, p_hermes |
| Benchmarks | 2/5 | b_longmemeval, b_methodology |

**Total: 45/58 features present (78%)**

---

## Key Differentiators

1. **Knowledge graph with zero-LLM edge extraction**: Every page write auto-extracts entity refs and creates typed edges (`attended`, `works_at`, `invested_in`, `founded`, `advises`) with zero LLM calls. This is the source of the +31.4 P@5 lift over vector-only RAG.

2. **Gap-aware synthesis (`gbrain think`)**: Unlike systems that return "top-N chunks", gbrain produces a synthesized prose answer with citations AND an explicit gap analysis telling you what the brain doesn't know yet.

3. **Agent-authored schema packs**: v0.40.7.0+ allows agents to evolve the brain's ontology — adding types, link verbs, extractable fields — with atomic file locks, audit trails, and safe chunked backfill.

4. **24/7 autonomous dream cycle**: 66+ cron jobs run enrichment, dedup, fact extraction, citation fixing, contradiction detection, and salience scoring while the user sleeps.

5. **Database-in-process (PGLite)**: Zero-config Postgres 17 via WASM — no server, no Docker, instant setup. Seamlessly upgrades to full Postgres + pgvector at scale.

6. **MECE canonical taxonomy**: Default 15-type taxonomy (14 canonical + `note` catch-all) with migration path from legacy 24-type pack. Domain packs (research, legal, founder ops) via fork-and-extend.
