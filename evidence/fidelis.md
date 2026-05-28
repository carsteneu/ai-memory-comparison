# Fidelis — Audit Evidence

**Date**: 2026-05-28
**Source**: https://github.com/hermes-labs-ai/fidelis (NOT fidelis-memory/fidelis — that returns 404)
**License**: MIT (confirmed in pyproject.toml: `license = { text = "MIT" }`)
**Version**: 0.0.9 (pre-release, Alpha)
**Stars**: 20
**Language**: Python 99.6%
**Created**: ~2026-03/04 (CHANGELOG.md goes back to v0.0.1)
**Author**: Hermes Labs (Rolando "Roli" Bosch), solo founder, San Francisco Bay Area
**Website**: https://hermes-labs.ai

> Note: The URL `fidelis-memory/fidelis` provided in the task does not exist (404). The actual repository is `hermes-labs-ai/fidelis`. The project was developed under the internal codename `cogito-ergo`; the on-disk store path remains `~/.cogito/` for v0.0.x compatibility.

---

## Claim-by-Claim Audit

### Infrastructure & Core

| Claim | Verdict | Evidence |
|-------|---------|----------|
| **offline** | TRUE | "local-first", "fully local with no outbound network calls" in default zero-LLM path. Server runs at `http://127.0.0.1:19420`. Data stored in ChromaDB + SQLite at `~/.cogito/`. `unset OPENAI_API_KEY ANTHROPIC_API_KEY` — recall still works. The entry `offline: true` is correct. |
| **privacy** | TRUE | "private - local memory store by default". "Zero data egress in the default zero-LLM path simplifies SOC2 / HIPAA scoping for the memory layer." "Your notes never leave the box." Default path has no outbound network calls. Optional `--tier filter` and `--tier flagship` modes do call an LLM but only for integer-pointer selection — the LLM cannot rephrase memory content. |

### Schema Fields

The memory model is passage-based: verbatim text stored and retrieved. The `/store` endpoint takes `{"text": "...", "id": "<optional uuid>"}`. Responses are `{"text": "...", "score": 0.87}`. No formal schema with enumerated metadata fields is documented.

| Claim | Verdict | Evidence |
|-------|---------|----------|
| **entities** | FALSE | No entity extraction mentioned. The system stores verbatim passages, not structured entity-key-value triples. The `/add` endpoint uses a mem0 extraction LLM to break raw text into facts, but these are atomic fact strings, not typed entities. |
| **keywords** | FALSE | No keyword tagging on memories. The `fidelis calibrate` command builds a "vocab bridge" for query expansion, but this is query-side expansion, not per-memory keyword metadata. |
| **schemaFields=8** | OVERCLAIM | From the API response shapes and pyproject.toml dependencies, the stored memory appears to have at most: (1) `text`, (2) `id`, (3) embedding vector (ChromaDB internal), (4) score (retrieval-time). No additional metadata fields (source, timestamp, tags, category, etc.) are documented. 8 fields is not supported. Recommend: 3–4 fields. |

### Search & Retrieval

| Claim | Verdict | Evidence |
|-------|---------|----------|
| **fulltext** | TRUE | BM25 search confirmed in recall_hybrid path: "BM25 + dense + RRF, no LLM". The `fidelis query` command and `/query` endpoint provide lexical search. pyproject.toml lists `bm25s>=0.2` as an optional dependency for hybrid mode. |
| **semantic** | TRUE | Dense embeddings via Ollama `nomic-embed-text` (~280 MB model). Vector similarity search. The `/recall_b` endpoint does "Stop-word stripping → Sub-query decomposition (up to 8) → Bigram + trigram generation → Vocab expansion → RRF merge". ChromaDB is the vector store. |
| **searchModes=2** | TRUE | Two fundamental retrieval modes: (1) BM25/lexical (fulltext), (2) dense/vector (semantic). Combined via RRF fusion in the hybrid path. The `/recall_hybrid` endpoint merges both. Distinct endpoints: `/query` (vector), `/recall_b` (zero-LLM decomposed), `/recall_hybrid` (BM25+dense+RRF). The entry `searchModes: 2` is correct. |

### Knowledge Lifecycle

| Claim | Verdict | Evidence |
|-------|---------|----------|
| **supersede** | FALSE | No versioning, update, or replace semantic documented. The `/store` endpoint accepts an optional `id` parameter, but there is no described behavior for updates to existing IDs (likely overwrite, not supersede with history). No version chain or "supersedes" relationship. |
| **explicitForget** | FALSE | No delete/forget endpoint in the HTTP API. Agents.md lists all 9 endpoints: `/health`, `/snapshot`, `/recall`, `/recall_b`, `/recall_hybrid`, `/query`, `/store`, `/add`, `/replay`. No `/delete`, `/forget`, or equivalent. |

### Intelligence / Extraction

| Claim | Verdict | Evidence |
|-------|---------|----------|
| **autoExtract** | PARTIAL (opt-in) | The `/add` endpoint extracts facts from raw text using a mem0 extraction LLM (`qwen3.5:0.8b` by default). The CLI `fidelis watch ~/notes` auto-ingests markdown files via filesystem watching. However, the core design philosophy is verbatim storage — the default write path (`/store`) takes pre-curated text. AutoExtract exists but is not the primary workflow. Recommend: `true` with note "opt-in via /add endpoint and fidelis watch". |
| **dedup** | FALSE | No deduplication logic described in README, agents.md, or STATUS.md. No `consolidate()` or dedup endpoint. |
| **narrative** | FALSE | No narrative construction mentioned. The system returns verbatim passages. |
| **recurrence** | FALSE | No recurrence tracking mentioned. |
| **persona** | FALSE | No persona/profile system mentioned. The config has a `user_id` field (default `"agent"`) but this is a namespace label, not a persona with traits/preferences. |

### Other Features (not claimed)

The snapshot layer is a notable unclaimed feature: the `/snapshot` endpoint returns a compressed index (~741 tokens) for context injection at session start. This enables cross-reference recall (snapshot + recall gets 50% on cross-ref queries vs. 0% with recall alone per agents.md).

| Claim | Verdict | Evidence |
|-------|---------|----------|
| **layeredMemory** | FALSE | No explicit layer system (working/session/long-term). There are two retrieval paths (Path A: atomic facts, Path B: session retrieval), but these are architectural paths, not memory lifecycle layers. The snapshot is a compressed index, not a layer. |
| **timeTravel** | FALSE | No version history, timeline view, or state rollback. The `/snapshot` endpoint provides a current-state index, not historical snapshots. No "go back to previous state" mechanism. |

### Platform Support

| Claim | Verdict | Evidence |
|-------|---------|----------|
| **p_claude** | TRUE | MCP server for Claude Code. `fidelis mcp install` "wires Claude Code". Three MCP tools: `fidelis_recall`, `fidelis_query`, `fidelis_health`. README: "Claude Code via MCP in about 60 seconds." pyproject.toml: `fidelis-server = "fidelis.server:main"`. The entry `p_claude: true` is correct. |
| **p_codex** | FALSE | Not mentioned in README, agents.md, or pyproject.toml. |
| **p_opencode** | FALSE | Not mentioned in README, agents.md, or pyproject.toml. |
| **p_gemini** | FALSE | Not mentioned in README, agents.md, or pyproject.toml. |
| **p_cursor** | FALSE (implicit MCP) | Not explicitly named. fidelis is MCP-compatible and Cursor supports MCP, but no Cursor-specific integration, documentation, or config is provided. MCP alone is not platform certification. The README names only Claude Code. |
| **p_windsurf** | FALSE | Not mentioned in README, agents.md, or pyproject.toml. |

No platform support for: p_codex, p_opencode, p_gemini, p_windsurf. Only Claude is explicitly supported. Cursor is technically possible via MCP but not documented.

---

## Summary of data.js Corrections Needed

### Fields to change:

| Field | Current | Correct | Evidence |
|-------|---------|---------|----------|
| `sourceUrl` | `"https://github.com/fidelis-memory/fidelis"` | `"https://github.com/hermes-labs-ai/fidelis"` | 404 on old URL; actual repo is `hermes-labs-ai/fidelis` |
| `offline` | (verify) | `true` | Local-first, zero network in default path |
| `privacy` | (verify) | `true` | Zero data egress in default path, SOC2/HIPAA-friendly |
| `fulltext` | (verify) | `true` | BM25 via bm25s package, confirmed in pyproject.toml |
| `semantic` | (verify) | `true` | Dense embeddings via Ollama nomic-embed-text + ChromaDB |
| `searchModes` | `2` | `2` (correct) | BM25 + dense, combined via RRF |
| `autoExtract` | (verify) | `true` | `/add` endpoint + `fidelis watch` for auto-ingestion |
| `license` | (verify) | `"MIT"` | pyproject.toml: `license = { text = "MIT" }` |
| `schemaFields` | `8` | `3` | text, id, embedding (conservative); 8 is overclaim |
| `storage` | (verify) | `"ChromaDB + SQLite (~/.cogito/)"` | README + agents.md |
| `setup` | (verify) | `"pip install fidelis"` | pyproject.toml + README quickstart |
| `deployment` | (verify) | `"Local server (launchd/systemd)"` | `fidelis init` installs background service |

### Fields to keep as-is (verified correct):

- `p_claude: true` — MCP server documented for Claude Code
- `searchModes: 2` — BM25 + dense = 2 fundamental modes
- `offline: true`, `privacy: true`, `fulltext: true`, `semantic: true`

### Fields that are OVERCLAIMS (should be false):

- `entities: false` — no entity extraction
- `keywords: false` — no keyword tagging
- `layeredMemory: false` — no layer system
- `timeTravel: false` — no history/versioning
- `supersede: false` — no update-with-history
- `explicitForget: false` — no delete endpoint
- `dedup: false` — no dedup logic
- `narrative: false` — no narrative construction
- `recurrence: false` — no recurrence tracking
- `persona: false` — no persona system
- `p_codex: false`, `p_opencode: false`, `p_gemini: false`, `p_windsurf: false` — no platform support
- `schemaFields` should be 3, not 8

---

## Other Findings

### Unique Architecture: Zero-LLM Retrieval

fidelis's defining feature is that the default retrieval path contains no LLM. The optional `--tier filter` and `--tier flagship` modes use an LLM, but strictly as an integer-pointer selector: the LLM sees indexed passages and returns integer indices; the server dereferences those to the original verbatim text. The LLM *cannot* rephrase memory content. This is a structural fidelity guarantee, not a prompting convention.

### Two Retrieval Paths (Path A / Path B)

Per STATUS.md, fidelis has two distinct retrieval architectures:
- **Path A (`/recall`)**: Atomic facts (~50-200 chars), dense retrieval + optional LLM reranker. 75% on internal 31-case eval.
- **Path B (`/recall_hybrid`)**: Session retrieval (2000+ char multi-turn), BM25 + dense + RRF, regex router, tiered LLM escalation. 96.4% R@1 on LongMemEval_S but only 54% on internal eval — 21pt regression due to architectural mismatch.

This workload divergence is transparently documented in STATUS.md as a known bug.

### LongMemEval-S Benchmark Results

- Retrieval R@1: **83.2%** (zero-LLM hybrid)
- Retrieval R@5: **98.3%**
- End-to-end QA: **73.0%**, Wilson 95% CI [68.7%, 77.0%]
- Per-category R@1: single-session-user 100%, multi-session 99.2%, knowledge-update 98.6%, single-session-assistant 98.2%, temporal-reasoning 92.1%, single-session-preference 86.7%
- Cost: **$0/query** (local retrieval)
- Mean latency: **216 ms** (zero-LLM hybrid)
- Raw evidence: `bench/runs/zeroLLM-full-20260424/aggregate.json` and `experiments/zeroLLM-FLAGSHIP-evidence/SUMMARY.json`

Competitive context from README: Mem0 ~66–70%, Zep 71.2%, Supermemory 81.6%, raw GPT-4o 60.2%.

### Honest Limitations

STATUS.md documents known issues transparently:
1. The optional LLM tier escalates ~80% of queries instead of the intended ~10% (8x cost miss)
2. Verify-guard logic is coded but never activated in pipeline
3. Workload divergence between Path A and Path B
4. Temporal-reasoning (58%) and preference (~37%) are the weakest question types

### Snapshot Layer (Unclaimed Feature)

The `/snapshot` endpoint returns a ~741 token compressed index for context injection at session start. This is a notable feature not reflected in the claims: combined snapshot + recall achieves 85% R@1 and 96% hit@any on the internal 31-case eval per STATUS.md.

### Graceful Degradation Queue

Writes queued locally when upstream LLM is unreachable, replayed with exponential backoff, dead-letter after 5 failures. This is a production-hardening feature not claimed.

### Dependencies

- **mem0ai>=2.0.0,<3.0**: fidelis builds on mem0 as a dependency (for extraction LLM path), NOT as a competitor. The dependency is documented in pyproject.toml with the comment that mem0's ollama embedder lazy-imports `ollama` and crashes non-tty server contexts without it.
- **chromadb>=0.5.0**: vector store
- **bm25s>=0.2**: BM25 for hybrid retrieval (optional)

### Naming / Branding

The project was developed under the codename `cogito-ergo`. The package, CLI, MCP server, and HTTP service are all named `fidelis` as of v0.0.9, but the on-disk store path remains `~/.cogito/` for migration safety. Config file is `.cogito.json` (legacy filename). Environment variables support both `FIDELIS_*` and `COGITO_*` prefixes. This split branding is a known transitional artifact.

### License

MIT. Confirmed in pyproject.toml: `license = { text = "MIT" }`. Also visible as badge in README.

### Solo Founder / Small Project

20 stars, 1 fork, 59 commits, 1 contributor. Python 99.6%. Pre-release status (Alpha, v0.0.9). The project is transparently labeled as "pre-release" and warns that "Python function names and CLI commands may change."

### MCP Tool Count

Three MCP tools: `fidelis_recall`, `fidelis_query`, `fidelis_health`. Matches README documentation.
