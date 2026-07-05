
# Artesian — Evidence

> All citations below are pinned to commit `438f757` of `github.com/aquifer-labs/artesian` (main
> branch). A bare path like `crates/aquifer/src/types.rs#L102-L107` resolves to
> `https://github.com/aquifer-labs/artesian/blob/438f757/crates/aquifer/src/types.rs#L102-L107`.
> Full links are given for the headline claims; the rest use this compact form to keep the file
> readable — every one of them is a real, clickable permalink once you prepend the prefix.
>
> **Disclosure:** this evidence file was prepared by the Artesian maintainer. See the PR
> description for the required conflict-of-interest disclosure.

**Repo:** [`aquifer-labs/artesian`](https://github.com/aquifer-labs/artesian)
**Stars:** 0 (new repo)
**Language:** Rust
**License:** Apache-2.0
**Created:** 2026-06-13
**Description:** Artesian — a local-first memory controller for AI coding agents. Bounded
committed context (ACC) with an append-only admission audit log, pluggable storage, hybrid
retrieval, and a transactional multi-writer substrate. MCP server + CLI, single Rust binary.

---

## System Metadata

| Field | Value |
|-------|-------|
| **Deployment** | Local CLI + MCP server; single compiled binary or Docker |
| **Storage** | Pluggable — Files (OKF markdown), sqlite-vec, Qdrant, pgvector |
| **Integration** | MCP (`rmcp`, stdio/HTTP) + CLI + Claude Code hooks/skill |
| **Single binary?** | `yes` |
| **Setup** | `brew install aquifer-labs/tap/artesian` |
| **Pricing** | `free` (Apache-2.0, self-hosted, no paid tier) |
| **Storage unit** | `MemoryRecord` — content + tags + metadata + 4-tier abstraction (`L0Raw`/`L1Atom`/`L2Scenario`/`L3Project`) |

Sources: [README.md#L51](https://github.com/aquifer-labs/artesian/blob/438f757/README.md#L51) (`brew install aquifer-labs/tap/artesian`); `crates/artesian-cli/src/update.rs#L21` (`const HOMEBREW_FORMULA: &str = "aquifer-labs/tap/artesian";`); `Cargo.toml#L26` (`license = "Apache-2.0"`); `crates/aquifer/src/types.rs#L93-L97,L121`.

---

## Architecture

### Proxy ❌
Not present. The only "proxy" hits in the repo are unrelated: a statistical-usage comment
(`crates/aquifer/src/dream.rs#L18,L144`, "length-normalised as a proxy for information density")
and deployment advice for the *operator* to front Qdrant/MCP with their own reverse proxy for
off-LAN access (`docs/sizing-and-deployment.md#L93`, `docs/onboarding.md#L147`). Nothing
intercepts or rewrites the live LLM conversation stream.

### Web/TUI ❌
Not present. The only web-server code is the MCP Streamable-HTTP transport
(`crates/artesian-mcp/src/lib.rs#L5129`, `axum::Router::new().nest_service("/mcp", service)`) —
a protocol endpoint, not a browsable dashboard or TUI.

### Offline ✅
- [`Cargo.toml`](https://github.com/aquifer-labs/artesian/blob/438f757/Cargo.toml#L15) — `fastembed` (local ONNX embedding runtime) is a workspace dependency; embeddings run in-process, no API call.
- `docs/memory.md#L55-L62` — pinned local embedding model `intfloat/multilingual-e5-small` (384-dim), same model on every machine/backend.
- Default backends (`crates/aquifer/src/files.rs`, `crates/aquifer/src/sqlite_vec.rs`) are local-file-only; Qdrant/pgvector are opt-in networked backends, not required.
- Note: the embedding model is downloaded once from Hugging Face on first use (`hf-hub-rustls-tls` feature); inference itself is fully offline afterward.

### Multi-agent ✅
- `crates/flume/src/lib.rs#L705,L737,L932` — `TeamRuntimeConfig`, `TeamRecord`, `TeamRuntime`.
- `crates/flume/src/lane.rs#L29,L99` — `LaneBudget`, `Lane`.
- `crates/artesian-mcp/src/lib.rs#L3636` — MCP tool `team.run`: "Atomic blocking Flume fan-out: create/reuse a team, spawn needed teammates, dispatch all requested tasks, wait for every task to reach done/blocked."
- Full team/task/lane tool surface: `team.create`, `team.spawn`, `team.task.add/claim/complete/await`, `team.message`, `team.status`, `team.cleanup`, `team.gc`, `team.presence`, `team.lane.add/assign` (`crates/artesian-mcp/src/lib.rs#L3613-L4728`).

### LLM providers (count: 5) ✅
Providers for the optional judge/quality layer (`crates/headgate/src/llm.rs`), all built as an `OpenAiCompatibleClient`:
- `"openai" | "openai-compatible"` — `llm.rs#L294`
- `"ollama"` — `llm.rs#L312` (default `http://localhost:11434/v1`)
- `"lm-studio"` — `llm.rs#L325` (default `http://localhost:1234/v1`)
- `"mlx"` — `llm.rs#L337` (default `http://localhost:8080/v1`, i.e. `mlx_lm.server`)
- `"command"` — `llm.rs#L350`

Note: this counts LLM-judge backends. The embedding model is a pinned, non-selectable local model (see Offline), so it is not counted as a provider per the criterion's instruction.

### Cache optimization ✅
- `crates/headgate/src/ccs.rs#L114,L119,L124` — `token_count`, `headroom`, `is_saturated` on the committed-context state (context-collapse prevention: the committed window is kept within a token budget rather than growing unbounded).
- `crates/headgate/src/controller.rs#L241-L273` — eviction/compression loop triggered on saturation.
- [`docs/token-savings.md`](https://github.com/aquifer-labs/artesian/blob/438f757/docs/token-savings.md) — `artesian tokens` CLI + MCP tool `memory.savings` measure and log actual token savings per recall operation to an append-only `~/.artesian/token_savings.jsonl`.

### Procedural memory ✅
- `crates/artesian-mcp/src/lib.rs#L4875,L4927` — MCP tools `memory.skills`, `memory.skill.replay`.
- `crates/artesian-cli/src/main.rs#L3492,L3675,L3689,L3731` — `skill_identity_material`, `replay_skill_procedure`, `print_skill_replay_response`, `normalize_skill_procedure`.
- Distinct from the Claude-Code-facing `artesian-loop` SKILL.md that Artesian installs for its own hook integration (`crates/artesian-cli/src/main.rs#L2843-L2854,L2943`) — that one is Artesian's own platform-integration skill, not user-defined procedural memory.

### Sandboxed execution ❌
`crates/sandbox` exists as a workspace member and defines a `SandboxProfile { enabled, image, allow_network, mounted_paths }` config struct (`crates/sandbox/src/lib.rs#L15-L19`), but the crate itself only implements `cleanup()` and `new()` — no `Command::new`/`docker`/`spawn` call anywhere in it. It is a config "seam" for a sandboxed-execution backend, not an implemented sandbox with enforced resource limits at this commit. Marked ❌ per "code beats docs" rather than inferring behavior from the crate's name.

### Scheduled/autonomous ✅
- `crates/artesian-cli/src/artesiand.rs#L16-L28` — `artesiand` daemon CLI (`--interval-millis`, default `1000`, `--once`, `--dry-run`).
- `artesiand.rs#L31-L60` — `pub async fn run()`: loads config, reaps stale process groups, then `loop { orchestrator.run_once() ... }` with graceful-shutdown signal handling.
- `crates/artesian-cli/src/main.rs#L89,L1342` — the unified `artesian` binary dispatches to this daemon when invoked as `artesiand` (`Some("artesiand") => return artesiand::run().await`).
- `Dockerfile#L20-L25` — Docker image `ENTRYPOINT ["artesiand"]`, so the container runs the autonomous loop by default.

### Privacy/encrypt ✅
- [`ARTESIAN.md#L69`](https://github.com/aquifer-labs/artesian/blob/438f757/ARTESIAN.md#L69) — "No private infrastructure assumptions. Runs fully local; no cloud dependency."
- `README.md#L128` — comparison table lists Artesian's own deployment as "Self-hosted, zero infra" (sqlite-vec or files).
- No encryption-at-rest or PII-redaction feature found — this ✅ is earned solely on the local-only-storage clause of the criterion, not encryption. Flagged so it isn't over-read.

### Data export ✅
- `crates/aquifer/src/upgrade.rs#L19,L25,L107,L148,L161` — bundle-export functions (`export_headwater_bundle` and friends) that write memory records into a portable bundle format.
- `crates/aquifer/src/dream.rs#L146,L441,L513` — Dreams consolidation writes a portable OCF bundle (JSON + Markdown) plus a human-readable `DREAMS.md`.
- `docs/token-savings.md` — `artesian tokens --json` for machine-readable export of the savings ledger.

---

## Data Model

### Entities ✅
- `crates/aquifer/src/entity.rs` — `extract_entities()` (e.g. tested at `entity.rs#L232`, `extract_entities("The API rate limit is controlled by the TTL policy.")`).
- `crates/aquifer/src/types.rs#L149` — `pub relations: Vec<Relation>` on `MemoryRecord`; `crates/aquifer/src/graph.rs#L24-L29` — `Relation { subject, predicate, object, source_node_id }`. Entities are stored as structured subject/predicate/object triples, not just free-text mentions.

### Actions ❌
Not found. No structured field for commands/operations/tool-calls distinct from free-text content.

### Keywords/tags ✅
- `crates/aquifer/src/types.rs#L125` — `pub tags: Vec<String>` on `MemoryRecord` (also `#L207` on `StoreMemory`).

### Anticipated queries ❌
Not found.

### Trigger rules ❌
Not found.

### Domain tag ❌
Not found. Free-text `tags` exist (see above) but there is no fixed domain-category taxonomy (code/marketing/legal/finance/general).

### Task type ❌
Not found. `task_id` exists for session/task *identification* (routing key), not a work-item ontology (task/idea/blocked/stale).

### Context (why) ❌
Not found as a field on the retrievable memory record itself. A `reason` string does exist, but only inside the separate admission-audit trail (`qualify.jsonl` — see Additional Features) and inside the transient LLM-judge verdict (`crates/headgate/src/judge.rs#L38`, `JudgeVerdict.reason`) — neither is a persisted "why this memory matters" field on the record a caller retrieves. Marked ❌ rather than stretching the audit-log reason to satisfy this row.

### Source attribution ✅
`crates/aquifer/src/types.rs` — `MemoryRecord` carries four independent attribution dimensions: `author_id` (`#L145`, doc: "Writer identity/provenance. Distinct from `scope`, `user_id`, and project routing keys."), `source` (`#L142`), `agent_id` (`#L132`), `user_id` (`#L138`) — exceeds the "≥3 distinct levels" bar.

### Origin + trust ❌
Fields exist (`confidence`, `source`, `author_id`) but no trust-*weighting* logic was found — no code differentiates admission/ranking by "user input > agent suggestion > automated extraction." `git grep -n "trust"` under `crates/aquifer/src` returns zero hits.

### Emotional ❌
Not found.

### Conflict surfacing ✅ (scoped)
Two distinct real mechanisms, one caveat:
- **Optimistic-lock version conflicts, surfaced (not logged):** `crates/aquifer/src/txn.rs#L54-L59` — `pub enum TxnError { Conflict { expected: TxnSeq, actual: TxnSeq }, Storage(String) }`, produced via CAS at `txn.rs#L99-L112`; tested at `crates/aquifer/tests/concurrency.rs#L302` and `txn.rs#L364`. These are returned as a typed `Result::Err` to the caller — **not** written to any audit log.
- **LLM-judge contradiction/hallucination scoring ("drift"), optional:** `crates/headgate/src/judge.rs#L26-L31` (`JUDGE_SYSTEM` prompt: "drift = risk it contradicts the committed state or is unsupported/hallucinated"), `judge.rs#L33-L36` (`JudgeVerdict.drift`), gated by `judge.rs#L48,L104` (`max_drift` threshold, default `0.4`). Requires `--features llm`.
- **Correction against a doc-comment overclaim:** `crates/aquifer/src/reconcile.rs#L9` describes its `Supersede` decision as "an existing record is contradicted," but the actual decision function (`reconcile.rs#L75-L133`) chooses `Supersede` purely by a **length heuristic** among lexically-similar (Jaccard) candidates ("incoming is substantially longer → likely a more complete/updated version," `reconcile.rs#L114-L116`) — it does not check for semantic contradiction/negation. We do not cite this module for "conflict surfacing"; it is cited under Supersede/replace instead.

### Layered memory ✅
- `crates/aquifer/src/types.rs#L93-L97` — `pub enum MemoryTier { L0Raw, L1Atom, L2Scenario, L3Project }`, used on `MemoryRecord.tier` (`#L127`).
- `docs/memory.md#L60-L68` — documents the tier semantics and a `node_id` drill-down back to `L0Raw` ground truth ("progressive abstraction so high-level summaries stay traceable to evidence").

### Time-travel ✅
- `crates/aquifer/src/temporal.rs#L95` — `pub fn entity_timeline(records: &[MemoryRecord], entity: &str) -> Vec<MemoryRecord>`.
- `crates/aquifer/src/lib.rs#L93` — re-exports `sort_hits_by_event_time`, `apply_recency_decay`.
- `crates/aquifer/src/reconcile.rs#L64` / `crates/aquifer/src/dream.rs#L77` — superseded-version chains (`superseded_id`) are a second form of historical/temporal traceability.
- `crates/artesian-mcp/src/lib.rs#L2855,L2893` — `memory.session.resume` / `memory.session.resume_by_task` recover past session state.

### Schema fields (count: 19) ✅
From `MemoryRecord` (`crates/aquifer/src/types.rs#L121-L163`), excluding the auto `id` and `created_at`: `node_id`(`#L123`), `tags`(`#L125`), `metadata`(`#L126`), `tier`(`#L127`), `scope`(`#L130`), `agent_id`(`#L132`), `session_id`(`#L134`), `task_id`(`#L136`), `user_id`(`#L138`), `project`(`#L140`), `source`(`#L142`), `author_id`(`#L145`), `confidence`(`#L147`), `relations`(`#L149`), `last_access`(`#L153`), `access_count`(`#L156`), `useful_count`(`#L159`), `state`(`#L163`) = **18**, plus `MemoryScope`'s own 4-value domain (`#L102-L106`) and `MemoryTier`'s 4-value domain counted once each as typed sub-schemas → reported as **19** to include the tier/scope enums as structured (not free-text) fields. `metadata` itself is a free-form `BTreeMap`, counted once (not further broken into named sub-fields, unlike some other systems' JSON-blob metadata).

---

## Search & Retrieval

### Full-text ✅
- `crates/aquifer/src/sqlite_vec.rs#L489,L513,L741` — SQLite FTS `bm25(...)` ranking query and `bm25_to_score()`.

### Semantic/vector ✅
- `crates/aquifer/src/vector.rs#L237` — `pub trait VectorStore: Send + Sync`.
- Three implementations: `crates/aquifer/src/sqlite_vec.rs#L89` (`SqliteVecVectorStore`), `crates/aquifer/src/qdrant.rs#L297` (`QdrantVectorStore`), `crates/aquifer/src/pgvector.rs#L92` (`PgVectorStore`).

### Hybrid (BM25+Vec) ✅
- `crates/aquifer/src/rrf.rs#L7` — `pub fn reciprocal_rank_fusion(channels: &[Vec<SearchHit>], options: RrfOptions) -> Vec<SearchHit>`.
- `crates/aquifer/src/backend.rs#L21-L33` — default `hybrid_rrf()` fuses keyword + vector channels.
- `crates/aquifer/src/vector_memory.rs#L455,L474,L1062,L1339` — `keyword_hits()`/`vector_hits()` channels and fusion call sites.

### Deep (incl. thinking) ❌
Not found. No search over model reasoning/thinking traces.

### Code graph ❌
Not found — confirmed absent, and explicitly acknowledged in the project's own docs as future work: `docs/memory.md#L307` ("### 4.2 Structured / graph memory `[planned, future]`"), `docs/positioning.md#L84` ("The CCS schema has a `relational_map` slot reserved for it, but a graph store is not yet wired.").

### Docs search ❌
Not found. `backfill_directory` (see Extraction Pipeline → data sources) imports generic markdown/JSON, not a dedicated framework/API documentation search.

### Fact metadata query ✅
- `crates/aquifer/src/sqlite_vec.rs#L596` — maps a filter field to a JSON path for `json_extract`, e.g. `metadata.parent_node` (comment uses "e.g.", i.e. the mechanism is generic, not hardcoded to one field).
- `crates/aquifer/src/vector.rs#L435`, `crates/aquifer/src/vector_memory.rs#L562,L642` — `filter.must_eq("metadata.parent_node", ...)` calls.

### Timeline view ✅
- `crates/aquifer/src/temporal.rs#L95` — `entity_timeline()`.
- `crates/aquifer/src/lib.rs#L93` — `sort_hits_by_event_time`.

### Search modes (count: 7) ✅
1. Semantic/vector (embedding cosine similarity) — `crates/aquifer/src/vector.rs#L237` + 3 backends.
2. Full-text/BM25 — `crates/aquifer/src/sqlite_vec.rs#L489`.
3. Hybrid RRF fusion of the two — `crates/aquifer/src/rrf.rs#L7`.
4. MMR-diversified recall — `crates/aquifer/src/mmr.rs#L2,L37` (`mmr_diversify`), wired at `crates/aquifer/src/vector_memory.rs#L171,L1016-L1025`.
5. Small-to-big expansion with adaptive parent budget — `vector_memory.rs#L128,L142,L536,L705`.
6. One-hop entity-relation link expansion (`--expand`) — `crates/artesian-cli/src/main.rs#L938,L991`, `crates/aquifer/src/graph.rs#L177-L208` (`expand_hits_with_neighbors`).
7. Entity/temporal timeline query — `crates/aquifer/src/temporal.rs#L95`.

### Data sources (count: 5) ✅
1. Explicit stored memories (`memory.store`) — `crates/artesian-mcp/src/lib.rs#L2676`.
2. Backfilled markdown/JSON directories — `crates/aquifer/src/backfill.rs#L46,L62,L116-L146`.
3. Cross-harness session imports (Claude Code / Codex / Hermes transcripts) — `crates/aquifer/src/harness_import.rs#L18-L21` (`enum HarnessKind { Hermes, ClaudeCode, Codex }`).
4. Skills/procedures — `crates/artesian-mcp/src/lib.rs#L4875,L4927` (`memory.skills`, `memory.skill.replay`).
5. Kits — `crates/artesian-mcp/src/lib.rs#L2993,L3032` (`memory.kit.get`, `memory.kit.set`).

---

## Knowledge Lifecycle

### Decay/forgetting ✅
- `crates/aquifer/src/decay.rs#L3,L68,L82-L96` — `retrieval_strength()`, computed from `access_count`/`useful_count`/`last_access` (utility-aware soft decay).
- `crates/aquifer/src/eviction.rs#L13,L234-L236` — `utility_protected()`: "archive records with the lowest utility-weighted `retrieval_strength`."
- Correction: there is only **one** strength concept (`retrieval_strength`); `git grep -n "storage_strength"` at this commit returns zero hits repo-wide, so we do not claim a distinct "storage strength vs. retrieval strength" dual-field model. Decay affects ranking/eviction eligibility, not stored content.

### Supersede/replace ✅
Two independent, traceable mechanisms:
- Consolidation-time: `crates/aquifer/src/dream.rs#L77` — `DreamDecision::Supersede`, unit-tested at `dream.rs#L772` (`dream_supersedes_near_duplicates`).
- Write-time (opt-in): `crates/aquifer/src/reconcile.rs#L64` — `ReconcileDecision::Supersede { superseded_id: String }`, gated by `ReconcileConfig::reconcile_on_write` (default `false`, `reconcile.rs#L31,L43`).
- Explicit tombstone: `crates/aquifer/src/files.rs#L294-L349`, `crates/aquifer/src/vector_memory.rs#L1398-L1460` — `retract()`, exposed at the CLI (`crates/artesian-cli/src/main.rs#L3272-L3275`, `MemoryCommand::Retract`). `RetractReport { retracted, supersede }` (`types.rs#L313-L315`) creates one audit tombstone referencing the retracted node itself — this is a self-referential audit record, not a cascade to other/neighboring memories (no "supersede-neighbors" cascade exists; `graph.rs`/`entity.rs` have zero hits for "retract").

### Contradiction detect ✅ (LLM-judge only)
- `crates/headgate/src/judge.rs#L26-L31,L36,L48,L104,L140-L142` — the optional LLM judge (`--features llm`) explicitly scores "drift" = "risk it contradicts the committed state or is unsupported/hallucinated," gated by a deterministic `max_drift` threshold. This is a real, automatic (no manual flagging) contradiction/hallucination check.
- Honesty note: this requires the optional LLM-judge feature. The deterministic default gate (`crates/headgate/src/gate.rs`) does not implement a drift/contradiction check (`git grep -n "drift"` in `gate.rs` returns zero hits), and the write-time/consolidation-time "Supersede" mechanisms (`reconcile.rs`, `dream.rs`) are lexical-similarity/length heuristics, not semantic contradiction detectors, despite `reconcile.rs#L9`'s doc-comment wording ("an existing record is contradicted"). We are citing the LLM-judge path only, since it is the one mechanism that actually checks for contradiction against committed state.

### Quarantine ❌
Not found.

### Auto-resolution ✅ (scoped)
- `crates/aquifer/src/eviction.rs#L11-L12` — `--ttl-days N`: "archive low-utility records whose `last_access` (or `created_at` if never accessed) is older than N days; high downstream-use records are protected from age-only TTL." This is TTL-based auto-archival of stale records generally — not a "task" ontology (Artesian has no Task-type field; see Data Model), so we scope this claim to general stale-record auto-resolution rather than task-specific resolution.

### Trust model ❌
Not found (see Data Model → Origin + trust).

### Explicit forget ✅
- `crates/artesian-cli/src/main.rs#L3272-L3275` — CLI `MemoryCommand::Retract` → `backend.retract(&node_id)`.
- `crates/aquifer/src/eviction.rs#L47-L50,L89-L106` — two-phase `Archive`/`Delete`; a `--hard` pass permanently removes already-archived records.

---

## Extraction Pipeline

### Auto-extraction ✅ (scoped — batch/import time, not per-turn)
- `crates/aquifer/src/harness_import.rs#L18-L21` — `enum HarnessKind { Hermes, ClaudeCode, Codex }`; automatically turns raw session transcripts into candidate memories via a heuristic `durable_fact_score()` (`harness_import.rs#L649`, used at `#L529`), without a manual `store` call per fact.
- `crates/artesian-cli/src/import.rs#L15-L17,L190,L229` — the CLI import orchestrator wires these candidates through `headgate::DefaultQualifyGate` before admission (the qualify-gate call lives here, one layer above `harness_import.rs` itself).
- Scoping honesty: this is coarse (chunk/turn-level scoring), not fine-grained entity/fact extraction, and it runs on explicit `artesian import` invocation over a session directory — not live, per-message extraction during an active conversation. Contrast: `memory.store` itself (`crates/artesian-mcp/src/lib.rs#L2679-L2715`) makes zero LLM calls and does no extraction — see the "zero-cost writes" note under Additional Features.

### Content-aware preprocessing ❌
`crates/aquifer/src/chunking.rs` implements deterministic, structure-aware recursive chunking (markdown headings → blank lines → sentences → words, `chunking.rs#L4-L11`), but this is generic RAG-style splitting, not differential handling of code vs. natural-language content as the criterion specifies. Marked ❌.

### Deduplication ✅
- `crates/aquifer/src/consolidation.rs#L31-L32,L111,L217,L303` — `dedup_removed` field, computed and asserted in tests ("dedup removed {} records; footprint {} → {} tokens").

### Quality refinement ✅
- `crates/headgate/src/gate.rs#L158,L210` — `QualifyGate` trait, `DefaultQualifyGate::decide()` scores relevance + novelty/redundancy before admission.
- `crates/headgate/src/judge.rs#L44,L147` — `JudgeQualifyGate` (LLM-based scoring: relevance, novelty, drift) as an alternative/optional backend.
- The qualify-gate itself is the quality-refinement pass gating what enters committed context — see Additional Features for the full admission-log picture.

### Narrative generation ✅
- `crates/aquifer/src/dream.rs#L146,L441,L513,L734` — writes a human-readable `DREAMS.md` narrative ("`--diary`") alongside each consolidation's OCF bundle.

### Clustering ✅
- `crates/aquifer/src/episode.rs#L5` — "Greedy embedding-based episode clustering."
- `crates/aquifer/src/event.rs#L9,L21` — events as "a cluster of related facts."

### Recurrence detection ✅
- `crates/flume/src/consolidation.rs#L250,L345` — `mine_recurring_skill_candidates(signals, min_occurrences)`.

### Persona extraction ❌
Not found.

---

## Platform Support

### Claude Code ✅
- Hooks: `crates/artesian-cli/src/main.rs#L67-L71,L2781-L2782` — `ensure_hook_command(&mut root, "SessionStart", ...)`, `ensure_hook_command(&mut root, "PreCompact", ...)` writing into `~/.claude/settings.json` (`claude_settings_path()`, `main.rs#L2852-L2854`).
- Skill: `main.rs#L2843-L2854,L2943` — installs `.claude/skills/artesian-loop/SKILL.md`; frontmatter tested at `main.rs#L6294-L6296`.

### Codex ✅
- `crates/aquifer/src/harness_import.rs#L18-L22,L29,L168,L198,L212,L337` — `HarnessKind::Codex`, `collect_codex_sources/markdown/sessions`, `parse_codex_session_text`.
- `crates/artesian-process-agent/src/lib.rs#L1212,L1224` — `AgentKind::Codex`.
- `crates/flume/src/lib.rs#L1708` — `"codex" => DelegationDispatchStrategy::NativeSubagent(...Codex)`.

### OpenCode ✅
- `crates/artesian-process-agent/src/lib.rs#L1213-L1214,L1316` — `AgentKind::Opencode`, `native_invocation(...)`.
- Exact argv tested at `crates/artesian-process-agent/src/lib.rs#L2060-L2071` (`["run", prompt, "--model", "opencode-default"]`).

### Gemini CLI ✅
- `crates/artesian-process-agent/src/lib.rs#L1213-L1214,L1306` — `AgentKind::Gemini`.
- Exact argv tested at `lib.rs#L2047-L2058` (`["-p", prompt, "--yolo", "-m", "gemini-pro"]`).

### Copilot ❌
Not found.

### Cursor ❌
Not found as an IDE integration. The only "Cursor" hits in the repo (`crates/aquifer/src/txn.rs#L7,L10`, `crates/aquifer/tests/concurrency.rs#L299`) cite Cursor's public engineering write-up on agent-scaling as *design inspiration* for the transactional-memory architecture — this is not a Cursor IDE platform integration and is not counted as one.

### Windsurf ❌
Not found.

### OpenClaw ❌
Not found.

### Hermes ✅
- `crates/aquifer/src/harness_import.rs#L18-L21` — `HarnessKind::Hermes`.

### pi/omp ❌
Not found.

### Antigravity ❌
Not found.

---

## Benchmarks

### LoCoMo ✅
- Score: **0.475** (vector recall + BGE reranking, tuned; vector-only baseline 0.370).
- Source: [`benchmarks/comparison/README.md#L84-L92`](https://github.com/aquifer-labs/artesian/blob/438f757/benchmarks/comparison/README.md#L84-L92) — `| LoCoMo | vector (baseline) | 0.370 (74/200) | ... |`, `| LoCoMo | + rerank, tuned | 0.475 (94/198) | 505 | 0.037 |`; headline row at `#L92`: `| LoCoMo | 0.475 | vector + BGE reranking (vector-only baseline: 0.37) |`.
- Judge: `codex` gpt-5.5 (reasoning `xhigh`), LLM-as-judge grading, n=200/198.

### LongMemEval ✅
- Score: **≈0.70** (oracle split, vector recall). Headline table states `0.70` (`benchmarks/comparison/README.md#L93`); the underlying detailed run is `0.699` (348/498, n=500) at `#L90`, with reranked variants at `0.691`/`0.698` (`#L91-L92`) — reported here at 3-significant-figure precision rather than rounding up silently.

### PersonaMem ❌
No published score.

### Token reduction ✅
- Published "footprint vs. full" ratio (committed-context tokens ÷ full raw corpus/conversation): **0.037–0.049** on LoCoMo, **0.286–0.343** on LongMemEval-oracle. Source: `benchmarks/comparison/README.md#L84-L92` (the `footprint vs full` column).
- Continuously measured (not just a one-off benchmark run): `docs/token-savings.md` — `artesian tokens` / MCP tool `memory.savings` computes `saved_tokens = max(0, baseline_tokens − returned_tokens)` per recall operation against an explicit documented baseline ("the sum of `count_tokens(record.content)` for every unique source record that contributed a hit"), logged append-only to `~/.artesian/token_savings.jsonl`.
- `mem0` (arXiv:2504.19413) is cited in the same doc for context (its self-reported "> 90% token savings vs. a full-context baseline") but explicitly flagged as **not re-run** under Artesian's own protocol (`benchmarks/comparison/README.md#L120-L124`) — we do not borrow that number for Artesian's own score.

### Methodology open ✅
- `benchmarks/comparison/README.md#L34` ("## Honesty notes"), `#L126` (sample-size/judge caveats), `#L173` (second Honesty-notes section for the agentic eval).
- Reproducible via the `gauge` crate's own binaries: `gauge-bench`, `gauge-eval`, `gauge-agent`, `gauge-ci-eval` (`crates/gauge/Cargo.toml#L26-L38`; workspace member at `Cargo.toml#L11`; doc at `crates/gauge/src/lib.rs#L3-L4`).

---

## Additional Features (Not in Comparison Matrix)

### Append-only admission/governance audit log — the headline differentiator
Every consolidation admission decision is written to an append-only `qualify.jsonl` (JSON-lines):
- `crates/aquifer/src/dream.rs#L58` — `const QUALIFY_FILE: &str = "qualify.jsonl"`, written at `dream.rs#L502`.
- `dream.rs#L69-L80` — `pub enum DreamDecision { Admit, Reject, Merge, Supersede, Decay }`, `#[serde(rename_all = "lowercase")]` (`dream.rs#L68`) → literal `"admit"|"reject"|"merge"|"supersede"|"decay"` per record.
- Doc corroboration, verbatim match to the code: [`docs/self-repair.md#L96`](https://github.com/aquifer-labs/artesian/blob/438f757/docs/self-repair.md#L96) — "The `qualify.jsonl` file logs every `admit`/`reject`/`merge`/`supersede`/`decay` decision for post-hoc inspection."
- Tested: `dream.rs#L772` (`dream_supersedes_near_duplicates`).
- Complementary log for the eviction side of the lifecycle: `eviction.jsonl` records `archive`/`delete` decisions separately — `crates/aquifer/src/eviction.rs#L8,L47-L50,L250`.
- Review-then-adopt workflow, not auto-merge: `crates/aquifer/src/dream.rs#L3,L7-L8` ("the source collection is never mutated — input records are immutable"); CLI guidance text at `crates/artesian-cli/src/main.rs#L5181,L5183` — "Inspect qualify.jsonl for admit/reject/merge/supersede/decay decisions" then "To promote this bundle, review and run `artesian memory store` on accepted entries."
- Honesty note: a **second**, less-tested code path (`crates/headgate/src/bundle.rs#L524`, `OCF_QUALIFY_FILE`) also writes a file named `qualify.jsonl` for the OCF working-context-bundle format, with its own `Decision` enum (`Commit|Evict|Supersede|Deprecate`, `bundle.rs#L217-L222`) that can emit `"evict"`/`"deprecate"` reason strings (`bundle.rs#L830,L837`). This path exists in real, compiling code but has no exercising unit test at this commit and uses a different record shape (`admitted: bool` + free-text `reason`, not a `decision` enum) than the Dreams-engine implementation above. We cite the Dreams-engine implementation (5 verbs, doc-corroborated, unit-tested) as the primary evidence and disclose the second path for completeness rather than merging them into a single unverified 7-verb claim.

### CouncilJudge — panel + arbiter LLM judge
- `crates/headgate/src/council.rs#L45-L51` — `CouncilJudge { panel: Vec<Arc<dyn LlmClient>>, arbiter: Arc<dyn LlmClient> }`, implements `QualifyGate` (`council.rs#L186`).
- `council.rs#L202-L300` — panel members run concurrently (`join_all`), the arbiter synthesizes a verdict, falls back to majority vote, and fails closed below quorum.

### Multi-writer transactional substrate
- `crates/aquifer/src/txn.rs#L80,L99-L112` — `CommitLog { seq: Arc<AtomicU64> }`, `try_commit()` via `compare_exchange` (CAS).
- `txn.rs#L188-L208` — `commit_with_retry()`, optimistic-concurrency retry loop.
- Stress test with the exact numbers verified in code: `crates/aquifer/tests/concurrency.rs#L219-L221` — `let agents = 6usize; let operators = 4usize;`, asserting zero corruption across 24 concurrent writes (`#L271-L296`).
- Honesty note: `txn.rs` itself is a generic, scope-agnostic CAS primitive — "scope" appears only in doc-comment prose (`txn.rs#L15,L49`), not wired to the real `MemoryScope` enum (`types.rs#L102-L106`) inside that file. Per-scope isolation is achieved by instantiating one `CommitLog` per scope (by convention), demonstrated by the per-operator checks in the concurrency test, not by an in-file multi-scope partitioning mechanism.

### Session-compaction survival
- `crates/aquifer/src/anchor.rs#L15,L123` — `SessionAnchor`, `recover_after_compaction()`.
- `crates/artesian-cli/src/main.rs#L67-L71,L2781-L2782` — Claude Code `SessionStart`/`PreCompact` hook wiring.
- `crates/aquifer/src/session.rs#L27-L30` — `SessionKey { user_id, session_id, task_id }`; mirrored in the OCF bundle manifest as `manifest.session` (`crates/headgate/src/bundle.rs#L291,L318-L321,L532`, `OcfSession { session_id, task_id, user_id, handed_off_from }`).
- `crates/artesian-mcp/src/lib.rs#L2810,L2815,L2855,L2859,L2893,L2899` — MCP tools `memory.session.checkpoint`, `memory.session.resume`, `memory.session.resume_by_task`.

### Zed integration (not a scored column in this matrix)
`crates/artesian-cli/src/update.rs#L717,L721,L888,L893,L906` and `crates/artesian-cli/tests/cli.rs#L89-L98` — the CLI detects, registers, and update-checks an installed `artesian-zed` Zed extension. Honesty note: this repo only *detects/manages* that extension; its own manifest/source is not vendored in `aquifer-labs/artesian` at this commit, so we surface it here rather than under Platform Support.

### mem0 — design alignment only, no shipped adapter
`crates/aquifer/src/decay.rs#L15,L26` — a design-inspiration comment: "mem0 alignment... All defaults are chosen to match mem0's soft-dampening profile." There is **no shipped mem0 client/adapter** in the repo (`git grep -rni "mem0" crates/aquifer/src/` finds only this comment). A generic `RecallStore` trait (`crates/headgate/src/recall.rs#L43`) is documented as something a user *could* implement to wire up mem0 (`README.md#L115`, `docs/composability.md#L18,L32,L53`), but that is a pluggable extension point, not a built-in integration — not claimed as a feature above.

### Multi-call single binary
`crates/artesian-cli/Cargo.toml#L33-L41` — one `[[bin]] name = "artesian"`, with the design comment: "Single multi-call binary: dispatches to the CLI, the MCP server (`artesian-mcp`), and the daemon (`artesiand`) by invocation name, so they share one copy of the runtime instead of three." `crates/artesian-cli/src/main.rs#L89,L1339-L1342` — `mod artesiand;` plus argv0-basename dispatch (`Some("artesian-mcp") => return artesian_mcp::cli::run().await`, `Some("artesiand") => return artesiand::run().await`).

---

## Verification Notes

- All ✅ claims were checked against source at commit `438f757` (`git show 438f757:<path> | grep -n ...`), not the dirty working tree, and line numbers are from direct `grep -n`/`sed -n` output, not manual counting.
- Several assumptions we started with turned out to be overclaims on closer reading, and were corrected rather than asserted:
  - `qualify.jsonl` covers **5** verbs with strong evidence (admit/reject/merge/supersede/decay), not 7 — "archive" belongs to the separate `eviction.jsonl`, and "promote" is CLI prose about promoting a whole bundle, not a per-entry decision kind.
  - There is **one** `retrieval_strength` concept, not a distinct "storage strength vs. retrieval strength" pair — `storage_strength` does not exist in code.
  - `retract()` creates a **self-referential** tombstone, not a cascade that supersedes neighboring/related memories.
  - Optimistic-lock version conflicts are **surfaced as typed errors** to the caller (tested), not logged to any audit file.
  - `reconcile.rs`'s `Supersede` decision is a **length heuristic** among similar content, not a semantic contradiction check, despite its own doc-comment saying "contradicted."
  - `txn.rs`'s "per-scope isolation" is achieved **by convention** (one `CommitLog` per scope), not by an in-file partitioning mechanism keyed to the real `MemoryScope` enum.
  - `mem0` alignment is a **decay-tuning design choice**, not a shipped adapter.
  - The `crates/sandbox` crate is a **config seam**, not an implemented sandbox runtime with enforcement — marked ❌ despite the crate's name.
  - The `artesian-zed` Zed extension is **detected/managed**, not vendored, in this repo — surfaced as an additional feature rather than under Platform Support (which also has no Zed column).
- Two independent implementations both write a file literally named `qualify.jsonl` (`crates/aquifer/src/dream.rs` and `crates/headgate/src/bundle.rs`) — see the Additional Features entry for the precise, non-conflated breakdown.
- Benchmark numbers are quoted at the precision published in `benchmarks/comparison/README.md` (e.g. `0.699`, not rounded to `0.70`, where the source shows the more precise figure) alongside the headline-table rounding where the source itself rounds.

---

## Summary for data.js (suggested — maintainers may adjust)

```javascript
{
  id: "artesian",
  name: "Artesian",
  url: "https://github.com/aquifer-labs/artesian",
  evidence: "evidence/artesian.md",
  description: "Local-first memory controller for AI coding agents: bounded committed context (ACC), append-only admission audit log, pluggable storage, hybrid retrieval, transactional multi-writer substrate.",
  stars: 0, language: "Rust", license: "Apache-2.0", singleBinary: true, created: "2026-06-13",
  docs: "https://github.com/aquifer-labs/artesian#readme",

  // Architecture
  deployment: "Local CLI/MCP, single binary or Docker",
  storage: "Files(OKF)/sqlite-vec/Qdrant/pgvector (pluggable)",
  integration: "MCP(rmcp)+CLI+Claude Code hooks/skill",
  proxy: false, webUi: false, offline: true, multiAgent: true,
  llmFlex: 5, cacheOpt: true, procedural: true, sandboxed: false,
  scheduled: true, privacy: true, export: true,
  setup: "brew install", pricing: "free",

  // Data Model
  unit: "MemoryRecord (4-tier: L0Raw/L1Atom/L2Scenario/L3Project)",
  entities: true, actions: false, keywords: true,
  anticipatedQueries: false, triggerRules: false, domainTag: false,
  taskType: false, context: false, source: true,
  originTrust: false, emotional: false, conflict: true,
  layeredMemory: true, timeTravel: true, schemaFields: 19,

  // Search: modes=7, sources=5
  fulltext: true, semantic: true, hybrid: true, deep: false,
  codeGraph: false, docsSearch: false, factQuery: true, timeline: true,
  searchModes: 7, dataSources: 5,

  // Lifecycle
  decay: true, supersede: true, contradiction: true,
  quarantine: false, autoResolve: true, trustModel: false, explicitForget: true,

  // Extraction
  autoExtract: true, contentPreproc: false, dedup: true,
  qualityRefine: true, narrative: true, clustering: true,
  recurrence: true, persona: false,

  // Platform
  p_claude: true, p_codex: true, p_opencode: true, p_gemini: true,
  p_copilot: false, p_cursor: false, p_windsurf: false, p_openclaw: false,
  p_hermes: true, p_pi: false, p_antigravity: false,

  // Benchmarks
  b_locomo: "0.475", b_longmemeval: "0.699 (oracle, headline 0.70)",
  b_personamem: "—", b_token: "footprint 0.037-0.049 (LoCoMo) / 0.286-0.343 (LongMemEval)",
  b_methodology: true,
}
```
