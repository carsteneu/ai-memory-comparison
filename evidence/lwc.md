# LWC — Evidence

**Repo:** `github.com/JanYork/llm-wiki-cli`
**Stars:** 32
**Language:** Rust
**License:** Apache-2.0
**Created:** 2026-07-29
**Description:** Agent-driven proactive memory CLI that maintains persistent, source-grounded Wiki knowledge across sessions.

---

## System Metadata

| Field | Value |
|-------|-------|
| **Deployment** | `Local CLI` |
| **Storage** | `SQLite` |
| **Integration** | `CLI / MCP / Hooks / Skill` |
| **Single binary?** | `yes` |
| **Setup** | `brew / npm / cargo install` |
| **Pricing** | `free` |
| **Storage unit** | `Source / Wiki page` |

---

## Architecture

### Proxy ❌
> Intercepts and modifies the LLM conversation stream in-flight (context collapsing, prompt injection). Not MCP or hooks.

### Web/TUI ✅
> Ships a visual interface accessible in a browser or terminal.
- Source: [README.md:759-765](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L759-L765) — `lwc view` starts a loopback-only browser inspector backed by an embedded Lit application.

### Offline ✅
> Core memory functionality works without internet connection.
- Source: [README.md:134-153](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L134-L153) — The core is a local Rust CLI with canonical SQLite storage and rebuildable local Markdown.
- Source: [README.md:891-906](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L891-L906) — The core has no built-in LLM calls, vector database, daemon, or background service.

### Multi-agent ❌
> Supports cross-agent memory sharing, agent directory, or inter-agent communication.

### LLM providers (count: 0) ✅
> Count of distinct embedding/LLM providers supported.
- Source: [README.md:891-906](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L891-L906) — LWC explicitly has no built-in LLM calls or vector database, so the provider count is zero.

### Cache optimization ❌
> Caches intermediate results (embeddings, search results) for performance.

### Procedural memory ❌
> Stores and executes reusable scripts/code at retrieval time (not just data).

### Sandboxed execution ❌
> Executes user-provided code in a sandboxed environment.

### Scheduled/autonomous ❌
> Can run scheduled tasks or autonomous operations without user prompt.

### Privacy/encrypt ✅
> Data encryption at rest or in transit, self-hosting, zero-telemetry.
- Source: [README.md:759-765](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L759-L765) — The browser inspector is foreground, loopback-only, CDN-free, and read-only.
- Source: [README.md:781-785](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L781-L785) — Optional CodeGraph telemetry is always off and its state remains local.

### Data export ✅
> Built-in export functionality (JSON, Markdown, etc.).
- Source: [README.md:150-153](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L150-L153) — Canonical SQLite knowledge is projected into a rebuildable Markdown tree.
- Source: [README.md:843-845](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L843-L845) — `maintenance materialize` rebuilds the projected Markdown tree.

---

## Data Model

### Entities ✅
> Structured extraction of named entities (files, people, systems, packages) as separate fields or tables.
- Source: [src/cli/definitions.rs:1233-1239](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/src/cli/definitions.rs#L1233-L1239) — Wiki pages have a structured `kind`, including the documented `entity` kind.
- Source: [docs/agent-workflow.md:170-187](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/docs/agent-workflow.md#L170-L187) — The ingest workflow explicitly creates or revises entity pages as compiled knowledge.

### Actions ✅
> Stores commands, operations, or tool calls as separate structured fields.
- Source: [src/store/schema.rs:105-110](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/src/store/schema.rs#L105-L110) — The operations table stores `action`, `target`, and structured detail JSON separately.

### Keywords/tags ✅
> Explicit keyword or tag system for categorizing stored items.
- Source: [README.md:431-441](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L431-L441) — Strong tags associate named tags with pages and support bounded tag loading.

### Anticipated queries ❌
> Generates predicted search queries for each memory entry to improve retrieval recall.

### Trigger rules ✅
> Condition-based activation (e.g. "show this when file X is opened", deadlines).
- Source: [README.md:431-441](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L431-L441) — `tag autoload` activates bounded full-page memory at Agent session boundaries.

### Domain tag ❌
> Tags memories with domain categories (code, marketing, legal, finance, general).

### Task type ❌
> Classifies unfinished work by type (task, idea, blocked, stale).

### Context (why) ✅
> Stores *why* a memory is relevant alongside the content.
- Source: [src/store/schema.rs:56-78](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/src/store/schema.rs#L56-L78) — Tag policies and page-tag memberships persist both priority and a required reason alongside the associated page.

### Source attribution ✅
> Records who/what authored the memory (user, agent, pipeline) with ≥3 distinct levels.
- Source: [README.md:574-593](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L574-L593) — Pages distinguish source-grounded, user-provided, agent-observed, and hypothesis provenance.

### Origin + trust ❌
> Different trust weights based on capture method (user > agent > automated).

### Emotional ❌
> Tracks sentiment or emotional intensity per memory or session.

### Conflict surfacing ❌
> Detects and surfaces conflicting information between memories.

### Layered memory ✅
> Hierarchical memory organization (e.g. L0 raw → L1 summary → L2 persona).
- Source: [README.md:142-153](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L142-L153) — The persistent model has raw immutable sources, an Agent-maintained Wiki, and schema/purpose policy layers.

### Time-travel ✅
> Historical state queries (past sessions, superseded versions, temporal search).
- Source: [README.md:482-503](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L482-L503) — Source history reports superseded revisions and supports diffs between immutable snapshots.

### Schema fields (count: 8) ✅
> Count of distinct structured fields per memory entry (exclude auto IDs/timestamps).
- Source: [src/store/types.rs:379-390](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/src/store/types.rs#L379-L390) — A Wiki page has eight non-timestamp fields: slug, title, kind, summary, body, source IDs, provenance, and links.

---

## Search & Retrieval

### Full-text ✅
> Keyword-based search (FTS5, BM25, grep, or equivalent).
- Source: [README.md:697-724](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L697-L724) — Search is lexical and deterministic, with CJK bigrams, Latin tokenization, field scoring, and exact score explanations.

### Semantic/vector ❌
> Embedding-based semantic search.

### Hybrid (BM25+Vec) ❌
> Combines full-text and vector search with result fusion (e.g. RRF).

### Deep (incl. thinking) ❌
> Search includes model thinking/reasoning traces.

### Code graph ✅
> Indexes and queries code structure (Tree-sitter, AST, or equivalent).
- Source: [README.md:781-815](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L781-L815) — Optional project CodeGraph indexes source files and exposes query, node, callers, callees, impact, and file operations.

### Docs search ❌
> Dedicated search across ingested framework/API documentation.

### Fact metadata query ✅
> Structured queries on memory metadata (e.g. "all unfinished tasks in project X").
- Source: [docs/agent-workflow.md:96-102](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/docs/agent-workflow.md#L96-L102) — Ingest jobs can be queried by structured status such as `pending`.
- Source: [README.md:595-604](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L595-L604) — Search supports structured type and page-kind filters.

### Timeline view ✅
> Chronological browsing or temporal search (since/before parameters).
- Source: [README.md:821-834](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L821-L834) — `lwc log` browses recent durable operations.
- Source: [README.md:482-503](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L482-L503) — Source status and diff expose ordered revision history.

### Search modes (count: 4) ✅
> Count of distinct search tools/modes available.
- Source: [src/store/types.rs:637-651](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/src/store/types.rs#L637-L651) — Search has four layer modes (`Auto`, `Page`, `Source`, `All`) and separately supports document, passage, sentence, or all granularities.

### Data sources (count: 3) ✅
> Count of distinct data types searchable (learnings, messages, code, docs, etc.).
- Source: [README.md:595-604](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L595-L604) — Search covers compiled Wiki pages and immutable raw sources.
- Source: [README.md:807-815](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L807-L815) — Unified exploration also exposes current project code through CodeGraph, for three source types total.

---

## Knowledge Lifecycle

### Decay/forgetting ❌
> Automatically reduces relevance or removes memories based on time or disuse.

### Supersede/replace ✅
> Mechanism to mark one memory as replacing another, with traceable chain.
- Source: [README.md:482-503](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L482-L503) — File-backed sources retain current/superseded lineage and immutable A→B→A revision observations.

### Contradiction detection ❌
> Automatically detects new memories contradicting existing ones.

### Quarantine ❌
> Can exclude a session's memories from retrieval without deleting them.

### Auto-resolution ❌
> Automatically resolves or archives stale items (e.g. unfinished tasks after TTL).

### Trust model ❌
> Multi-tier trust hierarchy where some sources override others.

### Explicit forget ✅
> User or agent can explicitly delete/forget a specific memory or session.
- Source: [README.md:852-858](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L852-L858) — `source remove` and `page remove` explicitly delete knowledge with citation and backlink guards.

---

## Extraction Pipeline

### Auto-extraction ❌
> Automatically extracts structured knowledge from sessions without manual `save` calls.

### Content-aware preprocessing ❌
> Truncates or filters content by type before extraction (code vs. text differently).

### Deduplication ✅
> Detects and merges duplicate or near-duplicate memories.
- Source: [README.md:461-472](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L461-L472) — Identical source bytes are deduplicated by SHA-256.

### Quality refinement ✅
> LLM or rule-based quality pass after initial extraction (confidence, contradiction check).
- Source: [docs/agent-workflow.md:328-352](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/docs/agent-workflow.md#L328-L352) — `lwc lint` performs deterministic structural quality checks and supplies context for a subsequent semantic review.

### Narrative generation ❌
> Generates session summaries, handover narratives, or project profiles.

### Clustering ❌
> Groups related memories by topic, embedding similarity, or semantic relationship.

### Recurrence detection ❌
> Detects recurring patterns across sessions (same bug, repeated question).

### Persona extraction ❌
> Extracts user traits, preferences, or working style into a persistent persona model.

---

## Platform Support

For each platform: ✅ if documented integration exists (MCP, hooks, plugin, skill, or SDK).

### Claude Code ✅
- Source: [AgentTarget capability matrix:14-17](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/docs/superpowers/specs/2026-08-12-lwc-agent-target-capability-matrix.md#L14-L17) — Claude has documented global and project MCP, Skill, Hook, and Instructions integration.

### Codex ✅
- Source: [AgentTarget capability matrix:18-19](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/docs/superpowers/specs/2026-08-12-lwc-agent-target-capability-matrix.md#L18-L19) — Codex has documented global and project MCP, Skill, Hook, and AGENTS.md integration.

### OpenCode ✅
- Source: [AgentTarget capability matrix:24-25](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/docs/superpowers/specs/2026-08-12-lwc-agent-target-capability-matrix.md#L24-L25) — OpenCode has documented global and project MCP, Skill, plugin Hook, and Instructions integration.

### Gemini CLI ✅
- Source: [AgentTarget capability matrix:28-29](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/docs/superpowers/specs/2026-08-12-lwc-agent-target-capability-matrix.md#L28-L29) — Gemini CLI has documented global and project MCP, Skill, Hook, and GEMINI.md integration.

### Copilot ✅
- Source: [AgentTarget capability matrix:34-39](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/docs/superpowers/specs/2026-08-12-lwc-agent-target-capability-matrix.md#L34-L39) — Copilot VS Code, CLI, and JetBrains have documented supported integrations and explicit unsupported/user-managed surfaces.

### Cursor ✅
- Source: [AgentTarget capability matrix:22-23](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/docs/superpowers/specs/2026-08-12-lwc-agent-target-capability-matrix.md#L22-L23) — Cursor has documented global and project MCP, Skill, Hook, and project Rules integration.

### Windsurf ❌

### OpenClaw ❌

### Hermes ✅
- Source: [AgentTarget capability matrix:26-27](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/docs/superpowers/specs/2026-08-12-lwc-agent-target-capability-matrix.md#L26-L27) — Hermes has documented global MCP, Skill, pre-LLM Hook, and SOUL.md integration, with project limitations explicitly reported.

### pi/omp ✅
- Source: [AgentTarget capability matrix:20-21](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/docs/superpowers/specs/2026-08-12-lwc-agent-target-capability-matrix.md#L20-L21) — Pi has a documented MCP extension bridge, Skill, lifecycle Hook, and injected guidance at global and project scopes.

### Antigravity ✅
- Source: [AgentTarget capability matrix:30-31](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/docs/superpowers/specs/2026-08-12-lwc-agent-target-capability-matrix.md#L30-L31) — Antigravity has documented global and project plugin, MCP, Skill, Hook, and Rules integration.

---

## Benchmarks

### LoCoMo ❌
> Published score on the LoCoMo long-conversation memory benchmark.
- Score: `—`

### LongMemEval ❌
> Published score on LongMemEval(-S) benchmark.
- Score: `—`

### PersonaMem ❌
> Published score on PersonaMem benchmark.
- Score: `—`

### Token reduction ❌
> Published token savings compared to a defined baseline.
- Score: `—`

### Methodology open ✅
> Benchmark methodology is publicly documented and reproducible.
- Source: [README.md:871-889](https://github.com/JanYork/llm-wiki-cli/blob/88d72b7b8b98a74ba645e994d8698f0fbb82e419/README.md#L871-L889) — The public benchmark contract defines local corpus and JSONL ground truth inputs, metrics, environment variables, and the exact command to reproduce it.
