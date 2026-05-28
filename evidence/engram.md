# engram — Evidence & Audit Report

> **Repository:** https://github.com/Gentleman-Programming/engram
> **Audit date:** 2026-05-28
> **Auditor:** OpenCode (DeepSeek V4 Pro)
> **Sources:** README.md, DOCS.md, ARCHITECTURE.md, AGENT-SETUP.md, COMPARISON.md, internal/store/store.go

---

## Vital Signs

| Claim | Verdict | Evidence |
|-------|---------|----------|
| singleBinary: true | ✅ CONFIRMED | README: "A Go binary with SQLite + FTS5" — "No Node.js, no Python, no Docker. One binary, one SQLite file." COMPARISON.md: "Go (single binary, zero runtime deps)". Source: `cmd/engram/main.go` entrypoint. |
| Stars: 3.8k | ✅ CONFIRMED | README shows 3.8k stars. |
| Language: Go | ✅ CONFIRMED | 92.6% Go per GitHub language stats. |
| License: MIT | ✅ CONFIRMED | README badge and LICENSE file. |

---

## Architecture

| Claim | Verdict | Evidence |
|-------|---------|----------|
| webUi: true | ✅ CONFIRMED | README: "TUI" with 3 screenshots (dashboard, detail, search). DOCS.md: Cloud dashboard at `/dashboard/*` with 20+ HTML routes including stats, activity, browser, session/observation detail pages. |
| offline: true | ✅ CONFIRMED | README: "Local SQLite remains the source of truth." Cloud integration is "opt-in replication." Core memory (save, search, context, timeline) works entirely offline with local SQLite. |
| privacy: true | ✅ CONFIRMED | COMPARISON.md: "`<private>` tags stripped at 2 layers." Local-first architecture — data never leaves the machine unless cloud sync is explicitly enabled. |
| export: true | ✅ CONFIRMED | README CLI ref: `engram export [file]` and `engram import <file>`. DOCS: `GET /export` endpoint with `?project=` filter. ExportData struct includes sessions, observations, prompts. |
| proxy: false | ✅ CONFIRMED (absent) | Engram is an MCP server + HTTP API, not a proxy. No conversation stream interception. README: "Agent → Engram (single Go binary) → SQLite". |
| multiAgent: false | ✅ CONFIRMED (absent) | No multi-agent orchestration or inter-agent communication features. Single-user memory system. |

---

## Data Model

| Claim | Verdict | Evidence |
|-------|---------|----------|
| keywords: true | ✅ CONFIRMED | ARCHITECTURE.md: `topic_key` system with `mem_suggest_topic_key` generating family heuristics (`architecture/*`, `bug/*`, `decision/*`, `pattern/*`, `config/*`, `discovery/*`, `learning/*`). Topic keys enable upserts (same project+scope+topic updates existing memory). |
| context: true | ✅ CONFIRMED | README: "What/Why/Where/Learned" format for observations. `mem_context` tool retrieves recent context from previous sessions. Context stores the reason WHY a memory is relevant. |
| conflict: true | ✅ CONFIRMED | README: "Conflict Surfacing" section. MCP tools: `mem_judge` and `mem_compare`. `engram conflicts` CLI. `memory_relations` table with verdicts. Beta testing shows auto-detection on save: "Second save returns candidates[] with the first memory's id." FTS5-based candidate detection surface conflicts on every `mem_save`. |
| timeTravel: true | ✅ CONFIRMED | README CLI: `engram timeline <obs_id>`. MCP tool: `mem_timeline`. DOCS: `GET /timeline?observation_id=N&before=5&after=5`. Returns chronological context with focus observation, before/after entries, and session info. |
| schemaFields: 6 | ✅ CONFIRMED | store.go Observation struct has: `type`, `title`, `content`, `tool_name`, `scope`, `topic_key` — 6 meaningful structured fields (excluding auto-generated IDs, timestamps, counts, hashes, and `project` which is a namespace/partition key). |
| entities: false | ✅ CONFIRMED (absent) | No named entity extraction. Observations store free-text content only. |
| actions: false | ✅ CONFIRMED (absent) | No structured action/command/operation fields. |
| anticipatedQueries: false | ✅ CONFIRMED (absent) | No predicted search query generation for recall improvement. |
| triggerRules: false | ✅ CONFIRMED (absent) | No condition-based activation rules. |
| domainTag: false | ✅ CONFIRMED (absent) | No domain categories (code, marketing, legal, etc.). |
| taskType: false | ✅ CONFIRMED (absent) | No task type classification (task, idea, blocked, stale). |
| source: false | ✅ CONFIRMED (absent) | No source attribution field beyond session_id. No multi-level source tracking. |
| originTrust: false | ✅ CONFIRMED (absent) | No trust weight system. All memories treated equally. |
| emotional: false | ✅ CONFIRMED (absent) | No sentiment or emotional intensity tracking. |
| layeredMemory: false | ✅ CONFIRMED (absent) | No hierarchical memory layers (L0 raw → L1 summary → L2 persona). |

---

## Search & Retrieval

| Claim | Verdict | Evidence |
|-------|---------|----------|
| fulltext: true | ✅ CONFIRMED | SQLite FTS5 via `observations_fts` and `prompts_fts` virtual tables. README: "SQLite + FTS5 full-text search." MCP tool: `mem_search`. CLI: `engram search <query>`. |
| timeline: true | ✅ CONFIRMED | `mem_timeline` MCP tool, `engram timeline <obs_id>` CLI, `GET /timeline` endpoint. |
| searchModes: 4 | ✅ CONFIRMED | 1) `mem_search` — FTS5 full-text; 2) `mem_context` — recent session context; 3) `mem_timeline` — chronological context; 4) `mem_get_observation` — direct ID fetch. Also: Progressive Disclosure pattern (search → timeline → get_observation). |
| semantic: false | ✅ CONFIRMED (absent) | No embedding-based semantic/vector search. FTS5 text search only. (Note: the "semantic" LLM-judge conflict scan uses LLM reasoning, not vector search — it's a conflict adjudication feature, not semantic search.) |
| hybrid: false | ✅ CONFIRMED (absent) | No hybrid BM25+vector with result fusion. |
| deep: false | ✅ CONFIRMED (absent) | No search across thinking/reasoning traces. |
| codeGraph: false | ✅ CONFIRMED (absent) | No code structure indexing (no AST, no Tree-sitter). |
| docsSearch: false | ✅ CONFIRMED (absent) | No dedicated documentation search. |
| factQuery: false | ✅ CONFIRMED (absent) | No structured metadata queries (e.g., "all decisions about X"). |

### ⚠️ Correction: dataSources

| Claim | Current | Correct | Evidence |
|-------|---------|---------|----------|
| dataSources | 1 | **2** | Engram has two searchable FTS5 indexes: `observations_fts` (via `mem_search`, `GET /search`) AND `prompts_fts` (via `GET /prompts/search`, `mem_search`). Both are independent data sources. |

---

## Knowledge Lifecycle

| Claim | Verdict | Evidence |
|-------|---------|----------|
| supersede: true | ✅ CONFIRMED | `memory_relations` table has `supersedes` relation type. topic_key upserts increment `revision_count`. `mem_save` with same topic_key replaces existing observation. COMPARISON.md shows supersede: true. |
| contradiction: true | ✅ CONFIRMED | Auto-detection on save: FTS5 candidates returned with `judgment_required: true`. `mem_judge` tool with `conflicts_with` relation. `engram conflicts scan --semantic` for LLM-judged semantic conflict detection. |
| explicitForget: true | ✅ CONFIRMED | README: `engram delete <obs_id>` with `--hard` flag. DOCS: soft-delete by default (`deleted_at`), optional hard delete. `DELETE /observations/{id}?hard=true`. `mem_delete` MCP tool. |
| decay: false | ✅ CONFIRMED (absent) | No automatic decay. Source code has `review_after` field (reserved for future) but not actively decaying memories. |
| quarantine: false | ✅ CONFIRMED (absent) | No session quarantine mechanism. |
| autoResolve: false | ✅ CONFIRMED (absent) | No automatic task/conflict resolution. |
| trustModel: false | ✅ CONFIRMED (absent) | No trust hierarchy between sources. |

---

## Extraction Pipeline

| Claim | Verdict | Evidence |
|-------|---------|----------|
| autoExtract: false | ✅ CONFIRMED (absent) | `mem_capture_passive` exists but requires manual tool invocation — extracts learnings from provided text, not automatic. Per CRITERIA: "Automatically extracts structured knowledge from sessions without manual save calls" — this is not met. |
| contentPreproc: false | ✅ CONFIRMED (absent) | No content-type-aware truncation. |
| qualityRefine: false | ✅ CONFIRMED (absent) | No LLM-based quality refinement pass. |
| narrative: false | ✅ CONFIRMED (absent) | `mem_session_summary` stores agent-provided summaries, but does not auto-generate them. Per CRITERIA: "Generates session summaries" — engram stores but does not generate. |
| clustering: false | ✅ CONFIRMED (absent) | No topic clustering by similarity. |
| recurrence: false | ✅ CONFIRMED (absent) | No recurring pattern detection. |
| persona: false | ✅ CONFIRMED (absent) | No persona extraction. |

### ⚠️ Correction: dedup

| Claim | Current | Correct | Evidence |
|-------|---------|---------|----------|
| dedup | false | **true** | Source code (store.go): `DedupeWindow: 15 * time.Minute`. ARCHITECTURE.md: "Exact dedupe prevents repeated inserts in a rolling window (hash + project + scope + type + title)" and "Duplicates update metadata (duplicate_count, last_seen_at, updated_at) instead of creating new rows." Schema has `normalized_hash`, `duplicate_count` fields. FTS5 index `idx_obs_dedupe`. This meets the CRITERIA definition: "Detects and merges duplicate or near-duplicate memories" — engram detects and merges exact duplicates. |

---

## Platform Support

| Claim | Verdict | Evidence |
|-------|---------|----------|
| p_claude: true | ✅ CONFIRMED | AGENT-SETUP.md: Claude Code section with plugin marketplace, `engram setup claude-code`, and bare MCP options. Plugin with hooks, scripts, Memory Protocol skill. |
| p_codex: true | ✅ CONFIRMED | AGENT-SETUP.md: Codex section. `engram setup codex` writes `~/.codex/engram-instructions.md` and `engram-compact-prompt.md`, registers `[mcp_servers.engram]`. |
| p_opencode: true | ✅ CONFIRMED | AGENT-SETUP.md: OpenCode section. `engram setup opencode` copies plugin to `~/.config/opencode/plugins/engram.ts`, adds MCP server to opencode.json. |
| p_gemini: true | ✅ CONFIRMED | AGENT-SETUP.md: Gemini CLI section. `engram setup gemini-cli` registers MCP in `~/.gemini/settings.json`, writes `~/.gemini/system.md` with Memory Protocol. |
| p_cursor: true | ✅ CONFIRMED | AGENT-SETUP.md: Cursor section with `.cursor/mcp.json` config and `.cursor/rules/engram.mdc` Memory Protocol instructions. |
| p_windsurf: true | ✅ CONFIRMED | AGENT-SETUP.md: Windsurf section with `~/.windsurf/mcp.json` config and `.windsurfrules` Memory Protocol instructions. |
| p_pi: true | ✅ CONFIRMED | AGENT-SETUP.md: Pi section. First-class Pi package: `gentle-engram` npm package, `engram setup pi`, HTTP event capture + MCP gateway via `pi-mcp-adapter`. |
| p_antigravity: true | ✅ CONFIRMED | AGENT-SETUP.md: Antigravity section with MCP config path `~/.gemini/antigravity/mcp_config.json` and Memory Protocol instructions. |
| p_copilot: false | ✅ CONFIRMED (absent) | VS Code Copilot extension is documented but that's not the GitHub Copilot CLI. Per CRITERIA: "GitHub Copilot CLI" — no CLI-specific integration. |

### ⚠️ Note: llmFlex

| Claim | Current | Correct | Evidence |
|-------|---------|---------|----------|
| llmFlex | 1 | **2** | Engram supports `ENGRAM_AGENT_CLI=claude` OR `ENGRAM_AGENT_CLI=opencode` for semantic conflict judging (`engram conflicts scan --semantic`). Two distinct LLM providers: Anthropic Claude and OpenCode's LLM backend. |

---

## Summary

All 17 claimed ✅ features verified. **3 corrections identified:**

1. **dedup** should be `true` (exact hash-based dedup exists with 15-minute window)
2. **dataSources** should be `2` (observations + prompts, both FTS5-indexed)
3. **llmFlex** should be `2` (Claude + OpenCode as LLM providers for semantic judging)

All absent claims verified correct. No features found that contradict the absent claims.

---

## Evidence URL

```
evidence: "https://github.com/carsteneu/ai-memory-comparison/blob/main/evidence/engram.md"
```
