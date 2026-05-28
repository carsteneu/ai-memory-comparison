# YesMem — Evidence

> Every ✅ claim backed by public source code or documentation.
> Lines may shift; permalinks use `main` for readability. For permanent citations, pin to a commit hash.

## Data Model

### Entities ✅
- `internal/storage/schema.go` — `tableLearningEntities` junction table
- `docs/features/memory.md` — "entities: Affected files, systems, people (junction table)"
- `docs/mcp-tools-reference.md` — `remember()` parameter: `entities`

### Actions ✅
- `internal/storage/schema.go:39` — `tableLearningActions = "learning_actions"`
- `docs/mcp-tools-reference.md` — `remember()` parameter: `actions`

### Keywords ✅
- `internal/storage/schema.go:40` — `tableLearningKeywords = "learning_keywords"`
- `docs/features/memory.md` — "keywords: Explicit search terms (junction table)"

### Anticipated queries ✅
- `internal/storage/schema.go:41` — `tableLearningAnticipatedQueries`
- `docs/features/memory.md` — "anticipated_queries: 3-5 concrete search phrases for better vector retrieval"

### Trigger rules ✅
- `internal/storage/schema.go:254` — `ALTER TABLE learnings ADD COLUMN trigger_rule TEXT`
- `docs/features/memory.md` — "trigger_rule: When should this knowledge activate" and "Deadline parsing: trigger_rule: 'deadline:YYYY-MM-DD'"

### Domain tag ✅
- `internal/storage/schema.go:253` — `ALTER TABLE learnings ADD COLUMN domain TEXT DEFAULT 'code'`
- `docs/features/memory.md` — "domain: code / marketing / legal / finance / general"

### Task type ✅
- `internal/storage/schema.go:351` — `ALTER TABLE learnings ADD COLUMN task_type TEXT DEFAULT ''`
- `docs/features/memory.md` — "task_type: Sub-classification for unfinished: task, idea, blocked, stale"

### Context (why) ✅
- `docs/features/memory.md` — "context: Why/when relevant"
- `docs/mcp-tools-reference.md` — `remember()` parameter: `context`

### Source attribution ✅ (5-tier)
- `docs/features/memory.md` — Source table: `user_stated`, `claude_suggested`, `agreed_upon`, `llm_extracted`, `hook_auto_learned`

### Origin + trust multiplier ✅
- `internal/models/scoring.go:268-272` — `OriginMultiplier()` function with per-origin weights (1.0 to 0.4)
- `docs/features/memory.md` — "Origin Tool & Trust Multiplier" table

### Emotional ✅
- `internal/storage/schema.go:232` — `ALTER TABLE learnings ADD COLUMN emotional_intensity REAL DEFAULT 0.0`
- `docs/features/memory.md` — "emotional_intensity: 0.0–1.0 (session mood)"

### Conflict surfacing ✅
- `docs/features/memory.md` — "Contradiction detection and resolution" in Phase 3, "Pearce & Hall" contradiction boost
- `docs/features/memory.md` — "Trust-Based Supersede Resistance" with `pending_confirmation` state

### Time-travel ✅
- `docs/features/memory.md` — "Supersede chain resolution: Recursive CTE query resolves entire supersede chain"
- `docs/features/memory.md` — "Session indexing: Every Claude Code session... automatically indexed"
- `docs/mcp-tools-reference.md` — `get_session()`, `expand_context()`, `deep_search()` with `since`/`before` parameters

### Schema fields (~22) ✅
- `internal/storage/schema.go:517-545` — Learnings table schema showing 22+ columns: content, context, domain, trigger_rule, task_type, emotional_intensity, source, origin_tool, source_msg_from, source_msg_to, importance, use_count, save_count, fail_count, noise_count, match_count, inject_count, stability, ebbinghaus_stability, turns_at_creation, current_turn_count, etc.

---

## Search & Retrieval

### Full-text ✅
- `internal/storage/schema.go:74-82` — FTS5 virtual table `learnings_fts` with triggers
- `Features.md` — "FTS5 full-text search"

### Semantic/vector ✅
- `README.md` — "512d vectors" in Foundations section
- `internal/embedding/` — embedding package

### Hybrid (BM25+Vec) ✅
- `README.md` — "Hybrid BM25 + 512d vectors, Reciprocal Rank Fusion"
- `Features.md` — "BM25 + Vector (Reciprocal Rank Fusion)"

### Deep (incl. thinking) ✅
- `docs/mcp-tools-reference.md` — `deep_search()` tool: "Deep search with full content and ±3 message context, include_thinking? parameter"

### Code graph ✅
- `docs/mcp-tools-reference.md` — `search_code_index()`, `get_file_symbols()`, `graph_traverse()` — Tree-sitter based code navigation
- `Features.md` — "Code graph, graph-first steering, worktree-aware indexing"

### Docs search ✅
- `docs/mcp-tools-reference.md` — `docs_search()` tool: "Search indexed documentation"
- `docs/mcp-tools-reference.md` — `ingest_docs()` tool: "Import documentation (.md/.txt/.rst/.pdf) into knowledge base"

### Fact metadata query ✅
- `docs/mcp-tools-reference.md` — `query_facts()` tool: "Search learning metadata by entity, action, or keyword"
- `docs/mcp-tools-reference.md` — `get_learnings()` tool: "Retrieve learnings by category or ID"

### Timeline view ✅
- `docs/mcp-tools-reference.md` — `deep_search()` with `since?` and `before?` parameters
- `docs/features/memory.md` — "Timestamp hints: Per-message temporal markers"

### Search modes (9) ✅
- `docs/mcp-tools-reference.md` — 9 distinct search tools: `search`, `deep_search`, `hybrid_search`, `docs_search`, `search_code_index`, `search_code`, `get_code_snippet`, `get_file_symbols`, `query_facts`

### Data sources (4) ✅
- `docs/mcp-tools-reference.md` — Learnings DB, Messages DB, Code Graph (Tree-sitter), Docs Index

---

## Knowledge Lifecycle

### Decay/forgetting ✅
- `internal/models/scoring.go:44` — `TurnBasedDecay()` function: `exp(-turns_since / effective_stability)`
- `docs/features/memory.md` — "Ebbinghaus decay based on conversation turns"

### Supersede/replace ✅
- `docs/features/memory.md` — "Supersede chain resolution: Recursive CTE, max 10 hops, cycle detection"
- `docs/mcp-tools-reference.md` — `remember()` parameter: `supersedes`

### Contradiction detect ✅
- `docs/features/memory.md` — "Contradiction detection and resolution" in Phase 3
- `docs/features/memory.md` — "Contradiction-Boost (Pearce & Hall)" — correcting learnings get boosted

### Quarantine ✅
- `docs/mcp-tools-reference.md` — `quarantine_session()` tool: "Quarantine session — exclude learnings from search"
- `docs/mcp-tools-reference.md` — `skip_indexing()` tool: "Skip indexing for this session"

### Auto-resolution ✅
- `docs/features/memory.md` — "Auto-resolution: Unfinished tasks auto-archive after configurable TTL (default: 30 days)"

### Trust model ✅ (4-tier)
- `README.md` — "4-tier trust hierarchy: user_stated > agreed_upon > claude_suggested > llm_extracted"
- `internal/models/scoring.go:268-272` — `OriginMultiplier()` with per-origin weights

### Explicit forget ✅
- `docs/mcp-tools-reference.md` — `quarantine_session()`: excludes all learnings from search without deletion
- `docs/mcp-tools-reference.md` — `skip_indexing()`: prevents extraction pipeline from processing a session

---

## Extraction Pipeline

### Auto-extraction ✅ (6-phase)
- `docs/features/memory.md` — "Extraction Pipeline (Multi-Phase)" section detailing Phases 2–6
- `internal/daemon/extract.go` — extraction implementation

### Content-aware preproc ✅
- `docs/features/memory.md` — "Content-Aware Pre-Processing" table: limits by content type (Paste: 1000 chars, Plans: 1000+500, Natural: 1500-3000, Tool results: 200, Thinking: 0)
- `docs/features/memory.md` — "Content-aware truncation reduces Pass 1 input by ~70%"

### Deduplication ✅ (3-method)
- `docs/features/memory.md` — "Rule-based pre-dedup: IsSubstanzlos() + BigramJaccard() > 0.85"
- `docs/features/memory.md` — "LLM-based dedup via TokenSimilarity (Jaccard ≥0.5) + Embedding (≥0.92)"
- `docs/features/memory.md` — "Pre-Admission Dedup: remember() checks via TokenSimilarity"

### Quality refinement ✅
- `docs/features/memory.md` — "Phase 3 — Quality Refinement: LLM-based dedup, confidence rating, contradiction detection and resolution"

### Narrative generation ✅
- `docs/features/memory.md` — "Phase 4 — Narrative Generation: Session handover narratives with concrete line numbers, commit hashes, error quotes. Project profiles. Persona trait extraction."

### Clustering ✅
- `docs/features/memory.md` — "Phase 4.5 — Learning Clustering: Agglomerative clustering on learning embeddings (cosine 0.85)"

### Recurrence detection ✅
- `docs/features/memory.md` — "Phase 4.6 — Recurrence Detection: Detects recurring patterns in learning clusters"

### Persona extraction ✅
- `docs/features/memory.md` — "Phase 6 — Persona Signals: Updates persona traits from session patterns"
- `Features.md` — "Persona engine: 50+ traits across 6 dimensions"

---

## Platform Support

### Claude Code ✅
- `README.md` — Listed as supported agent

### Codex ✅
- `README.md` — Listed as supported agent

### OpenCode ✅
- `README.md` — Listed as supported agent

---

## Benchmarks

### LoCoMo (0.87) ✅
- `docs/BENCHMARK.md` — Published LoCoMo methodology and score

### Methodology open ✅
- `docs/BENCHMARK.md` — Reproducible methodology with parameter documentation
