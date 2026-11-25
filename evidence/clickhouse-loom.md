# ClickHouse Loom — Evidence

- **Repo:** [ClickHouse/loom](https://github.com/ClickHouse/loom)
- **Stars:** 221 as of 2026-11-25
- **Language:** Python
- **License:** Apache-2.0
- **Created:** 2026-10-08
- **Description:** Self-hosted shared memory, cited document search, and a structural code index for coding agents.

Evidence is pinned to [v1.3.0](https://github.com/ClickHouse/loom/releases/tag/v1.3.0). The [coding-agent memory guide](https://loom.clickhouse.com/docs/use-cases/agent-memory) describes how to evaluate the workflows. Positive ratings follow the comparison criteria, including the distinction between a documented integration and a completed agent task.

---

## System Metadata

| Field | Value |
|-------|-------|
| **Deployment** | Self-hosted Docker or Kubernetes |
| **Storage** | ClickHouse, with optional PostgreSQL for live memory and knowledge state |
| **Integration** | MCP, HTTP API, hooks, CLI, and SDKs |
| **Single binary?** | No |
| **Setup** | Docker installer or Helm |
| **Pricing** | Free Apache-2.0 software with separate infrastructure and optional provider costs |
| **Storage unit** | Versioned memory with a textual or structured value |

---

## Architecture

### Proxy ❌

### Web/TUI ✅

- Source: [dashboard.md:1–15](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/dashboard.md#L1-L15) — The shipped browser dashboard browses stored records and configures a deployment.

### Offline ✅

- Source: [models-and-keys.md:18–33](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/getting-started/models-and-keys.md#L18-L33) — After the Docker images are pulled, the bundled CPU embedder provides semantic recall without network or model keys. A real local LLM is needed for generated answers or meaningful extraction.

### Multi-agent ✅

- Source: [multi-agent.md:1–26](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/use-cases/multi-agent.md#L1-L26), [tasks-and-decisions.md:17–35](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/tasks-and-decisions.md#L17-L35) — Agents share namespace-scoped memory and can hand off work through durable inboxes.

### LLM providers (count: 5) ✅

- Source: [configuration.md:1756](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/reference/configuration.md#L1756), [models-and-keys.md:58–61](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/getting-started/models-and-keys.md#L58-L61) — Four real generation backends (OpenAI, Anthropic, Bedrock and a configured local endpoint), plus a distinct Google Gemini embedding backend. Excludes test fakes and counts OpenAI only once.

### Cache optimization ✅

- Source: [results.md:536–550](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/benchmarks/results.md#L536-L550) — `code.ask` can serve a cached generated answer without repeating generation when the cached question clears its threshold.

### Procedural memory ❌

### Sandboxed execution ❌

### Scheduled/autonomous ❌

### Privacy/encrypt ✅

- Source: [models-and-keys.md:69–89](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/getting-started/models-and-keys.md#L69-L89), [conversations-and-sessions.md:238–254](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/conversations-and-sessions.md#L238-L254) — The administrator’s stored model-provider keys are encrypted. Transcript logging and extracted memory have separate capture controls.

### Data export ✅

- Source: [okf.md:1–27](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/integrations/okf.md#L1-L27) — `loom export-okf` renders a namespace’s memories as Markdown with structured metadata. `loom import-okf --dry-run` previews an import.

---

## Data Model

### Entities ✅

- Source: [writing.md:215–223](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/writing.md#L215-L223) — Memory rows have separate searchable entity and repository-file fields, with background entity extraction when omitted.

### Actions ✅

- Source: [conversations-and-sessions.md:249–254](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/conversations-and-sessions.md#L249-L254) — Coding-agent hooks can record tool actions as structured episodic observations.

### Keywords/tags ✅

- Source: [writing.md:215–221](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/writing.md#L215-L221) — Tags are stored on memories and can filter recall.

### Anticipated queries ❌

### Trigger rules ✅

- Source: [claude-code.md:322–336](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/integrations/claude-code.md#L322-L336) — An enabled Claude Code pre-edit hook retrieves context for the file about to be edited.

### Domain tag ✅

- Source: [search-and-ask.md:104–113](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/search-and-ask.md#L104-L113), [extraction.md:29–40](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/extraction.md#L29-L40) — Namespace-registered categories are structured memory facets used during extraction and retrieval.

### Task type ✅

- Source: [tasks-and-decisions.md:17–63](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/tasks-and-decisions.md#L17-L63) — A separate task inbox stores a task’s kind and unfinished states such as deferred and blocked.

### Context (why) ✅

- Source: [tasks-and-decisions.md:249–269](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/tasks-and-decisions.md#L249-L269) — A decision record stores the scenario, reasoning, alternatives and outcome. Its searchable memory includes the reasoning alongside the chosen outcome.

### Source attribution ✅

- Source: [memory.md:885–893](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/reference/operations/memory.md#L885-L893) — The row records its writer and one of six source classes, including asserted, extracted, observed and imported.

### Origin + trust ✅

- Source: [history-and-provenance.md:56–73](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/history-and-provenance.md#L56-L73), [search-and-ask.md:133–147](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/search-and-ask.md#L133-L147) — An optional ranking term uses provenance and attestation. This term is off by default.

### Emotional ❌

### Conflict surfacing ✅

- Source: [conflicts-and-refusal.md:21–41](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/conflicts-and-refusal.md#L21-L41) — Eligible writes compare peer memories and flag and cross-link detected conflicts.

### Layered memory ❌

### Time-travel ✅

- Source: [writing.md:200–213](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/writing.md#L200-L213), [history-and-provenance.md:30–40](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/history-and-provenance.md#L30-L40) — Key history exposes previous versions. Retrieval can replay valid time or knowledge time.

### Schema fields (count: 22) ✅

- Source: [memory.md:871–912](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/reference/operations/memory.md#L871-L912) — Count is a conservative inventory of 22 distinct fields in the public memory read shape: value, memory_type, confidence, on_expire, expire_reason, temporal_confidence, pinned, actor, source_class, source_trace, source_resource_id, agent, user_id, session_id, status, code, superseded_by, duplicate_of, tags, entities, char_limit and lock_mode. Excludes request flags, the generated memory ID and timestamps.

---

## Search & Retrieval

### Full-text ✅

- Source: [search-and-ask.md:55–69](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/search-and-ask.md#L55-L69) — The lexical mode ranks by token overlap.

### Semantic/vector ✅

- Source: [search-and-ask.md:55–69](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/search-and-ask.md#L55-L69) — The semantic mode ranks by embedding cosine similarity.

### Hybrid (BM25+Vec) ✅

- Source: [search-and-ask.md:55–69](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/search-and-ask.md#L55-L69) — `bm25_hybrid` fuses BM25 and cosine. The separate `rrf` mode fuses lexical and semantic ranks.

### Deep (incl. thinking) ❌

### Code graph ✅

- Source: [overview.md:63–84](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/code-index/overview.md#L63-L84), [code-intelligence.md:9–23](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/use-cases/code-intelligence.md#L9-L23) — The structural index parses repository files and serves definitions, callers and impact queries.

### Docs search ✅

- Source: [knowledge.md:9–19](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/knowledge.md#L9-L19), [knowledge.md:89–98](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/knowledge.md#L89-L98) — An explicit knowledge search retrieves passages from ingested documentation with source context.

### Fact metadata query ✅

- Source: [search-and-ask.md:104–130](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/search-and-ask.md#L104-L130) — Memory retrieval supports structured filters, including type, tags and registered category.

### Timeline view ✅

- Source: [search-and-ask.md:293–307](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/search-and-ask.md#L293-L307) — `memory.timeline` reads retained memory events in time order and accepts `since` and `until`.

### Search modes (count: 8) ✅

- Source: [search-and-ask.md:55–69](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/search-and-ask.md#L55-L69) — Count covers the eight values of `memory.search(search_mode=…)`: semantic, rrf, lexical, hybrid, bm25_hybrid, graph, related and temporal.

### Data sources (count: 6) ✅

- Source: [unified-search.md:29–37](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/unified-search.md#L29-L37), [code-intelligence.md:9–23](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/use-cases/code-intelligence.md#L9-L23) — Six groups used for this count: memories, documents, profiles, conversations and tracker records in unified search, plus repository code through the code search plane.

---

## Knowledge Lifecycle

### Decay/forgetting ✅

- Source: [retention-and-erasure.md:52–63](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/retention-and-erasure.md#L52-L63) — Configured expiry automatically hides a memory, then a sweep applies its expiry policy, which can lower confidence.

### Supersede/replace ✅

- Source: [conflicts-and-refusal.md:87–99](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/conflicts-and-refusal.md#L87-L99), [memory.md:893–899](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/reference/operations/memory.md#L893-L899) — A replacement can retire the earlier version as superseded. Reads that include it identify its successor.

### Contradiction detection ✅

- Source: [conflicts-and-refusal.md:21–41](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/conflicts-and-refusal.md#L21-L41), [conflicts-and-refusal.md:54–62](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/conflicts-and-refusal.md#L54-L62) — The write path can identify conflicting active facts. An enabled resolver can judge flagged and nearby pairs later.

### Quarantine ❌

### Auto-resolution ✅

- Source: [conflicts-and-refusal.md:87–99](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/conflicts-and-refusal.md#L87-L99) — `auto_reinforce` can retire the older row when the configured conflict resolver confirms an update. The review policy can instead leave both rows pending.

### Trust model ✅

- Source: [history-and-provenance.md:56–73](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/history-and-provenance.md#L56-L73), [search-and-ask.md:133–147](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/search-and-ask.md#L133-L147), [writing.md:192–198](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/writing.md#L192-L198) — The optional ranking term uses source class and attestation. Unattested external rows are excluded from synthesized answers.

### Explicit forget ✅

- Source: [writing.md:179–188](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/writing.md#L179-L188), [retention-and-erasure.md:35–50](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/retention-and-erasure.md#L35-L50), [retention-and-erasure.md:103–110](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/retention-and-erasure.md#L103-L110) — Delete tombstones a key and hides it from reads. The separately scoped erasure operation removes the underlying content.

---

## Extraction Pipeline

### Auto-extraction ✅

- Source: [conversations-and-sessions.md:246–254](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/conversations-and-sessions.md#L246-L254), [extraction.md:1–10](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/extraction.md#L1-L10) — Enabled coding-agent hooks submit captured transcripts at session end. A real LLM extracts durable facts.

### Content-aware preprocessing ❌

### Deduplication ✅

- Source: [conflicts-and-refusal.md:280–297](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/conflicts-and-refusal.md#L280-L297) — Duplicate memories point to a canonical. Explicit consolidation can merge near-duplicate clusters.

### Quality refinement ✅

- Source: [extraction.md:29–44](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/extraction.md#L29-L44) — The extraction pipeline includes deterministic filters and a coding-capture verification pass for durable facts.

### Narrative generation ✅

- Source: [conversations-and-sessions.md:275–286](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/conversations-and-sessions.md#L275-L286) — A configured model can summarize recorded events into a handoff brief. A deterministic fallback produces a more limited brief.

### Clustering ✅

- Source: [conflicts-and-refusal.md:280–297](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/conflicts-and-refusal.md#L280-L297) — Memory consolidation groups clusters of near-duplicates before merging their contents.

### Recurrence detection ✅

- Source: [knowledge.md:1683–1698](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/knowledge.md#L1683-L1698), [knowledge.md:1701–1706](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/knowledge.md#L1701-L1706) — When gap detection and consent settings permit it, a worker groups repeated unanswered queries from distinct people.

### Persona extraction ✅

- Source: [working-memory-and-profiles.md:102–114](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/working-memory-and-profiles.md#L102-L114), [working-memory-and-profiles.md:141–160](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/memory/working-memory-and-profiles.md#L141-L160) — An optional worker builds a persistent operator-defined user profile from current memories. This is schema-driven rather than an unrestricted inferred persona.

---

## Platform Support

### Claude Code ✅

- Source: [mcp-clients.md:10–20](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/integrations/mcp-clients.md#L10-L20), [claude-code.md:322–336](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/integrations/claude-code.md#L322-L336) — Documented native plugin, MCP connection and optional hooks.

### Codex ✅

- Source: [mcp-clients.md:10–20](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/integrations/mcp-clients.md#L10-L20), [mcp-clients.md:148–160](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/integrations/mcp-clients.md#L148-L160) — Documented plugin and a plain MCP option.

### OpenCode ✅

- Source: [mcp-clients.md:200–205](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/integrations/mcp-clients.md#L200-L205), [mcp-clients.md:238–244](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/integrations/mcp-clients.md#L238-L244) — Documented MCP configuration. The client reported a connection in the documented check.

### Gemini CLI ✅

- Source: [mcp-clients.md:55–66](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/integrations/mcp-clients.md#L55-L66), [mcp-clients.md:238–244](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/integrations/mcp-clients.md#L238-L244) — Documented MCP installer and a client connection check.

### Copilot ✅

- Source: [mcp-clients.md:310–336](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/integrations/mcp-clients.md#L310-L336) — Documented experimental CLI plugin, with install and MCP discovery checked. A signed-in session was outside that check.

### Cursor ✅

- Source: [mcp-clients.md:10–20](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/integrations/mcp-clients.md#L10-L20), [mcp-clients.md:55–66](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/integrations/mcp-clients.md#L55-L66) — Documented plain MCP configuration and installer. The plugin is documented as untested in Cursor.

### Windsurf ✅

- Source: [mcp-clients.md:55–66](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/integrations/mcp-clients.md#L55-L66) — Documented MCP installer and configuration location.

### OpenClaw ✅

- Source: [mcp-clients.md:221–227](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/integrations/mcp-clients.md#L221-L227), [mcp-clients.md:238–244](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/integrations/mcp-clients.md#L238-L244) — Documented gateway MCP configuration and connection check.

### Hermes ✅

- Source: [mcp-clients.md:217–226](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/integrations/mcp-clients.md#L217-L226), [mcp-clients.md:238–244](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/integrations/mcp-clients.md#L238-L244) — Documented Hermes Agent MCP configuration and connection check.

### pi/omp ❌

### Antigravity ✅

- Source: [mcp-clients.md:198–210](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/features/integrations/mcp-clients.md#L198-L210) — Documented MCP configuration for Google Antigravity.

---

## Benchmarks

### LoCoMo ✅

- Score: 79.7% with an external reader given ten memory hits and 89.6% with Loom’s configured `memory.ask`.
- Source: [results.md:91–122](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/benchmarks/results.md#L91-L122) — All 10 conversations. The scores below are the 1,540 answerable category 1–4 questions. The release reports adversarial abstention separately.

### LongMemEval ✅

- Score: 92.0% with the fixed GPT-5 reader over the top 200 hits and 96.6% with Loom’s configured `memory.ask`.
- Source: [results.md:124–148](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/benchmarks/results.md#L124-L148), [results.md:179–188](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/benchmarks/results.md#L179-L188) — All 500 LongMemEval-S questions with the official judge. The configured end-to-end answer model differs from the fixed-reader setup.

### PersonaMem ❌

### Token reduction ✅

- Score: 91% fewer reader prompt tokens in this comparison.
- Source: [results.md:434–457](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/benchmarks/results.md#L434-L457) — On a 100-question paired LongMemEval-S sample, the same GPT-5 reader saw 9,443 prompt tokens per question with Loom retrieval versus 103,879 with the whole history. Memory-construction tokens are excluded.

### Methodology open ✅

- Source: [results.md:113–122](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/benchmarks/results.md#L113-L122), [results.md:175–189](https://github.com/ClickHouse/loom/blob/47b479dcdae4c089aef2690428fa4c9a8f54554c/docs/benchmarks/results.md#L175-L189) — The release publishes dataset and harness invocations, judge and model settings, result artifacts and reproduction steps.
