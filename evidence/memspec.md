# memspec — Evidence

> Every ✅ claim backed by public source code or documentation.
> Audit date: 2026-07-27. Source: GitHub `siimvene/memspec` main branch (v0.9.0).

**Repo:** `siimvene/memspec`
**Stars:** 3  
**npm:** `memspec` (latest `v0.9.0` on npm registry, published 2026-07-27)
**Language:** TypeScript
**License:** MIT
**Created:** 2026-04
**Description:** Git-backed project memory for AI coding agents, with code-anchored verification and drift detection — canonical markdown files, typed supersede chains, four-tier witness provenance.

---

## System Metadata

| Field | Value |
|-------|-------|
| **Deployment** | `Local CLI + MCP + Library` |
| **Storage** | `Markdown files (canonical) + SQLite FTS5 (derived index) + optional embeddings` |
| **Integration** | `MCP + CLI + Claude Code hooks` |
| **Single binary?** | `no` (Node package, ships three bins) |
| **Setup** | `npm install -g memspec` |
| **Pricing** | `free / open source (MIT)` |
| **Storage unit** | `Memory record (fact / decision / procedure / observation)` |

---

## Architecture

### Proxy ❌

### Web/TUI ❌
> No browser or TUI ships with memspec. `memspec status` prints a plain-text health readout only.

### Offline ✅
- Source: [`README.md#L32`](https://github.com/siimvene/memspec/blob/main/README.md#L32) — "Zero infrastructure. `npm install -g memspec` + `memspec init`. No accounts, no API keys, no hosted services."
- Source: [`README.md#L115-L118`](https://github.com/siimvene/memspec/blob/main/README.md#L115-L118) — "FTS5 (default): SQLite full-text + BM25. Zero setup beyond `better-sqlite3`." Local SQLite; no network calls required at read/write time.
- Source: [`src/lib/fts.ts#L38-L48`](https://github.com/siimvene/memspec/blob/main/src/lib/fts.ts#L38-L48) — FTS5 index runs in-process against a local SQLite file or `:memory:`.

### Multi-agent ❌
> Multiple agents can read/write the same store, but memspec has no agent directory, cross-agent messaging, or orchestration surface. SPEC §7 covers concurrent file I/O only.

### LLM providers (count: 2) ✅
- Source: [`src/lib/embeddings.ts#L20-L27`](https://github.com/siimvene/memspec/blob/main/src/lib/embeddings.ts#L20-L27) — `ApiProviderConfig` supports `'openai' | 'ollama'` for optional hybrid-search reranking.
- Source: [`README.md#L28`](https://github.com/siimvene/memspec/blob/main/README.md#L28) — "SQLite FTS5 + BM25 by default; optional dense embeddings rerank via OpenAI-compatible endpoints or Ollama."

### Cache optimization ✅
- Source: [`src/lib/fts.ts#L78-L89`](https://github.com/siimvene/memspec/blob/main/src/lib/fts.ts#L78-L89) — `FtsIndex.openOrBuild` reuses an on-disk FTS cache if mtime-fresh; only rebuilds when a source file changed.

### Procedural memory ❌
> `procedure` is a memory type, but memspec never executes stored bodies — they're prose retrieved for the agent to read.

### Sandboxed execution ❌

### Scheduled/autonomous ✅
- Source: [`README.md#L252-L258`](https://github.com/siimvene/memspec/blob/main/README.md#L252-L258) — `memspec-dream` weekly cron example: `0 22 * * 0  cd /path/to/project && MEMSPEC_DREAM_AUTOCOMMIT=1 memspec-dream`.
- Source: [`scripts/dream.sh#L1-L36`](https://github.com/siimvene/memspec/blob/main/scripts/dream.sh#L1-L36) — Periodic reflection script; designed to run headlessly.

### Privacy/encrypt ✅
- Source: [`README.md#L5`](https://github.com/siimvene/memspec/blob/main/README.md#L5) — "No backend service. No hosted memory API. No vendor lock-in." Data lives entirely on disk under `.memspec/`.
- Source: [`README.md#L135`](https://github.com/siimvene/memspec/blob/main/README.md#L135) — Trust profiles: "Secrets: never stored. Anywhere. Ever."
- Source: [`package.json#L48-L56`](https://github.com/siimvene/memspec/blob/main/package.json#L48-L56) — Dependencies: MCP SDK, SQLite driver, CLI parser, YAML, ULID, Zod — no telemetry or analytics.

### Data export ✅
- Source: [`src/mcp.ts#L450-L479`](https://github.com/siimvene/memspec/blob/main/src/mcp.ts#L450-L479) — `memspec_export` tool: JSONL / GraphML / DOT of the memory graph.
- Source: [`README.md#L232`](https://github.com/siimvene/memspec/blob/main/README.md#L232) — CLI mirror: `memspec export --format <jsonl|graphml|dot>`.

---

## Data Model

### Entities ❌
> Anchors point to source files, but memspec has no separate entity extraction (people / packages / systems as structured rows). Anchors are file-references only.

### Actions ❌
> `procedure` bodies are prose; no structured field for commands, arguments, or tool calls.

### Keywords/tags ✅
- Source: [`src/lib/schema.ts#L48-L49`](https://github.com/siimvene/memspec/blob/main/src/lib/schema.ts#L48-L49) — `tags: z.array(z.string()).default([]).describe('Free-form tag list for filtering and search.')`.
- Source: [`SCHEMA.md#L62-L67`](https://github.com/siimvene/memspec/blob/main/SCHEMA.md#L62-L67) — Tags documented as first-class frontmatter field.

### Anticipated queries ❌

### Trigger rules ❌
> `check_by` is passive stale-flagging on read, not conditional activation. No "activate when file X opens" primitive.

### Domain tag ❌
> Tags are free-form (see above). No enforced domain taxonomy (code / marketing / legal / finance / general).

### Task type ❌
> memspec has memory *types* (fact / decision / procedure / observation), not task-status types (task / idea / blocked / stale). Different taxonomy.

### Context (why) ✅
- Source: [`SPEC.md#L366-L370`](https://github.com/siimvene/memspec/blob/main/SPEC.md#L366-L370) — Body template includes explicit `## Context` ("why this matters, what prompted it") and `## Alternatives` sections alongside content.
- Source: [`SPEC.md#L204-L227`](https://github.com/siimvene/memspec/blob/main/SPEC.md#L204-L227) — `supersede_reason` is a durable frontmatter field persisted on every superseded and replacement record: the *why* of a correction.

### Source attribution ✅
- Source: [`src/lib/schema.ts#L44-L47`](https://github.com/siimvene/memspec/blob/main/src/lib/schema.ts#L44-L47) — `source` (required, `"unknown"` rejected) and `source_kind: operator | agent | import` (three explicit tiers).
- Source: [`SPEC.md#L381`](https://github.com/siimvene/memspec/blob/main/SPEC.md#L381) — `source_kind` inference rule: `siim|human:*|user → operator`; import names → `import`; else `agent`.

### Origin + trust ✅
- Source: [`SPEC.md#L230-L232`](https://github.com/siimvene/memspec/blob/main/SPEC.md#L230-L232) — §4.2.1 Operator Record Protection: operator-sourced records MUST NOT be superseded without an explicit `override_operator` flag, which is logged into the persisted reason.
- Source: [`src/mcp.ts#L295`](https://github.com/siimvene/memspec/blob/main/src/mcp.ts#L295) — `override_operator` required at the MCP surface to supersede operator-tier records.
- Source: [`SPEC.md#L318-L324`](https://github.com/siimvene/memspec/blob/main/SPEC.md#L318-L324) — Operator-tier records live in a separate filesystem path (`memory/operator/{type}s/`) so trust tier is enforced at storage level, not just metadata.

### Emotional ❌

### Conflict surfacing ✅
- Source: [`src/lib/schema.ts#L70-L71`](https://github.com/siimvene/memspec/blob/main/src/lib/schema.ts#L70-L71) — `conflicts_with` explicit conflict-edge array on every record.
- Source: [`src/mcp.ts#L38-L39`](https://github.com/siimvene/memspec/blob/main/src/mcp.ts#L38-L39) — Search results carry `[CONFLICTS WITH ...]` markers inline.
- Source: [`SPEC.md#L262-L263`](https://github.com/siimvene/memspec/blob/main/SPEC.md#L262-L263) — Retrieval response MUST include declared `conflicts_with` edges "including edges to non-returned claims, with their titles inline."

### Layered memory ✅
- Source: [`README.md#L24`](https://github.com/siimvene/memspec/blob/main/README.md#L24) — "Layered stores (v0.6+). A project `.memspec/` and a global `~/.memspec/` merge at retrieval time — project records take priority, global merges as a lower layer."
- Source: [`SPEC.md#L612-L672`](https://github.com/siimvene/memspec/blob/main/SPEC.md#L612-L672) — §12 Store Composition: named layers with priority, writable flag, precedence rules for search and write.
- Source: [`src/lib/composite-store.ts`](https://github.com/siimvene/memspec/blob/main/src/lib/composite-store.ts) — `CompositeStore.forCwd(cwd)` implements layered retrieval.
- Source: [`README.md#L171-L197`](https://github.com/siimvene/memspec/blob/main/README.md#L171-L197) — v0.9 multi-store: `.memspec.yaml` pointer file binds a store-less repo to explicit layers; `claims:` route ingestion by owned working directories, unclaimed content held local ([`src/lib/registry.ts`](https://github.com/siimvene/memspec/blob/main/src/lib/registry.ts)).

### Time-travel ✅
- Source: [`src/lib/schema.ts#L82-L85`](https://github.com/siimvene/memspec/blob/main/src/lib/schema.ts#L82-L85) — Optional `valid_from` / `valid_to` ISO8601 fields on every record: world-state truth window, orthogonal to `check_by`.
- Source: [`src/mcp.ts#L70`](https://github.com/siimvene/memspec/blob/main/src/mcp.ts#L70) — `as_of` search parameter drops records whose validity window excludes the given timestamp.
- Source: [`src/mcp.ts#L71`](https://github.com/siimvene/memspec/blob/main/src/mcp.ts#L71) — `include_superseded: true` on search lets link-following reach superseded predecessors via the supersede chain (v0.6+).
- Source: [`CHANGELOG.md#L166-L203`](https://github.com/siimvene/memspec/blob/main/CHANGELOG.md#L166-L203) — v0.5.0 "Temporal validity intervals" release note.

### Schema fields (count: 20) ✅
- Source: [`src/lib/schema.ts#L31-L91`](https://github.com/siimvene/memspec/blob/main/src/lib/schema.ts#L31-L91) — Zod schema defines 20 structured frontmatter fields excluding auto identifiers/timestamps and derived `stale`: `kind`, `type`, `state`, `source`, `source_kind`, `tags`, `check_by`, `verified_with`, `pinned`, `anchors`, `supersedes`, `superseded_by`, `supersede_reason`, `conflicts_with`, `refines`, `supports`, `depends_on`, `expires`, `valid_from`, `valid_to`, plus the `ext` bag.
- Source: [`SCHEMA.md`](https://github.com/siimvene/memspec/blob/main/SCHEMA.md) — Full generated field reference.

---

## Search & Retrieval

### Full-text ✅
- Source: [`src/lib/fts.ts#L60-L70`](https://github.com/siimvene/memspec/blob/main/src/lib/fts.ts#L60-L70) — SQLite FTS5 virtual table with `porter unicode61` tokenizer.
- Source: [`src/lib/fts.ts#L158-L165`](https://github.com/siimvene/memspec/blob/main/src/lib/fts.ts#L158-L165) — BM25 ranking with weighted title(10) / tags(5) / body(1).

### Semantic/vector ✅
- Source: [`src/lib/embeddings.ts#L8-L13`](https://github.com/siimvene/memspec/blob/main/src/lib/embeddings.ts#L8-L13) — `EmbeddingProvider` interface for hybrid re-ranking.
- Source: [`src/lib/embeddings.ts#L89-L103`](https://github.com/siimvene/memspec/blob/main/src/lib/embeddings.ts#L89-L103) — `cosineSimilarity` for vector re-rank against BM25 candidates.
- Source: [`README.md#L115-L118`](https://github.com/siimvene/memspec/blob/main/README.md#L115-L118) — CLI init flag `--search-engine hybrid` opts into embeddings.

### Hybrid (BM25+Vec) ✅
- Source: [`README.md#L28`](https://github.com/siimvene/memspec/blob/main/README.md#L28) — "Hybrid search. SQLite FTS5 + BM25 by default; optional dense embeddings rerank via OpenAI-compatible endpoints or Ollama."
- Source: [`README.md#L114-L119`](https://github.com/siimvene/memspec/blob/main/README.md#L114-L119) — Two engines picked at `memspec init`: FTS5 (default) or Hybrid.
- Source: [`src/cli.ts#L37`](https://github.com/siimvene/memspec/blob/main/src/cli.ts#L37) — `--search-engine <engine>` init flag: `fts5 | hybrid`.

### Deep (incl. thinking) ❌

### Code graph ❌
> No Tree-sitter / AST indexing. Anchors are file-blob-SHA references, not code structure.

### Docs search ❌

### Fact metadata query ✅
- Source: [`src/mcp.ts#L63`](https://github.com/siimvene/memspec/blob/main/src/mcp.ts#L63) — `memspec_search` accepts a `type` filter (`fact | decision | procedure`).
- Source: [`src/mcp.ts#L405-L421`](https://github.com/siimvene/memspec/blob/main/src/mcp.ts#L405-L421) — `memspec_status` returns structured metadata queries: counts by type, state, witness, plus stale flags, drifted anchors, conflicts, and sweep candidates.

### Timeline view ✅
- Source: [`src/mcp.ts#L70`](https://github.com/siimvene/memspec/blob/main/src/mcp.ts#L70) — `as_of` ISO8601 filter on search: temporal state query.
- Source: [`SPEC.md#L254-L255`](https://github.com/siimvene/memspec/blob/main/SPEC.md#L254-L255) — `as_of` drops records whose `valid_from`/`valid_to` window excludes the given instant.

### Search modes (count: 3) ✅
- Source: [`src/mcp.ts#L58-L102`](https://github.com/siimvene/memspec/blob/main/src/mcp.ts#L58-L102) — `memspec_search` MCP tool (BM25 + optional hybrid).
- Source: [`src/mcp.ts#L104-L159`](https://github.com/siimvene/memspec/blob/main/src/mcp.ts#L104-L159) — `memspec_get` id-lookup with lineage chain.
- Source: [`src/mcp.ts#L379-L403`](https://github.com/siimvene/memspec/blob/main/src/mcp.ts#L379-L403) — `memspec_reconcile` retrieves anchored claims by drift-status.

### Data sources (count: 4) ✅
- Source: [`SPEC.md#L104-L113`](https://github.com/siimvene/memspec/blob/main/SPEC.md#L104-L113) — Four record kinds indexed in the same store: `fact`, `decision`, `procedure`, `observation`.
- Source: [`src/lib/fts.ts#L94-L111`](https://github.com/siimvene/memspec/blob/main/src/lib/fts.ts#L94-L111) — FTS index populates all four record types uniformly.

---

## Knowledge Lifecycle

### Decay/forgetting ✅
- Source: [`src/lib/store.ts#L17-L25`](https://github.com/siimvene/memspec/blob/main/src/lib/store.ts#L17-L25) — `withLazyStale` auto-flags records past `check_by` as `stale: true` at read time.
- Source: [`src/lib/decay.ts#L35-L80`](https://github.com/siimvene/memspec/blob/main/src/lib/decay.ts#L35-L80) — `findDecayCandidates` computes per-type TTL defaults and surfaces expired records.
- Source: [`SPEC.md#L175-L185`](https://github.com/siimvene/memspec/blob/main/SPEC.md#L175-L185) — §3.3 Decay defaults: `fact 90d`, `decision 180d`, `procedure 90d`, observation `7d`.

### Supersede/replace ✅
- Source: [`src/mcp.ts#L286-L299`](https://github.com/siimvene/memspec/blob/main/src/mcp.ts#L286-L299) — `memspec_supersede`: body → replacement, empty → retraction, `merge_from` → N→1 atomic merge. Reason is persisted on every record involved.
- Source: [`SPEC.md#L204-L227`](https://github.com/siimvene/memspec/blob/main/SPEC.md#L204-L227) — §4 Self-Correction Protocol: `supersedes`/`superseded_by` chain preserves lineage; reason durable on both records.

### Contradiction detection ✅
- Source: [`src/commands/remember.ts#L185-L207`](https://github.com/siimvene/memspec/blob/main/src/commands/remember.ts#L185-L207) — Write-path neighbour walk: mid-band similarity auto-attaches a suggested `conflicts_with` edge to the closest candidate.
- Source: [`SPEC.md#L51`](https://github.com/siimvene/memspec/blob/main/SPEC.md#L51) — v0.4 "Write-path neighbour-walk" surfaces contradictions at write time.
- Source: [`src/lib/inference.ts`](https://github.com/siimvene/memspec/blob/main/src/lib/inference.ts) — Shared conflict-inference rule used by both read (search) and write (remember).

### Quarantine ❌
> `superseded` and `retired` states exist, but there's no session-scoped exclude-from-retrieval concept.

### Auto-resolution ❌
> The dream loop (v0.7) surfaces stale/supersede candidates, but every proposal is human-reviewed — nothing auto-applies. Output at `<store>/dream/YYYY-MM-DD.md` is review material only. See [`scripts/dream.sh#L12-L13`](https://github.com/siimvene/memspec/blob/main/scripts/dream.sh#L12-L13).

### Trust model ✅
- Source: [`SPEC.md#L187-L200`](https://github.com/siimvene/memspec/blob/main/SPEC.md#L187-L200) — §3.4 Witness Class: four-tier `anchor > operator > evidence > assertion` hierarchy explicitly ranked by strength.
- Source: [`src/lib/schema.ts#L58-L59`](https://github.com/siimvene/memspec/blob/main/src/lib/schema.ts#L58-L59) — `verified_with` enum enforces witness tier; "in descending strength: anchor > operator > evidence > assertion."
- Source: [`context.jsonld#L150-L173`](https://github.com/siimvene/memspec/blob/main/context.jsonld#L150-L173) — SKOS mapping of the four witness classes with definitions.

### Explicit forget ✅
- Source: [`README.md#L231`](https://github.com/siimvene/memspec/blob/main/README.md#L231) — `memspec sweep` — interactive per-item retirement, "the only path that physically removes items."
- Source: [`SPEC.md#L185`](https://github.com/siimvene/memspec/blob/main/SPEC.md#L185) — "Physical retirement is `memspec sweep` — interactive, one prompt per candidate, CLI-only by design."
- Source: [`src/commands/sweep.ts`](https://github.com/siimvene/memspec/blob/main/src/commands/sweep.ts) — Implementation.

---

## Extraction Pipeline

### Auto-extraction ✅
- Source: [`README.md#L26`](https://github.com/siimvene/memspec/blob/main/README.md#L26) — "Transcript ingestion (v0.9+). `normalize` → `distill` → `reduce` turns raw harness session logs (Claude Code, Codex) into weekly experience digests" — no manual save calls in the pipeline.
- Source: [`src/commands/normalize.ts`](https://github.com/siimvene/memspec/blob/main/src/commands/normalize.ts) — harness session logs → structured trajectory records (deterministic, watermark-driven, per-harness adapters).
- Source: [`src/commands/distill.ts#L111-L165`](https://github.com/siimvene/memspec/blob/main/src/commands/distill.ts#L111-L165) — automatic per-session LLM distillation into structured digests (what happened / decisions / fixes / discoveries).
> Scope note: sessions are auto-extracted into structured *digests*; promotion into memory records stays proposal-gated (the dream pass emits ready-to-run `remember` proposals under `UNRECORDED WORK`, human-reviewed).

### Content-aware preprocessing ✅
- Source: [`src/commands/normalize.ts#L47-L50`](https://github.com/siimvene/memspec/blob/main/src/commands/normalize.ts#L47-L50) — type-differentiated truncation budgets at ingest: tool input 500 / tool output 1500 / reasoning 2000 / natural text 10000 chars.
- Source: [`src/commands/distill.ts#L46`](https://github.com/siimvene/memspec/blob/main/src/commands/distill.ts) — prompt budget (~400k chars) keeps head+tail of oversized sessions and elides the middle; secret-shaped strings redacted before extraction.

### Deduplication ✅
- Source: [`src/commands/remember.ts#L170-L179`](https://github.com/siimvene/memspec/blob/main/src/commands/remember.ts#L170-L179) — `remember` refuses near-duplicate writes when an active same-type record with the same normalised title exists; points at `memspec supersede`.
- Source: [`README.md#L27`](https://github.com/siimvene/memspec/blob/main/README.md#L27) — "Dedup-aware writes. `remember` refuses near-duplicate claims and points at the existing record, so memory accretes corrections via `supersede` instead of silent duplicates."
- Source: [`src/mcp.ts#L294`](https://github.com/siimvene/memspec/blob/main/src/mcp.ts#L294) — `merge_from` on supersede collapses N duplicates into one survivor atomically.

### Quality refinement ❌
> No LLM-based post-extraction quality pass. The dream loop (v0.7) is a human-reviewed proposal surface, not an automated quality filter.

### Narrative generation ✅
- Source: [`src/commands/distill.ts#L158-L162`](https://github.com/siimvene/memspec/blob/main/src/commands/distill.ts#L158-L162) — per-session digest with fixed narrative sections: WHAT HAPPENED / DECISIONS / PROBLEMS-FIXES / DISCOVERED / UNRESOLVED.
- Source: [`README.md#L264-L279`](https://github.com/siimvene/memspec/blob/main/README.md#L264-L279) — `reduce` merges session digests into a committed weekly experience digest (handover narrative per machine).

### Clustering ❌

### Recurrence detection ❌

### Persona extraction ❌
> No user-trait extraction pipeline. memspec is agent-authored, explicit-write-only.

---

## Platform Support

### Claude Code ✅
- Source: [`README.md#L29`](https://github.com/siimvene/memspec/blob/main/README.md#L29) — "MCP server. Eleven tools, first-class integration with Claude Code, Cursor, Codex."
- Source: [`README.md#L146`](https://github.com/siimvene/memspec/blob/main/README.md#L146) — `memspec init` auto-creates `.mcp.json` for host tool discovery (Claude Code, Cursor).
- Source: [`README.md#L235-L242`](https://github.com/siimvene/memspec/blob/main/README.md#L235-L242) — Two Claude Code hooks installed at `~/.claude/hooks/`: `memspec-session-start.js` and `memspec-consolidate.js`.
- Source: [`hooks/memspec-session-start.js`](https://github.com/siimvene/memspec/blob/main/hooks/memspec-session-start.js) — Session-start hook (emits Claude Code `SessionStart` `hookEventName`).

### Codex ✅
- Source: [`README.md#L29`](https://github.com/siimvene/memspec/blob/main/README.md#L29) — "MCP server. Eleven tools, first-class integration with Claude Code, Cursor, Codex."

### OpenCode ❌
> Not named in README/SPEC.

### Gemini CLI ❌

### Copilot ❌

### Cursor ✅
- Source: [`README.md#L29`](https://github.com/siimvene/memspec/blob/main/README.md#L29) — "first-class integration with Claude Code, Cursor, Codex."
- Source: [`README.md#L146`](https://github.com/siimvene/memspec/blob/main/README.md#L146) — Auto-created `.mcp.json` for host tool discovery names Cursor explicitly.

### Windsurf ❌

### OpenClaw ❌
> memspec ships an OpenClaw *import* path (`src/lib/import-openclaw.ts`), but that's brownfield ingest — not a documented MCP/hook integration on OpenClaw itself.

### Hermes ❌

### pi/omp ❌

### Antigravity ❌

---

## Benchmarks

### LoCoMo ✅
- Score: Recall@5 / Recall@10 / MRR = 0.700 / 0.700 / 0.675 on cat-2 Temporal slice (n=20, seed=42; retrieval-only protocol, no LLM in the loop).
- Source: [`BENCHMARK.md`](https://github.com/siimvene/memspec/blob/main/BENCHMARK.md) — v0.9.0 rerun 2026-07-27; dataset `snap-research/locomo` `locomo10.json` sha256-pinned; identical scores to the v0.5-era multi-condition runs (full analysis at git tag `v0.6.3`).

### LongMemEval ✅
- Score: Recall@5 / Recall@10 / MRR = 1.000 on Knowledge-Update slice (n=20, seed=42; v0.9.0 rerun 2026-07-27); saturated ceiling — dataset does not differentiate strategies.
- Source: [`BENCHMARK.md`](https://github.com/siimvene/memspec/blob/main/BENCHMARK.md) — methodology, dataset sha256, and rerun instructions; restored to main with the v0.9.0 results.
- Source: [`CHANGELOG.md#L197-L220`](https://github.com/siimvene/memspec/blob/main/CHANGELOG.md#L197-L220) — v0.5.0 release notes: `BENCHMARK.md` + `scripts/run-bench.mjs` "homegrown retrieval-only eval harness running against the public LongMemEval-S dataset. Recall@5, Recall@10, MRR, plus latency p50/p99."
- Note: Honest finding in the changelog — retrieval saturates because ground-truth tags are lexically distinctive; harness commits methodology + baseline for future regressions.

### PersonaMem ❌
- Score: `—`

### Token reduction ❌
- Score: `—`
> memspec does not publish a headline token-reduction number.

### Methodology open ✅
- Source: [`CHANGELOG.md#L197-L220`](https://github.com/siimvene/memspec/blob/main/CHANGELOG.md#L197-L220) — Harness committed to repo (`scripts/run-bench.mjs`), documented in `BENCHMARK.md`; four-condition comparison run at v0.5 release. Methodology reproducible; not paper-comparable (different protocol, smaller sample).
- Source: [`CHANGELOG.md#L30`](https://github.com/siimvene/memspec/blob/main/CHANGELOG.md#L30) — v0.7 carry-forward note: v0.5 baselines hold for v0.6 / v0.7 because none of those releases touch the retrieval ranking path.

---
