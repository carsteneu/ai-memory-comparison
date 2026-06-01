# ArcRift — Evidence

> `evidence: "evidence/arcrift.md"`
> Updated: 2026-06-01 (v1.6.1 Desktop App release)

## Repo Identity

- **URL:** https://github.com/Eshaan-Nair/ArcRift
- **Website:** https://arcrift.vercel.app/
- **npm:** `arcrift-setup`
- **License:** MIT
- **Language:** TypeScript
- **Stars:** 150, Forks: 20, Commits: 286
- **Latest release:** v1.6.1 Desktop App (2026-05-31)
- **Created:** 2026-04-21
- **Topics:** ai, ai-agents, ai-coding, browser-extension, chatgpt, claude, cursor, deepseek, gemini, llm, local-first, mcp, memory, productivity, rag, sqlite

**Rebranding history:** Previously known as "Glia" and "Synq" before rebranding to ArcRift.

**Evidence source:** This audit is based on the public README.md, GitHub API metadata, and the v1.6.1 release assets.

---

## Vital Signs

| Claim | Status | Evidence |
|-------|--------|----------|
| stars = 150 | ✅ | GitHub API: `stargazers_count: 150` |
| language = TypeScript | ✅ | GitHub API: `language: "TypeScript"` |
| license = MIT | ✅ | GitHub API: `license: { key: "mit" }` |
| singleBinary = false | ✅ | Requires Node.js + Ollama + optional Docker |
| created = 2026-04-21 | ✅ | GitHub API: `created_at: "2026-04-21T06:26:25Z"` |

---

## Architecture

### Deployment ✅
- README: **Tauri Desktop App** — native system tray application, backend runs as hidden Rust sidecar
- README: Chrome extension + MCP server modes also available
- README: Three install paths: `.exe`/`.dmg`/`.deb` installers, `npx arcrift-setup`, or `git clone + npm run dev:desktop`
- GitHub release v1.6.1: assets include `.exe`, `.msi`, `.dmg`, `.deb`, `.rpm`, `.AppImage` — cross-platform desktop binaries

### Storage ✅
- README: "SQLite-vec (vec0 virtual tables, 768-dim float32)" + "SQLite FTS5 with Porter stemmer"
- README: "SQLite facts table (or Neo4j in Docker mode)" for knowledge graph
- README: "Zero-Docker Mode: replaces all Docker services with a single `ArcRift.db` file"

### Integration ✅
- README: Chrome extension (6 AI chat platforms) + MCP server (3+ coding tools)
- README: Both modes share the same database — "Memory saved via the extension is immediately available in `recall_context`, and vice versa"
- README: "WAL mode on all writes" allows concurrent reads/writes

### Proxy ❌
- Not a proxy — it's a local backend server + MCP

### Web UI ✅
- README: Dashboard at `localhost:3001` with 4 tabs: Graph (D3.js force-directed), History (triples), Chat (conversation bubbles), Job Queue (background indexing)
- README: "React 19 + D3.js + Vite" tech stack

### Offline ✅
- README: "100% Local (Ollama)", "Your conversations never leave your machine"
- README: SQLite mode: "All features — single `.db` file + Ollama"

### Multi-agent ❌
- No multi-agent coordination documented

### LLM providers = 2 ✅
- README: Ollama primary (`nomic-embed-text` + `llama3.1:8b`), Grok API key as fallback
- README: "Ollama must be running for the MCP server to generate embeddings and extract knowledge graph triples"

### Cache optimization ❌
- Not mentioned

### Procedural memory ❌
- Not mentioned

### Sandboxed exec ❌
- Not mentioned

### Scheduled/autonomous ❌
- Background job queue is for internal indexing, not user-scheduled execution

### Privacy ✅
- README: "PII Scrubbing: API keys, JWTs, connection strings, email addresses, and internal IPs are redacted to `[REDACTED]` in the browser before any data is sent to the backend"
- README: "Local Embeddings: `nomic-embed-text` runs entirely via Ollama — zero API calls for embeddings"
- README: "CORS Locked: The backend rejects requests from any origin other than `localhost`"
- README: Helmet security headers (CSP, X-Frame-Options, X-Content-Type-Options)

### Export ❌ (not claimed)
- Not mentioned — but SQLite `.db` file is inherently portable

### Setup ✅
- README: "npx arcrift-setup" — clones repo, checks deps, pulls Ollama models, installs packages, builds backend
- README: Or download installer from GitHub Releases

---

## Data Model

### Storage unit ✅
- README: Three-tier: **sentence-level chunks** (surgical retrieval), **chunk-level** (300 word windows, 80-word overlap), **knowledge graph facts** (subject-relation-object triples)
- README: "Sentence vectors, chunk vectors, and FTS5 keyword search run in parallel"

### Entities ✅
- README: "22 entity types, 20+ relation types" in knowledge graph
- README: Graph Stress Audit: "1,200+ nodes, 1,087 triples in a single session"

### Context (why) ✅
- README: Conversations saved with project name, timestamps, platform attribution
- README: MCP tools: `store_memory` saves "decisions and context", `get_project_summary` returns "structured knowledge graph summary"

### Keywords ✅
- README: "FTS5 keyword search" with "Prefix keyword matching" (wildcard suffixes)
- README: FTS5 engine contributed 43/54 hits in web benchmark, 24/27 hits in MCP benchmark

### Data sources = 3 ✅
- README: (1) Browser chat conversations via Chrome extension, (2) MCP `store_memory` tool, (3) **Direct Codebase Indexing** (v1.6.1 new — scan project files into knowledge graph)

### Schema fields = 7 (estimate) ⚠️
- README does not provide exact schema field count
- Source inspection needed for precise count

### Layered memory ❌
- All layers (sentence/chunk/graph) are searched in parallel, not promoted between tiers

### Time-travel ❌
- No git-like versioning, branching, or rollback documented

### Emotional ❌
- Not mentioned

### Conflict ❌
- Not mentioned

### Origin + trust ❌
- Not mentioned

### Actions ❌
- Not mentioned

### Anticipated queries ❌
- Not mentioned (though HyDE generates hypothetical answers)

### Trigger rules ❌
- Auto-connect is always-on per project, not rule-based

### Domain tag ❌
- Not mentioned

### Task type ❌
- Not mentioned

---

## Search & Retrieval

### Full-text ✅
- README: "SQLite FTS5 with Porter stemmer" in tech stack
- README: Keyword engine documented in both web and MCP benchmarks

### Semantic/vector ✅
- README: "Sentence vectors" and "chunk vectors" with `nomic-embed-text` (768-dim) via sqlite-vec
- README: "Chunks are split into individual sentences at index time. On retrieval, only the sentences that directly match the query are returned"

### Hybrid (BM25+Vec) ✅
- README: "Three-Layer Hybrid Search: Sentence vectors, chunk vectors, and FTS5 keyword search run in parallel. Results are fused and ranked by a combined score."

### Deep (incl. thinking) ❌
- Not mentioned

### Code graph ❌
- README: "Direct Codebase Indexing" scans files into knowledge graph, but does not build an AST-level code graph with symbol resolution

### Docs search ❌
- Not mentioned

### Fact metadata query ❌
- Not mentioned

### Timeline view ✅
- README: Dashboard "History" tab shows "All extracted triples (subject / relation / object) with timestamps"

### Search modes = 3 ✅
- README: (1) sentence vector, (2) chunk vector, (3) FTS5 keyword — all three verified

### HyDE ✅ (bonus, not in comparison schema)
- README: "Before querying the vector store, ArcRift generates a hypothetical answer to your query and uses that embedding alongside the raw query"

### Small-to-big retrieval ✅ (bonus)
- README: "High-precision sentence match triggers fetching the parent chunk for broader context"

### Surgical sentence trimming ✅ (bonus)
- README: "Reduces prompt noise by up to 95%" — only matching sentences returned, not full paragraphs

---

## Knowledge Lifecycle

### Decay/forgetting ❌
- Not mentioned — no time-based decay or Ebbinghaus curve

### Supersede/replace ✅
- README: `prune_memory` tool: "Surgically removes facts or chunks matching a description. Corrects outdated information without wiping an entire project."
- README: "Delete-then-insert for vector updates" pattern handles re-saving

### Contradiction detection ❌
- Not mentioned

### Quarantine ❌
- Not mentioned

### Auto-resolution ❌
- Not mentioned

### Trust model ❌
- Not mentioned

### Explicit forget ✅
- README: `prune_memory` MCP tool explicitly removes memories
- README: Dashboard graph pruning

---

## Extraction Pipeline

### Auto-extraction ✅
- README: "Auto-Connect: Once a session is active, ArcRift re-attaches automatically on every page load" — prompts intercepted without manual action
- README: Knowledge graph extraction: "Every saved conversation is processed to extract subject-relation-object triples (22 entity types, 20+ relation types)"
- README: Background job queue: sentence-level embedding offloaded to async jobs

### Content-aware preprocessing ✅
- README: **PII scrubbing** (API keys, JWTs, emails, IPs → `[REDACTED]`)
- README: **Injection defence**: "Retrieved chunks are scanned for 10 known prompt injection patterns before being injected"
- README: **5-character minimum sentence filter**: "ignores fragments shorter than 5 characters"
- README: **History-aware fallback**: if query is history-seeking, returns first 3 sentences

### Deduplication ✅
- README: "FNV-1a Deduplication: Identical conversation segments are fingerprinted and skipped"

### Quality refinement ❌
- No LLM-based consolidation or two-pass refinement documented

### Narrative generation ❌
- Not mentioned

### Clustering ❌
- Not mentioned

### Recurrence detection ❌
- Not mentioned

### Persona extraction ❌
- Not mentioned

---

## Platform Support

### Claude Code ✅
- README: `claude mcp add ArcRift node /path/to/ARCRIFT/backend/dist/mcp/server.js`
- README: Browser extension supports Claude.ai web interface

### Codex ❌
- Not mentioned in README

### OpenCode ❌
- Not mentioned in README

### Gemini CLI ❌
- Browser extension supports Gemini web, no Gemini CLI integration

### Copilot (IDE) ❌
- Browser extension supports Microsoft Copilot web, but no GitHub Copilot IDE plugin

### Cursor ✅
- README: `.cursor/mcp.json` MCP setup documented

### Windsurf ✅
- README: `.windsurf/mcp.json` MCP setup documented

### OpenClaw ❌
- Not mentioned

### Hermes ❌
- Not mentioned

### pi/omp ❌
- Not mentioned

### Antigravity ❌
- Not mentioned

---

## Benchmarks

Custom benchmarks published in README (not LoCoMo/LongMemEval):

| Benchmark | Result | Detail |
|-----------|--------|--------|
| Web Recall@1 | 90.0% | 54/60 correct facts at rank 1 |
| Web MRR | 0.806 | Correct answer at position 1.24 avg |
| Web Context Compression | 95.0% | 55,350 → 2,784 chars |
| MCP Total Recall | 90% | 27/30 correct across 3 phrasings |
| MCP Context Compression | 81.3% | 131,700 chars noise redacted |
| Project Isolation | 100% | Zero cross-project leakage (10 projects) |
| Graph Stress | 1,087 triples | 4,056 triples/sec ingestion |
| Graph Dashboard Load | < 1.5s | D3.js physics-simulated render |

### LoCoMo: —
- Not submitted to LoCoMo benchmark

### LongMemEval: —
- Not submitted to LongMemEval

### Methodology open ✅
- README: Full benchmark reports in `reports/benchmark_web.md`, `reports/benchmark_mcp.md`, `reports/mcp_stress_test.md`, `reports/graph_stress_test.md`
- Scripts in `backend/scripts/` — "All results are reproducible"

---

## Notable Features Not in Comparison Schema

| Feature | Detail |
|---------|--------|
| **HyDE (Hypothetical Document Embedding)** | Generates hypothetical answer, embeds both query and answer for improved recall |
| **Surgical Sentence Trimming** | Only returns matching sentences, not full paragraphs — 95% noise reduction |
| **Small-to-Big Retrieval** | Sentence-level precision triggers parent chunk for broader context |
| **FNV-1a Dedup** | Fingerprints segments, skips duplicates |
| **Dead Letter Queue** | Failed jobs retried 5× with exponential backoff, visible in dashboard |
| **Ghost Job Cleanup** | Auto-resets stuck jobs on restart |
| **WAL Concurrency** | SQLite WAL mode allows concurrent reads/writes |
| **Multi-Strategy DOM Resolver** | 5 ordered selector strategies per platform, auto-fallback on UI changes |
| **Rate Limiting** | Separate rate limits for save vs read endpoints |
| **PII Scrubbing** | JWTs, API keys, emails, IPs → `[REDACTED]` before disk |
| **Injection Defence** | 10 prompt injection patterns scanned on retrieved chunks |
| **Tauri Desktop App** | v1.6.1 — native system tray app, Rust sidecar, esbuild (~0.1s start) |
| **Esbuild Backend** | Start time reduced from 60s → ~0.1s |
| **Direct Codebase Indexing** | v1.6.1 — index project files into knowledge graph |
| **GitHub Actions Auto-Releases** | Cross-compiled Mac/Windows/Linux installers |
