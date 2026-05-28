# omega-memory — Evidence Dossier

> Audit date: 2026-05-28
> Source: https://github.com/omega-memory/omega-memory (148 stars, 22 forks)
> Analyzed: README.md, CHANGELOG.md (v0.2.0–v1.4.14), CONTRIBUTING.md, docs/architecture.md, docs/benchmark-report.md, docs/memory-benchmarks-landscape-2026.md, integrations/README.md, GitHub API, docs directory listing

---

## Meta

| Field | Value | Evidence |
|-------|-------|----------|
| description | "Persistent memory for AI coding agents" | GitHub repo description |
| deployment | MCP server (stdio transport), pip installable | README: `pip install omega-memory[server]`, MCP server spawned on demand with 3600s idle timeout |
| storage | SQLite + sqlite-vec + FTS5 at `~/.omega/omega.db` | Architecture doc, README advanced details |
| integration | Claude Code, Cursor, Windsurf, Cline, Codex, Antigravity, OpenClaw, Claude Desktop, CrewAI, any MCP client | README quick install, integrations/README.md |
| setup | `omega setup` (downloads ONNX model ~90MB, registers MCP, installs hooks, modifies ~/.claude/CLAUDE.md) | README quick install |
| license | Apache-2.0 | LICENSE file, GitHub API |
| created | 2026-02-13 | GitHub API `created_at` |
| docs URL | https://omegamax.co (homepage); docs/ in repo | GitHub API `homepage`; docs directory listing (architecture.md, benchmark-report.md, cli.md, etc.) |
| releases | 41 (latest v1.4.14, 2026-05-19) | GitHub releases |

---

## Architecture

| Feature | Present | Evidence |
|---------|---------|----------|
| webUi | **false** | No web UI in core open-source product. CLI + MCP only. Admin dashboard (3D graphs) is omega-pro/commercial. GitHub repo has `has_pages: false`. |
| offline | **true** | "Your data stays on your machine", "No cloud dependency", ONNX embeddings run on CPU locally, sqlite-vec on-device. Architecture: "OMEGA runs entirely on-device, including embeddings (ONNX)." |
| privacy | **true** | Local-first storage, AES-256 encrypted profiles (macOS Keychain), `~/.omega/` directory `0o700` permissions, zero external API dependencies for core memory. "Your data never leaves your machine." |
| export | **true** | `omega_backup` (export/import memories, keeps last 5). `omega export-obsidian` for Obsidian vault export (v1.3.1). Export/import via MCP tool. |
| multiAgent | **true** | 28 coordination tools (omega-pro): file claims, branch guards, task management with dependencies, peer messaging, intent broadcasting, session lifecycle. "OMEGA is the only memory system that solves multi-agent coordination." |
| llmFlex | **true** | Router module (10 tools, omega-pro): 5 providers (Anthropic, OpenAI, Google, xAI, Groq), 5 intent classifications, 4 priority modes (cost/speed/quality/balanced). Also works with any LLM via MCP protocol. |

---

## Data Model

| Feature | Present | Evidence |
|---------|---------|----------|
| entities | **true** | Entity Registry (omega-pro): "Multi-entity corporate memory with relationships, hierarchies, and entity-scoped memories/profiles/documents." Auto-entity extraction from conversations (v1.1.0 Phase 3). `entity_id` column in schema v3. |
| actions | **true** | `event_type` field classifies memory by action: decision, lesson_learned, error_pattern, task_completion, session_summary. Coordination tools track actions: task_create, claim_file, branch_claim, heartbeat, push guard. |
| keywords | **true** | Auto-tag extraction at store time (language, tools, project). `filter_tags` parameter on omega_query with AND-logic. File-extension-to-tag mapping for contextual re-ranking. Word/tag overlap boost in retrieval pipeline. |
| context | **true** | Session awareness via session_id. Contextual re-ranking with `context_file` and `context_tags`. Metadata JSON blob per memory. Project-scoped storage. "Context virtualization" via checkpoint/resume_task. |
| source | **true** | Memories tagged with `session_id` and `project`. OmegaStorage backend carries `agent_type`. Event types encode source semantics. Feedback tracking (`omega_feedback`) records source-quality assessments. |
| emotional | **false** | No sentiment analysis, emotional valence, or affective state tracking found. Not in schema, not in tool descriptions. |
| conflict | **true** | Contradiction detection surfaced in store output (v1.1.0). CrewAI integration: "conflicting memories are flagged and resolved." `_word_overlap` for Jaccard similarity comparison. |
| layeredMemory | **true** | Multiple memory types with distinct TTLs: session_summary (1 day), checkpoint (7 days), lesson/preference/decision/error (permanent). Compaction clusters into summary nodes preserving original granularity underneath. Event-type weighted scoring. |
| timeTravel | **true** | Bi-temporal data model with `valid_from`/`valid_until` for point-in-time queries (v1.1.0). `omega_timeline` (memories grouped by day). `referenced_date` column for temporal anchoring. Temporal penalty in scoring (0.05x for old memories). |
| schemaFields | **15** | Core `memories` table: id, node_id, content, metadata, created_at, last_accessed, access_count, ttl_seconds, session_id, event_type, project, content_hash, priority, referenced_date, entity_id = 15 columns. (Architecture doc SQL DDL) |

---

## Search

| Feature | Present | Evidence |
|---------|---------|----------|
| fulltext | **true** | FTS5 full-text search with BM25 scoring. "Catches keyword matches that may be distant in embedding space." Phase phrase matching via CLI. |
| semantic | **true** | Vector similarity via sqlite-vec (cosine distance, 384-dim bge-small-en-v1.5 ONNX). Semantic search with `omega_query`. |
| hybrid | **true** | Blended ranking: "70% vector score, 30% text score." Both result sets combined. FTS5 + vector in same pipeline. |
| deep | **false** | No full conversation transcript search with context windows. Search returns memory nodes/embeddings, not raw message history. Checkpoint/resume preserves task state but is not a "deep search" feature. |
| codeGraph | **false** | Graph exists (edges table, `omega_traverse` with BFS up to 5 hops) but it is a *memory relationship graph* — not a code symbol-level call graph or dependency tree. No source-code-aware graph traversal. |
| docsSearch | **true** | Knowledge Base module (omega-pro): "Ingest PDFs, markdown, web pages, and text files into a searchable knowledge base with semantic chunking." Document RAG/search. |
| factQuery | **true** | `omega_type_stats` (memory counts by event type), `omega_session_stats` (by session). Entity registry queries. Structured `omega_query` with tag filters, priority range, date range. OmegaStorage structured recall in CrewAI integration. |
| timeline | **true** | `omega_timeline` (memories grouped by day), `omega_activity` (recent session overview), `omega_weekly_digest`. Temporal penalty in scoring pipeline. |
| searchModes | **5** | 1) Hybrid semantic+FTS5 (`omega_query`), 2) Similarity find (`omega_similar`), 3) Timeline/chronological (`omega_timeline`, `omega_activity`), 4) Graph traversal (`omega_traverse`), 5) Cross-session lessons (`omega_lessons`). Count: 5 distinct retrieval modes. |

---

## Lifecycle

| Feature | Present | Evidence |
|---------|---------|----------|
| decay | **true** | TTL system: session_summaries expire after 1 day, checkpoints 7 days. "Time decay" in retrieval scoring. Memory strength scoring with decay (v1.1.0). Temporal hard penalty: "very old, unaccessed memories get a 0.05x multiplier." |
| supersede | **true** | Evolution: similar content (55-95%) appends new insights to existing memories. Compaction "marks originals as superseded" via `superseded_by` edge type. Superseded-by linking on store. |
| contradiction | **true** | "Contradiction detection surfaced in store output" (v1.1.0). CrewAI integration: "conflicting memories are flagged and resolved." |
| quarantine | **true** | `omega_consolidate`: "Prune stale memories, cap summaries, clean edges." `omega_clear_session`: clear all memories for a session. Blocklist check (system noise patterns) during ingestion. |
| autoResolve | **true** | Auto-compaction every 14 days at session start. Auto-feedback on surfaced memories at session stop. Auto-relate creating edges (similarity >= 0.45) to top-3 similar memories. Auto-tags at store time. Dedup resolves duplicates automatically. |
| trustModel | **true** | Feedback dampening (memories rated "unhelpful" or "outdated" are penalized). Priority field (1-5). Event-type weighting (decisions/lessons 2x). Access count tracking. `recency_weight`, `semantic_weight`, `importance_weight` in CrewAI integration. |
| explicitForget | **true** | `omega_delete_memory` (by ID), `omega_edit_memory` (content edit), `omega_clear_session` (all session memories). CrewAI integration: `memory.forget(...)` → `omega.bridge.delete_memory(id)`. |

---

## Extraction

| Feature | Present | Evidence |
|---------|---------|----------|
| autoExtract | **true** | Auto-capture hook (UserPromptSubmit → `auto_capture`) extracts lessons/decisions. Behavioral learning engine (v1.3.1): "Pattern analysis engine that learns tool preferences, git style, session patterns, co-edit graphs, and workflow sequences." Trajectory distillation: auto-extracts session summaries at stop. |
| contentPreproc | **true** | Unicode normalization (NFC). Blocklist check (system noise patterns). Auto-tag extraction (language, tools, file paths, project names). |
| dedup | **true** | Three layers: SHA256 content hash (exact), embedding cosine similarity >= 0.85 (semantic), per-type Jaccard similarity. Also query-time deduplication. |
| qualityRefine | **true** | Contextual re-ranking (Phase 2.5 boost capped at 50%). Type-weighted scoring. Feedback dampening. Abstention floor (0.35 vec, 0.5 text). LLM-based query expansion (v1.2.0). Position-aware reranking (QMD-inspired). |
| narrative | **true** | Session summaries auto-generated at session stop. `omega_weekly_digest` with stats and trends. Compaction clusters and summarizes related memories. |
| clustering | **true** | `omega_compact`: Jaccard clustering on related memories, creates consolidated summary nodes. Compaction runs auto-every 14 days. |
| recurrence | **true** | `omega_lessons`: cross-session lessons ranked by access count. Behavioral pattern analysis: workflow sequences, co-edit graphs. |
| persona | **true** | `omega_profile`: read/update user profile. `omega_welcome`: session briefing with profile. Behavioral profile engine: tool preferences, git style, session patterns. User preferences memory type (permanent TTL). `omega_list_preferences`. |

---

## Platform Support

| Feature | Present | Evidence |
|---------|---------|----------|
| p_claude | **true** | Claude Code (primary target, hooks into `~/.claude/settings.json`), Claude Desktop (`omega setup --client claude-desktop`). README: "Works with Claude Code, Cursor, Claw Code." |
| p_codex | **true** | Codex CLI listed in `omega setup --client codex` and `omega doctor --client` options (v1.3.1). Framework support added in changelog. |
| p_opencode | **false** | Not mentioned in any documentation or integration list. No explicit OpenCode support. (May work via generic MCP but no evidence of explicit support.) |
| p_gemini | **true** | README hero: "Works with Claude, GPT, Gemini, Cursor, Claw Code, and any MCP client." Router module supports Google/Gemini as provider. |
| p_copilot | **false** | Not mentioned in any documentation. |
| p_cursor | **true** | `omega setup --client cursor` supported. Listed in README comparison table. Hook system "abstracted for multi-client support (Claude Code, Cursor, Windsurf, Cline)" (v1.2.0). |
| p_windsurf | **true** | `omega setup --client windsurf` supported. Listed in comparison table. Topics include "windsurf". |
| p_openclaw | **true** | `openclaw-skill/` directory in repo. `docs/openclaw-plugin-architecture.md` (19,961 bytes). Claw Code listed as supported client. |
| p_hermes | **false** | Not mentioned in any documentation. |
| p_pi | **false** | Not mentioned in any documentation. |
| p_antigravity | **true** | Listed in `omega doctor --client` options and setup (v1.3.1 changelog: "Added Codex CLI, Antigravity IDE, and venv Python resolution"). |

**Also supports (not in audit list):** Cline, CrewAI (dedicated integration), venv-based Python resolution, any MCP-compatible client.

---

## Benchmarks

| Feature | Present | Evidence |
|---------|---------|----------|
| b_locomo | **false** | OMEGA's benchmark report discusses LoCoMo as background but does not claim a LoCoMo score. "Near-saturated by modern systems." No OMEGA LoCoMo results. |
| b_longmemeval | **true** | **76.8% on LongMemEval** (standard 500-question LongMemEval_S protocol, GPT-4.1 generation, GPT-4o/GPT-4.1 grading). Full category breakdown: Single-Session 95.7%, Knowledge Updates 87.2%, Temporal Reasoning 70.7%, Multi-Session 65.4%, Preference 50.0%. Internal retrieval benchmark (`longmemeval_bench.py`) scores 100/100 for component-level retrieval precision. Reproducible with open-source evaluation harness (`benchmarks/longmemeval/scripts/longmemeval_official.py`). |
| b_personamem | **false** | No PersonaMem benchmark results. Preference extraction scored 50% on LongMemEval (identified as "primary improvement target") but no dedicated PersonaMem test. |
| b_token | **false** | No token-efficiency benchmark claimed. Memory footprint reported (~31MB startup, ~337MB after query) but not a formal benchmark. Condensed mode claims ~80% context token savings (v1.3.1) but this is a feature claim, not a benchmark result. |
| b_methodology | **true** | Detailed methodology in `docs/benchmark-report.md`: standard LongMemEval_S protocol (500 questions, 5 capability dimensions), GPT-4o/GPT-4.1 judge with official grading rubrics. Reproducible: open-source code, evaluation harness script, result files as JSONL. No cloud dependencies. 1,592 tests verify correctness. |

---

## Tool Summary

| Module | Tools | Scope |
|--------|------:|-------|
| Core Memory | 27 | Store, query, traverse, checkpoint, resume, consolidate, compact, timeline, weekly digest |
| Coordination (pro) | 28 | Sessions, file claims, branch guards, tasks, messaging, audit |
| Router (pro) | 10 | Multi-LLM routing, intent classification, model switching |
| Entity (pro) | 8 | Corporate entities, relationships, hierarchies |
| Knowledge (pro) | 5 | Document ingestion (PDF, web, markdown), RAG |
| Profile (pro) | 3 | AES-256 encrypted personal data |
| **Total** | **73** | (when all pro modules active) |

---

## Search Pipeline (Detailed)

1. **Vector similarity** — sqlite-vec cosine distance, 384-dim bge-small-en-v1.5
2. **Full-text search** — FTS5 with BM25 scoring
3. **Blended ranking** — 70% vector + 30% text
4. **Type-weighted scoring** — decisions/lessons 2x, session summaries lower
5. **Contextual re-ranking** — tag/project overlap boost, Jaccard word overlap (50% max), feedback dampening, temporal hard penalty (0.05x for old memories), abstention floor (0.35 vec / 0.5 text)

## Hook System (11 handlers, 6 processes)

| Event | Handler |
|-------|---------|
| SessionStart | Welcome briefing, context resume, coordination register |
| Stop | Summary, deregister, release claims |
| UserPromptSubmit | Auto-capture lessons/decisions |
| PostToolUse (Edit/Write) | Memory surfacing, heartbeat, file claim |
| PostToolUse (Bash/Read) | Memory surfacing, heartbeat |
| PreToolUse (Bash) | Git push divergence + branch claim guard |
| PreToolUse (Edit/Write) | File claim guard + task guard |

Dispatch via `fast_hook.py` → Unix Domain Socket → `hook_server.py` daemon (~5ms vs ~750ms cold start). Fail-open: hook unavailability never blocks agent work.
