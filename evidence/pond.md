# pond — Evidence

**Repo:** `github.com/tenequm/pond`
**Stars:** 35
**Language:** Rust
**License:** Apache-2.0
**Created:** 2026-05-07
**Description:** Lossless storage and search for AI agent sessions, across every agentic client.

---

## System Metadata

| Field | Value |
|-------|-------|
| **Deployment** | `Local CLI (self-host object store optional)` |
| **Storage** | `Lance (local FS / S3 / GCS / Azure)` |
| **Integration** | `MCP / CLI / HTTP` |
| **Single binary?** | `yes` ([docs/spec.md#L8](https://github.com/tenequm/pond/blob/main/docs/spec.md#L8): "One static binary, two transports, two deployments") |
| **Setup** | `brew install` ([README.md#L30](https://github.com/tenequm/pond/blob/main/README.md#L30); also Nix and cargo install) |
| **Pricing** | `free (Apache-2.0)` |
| **Storage unit** | `Session (Sessions -> Messages -> Parts, lossless)` ([docs/spec.md#L442](https://github.com/tenequm/pond/blob/main/docs/spec.md#L442): three Lance datasets `sessions`, `messages`, `parts`) |

---

## Architecture

### Proxy ❌
> Intercepts and modifies the LLM conversation stream in-flight (context collapsing, prompt injection). Not MCP or hooks.
- Note: deliberately out of scope; pond "does not execute tools, run an agent loop, compact context" ([docs/spec.md#L107](https://github.com/tenequm/pond/blob/main/docs/spec.md#L107)).

### Web/TUI ❌
> Ships a visual interface accessible in a browser or terminal.
- Note: explicit non-goal, "there is no UI and no daemon beyond `pond serve`" ([docs/spec.md#L108](https://github.com/tenequm/pond/blob/main/docs/spec.md#L108)).

### Offline ✅
> Core memory functionality works without internet connection.
- Source: [README.md#L158](https://github.com/tenequm/pond/blob/main/README.md#L158) — default storage is a local directory; [packages/pond/src/embed.rs#L333](https://github.com/tenequm/pond/blob/main/packages/pond/src/embed.rs#L333) — embeddings run on a bundled local model (`intfloat/multilingual-e5-small`, weights cached after one-time download); [docs/spec.md#L692](https://github.com/tenequm/pond/blob/main/docs/spec.md#L692) — a caught-up sync on an offline host with no cached weights still completes as a no-op. No external API in ingest, search, or serve.

### Multi-agent ✅
> Supports cross-agent memory sharing, agent directory, or inter-agent communication.
- Source: [README.md#L14](https://github.com/tenequm/pond/blob/main/README.md#L14) — sessions from every client and machine searchable in one place; any session restorable into any supported client ([README.md#L21](https://github.com/tenequm/pond/blob/main/README.md#L21)); [docs/spec.md#L738](https://github.com/tenequm/pond/blob/main/docs/spec.md#L738) — search filters by `source_agent` incl. subagent subpaths; dedicated OpenClaw and Hermes plugins project pond recall into those agents ([packages/openclaw-pond/package.json#L4](https://github.com/tenequm/pond/blob/main/packages/openclaw-pond/package.json#L4), [packages/hermes-pond/\_\_init\_\_.py#L1](https://github.com/tenequm/pond/blob/main/packages/hermes-pond/__init__.py#L1)).

### LLM providers (count: 1) ✅
> Count of distinct embedding/LLM providers supported.
- Source: [packages/pond/src/embed.rs#L333](https://github.com/tenequm/pond/blob/main/packages/pond/src/embed.rs#L333) — one bundled local embedding backend (candle XLM-RoBERTa, e5 family variants selectable via config). No external LLM/embedding APIs; remote embedding providers explicitly deferred ([docs/spec.md#L782](https://github.com/tenequm/pond/blob/main/docs/spec.md#L782)).

### Cache optimization ✅
> Caches intermediate results (embeddings, search results) for performance.
- Source: [docs/spec.md#L501](https://github.com/tenequm/pond/blob/main/docs/spec.md#L501) — local freshness cache lets `pond sync` skip re-decoding unchanged sources; [docs/spec.md#L754](https://github.com/tenequm/pond/blob/main/docs/spec.md#L754) — embeddings computed once at ingest and persisted, never recomputed per query; [docs/spec.md#L186](https://github.com/tenequm/pond/blob/main/docs/spec.md#L186) — datasets share one Lance cache and object-store client.

### Procedural memory ❌
> Stores and executes reusable scripts/code at retrieval time (not just data).

### Sandboxed execution ❌
> Executes user-provided code in a sandboxed environment.

### Scheduled/autonomous ✅
> Can run scheduled tasks or autonomous operations without user prompt.
- Source: [README.md#L144](https://github.com/tenequm/pond/blob/main/README.md#L144) — `pond schedule start` (every 5m by default) via launchd on macOS, systemd user timers or cron on Linux ([packages/pond/src/schedule.rs#L3](https://github.com/tenequm/pond/blob/main/packages/pond/src/schedule.rs#L3)); [docs/spec.md#L699](https://github.com/tenequm/pond/blob/main/docs/spec.md#L699) — `pond serve --with-sync` folds periodic sync into the serving process.

### Privacy/encrypt ✅
> Data encryption at rest or in transit, self-hosting, zero-telemetry.
- Source: [README.md#L21](https://github.com/tenequm/pond/blob/main/README.md#L21) — storage you own (local dir or your own S3 bucket); [docs/spec.md#L107](https://github.com/tenequm/pond/blob/main/docs/spec.md#L107) — no telemetry; [docs/spec.md#L106](https://github.com/tenequm/pond/blob/main/docs/spec.md#L106) — encryption is operational (server-side bucket encryption + filesystem encryption; documented as not zero-knowledge); [docs/spec.md#L263](https://github.com/tenequm/pond/blob/main/docs/spec.md#L263) — secret redaction rules at storage boundary.

### Data export ✅
> Built-in export functionality (JSON, Markdown, etc.).
- Source: [packages/pond/src/sql.rs#L284](https://github.com/tenequm/pond/blob/main/packages/pond/src/sql.rs#L284) — `pond sql` results export to parquet/ndjson; [docs/spec.md#L705](https://github.com/tenequm/pond/blob/main/docs/spec.md#L705) — `pond copy` exports the corpus to a `.pond` archive or a JSONL wire stream.

---

## Data Model

### Entities ❌
> Structured extraction of named entities (files, people, systems, packages) as separate fields or tables.
- Note: deliberate; pond is a lossless archive, not an extraction pipeline. No NER.

### Actions ✅
> Stores commands, operations, or tool calls as separate structured fields.
- Source: [docs/spec.md#L373](https://github.com/tenequm/pond/blob/main/docs/spec.md#L373) — typed `ToolCallPart` / `ToolResultPart` (call_id, name, params, is_failure) as canonical Part variants; [docs/spec.md#L519](https://github.com/tenequm/pond/blob/main/docs/spec.md#L519) — scalar-indexed analytics columns `tool_name`, `call_id`, `is_failure` materialized on `parts`.

### Keywords/tags ❌
> Explicit keyword or tag system for categorizing stored items.

### Anticipated queries ❌
> Generates predicted search queries for each memory entry to improve retrieval recall.

### Trigger rules ❌
> Condition-based activation (e.g. "show this when file X is opened", deadlines).

### Domain tag ❌
> Tags memories with domain categories (code, marketing, legal, finance, general).
- Note: sessions carry a `project` scope ([docs/spec.md#L309](https://github.com/tenequm/pond/blob/main/docs/spec.md#L309)), which is attribution, not a domain taxonomy.

### Task type ❌
> Classifies unfinished work by type (task, idea, blocked, stale).

### Context (why) ❌
> Stores *why* a memory is relevant alongside the content.

### Source attribution ✅
> Records who/what authored the memory (user, agent, pipeline) with ≥3 distinct levels.
- Source: [docs/spec.md#L334](https://github.com/tenequm/pond/blob/main/docs/spec.md#L334) — four message roles (system/user/assistant/tool); [docs/spec.md#L307](https://github.com/tenequm/pond/blob/main/docs/spec.md#L307) — `Session.source_agent` records the producing harness; [docs/spec.md#L355](https://github.com/tenequm/pond/blob/main/docs/spec.md#L355) — every Part classified `conversational` vs `injected` (harness scaffolding), compile-enforced per adapter; [docs/spec.md#L432](https://github.com/tenequm/pond/blob/main/docs/spec.md#L432) — pond-owned ingest-host provenance stamp (username/hostname/device).

### Origin + trust ❌
> Different trust weights based on capture method (user > agent > automated).

### Emotional ❌
> Tracks sentiment or emotional intensity per memory or session.

### Conflict surfacing ❌
> Detects and surfaces conflicting information between memories.

### Layered memory ❌
> Hierarchical memory organization (e.g. L0 raw → L1 summary → L2 persona).
- Note: pond stores only the raw layer, by design ("memory is a derived view you can always rebuild from an archive", [README.md#L51](https://github.com/tenequm/pond/blob/main/README.md#L51)); no summary/persona layers.

### Time-travel ✅
> Historical state queries (past sessions, superseded versions, temporal search).
- Source: [packages/pond/src/wire.rs#L649](https://github.com/tenequm/pond/blob/main/packages/pond/src/wire.rs#L649) — `from_date` / `to_date` search filters; the corpus itself is the full history of past sessions ([README.md#L14](https://github.com/tenequm/pond/blob/main/README.md#L14)); storage-layer versioning is Lance manifest versions ([docs/spec.md#L103](https://github.com/tenequm/pond/blob/main/docs/spec.md#L103)).

### Schema fields (count: 22) ✅
> Count of distinct structured fields per memory entry (exclude auto IDs/timestamps).
- Source: [docs/spec.md#L444](https://github.com/tenequm/pond/blob/main/docs/spec.md#L444) — across the three datasets, excluding ids/timestamps: `sessions` 5 (parent_session_id, parent_message_id, source_agent, project, options), `messages` 8 (role, source_agent, project, content, search_text, vector, embedding_model, options), `parts` 9 (ordinal, type, provenance, tool_name, call_id, is_failure, variant_data, data, options).

---

## Search & Retrieval

### Full-text ✅
> Keyword-based search (FTS5, BM25, grep, or equivalent).
- Source: [packages/pond/src/sessions.rs#L2361](https://github.com/tenequm/pond/blob/main/packages/pond/src/sessions.rs#L2361) — BM25 full-text retriever over `messages.search_text` (Lance inverted index); [packages/pond/src/main.rs#L436](https://github.com/tenequm/pond/blob/main/packages/pond/src/main.rs#L436) — `pond search --mode fts`; [docs/spec.md#L722](https://github.com/tenequm/pond/blob/main/docs/spec.md#L722) — language-neutral word tokenizer with English stemming.

### Semantic/vector ✅
> Embedding-based semantic search.
- Source: [docs/spec.md#L722](https://github.com/tenequm/pond/blob/main/docs/spec.md#L722) — vector retriever (cosine, default arm) over message embeddings; [packages/pond/src/embed.rs#L333](https://github.com/tenequm/pond/blob/main/packages/pond/src/embed.rs#L333) — `intfloat/multilingual-e5-small` FP16 local embeddings; [packages/pond/src/sessions.rs#L2608](https://github.com/tenequm/pond/blob/main/packages/pond/src/sessions.rs#L2608) — IVF_SQ index above a 100k-vector activation threshold, flat scan below.

### Hybrid (BM25+Vec) ❌
> Combines full-text and vector search with result fusion (e.g. RRF).
- Note: deliberate design choice, not a gap: single-arm retrieval, one arm per query, no server-side fusion ([docs/spec.md#L718](https://github.com/tenequm/pond/blob/main/docs/spec.md#L718)); the vector arm falls back to fts when the store has no embeddings.

### Deep (incl. thinking) ❌
> Search includes model thinking/reasoning traces.
- Note: reasoning IS stored losslessly as `ReasoningPart` rows ([docs/spec.md#L366](https://github.com/tenequm/pond/blob/main/docs/spec.md#L366)) but deliberately excluded from the ranked search index; only conversational text is indexed ([docs/spec.md#L730](https://github.com/tenequm/pond/blob/main/docs/spec.md#L730)). Reasoning is reachable via `pond_get_message` and `pond_sql` over `parts`.

### Code graph ❌
> Indexes and queries code structure (Tree-sitter, AST, or equivalent).

### Docs search ❌
> Dedicated search across ingested framework/API documentation.
- Note: knowledge-base/resource files are an explicitly deferred consumer ([docs/spec.md#L771](https://github.com/tenequm/pond/blob/main/docs/spec.md#L771)).

### Fact metadata query ✅
> Structured queries on memory metadata (e.g. "all unfinished tasks in project X").
- Source: [docs/spec.md#L697](https://github.com/tenequm/pond/blob/main/docs/spec.md#L697) — `pond sql` / `pond_sql` MCP tool: read-only DataFusion SELECT over `sessions` / `messages` / `parts` (joins, counts, group-by); [README.md#L130](https://github.com/tenequm/pond/blob/main/README.md#L130) — e.g. `SELECT project, count(*) FROM messages GROUP BY project`; pushdown filters on project / session / source_agent / time range ([docs/spec.md#L738](https://github.com/tenequm/pond/blob/main/docs/spec.md#L738)).

### Timeline view ✅
> Chronological browsing or temporal search (since/before parameters).
- Source: [packages/pond/src/main.rs#L476](https://github.com/tenequm/pond/blob/main/packages/pond/src/main.rs#L476) — `--from-date` / `--to-date` (inclusive ISO date bounds); [packages/pond/src/main.rs#L462](https://github.com/tenequm/pond/blob/main/packages/pond/src/main.rs#L462) — `--sort-by recency`; [docs/spec.md#L667](https://github.com/tenequm/pond/blob/main/docs/spec.md#L667) — `pond_get_session` pages chronologically from `start` or `end` with `after_message_id` / `before_message_id`.

### Search modes (count: 3) ✅
> Count of distinct search tools/modes available.
- Source: [packages/pond/src/main.rs#L436](https://github.com/tenequm/pond/blob/main/packages/pond/src/main.rs#L436) — `vector` (semantic, default) and `fts` (BM25) arms; [docs/spec.md#L697](https://github.com/tenequm/pond/blob/main/docs/spec.md#L697) — read-only SQL surface with `contains_tokens` and `fts()` table functions ([packages/pond/src/transport.rs#L295](https://github.com/tenequm/pond/blob/main/packages/pond/src/transport.rs#L295)).

### Data sources (count: 3) ✅
> Count of distinct data types searchable (learnings, messages, code, docs, etc.).
- Source: [docs/spec.md#L442](https://github.com/tenequm/pond/blob/main/docs/spec.md#L442) — three queryable Lance datasets: `sessions`, `messages`, `parts` (parts include tool calls, tool results, reasoning, files). The ranked search index covers conversational message text only ([docs/spec.md#L730](https://github.com/tenequm/pond/blob/main/docs/spec.md#L730)); the other types are reachable via `pond_sql` and the get operations.

---

## Knowledge Lifecycle

### Decay/forgetting ❌
> Automatically reduces relevance or removes memories based on time or disuse.
- Note: the opposite is the product, "never pruned" ([README.md#L51](https://github.com/tenequm/pond/blob/main/README.md#L51)); the vector arm applies only a gentle recency tiebreaker ([docs/spec.md#L722](https://github.com/tenequm/pond/blob/main/docs/spec.md#L722)).

### Supersede/replace ❌
> Mechanism to mark one memory as replacing another, with traceable chain.
- Note: append-only by contract; a stored row is never overwritten ([docs/spec.md#L602](https://github.com/tenequm/pond/blob/main/docs/spec.md#L602)).

### Contradiction detection ❌
> Automatically detects new memories contradicting existing ones.

### Quarantine ❌
> Can exclude a session's memories from retrieval without deleting them.
- Note: injected scaffolding parts and subagent sessions are excluded from search by default ([docs/spec.md#L730](https://github.com/tenequm/pond/blob/main/docs/spec.md#L730), [docs/spec.md#L738](https://github.com/tenequm/pond/blob/main/docs/spec.md#L738)), but there is no per-session operator quarantine flag.

### Auto-resolution ❌
> Automatically resolves or archives stale items (e.g. unfinished tasks after TTL).

### Trust model ❌
> Multi-tier trust hierarchy where some sources override others.

### Explicit forget ❌
> User or agent can explicitly delete/forget a specific memory or session.
- Note: `pond erase <session-id>` (true byte purge, cascade to children, resurrection denylist) is fully specified ([docs/spec.md#L505](https://github.com/tenequm/pond/blob/main/docs/spec.md#L505), [docs/spec.md#L706](https://github.com/tenequm/pond/blob/main/docs/spec.md#L706)) but not yet shipped in the binary: [packages/pond/src/main.rs#L3781](https://github.com/tenequm/pond/blob/main/packages/pond/src/main.rs#L3781) logs "erase pending; pond erase is not yet implemented".

---

## Extraction Pipeline

### Auto-extraction ✅
> Automatically extracts structured knowledge from sessions without manual `save` calls.
- Source: [README.md#L47](https://github.com/tenequm/pond/blob/main/README.md#L47) — sessions picked up automatically from all enabled adapters; [README.md#L32](https://github.com/tenequm/pond/blob/main/README.md#L32) — `pond sync` ingests, embeds, and indexes with no manual save calls, parsing raw session logs into the structured canonical model plus derived tool columns ([docs/spec.md#L519](https://github.com/tenequm/pond/blob/main/docs/spec.md#L519)). Note: this is automatic lossless structural capture, not LLM fact/summary extraction; the latter is deliberately out of scope ([README.md#L51](https://github.com/tenequm/pond/blob/main/README.md#L51)).

### Content-aware preprocessing ✅
> Truncates or filters content by type before extraction (code vs. text differently).
- Source: [docs/spec.md#L730](https://github.com/tenequm/pond/blob/main/docs/spec.md#L730) — `search_text` built per message from conversational TextParts and FilePart metadata only; reasoning, tool bodies, approvals, and harness-injected parts filtered out by type/provenance before indexing; [docs/spec.md#L570](https://github.com/tenequm/pond/blob/main/docs/spec.md#L570) — oversized text values truncate to a marked sentinel at the adapter seam, binary blobs exempt.

### Deduplication ✅
> Detects and merges duplicate or near-duplicate memories.
- Source: [docs/spec.md#L152](https://github.com/tenequm/pond/blob/main/docs/spec.md#L152) — deterministic primary keys make ingest idempotent (merge-insert no-ops present rows); [docs/spec.md#L604](https://github.com/tenequm/pond/blob/main/docs/spec.md#L604) — adapters detect duplicate PKs, the write path drops them as a floor, with content-identity confirmation before dropping; [packages/pond/src/substrate.rs#L2190](https://github.com/tenequm/pond/blob/main/packages/pond/src/substrate.rs#L2190) — skipped-duplicate counts surfaced in the ingest summary. Note: exact/id-level dedup on ingest, not near-duplicate semantic merging.

### Quality refinement ❌
> LLM or rule-based quality pass after initial extraction (confidence, contradiction check).

### Narrative generation ❌
> Generates session summaries, handover narratives, or project profiles.
- Note: search groups hits to one representative message per session ([docs/spec.md#L722](https://github.com/tenequm/pond/blob/main/docs/spec.md#L722)); that is a matched message, not generated narrative.

### Clustering ❌
> Groups related memories by topic, embedding similarity, or semantic relationship.
- Note: IVF partitioning exists only as vector-index internals, not user-facing clustering.

### Recurrence detection ❌
> Detects recurring patterns across sessions (same bug, repeated question).

### Persona extraction ❌
> Extracts user traits, preferences, or working style into a persistent persona model.

---

## Platform Support

### Claude Code ✅
- Source: [packages/pond/src/adapter/mod.rs#L516](https://github.com/tenequm/pond/blob/main/packages/pond/src/adapter/mod.rs#L516) — `ClaudeCodeFactory` in the adapter registry; [packages/pond/src/init.rs#L851](https://github.com/tenequm/pond/blob/main/packages/pond/src/init.rs#L851) — `pond init` auto-registers the MCP server via `claude mcp add`; bundled agent skill installed into Claude Code's user skills dir ([README.md#L35](https://github.com/tenequm/pond/blob/main/README.md#L35)).

### Codex ✅
- Source: [packages/pond/src/adapter/mod.rs#L519](https://github.com/tenequm/pond/blob/main/packages/pond/src/adapter/mod.rs#L519) — `CodexCliFactory`; [packages/pond/src/init.rs#L901](https://github.com/tenequm/pond/blob/main/packages/pond/src/init.rs#L901) — MCP registration via `codex mcp add pond -- pond mcp`.

### OpenCode ✅
- Source: [packages/pond/src/adapter/mod.rs#L520](https://github.com/tenequm/pond/blob/main/packages/pond/src/adapter/mod.rs#L520) — `OpencodeFactory`; [README.md#L47](https://github.com/tenequm/pond/blob/main/README.md#L47) — opencode sessions picked up automatically.

### Gemini CLI ❌
- Note: named as a deferred future adapter ([docs/spec.md#L777](https://github.com/tenequm/pond/blob/main/docs/spec.md#L777)).

### Copilot ❌

### Cursor ❌
- Note: named as a deferred future adapter ([docs/spec.md#L777](https://github.com/tenequm/pond/blob/main/docs/spec.md#L777)).

### Windsurf ❌

### OpenClaw ✅
- Source: [packages/pond/src/adapter/mod.rs#L521](https://github.com/tenequm/pond/blob/main/packages/pond/src/adapter/mod.rs#L521) — `OpenClawFactory`; [packages/openclaw-pond/package.json#L4](https://github.com/tenequm/pond/blob/main/packages/openclaw-pond/package.json#L4) — dedicated OpenClaw plugin projecting pond's read-only recall tools into OpenClaw agents.

### Hermes ✅
- Source: [packages/pond/src/adapter/mod.rs#L523](https://github.com/tenequm/pond/blob/main/packages/pond/src/adapter/mod.rs#L523) — `HermesFactory`; [packages/hermes-pond/\_\_init\_\_.py#L1](https://github.com/tenequm/pond/blob/main/packages/hermes-pond/__init__.py#L1) — Hermes plugin registering `pond_search` / `pond_get_session` / `pond_get_message` / `pond_sql` under the `pond` toolset.

### pi/omp ✅
- Source: [packages/pond/src/adapter/mod.rs#L524](https://github.com/tenequm/pond/blob/main/packages/pond/src/adapter/mod.rs#L524) — `PiCodingAgentFactory`; [README.md#L47](https://github.com/tenequm/pond/blob/main/README.md#L47) — pi-coding-agent sessions picked up automatically.

### Antigravity ❌

> Additional platforms beyond this template's list: Claude desktop app (local agent mode), NanoClaw, and Claude.ai data export (manual import) — [packages/pond/src/adapter/mod.rs#L517](https://github.com/tenequm/pond/blob/main/packages/pond/src/adapter/mod.rs#L517), [README.md#L47](https://github.com/tenequm/pond/blob/main/README.md#L47).

---

## Benchmarks

### LoCoMo ❌
- Score: `—`

### LongMemEval ❌
- Score: `—`

### PersonaMem ❌
- Score: `—`

### Token reduction ❌
- Score: `—`

### Methodology open ✅
- Source: [docs/spec.md#L734](https://github.com/tenequm/pond/blob/main/docs/spec.md#L734) — published retrieval-quality experiment (word tokenizer vs ngram: EN Success@3 66/111 vs 31/111, UK 7/21 vs 8/21) with full rationale, plan, query set, and report in-repo under [docs/researches/](https://github.com/tenequm/pond/tree/main/docs/researches) (tokenizer-experiment-report.md, tokenizer-experiment-plan.md, tokenizer-experiment-queries.tsv, embeddings.md); criterion benches under `packages/pond/benches/`. Note: pond's own retrieval-quality experiments; no scores on the standard memory benchmarks above.
