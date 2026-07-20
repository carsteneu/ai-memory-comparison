# Midas — Evidence

> Every ✅ claim is backed by public source code or documentation.
> Audited 2026-07-20 against public Midas v1.0.0 at commit [`face702`](https://github.com/vornicx/Midas/commit/face702d33b9d37d0e0f521a47ff8d663ece9d38).

**Repo:** `github.com/vornicx/Midas`

**Version:** `1.0.0`

**Stars:** 12 (2026-07-20)

**Language:** Python · TypeScript (experimental parity port)

**License:** Apache-2.0

**Created:** 2026-06-04
**Description:** Local, governed memory and trust plane for long-horizon coding agents — source-traceable recall, action-safety guard, conflict and time-travel views, and a default no-LLM ingest/query path.

---

## System Metadata

| Field | Value |
|---|---|
| **Deployment** | `Local CLI + MCP server + SDK` |
| **Storage** | `SQLite` (optional SQLCipher encryption at rest) |
| **Integration** | `MCP / CLI / SDK / LangGraph` |
| **Single binary?** | `no` (Python package; experimental TypeScript port also ships through npm) |
| **Setup** | `uv tool install "midas-memory[mcp,local]"` then `midas init` · Node: `npx -y midas-memory-mcp` |
| **Pricing** | `free` (Apache-2.0; no paid tiers or feature gates) |
| **Storage unit** | `Memory (verbatim text record)` |

- Sources: [README install and setup](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/README.md#L13-L23), [client and interface overview](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/README.md#L132-L166), [free and open-source terms](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/README.md#L346-L351), and [`pyproject.toml`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/pyproject.toml#L1-L7).

---

## Architecture

### Proxy ❌

### Web/TUI ✅
> `midas inspect` is a local glass-box web interface over the SQLite store. It includes overview, browse/search, belief history, project state and diff, governance, conflicts, open loops, and the audit chain.
- Sources: [README — Memory Inspector](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/README.md#L315-L344) and [`midas/inspector.py`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/inspector.py#L1-L12).

### Offline ✅
> The default hashing backend and the local ONNX embedding path run without an API key; the core memory operations make no network calls.
- Sources: [`HashingEmbedder` and local embedding implementations](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/embeddings.py#L38-L57) and [README privacy boundary](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/README.md#L389-L396).

### Multi-agent ✅
> Multiple MCP clients/processes share one live SQLite file, detect each other's writes, and can be partitioned by namespace/project. The Python and TypeScript runtimes share the same schema.
- Sources: [README — one memory, many clients](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/README.md#L199-L216), [`SQLiteStore` cross-process refresh](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/sqlite_store.py#L1-L12), and [`_refresh_if_stale`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/sqlite_store.py#L166-L181).

### LLM providers (count: 3) ✅
> Under this comparison's rule that first-class embedding backends count, Midas exposes hashing/offline, local FastEmbed/ONNX, and OpenAI embedding implementations. No LLM is required for the default ingest/query path.
- Sources: [`HashingEmbedder` and `OpenAIEmbedder`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/embeddings.py#L38-L105) and [`LocalEmbedder`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/embeddings.py#L313-L357).

### Cache optimization ✅
> Embeddings are persistently cached, and context assembly has a measured relevance floor that removes 30–40% of context tokens without reducing recall on the published deterministic A/Bs.
- Sources: [`DiskCachedEmbedder`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/embeddings.py#L158-L237) and [BENCHMARKS — context parsimony](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/BENCHMARKS.md#L109-L129).

### Procedural memory ❌

### Sandboxed execution ❌

### Scheduled/autonomous ✅
> `MIDAS_MCP_AUTO_MAINTAIN=<minutes>` starts a daemon loop that periodically expires configured TTLs, consolidates duplicates, and re-bounds the store without a manual tool call. The interval is configuration-backed and is restored whenever the MCP server restarts.
- Sources: [MCP server configuration](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/mcp_server.py#L23-L37) and [background maintenance loop/startup](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/mcp_server.py#L902-L963).

### Privacy/encrypt ✅
> Local-only storage, no telemetry/account, zero data egress for core memory operations, and optional SQLCipher encryption at rest that fails closed when encryption support is unavailable.
- Sources: [README privacy and encryption](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/README.md#L389-L396) and [`SQLiteStore` SQLCipher guard](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/sqlite_store.py#L77-L94).

### Data export ✅
> `midas export` writes a structured JSON backup that can be imported on another machine; importers also cover Midas JSON, CLAUDE.md, Cursor rules, JSONL, Mem0, and Zep.
- Sources: [`cmd_export`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/cli.py#L570-L650), [`cmd_import`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/cli.py#L652-L704), and [CLI command definitions](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/cli.py#L858-L873).

---

## Data Model

### Entities ❌

### Actions ❌

### Keywords/tags ❌

### Anticipated queries ❌

### Trigger rules ❌

### Domain tag ❌

### Task type ❌

### Context (why) ❌

### Source attribution ✅
> Every record carries `actor`, a four-level `provenance`, and a free-form `source` pointer; recall and inspection preserve these fields.
- Source: [`MemoryProvenance` and `MemoryRecord`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/types.py#L24-L46).

### Origin + trust ✅
> Trust is ordered by capture origin (`user_confirmation > action > observation > planning`), and duplicate capture can only upgrade provenance.
- Sources: [provenance rank](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/memory.py#L151-L156) and [`_upgrade_provenance`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/memory.py#L511-L532).

### Emotional ❌

### Conflict surfacing ✅
> `memory_conflicts` surfaces and ranks pairs of live beliefs that appear to contradict one another without auto-deleting either; it is exposed through the SDK, MCP, `resume`, and Inspector.
- Sources: [control-plane contract](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/continuity.py#L1-L20), [`memory_conflicts`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/continuity.py#L113-L164), and [Inspector conflict view](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/README.md#L326-L336).

### Layered memory ✅
> Optional distillation keeps verbatim raw turns as an audit layer and stores marked distilled facts as an index layer above them. The default remains raw/verbatim and the LLM-based distiller is explicitly opt-in.
- Sources: [`Memory.distill` layered behavior](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/memory.py#L457-L506) and [documented default/off-by-default boundary](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/README.md#L357-L368).

### Time-travel ✅
> `recall(as_of=...)` resolves supersession chains to the belief version valid at a past time; Inspector exposes belief history and time travel.
- Sources: [`recall(as_of=...)`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/memory.py#L584-L645), [historical chain resolution](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/memory.py#L1009-L1032), and [Inspector time-travel view](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/README.md#L326-L335).

### Schema fields (count: 8) ✅
> Count excludes generated IDs/timestamps and the derived embedding: `content`, `kind`, `importance`, `source`, `provenance`, `actor`, `metadata`, `superseded_by`.
- Source: [`MemoryRecord`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/types.py#L33-L46).

---

## Search & Retrieval

### Full-text ✅
> Pure-Python Okapi BM25 keyword ranking.
- Source: [`midas/bm25.py`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/bm25.py#L1-L54).

### Semantic/vector ✅
> Embedding-based cosine search with a configurable store/index protocol.
- Sources: [`Memory.recall`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/memory.py#L584-L665) and [`cosine`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/embeddings.py#L404-L406).

### Hybrid (BM25+Vec) ✅
> Semantic and BM25 candidate sets are fused with RRF.
- Source: [`_hybrid_candidates`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/memory.py#L766-L833).

### Deep (incl. thinking) ❌

### Code graph ❌

### Docs search ❌

### Fact metadata query ✅
> Recall supports structured filters for memory kind, minimum importance, arbitrary metadata equality, and namespace/project scope.
- Source: [`Memory.recall` filter parameters and predicate](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/memory.py#L584-L633).

### Timeline view ✅
> Historical `as_of` retrieval and Inspector belief history/project diff provide temporal search and chronological browsing.
- Sources: [SDK `as_of` example](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/README.md#L290-L304) and [Inspector belief history/diff](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/README.md#L326-L335).

### Search modes (count: 3) ✅
> Semantic bi-encoder, hybrid lexical+vector RRF, and optional reranked retrieval.
- Source: [semantic/hybrid/reranker branches in `Memory.recall`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/memory.py#L635-L663).

### Data sources (count: 1) ✅
> One unified memory-record corpus, typed by `kind`.
- Source: [`MEMORY_KINDS`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/types.py#L13-L22).

---

## Knowledge Lifecycle

### Decay/forgetting ✅
> Selective forgetting evicts the lowest-value memories by importance × recency. Per-kind TTLs can also expire records during manual or scheduled maintenance while protecting confirmed/standing memories and supersession chains.
- Sources: [`forget_decayed`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/memory.py#L1272-L1331), [`forget_expired`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/memory.py#L1345-L1367), and [MCP maintenance tool](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/mcp_server.py#L788-L817).

### Supersede/replace ✅
> Belief revision marks the old record with a traceable `superseded_by` chain and resolves recall to the current head rather than deleting history.
- Sources: [`MemoryRecord.superseded_by`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/types.py#L33-L46) and [supersession resolution](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/memory.py#L970-L1032).

### Contradiction detection ✅
> Optional local NLI gates belief revision, while the control-plane also surfaces unresolved live conflicts.
- Sources: [`LocalNLI.contradiction`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/nli.py#L24-L90) and [`memory_conflicts`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/continuity.py#L113-L164).

### Quarantine ❌

### Auto-resolution ❌

### Trust model ✅
> Planning may use any provenance, answers reject planning-only memory, and external/destructive actions require current `user_confirmation` evidence. Prohibitions veto authorization and cross-namespace confirmations cannot authorize another namespace.
- Sources: [allowed provenance tiers](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/guard.py#L20-L27) and [`decide_memory_use`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/guard.py#L116-L201).

### Explicit forget ✅
> Delete one record chain-safely, preview and erase a relevance-matched topic with a receipt, or clear the store.
- Sources: [`forget`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/memory.py#L1369-L1385) and [`forget_matching`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/memory.py#L1386-L1414).

---

## Extraction Pipeline

### Auto-extraction ❌
> Midas can auto-capture user turns through an optional Claude Code SessionEnd hook, but the default path deliberately stores selected turns verbatim rather than automatically extracting structured facts. Optional LLM distillation requires explicit configuration/call, so it does not meet this criterion.

### Content-aware preprocessing ❌

### Deduplication ✅
> Capture skips near-duplicates; maintenance can collapse highly similar restatements while retaining the highest-value copy.
- Sources: [dedup policy](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/policy.py#L24-L38) and [`consolidate`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/memory.py#L1416-L1463).

### Quality refinement ✅
> Deterministic importance scoring, retrieval confidence/abstention, and optional local contradiction/reranking passes refine what is retained and returned.
- Sources: [`ContentImportance` / `StructuralImportance`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/importance.py#L42-L137) and [`recall_confidence`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/memory.py#L860-L881).

### Narrative generation ✅
> `resume` generates a token-budgeted, prompt-ready session handoff containing pinned directives, current state, changes, open loops, and unresolved conflicts.
- Sources: [control-plane contract](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/continuity.py#L1-L20) and [`resume`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/continuity.py#L224-L295).

### Clustering ❌

### Recurrence detection ✅
> Restatements reinforce an existing memory's salience/recency instead of creating another record.
- Source: [`_reinforce_record` / `_reinforce_existing`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/midas/memory.py#L542-L563).

### Persona extraction ❌

---

## Platform Support

### Claude Code ✅
- Source: [documented Claude Code MCP setup](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/README.md#L174-L180) and [optional SessionEnd hook](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/README.md#L158-L164).

### Codex ✅
- Source: [documented Codex CLI setup](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/README.md#L179-L183).

### OpenCode ❌

### Gemini CLI ✅
- Source: [`midas init` client list and Gemini configuration path](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/README.md#L144-L146) and [manual setup table](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/README.md#L181-L186).

### Copilot ❌

### Cursor ✅
- Source: [documented Cursor MCP configuration](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/README.md#L174-L181).

### Windsurf ✅
- Source: [documented Windsurf MCP configuration](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/README.md#L179-L184).

### OpenClaw ❌

### Hermes ❌

### pi/omp ❌

### Antigravity ❌

---

## Benchmarks

### LoCoMo ✅
- Score: `recall@k 0.73` on the full public set (10 conversations, n=1,540), vs recency baseline `0.05`.
- Source: [BENCHMARKS full-set table, correction notice, and reproduce command](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/BENCHMARKS.md#L20-L51).

### LongMemEval ✅
- Score: `recall@k 0.92` on LongMemEval-s full set (500 questions, 246,750 turns), vs recency baseline `0.01`; published judged answer rate is `0.84` on the cost-bounded reader sample.
- Source: [BENCHMARKS full-set retrieval](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/BENCHMARKS.md#L14-L18) and [full results/reproduction](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/BENCHMARKS.md#L35-L58).

### PersonaMem ❌

### Token reduction ✅
- Score: `30–40% fewer context tokens` at unchanged recall on deterministic A/Bs; the relative relevance floor is the default.
- Source: [BENCHMARKS — context parsimony](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/BENCHMARKS.md#L109-L129).

### Methodology open ✅
> Public datasets/adapters/metrics/runner, exact commands, cost/latency instrumentation, precision@k, dumb-reader ablation, failure traces, and explicit corrections.
- Sources: [BENCHMARKS methodology and commands](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/BENCHMARKS.md#L1-L7), [`docs/methodology.md`](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/docs/methodology.md), and [`eval/`](https://github.com/vornicx/Midas/tree/face702d33b9d37d0e0f521a47ff8d663ece9d38/eval).

### Additional published evaluations (not separate comparison columns)
- **BEAM 100K → 10M:** deterministic recall@k `0.56 → 0.32` across a 100× scale-up, with the recency baseline at `0.00` on every tier; full tier sizes and weaknesses are published in [BENCHMARKS](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/BENCHMARKS.md#L136-L163).
- **Memory-safety / governance:** 10/10 adversarial attacks blocked (`ASR 0.00`) and all benign cases passed (`1.00`) in the deterministic governance suite, with the one-command reproduction path documented in the [README](https://github.com/vornicx/Midas/blob/face702d33b9d37d0e0f521a47ff8d663ece9d38/README.md#L80-L99).
