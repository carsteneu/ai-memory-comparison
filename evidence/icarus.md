# Icarus Audit

**Date:** 2026-05-28
**Source:** https://github.com/esaradev/icarus-memory-infra
**Version:** v0.3.0 (latest as of audit)
**Language:** Python
**Stars:** 285
**License:** MIT

## URL Correction

The claimed URL `https://github.com/ICARUS-Memory/ICARUS` returns **404** — the organization `ICARUS-Memory` and repository `ICARUS` do not exist on GitHub. The actual repository is `https://github.com/esaradev/icarus-memory-infra`. This was already correctly registered in data.js (line 515). No redirect, no renamed org — just a different URL entirely.

## Summary

Icarus is an agent coherence infrastructure providing persistent, sourced, version-controlled memory for AI agents. Local-first, markdown-native Python library + MCP server. Three-layer model: working memory (per-task scratch), session archive (per-agent history), wiki (shared markdown source of truth). Implements provenance, non-destructive rollback, supersession chains, and verification lifecycle. ~23 schema fields. 3 search modes (keyword, embedding, hybrid) plus auto-selection.

The user's claims are **significantly inflated**: of ~30 claimed features, only 12 are verified present. 17 are absent entirely (webUi, entities, keywords, decay, autoExtract, contentPreproc, dedup, qualityRefine, narrative, recurrence, persona, deep, and 5 platform supports). The claimed URL is wrong. Multiple features the user didn't claim (verification, rollback, provenance, contradiction, lineage) are actually present.

## Claim Audit

### Verified Claims

| Claim | Status | Evidence |
|-------|--------|----------|
| offline | ✅ Verified | "Local-first. Your data stays on your machine or in your cloud." No cloud dependency, no API calls required. |
| privacy | ✅ Verified | "Agent memory is sensitive — codebase decisions, internal architecture, customer context — and shouldn't live inside a vendor's black box." All data stays local. |
| layeredMemory | ✅ Verified | Three explicit layers: working memory (per-task scratch), session archive (per-agent history, private), wiki (shared markdown source of truth). `IcarusMemory` class exposes `start_session()`, `end_session()`, `get_wiki_page()`. |
| timeTravel | ✅ Verified | Markdown-native, git-versionable files on disk. Non-destructive rollback via `memory_rollback` MCP tool: walks revises backward, finds verified ancestor, marks intermediates rolled_back. `lineage()` returns full ancestry chains. `memory_audit_search` recovers rolled-back entries. |
| fulltext | ✅ Verified | `memory_search` MCP tool: substring search across summary + body. `audit_search()` variant includes superseded + rolled-back entries. |
| semantic | ✅ Verified | Opt-in `[embeddings]` extra via sentence_transformers. Default model: `BAAI/bge-small-en-v1.5`. Embeddings cached per entry with cache-key on (model, file_mtime, file_size). |
| hybrid | ✅ Verified | `mode="hybrid"` or `"auto"`: BM25 + embedding fusion via Reciprocal Rank Fusion (k=60). Sort key is (verified-status-bucket, score). |
| supersede | ✅ Verified | Entries have `lifecycle` field (active/superseded), `superseded_by`, `supersedes` fields. `write_with_supersession()` atomically marks old entries superseded. "Stale facts get marked superseded — never overwritten." |
| explicitForget | ✅ Verified | Supersession marks entries inactive but preserves them. Rollback marks entries `rolled_back`. Both are intentional, user-triggered. No permanent deletion — audit trail preserved. |
| p_claude | ✅ Verified | INTEGRATIONS.md: explicit Claude Code MCP configuration with `~/.claude/mcp_servers.json` snippet. |
| p_cursor | ✅ Verified | INTEGRATIONS.md: explicit Cursor MCP configuration with `~/.cursor/mcp.json` snippet. |
| searchModes=3 | ⚠️ Misstated: 4 | Actually 4 modes: `keyword`, `embedding`, `hybrid`, `auto` (intelligently picks keyword or hybrid based on installed extras). User undersold this. |

### Partially Verified

| Claim | Issue | Evidence |
|-------|-------|----------|
| export | No explicit `export` tool. All data is markdown on disk, inherently portable. You can `git add .icarus/` and version memory alongside code. No formal export command. | MarkdownStore: entries at `<root>/YYYY/MM/icarus-<id>.md`. Wiki at `.icarus/wiki/`. |
| multiAgent | Per-agent session archives (private) + shared wiki. `start_session(agent_id, ...)` creates per-agent working memory. No agent orchestration, messaging, or coordination. Multi-agent data isolation but not multi-agent orchestration. | `SessionArchive` is per-agent. Wiki is global. No agent-to-agent communication. |

### Not Present (Falsely Claimed)

| Claim | Evidence of Absence |
|-------|---------------------|
| webUi | No web UI, TUI, dashboard, or viewer mentioned anywhere in README, DESIGN.md, INTEGRATIONS.md, or source. `mcp_server.py` provides stdio + HTTP MCP transport only. |
| entities | No entity extraction, tagging, or metadata field. `EvidencePointer` can reference files/URLs/entries but there's no named-entity annotation on entries. |
| keywords | No keyword/tag metadata field on entries. BM25 keyword search exists as a retrieval technique (`_keyword_score` in retrieval.py), but entries have no keyword annotation. |
| decay | No time-based decay or forgetting curve. Lifecycle transitions are explicit (active → superseded via `write_with_supersession()`). No automatic expiration. |
| autoExtract | No automatic background extraction pipeline. All entries are created explicitly via `memory_write` MCP tool or `IcarusMemory.write()` API. BriefingGenerator optionally uses LLM for briefing text but this is on-demand, not background extraction. |
| contentPreproc | No content preprocessing mentioned in any file. Entries store raw markdown body as-is. |
| dedup | No deduplication. `generate_id()` uses `secrets.token_hex(6)` — purely random, no content-hash dedup. The store checks for id collision but not content collision. |
| qualityRefine | No quality refinement pipeline. Verification is manual via `memory_verify` tool. `VerifiedStatus` tracks manual review state, not automated quality scoring. |
| narrative | No narrative generation. BriefingGenerator produces task briefings assembling existing facts from wiki + archive — these are compilations, not generated narratives. |
| recurrence | No recurrence or pattern detection. `recent_superseded` queries recent supersessions but there's no recurring pattern analysis. |
| persona | No persona extraction or modeling. No agent profile system beyond per-agent session archives. |
| deep | No deep search (thinking chain). Recall modes are: keyword (token overlap), embedding (cosine similarity), hybrid (BM25+embedding RRF). No chain-of-thought or deep reasoning search. |
| p_codex | Not in INTEGRATIONS.md. MCP-compatible in theory but no explicit Codex configuration doc, examples, or testing mentioned. |
| p_opencode | Not in INTEGRATIONS.md. No OpenCode plugin or configuration documented. |
| p_gemini | Not in INTEGRATIONS.md. No Gemini CLI configuration documented. |
| p_windsurf | Not in INTEGRATIONS.md. No Windsurf configuration documented. |
| p_openclaw | Not in INTEGRATIONS.md. Hermes adapter exists (`examples/hermes_adapter.py`) but no OpenClaw integration. |

### Schema Fields: Claimed 9 → Actual ~23

The `Entry` model (schema.py) has these fields:

1. `id` — Unique entry identifier (icarus:<12-hex>)
2. `agent` — Agent that produced the entry
3. `platform` — Platform name
4. `timestamp` — UTC creation time
5. `type` — Entry type (decision, observation, attempt, etc.)
6. `summary` — ≤200 char summary
7. `body` — Full markdown body
8. `project_id` — Optional project scope
9. `session_id` — Optional session scope
10. `status` — Task status (open/in-progress/closed)
11. `assigned_to` — Task assignee
12. `review_of` — Peer review link
13. `revises` — Revision chain link
14. `training_value` — LLM training data priority (high/normal/low)
15. `evidence` — List of EvidencePointer (kind, ref, excerpt, hash)
16. `source_tool` — Which tool created this entry
17. `verified` — VerifiedStatus (unverified/verified/contradicted/rolled_back)
18. `contradicted_by` — Conflicting entry reference
19. `artifact_paths` — Linked file paths
20. `verification_log` — List of VerificationRecord (verifier, timestamp, status, note)
21. `lifecycle` — Lifecycle state (active/superseded)
22. `superseded_by` — Superseding entry reference
23. `supersedes` — List of superseded entry references

Plus nested models add ~4 more structured fields: EvidencePointer (4 sub-fields), VerificationRecord (4 sub-fields).

### Features NOT Claimed but Present

These are significant features the user didn't list:

| Feature | Evidence |
|---------|----------|
| **verification** | First-class verification model: unverified → verified → contradicted → rolled_back. `memory_verify`, `memory_contradict` MCP tools. Verification records with verifier, timestamp, status, note. |
| **provenance / source** | `EvidencePointer` with 5 kinds (file, url, fabric_ref, tool_output, message), SHA256 hash, excerpt. Every entry links to its evidence. |
| **contradiction** | `memory_contradict` MCP tool links entries as contradictory. `contradicted_by` field with cross-reference validation. |
| **rollback** | Non-destructive rollback: walks `revises` backward, finds verified ancestor, writes rollback entry. `memory_rollback` MCP tool with dry_run + cascade options. |
| **lineage** | `memory_lineage` MCP tool: BFS walk of revises + review_of chains returning full ancestry. |
| **conflict surfacing** | Verified status filtering in recall: verified entries sorted above unverified, contradicted always sinks below unverified. |
| **task tracking** | `status` field (open/in-progress/closed), `assigned_to` for task assignment, `memory_pending` MCP tool. |
| **context (why)** | `BriefingGenerator` compiles task briefings from wiki pages + session archives + recent supersessions. LLM-enhanced when OPENAI_API_KEY set, template-based fallback. |
| **wiki** | `WikiManager`: shared markdown pages organized by topic/decision/project/agent. Entries linked to pages. Auto-classification via LLM (opt-in). |
| **training_value** | Entry-level `training_value` field to filter/prioritize training data selection. |
| **Hermes integration** | Native adapter at `examples/hermes_adapter.py` wiring Hermes session hooks onto `IcarusMemory.write`. |
| **MCP server** | Full MCP server with 10 tools: memory_write, memory_get, memory_recall, memory_search, memory_audit_search, memory_verify, memory_contradict, memory_rollback, memory_lineage, memory_pending. Stdio + HTTP transport. |

## Feature Inventory (from source)

### MCP Tools (10)
`memory_write`, `memory_get`, `memory_recall`, `memory_search`, `memory_audit_search`, `memory_verify`, `memory_contradict`, `memory_rollback`, `memory_lineage`, `memory_pending`

### Python API
`IcarusMemory.write()`, `write_with_supersession()`, `get()`, `recall()`, `search()`, `audit_search()`, `verify()`, `contradict()`, `rollback()`, `lineage()`, `pending()`, `start_session()`, `end_session()`, `get_briefing()`, `get_wiki_page()`, `search_wiki()`

### Three-Layer Memory Model
1. **Working memory** — Per-task scratch (observations, attempts, hypotheses). Cleared when task ends.
2. **Session archive** — Per-agent history. Private to the agent. Failed attempts stay private.
3. **Wiki** — Shared markdown source of truth, organized by topic. Cross-agent visible.

### Search Modes (4, not 3)
- `keyword` — Token overlap scoring across summary + body
- `embedding` — Cosine similarity via sentence_transformers
- `hybrid` — BM25 + embedding fused via RRF (k=60)
- `auto` — Picks keyword (no extras) or hybrid (extras installed)

### Platform Support
- Python library (any codebase)
- MCP server (stdio + HTTP)
- Claude Code, Cursor (explicit docs)
- LangChain (via `langchain-mcp-adapters`)
- Hermes (native adapter)
- Any MCP-compatible agent (generic)

## Architecture Notes

- **Storage:** Markdown files on disk. Entries at `<root>/YYYY/MM/icarus-<id>.md`. Wiki at `.icarus/wiki/`. Embedding cache at `.cache/embeddings/`.
- **Serialization:** YAML frontmatter + Markdown body. Human-readable, git-friendly.
- **Atomic writes:** `os.replace` with tmp file. Crash during write leaves previous version intact.
- **No binary index:** Globs the disk for lookups. Simple, git-friendly, no index corruption risk.
- **Embeddings optional:** `[embeddings]` extra. Without it, keyword-only recall works fine for small-to-medium fabrics.
- **LLM optional:** Briefing enhancement and wiki classification use gpt-4o-mini when `OPENAI_API_KEY` is set. Fall back to deterministic templates otherwise.

## Evidence

`evidence: "https://github.com/carsteneu/ai-memory-comparison/blob/main/evidence/icarus.md"`
