# Octopoda-OS — Audit Evidence

**Date**: 2026-05-28
**Source**: https://github.com/RyjoxTechnologies/Octopoda-OS
**License**: MIT (confirmed in pyproject.toml)
**Version**: 3.2.2 (pyproject.toml)
**Stars**: 337
**Language**: Python 95.7%, C 1.8%, JS 0.8%
**Created**: 2026-04-02
**Website**: https://octopodas.com

> Note: The URL `https://github.com/toc-framework/octopoda` provided in the task does not exist (404). The actual repository is `https://github.com/RyjoxTechnologies/Octopoda-OS`.

---

## Claim-by-Claim Audit

### Infrastructure & Core

| Claim | Verdict | Evidence |
|-------|---------|----------|
| **webUi** | TRUE | Local dashboard at `http://localhost:7842` (`pip install octopoda[server]`), cloud dashboard at octopodas.com/dashboard. Screenshots in README show agent performance, memory explorer, and audit trail views. |
| **offline** | TRUE | Local-first with SQLite at `~/.synrix/data/synrix.db`. Runs without API key. The entry `offline: true` is correct. |
| **privacy** | PARTIAL (local only) | Local mode: data stays on machine. Cloud mode: data sent to octopodas.com. The `openclaw-skill` README states "All memory stored in your isolated Octopoda account (separate database per user)". Not a fully offline-only privacy model. Recommend: `true` with note "local mode only". |
| **export** | TRUE | `agent.export_memories()` returns a bundle, `agent.import_memories(bundle)` imports. Confirmed in README "Export / Import" section. The entry `export: false` needs correction to `true`. |
| **singleBinary** | FALSE (correct) | Python package via pip, not a single binary. |

### Schema Fields

The memory model is key-value based (`remember("user_name", "Alice")`). The README does not enumerate formal schema fields. Memory entries appear to have: key, value, agent name, version, timestamp.

| Claim | Verdict | Evidence |
|-------|---------|----------|
| **entities** | FALSE (correct) | No entity extraction mentioned in README. The NLP extra (`octopoda[nlp]`) mentions "knowledge graph extraction" which could imply entities, but this is not part of the core memory schema. |
| **keywords** | FALSE (correct) | Not mentioned as a schema field. |
| **taskType** | FALSE (correct) | Not mentioned. |
| **context** | PARTIAL | Context captured in `log_decision(context={...})` for audit trail, but not a general-purpose memory schema field. Not the same as a per-memory context metadata field. |
| **source** | FALSE (correct) | Not mentioned as metadata on memory entries. |
| **layeredMemory** | FALSE (correct) | No explicit layer system (working/session/long-term). Version history exists for individual keys, but that's versioning, not layering. |
| **timeTravel** | PARTIAL | `agent.snapshot()` and `agent.restore()` provide checkpoint-based time travel. Version history (`recall_history`) lets you see old values. Not labeled "time travel" but functionally similar. Recommend: note "via snapshots + version history". |
| **schemaFields=12** | OVERCLAIM | Not verifiable from README. The core memory model is key-value. Even counting all optional metadata (version, timestamp, agent, space, author, message_type), 12 is not supported by the documentation. Recommend: 5-6 fields (key, value, agent, version, timestamp, optional space). |

### Search

| Claim | Verdict | Evidence |
|-------|---------|----------|
| **fulltext** | LIKELY TRUE | `agent.search()` in cloud mode. MCP `octopoda_search` tool. The README doesn't specify "fulltext" explicitly, but a search method exists. PostgreSQL-backed search in cloud mode would support fulltext. |
| **semantic** | TRUE | `agent.recall_similar()` for meaning-based search. Local embeddings via `octopoda[ai]` (sentence-transformers, BAAI/bge-small-en-v1.5). Cloud mode has built-in embeddings. MCP has `octopoda_recall_similar`. The entry `semantic: true` is correct. |
| **timeline** | PARTIAL | Audit trail shows chronological timeline of decisions/crashes/recoveries. Version history shows changes over time. Not a dedicated timeline view for all memories. |
| **searchModes=3** | TRUE (generous) | Evidence: `search()` (lexical/fulltext), `recall_similar()` (semantic/vector), `search_filtered()` (filtered search). That's 3 distinct search modes. The entry `searchModes: 1` needs correction to `3`. |

### Lifecycle

| Claim | Verdict | Evidence |
|-------|---------|----------|
| **decay** | TRUE (manual) | `agent.forget_stale(max_age_seconds=30*86400)` removes memories older than a threshold. This is explicit cleanup, not automatic decay. Functionally equivalent for the comparison. Recommend: mark as true with note "manual age-based cleanup, not automatic decay". |
| **supersede** | TRUE (versioning) | All memories are "versioned by default" per README. Version history (`recall_history`) lets you see old values. `consolidate()` merges near-duplicates. Recommend: mark as true. |
| **explicitForget** | TRUE | `agent.forget("outdated_config")` deletes specific memories. The entry `explicitForget: false` needs correction to `true`. |

### Intelligence

| Claim | Verdict | Evidence |
|-------|---------|----------|
| **autoExtract** | TRUE | "AI extractions" in pricing tiers (100 free, up to Unlimited on Scale). NLP extra installs spaCy for "knowledge graph extraction". The `openclaw-skill` README: "the conversation is stored with automatic fact extraction". The entry `autoExtract: false` needs correction to `true`. |
| **dedup** | TRUE | `agent.consolidate(dry_run=False)` merges near-duplicates. The entry `dedup: false` needs correction to `true`. |
| **qualityRefine** | FALSE (correct) | No quality refinement or content preprocessing mentioned. |
| **narrative** | FALSE (correct) | No narrative construction mentioned. |
| **persona** | FALSE (correct) | No persona/profile system mentioned. |

### Platform Support

| Claim | Verdict | Evidence |
|-------|---------|----------|
| **p_claude** | TRUE | MCP server supports Claude Code (`claude mcp add octopoda ...`) and Claude Desktop (`claude_desktop_config.json`). |
| **p_codex** | FALSE (correct) | Not mentioned in README or pyproject.toml. |
| **p_opencode** | FALSE (correct) | Not mentioned. |
| **p_gemini** | FALSE (correct) | Not mentioned. |
| **p_cursor** | TRUE | MCP server section: "Give Claude, Cursor, or any MCP-compatible AI persistent memory". |
| **p_windsurf** | FALSE (correct) | Not mentioned. |
| **p_openclaw** | TRUE | `openclaw-skill/` directory exists in repo with dedicated README, install script, and SKILL.md. Confirmed via GitHub directory listing. The entry `p_openclaw: false` needs correction to `true`. |
| **p_pi** | FALSE (correct) | Not mentioned. |
| **p_antigravity** | FALSE (correct) | Not mentioned. |

---

## Summary of data.js Corrections Needed

### Fields to change:

| Field | Current | Correct | Evidence |
|-------|---------|---------|----------|
| `license` | `"?"` | `"MIT"` | pyproject.toml: `license = {text = "MIT"}` |
| `webUi` | `false` | `true` | Local dashboard localhost:7842 + cloud dashboard octopodas.com/dashboard |
| `export` | `false` | `true` | `export_memories()` / `import_memories()` |
| `integration` | `"?"` | `"Python SDK, MCP, LangChain, CrewAI, AutoGen, OpenAI Agents SDK"` | README framework integrations section |
| `storage` | `"?"` | `"SQLite (local), PostgreSQL+pgvector (cloud)"` | README Local vs Cloud table |
| `setup` | `"?"` | `"pip install octopoda"` | README quick start |
| `deployment` | `"Local server"` | Could add "Local server + Cloud" | README describes both modes |
| `explicitForget` | `false` | `true` | `agent.forget()` |
| `autoExtract` | `false` | `true` | AI extractions + NLP knowledge graph |
| `dedup` | `false` | `true` | `agent.consolidate()` |
| `searchModes` | `1` | `3` | search + recall_similar + search_filtered |
| `schemaFields` | `4` | `5` | key, value, agent, version, timestamp (conservative estimate) |
| `p_openclaw` | `false` | `true` | openclaw-skill directory in repo |

### Fields to keep as-is (verified correct):

- `offline: true`, `semantic: true`, `p_claude: true`, `p_cursor: true`
- All `false` entries for unsupported platforms: p_codex, p_opencode, p_gemini, p_windsurf, p_pi, p_antigravity
- All `false` entries for unsupported features: entities, keywords, taskType, source, layeredMemory, qualityRefine, narrative, persona

### Fields to consider:

- `privacy`: could be `true` with note "local mode", currently `false`. Depends on comparison methodology.
- `decay`: `forget_stale()` exists but is manual. Could argue either way.
- `supersede`: versioning exists. Recommend `true`.
- `timeTravel`: snapshots + restore exist. Recommend `true` with note.
- `context`: partial support via log_decision. Not a general schema field.
- `fulltext`: `search()` exists. Recommend `true`.
- `timeline`: audit trail timeline exists. Recommend `true` with note.

---

## Other Findings

### MCP Tool Count Inconsistency
The README comparison table says "29 tools" for MCP server. The detailed tool list in the MCP section shows 28 tools. Discrepancy of 1.

### Verification Harnesses
The repo includes 4 integration test scripts (`scripts/integration/`) exercising the product against both PyPI install and live api.octopodas.com. This is unusual and indicates real functionality, not just documentation.

### OpenClaw Integration
The `openclaw-skill/` directory includes a full skill with install script, SKILL.md, and natural language command support. This is a concrete, working integration — not just a compatibility claim.

### Package Structure
The package name is `octopoda` but the runtime lives in `synrix_runtime/` and `synrix/` directories. SQLite data goes to `~/.synrix/data/synrix.db`. The branding split (Octopoda product name, Synrix internal name) suggests prior rebranding or internal codename.

### Cloud Dependency
Most features described in README work locally, but some (semantic search without `[ai]` extra, cloud dashboard) require either additional installs or the cloud service. This is transparently documented, so it's not deceptive, but worth noting for the "offline" claim: local mode is genuine but some power features need the AI extra or cloud.

### Pricing
Free tier: 5 agents, 5,000 memories, 100 AI extractions, 60 rpm, basic loop detection. Paid tiers from $19/mo to $99/mo.
