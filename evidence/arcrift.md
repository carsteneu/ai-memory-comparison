# arcrift — Evidence

> `evidence: "https://github.com/carsteneu/ai-memory-comparison/blob/main/evidence/arcrift.md"`

## Repo Identity

- **Claimed:** `https://github.com/arcrift/memory` — **404, repo does not exist**
- **Actual:** `https://github.com/Eshaan-Nair/ArcRift` — verified 2026-05-28
- **Website:** https://arcrift.vercel.app
- **npm:** `arcrift-setup`
- **License:** MIT
- **Language:** TypeScript (86.2%), CSS (6.5%), JavaScript (2.3%), Shell (2.0%)
- **Stars:** 75, Forks: 17, Commits: 250
- **Latest release:** v1.5.3 (2026-05-23)
- **Created:** April 2026

**Note:** The `github.com/arcrift` org exists but has zero public repositories. The actual project lives under `Eshaan-Nair/ArcRift`. The project was previously known as "Glia" and "Synq" before rebranding to ArcRift.

---

## Corrections

| Claim | Status | Detail |
|-------|--------|--------|
| `github.com/arcrift/memory` | **❌ URL correction** | 404. Correct repo is `github.com/Eshaan-Nair/ArcRift`. |
| privacy = false (data.js) | **❌ wrong** | Should be true — local-first, PII scrubbing, CORS locked to localhost |
| fulltext = false (data.js) | **❌ wrong** | Should be true — FTS5 keyword search |
| hybrid = false (data.js) | **❌ wrong** | Should be true — three-layer hybrid (sentence + chunk + keyword) |
| searchModes = 1 (data.js) | **❌ wrong** | Should be 3 — sentence vectors, chunk vectors, FTS5 keyword |
| entities = false (data.js) | **❌ wrong** | Should be true — 22 entity types, 20+ relation types |
| autoExtract = false (data.js) | **❌ wrong** | Should be true — auto-connect + knowledge graph extraction |
| dedup = false (data.js) | **❌ wrong** | Should be true — FNV-1a deduplication |
| explicitForget = false (data.js) | **❌ wrong** | Should be true — `prune_memory` tool |
| supersede = false (data.js) | **❌ wrong** | Should be true — `prune_memory` + delete-then-insert update pattern |
| p_cursor = false (data.js) | **❌ wrong** | Should be true — Cursor MCP setup documented |
| p_windsurf = false (data.js) | **❌ wrong** | Should be true — Windsurf MCP setup documented |

---

## Architecture

### Offline ✅
- `README.md` — "100% Local (Ollama)", "A local-first memory layer", "local-first philosophy"
- `README.md` — SQLite mode: all features in a single `ArcRift.db` file, no Docker needed
- `README.md` — Privacy section: "All data lives in `ArcRift.db` on your machine", "Your conversations never leave your machine"

### Privacy ✅
- `README.md` — PII scrubbing: "API keys, JWTs, connection strings, email addresses, and internal IPs are redacted to `[REDACTED]`"
- `README.md` — "Local Embeddings: `nomic-embed-text` runs entirely via Ollama — zero API calls"
- `README.md` — "CORS Locked: rejects requests from any origin other than `localhost`"
- `README.md` — Injection defence: "scanned for 10 known prompt injection patterns"

### Export ❌ (not claimed in README)
- Not mentioned — but SQLite `.db` file is inherently portable

### Web UI ✅
- `README.md` — Dashboard at `localhost:3001` with Graph, History, Chat, Job Queue tabs
- `README.md` — "React 19 + D3.js + Vite" dashboard

---

## Data Model

### Entities ✅
- `README.md` — "22 entity types, 20+ relation types" in knowledge graph
- `README.md` — Knowledge Graph Stress Audit: "1,200+ nodes, 1,087 triples"
- `README.md` — D3.js force-directed graph, "Nodes are entities, edges are relations"

### Keywords ✅
- `README.md` — "FTS5 keyword search run in parallel" as part of three-layer hybrid search
- `README.md` — "Prefix keyword matching": FTS5 queries use wildcard suffixes
- `README.md` — "FTS5 Keyword" engine: "43 hits" in web benchmark, "24 hits" in MCP benchmark

### Context (why) ✅
- `README.md` — "ArcRift captures your AI conversations, extracts structured facts into a knowledge graph"
- `README.md` — Conversations saved with project context, timestamps, platform attribution
- `README.md` — MCP tools: `store_memory` saves "decisions and context", `get_project_summary` returns "structured knowledge graph summary"

### Time-travel ❌
- Not mentioned in README — no git-like versioning, branching, or rollback features

### Schema fields = 7 ❌
- Cannot verify from README alone — requires source inspection

---

## Search & Retrieval

### Full-text ✅
- `README.md` — "FTS5 with Porter stemmer" in tech stack
- `README.md` — Keyword engine documented in both web and MCP benchmarks

### Semantic ✅
- `README.md` — "Sentence vectors" and "Chunk vectors" with nomic-embed-text (768-dim)
- `README.md` — HyDE (Hypothetical Document Embedding) for improved recall
- `README.md` — Recall@1 of 90% in web benchmarks

### Search modes = 2 (user claim) / 3 (actual) ✅
- `README.md` — Three engines: (1) sentence vector, (2) chunk vector, (3) FTS5 keyword — run in parallel and fused
- User claimed 2, but README documents 3 search modes

### Hybrid search ✅ (not in submitted claims, but in README)
- `README.md` — "Three-Layer Hybrid Search: Sentence vectors, chunk vectors, and FTS5 keyword search run in parallel. Results are fused and ranked by a combined score."

---

## Knowledge Lifecycle

### Supersede/replace ✅
- `README.md` — `prune_memory` tool: "Surgically removes facts or chunks matching a description"
- `README.md` — "Delete-then-insert for vector updates": "ArcRift uses a delete-then-insert pattern to avoid UNIQUE constraint errors when re-saving a conversation"

### Explicit forget ✅
- `README.md` — `prune_memory`: "Corrects outdated information without wiping an entire project"
- `README.md` — "Knowledge Graph Pruning" in v1.5.3 changelog: "Click a node in the graph to prune it instantly"

---

## Extraction Pipeline

### Auto-extraction ✅
- `README.md` — "Auto-Connect: Once a session is active, ArcRift re-attaches automatically on every page load"
- `README.md` — Knowledge graph extraction: "Every saved conversation is processed to extract subject-relation-object triples"
- `README.md` — Background indexing: "Sentence-level embedding is offloaded to a background job queue so Save is instant"

### Deduplication ✅
- `README.md` — "FNV-1a Deduplication: Identical conversation segments are fingerprinted and skipped — re-saving a chat never creates duplicate embeddings"

### Narrative ❌
- Not mentioned in README

### Recurrence ❌
- Not mentioned in README

---

## Platform Support

### Claude Code ✅
- `README.md` — MCP setup section: `claude mcp add ArcRift node /path/to/ARCRIFT/backend/dist/mcp/server.js`
- `README.md` — Browser extension supports Claude web interface

### Cursor ✅
- `README.md` — MCP setup section: documented `.cursor/mcp.json` config

### OpenAI Codex ❌
- Not mentioned in README

### OpenCode ❌
- Not mentioned in README

### Windsurf ✅ (not in submitted claims, but in README)
- `README.md` — MCP setup section: documented `.windsurf/mcp.json` config

### GitHub Copilot ❌
- Not mentioned as MCP target — browser extension supports Copilot web interface only

### Gemini ❌ (as IDE tool)
- Browser extension supports Gemini web, but no Gemini CLI integration documented

---

## Claims NOT verified from public README

These are claimed by the submitter but have **no citation in the public README**:

| Claim | Status | Note |
|-------|--------|------|
| time-travel | ❌ no citation | No git-like versioning, branching, or rollback documented |
| schemaFields=7 | ❌ no citation | Cannot verify from README alone |
| narrative | ❌ no citation | Not documented |
| recurrence | ❌ no citation | Not documented |
| export | ❌ no citation | Not documented — though SQLite file is inherently exportable |
| OpenCode support | ❌ not mentioned | Not in README |
| Codex support | ❌ not mentioned | Not in README |
| Copilot IDE support | ❌ not mentioned | Extension supports Copilot web only |

---

## Notable: Not in submitted claims but present in README

| Feature | Detail |
|---------|--------|
| **Hybrid search** | Three-layer: sentence + chunk + keyword, fused and ranked |
| **Search modes = 3** | Not 1 (data.js) or 2 (user claim) — actually 3 distinct engines |
| **Windsurf support** | `.windsurf/mcp.json` config documented |
| **Deduplication** | FNV-1a fingerprinting |
| **Benchmarks** | Comprehensive: R@1=90%, MRR=0.806, context compression=95%, graph stress audit, project isolation audit |
| **Injection defence** | 10 known prompt injection patterns scanned |
| **HyDE** | Hypothetical Document Embedding for improved recall |
| **Small-to-big retrieval** | Sentence-level precision with paragraph-level context |
| **Dead letter queue** | Failed jobs retried 5× with exponential backoff |
