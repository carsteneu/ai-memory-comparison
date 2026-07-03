# mnemos — Evidence

**Repo:** `github.com/arhuman/mnemos`
**Stars:** 4
**Language:** Go (go 1.25, cgo-free)
**License:** MIT
**Created:** 2026-06-29
**Description:** Local, cited memory for AI agents — a single cgo-free Go binary that indexes your Markdown/OKF/docs/code into SQLite (FTS5) and serves them over MCP, so the agent can search, read, and cite your own knowledge with an exact `file#section` + line range.

---

## System Metadata

| Field | Value |
|-------|-------|
| **Deployment** | `Local CLI + MCP server (self-host)` |
| **Storage** | `SQLite (FTS5) + optional embeddings table` |
| **Integration** | `MCP (stdio) + CLI` |
| **Single binary?** | `yes` |
| **Setup** | `git clone + make install` |
| **Pricing** | `free` (open source, MIT) |
| **Storage unit** | `Chunk (document → heading-scoped chunks, cited by file#section + line range)` |

---

## Architecture

### Proxy ❌
> No conversation-stream interception. Pure MCP stdio server + CLI over the `memory` verb layer.

### Web/TUI ❌
> No visual interface. CLI (`cmd/mnemos`) + MCP tools only; no browser dashboard or TUI.

### Offline ✅
- Source: `README.md:92` — "Truly local-first: runs entirely on your machine. No network, no telemetry, no data leaves your project."
- Source: `docs/architecture.md:8` — Design principle 1 "Local-first. All data stays on the machine; no external services." Default build is lexical-only; even the optional embed build runs inference locally (pure-Go ONNX).

### Multi-agent ❌
> Single-project memory served over MCP. Any MCP client can connect, but there is no cross-agent memory sharing, agent directory, or inter-agent communication.

### LLM providers (count: 1) ✅
- Source: `README.md:284-287` — Optional `embed` build uses one local embedding provider: ONNX `all-MiniLM-L6-v2` via pure-Go inference (`internal/embed`, `internal/model`). No external LLM/embedding APIs.

### Cache optimization ❌
> Content-hash change detection avoids re-parsing unchanged files (`ingest`), and embeddings are persisted (`reindex --embeddings`), but there is no intermediate embedding/search-result cache layer.

### Procedural memory ❌
> Stores documents/notes only; no reusable scripts executed at retrieval time.

### Sandboxed execution ❌
> No user-code execution.

### Scheduled/autonomous ✅
- Source: `README.md:257-261` — `mnemos watch . --collection myproject` runs a background fsnotify watcher that debounces and incrementally re-ingests on file change (removing deleted files) without a user prompt.
- Source: `docs/architecture.md` data-flow diagram — `watcher: fsnotify → debounce → re-ingest`.

### Privacy/encrypt ✅
- Source: `README.md:319-325` (Security) — "No network, no telemetry; the MCP server is stdio-only." Read-only by default; write/delete are separate opt-ins. Path confinement guard rejects `..` traversal, symlink escapes, and `.mnemos/` access. Captured content is secret-scanned before write/index; `.env`/keys excluded from the index. (Self-hosted + zero-telemetry; no at-rest encryption.)

### Data export ❌
> The OKF tree is plain Markdown on disk (inherently portable), but there is no dedicated export command/format.

---

## Data Model

### Entities ❌
> No structured named-entity extraction.

### Actions ❌
> No command/tool-call fields.

### Keywords/tags ✅
- Source: `internal/storage/migrations/0001_init.sql:28` — `chunks.tags` column; `internal/storage/migrations/0001_init.sql:39-46` — `chunks_fts` FTS5 virtual table indexes `tags` (and `doc_type`).
- Source: `README.md:304` — frontmatter `tags`/`type` become fuzzy ranking signals in FTS.

### Anticipated queries ❌
> No generated predicted-query field.

### Trigger rules ❌
> No condition-based activation.

### Domain tag ❌
> `collection` is a namespace, not a code/marketing/legal/finance domain category.

### Task type ❌
> No task/idea/blocked/stale classification.

### Context (why) ❌
> Stores content + citation; no separate "why relevant" field.

### Source attribution ❌
> No ≥3-level author (user/agent/pipeline) field on entries.

### Origin + trust ❌
> No capture-method-based trust weighting.

### Emotional ❌
> No sentiment tracking.

### Conflict surfacing ❌
> No conflict detection between memories.

### Layered memory ❌
> Flat document→chunk model; no L0/L1/L2 hierarchy.

### Time-travel ❌
> No historical/superseded-version queries.

### Schema fields (count: ~8) ✅
- Source: `internal/storage/migrations/0001_init.sql` — per-entry structured fields (excluding auto IDs/timestamps): document-level `uri`, `collection`, `title`, `mime_type`, `frontmatter_json`; chunk-level `heading_path`, `tags`, `doc_type`, `start_line`, `end_line`, `metadata_json`. Plus `links` edges (src_doc→dst_doc).

---

## Search & Retrieval

### Full-text ✅
- Source: `internal/storage/migrations/0001_init.sql:39-46` — `CREATE VIRTUAL TABLE chunks_fts USING fts5(...)`; `README.md:96` — "SQLite FTS5 / bm25 out of the box."

### Semantic/vector ✅
- Source: `README.md:276-292` — Optional `embed` build: `all-MiniLM-L6-v2`, pure-Go ONNX inference, `mnemos search --semantic`; `internal/storage/migrations/0002_embeddings.sql` — `embeddings` table.

### Hybrid (BM25+Vec) ✅
- Source: `README.md:290-295` — "`--semantic` fuses bm25 with vector similarity" via RRF fusion; `docs/architecture.md#semantic-search-the-embed-build`.

### Deep (incl. thinking) ❌
> No reasoning-trace search.

### Code graph ❌
> Indexes Markdown/text; markdown links are captured as edges (`links` table, stored not yet traversed) but there is no AST/Tree-sitter code graph.

### Docs search ✅
- Source: `README.md:20-31` — mnemos ingests and searches your ADRs, design docs, notes, runbooks, and OKF knowledge base as its core purpose.

### Fact metadata query ✅
- Source: `README.md:243` — `mnemos.list` walks the OKF tree and filters by `path`, `collection`, `type`, or indexed state; `mnemos.search` accepts collection/type filters — structured queries over memory metadata.

### Timeline view ❌
> No since/before temporal browsing.

### Search modes (count: 4) ✅
- Source: `README.md:238-244` — read-only query tools: `mnemos.search` (ranked cited retrieval), `mnemos.read` (chunk/document by id/uri), `mnemos.context` (top-k LLM-ready context blocks), `mnemos.list` (tree walk + index metadata).

### Data sources (count: 1) ✅
- Source: `docs/architecture.md` — one unified index over the OKF/Markdown tree (ADRs, docs, notes, source code, OKF bundles all ingest into the same `documents`/`chunks` store).

---

## Knowledge Lifecycle

### Decay/forgetting ❌
> No time/disuse-based relevance decay.

### Supersede/replace ❌
> `mnemos.move` renames/relocates a doc and re-indexes it, but there is no supersede chain marking one memory as replacing another.

### Contradiction detection ❌
> None.

### Quarantine ❌
> None.

### Auto-resolution ❌
> None.

### Trust model ❌
> No multi-tier trust hierarchy.

### Explicit forget ✅
- Source: `README.md:252` — `mnemos.forget` removes a file from the OKF tree and de-indexes it (idempotent); requires `allow_delete = true`.

---

## Extraction Pipeline

### Auto-extraction ❌
> `mnemos.remember` is an explicit capture call; `ingest` indexes files but does not auto-extract structured knowledge from a session transcript.

### Content-aware preprocessing ✅
- Source: `README.md:306` — `index.md` files are treated as structure-only (kept out of FTS and the link graph); frontmatter is parsed into ranking signals — content is filtered by type before indexing.

### Deduplication ❌
> URI is document identity (second ingest of same URI overwrites), and content hashing skips unchanged files, but there is no near-duplicate detection/merge.

### Quality refinement ❌
> Secret-scanning is a safety pass, not a quality/confidence refinement.

### Narrative generation ❌
> No session summaries or handover narratives.

### Clustering ❌
> None.

### Recurrence detection ❌
> None.

### Persona extraction ❌
> None.

---

## Platform Support

### Claude Code ✅
- Source: `README.md:62-66` — `claude mcp add mnemos -- mnemos serve --config /abs/path/.mnemos.toml`; `README.md:207-230` — bundled `mnemos-okf` skill (`make install-skill`) encoding when to recall/capture.

### Codex ❌
> No dedicated integration documented (generic MCP stdio would work, but not documented/templated).

### OpenCode ❌

### Gemini CLI ❌

### Copilot ❌

### Cursor ❌

### Windsurf ❌

### OpenClaw ❌

### Hermes ❌

### pi/omp ❌

### Antigravity ❌

> mnemos is a standard MCP stdio server, so any MCP-capable client can connect (`README.md:94` — "Any MCP client"), but only Claude Code has documented setup + a bundled skill.

---

## Benchmarks

### LoCoMo ❌
- Score: —

### LongMemEval ❌
- Score: —

### PersonaMem ❌
- Score: —

### Token reduction ❌
- Score: —

### Methodology open ✅
- Source: `README.md:133-162` — `mnemos eval` auto-derives held-out query→source pairs from an OKF bundle and reports Hit@1 / Recall@12 / MRR@12 against a committed baseline; documented and reproducible in `docs/architecture.md#retrieval-evaluation`. On the shipped `examples/git-recipes` bundle: lexical 0.83, semantic+hybrid 1.00 (N=6, described as a smoke signal, not a formal benchmark).
