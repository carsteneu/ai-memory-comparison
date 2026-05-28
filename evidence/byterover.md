# ByteRover — Evidence

> Every ✅ claim backed by public source code, documentation, or published paper.
> Lines may shift; citations reference `main` for readability.
> Published paper: [arXiv:2604.01599](https://arxiv.org/abs/2604.01599)

## Corrections to Claimed Data

The following features are listed as absent in the ByteRover claim set but are **actually present** in the codebase/documentation:

### keywords — CORRECTION: PRESENT ❌→✅
- `docs.byterover.dev/context-tree/local-space-structure` — Frontmatter includes `keywords: string[]` field
- Each knowledge file carries explicit search keywords in YAML frontmatter
- Example: `keywords: ["token", "access_token", "refresh_token", "RS256"]`

### decay — CORRECTION: PRESENT ❌→✅
- Paper §3.2.3 — Adaptive Knowledge Lifecycle: "A daily decay factor of 0.995" (importance) and "r_i = exp(-Δt_i/τ) where τ=30" (recency, ~21-day half-life)
- `docs.byterover.dev/context-tree/local-space-structure` — "Scoring Metadata" section: importance decays by `0.995^days`, recency halves ~every 21 days

### contentPreproc — CORRECTION: PRESENT ❌→✅
- Paper §4.1.1 — Preprocessing: "Source documents are read and validated (max 5 files, 40K characters each). PDFs are converted to text; code files are truncated to 2000 lines."
- Paper §4.1.1 — Pre-Compaction: L1-L3 escalated compression strategy

### dedup — CORRECTION: PRESENT ❌→✅
- `src/agent/infra/memory/memory-deduplicator.ts` — `MemoryDeduplicator` class with LLM-based deduplication (CREATE/MERGE/SKIP actions)
- `docs.byterover.dev/context-tree/session-learning` — "Deduplication" section: compares drafts against 60 most recent memories

### autoExtract — CORRECTION: PRESENT ❌→✅
- `docs.byterover.dev/context-tree/session-learning` — "After each task session, ByteRover automatically extracts durable knowledge"
- Triggers after sessions with ≥4 messages; extracts patterns, preferences, entities, decisions, skills
- Categories: Patterns, Preferences, Entities, Decisions, Skills

### p_copilot — CORRECTION: MISMATCH ⚠️
- ByteRover integrates with **GitHub Copilot (VS Code extension)**, skill connector via `.github/skills/byterover/`
- CRITERIA.md specifies: "Documented integration with **GitHub Copilot CLI**" — these are different products
- The VS Code extension connector does NOT constitute Copilot CLI support per the criteria definition

### layeredMemory — BORDERLINE ⚠️
- ByteRover generates `.abstract.md` (~80 tokens), `.overview.md` (~1,500 tokens), and `_index.md` hierarchical summaries
- This creates L0 (full entry) → L1 (overview) → L2 (abstract) → L3 (_index.md summary) hierarchy
- However, these are compression/performance artifacts, not explicitly organized "L0 raw → L1 summary → L2 persona/semantic" layers
- Judgement call: technically present as hierarchical summarization but not as a deliberate layered memory architecture

---

## Architecture

### webUi ✅
- `README.md` — "Web dashboard for curating and querying context (`brv webui`)"
- `docs.byterover.dev/local-web-ui/overview` — Full browser-based UI served by local daemon on localhost
- Source: `src/webui/` directory with React/Vite app, `src/server/infra/webui/` server-side

### offline ✅
- `README.md` — "Everything works locally by default"
- `docs.byterover.dev/local-vs-cloud` — "All local features — curate, query, version control, provider selection, hub, connectors — work without a cloud account and without an internet connection when using a third-party or local LLM provider"
- Core memory (context tree, MiniSearch, curation) operates on local filesystem

### llmFlex: 20 ✅
- `README.md` — "20 LLM providers (Anthropic, OpenAI, Google, Groq, Mistral, xAI, DeepSeek, and more)"
- Full table in README lists: Anthropic, OpenAI, Google, Groq, Mistral, xAI, Cerebras, Cohere, DeepInfra, DeepSeek, OpenRouter, Perplexity, TogetherAI, Vercel, Minimax, Moonshot, GLM, GLM Coding Plan, OpenAI-Compatible, ByteRover
- Source: `src/agent/infra/llm/providers/`

---

## Data Model

### timeTravel ✅
- `README.md` — "Git-like version control for the context tree (branch, commit, merge, push/pull)"
- `docs.byterover.dev/git-semantic/overview` — Git-Semantic VC with full commit history, branching, checkout, log
- `brv vc log` — shows commit history; `brv vc checkout` — switch to historical state
- Meets CRITERIA.md definition: "Historical state querying (git-like VC for context)"

### schemaFields: 7 (claimed 6) ✅ (approximately correct)
Knowledge file YAML frontmatter fields (`docs.byterover.dev/context-tree/local-space-structure`):
1. `title` — Knowledge file title
2. `summary` — One-line summary
3. `tags` — Tags for categorization
4. `keywords` — Search keywords
5. `related` — Paths to related topics
6. `createdAt` — ISO 8601 creation timestamp (auto-generated, excluded per criteria)
7. `updatedAt` — ISO 8601 last-update timestamp (auto-generated, excluded per criteria)

Plus scoring metadata (importance, recency, maturity tier) stored in per-project sidecar.

Non-timestamp fields: 5 (title, summary, tags, keywords, related). Claim of 6 is in the right ballpark when counting one scoring field.

---

## Search & Retrieval

### fulltext ✅
- Paper §4.2.1 — "MiniSearch—a lightweight full-text search library with BM25 ranking, fuzzy matching (0.2 character similarity threshold), and prefix search"
- Paper Eq. 5 — Compound retrieval score: `Score(n_i,q) = w_r·BM25(n_i,q) + w_ι·ι̂_i + w_t·r_i`
- `README.md` — Search capabilities described in query workflow
- `brv search <query>` — "pure BM25 retrieval over the context tree (minisearch, no LLM, no token cost)"

---

## Knowledge Lifecycle

### supersede ✅
- Paper §4.1, Table 1 — Five atomic curate operations including MERGE ("Combine two entries intelligently; delete the source") and UPDATE ("Replace content of an existing entry")
- Git-semantic VC (`brv vc`) — tracks version history, every UPDATE/MERGE creates a traceable commit chain
- Meets CRITERIA.md definition: "Explicit mechanism to mark one memory as replacing/updating another, with a traceable chain"

---

## Platform Support

### p_claude ✅ (Claude Code)
- `docs.byterover.dev/connectors/cli-tools` — Claude Code connector with Skill (default), Hook, MCP, Rules support
- `README.md` — Listed as supported agent: "Works with 22+ AI coding agents"
- Skill directory: `.claude/skills/byterover/`

### p_codex ✅ (Codex CLI)
- `docs.byterover.dev/connectors/cli-tools` — Codex connector with Skill (default), MCP, Rules
- MCP config: `~/.codex/config.toml` (auto-setup)
- Skill directory: `.agents/skills/byterover/`

### p_cursor ✅ (Cursor IDE)
- `docs.byterover.dev/connectors/ai-ides` — Cursor connector with Skill (default), MCP, Rules
- Skill directory: `.cursor/skills/byterover/`
- MCP config: `.cursor/mcp.json` (auto-setup)

### p_windsurf ✅ (Windsurf IDE)
- `docs.byterover.dev/connectors/ai-ides` — Windsurf connector with Skill (default), MCP, Rules
- Skill directory: `.windsurf/skills/byterover/`
- MCP config: `~/.codeium/windsurf/mcp_config.json` (auto-setup)

### p_copilot — CORRECTION ⚠️ (see Corrections section above)
- Integration is with GitHub Copilot **VS Code extension**, not GitHub Copilot **CLI**
- Criteria specifically requires Copilot CLI integration
- Connector category: "VS Code Extensions", skill directory: `.github/skills/byterover/`

---

## Benchmarks

### b_locomo: "96.1" ✅
- Paper §5.2, Table 3 — "ByteRover achieves the highest overall accuracy at 96.1%"
- Dataset: LoCoMo, 1,982 questions across 272 docs
- Categories: Single-Hop (97.5), Multi-Hop (93.3), Open-Domain (85.9), Temporal (97.8)
- Judge: Gemini 3 Flash at temperature 0.0; justifier: Gemini 3.1 Pro
- Evaluation prompts reused from Hindsight's public benchmark repo: `github.com/vectorize-io/hindsight/tree/main/hindsight-dev/benchmarks`
- Methodology documented in paper §5.1 with full hyperparameters in Appendix B

### b_longmemeval: "92.8" ✅
- Paper §5.3, Table 4 — "ByteRover achieves the highest overall accuracy at 92.8%"
- Dataset: LongMemEval-S, 500 questions, 23,867 docs, ~48 sessions per question
- Categories: KU (98.7), SSU (98.6), SSA (98.2), SSP (96.7), TR (91.7), MS (84.2)
- Same judge/justifier configuration as LoCoMo

### b_methodology: true ✅
- Paper publicly available at arXiv:2604.01599 (CC BY 4.0 license)
- Full experimental setup in §5.1: datasets, baselines, metrics, evaluation prompts
- Evaluation prompts publicly available from Hindsight benchmark repo
- Ablation study in §5.5 with per-component analysis
- Hyperparameter configuration in Appendix B
- Codebase is open source (Elastic License 2.0) at github.com/campfirein/byterover-cli
- Operational profile metrics published in Table 5 (latency percentiles)

---

## Absent Features (Verified)

The following features from the "verify absent" list are confirmed as genuinely absent:

| Feature | Evidence of Absence |
|---|---|
| proxy | MCP server present, but no conversation-stream interception/proxy layer |
| multiAgent | Agent pool per project, but no inter-agent communication/coordination (swarm is provider federation, not agent orchestration) |
| entities | No dedicated entities table/field; knowledge entries have inline facts but not structured entity extraction |
| actions | No structured actions field for commands/operations |
| anticipatedQueries | No predicted search query generation |
| triggerRules | No condition-based activation rules |
| domainTag | No domain category tag (hierarchy is folder-based, not metadata) |
| taskType | No task/idea/blocked/stale classification |
| context | No dedicated "why" field for relevance rationale |
| source | No structured source attribution field (provenance is inline in content section, not a separate DB column) |
| originTrust | No trust weight hierarchy based on capture method |
| emotional | No sentiment or emotional intensity tracking |
| conflict | No contradiction detection between memories |
| semantic | No embedding-based vector search (BM25 only) |
| hybrid | No combined BM25+vector search with result fusion |
| deep | No search of model thinking/reasoning traces |
| codeGraph | No Tree-sitter/AST-based code indexing (agentic map is LLM-based, not AST) |
| docsSearch | No dedicated documentation search (docs site is separate from tool) |
| factQuery | No structured metadata query tool (no query_facts equivalent) |
| timeline | No temporal search with since/before parameters on memory metadata (VC log is about file versions, not memory time-filtering) |
| contradiction | No automatic contradiction detection |
| quarantine | No session quarantine/exclusion from search |
| autoResolve | Archive system is garbage collection, not task resolution; no configurable TTL for stale items |
| trustModel | No multi-tier trust hierarchy |
| explicitForget | DELETE curate operation exists but no dedicated user-facing forget/delete command for individual memories |
| qualityRefine | No explicit second-pass quality refinement; LLM curation is single-pass |
| narrative | No session handover narratives or project profiles; `_index.md` summaries are directory-level knowledge compression |
| clustering | No embedding-based clustering of related memories |
| recurrence | No recurrence/pattern detection across sessions |
| persona | No persistent persona trait extraction |
