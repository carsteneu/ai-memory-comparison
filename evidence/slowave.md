# slowave — Evidence

**Repo:** `mrsalty/slowave` — https://github.com/mrsalty/slowave  
**Stars:** 7
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
- Source: [`README.md`](https://github.com/mrsalty/slowave/blob/main/README.md#L101-L129) — `slowave dashboard` opens a local dashboard with memories, procedures, retrievals, activity, a memory graph, and system health.

### Offline ✅
> Fully local — SQLite in the OS user's application-data directory, a local Hugging Face text encoder (~45 MB, cached after first download), and no hosted memory service.
- Source: [`README.md`](https://github.com/mrsalty/slowave/blob/main/README.md#L152-L155) — local model download and no hosted-memory service; [`docs/install.md`](https://github.com/mrsalty/slowave/blob/main/docs/install.md#L207-L218) — runtime-data locations.

### Multi-agent ❌
> No documented cross-agent memory sharing or agent directory.

### LLM providers (count: 0) ✅
> Zero LLM calls for any memory operation — consolidation, recall, and reinforcement all run locally on CPU with a local embedding model.
- Source: `README.md` — "Zero LLM calls for memory operations — consolidation and recall run locally, at €0 per query." / `docs/benchmarks.md` — "All Slowave runs: zero LLM calls, local CPU, no API key."

### Cache optimization ❌
> No documented caching layer for embeddings or search results.

### Procedural memory ✅
> Procedures are explicit records captured at commit time with a summary, durable context, ordered steps, and caveats; relevant procedures can be returned during retrieval and later assessed for usefulness.
- Source: [`docs/architecture.md`](https://github.com/mrsalty/slowave/blob/main/docs/architecture.md#L132-L136).

### Sandboxed execution ❌
> No sandboxed execution documented.

### Scheduled/autonomous ✅
> Setup installs auto-started HTTP daemon and background-worker services, plus a daily backup service/timer; the worker consolidates events offline.
- Source: [`docs/install.md`](https://github.com/mrsalty/slowave/blob/main/docs/install.md#L20-L28) — setup starts the daemon and worker as system services; [`docs/install.md`](https://github.com/mrsalty/slowave/blob/main/docs/install.md#L48-L57) — service installation includes daily backup; [`docs/install.md`](https://github.com/mrsalty/slowave/blob/main/docs/install.md#L186-L205) — worker and daily-backup service details.

### Privacy/encrypt ✅
> Memory is local and plaintext by default; Slowave does not send it to a hosted memory service. Runtime data lives in the OS user's application-data directory.
- Source: [`README.md`](https://github.com/mrsalty/slowave/blob/main/README.md#L152-L155) — local storage and no hosted-memory service; [`docs/install.md`](https://github.com/mrsalty/slowave/blob/main/docs/install.md#L207-L218) — platform-specific runtime-data locations.

### Data export ✅
> `slowave backup` creates a gzip-compressed SQLite snapshot using SQLite's online backup API; `slowave restore` restores a selected snapshot.
- Source: [`docs/cli.md`](https://github.com/mrsalty/slowave/blob/main/docs/cli.md#L143-L158) — backup and restore commands; [`slowave/cli/backup.py`](https://github.com/mrsalty/slowave/blob/main/slowave/cli/backup.py#L1-L5) — online SQLite backup implementation.

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
> `type` field on `slowave_remember` supports: `fact`, `preference`, `decision`, `constraint`, `instruction`, `lesson`, `warning`, `open_question`, `task`, and `artifact` — 10 distinct types.
- Source: [`slowave/mcp/tools.py`](https://github.com/mrsalty/slowave/blob/main/slowave/mcp/tools.py#L61-L72) — accepted types; [`slowave/mcp/tools.py`](https://github.com/mrsalty/slowave/blob/main/slowave/mcp/tools.py#L99-L110) — public tool-schema type.

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

### Schema fields (count: 19) ✅
> Per stored Schema entry (excluding auto ID and timestamps): `prototype_id`, `content_text`, `facets_json`, `tags_json`, `scope_id`, `scope_kind`, `status`, `stale_reason`, `confidence`, `salience`, `embedding`, `dim`, `facet_axes`, `facet_strengths`, `n_facet_axes`, `supporting_episode_ids`, `is_labile`, `generalization_stage`, and `logic_version`.
- Source: [`slowave/storage/schema.sql`](https://github.com/mrsalty/slowave/blob/main/slowave/storage/schema.sql#L167-L199) — current Schema table definition.

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

### Codex ✅
> `slowave setup --client codex` configures the local MCP server and lifecycle instructions for Codex CLI, the ChatGPT desktop app, and the Codex IDE extension.
- Source: [`README.md`](https://github.com/mrsalty/slowave/blob/main/README.md#L139-L148) — verified Codex support on macOS, Linux, and Windows; [`integrations/codex/README.md`](https://github.com/mrsalty/slowave/blob/main/integrations/codex/README.md#L7-L28) — configuration details and covered Codex surfaces.

### OpenCode ✅
> `slowave setup --client opencode` configures the OpenCode MCP server and lifecycle instruction file on macOS, Linux, and Windows.
- Source: [`README.md`](https://github.com/mrsalty/slowave/blob/main/README.md#L139-L148) — verified OpenCode support on macOS, Linux, and Windows; [`integrations/opencode/README.md`](https://github.com/mrsalty/slowave/blob/main/integrations/opencode/README.md#L7-L25) — configuration details.

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
> Published evidence-containment score for consolidated top-20 retrieval over 1,534 answerable questions; the documentation distinguishes it from end-to-end QA accuracy.
- Score: `71.84%` (LoCoMo multi-session category: `87.04%`)
- Source: [`docs/benchmarks.md`](https://github.com/mrsalty/slowave/blob/main/docs/benchmarks.md#L1-L21) — current result and scope; [`docs/benchmarks.md`](https://github.com/mrsalty/slowave/blob/main/docs/benchmarks.md#L91-L104) — metric caveats.

### LongMemEval ✅
> Published evidence-containment score across all 500 LongMemEval oracle questions using consolidated hybrid top-20 retrieval; this is not a distractor-retrieval result.
- Score: `65.20%`
- Source: [`docs/benchmarks.md`](https://github.com/mrsalty/slowave/blob/main/docs/benchmarks.md#L14-L21) — current result and scope; [`docs/benchmarks.md`](https://github.com/mrsalty/slowave/blob/main/docs/benchmarks.md#L81-L88) — oracle-setting caveat.

### PersonaMem ❌
> Not documented.

### Token reduction ❌
> No current, source-backed token-reduction benchmark is published in the project documentation.

### Methodology open ✅
> Reproduction scripts and run conditions published; independent verification explicitly invited.
- Source: `docs/benchmarks.md` — "Reproduction scripts and full run conditions: docs/reproducibility.md"; `docs/reproducibility.md` linked with CLI commands.
