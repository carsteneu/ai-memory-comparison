# Coverage Criteria

What each feature means, and what a system must demonstrate to earn the ✅.

> **Rule:** If a feature isn't documented in the project's public README, docs, or source code, it's marked `—` (not present). No assumptions, no inferences.
> **Corrections:** Open a PR with a link to the public source proving the feature.

---

## Vital Signs

| Feature | ✅ Criterion |
|---|---|
| **Single binary** | Ships as a single executable file. No runtime dependency on Node.js, Python, Docker, or external services. |
| **Coverage** | Automatically computed: percentage of all Boolean features below that this system implements. Displayed as `XX%`. |

---

## Architecture

| Feature | ✅ Criterion |
|---|---|
| **Deployment** | Described in README. |
| **Storage** | Described in README. |
| **Integration** | Described integration method with coding agents (MCP server, REST API, hooks, plugin, CLI, SDK, or skill). |
| **Proxy** | Intercepts and modifies the LLM conversation stream in-flight (e.g., context collapsing, prompt injection). Not the same as an MCP server or hook system. |
| **Web/TUI** | Ships a visual interface accessible in a browser or terminal. |
| **Offline** | Core memory functionality works without any internet connection. |
| **Multi-agent** | Supports coordination between multiple agents (shared memory, agent registry/directory, inter-agent communication, or parallel agent orchestration). |
| **LLM providers** | Number of distinct LLM provider backends supported (Anthropic, OpenAI, Google, DeepSeek, etc.). Count embedding providers only when they are first-class selectable backends. |
| **Cache optimization** | Has prompt cache optimization, context collapse prevention, or token-saving mechanisms (e.g., Sawtooth freeze, cache keepalive, fingerprint-based cache invalidation). |
| **Procedural memory** | Stores user-defined executable tools, workflows, or scripts that persist across sessions (Caps, Hooks, Skills). Not the same as session history or declarative knowledge. |
| **Sandboxed exec** | Can execute code or tools in a sandboxed environment with resource limits (CPU, memory, network) and security boundaries. |
| **Scheduled/autonomous** | Has a scheduler or daemon for autonomous task execution (cron, interval-based, background daemon). Must persist across restarts and run without manual triggering. |
| **Privacy/encrypt** | Has explicit privacy features (local-only storage, PII redaction, telemetry opt-out, content encryption, or confidential computing). |
| **Data export** | Can export or back up memory data in a structured, reusable format (Markdown, JSON, archive, or filesystem mirror). |
| **Setup** | Setup method is described. |
| **Pricing** | Pricing model is described.

---

## Data Model

| Feature | ✅ Criterion |
|---|---|
| **Entities** | Extracts or stores named entities (files, people, systems, packages) as separate structured fields or database tables, not just free-text mentions. |
| **Actions** | Extracts or stores commands, operations, or tool calls as separate structured fields. |
| **Keywords/tags** | Explicit keyword or tag system for categorizing stored items. |
| **Anticipated queries** | Generates predicted search queries for each memory entry to improve retrieval recall. |
| **Trigger rules** | Supports condition-based activation (e.g., "show this memory when file X is opened", deadline-based triggers). |
| **Domain tag** | Tags memories with domain categories (code, marketing, legal, finance, general). |
| **Task type** | Classifies unfinished work by type (task, idea, blocked, stale). |
| **Context (why)** | Stores the reason *why* a memory is relevant, alongside the memory content itself. |
| **Source attribution** | Records who/what authored the memory (user, agent, extraction pipeline) with at least 3 distinct source levels. |
| **Origin + trust** | Assigns different trust weights based on how the memory was captured (user input > agent suggestion > automated extraction). |
| **Emotional** | Tracks sentiment or emotional intensity per memory or session. |
| **Conflict surfacing** | Detects and surfaces conflicting information (e.g., two memories contradict each other). |
| **Layered memory** | Organizes memories in a hierarchical structure (e.g., L0 raw → L1 summary → L2 persona/semantic). |
| **Time-travel** | Supports querying or browsing historical state (past sessions, superseded versions, or temporal search). |
| **Schema fields** | Approximate count of distinct structured fields per memory entry (entities, actions, keywords, metadata — not including auto-generated IDs/timestamps). |

---

## Search & Retrieval

| Feature | ✅ Criterion |
|---|---|
| **Full-text** | Keyword-based search (FTS5, BM25, grep, or equivalent). |
| **Semantic/vector** | Embedding-based semantic search. |
| **Hybrid (BM25+Vec)** | Combines full-text and vector search with result fusion (e.g., Reciprocal Rank Fusion). |
| **Deep (incl. thinking)** | Search includes model thinking/reasoning traces, not just final outputs. |
| **Code graph** | Indexes and queries code structure (Tree-sitter, AST, or equivalent) — not just file contents. |
| **Docs search** | Dedicated documentation search across ingested framework/API docs. |
| **Fact metadata query** | Structured queries on memory metadata (e.g., "all unfinished tasks in project X", "all decisions about Y"). |
| **Timeline view** | Chronological browsing or temporal search (`since`/`before` parameters, timeline tool). |
| **Search modes** | Count of distinct search tools/modes available. |
| **Data sources** | Count of distinct data types that can be searched (e.g., learnings, messages, code, docs). |

---

## Knowledge Lifecycle

| Feature | ✅ Criterion |
|---|---|
| **Decay/forgetting** | Automatically reduces relevance or removes memories based on time, disuse, or engagement signals. Must be automatic, not manual. |
| **Supersede/replace** | Explicit mechanism to mark one memory as replacing/updating another, with a traceable chain. |
| **Contradiction detect** | Automatically detects when a new memory contradicts an existing one. |
| **Quarantine** | Can exclude a session's memories from retrieval without deleting them. |
| **Auto-resolution** | Automatically resolves or archives stale items (e.g., unfinished tasks after a TTL). |
| **Trust model** | Multi-tier trust hierarchy where some sources override others (e.g., user > agent > extracted). |
| **Explicit forget** | User or agent can explicitly delete/forget a memory or session. |

---

## Extraction Pipeline

| Feature | ✅ Criterion |
|---|---|
| **Auto-extraction** | Automatically extracts structured knowledge from sessions without manual `save` calls. |
| **Content-aware preproc** | Truncates or filters content by type before extraction (e.g., limiting pasted code vs. natural text differently). |
| **Deduplication** | Detects and merges duplicate or near-duplicate memories. |
| **Quality refinement** | LLM-based or rule-based quality pass after initial extraction (confidence scoring, contradiction checking). |
| **Narrative generation** | Generates session summaries, handover narratives, or project profiles. |
| **Clustering** | Groups related memories by topic, embedding similarity, or semantic relationship. |
| **Recurrence detection** | Detects recurring patterns across sessions (same bug, repeated question, recurring topic). |
| **Persona extraction** | Extracts user traits, preferences, or working style into a persistent persona model. |

---

## Platform Support

| Feature | ✅ Criterion |
|---|---|
| **Claude Code** | Documented integration with Claude Code (MCP, hooks, plugin, or skill). |
| **Codex** | Documented integration with OpenAI Codex CLI. |
| **OpenCode** | Documented integration with OpenCode. |
| **Gemini CLI** | Documented integration with Google Gemini CLI. |
| **Copilot** | Documented integration with GitHub Copilot CLI. |
| **Cursor** | Documented integration with Cursor IDE. |
| **Windsurf** | Documented integration with Windsurf IDE. |
| **OpenClaw** | Documented integration with OpenClaw gateway. |
| **Hermes** | Documented integration with Nous Research Hermes. |
| **pi/omp** | Documented integration with pi or Oh My Pi. |
| **Antigravity** | Documented integration with Antigravity CLI. |

---

## Benchmarks

| Feature | ✅ Criterion |
|---|---|
| **LoCoMo** | Published score on the LoCoMo long-conversation memory benchmark, with methodology. Claims without published numbers or reproduction steps are marked `—`. |
| **LongMemEval** | Published score on LongMemEval(-S) benchmark. |
| **PersonaMem** | Published score on PersonaMem benchmark. |
| **Token reduction** | Published token savings compared to a defined baseline (e.g., full context). |
| **Methodology open** | Benchmark methodology is publicly documented and reproducible (scripts, dataset links, configuration). Claims without reproduction steps are not considered "methodology open". |

---

## Contributing

1. A feature is marked `—` unless publicly documented. If your project has the feature but it's not in the README/docs: document it first, then open a PR.
2. Gray areas: open an issue. The criteria above define the default interpretation.
3. Disagree with a criterion? PR to this file with reasoning.
