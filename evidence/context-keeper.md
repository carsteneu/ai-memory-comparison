# context-keeper — Evidence

> Every ✅ claim backed by public source code or documentation.
> Sources: GitHub repo `jarmstrong158/context-keeper`. Version observed: 0.7.0 (pyproject.toml). Lines may shift; pinned to `main` for readability.
> Disclosure: submitted by the project author.

**Repo:** `github.com/jarmstrong158/context-keeper`
**Stars:** 0
**Language:** Python
**License:** MIT
**Created:** 2026-04-10
**Description:** Project memory for AI coding agents: records decisions, pipelines, and constraints with schema-enforced structured rationale, and injects them back at session start.

---

## System Metadata

| Field | Value |
|-------|-------|
| **Deployment** | `Local (stdio MCP server)` |
| **Storage** | `JSON files (.context/ in the project)` |
| **Integration** | `MCP / Claude Code hooks` |
| **Single binary?** | `no (single Python file, stdlib-only)` |
| **Setup** | `pip install context-keeper-mcp` |
| **Pricing** | `free (MIT)` |
| **Storage unit** | `Entry (decision / pipeline / constraint)` |

---

## Architecture

### Proxy ❌

### Web/TUI ❌

### Offline ✅
- `README.md` — "By default, `get_context` ranks entries with pure lexical matching (tag + word overlap) — zero dependencies, works offline."
- `README.md` — "All data stored as human-editable JSON files in `.context/` inside your project directory. Zero external dependencies."
- Semantic mode is opt-in and fail-safe: "if Ollama is unreachable or the model is missing, retrieval silently falls back to lexical ranking" (`README.md`, Semantic Retrieval section)

### Multi-agent ❌
- (Cross-project queries exist via `project_dir`, but no shared-memory coordination between agents.)

### LLM providers (count: 1) ✅
- `README.md` (Configuration) — `"semantic": { "model": "nomic-embed-text", "url": "http://localhost:11434" }` — Ollama is the one selectable embedding backend; model and URL are configurable
- `semantic_index.py` — `_Embedder` class posts to Ollama `/api/embed`

### Cache optimization ✅
- `README.md` — "Entry embeddings are cached per store in `.context/embeddings.json`, keyed by a hash of the entry text, so an edited entry is re-embedded automatically."
- `semantic_index.py` (`query_cosines`) — cache hit/miss split; only misses are embedded, in batched requests

### Procedural memory ❌
- (Pipelines store ordered workflow steps as *data* for the agent to follow, not executable scripts.)

### Sandboxed execution ❌

### Scheduled/autonomous ❌

### Privacy/encrypt ✅
- `README.md` — "All data stored as human-editable JSON files in `.context/` inside your project directory. Zero external dependencies." — local-only storage, no cloud component, no telemetry; the only optional network call is to a user-run local Ollama server

### Data export ✅
- `README.md` (Data Storage) — "All files are human-readable JSON. You can edit them directly." — the store itself is a structured filesystem mirror (decisions.json / pipelines.json / constraints.json), directly reusable without an export step

---

## Data Model

### Entities ❌

### Actions ✅
- `server.py` (record_pipeline inputSchema) — pipeline steps are structured objects: `{"order": integer, "action": string, "output": string}`, stored as separate fields per step
- `README.md` — "`record_pipeline` — Save a multi-step workflow with ordering and `purpose`"

### Keywords/tags ✅
- `server.py` — every entry type carries `"tags": {"type": "array"}` in its input schema; retrieval scores tag overlap (`score_entry`: "Tag matching (0-40)")
- `CLAUDE.md` (Tags Convention) — "Use lowercase, hyphen-separated tags."

### Anticipated queries ✅
- `server.py` (record_* inputSchemas) — `retrieval_hints`: "2-4 alternate phrasings a future session might search for (synonyms, symptom descriptions, error messages). Indexed for retrieval — rescues vocabulary-mismatch queries without needing embeddings." The recording agent is prompted by the schema to predict search phrasings at capture time
- `server.py` (`_text_words`) — hints are indexed into the lexical retrieval word set; `semantic_index.py` (`entry_text`) includes them in embeddings
- `README.md` (v0.7) — documented with a measured result: two held-out eval queries crowded out of the top-5 recovered to rank 1 after their gold entries got hints

### Trigger rules ✅
- `hooks/scope_guard.py` — "the moment the agent edits a file that a constraint's `scope` covers, the constraint is injected right there via hookSpecificOutput.additionalContext"
- `README.md` (v0.6) — "Scoped constraint injection. New `scope_guard.py` hook (PostToolUse on `Edit|Write|NotebookEdit`): the moment the agent edits a file covered by a constraint's `scope`, that constraint is injected into context"

### Domain tag ❌

### Task type ❌

### Context (why) ✅
- This is the system's core thesis. `README.md` — "`record_decision` — Save a decision with structured rationale (problem, why_chosen, what_we_tried, tradeoffs)"
- `server.py` (record_decision inputSchema) — `problem` ("What forced this decision?"), `why_chosen` ("Actual reasoning... What evidence, principle, or constraint drove the choice?"), both required with server-side min-length validation: "Thin entries are rejected server-side with field-specific guidance" (`README.md`)
- Constraints store `reason` (required, min 40 chars) and `triggering_incident` ("the gotcha story behind the rule")

### Source attribution ✅
- `server.py` (record_* inputSchemas) — `origin` enum with 3 distinct source levels: `"user"` (explicitly stated), `"agent"` (inferred from the session), `"import"` (backfilled/migrated); stored on every entry, default `agent`

### Origin + trust ✅
- `server.py` (`score_entry`) — "Origin trust (0-10): user-stated entries outrank agent-inferred, which outrank imported/backfilled" — trust weights `{"user": 10, "agent": 5, "import": 2}`
- `CLAUDE.md` — agent guidance: "only claim `user` for things the user actually said"

### Emotional ❌

### Conflict surfacing ✅
- `server.py` (`_find_similar_entries`) — "surface near-duplicates and potential contradictions at capture time"; every `record_*` response includes `similar_entries` when overlap is detected
- `server.py` (`_SIMILAR_NOTE`) — "if it contradicts one, resolve the conflict (deprecate_entry with superseded_by)"
- `CLAUDE.md` (Acting on similar_entries) — explicit resolution protocol: restatement → deprecate; contradiction → supersede; distinct → link
- Note: detection is lexical overlap (word-set Jaccard); judging duplicate-vs-contradiction is delegated to the agent

### Layered memory ❌

### Time-travel ✅
- `server.py` (`handle_deprecate_entry`) — deprecated entries are never deleted: status flips to "deprecated", `deprecated_reason` and `superseded_by` are recorded, and the entry stays in the store
- `server.py` (`handle_get_context`) — direct ID lookup returns any entry including deprecated ones ("Fetch a single entry by ID"), so superseded versions remain queryable with a traceable chain
- Temporal search also available via `since`/`before` (see Timeline view)

### Schema fields (count: 13) ✅
- `server.py` (`handle_record_decision`) — decision entries carry: summary, problem, why_chosen, what_we_tried, tradeoffs, alternatives, constraints_created, related_to, tags, retrieval_hints, origin, status, superseded_by (excluding auto IDs/timestamps/schema_version). Constraints: rule, reason, triggering_incident, scope, hardness, related_to, tags, retrieval_hints, origin, status (10)

---

## Search & Retrieval

### Full-text ✅
- `server.py` (`score_entry`) — "Free-text word matching against tags + text fields (0-40)"; `README.md` — "Text match — query words found in summary/rationale/rule text"

### Semantic/vector ✅
- `README.md` (Semantic Retrieval) — "Setting `semantic.enabled: true` blends an embedding-cosine signal into the ranking, using a local Ollama server (`ollama pull nomic-embed-text`)"
- `semantic_index.py` — full implementation with per-store embedding cache

### Hybrid (BM25+Vec) ✅
- `server.py` (`handle_get_context`) — `score_entry(...) + sem_weight * sem_map.get(...)`: lexical score and embedding cosine fused into one ranking via weighted linear combination (weight tuned on a dev split, see Benchmarks)
- Note: fusion is weighted-sum, not RRF

### Deep (incl. thinking) ❌

### Code graph ❌

### Docs search ❌

### Fact metadata query ✅
- `server.py` (get_context inputSchema) — structured filters: `types` (decisions/pipelines/constraints), `tags`, `scope`, `id` — e.g. "all decisions tagged Y" is `types=["decisions"], tags=["Y"]`
- `README.md` — "`get_context` — Retrieve relevant entries by query, tags, scope, or ID"

### Timeline view ✅
- `server.py` (get_context inputSchema) — `since`: "Temporal filter: only entries verified/created on or after this ISO date"; `before`: "only entries verified/created strictly before this ISO date"
- `README.md` (v0.7) — "'what did we decide this month' is now a query"
- `prune_stale` additionally lists entries by age (staleness view)

### Search modes (count: 3) ✅
- `server.py` (TOOLS) — three retrieval tools: `get_context` (query/tags/scope/id), `get_project_summary` (compact overview), `prune_stale` (staleness listing)

### Data sources (count: 3) ✅
- `server.py` — three entry stores searched: decisions, pipelines, constraints (`_resolve_paths`)

---

## Knowledge Lifecycle

### Decay/forgetting ✅
- `server.py` (`score_entry`) — "Recency (0-20)": relevance automatically decays with days since `verified_at` (`recency = max(0.0, min(1.0, 1 - (days_ago / 90)))`); unverified entries sink in the ranking without any manual action
- Entries are never auto-deleted — decay is relevance-only, deletion stays human-in-the-loop by design

### Supersede/replace ✅
- `server.py` (`handle_deprecate_entry`) — `superseded_by` field links a deprecated decision to its replacement
- `README.md` — "`deprecate_entry` — Retire an entry with reason"; decisions carry `superseded_by` from creation

### Contradiction detection ❌
- (Capture-time similar-entry surfacing flags heavy overlap for the agent to judge — see Conflict surfacing — but there is no semantic contradiction detection.)

### Quarantine ❌

### Auto-resolution ❌
- (`prune_stale` flags stale entries for review but deliberately never auto-archives: "Returns them for review — does not delete.")

### Trust model ❌

### Explicit forget ✅
- `server.py` (`handle_deprecate_entry`) — agent or user retires any entry by ID with a required reason; store files are also plain JSON, directly editable/deletable by the user

---

## Extraction Pipeline

### Auto-extraction ❌
- (Deliberate design: capture is agent-invoked `record_*` calls, prompted by hooks at commit time and session start — not automatic extraction.)

### Content-aware preprocessing ❌

### Deduplication ⚠️ (detects; agent merges)
- `server.py` (`_find_similar_entries`) — automatic near-duplicate detection on every `record_*` (word-set Jaccard vs all active entries, configurable `similar_threshold`)
- `CLAUDE.md` — merge protocol: "Restatement — deprecate the entry you just created and `update_entry` the original instead"
- ⚠️ Detection is automatic; the merge itself is performed by the agent following the returned guidance, not by the server

### Quality refinement ✅
- `server.py` (`handle_verify_quality`) — rule-based quality pass over all entries: flags `legacy` (pre-v0.4 schema), `thin_reason` (rationale below threshold), `no_tags`, `isolated` (tag overlap but no links)
- `README.md` — "`verify_quality` — Scan entries for thin rationale, missing tags, isolated arcs (auto-called by PreCompact hook)"
- Capture-time validation: min-length schema enforcement rejects thin entries with field-specific guidance (`_check_min_lengths`)

### Narrative generation ✅
- `server.py` (`handle_get_project_summary`) — generates a compact project profile (absolute constraints first, then decisions, pipelines, staleness warnings), designed for conversation start and injected by the SessionStart hook
- Note: project-profile generation only; no per-session summaries

### Clustering ❌
- (`related_to` arc links are explicit/manual; graph traversal at retrieval is not clustering.)

### Recurrence detection ❌

### Persona extraction ❌

---

## Platform Support

### Claude Code ✅
- `README.md` (Claude Code Hook Setup) — full hooks config for SessionStart, PreCompact, Stop, PostToolUse (commit capture + scoped constraints); MCP install: `claude mcp add --scope user context-keeper -- python /path/to/context-keeper/server.py`
- Also documents Claude Desktop setup (`claude_desktop_config.json`)

### Codex ✅
- `README.md` (Other MCP clients) — documented `~/.codex/config.toml` `[mcp_servers.context-keeper]` configuration

### OpenCode ❌

### Gemini CLI ✅
- `README.md` (Other MCP clients) — documented `~/.gemini/settings.json` `mcpServers` configuration

### Copilot ❌

### Cursor ✅
- `README.md` (Other MCP clients) — documented `~/.cursor/mcp.json` / per-project `.cursor/mcp.json` configuration

### Windsurf ✅
- `README.md` (Other MCP clients) — documented `~/.codeium/windsurf/mcp_config.json` configuration

### OpenClaw ❌

### Hermes ❌

### pi/omp ❌

### Antigravity ❌

---

## Benchmarks

### LoCoMo ❌
- Score: `—`

### LongMemEval ❌
- Score: `—`

### PersonaMem ❌
- Score: `—`

### Token reduction ❌
- Score: `—`
- (Retrieval is token-budget-capped — "Results are capped by a configurable token budget (default: 4000 tokens)" — but no savings-vs-baseline number is published.)

### Methodology open ✅
- `evals/README.md` — full retrieval eval harness: labeled query→gold-entry datasets across three real project stores, dev/test splits ("Tune weights on `dev`, report on the held-out `test` split"), runnable scripts (`run_eval.py`), stored baselines
- `README.md` — published result: "this lifted hit@5 from 80% to 93% and MRR from 0.63 to 0.88 (the retrieval harness lives in `evals/`)"
- Datasets and run artifacts in `evals/datasets/` and `evals/runs/`
