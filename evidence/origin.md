# Origin — Audit Evidence

**Repository:** https://github.com/7xuanlu/origin  
**Audited:** 2026-05-29  
**Source:** GitHub README, docs (useorigin.app), AGENTS.md, CLAUDE.md, PRIVACY.md, crate READMEs, db.rs source

---

## Vital Signs

| Field | Value | Evidence |
|-------|-------|----------|
| stars | 31 | GitHub API: `stargazers_count: 31`; README shows 31 stars |
| language | Rust | GitHub API: `language: "Rust"`; README shows Rust 98.4% |
| license | Apache 2.0 | GitHub API: `license.key: "apache-2.0"`; README footer: "Apache-2.0 license" |
| singleBinary | false | Ships 3 binaries: `origin` (CLI), `origin-server` (daemon), `origin-mcp` (MCP server). README: "All five ship from this monorepo" |
| created | 2026-04-19 | GitHub API: `created_at: "2026-04-19T22:07:06Z"` |
| coverage | 0 | No coverage badge on README; coverage is L5 informational only on PR (AGENTS.md) |

## Architecture

| Feature | Verdict | Evidence |
|---------|---------|----------|
| deployment | ✅ Local daemon | README: "Local daemon and HTTP API" on `127.0.0.1:7878`. origin-server README: "Local daemon for Origin. It owns the database, embeddings, search, distill cycles..." |
| storage | ✅ libSQL+FTS5 | AGENTS.md: "libSQL (Turso's SQLite fork — vectors, knowledge graph, documents)"; db.rs SCHEMA: FTS5 virtual table `memories_fts` |
| integration | ✅ MCP + Claude Code plugin | README: MCP-only setup section for "Claude Code, Codex, Cursor, Claude Desktop, VS Code, Gemini CLI"; Claude Code plugin via marketplace |
| proxy | ❌ false | No proxy mentioned; daemon binds directly to `127.0.0.1:7878` |
| webUi | ❌ false | Separate Tauri desktop app in `7xuanlu/origin-app` (AGPL-3.0, different repo). This repo is daemon-only. README: "No Tauri app required" to browse data files |
| offline | ✅ true | PRIVACY.md: "All data stays on your machine"; "No data is sent to any remote server by default." Local memory mode works without API key or model. README: "Local memory works without a local model or API key" |
| multiAgent | ❌ false | Has agent registry (`agent_connections` table, `/api/agents` endpoint) for tracking which agents wrote memories, but no multi-agent orchestration/coordination. AGENTS.md: agents are data sources, not coordinated workers |
| llmFlex | ✅ 2 | Two LLM options: (1) On-device Qwen via llama-cpp-2 (`origin model install`), (2) Anthropic API (`origin key set anthropic`). PRIVACY.md: "Two opt-in integrations exist" |
| cacheOpt | ❌ false | Has internal `EmbeddingCache` (200 entries) for embeddings, but no prompt caching, context optimization, or token reduction strategies documented |
| proceduralMemory | ✅ true | `/handoff` captures session-end decisions, lessons, gotchas, and open threads. README: "Session ends. /handoff writes what changed, what's still open, and where to continue." `working_memory.rs` module. Skills include `brief`, `capture`, `handoff`, `debrief` |
| sandboxedExec | ❌ false | No sandboxed execution capability documented |
| scheduledExec | ✅ true | `scheduler.rs` module: "Background periodic tasks (distill cycles, distillation, etc.)". AGENTS.md: "Background enrichment and decay: post-ingest passes link entities, enrich titles, grow matching pages, and update effective confidence" |
| privacy | ✅ true | PRIVACY.md: "All data stays on your machine", "No data is sent to any remote server by default", "None" telemetry. PII redaction module (`privacy.rs`). Daemon binds to `127.0.0.1` only |
| export | ✅ true | AGENTS.md: `export/` module: "Markdown, Obsidian, JSON, zip, and PDF export surfaces". README: "Markdown pages live in `~/.origin/pages/`", "symlink into Obsidian" |
| setup | ✅ npx setup | README: "`npx -y @7xuanlu/origin setup`". Claude Code: "/plugin marketplace add 7xuanlu/origin; /plugin install origin@7xuanlu; /init" |
| pricing | ✅ free | Apache-2.0 open source. No pricing tiers mentioned. Self-hosted, local-first |

## Data Model

| Feature | Verdict | Evidence |
|---------|---------|----------|
| unit | Memory + Page | README: "Atomic memory layer: every capture is stored first as a typed memory" + "Source-backed pages". Two-tier storage model. 6 memory types: decision, lesson, gotcha, preference, fact, correction |
| entities | ✅ true | Knowledge graph: `entities` table with name, entity_type, domain. AGENTS.md: "Knowledge graph: people, projects, tools, observations, and relations" |
| actions | ❌ false | No explicit "actions" concept as first-class field. Entities and relations exist, but no action tracking (commands, operations performed) |
| keywords | ✅ true | Spaces act as tags/keywords (e.g. `space=work`, `space=client-X`). README: "Explicit spaces: tag memories, pages, and recalls with space=work". 6-layer space resolution |
| anticipatedQueries | ❌ false | `retrieval_cue` field in memories table is closest analogue, but no dedicated "anticipated queries" field documented |
| triggerRules | ❌ false | No trigger rules system documented for conditional memory surfacing |
| domainTag | ❌ false | Memories have `domain` field (nullable text), but not a structured domain tag system. The `memory_type` field covers classification (decision, lesson, gotcha, preference, fact, correction) |
| taskType | ❌ false | Tasks (open items) are captured via `/handoff` as "open threads" but no dedicated task_type field with task/idea/blocked/stale classification |
| context | ✅ true | README: "context tool for the same underlying memory without replaying full chat history." `/brief` loads project status, identity, preferences. Memories carry source agent + confidence + stability |
| source | ✅ true | README: "source-backed pages: pages keep source memory IDs." Every capture has `source_agent` field. `source_id` tracks origin |
| originTrust | ✅ true | README: "Review before trust: Low-confidence captures and contradictions surface for review." `confidence` and `stability` fields on every memory. "Supersession chains and protected-memory conflicts stay visible." `quality_gate.rs` pre-store acceptance |
| emotional | ❌ false | No emotional analysis or sentiment tracking documented |
| conflict | ✅ true | `contradiction.rs` module. README: "contradictions surface for review when they happen, instead of silently entering context." "protected-memory conflicts stay visible" |
| layeredMemory | ✅ true | Two layers: (1) atomic memories, (2) distilled wiki pages. README: "Atomic memory layer" + "Source-backed pages". Also working memory (`working_memory.rs`) + profile narrative (`narrative.rs`) |
| timeTravel | ✅ true | README: "Real git versioning. Memory, page, and session writes commit into `~/.origin/.git/`." Git commits for every change: "inspect, diff, revert, branch, or symlink." `memories` table has `version` and `changelog` fields |
| schemaFields | 40+ | Counted from db.rs SCHEMA: `memories` table alone has 40 columns (id, content, source, source_id, title, summary, url, chunk_index, last_modified, chunk_type, language, byte_start, byte_end, semantic_unit, memory_type, domain, source_agent, confidence, confirmed, supersedes, pinned, pending_revision, word_count, entity_id, enrichment_status, quality, is_recap, supersede_mode, structured_fields, retrieval_cue, source_text, created_at, stability, access_count, last_accessed, refinement_status, effective_confidence, embedding, version, changelog). Plus: entities (10+), relations, observations, profiles, agent_connections, spaces, rejected_memories, pages, page_sources, access_log. Conservative estimate: 40 |

## Search & Retrieval

| Feature | Verdict | Evidence |
|---------|---------|----------|
| fulltext | ✅ true | FTS5: db.rs creates `memories_fts` virtual table with content + title. README: "FTS5 text search" |
| semantic | ✅ true | BGE-Base-EN-v1.5-Q embeddings (768-dim). `EmbeddingModel::BGEBaseENV15Q` in db.rs. DiskANN vector index on memories + entities |
| hybrid | ✅ true | README: "Hybrid retrieval on libSQL: memories, pages, FTS5 text search, vector embeddings, and graph context." RRF (Reciprocal Rank Fusion). origin-core README: "Vector similarity + FTS combined with Reciprocal Rank Fusion (RRF)" |
| deep | ❌ false | No "deep search" (searching raw conversation/thinking process) documented. Recall is over stored memories and pages |
| codeGraph | ❌ false | Has knowledge graph (entities, relations) but not code graph (no code symbol tracking, AST analysis, or code structure indexing) |
| docsSearch | ❌ false | No external documentation indexing or search. FTS5 searches only stored memories/pages |
| factQuery | ✅ true | `/recall` tool for targeted lookups. `list_pending` tool for unconfirmed memories. API supports query by space, memory_type, source_agent. `review` skill for deep audits |
| timeline | ✅ true | Session logs by date under `~/.origin/sessions/`. Git history provides full timeline. `last_modified`, `created_at`, `accessed_at` timestamps. README eval: "session logs and project status" for temporal tracking |
| searchModes | 3 | (1) Base: embedding similarity, (2) Reranked: LLM cross-encoder rerank (BGE-Reranker-V2-M3), (3) Expanded: LLM query expansion before search. AGENTS.md: "Three search methods: search_memory, search_memory_reranked, search_memory_expanded" |
| dataSources | 3 | (1) Direct text capture (memories), (2) Web page import (`/api/ingest/webpage`), (3) File import (`importer.rs`, Obsidian importer in `sources/`). AGENTS.md: "File importer pipeline", "Obsidian importer" |

## Knowledge Lifecycle

| Feature | Verdict | Evidence |
|---------|---------|----------|
| decay | ✅ true | README: "Background enrichment and decay: post-ingest passes... update effective confidence based on memory type, access, and age." `access_tracker.rs`: "Memory access counts + time decay." `effective_confidence` field in memories table |
| supersede | ✅ true | `supersedes` field in memories table. README: "Supersession chains... stay visible." `supersede_mode` field (hide). MCP `forget` tool deletes by ID |
| contradiction | ✅ true | `contradiction.rs` module. README: "contradictions surface for review." AGENTS.md: "Contradiction detection" |
| quarantine | ✅ true | README: "Review before trust: Low-confidence captures... surface for review." `review` skill for auditing pending memories. `list_pending` MCP tool. `quality_gate.rs` pre-store acceptance with warnings |
| autoResolve | ✅ true | README: "Background enrichment and decay: post-ingest passes link entities, enrich titles, grow matching pages." Auto-dedup, auto-linking. `refinery.rs` distill-cycle orchestration. `post_ingest.rs` enrichment |
| trustModel | ✅ true | Multi-dimensional: `confidence` (0-1 float) + `stability` (new/stable/etc.) + `source_agent` + `confirmed` flag + `quality` (low/medium/high). README: "Review before trust: Low-confidence captures... surface for review." Quality gate at ingest |
| explicitForget | ✅ true | `/forget` skill and MCP `forget` tool: "Delete a memory by ID. Destructive." CLI: `origin` command can delete memories |

## Extraction Pipeline

| Feature | Verdict | Evidence |
|---------|---------|----------|
| autoExtract | ✅ true | `classify.rs`: "Memory/profile classification via LlmEngine." `extract.rs`: "Knowledge-graph extraction (entities, relations)." Plugin README: With model/key enabled, "the daemon would normally call a model" for classification, extraction, synthesis |
| contentPreproc | ✅ true | `chunker/` module: "Code-aware, Markdown-aware, fixed-size chunking." PII redaction (`privacy.rs`). Origin-core README: "memory classification, extraction, quality gates, deduplication, and contradiction checks" |
| dedup | ✅ true | origin-core README: "deduplication" in core flow step 3. `post_ingest.rs`: "Dedup, entity linking, title enrichment, recap, page growth." README: "The daemon deduplicates overlapping captures and links related ideas in the background" |
| qualityRefine | ✅ true | `quality_gate.rs`: "Pre-store acceptance and warnings." README: "Review before trust: Low-confidence captures... surface for review." `quality` field (low/medium/high) on memories |
| narrative | ✅ true | `narrative.rs`: "Profile narrative assembly (editorial prose)." `/brief` loads identity + topic context. RLACE: "profile narrative assembly" |
| clustering | ✅ true | README: "distill cycles... cluster and link related memories." db.rs: `cluster_by_similarity()` with cosine similarity threshold. Distill cycles compile related memories into pages |
| recurrence | ❌ false | Auto-linking relates similar ideas, but no explicit "recurrence detection" (detecting repeated themes/patterns across time) documented |
| persona | ✅ true | README: "`/brief` loads project status, identity, preferences." `narrative.rs` for profile assembly. Agent identity tracking. Profile table in database. Origin-core README: "Profile narrative assembly" |

## Platform Support

| Platform | Verdict | Evidence |
|----------|---------|----------|
| p_claude | ✅ true | Primary platform. Claude Code plugin in `plugin/` directory. Marketplace install: `/plugin marketplace add 7xuanlu/origin` |
| p_codex | ✅ true | README badge: "OpenAI Codex — MCP". MCP setup: `origin mcp add codex` |
| p_opencode | ❌ false | Not listed in any supported client docs. AGENTS.md lists Claude Code, Cursor, Codex, GitHub Copilot, Zed, Aider but not OpenCode |
| p_gemini | ✅ true | README badge: "Gemini CLI — MCP". Docs: `origin mcp add gemini`. origin-mcp README: "Gemini CLI, and other MCP clients" |
| p_copilot | ✅ true | AGENTS.md: "This file guides any coding agent working in this repository — Claude Code, Cursor, Codex, GitHub Copilot, Zed, Aider, and similar." VS Code MCP connector supports Copilot |
| p_cursor | ✅ true | README badge: "Cursor — MCP". Docs: `origin mcp add cursor` |
| p_windsurf | ❌ false | Not listed. The `KNOWN_CLIENTS` registry in db.rs includes "windsurf" as a recognized client, but it's not promoted as a supported platform. No setup docs for Windsurf |
| p_openclaw | ❌ false | Not mentioned anywhere in docs, README, or code |
| p_hermes | ❌ false | Not mentioned |
| p_pi | ❌ false | Not mentioned |
| p_antigravity | ❌ false | Not mentioned |

*Note: Origin supports MCP generally, so any MCP-compatible client could theoretically work. This audit only marks platforms explicitly documented.*

## Benchmarks

| Benchmark | Value | Evidence |
|-----------|-------|----------|
| b_locomo | Recall@5: 70.0%, MRR: 0.647, NDCG@10: 0.684 | README eval table, LoCoMo (locomo10) row. "Retrieval-only, not end-to-end answer quality" |
| b_longmemeval | Recall@5: 93.6%, MRR: 0.857, NDCG@10: 0.883 | README eval table, LongMemEval (oracle, 500 Q) row |
| b_personamem | — | Not published |
| b_token | — | Not published. Eval notes: "~168 tokens per recall query" |
| b_methodology | ✅ true | Full eval harness at `crates/origin-core/src/eval/`. Methodology doc at `docs/eval/README.md`. "Run it yourself" with documented commands. AGENTS.md has detailed eval layer documentation (L1-L8) with runner commands |

---

## Additional Notes

- **6 memory types:** decision, lesson, gotcha, preference, fact, correction
- **Space system:** 6-layer resolution (inline arg → env var → spaces.toml → cwd git repo → topic → default)
- **Git versioning:** Every memory/page/session write auto-commits to `~/.origin/.git/`
- **Memory types documented in plugin skills:** `capture` skill picks one of 6 types from content
- **Setup modes:** (1) Local memory (no model/API needed), (2) On-device model (Qwen via llama-cpp-2), (3) Anthropic API key
- **16 releases:** Latest v0.7.0 (May 25, 2026)
- **310 commits on main**
- **98.4% Rust, 1.1% Shell**
- **Cross-platform:** macOS (arm64, x86_64), Linux (x86_64, aarch64; musl), Windows (x86_64)
- **Obsidian integration:** Symlink `~/.origin/pages/` into Obsidian vault; Markdown pages render natively
- **npm packages:** `@7xuanlu/origin` (setup wrapper), `origin-mcp` (standalone MCP server)
- **Homebrew:** `brew install 7xuanlu/tap/origin-mcp`
- **Schema version:** 54 (from db.rs: `pub const SCHEMA_VERSION: u32 = 54`)
