# slowave — Evidence

**Repo:** `mrsalty/slowave` — https://github.com/mrsalty/slowave  
**Stars:** 1  
**Language:** Python  
**License:** AGPL-3.0-or-later  
**Created:** 2026-06-08  
**Description:** One private memory layer across your AI clients — shared local memory for Claude Code, Cursor, Cline, Windsurf, and any MCP-compatible client.

---

## System Metadata

| Field | Value |
|-------|-------|
| **Deployment** | `Local CLI` |
| **Storage** | `SQLite` |
| **Integration** | `MCP` |
| **Single binary?** | `no` |
| **Setup** | `pipx install slowave` or `brew install slowave` |
| **Pricing** | `free` |
| **Storage unit** | `Memory (episode / prototype / schema)` |

---

## Architecture

### Proxy ❌
> No proxy layer — integrates via MCP server.
- Source: `README.md` — "Install once. Every AI client you use can remember your work … Claude Code, Cursor, Cline, Windsurf, and any MCP-compatible client all read and write the same local memory."

### Web/TUI ✅
> Local web dashboard to inspect memories, search recall, and view the memory graph.
- Source: `README.md` — "Watch memory compound through a local web UI: inspect what Slowave has learned, search recall, and see the memory graph grow."

### Offline ✅
> Fully local — SQLite at `~/.slowave/slowave.db`, local HuggingFace text encoder (~45 MB, cached after first download), zero cloud backend.
- Source: `README.md` — "Fully local memory — no cloud backend, no external memory service, no Ollama, no vector database to run."

### Multi-agent ❌
> No documented cross-agent memory sharing or agent directory.

### LLM providers (count: 0) ✅
> Zero LLM calls for any memory operation — consolidation, recall, and reinforcement all run locally on CPU with a local embedding model.
- Source: `README.md` — "Zero LLM calls for memory operations — consolidation and recall run locally, at €0 per query." / `docs/benchmarks.md` — "All Slowave runs: zero LLM calls, local CPU, no API key."

### Cache optimization ❌
> No documented caching layer for embeddings or search results.

### Procedural memory ❌
> Recurring workflows emerge implicitly via prototype-transition weights — no explicit procedural store.
- Source: `docs/architecture.md` — "Behavioral Patterns: Recurring workflows emerge implicitly — no explicit procedural store."

### Sandboxed execution ❌
> No sandboxed execution documented.

### Scheduled/autonomous ✅
> Background consolidation daemon (`slowave worker start`) runs an autonomous polling loop for offline memory consolidation; `slowave consolidate` provides a one-shot trigger. HTTP daemon mode (`slowave/mcp/daemon.py`) keeps the MCP server long-lived.
- Source: `slowave/mcp/daemon.py` — HTTP daemon for long-lived MCP service; `slowave/cli/main.py` — `worker start` and `consolidate` subcommands.

### Privacy/encrypt ✅
> Fully local, no cloud backend, no telemetry. Data stays at `~/.slowave/slowave.db`.
- Source: `README.md` — "Memory lives at ~/.slowave/slowave.db, a plain SQLite file. It is local and inspectable."

### Data export ✅
> `slowave backup --json` exports memory data to JSON; standard backup produces a gzip-compressed SQLite snapshot.
- Source: `slowave/cli/backup.py` — `backup()` command with `--json` flag; gzip-compressed SQLite via `.backup()` API.

---

## Data Model

### Entities ❌
> `entities` is a parameter to `slowave_activate` for retrieval context only — it is NOT stored as a structured field per memory entry; it is stored in `context_recall_events` as retrieval metadata.
- Source: `slowave` MCP tool schema — `slowave_activate` accepts `entities: string[]`; confirmed not stored on Schema dataclass (source audit of `slowave/storage/schema.sql`).

### Actions ❌
> No structured actions/commands field documented.

### Keywords/tags ❌
> No explicit keyword or tag system — retrieval is embedding-based.

### Anticipated queries ❌
> Not documented.

### Trigger rules ❌
> Not documented.

### Domain tag ✅
> `scope` parameter supports project, domain, user, and universal contexts; cross-scope bleed is prevented by default.
- Source: `README.md` — "Scoped memory — project, domain, relationship, or universal context. Cross-project bleed is prevented by default."

### Task type ✅
> `type` field on `slowave_remember` supports: `fact`, `preference`, `decision`, `constraint`, `procedure`, `lesson`, `warning`, `open_question`, `task`, `artifact` — 10 distinct types.
- Source: `slowave` MCP tool schema — `slowave_remember` `type` parameter; `docs/architecture.md` MCP tool description.

### Context (why) ✅
> Memory type system includes `decision`, `lesson`, and `constraint` types which encode *why* a fact was stored; type field is a required structured field.
- Source: `slowave` MCP tool schema — `slowave_remember` description: "Use for decisions, preferences, constraints, lessons, or any fact that should persist."

### Source attribution ❌
> `source_kind` field exists in retrieved memories (e.g. `explicit_remember`) but fewer than 3 distinct documented levels.

### Origin + trust ❌
> No multi-tier trust hierarchy where sources override others.

### Emotional ❌
> Not documented.

### Conflict surfacing ✅
> Contradiction handling is a documented responsibility of the Semantic Layer; reinforcement accepts `wrong_memory_ids` to surface incorrect memories.
- Source: `docs/architecture.md` — Semantic Layer responsibilities include "Contradiction handling". `README.md` — "Contradiction detection is heuristic, not guaranteed."

### Layered memory ✅
> Three explicit memory layers: Episodic (raw events) → Prototypes (consolidated from episodes) → Schemas (abstracted from prototypes).
- Source: `docs/architecture.md` — "Memory Layers: Episodic Layer … Semantic Layer … Behavioral Patterns"; architecture flowchart: `RE → EP → PR → SC`.

### Time-travel ❌
> Temporal awareness in recall ranking but no historical state queries or since/before parameters documented.

### Schema fields (count: 14) ✅
> Per stored Schema entry (excluding auto ID and timestamps): `content_text`, `facets` (flexible metadata dict), `tags`, `scope_id`, `scope_kind`, `status` (active/needs_review/superseded/contradicted/archived), `confidence`, `salience`, `supporting_episode_ids`, `contradicting_episode_ids`, `needs_review`, `embedding`, `dim`, `generalization_stage` (0–3).
- Source: `slowave/storage/schema.sql:113–133` — Schema table definition with all 14 non-ID non-timestamp columns.

---

## Search & Retrieval

### Full-text ✅
> FTS5 virtual tables on schemas, episodes, and raw events; FTS score used as a secondary signal (weight 0.35) alongside embedding search.
- Source: `slowave/storage/schema.sql:220–233` — three FTS5 virtual tables (`schemas_fts`, `episodes_fts`, `raw_events_fts`); `slowave/core/services/retrieval.py:152` — `search_fts()` called during recall.

### Semantic/vector ✅
> Embedding-based semantic recall using a local HuggingFace text encoder (default: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, 384-dim; ONNX Runtime or sentence-transformers backend).
- Source: `slowave/symbolic/encoder.py:20` — default model name; `docs/architecture.md` — "Recall Pipeline: Semantic similarity search."

### Hybrid (BM25+Vec) ✅
> Three scoring paths compete per retrieval: embedding cosine similarity (+0.25 bonus), FTS5 keyword score (flat 0.35), and prototype co-activation (0.15 + salience). Winner is `max()` across all three.
- Source: `slowave/core/services/retrieval.py:150–156` — three scoring branches with result fusion.

### Deep (incl. thinking) ❌
> Not documented.

### Code graph ❌
> Not documented.

### Docs search ❌
> Not documented.

### Fact metadata query ❌
> Not documented.

### Timeline view ❌
> No dedicated chronological browsing mode documented.

### Search modes (count: 2) ✅
> Two retrieval entry points: `slowave_activate` (spreading activation at session start) and `slowave_recall` (targeted mid-task semantic query).
- Source: `slowave` MCP tool schema — two distinct recall tools with different activation strategies.

### Data sources (count: 2) ✅
> Two memory source kinds retrievable: episodic memories (`explicit_remember`) and consolidated semantic schemas/prototypes.
- Source: `docs/architecture.md` — "Episodic Layer … Semantic Layer" as distinct retrieval pools; `slowave_activate` response shows `source_kind` field.

---

## Knowledge Lifecycle

### Decay/forgetting ✅
> Memory strength evolves over time; stale information gradually loses influence.
- Source: `docs/architecture.md` — "Time Matters: Memory strength evolves over time. Frequently used memories become more prominent while stale information gradually loses influence."

### Supersede/replace ✅
> `slowave_reinforce` accepts `stale_memory_ids` and `wrong_memory_ids` to mark superseded memories; `slowave_remember` instructs flagging old facts via these fields when re-encoding corrected versions.
- Source: `slowave` MCP tool schema — `slowave_reinforce` params `stale_memory_ids`, `wrong_memory_ids`.

### Contradiction detection ✅
> `GeometricContradictionJudge` runs automatically on every schema formation during consolidation (pure geometric: centroid similarity + facet-axis comparison, zero LLM calls); explicit feedback via `wrong_memory_ids` in `slowave_reinforce` also marks contradicted memories.
- Source: `slowave/latent/schema.py:387–464` — `GeometricContradictionJudge`; `docs/architecture.md` — Semantic Layer: "Contradiction handling".

### Quarantine ❌
> No quarantine (exclude-without-delete) mechanism documented.

### Auto-resolution ✅
> Stale memories automatically decay in salience; offline consolidation resolves outdated facts over time.
- Source: `docs/architecture.md` — "Time Matters: stale information gradually loses influence"; offline consolidation cycle described in architecture flowchart.

### Trust model ❌
> No multi-tier trust hierarchy documented.

### Explicit forget ✅
> `wrong_memory_ids` in `slowave_reinforce` explicitly suppresses incorrect memories; `stale_memory_ids` downgrades stale ones.
- Source: `slowave` MCP tool schema — `slowave_reinforce` description: "Strengthen or suppress memories based on how useful they were."

---

## Extraction Pipeline

### Auto-extraction ❌
> Memories must be explicitly stored via `slowave_remember` — no passive extraction from conversation without an explicit call.

### Content-aware preprocessing ❌
> Not documented.

### Deduplication ✅
> Near-duplicate schemas are suppressed at store time (consolidation reinforces existing entry instead of creating a new one) and at retrieval time via MMR cosine deduplication (threshold 0.92); exact-dedup CLI command also available.
- Source: `slowave/core/consolidation.py:220–222` — `dedup_existing_id` check reinforces existing schema on near-duplicate; `slowave/core/context.py:565–595` — `_mmr_deduplicate()` removes near-duplicate schemas from context; `slowave/core/engine.py:689–690` — `dedup_schemas_exact()`.

### Quality refinement ❌
> Consolidation is embedding-based with zero LLM calls; no LLM or rule-based quality pass on extraction.

### Narrative generation ❌
> Not documented.

### Clustering ✅
> Related episodes are consolidated into semantic prototypes and schemas via offline replay.
- Source: `docs/architecture.md` — "Over time, related episodes are consolidated into semantic prototypes and schemas."

### Recurrence detection ✅
> Prototype-to-prototype transition weights capture recurring behavioral patterns; repeated episodes converge into prototypes.
- Source: `docs/architecture.md` — "Behavioral Patterns: Pattern emergence via prototype transition graph (w_transition weights) … Habit formation through salience strengthening over repeated episodes."

### Persona extraction ❌
> Preferences are stored as typed memories but no dedicated persona model is extracted.

---

## Platform Support

### Claude Code ✅
- Source: `docs/install.md` — explicit Claude Code support with automatic `CLAUDE.md` injection and `UserPromptSubmit`/`Stop` hooks via `slowave setup`.

### Codex ❌
> Not documented.

### OpenCode ❌
> Not documented.

### Gemini CLI ❌
> Not documented.

### Copilot ❌
> Not documented.

### Cursor ✅
- Source: `docs/install.md` — "Cursor: ~/.cursor/mcp.json" listed as a supported client config path; `slowave setup --client cursor` documented.

### Windsurf ✅
- Source: `docs/install.md` — "Windsurf: ~/.codeium/windsurf/mcp_config.json" listed; `global_rules.md` injected automatically by `slowave setup`.

### OpenClaw ❌
> Not documented.

### Hermes ❌
> Not documented.

### pi/omp ❌
> Not documented.

### Antigravity ❌
> Not documented.

---

## Benchmarks

### LoCoMo ✅
> Published internal score; methodology and reproduction scripts public.
- Score: `76%` (total across 1 986 questions; beats all independently verified competitors)
- Source: `docs/benchmarks.md` — LoCoMo table, TOTAL row: 76%.

### LongMemEval ✅
> Published internal score across 500 questions, 6 categories.
- Score: `87.8%`
- Source: `docs/benchmarks.md` — LongMemEval table, TOTAL row: 87.8%.

### PersonaMem ❌
> Not documented.

### Token reduction ✅
> 86% smaller context compared to full history replay over 20 sessions.
- Score: `86%`
- Source: `README.md` — "internal tests showed 86% smaller context over 20 sessions while preserving expected recall quality." Full test: `docs/token_efficiency.md`.

### Methodology open ✅
> Reproduction scripts and run conditions published; independent verification explicitly invited.
- Source: `docs/benchmarks.md` — "Reproduction scripts and full run conditions: docs/reproducibility.md"; `docs/reproducibility.md` linked with CLI commands.
