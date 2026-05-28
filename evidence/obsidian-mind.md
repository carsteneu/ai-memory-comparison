# obsidian-mind — Evidence & Audit Report

> **Repository:** https://github.com/breferrari/obsidian-mind
> **Audit date:** 2026-05-28
> **Auditor:** OpenCode (DeepSeek V4 Pro)
> **Sources:** README.md, ARCHITECTURE.md, vault-manifest.json, CLAUDE.md

---

## Vital Signs

| Claim | Verdict | Evidence |
|-------|---------|----------|
| webUi: true | ✅ CONFIRMED | Obsidian is an Electron app with web-based UI. README: "Home.md embeds these views, making it the vault's dashboard." Bases provide dynamic database views (Work Dashboard, Incidents, People Directory, 1:1 History, Review Evidence, Competency Map). |
| offline: true | ✅ CONFIRMED | README: "Vault-first memory keeps context across sessions and machines." All data lives in local Markdown + QMD SQLite. QMD runs locally. No cloud dependency. ARCHITECTURE.md: "The vault is the persistent state. Everything else is machinery around it." |
| privacy: false | ✅ CONFIRMED (absent) | No dedicated privacy features (content sanitization, PII filtering, private tags). Privacy is a side effect of local-first architecture, not an explicit feature. |
| export: false | ✅ CONFIRMED (absent) | No dedicated export tool. Vault files can be copied manually (it's just Markdown), but no `export` command, endpoint, or structured export format exists. |
| multiAgent: false | ✅ CONFIRMED (absent) | Subagents run within a single Claude Code session as isolated context windows. No inter-agent communication, orchestration, or swarm coordination. ARCHITECTURE.md: "Subagents in `.claude/agents/` are invoked by those commands to keep heavy operations out of the main context window." They are invoked sequentially, not as parallel agents. |
| llmFlex: 1 | ✅ CONFIRMED | QMD optionally uses ONE local model for query reranking. README: "qmd query (with LLM reranking) also downloads a ~1.28GB model on first use." Hooks are procedural TypeScript with zero LLM calls. Content generation delegates to the agent's native LLM (Claude/Codex/Gemini), which is outside the memory system boundary. |

---

## Architecture

| Claim | Verdict | Evidence |
|-------|---------|----------|
| webUi: true | ✅ CONFIRMED (covered above) | See Vital Signs. |
| offline: true | ✅ CONFIRMED (covered above) | See Vital Signs. |
| singleBinary: false | ✅ CONFIRMED (correct) | README requires: Obsidian 1.12+, Node 22+, Git, optionally QMD. Deployment involves multiple components (Obsidian app, hook scripts, QMD binary/MCP server). Not a single binary. |

---

## Data Model

| Claim | Verdict | Evidence |
|-------|---------|----------|
| schemaFields: 4 | ✅ APPROXIMATELY CORRECT | vault-manifest.json `frontmatter_required.global` = ["date", "description", "tags"] = 3. The smallest actual template (Thinking Note) adds "context" = 4 fields. Other templates: Decision Record = 5, Work Note = 6, Incident Note = 7. A memory in obsidian-mind IS a Markdown note with frontmatter; the minimal note has 4 structured fields. Claim of 4 is defensible as the smallest complete template. |
| entities: false | ✅ CONFIRMED (absent) | No structured entity extraction. People exist in `org/people/` as manually created Markdown notes, not as auto-extracted entities. No entity type system, no entity linking engine. |
| actions: false | ✅ CONFIRMED (absent) | No structured action/command/operation fields in the memory model. |
| keywords: false | ✅ CONFIRMED (absent) | Notes have `tags` in frontmatter but no dedicated keyword extraction or keyword-based learning recall system. |
| anticipatedQueries: false | ✅ CONFIRMED (absent) | No predicted search query generation. |
| triggerRules: false | ✅ CONFIRMED (absent) | Hooks classify user messages (ARCHITECTURE.md: "UserPromptSubmit classifies, it does not route") but this is for filing hints, not trigger-based recall of stored memories. No condition-based rule engine for surfacing learnings. |
| domainTag: false | ✅ CONFIRMED (absent) | No domain categories (code, marketing, legal, finance, general). |
| taskType: false | ✅ CONFIRMED (absent) | Work notes have a `status` field (frontmatter) but no task type classification (task, idea, blocked, stale). |
| context: false | ✅ CONFIRMED (absent) | Some templates have a `context` field (Decision Record, Thinking Note) for the note's body context, but no dedicated learning metadata field for "why this memory was saved." Not equivalent to YesMem's context field. |
| source: false | ✅ CONFIRMED (absent) | No source attribution system. No multi-level source tracking (user_stated, agreed_upon, claude_suggested). |
| originTrust: false | ✅ CONFIRMED (absent) | No trust weight system. All notes treated equally. |
| emotional: false | ✅ CONFIRMED (absent) | No sentiment or emotional intensity tracking. |
| conflict: false | ✅ CONFIRMED (absent) | No conflict detection between memories. |
| layeredMemory: false | ✅ CONFIRMED (absent) | brain/ folder has topic notes (North Star, Memories, Key Decisions, Patterns, Gotchas) but these are flat Markdown notes, not hierarchical memory layers (L0 raw → L1 summary → L2 persona). |
| timeTravel: false | ✅ CONFIRMED (absent) | No timeline browsing of learning versions. Git history provides versioning at the file level but no per-memory version chain with time-travel querying. |

---

## Search & Retrieval

| Claim | Verdict | Evidence |
|-------|---------|----------|
| fulltext: true | ✅ CONFIRMED | README: "falls back to grep and the Obsidian CLI" as base level. QMD provides `qmd search` which is BM25-based full-text search over indexed markdown content. Two full-text paths: grep (raw) + QMD BM25 (indexed). |
| semantic: true | ✅ CONFIRMED | QMD provides `qmd vsearch` (pure vector/semantic) and `qmd query` (semantic + LLM reranking). README: "Semantic recall. Find 'what did we decide about caching' even when the note is titled 'Redis Migration ADR.'" |
| hybrid: false | ❌ CORRECTION → **true** | QMD's `query` mode is explicitly described as "Hybrid: FTS + Vector + Query Expansion + Re-ranking" (QMD README). It combines BM25 + vector search in a single call with RRF fusion. obsidian-mind exposes this via `mcp__qmd__query` as a primary MCP tool — the agent uses it by default. ARCHITECTURE.md: "MCP server is registered, the agent's normal path to QMD is through typed tools — `mcp__qmd__query`..." |
| deep: false | ✅ CONFIRMED (absent) | No search across thinking/reasoning traces. Session logs exist in `thinking/session-logs/` but are not searchable via the memory system. |
| codeGraph: false | ✅ CONFIRMED (absent) | No code structure indexing (no AST, no Tree-sitter, no call graph). |
| docsSearch: false | ✅ CONFIRMED (absent) | No dedicated documentation search. Vault can store reference docs in `reference/` but no structured docs index. |
| factQuery: false | ✅ CONFIRMED (absent) | No structured metadata queries (e.g., "all decisions about X"). Bases provide some filtering via Obsidian's database views but are pre-defined queries, not an ad-hoc structured query interface. |
| timeline: false | ✅ CONFIRMED (absent) | No chronological timeline browsing. Session logs are stored but not time-indexed for querying. |
| dataSources: 1 | ✅ CONFIRMED | One QMD index per vault (`qmd_index: "obsidian-mind"` in vault-manifest.json). QMD indexes all vault Markdown into a single named SQLite store. ARCHITECTURE.md: "This isolates the vault from any other QMD-using vault on the same machine." Grep is a fallback, not a separate data source with its own index. |

### ⚠️ Corrections: hybrid, searchModes

| Claim | Current | Correct | Evidence |
|-------|---------|---------|----------|
| hybrid | false | **true** | QMD README labels `qmd query` as "Hybrid: FTS + Vector + Query Expansion + Re-ranking." It combines BM25 + vector search in a single call with RRF (Reciprocal Rank Fusion), then LLM re-ranking. obsidian-mind exposes this via `mcp__qmd__query` as the primary MCP search tool. ARCHITECTURE.md confirms: "the agent's normal path to QMD is through typed tools — `mcp__qmd__query`..." |
| searchModes | 2 | **3** | QMD README search modes table: `search` (BM25 full-text), `vsearch` (vector semantic only), `query` (hybrid: FTS + Vector + Query Expansion + Re-ranking). Three distinct search modes, each with its own CLI command and MCP tool. Grep is a 4th fallback path. |

---

## Knowledge Lifecycle

| Claim | Verdict | Evidence |
|-------|---------|----------|
| decay: false | ✅ CONFIRMED (absent) | No temporal decay or staleness scoring. Notes have `date` frontmatter but no decay function. |
| supersede: false | ✅ CONFIRMED (absent) | No mechanism to mark one memory as superseding another. Decision Records have a `status` field (proposed/accepted/deprecated) but no cross-reference supersede relation. |
| contradiction: false | ✅ CONFIRMED (absent) | No contradiction detection between notes. |
| quarantine: false | ✅ CONFIRMED (absent) | No session or learning quarantine mechanism. |
| autoResolve: false | ✅ CONFIRMED (absent) | No automatic task/conflict resolution. |
| trustModel: false | ✅ CONFIRMED (absent) | No trust hierarchy between sources. |
| explicitForget: false | ✅ CONFIRMED (absent) | No dedicated forget/delete command for memories. Notes can be deleted manually in Obsidian or via file system, but no structured forget operation with audit trail. |

---

## Extraction Pipeline

| Claim | Verdict | Evidence |
|-------|---------|----------|
| autoExtract: false | ✅ CONFIRMED (absent) | `UserPromptSubmit` hook classifies messages (decision, incident, win, 1:1, etc.) but this produces routing hints, not extracted learnings. ARCHITECTURE.md: "classifies, it does not route." The agent must explicitly decide what to save and where. No automatic structured knowledge extraction from conversations. |
| contentPreproc: false | ✅ CONFIRMED (absent) | No content-aware truncation or type-specific preprocessing. |
| dedup: false | ✅ CONFIRMED (absent) | QMD skill instructs the agent to check for duplicates before creating notes (README: "before creating notes (to check for duplicates)"), but this is a procedural instruction to the agent, not an automatic dedup system with hash-based detection and merging. No automatic duplicate merging in the hooks or QMD layer. |
| qualityRefine: false | ✅ CONFIRMED (absent) | No LLM-based quality refinement pass on saved notes. |
| narrative: false | ✅ CONFIRMED (absent) | Session logs are stored in `thinking/session-logs/` but no automatic session summary generation. `/om-wrap-up` generates summaries on explicit user invocation. Per CRITERIA: "auto-generates narrative session summaries" — not met. |
| clustering: false | ✅ CONFIRMED (absent) | No topic clustering by similarity. |
| recurrence: false | ✅ CONFIRMED (absent) | No recurring pattern detection. `brain/Patterns.md` is manually curated by the agent. |
| persona: false | ✅ CONFIRMED (absent) | No persona extraction. `brain/North Star.md` is user-authored, not extracted. |

---

## Platform Support

| Claim | Verdict | Evidence |
|-------|---------|----------|
| p_claude: true | ✅ CONFIRMED | README: "Claude Code — full support." Badge: "Claude Code full support." ARCHITECTURE.md: Hooks, commands, subagents, and memory system all work out of the box. `.claude/settings.json` with 5 lifecycle hooks. 18 commands in `.claude/commands/`. 9 subagents in `.claude/agents/`. |
| p_codex: true | ✅ CONFIRMED | README: "Codex CLI — hooks + commands." Badge: "codex cli hooks + commands." ARCHITECTURE.md: "Hook config at `.codex/hooks.json` wires the same hook scripts Claude Code uses." Commands work as regular prompts. |
| p_gemini: true | ✅ CONFIRMED | README: "Gemini CLI — hooks + commands." Badge: "gemini cli hooks + commands." ARCHITECTURE.md: "Hook config at `.gemini/settings.json` maps Gemini's event names to the shared hook scripts." |
| p_opencode: false | ✅ CONFIRMED (absent) | No OpenCode-specific integration. No opencode.json config, no plugin, no MCP setup for OpenCode. |
| p_copilot: false | ✅ CONFIRMED (absent) | No GitHub Copilot CLI integration. |
| p_cursor: false | ✅ CONFIRMED (absent) | README: "Other agents (Cursor, Windsurf, GitHub Copilot, JetBrains AI) — read `AGENTS.md` for vault conventions. Hook support varies by agent." No dedicated Cursor integration — AGENTS.md provides conventions only, no hooks. |
| p_windsurf: false | ✅ CONFIRMED (absent) | Same as Cursor — AGENTS.md conventions only. |
| p_openclaw: false | ✅ CONFIRMED (absent) | Not mentioned anywhere. |
| p_hermes: false | ✅ CONFIRMED (absent) | Not mentioned anywhere. |
| p_pi: false | ✅ CONFIRMED (absent) | Not mentioned anywhere. |
| p_antigravity: false | ✅ CONFIRMED (absent) | Not mentioned anywhere. |

---

## Summary

All claimed ✅ features verified. **2 corrections identified:**

1. **hybrid** should be **true** (QMD's `query` mode is explicitly a hybrid BM25+vector pipeline with RRF fusion, exposed via `mcp__qmd__query` as the primary MCP tool)
2. **searchModes** should be **3** (QMD has three distinct search modes: `search` BM25, `vsearch` vector, `query` hybrid+rerank)

All absent claims verified correct. No features found that contradict the absent claims.

Note on schemaFields: Claim is 4. Vault-manifest.json global required = 3 (date, description, tags). The Thinking Note template (smallest) has 4 fields (adds "context"). Most templates have 5-7. Marked as approximately correct — 4 is the minimal usable template, though the global minimum is 3.

---

## Evidence URL

```
evidence: "https://github.com/carsteneu/ai-memory-comparison/blob/main/evidence/obsidian-mind.md"
```
