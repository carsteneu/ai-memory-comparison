# [System Name] — Evidence

> **Instructions:** Go through every feature below. For each ✅, provide a public source link (README, docs, source code file + line).
> For each ❌, just leave the ❌ — no source needed.
> Fill in the metadata header first (description, deployment, storage, etc.).
> When done, submit the PR with just this file. The maintainers will create the data.js entry.

**Repo:** `[org/repo]` (e.g. `github.com/user/repo`)
**Stars:** [number]  
**Language:** [language]  
**License:** [SPDX identifier]  
**Created:** [YYYY-MM-DD]  
**Description:** [one-line description of what the system does]  

---

## System Metadata

These describe *how* the system is deployed and used — one or two words each, not ✅/❌.

| Field | Value |
|-------|-------|
| **Deployment** | `[Local CLI / Library / Self-host / Cloud / Plugin / ...]` |
| **Storage** | `[SQLite / Postgres / Vector DB / ...]` |
| **Integration** | `[MCP / Hooks / SDK / API / CLI / Plugin / ...]` |
| **Single binary?** | `[yes / no]` |
| **Setup** | `[pip install / brew install / npx install / go install / ...]` |
| **Pricing** | `[free / freemium / paid / ...]` |
| **Storage unit** | `[Memory (text) / Observation / Chunk / ...]` |

---

## Architecture

### Proxy ✅ / ❌
> Intercepts and modifies the LLM conversation stream in-flight (context collapsing, prompt injection). Not MCP or hooks.
- Source: `[file:line]` — [evidence description]

### Web/TUI ✅ / ❌
> Ships a visual interface accessible in a browser or terminal.
- Source: `[file:line]` — [evidence description]

### Offline ✅ / ❌
> Core memory functionality works without internet connection.
- Source: `[file:line]` — [evidence description]

### Multi-agent ✅ / ❌
> Supports cross-agent memory sharing, agent directory, or inter-agent communication.
- Source: `[file:line]` — [evidence description]

### LLM providers (count: __) ✅
> Count of distinct embedding/LLM providers supported.
- Source: `[file:line]` — [evidence description / provider list]

### Cache optimization ✅ / ❌
> Caches intermediate results (embeddings, search results) for performance.
- Source: `[file:line]` — [evidence description]

### Procedural memory ✅ / ❌
> Stores and executes reusable scripts/code at retrieval time (not just data).
- Source: `[file:line]` — [evidence description]

### Sandboxed execution ✅ / ❌
> Executes user-provided code in a sandboxed environment.
- Source: `[file:line]` — [evidence description]

### Scheduled/autonomous ✅ / ❌
> Can run scheduled tasks or autonomous operations without user prompt.
- Source: `[file:line]` — [evidence description]

### Privacy/encrypt ✅ / ❌
> Data encryption at rest or in transit, self-hosting, zero-telemetry.
- Source: `[file:line]` — [evidence description]

### Data export ✅ / ❌
> Built-in export functionality (JSON, Markdown, etc.).
- Source: `[file:line]` — [evidence description]

---

## Data Model

### Entities ✅ / ❌
> Structured extraction of named entities (files, people, systems, packages) as separate fields or tables.
- Source: `[file:line]` — [evidence description]

### Actions ✅ / ❌
> Stores commands, operations, or tool calls as separate structured fields.
- Source: `[file:line]` — [evidence description]

### Keywords/tags ✅ / ❌
> Explicit keyword or tag system for categorizing stored items.
- Source: `[file:line]` — [evidence description]

### Anticipated queries ✅ / ❌
> Generates predicted search queries for each memory entry to improve retrieval recall.
- Source: `[file:line]` — [evidence description]

### Trigger rules ✅ / ❌
> Condition-based activation (e.g. "show this when file X is opened", deadlines).
- Source: `[file:line]` — [evidence description]

### Domain tag ✅ / ❌
> Tags memories with domain categories (code, marketing, legal, finance, general).
- Source: `[file:line]` — [evidence description]

### Task type ✅ / ❌
> Classifies unfinished work by type (task, idea, blocked, stale).
- Source: `[file:line]` — [evidence description]

### Context (why) ✅ / ❌
> Stores *why* a memory is relevant alongside the content.
- Source: `[file:line]` — [evidence description]

### Source attribution ✅ / ❌
> Records who/what authored the memory (user, agent, pipeline) with ≥3 distinct levels.
- Source: `[file:line]` — [evidence description]

### Origin + trust ✅ / ❌
> Different trust weights based on capture method (user > agent > automated).
- Source: `[file:line]` — [evidence description]

### Emotional ✅ / ❌
> Tracks sentiment or emotional intensity per memory or session.
- Source: `[file:line]` — [evidence description]

### Conflict surfacing ✅ / ❌
> Detects and surfaces conflicting information between memories.
- Source: `[file:line]` — [evidence description]

### Layered memory ✅ / ❌
> Hierarchical memory organization (e.g. L0 raw → L1 summary → L2 persona).
- Source: `[file:line]` — [evidence description]

### Time-travel ✅ / ❌
> Historical state queries (past sessions, superseded versions, temporal search).
- Source: `[file:line]` — [evidence description]

### Schema fields (count: __) ✅
> Count of distinct structured fields per memory entry (exclude auto IDs/timestamps).
- Source: `[file:line]` — [evidence description / count justification]

---

## Search & Retrieval

### Full-text ✅ / ❌
> Keyword-based search (FTS5, BM25, grep, or equivalent).
- Source: `[file:line]` — [evidence description]

### Semantic/vector ✅ / ❌
> Embedding-based semantic search.
- Source: `[file:line]` — [evidence description]

### Hybrid (BM25+Vec) ✅ / ❌
> Combines full-text and vector search with result fusion (e.g. RRF).
- Source: `[file:line]` — [evidence description]

### Deep (incl. thinking) ✅ / ❌
> Search includes model thinking/reasoning traces.
- Source: `[file:line]` — [evidence description]

### Code graph ✅ / ❌
> Indexes and queries code structure (Tree-sitter, AST, or equivalent).
- Source: `[file:line]` — [evidence description]

### Docs search ✅ / ❌
> Dedicated search across ingested framework/API documentation.
- Source: `[file:line]` — [evidence description]

### Fact metadata query ✅ / ❌
> Structured queries on memory metadata (e.g. "all unfinished tasks in project X").
- Source: `[file:line]` — [evidence description]

### Timeline view ✅ / ❌
> Chronological browsing or temporal search (since/before parameters).
- Source: `[file:line]` — [evidence description]

### Search modes (count: __) ✅
> Count of distinct search tools/modes available.
- Source: `[file:line]` — [evidence description / mode names]

### Data sources (count: __) ✅
> Count of distinct data types searchable (learnings, messages, code, docs, etc.).
- Source: `[file:line]` — [evidence description / source names]

---

## Knowledge Lifecycle

### Decay/forgetting ✅ / ❌
> Automatically reduces relevance or removes memories based on time or disuse.
- Source: `[file:line]` — [evidence description]

### Supersede/replace ✅ / ❌
> Mechanism to mark one memory as replacing another, with traceable chain.
- Source: `[file:line]` — [evidence description]

### Contradiction detection ✅ / ❌
> Automatically detects new memories contradicting existing ones.
- Source: `[file:line]` — [evidence description]

### Quarantine ✅ / ❌
> Can exclude a session's memories from retrieval without deleting them.
- Source: `[file:line]` — [evidence description]

### Auto-resolution ✅ / ❌
> Automatically resolves or archives stale items (e.g. unfinished tasks after TTL).
- Source: `[file:line]` — [evidence description]

### Trust model ✅ / ❌
> Multi-tier trust hierarchy where some sources override others.
- Source: `[file:line]` — [evidence description]

### Explicit forget ✅ / ❌
> User or agent can explicitly delete/forget a specific memory or session.
- Source: `[file:line]` — [evidence description]

---

## Extraction Pipeline

### Auto-extraction ✅ / ❌
> Automatically extracts structured knowledge from sessions without manual `save` calls.
- Source: `[file:line]` — [evidence description]

### Content-aware preprocessing ✅ / ❌
> Truncates or filters content by type before extraction (code vs. text differently).
- Source: `[file:line]` — [evidence description]

### Deduplication ✅ / ❌
> Detects and merges duplicate or near-duplicate memories.
- Source: `[file:line]` — [evidence description]

### Quality refinement ✅ / ❌
> LLM or rule-based quality pass after initial extraction (confidence, contradiction check).
- Source: `[file:line]` — [evidence description]

### Narrative generation ✅ / ❌
> Generates session summaries, handover narratives, or project profiles.
- Source: `[file:line]` — [evidence description]

### Clustering ✅ / ❌
> Groups related memories by topic, embedding similarity, or semantic relationship.
- Source: `[file:line]` — [evidence description]

### Recurrence detection ✅ / ❌
> Detects recurring patterns across sessions (same bug, repeated question).
- Source: `[file:line]` — [evidence description]

### Persona extraction ✅ / ❌
> Extracts user traits, preferences, or working style into a persistent persona model.
- Source: `[file:line]` — [evidence description]

---

## Platform Support

For each platform: ✅ if documented integration exists (MCP, hooks, plugin, skill, or SDK).

### Claude Code ✅ / ❌
- Source: `[file:line]` — [evidence description]

### Codex ✅ / ❌
- Source: `[file:line]` — [evidence description]

### OpenCode ✅ / ❌
- Source: `[file:line]` — [evidence description]

### Gemini CLI ✅ / ❌
- Source: `[file:line]` — [evidence description]

### Copilot ✅ / ❌
- Source: `[file:line]` — [evidence description]

### Cursor ✅ / ❌
- Source: `[file:line]` — [evidence description]

### Windsurf ✅ / ❌
- Source: `[file:line]` — [evidence description]

### OpenClaw ✅ / ❌
- Source: `[file:line]` — [evidence description]

### Hermes ✅ / ❌
- Source: `[file:line]` — [evidence description]

### pi/omp ✅ / ❌
- Source: `[file:line]` — [evidence description]

### Antigravity ✅ / ❌
- Source: `[file:line]` — [evidence description]

---

## Benchmarks

### LoCoMo ✅ / ❌
> Published score on the LoCoMo long-conversation memory benchmark.
- Score: `[score or —]`
- Source: `[file:line]` — [evidence description]

### LongMemEval ✅ / ❌
> Published score on LongMemEval(-S) benchmark.
- Score: `[score or —]`
- Source: `[file:line]` — [evidence description]

### PersonaMem ✅ / ❌
> Published score on PersonaMem benchmark.
- Score: `[score or —]`
- Source: `[file:line]` — [evidence description]

### Token reduction ✅ / ❌
> Published token savings compared to a defined baseline.
- Score: `[percentage or —]`
- Source: `[file:line]` — [evidence description]

### Methodology open ✅ / ❌
> Benchmark methodology is publicly documented and reproducible.
- Source: `[file:line]` — [evidence description]

---

> **Next steps:** Delete this instruction block and submit the PR. Maintainers will create the data.js entry from this evidence file.
