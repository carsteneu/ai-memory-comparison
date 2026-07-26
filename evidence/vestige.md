# Vestige — Evidence

**Repo:** `github.com/samvallad33/vestige`
**Stars:** 592
**Language:** Rust
**License:** AGPL-3.0
**Created:** 2026-01-25
**Description:** Local-first cognitive memory for AI agents — FSRS-6 decay, prediction-error-gated ingest, MCP-native, single Rust binary with an embedded dashboard.

> **All citations pin to commit [`54f69b3`](https://github.com/samvallad33/vestige/tree/54f69b369ec478aefddfc72093bf06d0fc9d21a3)** (`origin/main`, v2.3.0, 2026-07-26) so line numbers stay valid permanently.
>
> This file updates the 2026-05-28 audit of Vestige at v2.1.23. That audit was explicit that it worked from the README — it wrote *"the following features are genuinely not mentioned anywhere in the README"* and titled its inventory *"Feature Inventory (from README)."* It was accurate and fair on that basis, and it corrected eleven cells in Vestige's favour unprompted plus a repo URL that pointed at a 404. Since `CONTRIBUTING.md` states *"Code beats docs,"* this pass re-checks every feature against source at a pinned commit.
>
> **Four cells currently marked ✅ are corrected DOWN to ❌ here** (`entities`, `deep`, `trustModel`, `autoExtract`). They did not survive their own definitions. They are listed with the same evidence standard as the upgrades.

---

## System Metadata

| Field | Value |
|-------|-------|
| **Deployment** | `Local binary (22MB)` |
| **Storage** | `SQLite + FTS5 + USearch HNSW` |
| **Integration** | `MCP` |
| **Single binary?** | `yes` |
| **Setup** | `cargo install` / `npx @vestige/init` |
| **Pricing** | `free` |
| **Storage unit** | `Cognitive memory unit` |

---

## Architecture

### Proxy ❌
> Intercepts and modifies the LLM conversation stream in-flight.

Integration is MCP stdio + Streamable HTTP + shell hooks — all excluded by the definition.

### Web/TUI ✅
- [`crates/vestige-mcp/src/dashboard/static_files.rs:14`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/dashboard/static_files.rs#L14) — `include_dir!("$CARGO_MANIFEST_DIR/../../apps/dashboard/build")` embeds the compiled SvelteKit app into the binary
- [`crates/vestige-mcp/src/bin/cli.rs:221`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/bin/cli.rs#L221) — `vestige dashboard` serves it on 127.0.0.1:3927

### Offline ✅
- [`crates/vestige-core/Cargo.toml:14`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/Cargo.toml#L14) — `reqwest` is `optional = true`, pulled in only by the non-default `connectors`/`cloud-sync` features; a default build links no HTTP client
- [`crates/vestige-core/src/embeddings/local.rs:17`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/embeddings/local.rs#L17) — local ONNX embeddings after a one-time model download

### Multi-agent ❌
Multiple MCP clients can share one `--data-dir`, but there is no agent identity (`git grep agent_id` returns nothing), no agent directory, and no inter-agent messaging. Not claimed.

### LLM providers (count: 1) ✅
- [`crates/vestige-core/src/embeddings/local.rs:47`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/embeddings/local.rs#L47) — one provider (fastembed). Two selectable models run on the same runtime; the second is behind a non-default cargo feature. Count stays 1.

### Cache optimization ✅ ← **was ❌**
- [`crates/vestige-core/src/storage/sqlite.rs:318`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/storage/sqlite.rs#L318) — `query_cache: Option<Mutex<LruCache<String, Vec<f32>>>>`
- [`crates/vestige-core/src/storage/sqlite.rs:2843`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/storage/sqlite.rs#L2843) — `get_query_embedding()` returns the cached vector on hit, `cache.put(...)` on miss, so repeated queries skip re-embedding
- [`crates/vestige-core/Cargo.toml:156`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/Cargo.toml#L156) — dependency declared under the comment "LRU cache for query embeddings"

*Definitional note, volunteered:* the evidence template's wording ("caches intermediate results — embeddings, search results") is satisfied plainly. `CRITERIA.md`'s wording leans toward prompt/token caching ("prompt cache optimization, context collapse prevention, token-saving"), which Vestige does not do. The two documents differ; happy to take your ruling under whichever governs.

### Procedural memory ❌
`MemorySystem::Procedural` ([`memory/mod.rs:81`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/memory/mod.rs#L81)) is a memory-type classification. Nothing loads, interprets, or executes stored content. The definition requires execution at retrieval time. Not claimed.

### Sandboxed execution ❌
`git grep -i sandbox` over `crates/` returns zero hits.

### Scheduled/autonomous ✅ ← **was ❌**
- [`crates/vestige-mcp/src/main.rs:451`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/main.rs#L451) — `autopilot::spawn(...)` runs at server startup, opt-*out* via `VESTIGE_AUTOPILOT_ENABLED=0`
- [`crates/vestige-mcp/src/autopilot.rs:461`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/autopilot.rs#L461) — `tokio::time::interval(Duration::from_secs(60))` poller
- [`crates/vestige-mcp/src/autopilot.rs:343`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/autopilot.rs#L343) — autonomously calls `storage.promote_memory()` when `composite_score > 0.85`, with no user prompt
- [`crates/vestige-core/src/storage/sqlite.rs:3633`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/storage/sqlite.rs#L3633) — unattended consolidation cycle every 6h (`VESTIGE_CONSOLIDATION_INTERVAL_HOURS`)

*Disclosure:* two autonomous behaviours are env-gated but default **on** — `VESTIGE_AUTO_CONSOLIDATE_MERGE` and `VESTIGE_BACKFILL_AUTOFIRE`.

### Privacy/encrypt ✅
- [`crates/vestige-core/src/storage/sqlite.rs:468`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/storage/sqlite.rs#L468) — SQLCipher at rest via `conn.pragma_update(None, "key", ...)`
- [`crates/vestige-core/src/storage/cloud_crypto.rs:35`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/storage/cloud_crypto.rs#L35) — Argon2id + XChaCha20-Poly1305 envelope applied client-side before any upload

### Data export ✅ ← **was ❌**
- [`crates/vestige-mcp/src/bin/cli.rs:158`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/bin/cli.rs#L158) — `vestige export <output> --format json|jsonl [--tags ...] [--since ...]` clap subcommand
- [`crates/vestige-mcp/src/bin/cli.rs:2075`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/bin/cli.rs#L2075) — `run_export()` implementation
- [`crates/vestige-core/src/storage/sqlite.rs:6414`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/storage/sqlite.rs#L6414) — second path, `export_portable_archive()` (ID/FSRS/edge-preserving JSON)

---

## Data Model

### Entities ❌ ← **was ✅ (corrected down)**
- [`crates/vestige-core/src/advanced/retroactive_backfill.rs:117`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/advanced/retroactive_backfill.rs#L117) — `extract_entities()` is a heuristic tokenizer (tags + UPPER_SNAKE tokens + tokens containing `/` or `.`) returning `Vec<String>`

It is computed per call and **never persisted**. There is no entity column and no entity table, and no extraction of people or packages. `CodeEntity`/`EntityType` ([`codebase/types.rs:440`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/codebase/types.rs#L440)) is unreachable from the MCP server. The definition requires entities "as separate fields or tables." Not met.

### Actions ❌
[`agent_traces`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/storage/migrations.rs#L1079) has a dedicated `tool` column written on every MCP call, but arguments are FNV-1a hashed and never stored, and unified dispatchers mean the real operation lives in `args.mode`/`args.action` inside that hash. `tool` records `"memory"`, never `"promote"` vs `"demote"`. Not claimed.

### Keywords/tags ✅
- [`crates/vestige-core/src/storage/migrations.rs:152`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/storage/migrations.rs#L152) — `tags TEXT DEFAULT '[]'`, FTS5-indexed with sync triggers at `:174`
- [`crates/vestige-mcp/src/tools/smart_ingest.rs:46`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/tools/smart_ingest.rs#L46) — first-class ingest parameter

### Anticipated queries ❌
HyDE ([`search/hyde.rs:79`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/search/hyde.rs#L79)) expands the *incoming query* at search time; variants are never persisted or bound to a node.

### Trigger rules ✅ ← **was ❌**
- [`crates/vestige-core/src/storage/migrations.rs:225`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/storage/migrations.rs#L225) — `intentions` table with `trigger_type`, `trigger_data` JSON, and `deadline` columns
- [`crates/vestige-core/src/neuroscience/prospective_memory.rs:261`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/neuroscience/prospective_memory.rs#L261) — `ContextPattern::FilePattern` / `InCodebase` / `TopicActive` / `UserMode`, evaluated by `IntentionTrigger::is_triggered(context, events)`
- [`crates/vestige-mcp/src/tools/intention_unified.rs:39`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/tools/intention_unified.rs#L39) — live `intention` tool schema exposing `file_pattern`, `codebase`, `topic`, `condition`
- [`crates/vestige-mcp/src/server.rs:303`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/server.rs#L303) — registered; dispatched at [`:556`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/server.rs#L556)

This is the definition's own example ("show this when file X is opened") plus deadlines, persisted and evaluated.

### Domain tag ❌
Columns exist but the production INSERT hardcodes `domains`/`domain_scores` to the string literals `'[]'` and `'{}'` ([`sqlite.rs:707`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/storage/sqlite.rs#L707)). No domain vocabulary exists.

### Task type ❌
`IntentionStatus` is a lifecycle, not a type. The closest match, `WorkStatus`, belongs to `WorkContext`, which is never constructed.

### Context (why) ❌
No "why" column exists. `build_and_save_receipt` has zero callers repo-wide, so `memory_receipts` is never populated.

### Source attribution ❌
`WriteSource` has 4 levels, but every production emit site hardcodes `Agent` ([`trace_recorder.rs:141`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/trace_recorder.rs#L141)); `Dream`/`Connector` appear only in unit tests. Fewer than 3 distinct levels in practice. Not claimed.

### Origin + trust ❌
Trust is derived from FSRS state, not capture method. The only capture-method-sensitive logic lives in `classify_write`, whose sole callers are its own `#[cfg(test)]` tests.

### Emotional ❌
`EmotionalMemory` ([`neuroscience/emotional_memory.rs:140`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/neuroscience/emotional_memory.rs#L140)) is consumed only by `DreamEngine`, which has no production callers. Live ingest hardcodes `sentiment_score: 0.0`; `emotional_valence` appears in exactly one code site, a `row.get()` read, and is never written.

### Conflict surfacing ✅ ← **was ❌**
- [`crates/vestige-mcp/src/tools/contradictions.rs:105`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/tools/contradictions.rs#L105) — pairwise detector gated on topic overlap ≥ 0.4, winner decided by higher FSRS trust
- [`crates/vestige-core/src/advanced/prediction_error.rs:549`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/advanced/prediction_error.rs#L549) — `detect_contradiction` runs at write time inside the `smart_ingest` gate
- [`crates/vestige-mcp/src/server.rs:282`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/server.rs#L282) — `recall(mode='contradictions')` registered; surfaced at `/api/contradictions`

*Stated plainly:* detection is lexical (negation and correction word pairs), not NLI.

### Layered memory ❌
`temporal_level` has no writer anywhere. The only non-NULL `summary_parent_id` write is inside `#[cfg(test)]`. `compressed_memories` was dropped in migration V11.

### Time-travel ❌
Supersede is invalidate-don't-delete, so old versions remain retrievable — but `query_at_time` has zero callers and `RecallInput.valid_at` is ignored by `Storage::recall`. No as-of query is reachable. Not claimed.

### Schema fields (count: 27) ✅
- [`crates/vestige-core/src/memory/node.rs:180-285`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/memory/node.rs#L180-L285) — `KnowledgeNode` has **31 fields**; 27 after excluding the 4 auto fields (`id`, `created_at`, `updated_at`, `last_accessed`)

```
content, node_type, stability, difficulty, reps, lapses, storage_strength,
retrieval_strength, retention_strength, sentiment_score, sentiment_magnitude,
next_review, source, tags, valid_from, valid_until, utility_score,
times_retrieved, times_useful, emotional_valence, flashbulb, temporal_level,
has_embedding, embedding_model, suppression_count, suppressed_at, source_envelope
```

The current entry lists 5. `CRITERIA.md` asks for an "approximate count of distinct structured fields per memory entry", which is 27 as defined. If you prefer to count only fields with a live production writer, the number is ~20 — either way, 5 is off by 4-5x. Both counts offered; your rubric, your pick.

---

## Search & Retrieval

### Full-text ✅
- [`crates/vestige-core/src/storage/migrations.rs:174`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/storage/migrations.rs#L174) — `CREATE VIRTUAL TABLE ... knowledge_fts USING fts5(...)`, queried with `MATCH ... ORDER BY rank` (BM25)

### Semantic/vector ✅
- [`crates/vestige-core/src/search/vector.rs:98`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/search/vector.rs#L98) — USearch HNSW, `MetricKind::Cos`

### Hybrid (BM25+Vec) ✅
- [`crates/vestige-core/src/storage/sqlite.rs:2970`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/storage/sqlite.rs#L2970) — `reciprocal_rank_fusion(&keyword_results, &semantic_results, 60.0)`, RRF k=60

### Deep (incl. thinking) ❌ ← **was ✅ (corrected down)**
- [`crates/vestige-core/src/trace/mod.rs:78`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/trace/mod.rs#L78) — MCP call args are stored as `args_hash` "so traces never leak prompt contents or secrets"
- [`crates/vestige-core/src/storage/trace_store.rs:159`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/storage/trace_store.rs#L159) — the trace store exposes `get_trace(run_id)` and `list_agent_runs` and **no search function**

No model thinking or reasoning trace is stored anywhere; a repo-wide grep for `thinking_trace`/`reasoning_trace`/`chain_of_thought` returns zero hits. `recall(mode='reason')` is deep reasoning *over memories*, which is not what this column measures. The v2.1.23 audit reasonably read `deep_reference`'s 8-stage pipeline as satisfying this; on source it does not.

### Code graph ❌
`codebase/relationships.rs` is a file-path co-edit graph, not code structure. `RelationshipSource::AstAnalysis` is a dead enum variant with zero constructors, the only code "parsing" is `line.starts_with("pub fn ")`, and there is no `tree-sitter` or `syn` dependency.

### Docs search ❌
The only connectors are GitHub Issues and Redmine issues ([`tools/source_sync.rs:35`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/tools/source_sync.rs#L35)). No documentation ingestion.

### Fact metadata query ✅ ← **was ❌**
> Structured queries on memory metadata (e.g. "all unfinished tasks in project X", "all decisions about Y").

- [`crates/vestige-core/src/storage/sqlite.rs:2767`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/storage/sqlite.rs#L2767) — `get_nodes_by_type_and_tag(node_type, tag_filter, limit)`: a pure metadata query, no text query required
- [`crates/vestige-mcp/src/tools/codebase_unified.rs:301`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/tools/codebase_unified.rs#L301) — exposed live: `codebase(action='get_context')` returns all `pattern`/`decision` nodes for a codebase tag — literally the criterion's "all decisions about Y"
- [`crates/vestige-mcp/src/tools/intention_unified.rs:129`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/tools/intention_unified.rs#L129) — `intention(action='list', filter_status='active')` — literally "all unfinished tasks"

*Scope stated plainly:* these are fixed structured surfaces, not a general metadata query language; the main search tool still requires a text query. Claimed because the criterion's own two examples are both directly satisfied.

### Timeline view ✅
- [`crates/vestige-mcp/src/tools/timeline.rs:17`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/tools/timeline.rs#L17) — ISO-8601 `start`/`end` range, `node_type`, `tags`, grouped by day

### Search modes (count: 7) ✅
`recall` lookup / `recall` reason / `recall` contradictions / `memory_status` timeline / `memory_status` changelog / `graph` associations / `graph` predict. (The auto-detected literal/exact routing inside `recall` is deliberately **not** counted as an eighth mode: it is a parameter, not a distinct tool.) — registered at [`server.rs:254`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/server.rs#L254) and [`:341`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/server.rs#L341). Current entry says 4.

### Data sources (count: 3) ✅
Memories/learnings; issue-tracker records (GitHub Issues with folded comment threads, Redmine issues and journals — [`connectors/github.rs:312`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/connectors/github.rs#L312)); codebase patterns and decisions. Connectors ship on by default ([`release.yml:41`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/.github/workflows/release.yml#L41)). Current entry says 1.

---

## Knowledge Lifecycle

### Decay/forgetting ✅
- [`crates/vestige-core/src/storage/sqlite.rs:3513`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/storage/sqlite.rs#L3513) — `apply_decay()` rewrites retrieval/retention strength from the FSRS-6 retrievability curve, in an unattended 6-hour loop

### Supersede/replace ✅
- [`crates/vestige-core/src/storage/migrations.rs:789`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/storage/migrations.rs#L789) — `superseded_by` column + index (bitemporal: the old node stays queryable, stamped `valid_until`)
- [`crates/vestige-core/src/storage/sqlite.rs:8384`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/storage/sqlite.rs#L8384) — previewable `plan_supersede` → `apply_plan` → reversible undo log

### Contradiction detect ✅
- [`crates/vestige-core/src/advanced/prediction_error.rs:364`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/advanced/prediction_error.rs#L364) — every non-forced ingest embeds the new content, pulls top-k similar memories, and runs `detect_contradiction` on each pair

Rule-based (8 negation pairs, 9 correction phrases), not an NLI model.

### Quarantine ❌
`suppress` is a ranking penalty capped at 80% ([`active_forgetting.rs:38`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/neuroscience/active_forgetting.rs#L38)), not exclusion — suppressed memories still return from search. The `ReviewMode::Quarantine` firewall exists but `gate_writes` has zero production callers. No session scoping exists.

### Auto-resolution ❌
`auto_expire` exists only on the in-process map; persisted intentions are never registered with it, so the poller checks an empty map.

### Trust model ❌ ← **was ✅ (corrected down)**
- [`crates/vestige-mcp/src/tools/cross_reference.rs:62`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/tools/cross_reference.rs#L62) — `compute_trust` is a single derived float: `0.4·retention + 0.2·min(stability/30,1) + 0.2·min(reps/10,1) + 0.2·(1−lapses/5)`

That is FSRS state, not provenance. The `WriteSource` hierarchy that would make this a multi-tier source model is hardcoded to `Agent` at every production site. The only live tier is the user `protected` pin.

### Explicit forget ✅
- [`crates/vestige-mcp/src/tools/memory_unified.rs:46`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/tools/memory_unified.rs#L46) — `memory action='purge'|'delete'` requiring `confirm=true`
- [`crates/vestige-core/src/storage/sqlite.rs:2333`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/storage/sqlite.rs#L2333) — `purge_node` removes content **and** embeddings, retaining only a content-free tombstone

---

## Extraction Pipeline

### Auto-extraction ❌ ← **was ✅ (corrected down)**
Every write path is an explicitly invoked MCP tool ([`server.rs:564`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/server.rs#L564)). A repo-wide grep for `transcript`, `auto_capture`, `auto_ingest`, and `session_end` returns zero hits in `crates/`.

`smart_ingest` enriches what it is handed (importance scoring, intent tagging, prediction-error routing), but an agent must call it. The definition's load-bearing clause is "without manual `save` calls," and Vestige is a manual-save system with a smart gate behind it.

### Content-aware preprocessing ❌
`preprocess_code`/`_error_log`/`_structured` are fully implemented at [`adaptive_embedding.rs:532`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/advanced/adaptive_embedding.rs#L532) but have no production caller; `smart_ingest` calls `ContentType::detect` and discards the result into `_content_type`.

### Deduplication ✅
- [`crates/vestige-core/src/storage/sqlite.rs:4066`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/storage/sqlite.rs#L4066) — `auto_dedup_consolidation` clusters at cosine ≥ 0.85 and merges automatically each cycle
- [`crates/vestige-mcp/src/tools/dedup.rs:173`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/tools/dedup.rs#L173) — manual `scan`/`plan_merge`/`apply`/`undo` with union-find clustering

### Quality refinement ✅ ← **was ❌**
> LLM-based or rule-based quality pass after initial extraction (confidence scoring, contradiction check).

Rule-based, exactly the criterion's parenthetical:

- [`crates/vestige-mcp/src/tools/smart_ingest.rs:186`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/tools/smart_ingest.rs#L186) — 4-channel importance/confidence composite computed for every ingest
- [`crates/vestige-core/src/advanced/prediction_error.rs:364`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/advanced/prediction_error.rs#L364) — contradiction check against top-k similar memories inside the same gate, rerouting create → update/supersede/merge
- [`crates/vestige-core/src/advanced/dreams.rs:1541`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/advanced/dreams.rs#L1541) — post-hoc: consolidation-generated insights are dropped unless `novelty_score >= config.min_novelty` and confidence passes

No LLM is involved; the criterion explicitly allows rule-based.

### Narrative generation ❌
`MemoryCompressor::generate_summary` runs in consolidation step 9, but its result is bound to `if let Some(_compressed)` at [`sqlite.rs:3909`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/storage/sqlite.rs#L3909) and discarded. Nothing is persisted or surfaced.

### Clustering ✅ ← **was ❌**
> Groups related memories by topic, embedding similarity, or semantic relationship.

- [`crates/vestige-core/src/advanced/dreams.rs:1456`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/advanced/dreams.rs#L1456) — `find_clusters`: connected components over discovered connections (embedding cosine when available, else tag/word Jaccard), running unattended in consolidation step 8 ([`sqlite.rs:3702`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-core/src/storage/sqlite.rs#L3702)); cluster membership persists via `insights.source_memories`
- [`crates/vestige-mcp/src/tools/dedup.rs:173`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/crates/vestige-mcp/src/tools/dedup.rs#L173) — on-demand union-find clusters at cosine ≥ threshold

"Embedding similarity" grouping is the criterion's own wording. There is no *topic model*; the criterion does not require one.

### Recurrence detection ❌
Tag-count heuristics only, with no session model or same-bug identity matching.

### Persona extraction ❌
The only occurrence of "persona" in `crates/` is a string in a sensitive-topics gating list.

---

## Platform Support

### Claude Code ✅
- [`docs/CONFIGURATION.md:209`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/docs/CONFIGURATION.md#L209) — `claude mcp add vestige vestige-mcp -s user`
- [`docs/CLAUDE-SETUP.md`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/docs/CLAUDE-SETUP.md) — dedicated protocol doc, plus a hook harness under `hooks/`

### Codex ✅
- [`docs/integrations/codex.md`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/docs/integrations/codex.md) — dedicated page; `codex mcp add vestige -- vestige-mcp`

### OpenCode ✅ ← **was ❌**
- [`docs/integrations/opencode.md`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/docs/integrations/opencode.md) — dedicated page, "Verified with OpenCode 1.16.2 on June 8, 2026", documents the OpenCode-specific `mcp` config shape and warns that `mcpServers` does not work there
- [`packages/vestige-init/bin/init.js:108`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/packages/vestige-init/bin/init.js#L108) — auto-detect/auto-install target

### Gemini CLI ❌
Zero occurrences tree-wide.

### Copilot ❌
[`docs/integrations/vscode.md`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/docs/integrations/vscode.md) is titled "VS Code (GitHub Copilot)" and names Copilot in its prerequisites, setup path, and verification steps. Left ❌ because the column may mean Copilot outside VS Code — happy to take the maintainer's ruling either way.

### Cursor ✅ ← **was ❌**
- [`docs/integrations/cursor.md`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/docs/integrations/cursor.md) — dedicated page with per-OS config paths and project-level `.cursor/mcp.json`

### Windsurf ✅
- [`docs/integrations/windsurf.md`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/docs/integrations/windsurf.md) — dedicated page, per-OS `mcp_config.json` paths

### OpenClaw ❌ / Hermes ❌ / pi-omp ❌ / Antigravity ❌
Zero occurrences tree-wide for each. (The single "Hermes" hit is a `.gitignore` rule.)

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

### Methodology open ✅ ← **was ❌**
- [`README.md:128-157`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/README.md#L128-L157) — the "Silent Rotation" experiment
- Artifacts on the public branch [`benchmark/silent-rotation`](https://github.com/samvallad33/vestige/tree/f7606e65b11aad0dcf6bda682236caa63eed9358/benchmarks/silent-rotation) — `PREREGISTRATION.md`, `EVIDENCE.md`, `harness/` with 7 competitor arm runners (mem0, supermemory, zep, hindsight, rag, sync, anarchy), and 246 raw agent transcripts

Pre-registered before results, with losing trials disclosed. The repro is stdlib-only and needs no network or API keys:

```
python3 tests/bm25_baseline.py results/runA-trial-1/corpus-export.json --no-dense
```

*Disclosure:* `benchmarks/` has **zero files on `main`** at the pinned SHA — the artifacts live on the `benchmark/silent-rotation` branch, which the README's clone command names explicitly. Flagging this rather than letting it read as a broken link.

*Also disclosed:* an earlier "CauseBench" benchmark was **withdrawn and its numbers retracted** by the project ([`CHANGELOG.md:170-181`](https://github.com/samvallad33/vestige/blob/54f69b369ec478aefddfc72093bf06d0fc9d21a3/CHANGELOG.md#L170-L181)). Stale copies of those figures survive in two dead files under `docs/launch/`. They are not live claims and should not be credited to this project.

---

## Summary of changes

**Upgraded (11):** `cacheOpt`, `scheduledExec`, `export`, `triggerRules`, `conflict`, `factQuery`, `qualityRefine`, `clustering`, `p_opencode`, `p_cursor`, `b_methodology`

**Corrected down (4):** `entities`, `deep`, `trustModel`, `autoExtract`

**Counts corrected:** `schemaFields` 5 → 27, `searchModes` 4 → 7, `dataSources` 1 → 3

Net effect on coverage: 21/60 → 28/60.
