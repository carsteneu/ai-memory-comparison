# MoltBrain — Evidence

> Every ✅ claim backed by public source code or documentation.
> Lines may shift; permalinks use `main` for readability. For permanent citations, pin to a commit hash.

## URL correction

- **Claimed:** `https://github.com/greenrobot-de/moltbrain` (404)
- **Actual:** `https://github.com/nhevers/MoltBrain`

---

## Data Model

### schemaFields ✅ (but 17, not 4)

- `schemas/observation.schema.json` — 17 properties: `id`, `session_id`, `type`, `title`, `subtitle`, `narrative`, `facts`, `concepts`, `files_read`, `files_modified`, `project`, `prompt_number`, `created_at`, `created_at_epoch`, `tokens_used`, `is_favorite`, `tags`
- Claimed 4 fields; actual observation schema has 17 fields.

### Offline ✅

- README.md — SQLite + ChromaDB on local disk; worker at `http://localhost:37777`
- Settings in `~/.moltbrain/settings.json` — no cloud dependency for core function

### Privacy ✅

- README.md — local-first architecture; data stored in `~/.moltbrain/`
- Storage dapp (paid cloud) is optional, separate from local memory

### Time-travel ✅

- README.md — `/api/timeline?project=my-app&days=7` endpoint
- `schemas/observation.schema.json` — `created_at` (ISO 8601) and `created_at_epoch` (Unix ms) on every observation

### p_claude ✅

- README.md — Claude Code integration section with plugin marketplace install
- `.claude-plugin/` directory in repository tree
- Topics: `claude`, `claude-code`

### Narrative ⚠️ (claimed absent, but PRESENT)

- `schemas/observation.schema.json` — `narrative` field: "Detailed narrative of what happened"
- Claimed absent in user's list; actually a first-class schema field

---

## Search & Retrieval

### Full-text ✅

- README.md — `moltbrain search <q>` CLI command
- README.md — `/api/search?q=authentication` REST endpoint

### Search modes (2) ✅

- README.md — Semantic search via ChromaDB (vector similarity)
- README.md — Full-text search via SQLite / search API
- Two distinct modes confirmed: semantic + fulltext

### Semantic ⚠️ (claimed absent, but PRESENT)

- README.md architecture diagram — ChromaDB: "Semantic similarity matching"
- README.md features — "Smart Search: Semantic search via MCP tools finds context"

### Timeline ⚠️ (claimed absent, but PRESENT)

- README.md — `/api/timeline?project=my-app&days=7` endpoint
- README.md — "Web Viewer: Timeline view"

### Hybrid search ❌

- README.md — semantic and fulltext are separate paths; no unified hybrid/BM25+vector fusion endpoint documented

### Deep search ❌

- Not documented in README or API section

### Code graph ❌

- Not documented; no tree-sitter or AST analysis mentioned

### Docs search ❌

- Not documented; no documentation ingestion or search

### Fact metadata query ❌

- Not documented; no entity/action/keyword metadata query

### Data sources (2) ✅

- README.md — SQLite (observations, sessions, summaries)
- README.md — ChromaDB (vector embeddings)
- Two data stores; no code graph or docs index

---

## Knowledge Lifecycle

### Supersede ❌

- No supersede mechanism in README or observation schema
- No `supersedes` field, no version chaining documented

### Explicit forget ❌

- Only `moltbrain prune` (age-based cleanup) via `MOLTBRAIN_PRUNE_DAYS` setting
- No targeted delete/forget of individual observations documented

### Auto-extract ⚠️ (claimed absent, but PRESENT)

- README.md "How It Works" — PostToolUse hook: "Capture output, extract facts"
- README.md "What It Does" — Auto-captures discoveries, decisions & code
- README.md — Stop hook: "Generate summary"
- README.md features — "Observations: Auto-captures discoveries, decisions & code"

### Decay ❌

- Not documented; prune is age-based bulk cleanup, not per-item decay

### Contradiction detection ❌

- Not documented

### Quarantine ❌

- Not documented

### Auto-resolve ❌

- Not documented

### Trust model ❌

- Not documented

### Content preprocessing ❌

- Not documented

### Dedup ❌

- Not documented

### Quality refinement ❌

- Not documented

### Clustering ❌

- Not documented

### Recurrence tracking ❌

- Not documented

---

## Metadata & Organization

### Entities ❌

- Not documented; observation schema has `concepts` (tag-like) and `files_read`/`files_modified` but no entity junction table
- No explicit entity linking or relationship edges

### Actions ❌

- Not documented

### Keywords ❌

- Not documented as a distinct field; `concepts` and `tags` exist but are untyped

### Anticipated queries ❌

- Not documented

### Trigger rules ❌

- Not documented

### Domain tag ❌

- Not documented; `project` field exists but no domain classification

### Task type ❌

- `schemas/observation.schema.json` — `type` enum: `discovery`, `decision`, `implementation`, `issue`, `learning`, `reference`
- These are observation types, not task tracking (no `task`, `idea`, `blocked`, `stale`)

### Context (why/metadata) ❌

- Not documented as a distinct field; `narrative` serves a different purpose

### Source attribution ❌

- Not documented; no `source`, `origin_tool`, or provenance tracking

### Origin trust ❌

- Not documented

### Emotional ❌

- Not documented

### Conflict surfacing ❌

- Not documented

---

## UI & Multi-Agent

### Web UI ⚠️ (claimed absent, but PRESENT)

- README.md — "Web Viewer: Browse history at localhost:37777"
- README.md features — Web Viewer with timeline, search, analytics, themes, keyboard shortcuts
- README.md — "Full keyboard navigation in the web viewer"

### Multi-agent ⚠️ (claimed absent, but PRESENT)

- README.md — MoltBook integration: "social network for AI agents! Share memories, learn from other agents, and build collective knowledge"
- README.md — x402 micropayment storage dapp with per-wallet vaults for agents
- README.md — Virtuals Protocol integration for multi-agent Game SDK

### Persona ❌

- Not documented

---

## Platform Support

### p_claude ✅ (see Data Model above)

### p_openclaw ✅

- README.md — OpenClaw integration: extension, skill, and MCP server
- README.md — `pnpm openclaw plugins enable moltbrain`

### p_moltbook ✅

- README.md — MoltBook MCP integration with `@moltbrain/moltbook-mcp`

---

## Benchmark score: 13/47 ✅ (claims verified)

### User claims CORRECT (10):
offline, privacy, timeTravel, fulltext, searchModes=2, p_claude, p_openclaw, p_moltbook (implicit), explicitForget (absent ✅), supersede (absent ✅)

### User claims INCORRECT (6):
- `schemaFields=4` → actual: 17
- `webUi` absent → present (web viewer at localhost:37777)
- `multiAgent` absent → present (MoltBook + Virtuals Protocol)
- `narrative` absent → present in observation schema
- `semantic` absent → present (ChromaDB)
- `timeline` absent → present (timeline API + web viewer)
- `autoExtract` absent → present (PostToolUse + Stop hooks)

### Correctly identified as ABSENT (31):
entities, actions, keywords, anticipatedQueries, triggerRules, domainTag, taskType, context, source, originTrust, emotional, conflict, layeredMemory, hybrid, deep, codeGraph, docsSearch, factQuery, decay, contradiction, quarantine, autoResolve, trustModel, contentPreproc, dedup, qualityRefine, clustering, recurrence, persona

> **Note:** `supersede` and `explicitForget` are correctly claimed absent. `autoExtract`, `narrative`, `semantic`, `timeline` are incorrectly claimed absent.

---

*Evidence date: 2026-05-28. Source: README.md and observation.schema.json from `https://github.com/nhevers/MoltBrain` (main branch).*

evidence: "https://github.com/carsteneu/ai-memory-comparison/blob/main/evidence/moltbrain.md"
