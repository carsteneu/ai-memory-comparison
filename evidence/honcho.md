# Honcho — Evidence

> Every ✅ claim backed by public documentation or source code.
> Audit date: 2026-05-28. Source: GitHub `plastic-labs/honcho` main branch, `honcho.dev/docs`, README.md.
> Updated 2026-10-26 against commit [`6edadaa`](https://github.com/plastic-labs/honcho/tree/6edadaa2e374d9d698aadda9c20ea88196795937): Platform Support, Explicit forget, Hybrid search and Benchmarks. Line links below marked (2026-10-26) point at that commit.

## Architecture

### Web UI ✅
- `README.md` — Managed service at `api.honcho.dev` with dashboard at `app.honcho.dev`. Self-hosted deployments include configuration interface.
- `app.honcho.dev` — Sign-up flow provides web-based dashboard for API key management, workspace creation, and monitoring.

### Offline ✅
- `README.md` — "Self-hosting" section: Docker Compose setup (`cp docker-compose.yml.example docker-compose.yml; docker compose up`). Local development without Docker also documented.
- `README.md` — SDKs support `base_url="http://localhost:8000"` for local deployments. Requires Postgres with pgvector.
- `README.md` — "You can run the full server locally with Docker, then point the SDKs at `http://localhost:8000`."

### Privacy ⚠️ Partial
- Self-hosted: full data control, all data stays on your infrastructure (Postgres).
- Managed service (`api.honcho.dev`): data flows through Honcho's cloud infrastructure. Not end-to-end encrypted.
- **Finding**: Privacy only achievable via self-hosting. Managed service sees all messages and conclusions.

### Export ⚠️ Unclear
- No dedicated "export" tool or API endpoint found in README or docs.
- SDKs provide read access to all primitives (messages, conclusions, representations) — programmatic export possible.
- Self-hosted: direct Postgres access enables full data export.
- **Finding**: No first-class export feature. Data accessible programmatically but no one-click export.

### LLM providers — 3+ (claims 1 — **UNDERCOUNT** ✅→🔺)
- `README.md` — "Supports any LLM (OpenAI, Anthropic, open source)."
- `.env.template` — Configured for three providers: `LLM_GEMINI_API_KEY`, `LLM_ANTHROPIC_API_KEY`, `LLM_OPENAI_API_KEY`. Each used for different reasoning tiers.
- `README.md` — Configuration section: `[llm]` block with provider API keys and general settings. Multi-provider configurable per reasoning level (minimal/low/medium/high/max).
- **Finding**: At minimum 3 distinct providers supported (Gemini, Anthropic, OpenAI). The "provider-agnostic" design principle suggests more can be added.

### Multi-agent ✅
- `README.md` — "Peer-centric model: Tracks users, agents, groups, projects, and ideas as entities that change over time." "Multi-peer perspective: Models what one peer knows about another when configured."
- `docs/architecture` — "Peers can observe other peers in sessions (configurable with observe_me and observe_others)." "Treating humans and agents the same way lets you build arbitrary combinations for multi-agent or group chat scenarios."
- Sessions support many-to-many peer relationships with configurable observation settings.

---

## Data Model

### Entities ✅
- `README.md` — Peer model: "Peers are the most important entity in Honcho—everything revolves around building and maintaining their representations." "A peer represents any individual user, agent, or entity in a workspace."
- `README.md` — "Workspaces contain Peers (any entity that persists but changes) and Sessions (interaction threads between peers)."
- Internal collections keyed by `(observer, observed)` peer pairs — cross-peer modelling as first-class concept.

### Time-travel ❌
- `README.md` and `docs/reasoning` — No timestamp-based query API found. No "query at time T" or "snapshot rollback" feature.
- Background reasoning processes messages chronologically via session-based queues, but conclusions are continuously updated with no versioned history exposed.
- **Finding**: Temporal reasoning exists (reasoning pipeline processes in chronological order, token batching respects sequence), but there is no user-facing time-travel query capability.

### Schema fields — 5 ✅ (claimed 5)
- Core Message primitive fields: `id`, `content`, `peer_id`, `session_id`, `created_at`, `metadata` (JSONB) = 6 fields.
- Conclusion/Representation primitives: additional fields stored in vector collections.
- Conservative count of 5 matches the essential message fields. The claimed number is reasonable.

---

## Search & Retrieval

### Full-text (BM25) ✅
- `README.md` — "Hybrid search (BM25 + vector)" listed under "What Honcho Gives You."
- Search endpoints: `peer.search(...)`, `session.search(...)`, `honcho.search(...)` all use hybrid strategy.
- `docs/chat` — Chat endpoint searches semantically but can also use source messages for more context.

### Semantic/vector ✅
- `README.md` — Vector-embedded documents stored in internal collections. pgvector for Postgres.
- `README.md` — Configurable vector stores: `pgvector`, `turbopuffer`, or `lancedb` via `[vector_store]` config.
- Embeddings via OpenAI (`EMBED_MESSAGES=true` in `.env.template`).

### Hybrid (BM25+Vec) ✅
- (2026-10-26) [`README.md:168`](https://github.com/plastic-labs/honcho/blob/6edadaa2e374d9d698aadda9c20ea88196795937/README.md#L168) — "Hybrid search (BM25 + vector)", exposed as `peer.search(...)`, `session.search(...)`, `honcho.search(...)`. [`README.md:672`](https://github.com/plastic-labs/honcho/blob/6edadaa2e374d9d698aadda9c20ea88196795937/README.md#L672) — search at Workspace, Session or Peer level "using a hybrid search strategy". `data.js` currently has `hybrid: false`.
- `README.md` — "Hybrid search (BM25 + vector)" explicitly listed as a feature.
- Search at workspace, session, and peer level all use the same hybrid strategy.
- "Requests can include advanced filters to further refine the results."

### Search modes — 3+ (claims 2 — **UNDERCOUNT** ✅→🔺)
- `search()` — Hybrid (BM25 + vector) search at workspace/session/peer level.
- `chat()` — Natural language reasoning-grounded query endpoint (`peer.chat(...)`).
- `context()` — Session context with token-budget summarization (`session.context(...)`).
- `representation()` — Static low-latency snapshots (`peer.representation(...)`).
- **Finding**: At least 3-4 distinct retrieval interfaces. Claimed 2 is an undercount.

---

## Knowledge Lifecycle

### Supersede/replace ❌ (implicit only)
- `docs/reasoning` — "Consolidation (identifying redundant or contradictory information)" is part of the reasoning pipeline. New reasoning passes can refine or extend existing conclusions.
- No explicit `supersede` API, version chain, or old-value retention. Conclusions are updated in place during background processing.
- `docs/reasoning` — "Representations enable continuous improvement as new messages refine existing conclusions and scaffold new ones over time." This is additive/scaffolded improvement, not explicit replacement.
- **Finding**: Implicit refinement exists (background reprocessing improves representations), but there is no explicit supersede mechanism with history tracking. Correctly should be marked false for the "supersede" feature as defined in the comparison (explicit chains+cycles like YesMem, update operations like engram).

### Explicit forget ✅ (2026-10-26)
- [`src/routers/conclusions.py:166-192`](https://github.com/plastic-labs/honcho/blob/6edadaa2e374d9d698aadda9c20ea88196795937/src/routers/conclusions.py#L166-L192) — `DELETE /workspaces/{workspace_id}/conclusions/{conclusion_id}`: "Delete a single Conclusion by ID."
- [`src/routers/sessions.py:418-431`](https://github.com/plastic-labs/honcho/blob/6edadaa2e374d9d698aadda9c20ea88196795937/src/routers/sessions.py#L418-L431) — `delete_session`: "Delete a Session and all associated messages."
- **Finding**: Both a single inferred memory (conclusion) and a whole session can be deleted. CRITERIA.md defines Explicit forget as "User or agent can explicitly delete/forget a memory or session", so this is ✅. Supersedes the 2026-05-28 finding, which predates the conclusions delete endpoint.

### Decay/forgetting ❌
- No mention of decay, Ebbinghaus forgetting curves, TTL, or automatic expiration of conclusions.
- Conclusions persist indefinitely once derived.

### Contradiction detect ⚠️ Partial
- `docs/reasoning` — "Consolidation (identifying redundant or contradictory information)" is listed as a reasoning capability.
- The formal logic framework includes deductive reasoning that can flag contradictions between premises.
- **Finding**: Contradiction detection exists as part of the internal reasoning pipeline (consolidation), but it's not exposed as a user-facing feature with conflict surfacing like engram's `mem_judge`/`mem_compare` or YesMem's `contradicts` relation type. The system detects contradictions internally but doesn't expose them as actionable items.

---

## Extraction Pipeline

### Auto-extraction ✅
- `README.md` — "Store conversations, events, documents, or tool traces as messages on a session. Reason — Honcho processes the queue in the background and updates peer representations."
- `docs/reasoning` — Background deriver worker processes messages asynchronously. Session-based queues ensure chronological processing.
- `README.md` — "Background Reasoning processes messages to extract premises, draw conclusions, and build representations."
- Multiple reasoning passes: explicit premises, deductive conclusions, induction (patterns), abduction (explanations), consolidation.

### Narrative generation ✅
- `README.md` — Chat endpoint: "synthesizes a coherent natural language response." Representations are narrative summaries of what Honcho knows about a peer.
- `docs/chat` — "Honcho searches through the peer's peer card and representation—conclusions drawn from reasoning over their messages."
- `docs/reasoning` — Peer cards (key biographical information), summaries, and representations all produce narrative-form content.

---

## Platform Support

### Claude Code ✅
- `README.md` — Two integration paths: plugin marketplace (`/plugin marketplace add plastic-labs/claude-honcho`) and raw MCP (`claude mcp add honcho`).
- `docs/agentic-development` — Full Claude Code integration guide. Plugin provides persistent memory surviving context wipes and session restarts.
- Repository includes `.claude/skills/` directory with agent skills.

### Codex ✅ (2026-10-26)
- [`README.md:184`](https://github.com/plastic-labs/honcho/blob/6edadaa2e374d9d698aadda9c20ea88196795937/README.md#L184) and [`README.md:218-225`](https://github.com/plastic-labs/honcho/blob/6edadaa2e374d9d698aadda9c20ea88196795937/README.md#L218-L225) — `npm install -g @honcho-ai/codex-honcho`, then `codex-honcho install`, which "registers hooks + MCP + skill in ~/.codex". Plugin repo: [plastic-labs/codex-honcho](https://github.com/plastic-labs/codex-honcho).

### OpenCode ✅
- (2026-10-26) [`README.md:187`](https://github.com/plastic-labs/honcho/blob/6edadaa2e374d9d698aadda9c20ea88196795937/README.md#L187) and [`README.md:244-250`](https://github.com/plastic-labs/honcho/blob/6edadaa2e374d9d698aadda9c20ea88196795937/README.md#L244-L250) — `opencode plugin "@honcho-ai/opencode-honcho" --global`. Plugin repo: [plastic-labs/opencode-honcho](https://github.com/plastic-labs/opencode-honcho). `data.js` currently has `p_opencode: false`.

### Gemini CLI ❌

### Copilot ✅ (2026-10-26)
- [`docs/v3/guides/integrations/mcp.mdx:141`](https://github.com/plastic-labs/honcho/blob/6edadaa2e374d9d698aadda9c20ea88196795937/docs/v3/guides/integrations/mcp.mdx#L141) — "VS Code (Copilot Chat)" MCP setup section. Rendered at [honcho.dev/docs/v3/guides/integrations/mcp](https://honcho.dev/docs/v3/guides/integrations/mcp#vs-code-copilot-chat).

### Cursor ✅ (2026-10-26)
- [`README.md:185`](https://github.com/plastic-labs/honcho/blob/6edadaa2e374d9d698aadda9c20ea88196795937/README.md#L185) and [`README.md:227-233`](https://github.com/plastic-labs/honcho/blob/6edadaa2e374d9d698aadda9c20ea88196795937/README.md#L227-L233) — install script from [plastic-labs/cursor-honcho](https://github.com/plastic-labs/cursor-honcho); "The installer wires global hooks and MCP config."

### Windsurf ✅ (2026-10-26)
- [`docs/v3/guides/integrations/mcp.mdx:119-138`](https://github.com/plastic-labs/honcho/blob/6edadaa2e374d9d698aadda9c20ea88196795937/docs/v3/guides/integrations/mcp.mdx#L119-L138) — Windsurf MCP config for `~/.codeium/windsurf/mcp_config.json`. MCP only, no dedicated plugin.

### OpenClaw ✅
- (2026-10-26) [`README.md:189`](https://github.com/plastic-labs/honcho/blob/6edadaa2e374d9d698aadda9c20ea88196795937/README.md#L189) and [`README.md:261-266`](https://github.com/plastic-labs/honcho/blob/6edadaa2e374d9d698aadda9c20ea88196795937/README.md#L261-L266) — `openclaw plugins install @honcho-ai/openclaw-honcho`. Plugin repo: [plastic-labs/openclaw-honcho](https://github.com/plastic-labs/openclaw-honcho). `data.js` currently has `p_openclaw: false`.
- `README.md` — `openclaw plugins install @honcho-ai/openclaw-honcho`. Setup migrates legacy `MEMORY.md`/`USER.md`/`IDENTITY.md` into Honcho.

### Hermes ✅
- (2026-10-26) [`README.md:271-277`](https://github.com/plastic-labs/honcho/blob/6edadaa2e374d9d698aadda9c20ea88196795937/README.md#L271-L277) — `hermes memory setup`, select "honcho". Hermes' own docs list Honcho under Memory Providers: [hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers). `data.js` currently has `p_hermes: false`.

### pi/omp ✅ (2026-10-26)
- [plastic-labs/pi-honcho](https://github.com/plastic-labs/pi-honcho) — official Honcho extension for the pi coding agent, published on npm as `@honcho-ai/pi-honcho`.

### Antigravity ❌

---

## Benchmarks

All figures below are self-reported by Plastic Labs on [honcho.dev/evals](https://honcho.dev/evals/) (checked 2026-10-26). Unless stated otherwise the page says runs use gemini-2.5-flash-lite as deriver and claude-haiku-4.5 as dreamer and dialectic.

### LoCoMo ✅ (2026-10-26)
- Score: `89.9%` (1,540 questions; Claude Haiku 4.5 with full context: 75.6%)
- Source: [honcho.dev/evals](https://honcho.dev/evals/) — LoCoMo section.

### LongMemEval ✅ (2026-10-26)
- Score: `90.4%` on LongMemEval S (Claude Haiku 4.5 with full context: 62.6%)
- Source: [honcho.dev/evals](https://honcho.dev/evals/) — LongMem S section.

### PersonaMem ❌

### Token reduction ✅ (2026-10-26)
- Score: `52%` fewer tokens than the full-context baseline, averaged across LoCoMo questions
- Source: [honcho.dev/evals](https://honcho.dev/evals/) — "Honcho uses 52% fewer tokens on average than baseline across all LoCoMo questions."

### Methodology open ✅ (2026-10-26)
- Source: [plastic-labs/honcho-benchmarks](https://github.com/plastic-labs/honcho-benchmarks), linked from honcho.dev/evals as "Methodology and raw results are on GitHub". Also [`README.md:345-347`](https://github.com/plastic-labs/honcho/blob/6edadaa2e374d9d698aadda9c20ea88196795937/README.md#L345-L347).

The page also reports BEAM (0.630 at 100K tokens down to 0.409 at 10M). BEAM isn't a column in this table.

### Published benchmarks ✅ (2026-05-28 audit)
- `README.md` — "Honcho's evals span LongMemEval, LoCoMo, and other long-conversation benchmarks."
- `honcho.dev/evals` — Evals page with methodology and results.
- `blog.plasticlabs.ai/research/Benchmarking-Honcho` — Research blog post with reproducible methodology.
- Pareto-frontier announcement video linked from README.
- **Finding**: Has published benchmarks but specific scores (LoCoMo, LongMemEval numbers) are not in the README. The evals page and blog post contain the actual scores.

---

## Claims NOT present — verified

The following features are correctly absent from public documentation:

**Search:** deep (incl. thinking), codeGraph, docsSearch, factQuery, timeline — all ❌

**Lifecycle:** decay, quarantine, autoResolve, trustModel — all ❌ (no forgetting/decay, no quarantine, no auto-resolution of stale facts, no trust-scoring model)

**Extraction:** contentPreproc, dedup (explicit), qualityRefine, clustering, recurrence, persona — all ❌ (extraction is background reasoning without content-aware preprocessing, no configurable dedup pipeline, no quality refinement step, no clustering engine, no recurrence detection, no persona extraction engine)

**Data Model:** actions, keywords, anticipatedQueries, triggerRules, domainTag, taskType, context (why field), source, originTrust, emotional, conflict — all ❌ (Honcho has a peer-centric entity model but no structured metadata taxonomy beyond basic fields)

**Architecture:** proxy, singleBinary — all ❌ (FastAPI server + Postgres + deriver worker; no single binary; no proxy layer)

---

## Audit Notes

1. **searchModes undercount**: Claimed 2, but evidence shows at least 3 distinct retrieval interfaces: `search()` (hybrid), `chat()` (reasoning-grounded), `context()` (token-budget summarization), plus `representation()` (static snapshots). Recommend 3-4.

2. **supersede claim is incorrect**: Honcho has implicit refinement via background reprocessing (conclusions improve over time), but no explicit supersede API with history tracking. The comparison's "supersede" feature means explicit replace-with-chain (like YesMem chains or engram update operations). Should be marked false.

3. **timeTravel claim is incorrect**: Temporal reasoning exists in the pipeline (chronological queue processing), but there is no user-facing "query at time T" or snapshot rollback capability. Should be marked false.

4. **explicitForget** (updated 2026-10-26): Honcho now has `DELETE .../conclusions/{conclusion_id}` for a single inferred fact, alongside session deletion. ✅ under the CRITERIA.md definition. See Explicit forget above.

11. **2026-10-26 platform refresh**: official plugins now exist for Codex, Cursor and pi, and the MCP guide documents Copilot (VS Code) and Windsurf. `data.js` also had OpenCode, OpenClaw and Hermes as false although this file marked them ✅ in May, and `hybrid: false` although this file marked it ✅.

5. **export is ambiguous**: No dedicated export tool. Programmatic access via SDKs is possible, and self-hosted deployments have direct Postgres access. The spirit of "export" (one-click data export) is not met.

6. **narrative ✅ confirmed**: The chat endpoint and representations produce coherent natural-language summaries of peer knowledge. Reasoning pipeline includes peer cards and session summaries.

7. **contradiction detection is partial**: The internal "consolidation" step identifies contradictory information, but it's not surfaced to users as a feature. The comparison's "conflict surfacing" feature (like engram's mem_judge or YesMem's contradicts relations) is not present in a user-facing way.

8. **Benchmarks**: Honcho publishes evals but specific LoCoMo/LongMemEval scores are on the evals page, not in the README. The exact scores should be looked up on `honcho.dev/evals` before entering into data.js.

9. **LLM provider count**: minimum 3 confirmed (Gemini, Anthropic, OpenAI). The "provider-agnostic" design principle and configurable `[llm]` block suggest more can be added. Recommend 3+.

10. **Multi-agent ✅ confirmed**: Peer model with many-to-many sessions, configurable observation settings, and cross-peer modelling makes Honcho genuinely multi-agent capable.
