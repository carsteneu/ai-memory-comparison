# Engram Alpha — Evidence

> **Note:** distinct project from the already-listed `engram` (Gentleman-Programming/engram, Go). "Alpha" is part of the product name.
> All source links are pinned to commit `58f26fe` (current `main` at audit time, 2026-07-09).

**Repo:** `github.com/techtheist/engram`
**Stars:** 5
**Language:** Rust (backend), TypeScript/Vue (pane), Kotlin (JetBrains plugin)
**License:** MIT
**Created:** 2026-07-03
**Description:** Local-first graph memory for AI coding assistants — decisions, problems, cautions, and insights as typed nodes on an editable canvas embedded in JetBrains / VS Code; one shared MCP-served memory across assistants.

---

## System Metadata

| Field | Value |
|-------|-------|
| **Deployment** | Local daemon (`engram serve`) + IDE plugins + browser UI |
| **Storage** | SQLite (+ sqlite-vec, FTS5) |
| **Integration** | MCP / CLI / JetBrains plugin / VS Code extension / skill (instruction files) |
| **Single binary?** | yes (Rust binary; pane embedded via rust-embed) |
| **Setup** | `curl -fsSL …/install.sh \| sh` (macOS/Linux/WSL) or `install.ps1` (Windows) |
| **Pricing** | free (MIT) |
| **Storage unit** | Typed graph node (8 types) + sentence-shaped edges (7 types) |

---

## Architecture

### Proxy ❌

### Web/TUI ✅
- Source: [crates/engram-http/src/lib.rs#L130](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-http/src/lib.rs#L130) — Vue graph pane embedded via `RustEmbed`, served by the daemon at `127.0.0.1:8787`; [README (screenshots)](https://github.com/techtheist/engram/blob/58f26fe/README.md) shows it inside JetBrains and VS Code.

### Offline ✅
- Source: [crates/engram-core/src/rag.rs#L111-L114](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/rag.rs#L111-L114) — embeddings run locally via fastembed/ONNX (`BGESmallENV15`); no remote services or API keys anywhere in the pipeline. One-time model download to a machine-wide cache on first run ([rag.rs#L172](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/rag.rs#L172)).

### Multi-agent ✅
- Source: [README §Choose your assistant](https://github.com/techtheist/engram/blob/58f26fe/README.md) — "Every wired assistant reads and writes the same `.engram/graph.db` through the same MCP server — one shared, local memory across your AI agents. … a decision captured by Claude is recalled by Codex." Wiring implemented in [crates/engram-cli/src/main.rs#L119-L176](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-cli/src/main.rs#L119-L176) (`engram setup --cli claude|codex|gemini|opencode|kilo|antigravity|all`). Shared memory, not inter-agent messaging.

### LLM providers (count: 1) ✅
- Source: [crates/engram-core/src/rag.rs#L111](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/rag.rs#L111) — one embedding provider (local fastembed/ONNX, bge-small-en-v1.5). No LLM calls in the system itself; extraction is done by the host assistant.

### Cache optimization ❌

### Procedural memory ❌

### Sandboxed execution ❌

### Scheduled/autonomous ✅
- Source: [crates/engram-cli/src/main.rs#L408-L416](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-cli/src/main.rs#L408-L416) — daemon runs the conflict-candidate sweep at startup and every 6 hours (`tokio::time::interval(6 * 60 * 60)`), without user prompt.

### Privacy/encrypt ✅
- Source: [crates/engram-core/src/redact.rs#L53](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/redact.rs#L53) — secret-redaction pass (`scrub`) on every write: credential patterns, key=value masking, Shannon-entropy fallback for opaque tokens ([redact.rs#L72](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/redact.rs#L72)). Fully local / self-hosted by design, zero telemetry ([README §Local](https://github.com/techtheist/engram/blob/58f26fe/README.md)). No encryption at rest.

### Data export ✅
- Source: [crates/engram-cli/src/main.rs#L315](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-cli/src/main.rs#L315) — `engram export` (JSON snapshot) and `engram import` ([main.rs#L334](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-cli/src/main.rs#L334)); HTTP `GET /export` ([crates/engram-http/src/lib.rs#L118](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-http/src/lib.rs#L118)).

---

## Data Model

### Entities ✅
- Source: [crates/engram-core/src/types.rs#L118](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/types.rs#L118) — `code_refs: Vec<String>` structured field for file references on every node; `Anchor` node type names code areas/responsibilities ([types.rs#L38-L48](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/types.rs#L38-L48)). Supplied by the writing assistant, not automatic NER.

### Actions ❌

### Keywords/tags ❌

### Anticipated queries ❌

### Trigger rules ❌

### Domain tag ❌

### Task type ✅
- Source: [crates/engram-core/src/types.rs#L38-L48](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/types.rs#L38-L48) — unfinished work is typed (`Problem`, `Intent`) with open/resolved `status` and a computed `stale` flag; `list_open` MCP tool returns the live worklist ([crates/engram-mcp/src/lib.rs#L358](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-mcp/src/lib.rs#L358)).

### Context (why) ✅
- Source: [crates/engram-core/src/types.rs#L49-L58](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/types.rs#L49-L58) — sentence-shaped edges store the why: a Decision links `because` a Principle, a Resolution `answers` a Problem ([README §The ontology](https://github.com/techtheist/engram/blob/58f26fe/README.md)).

### Source attribution ❌
> Only two author levels (`user`, `claude` — [types.rs#L66-L67](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/types.rs#L66-L67)); criterion requires ≥3.

### Origin + trust ✅
- Source: [crates/engram-core/src/policy.rs#L18-L31](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/policy.rs#L18-L31) — assistant-written nodes start provisional at 0.5 trust fading over ~6 months; user approval restarts trust at 1.0 on a slower 1-year track that never fully expires. Trust modulates retrieval ranking ([store.rs#L598](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/store.rs#L598)).

### Emotional ❌

### Conflict surfacing ✅
- Source: [crates/engram-core/src/engine.rs#L491](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/engine.rs#L491) — `scan_conflicts` (write-time + 6-hourly + on-demand) queues unlinked look-alike pairs ≥ 0.85 cosine ([policy.rs#L43](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/policy.rs#L43)) as suspects; judged via pane worklist or MCP `resolve_suspect` with verdicts conflict / replaces / dismiss ([engine.rs#L551](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/engine.rs#L551)). Writes near contradicted knowledge return warnings ([policy.rs#L49](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/policy.rs#L49)).

### Layered memory ❌

### Time-travel ✅
- Source: [crates/engram-core/src/engine.rs#L551](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/engine.rs#L551) — superseded versions are retained: a `replaces` verdict archives the older node (`valid_until`) instead of deleting it, keeping a traceable chain browsable in the pane (show-archived filter). No arbitrary as-of-date queries.

### Schema fields (count: 8) ✅
- Source: [crates/engram-core/src/types.rs#L95-L118](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/types.rs#L95-L118) — `node_type`, `title`, `body`, `durability`, `source`, `session_id`, `status`, `code_refs` (excluding id/timestamps; `trust`/`stale` are computed at read time).

---

## Search & Retrieval

### Full-text ✅
- Source: [crates/engram-core/src/store.rs#L448](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/store.rs#L448) — `search_fts`: SQLite FTS5 with bm25 ranking and snippet extraction.

### Semantic/vector ✅
- Source: [crates/engram-core/src/store.rs#L581](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/store.rs#L581) — `search_vec`: k-nearest by cosine distance over sqlite-vec.

### Hybrid (BM25+Vec) ✅
- Source: [crates/engram-core/src/store.rs#L598](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/store.rs#L598) — `search_hybrid`: blends normalized bm25 and cosine relevance, then multiplies by trust so an irrelevant-but-trusted node can't outrank an actual match.

### Deep (incl. thinking) ❌

### Code graph ❌
> Explicitly positioned as a reasoning/decision memory, not a code-structure graph ([README](https://github.com/techtheist/engram/blob/58f26fe/README.md)).

### Docs search ❌

### Fact metadata query ✅
- Source: [crates/engram-mcp/src/lib.rs#L358](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-mcp/src/lib.rs#L358) — `list_open` (all open Problems/Intents); `search` accepts a node-type filter ([lib.rs#L70-L75](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-mcp/src/lib.rs#L70-L75)); `list_suspects` queries the pending-conflict queue.

### Timeline view ❌
> On the roadmap (a `timeline` MCP tool + pane view), not implemented at audit time.

### Search modes (count: 5) ✅
- Source: [crates/engram-mcp/src/lib.rs#L45-L374](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-mcp/src/lib.rs#L45-L374) — `search` (hybrid, hits carry 1-hop neighbors with conflicts/supersessions first), `traverse` (bounded BFS subgraph, edge-type filterable), `brief` (token-budgeted session-start digest), `list_open`, `list_suspects`.

### Data sources (count: 1) ✅
- Source: [crates/engram-core/src/store.rs#L448](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/store.rs#L448) — one searchable corpus: the typed memory nodes (no separate message/code/docs indexes).

---

## Knowledge Lifecycle

### Decay/forgetting ✅
- Source: [crates/engram-core/src/policy.rs#L14-L46](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/policy.rs#L14-L46) — trust is computed at read time from created/last-seen/approved timestamps and decays continuously; below 0.3 a node is `stale`; a decay pass archives unapproved episodic/volatile nodes 14 days past stale-crossing ([engine.rs#L608](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/engine.rs#L608)).

### Supersede/replace ✅
- Source: [crates/engram-core/src/engine.rs#L551](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/engine.rs#L551) — `replaces` edge type; a replaces verdict records the edge AND archives the older node, leaving a traceable chain ([types.rs#L49-L58](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/types.rs#L49-L58)).

### Contradiction detection ✅
- Source: [crates/engram-core/src/engine.rs#L491](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/engine.rs#L491) — automatic scan (write-time, 6-hourly, on-demand) flags suspected conflicts for human/agent judgment; see Conflict surfacing above.

### Quarantine ❌

### Auto-resolution ✅
- Source: [crates/engram-core/src/engine.rs#L608](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/engine.rs#L608) — `decay(ttl_days, dry_run)` auto-archives stale provisional episodic/volatile nodes after the 14-day TTL ([policy.rs#L44-L46](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/policy.rs#L44-L46)).

### Trust model ✅
- Source: [crates/engram-core/src/policy.rs#L18-L31](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/policy.rs#L18-L31) — user-approved > surfaced-provisional > never-surfaced trust tracks; trust multiplies relevance in ranking ([store.rs#L598](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/store.rs#L598)).

### Explicit forget ✅
- Source: [crates/engram-http/src/lib.rs#L218](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-http/src/lib.rs#L218) — `DELETE /nodes/:id` hard-deletes a node and cascades its edges ([engine.rs#L103](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/engine.rs#L103)); deliberately user-only (pane/HTTP) — the agent-facing MCP surface has no node delete.

---

## Extraction Pipeline

### Auto-extraction ❌
> Capture is cooperative by design: the assistant calls `add_note` guided by a shipped instruction skill (three intensities); nothing is extracted without a save call.

### Content-aware preprocessing ❌

### Deduplication ✅
- Source: [crates/engram-core/src/engine.rs#L238-L258](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/engine.rs#L238-L258) — every `add_note` runs a same-type cosine pre-check; ≥ 0.90 similarity ([policy.rs#L37](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/policy.rs#L37)) returns `{matched, created: false}` for merge instead of creating a near-duplicate.

### Quality refinement ✅
- Source: [crates/engram-core/src/engine.rs#L238-L316](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/engine.rs#L238-L316) — rule-based write pass: secret redaction ([redact.rs#L53](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/redact.rs#L53)), duplicate pre-check, and contradiction warnings when the new text lands ≥ 0.70 cosine near conflicted/superseded knowledge ([policy.rs#L49](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-core/src/policy.rs#L49)). No LLM pass.

### Narrative generation ❌
> `brief` compiles a deterministic digest of stored nodes; nothing is generated/synthesized.

### Clustering ❌

### Recurrence detection ❌

### Persona extraction ❌

---

## Platform Support

### Claude Code ✅
- Source: [README §Choose your assistant](https://github.com/techtheist/engram/blob/58f26fe/README.md) — default target: `.mcp.json` registration + `.claude/skills/engram/SKILL.md` capture skill (three intensities, sources in [skills/engram/](https://github.com/techtheist/engram/tree/58f26fe/skills/engram)); wiring in [crates/engram-cli/src/main.rs#L119-L176](https://github.com/techtheist/engram/blob/58f26fe/crates/engram-cli/src/main.rs#L119-L176).

### Codex ✅
- Source: [README §Choose your assistant](https://github.com/techtheist/engram/blob/58f26fe/README.md) — `engram setup --cli codex`: MCP registration in `~/.codex/config.toml` + `AGENTS.md` capture instructions.

### OpenCode ✅
- Source: [README §Choose your assistant](https://github.com/techtheist/engram/blob/58f26fe/README.md) — `engram setup --cli opencode`: `opencode.json` + `AGENTS.md`.

### Gemini CLI ✅
- Source: [README §Choose your assistant](https://github.com/techtheist/engram/blob/58f26fe/README.md) — `engram setup --cli gemini`: `.gemini/settings.json` + `GEMINI.md`.

### Copilot ❌

### Cursor ✅
- Source: [README §Install](https://github.com/techtheist/engram/blob/58f26fe/README.md) — the graph-pane extension is published to Open VSX for VSCodium/Cursor/Windsurf ([open-vsx.org/extension/techtheist/engram-alpha](https://open-vsx.org/extension/techtheist/engram-alpha)). Pane/UI only — MCP wiring for Cursor's agent is not automated.

### Windsurf ✅
- Source: same as Cursor — Open VSX pane extension only; agent MCP wiring not automated.

### OpenClaw ❌

### Hermes ❌

### pi/omp ❌

### Antigravity ✅
- Source: [README §Choose your assistant](https://github.com/techtheist/engram/blob/58f26fe/README.md) — `engram setup --cli antigravity`: `.agents/mcp_config.json` + `AGENTS.md`.

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

### Methodology open ❌
