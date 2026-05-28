# Memvid — Evidence

> Audited: 2026-05-28. Sources: GitHub README, MV2_SPEC.md, CLAUDE.md, Cargo.toml, benches/, docs.memvid.com

---

## Vital Signs

### singleBinary ❌ CORRECTION: should be FALSE
- **Cargo.toml:1-2** — `[package] name = "memvid-core"` — this is a library crate, no `[[bin]]` targets
- **CLAUDE.md:7** — "Memvid is a Rust library" — explicitly states it's a library
- **README** — CLI is `npm install -g memvid-cli` (requires Node.js runtime), Python SDK is `pip install memvid-sdk` (requires Python)
- **Verdict:** Not a single binary. Requires Rust toolchain to build (library) or Node/Python runtime for SDKs. Currently marked `true` in comparison.md — **this is incorrect**.

---

## Data Model

### keywords ✅ VERIFIED
- **MV2_SPEC.md Frame Structure** — `tags: Map<String, String> — User-defined key-value pairs`
- **README Quick Start** — `.tag("project", "alpha")` API for adding tags
- **Verdict:** Confirmed. User-defined key-value tag system on frames.

### entities ❌ CORRECTION: should be TRUE
- **docs.memvid.com** — "Memory Cards (Entity Extraction): Extract structured facts and query them instantly"
- **docs.memvid.com** — `mem.state("Alice")` returns `{ employer: 'Anthropic', role: 'Senior Engineer' }` — SPO triplet extraction
- **docs.memvid.com** — "O(1) Entity Lookups via Memory Cards (SPO triplets)"
- **docs.memvid.com** — `mem.enrich(path, --engine rules)` to extract facts from documents
- **Verdict:** Entity extraction via Memory Cards / SPO triplets exists. Currently marked `false` in comparison.md — **this is incorrect**.

### layeredMemory ✅ VERIFIED (temporal layering)
- **MV2_SPEC.md** — Smart Frames are organized as append-only immutable sequence in Data Segments
- **MV2_SPEC.md** — Time Index segment for chronological ordering, frame-level timestamps
- **README** — "append-only, ultra-efficient sequence of Smart Frames" — temporal/organizational layering
- **Verdict:** Temporal/sequential layering (analogous to Graphiti's temporal edges). File format has structural layers (Header→WAL→Segments→Indices→TOC) but the "layering" refers to frame-based chronological organization.

### timeTravel ✅ VERIFIED
- **MV2_SPEC.md** — "Time Index enables chronological queries and time-travel"
- **README** — "Time-Travel Debugging: Rewind, replay, or branch any memory state"
- **SearchRequest struct** (benches/search_precision_benchmark.rs) — `as_of_frame: Option<u64>` and `as_of_ts: Option<u64>` parameters for point-in-time queries
- **CLAUDE.md** — `mem.timeline(TimelineQuery::default())` API
- **docs.memvid.com** — Session recording and replay: `memvid session start/replay`
- **Verdict:** Confirmed. Point-in-time queries, timeline inspection, session replay.

### schemaFields: 8 → MINOR CORRECTION: 9
- **MV2_SPEC.md Frame Structure** enumerates these fields:
  1. `frame_id` (u64)
  2. `uri` (String)
  3. `title` (String?)
  4. `created_at` (u64)
  5. `encoding` (u8)
  6. `payload` (bytes)
  7. `payload_checksum` ([u8; 32])
  8. `tags` (Map<String, String>)
  9. `status` (u8)
- **Verdict:** 9 schema fields, not 8. Minor correction.

---

## Search & Retrieval

### fulltext ✅ VERIFIED
- **MV2_SPEC.md Lex Index** — Tantivy index segment, BM25 ranking, phrase queries, boolean operators, date range filters
- **README** — `lex` feature: "Full-text search with BM25 ranking (Tantivy)"

### semantic ✅ VERIFIED
- **MV2_SPEC.md Vec Index** — HNSW index segment, 384 dimensions (BGE-small), cosine similarity
- **README** — `vec` feature: "Vector similarity search (HNSW + local text embeddings via ONNX)"
- **README** — `api_embed` feature: OpenAI cloud embeddings (text-embedding-3-small/large, ada-002)

### hybrid ❌ CORRECTION: should be TRUE
- **docs.memvid.com** — "Hybrid Search: Combines BM25 lexical search with vector similarity. Best of both worlds."
- **docs.memvid.com** — CLI `memvid find --mode lex|sem` and default (no `--mode`) = hybrid: "combines both - default"
- **docs.memvid.com** comparison table — "Memvid | Hybrid search: BM25 + vectors"
- **Verdict:** Hybrid search (BM25 + vector) exists via CLI default mode. Currently marked `false` in comparison.md — **this is incorrect**.

### timeline ✅ VERIFIED
- Same evidence as timeTravel above: Time Index, timeline queries, session replay, `as_of_frame`/`as_of_ts` parameters.

---

## Benchmarks

### b_locomo: "+35% SOTA" ⚠️ PARTIALLY VERIFIED — relative claim, no absolute score
- **README Benchmark Highlights** — "+35% SOTA on LoCoMo, best-in-class long-horizon conversational recall & reasoning"
- **README Benchmark Highlights** — "+76% multi-hop, +56% temporal vs. the industry average"
- **README Benchmark Highlights** — "Fully reproducible benchmarks: LoCoMo (10 × ~26K-token conversations), open-source eval, LLM-as-Judge"
- **No absolute LoCoMo score found** in README, docs site, or repo. Compare with ByteRover (96.1), Mem0 (91.6), Memori (81.95) which publish concrete numbers.
- **benches/ directory** — Contains performance microbenchmarks (search_precision_benchmark.rs, vec_search_benchmark.rs), NOT LoCoMo evaluation benchmarks.
- **Verdict:** Methodology is described (LoCoMo dataset, 10 conversations, LLM-as-Judge), but no absolute score is published. The "+35% SOTA" claim is relative to an unspecified baseline. Marked as claim only — no independently verifiable absolute score.

### b_methodology ✅ VERIFIED
- **README** — "Fully reproducible benchmarks: LoCoMo (10 × ~26K-token conversations), open-source eval, LLM-as-Judge"
- **Verdict:** Methodology described with dataset, sample size, and evaluation approach.

---

## Architecture — Verified Absences

All of the following are confirmed **absent** from README, MV2_SPEC.md, CLAUDE.md, and docs.memvid.com:

- **proxy** ❌ — Library/SDK architecture, no proxy layer
- **webUi** ❌ — No web UI or TUI mentioned (CLI only)
- **multiAgent** ❌ — No multi-agent orchestration

---

## Data Model — Verified Absences

All of the following are confirmed **absent**:

- **actions** ❌ — No action tracking
- **anticipatedQueries** ❌ — No anticipated query system
- **triggerRules** ❌ — No trigger rules
- **domainTag** ❌ — No domain tagging (tags are free-form key-value, not domain-specific)
- **taskType** ❌ — No task type classification
- **context** ❌ — No "why" context field on frames
- **source** ❌ — No source attribution field
- **originTrust** ❌ — No trust/origin scoring
- **emotional** ❌ — No emotional dimension
- **conflict** ❌ — No conflict detection

---

## Search — Verified Absences

- **deep** ❌ — No deep search over reasoning/thinking
- **codeGraph** ❌ — No code graph (no Tree-sitter or similar)
- **docsSearch** ❌ — No documentation ingestion/search subsystem
- **factQuery** ❌ — No structured fact/metadata query API (entity state() is O(1) key lookup, not fact query)

---

## Knowledge Lifecycle — Verified Absences

- **decay** ❌ — No decay/forgetting mechanism
- **supersede** ❌ — Frames are append-only, immutable. Tombstones exist (status=1) for deletion but no supersede/replace semantics
- **contradiction** ❌ — No contradiction detection
- **quarantine** ❌ — No quarantine mechanism
- **autoResolve** ❌ — No auto-resolution
- **trustModel** ❌ — No trust model
- **explicitForget** ❌ — Frame tombstoning exists internally (MV2_SPEC.md: status=1 tombstoned) but no user-facing "forget" API documented

---

## Extraction Pipeline — Verified Absences

- **autoExtract** ❌ — Manual `put_bytes()` API; no automatic extraction from conversation/context
- **contentPreproc** ❌ — No content preprocessing described
- **dedup** ❌ — No deduplication described
- **qualityRefine** ❌ — No quality refinement via LLM
- **narrative** ❌ — No narrative generation
- **clustering** ❌ — No clustering
- **recurrence** ❌ — No recurrence detection
- **persona** ❌ — No persona extraction

---

## Summary of Corrections

| Feature | Current | Should Be | Evidence |
|---------|---------|-----------|----------|
| **singleBinary** | true | **false** | Cargo.toml: library crate, no [[bin]] targets. CLI requires Node.js |
| **entities** | false | **true** | docs.memvid.com: Memory Cards, SPO triplets, `mem.state()`, `mem.enrich()` |
| **hybrid** | false | **true** | docs.memvid.com: "Hybrid search (combines both - default)" |
| **schemaFields** | 8 | **9** | MV2_SPEC.md Frame Structure: 9 fields (frame_id, uri, title, created_at, encoding, payload, payload_checksum, tags, status) |
| **b_locomo** | "+35% SOTA" | "+35% SOTA" | Claim verified as stated in README, but no absolute score published — relative claim only |

---

## Evidence URLs

- GitHub README: https://github.com/memvid/memvid#readme
- MV2_SPEC.md: https://github.com/memvid/memvid/blob/main/MV2_SPEC.md
- CLAUDE.md: https://github.com/memvid/memvid/blob/main/CLAUDE.md
- Cargo.toml: https://github.com/memvid/memvid/blob/main/Cargo.toml
- Docs: https://docs.memvid.com
- Benchmarks: https://github.com/memvid/memvid/tree/main/benches
