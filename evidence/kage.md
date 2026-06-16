# Kage — Evidence

> Every ✅ claim backed by public source code or documentation.
> Sources: GitHub repo `kage-core/Kage`, site at `kage-core.com`, package
> `@kage-core/kage-graph-mcp` (npm). Version observed: 2.3.0 (mcp/package.json).
> Lines shift; references pinned to `main` for readability.

**Repo:** `github.com/kage-core/Kage`
**Stars:** 6
**Language:** TypeScript
**License:** GPL-3.0-only
**Created:** 2026-05
**Description:** Verified memory for coding agents — every memory is checked against the code it cites, at write time, recall time, and when a diff changes the cited code.

---

## System Metadata

| Field | Value |
|-------|-------|
| **Deployment** | Local CLI + stdio MCP server + Claude Code plugin |
| **Storage** | Plain JSON packets in the repo (`.agent_memory/`) |
| **Integration** | MCP, hooks, CLI |
| **Single binary?** | no (Node package, two bins: `kage`, `kage-graph-mcp`) |
| **Setup** | `npx -y kage-graph-mcp install` |
| **Pricing** | free (open source) |
| **Storage unit** | Memory packet (cited, fingerprinted) |

---

## Architecture

### Proxy ❌

### Web/TUI ✅
- `mcp/viewer/` — bundled dashboard; `kage viewer` serves it. README "Viewer" section.
- `mcp/daemon.ts` — `startLiveFeed` serves `/kage/events` SSE; viewer streams packets/value-events live.

### Offline ✅
- `README.md` — "No API key, no database, no daemon." Recall uses local BM25 + a local vector index; no network calls in the core path.
- Packets are plain JSON on disk under `.agent_memory/`.

### Multi-agent ✅
- `README.md` — shared repo memory: one agent/person captures, every agent recalls; reviewed in the same PR as code.
- `mcp/index.ts` — `kage_workspace` / `kage_workspace_recall` recall across sibling repos.
- `kage sync` (`syncPersonal` in `mcp/kernel.ts`) shares personal memory across machines over a user-owned git remote.

### LLM providers (count: 0) ❌
- Core capture/recall use no external LLM or embedding provider — local BM25 + local vectors. No provider integrations to count.

### Cache optimization ✅
- `mcp/kernel.ts` — fingerprint/process cache and versioned code-graph cache (`CODE_GRAPH_BUILDER_VERSION`, `STRUCTURAL_EXTRACTOR_VERSION`) avoid recompute on unchanged inputs.

### Procedural memory ❌
- Stores knowledge, not executable scripts.

### Sandboxed execution ❌

### Scheduled/autonomous ❌
- Hooks are event-driven (SessionStart/PostToolUse/Stop), not scheduled.

### Privacy/encrypt ✅
- `mcp/kernel.ts` — `stripPrivateSpans`: `<private>…</private>` content is redacted before any packet/observation is written.
- Secret/PII scan at capture; local-only storage; no telemetry. GPL-3.0.

### Data export ✅
- Memory is plain JSON packets in the repo by design — inherently exportable, diffable, git-tracked.

---

## Data Model

### Entities ✅
- Packets carry a structured `paths[]` of cited files and `edges` to `path:` nodes (`mcp/kernel.ts`); citations are validated against the repo on write.

### Actions ❌
- No dedicated command/operation field.

### Keywords/tags ✅
- Packets carry a `tags[]` field (`kage learn --tags`).

### Anticipated queries ❌

### Trigger rules ✅
- PreToolUse(Read) hook + `kage file-context`: when the agent reads a file, verified memory citing *that file* is injected — condition-based activation. `mcp/kernel.ts` (`kageFileContext`), `plugin/hooks/kage-read-context.sh`.
- `kage context-slots`: pinned guidance included before task recall.

### Domain tag ❌
- Tags are freeform; no fixed domain taxonomy.

### Task type ❌

### Context (why) ✅
- Each packet stores a `context` object with `fact / why / trigger / action / verification / risk_if_forgotten / stale_when` (`mcp/kernel.ts`). The *why* is a first-class field.

### Source attribution ✅
- Packets record origin: `explicit_capture`, `auto_distill`, and observation-derived (`source_refs`, `observation_session` in `mcp/kernel.ts`) — ≥3 distinct capture levels, plus `author_branch`.

### Origin + trust ✅
- Auto-distilled drafts are written to a pending inbox and never enter trusted recall until approved; personal memory is recalled as a separate lower-trust `[personal]` section; admission scoring gates promotion (`mcp/kernel.ts`).

### Emotional ❌

### Conflict surfacing ✅
- Detects memory-vs-**code** conflict (a change invalidating a memory) via `staleCatch`, surfaces duplicate packets via `compact`, AND detects memory-vs-**memory** contradictions (same cited path, opposing claim) at write time via `detectContradictions` / `kage_conflicts` (`mcp/kernel.ts`; cue-based, no LLM).

### Layered memory ✅
- `kageLayers` / `kage layers` formalizes three tiers: L0 raw observations, L1 reviewed packets, L2 synthesis (repo maps, change summaries) (`mcp/kernel.ts`).

### Time-travel ✅
- `kage timeline` / `kage lineage` (`kageMemoryTimeline`, `kageMemoryLineage`) expose history and supersede chains; packets are git-tracked so prior versions are recoverable; `kage sessions`/`replay` show past sessions.

### Schema fields (count: 12) ✅
- Per packet: title, body/summary, type, paths, tags, context{fact, why, trigger, action, verification, risk_if_forgotten, stale_when}, freshness{path_fingerprints, last_verified_at, ttl}, edges, source_refs, quality. (`mcp/kernel.ts` packet schema, PACKET_SCHEMA_VERSION.)

---

## Search & Retrieval

### Full-text ✅
- BM25 over packet fields (`recallWithVectorScores` / recall path in `mcp/kernel.ts`).

### Semantic/vector ✅
- Local embedding index; recall fuses lexical + vector scores.

### Hybrid (BM25+Vec) ✅
- `recallWithVectorScores` combines BM25 and vector scores into one ranking.

### Deep (incl. thinking) ❌

### Code graph ✅
- TS-compiler AST + a tree-sitter WASM tier (Python/Go/Rust/Java/Ruby), import-aware call resolution. `README.md` ("tree-sitter tier"), `kage code-graph` / `kage_code_graph`. Memory is grounded to this graph.

### Docs search ❌
- No ingested framework/API documentation index. (The Truth Report reads repo docs to detect doc-vs-code lies, but that is not a doc search index.)

### Fact metadata query ✅
- Structured queries over memory metadata: `kage decisions`, `kage suppressed`, `kage memory-access`, `kage lifecycle` (`mcp/kernel.ts`).

### Timeline view ✅
- `kage timeline`; `kage resume` emits a recent-memory timeline index at session start.

### Search modes (count: 4) ✅
- recall, code-graph query, file-context (point-of-read), Truth Report scan.

### Data sources (count: 3) ✅
- memory packets, the code graph, and recorded session observations.

---

## Knowledge Lifecycle

### Decay/forgetting ✅
- TTL (365-day default) plus staleness: a memory whose cited evidence is gone is withheld from recall (`staleMemoryReasons`, `mcp/kernel.ts`).

### Supersede/replace ✅
- `kage supersede` (`supersedeMemory`) marks one packet as replaced by another and records a lineage edge.

### Contradiction detection ✅
- Both memory-vs-code (diff-time stale-catch) and memory-vs-memory: a new packet contradicting an approved one about the same cited path is surfaced at write time (`detectContradictions`, `kage_conflicts` in `mcp/kernel.ts`; deterministic cue-based, no LLM).

### Quarantine ✅
- Pending/auto-distilled packets are excluded from recall without deletion; `kage suppressed` lists withheld memory (`mcp/kernel.ts`).

### Auto-resolution ✅
- Stale memory is auto-withheld and flagged; auto-distill turns uncaptured sessions into drafts; reconciliation surfaces items needing update (`mcp/kernel.ts`).

### Trust model ✅
- Multi-tier: write-time citation rejection → pending (untrusted) vs approved → personal (lower-trust, separate recall section). Admission/quality scoring gates promotion.

### Explicit forget ✅
- `kage compact` / `kage gc` prune dead citations and packets; supersede/retire removes a memory from trusted recall.

---

## Extraction Pipeline

### Auto-extraction ✅
- Stop-hook `kage distill --auto` extracts a session's observations into draft packets without manual save (`distillSession`, `README.md`).

### Content-aware preprocessing ✅
- A signal gate (`observationSignalScore`, threshold 0.4) filters raw payloads/noise before drafting; content is truncated/handled by type.

### Deduplication ✅
- `kage compact` surfaces duplicate/near-duplicate packets; content-hash dedup on capture.

### Quality refinement ✅
- `evaluateMemoryQuality` + admission scoring run after capture; low-quality packets are flagged (`mcp/kernel.ts`).

### Narrative generation ✅
- `kage pr summarize` (branch summary), repo-map/profile packets, and the `kage resume` "previously…" digest generate summaries/handover narratives.

### Clustering ❌
- No topic/embedding clustering of memories. (Duplicate clustering exists in the Truth Report, not memory organization.)

### Recurrence detection ❌

### Persona extraction ❌

---

## Platform Support

### Claude Code ✅
- `kage setup claude-code` writes MCP + hooks; `plugin/` ships a Claude Code plugin. `README.md`, `kage setup list`.

### Codex ✅
- `kage setup codex` (`mcp/kernel.ts` setupAgent); `plugin/.codex-plugin/`.

### OpenCode ✅
- `kage setup opencode`.

### Gemini CLI ✅
- `kage setup gemini-cli`.

### Copilot ❌

### Cursor ✅
- `kage setup cursor`.

### Windsurf ✅
- `kage setup windsurf`.

### OpenClaw ❌

### Hermes ❌

### pi/omp ❌

### Antigravity ❌

> Also supports Cline, Goose, Roo Code, Kilo Code, Aider, Claude Desktop, and generic MCP via `kage setup <agent>` (not columns here).

---

## Benchmarks

### LoCoMo ❌
- Score: —

### LongMemEval ✅
- Score: 96.17% R@5 / 98.72% R@10 (LongMemEval-S)
- Source: `docs/BENCHMARKS.md` — methodology and command included.

### PersonaMem ❌
- Score: —

### Token reduction ⚠️
- A per-repo value ledger measures tokens saved per recall (memory read vs. re-reading source) and surfaces it via `kage gains` (`recordValueEvent` in `mcp/kernel.ts`). This is a self-measured ledger, not a standardized published token-reduction benchmark.

### Methodology open ✅
- `docs/BENCHMARKS.md` — methodology, exact commands, and caveats are public and reproducible.
