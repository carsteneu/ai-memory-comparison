# Stash — Evidence & Audit Report

> **Repository:** https://github.com/alash3al/stash
> **Audit date:** 2026-05-28
> **Auditor:** OpenCode (DeepSeek V4 Pro)
> **Sources:** README.md, docs/index.html, docs/GETTING_STARTED.md, cmd/cli/mcp.go, internal/models/models.go, internal/brain/consolidate.go, internal/brain/decay.go, internal/brain/recall.go, internal/db/migrations/*.sql

---

## Vital Signs

| Claim | Verdict | Evidence |
|-------|---------|----------|
| singleBinary: true | ⚠️ PARTIAL (needs Postgres) | Stash server is a single Go binary (`cmd/cli/main.go`). README: "Self-hosted, single binary, no cloud required." However, it REQUIRES PostgreSQL + pgvector as a backend — docker-compose.yml runs both stash and postgres. Not standalone like SQLite-based systems. |
| Stars: 702 | ✅ CONFIRMED | GitHub shows 702 stars. |
| Language: Go | ✅ CONFIRMED | 80.8% Go per GitHub language stats. go.mod confirms. |
| License: Apache 2.0 | ✅ CONFIRMED | README badge and LICENSE file. |

---

## Architecture

| Claim | Verdict | Evidence |
|-------|---------|----------|
| webUi: false | ✅ CONFIRMED (absent) | No web dashboard. docs/index.html is a static marketing page. No admin UI, TUI, or web viewer in source. |
| offline: true | ⚠️ PARTIAL (needs local Postgres + local LLM) | Can run offline using local Postgres, local Ollama models. Default setup needs API key. docker-compose.yml bundles Postgres. .env.example shows Ollama config: `STASH_OPENAI_BASE_URL=http://localhost:11434/v1`. |
| proxy: false | ✅ CONFIRMED (absent) | Stash is an MCP SSE server, not a conversation proxy. No stream interception. |
| multiAgent: false | ✅ CONFIRMED (absent) | No multi-agent orchestration, inter-agent communication, or swarm features. Single server per Postgres instance. |

---

## Data Model

| Claim | Verdict | Evidence |
|-------|---------|----------|
| entities: false → **true** | ❌ CORRECTION | Fact model has `entity`, `property`, `value` as structured optional columns (migration 00013: `ALTER TABLE facts ADD COLUMN entity/property/value TEXT`). models.go: Fact.Entity/Property/Value as `*string`. These are free-text fields, not a junction table, but they ARE entity-property-value extraction. |
| actions: false | ✅ CONFIRMED (absent) | No structured action/command/operation fields. |
| keywords: false | ✅ CONFIRMED (absent) | No tag/keyword system. No topic_key equivalent. |
| anticipatedQueries: false | ✅ CONFIRMED (absent) | No predicted query generation for recall improvement. |
| triggerRules: false | ✅ CONFIRMED (absent) | No condition-based activation rules. |
| domainTag: false | ✅ CONFIRMED (absent) | No domain classification. |
| taskType: false | ⚠️ PARTIAL (goals, not task types) | No taskType field (task/idea/blocked/stale). But stash has Goals with statuses (active/completed/abandoned) which partially overlaps. |
| context: true | ✅ CONFIRMED | `set_context`, `get_context`, `clear_context` MCP tools. Context model: focus string + expires_at per namespace. contexts table (migration 00009). |
| source: false | ✅ CONFIRMED (absent) | No source attribution field. Fact_Sources links facts to episodes but no multi-tier source tracking. |
| originTrust: false | ✅ CONFIRMED (absent) | No trust weight/level system. |
| emotional: false | ✅ CONFIRMED (absent) | No sentiment or emotional intensity tracking. |
| conflict: false → **true** | ❌ CORRECTION | contradictions table (migration 00014) with entity/property/old_value/new_value. Contradiction detection during consolidation stage 1 (consolidate.go: "Stage 4: Contradiction detection"). Tools: `list_contradictions`, `resolve_contradiction`. |
| layeredMemory: false → **true** | ❌ CORRECTION | 3-layer hierarchy: Episodes (raw, append-only) → Facts (LLM-synthesized beliefs with confidence) → Patterns (higher-order abstractions over facts+relationships). README: "Episodes become facts. Facts become relationships. Relationships become patterns." consolidate.go has all 3 stages. |
| timeTravel: false | ✅ CONFIRMED (absent) | `valid_from`/`valid_until` on facts for temporal scoping, but no session replay, timeline browsing, or frame rewinding. |
| schemaFields: 6 → **7** | ⚠️ CORRECTION | Fact has 7 meaningful structured fields: `content`, `confidence`, `entity`, `property`, `value`, `valid_from`, `valid_until`. (Excluding infrastructure: id, namespace_id, embedding, embedding_model, created_at, updated_at, deleted_at.) |

---

## Search & Retrieval

| Claim | Verdict | Evidence |
|-------|---------|----------|
| fulltext: true → **false** | ❌ CORRECTION | No FTS index on any table. No tsvector, no FTS5, no trigram index. Migrations show only btree indexes. recall.go uses pgvector `<=>` operator for semantic similarity only — pure vector search. |
| semantic: true | ✅ CONFIRMED | pgvector-based semantic search via `recall` tool. recall.go: `SELECT ... ORDER BY embedding <=> $2` with cosine distance. Configurable embedding model, cached embeddings. |
| hybrid: false | ✅ CONFIRMED (absent) | No BM25+vector hybrid with result fusion (RRF). |
| deep: false | ✅ CONFIRMED (absent) | No search across thinking/reasoning traces. |
| codeGraph: false | ✅ CONFIRMED (absent) | No code structure indexing. |
| docsSearch: false | ✅ CONFIRMED (absent) | No documentation search. |
| factQuery: false → **true** | ❌ CORRECTION | `query_facts` MCP tool exists: queries facts by namespace with pagination. Also `query_relationships` tool. |
| timeline: false | ✅ CONFIRMED (absent) | No timeline view or chronological context browsing. Facts have `valid_from`/`valid_until` but no timeline tool. |

---

## Knowledge Lifecycle

| Claim | Verdict | Evidence |
|-------|---------|----------|
| decay: false → **true** | ❌ CORRECTION | DecayConfidence in decay.go: `confidence = confidence * decay_factor` for facts not re-observed within configurable window. Facts below expiry threshold auto-expired (`valid_until = now()`). Configurable via DecayFactor, ExpiryThreshold, Window. Pure SQL, no LLM. |
| supersede: false → ⚠️ PARTIAL | ⚠️ CORRECTION | No explicit supersede chain (like YesMem learning versions). But contradictions track `old_fact_id`/`new_fact_id` and auto-resolution effectively replaces older facts. Not a full supersede mechanism. |
| contradiction: false → **true** | ❌ CORRECTION | See conflict above. Contradictions table, detection during fact creation, auto-resolution possible. |
| quarantine: false | ✅ CONFIRMED (absent) | No session quarantine mechanism. |
| autoResolve: false → **true** | ❌ CORRECTION | contradictions_auto_resolved in consolidation results. Decay auto-expires low-confidence facts below ExpiryThreshold. Hypothesis auto-confirm/reject based on confidence thresholds. |
| trustModel: false | ✅ CONFIRMED (absent) | No trust hierarchy or provenance weighting. |
| explicitForget: false → **true** | ❌ CORRECTION | `forget` MCP tool: soft-deletes episodes by content search across namespaces. models.go shows `deleted_at` on episodes, facts, relationships, patterns, goals, hypotheses. |

---

## Extraction Pipeline

| Claim | Verdict | Evidence |
|-------|---------|----------|
| autoExtract: false → **true** | ❌ CORRECTION | 8-stage consolidation pipeline runs automatically in background (runConsolidationTicker in mcp.go), configurable interval. Manual trigger also via `consolidate` tool. Stages: Episodes→Facts, Facts→Relationships, Facts→CausalLinks, GoalProgress, FailurePatterns, Facts+Rels→Patterns, HypothesisScan, ConfidenceDecay. |
| contentPreproc: false | ✅ CONFIRMED (absent) | No content-aware preprocessing or truncation. |
| dedup: false → **true** | ❌ CORRECTION | factExistsByVector: cosine similarity check against existing facts before inserting. `facts_deduplicated` in consolidation results. Configurable DedupThreshold. |
| qualityRefine: false → **true** | ❌ CORRECTION | LLM-based fact synthesis in consolidation stage 1: `reasoner.ReasonStructured()` extracts structured facts (entity/property/value + summary) from clustered episodes with confidence scoring. |
| narrative: false | ✅ CONFIRMED (absent) | No session summary or narrative generation. |
| clustering: false → **true** | ❌ CORRECTION | clusterEpisodes in consolidate.go: cosine similarity grouping with configurable SimilarityThreshold. Episodes within threshold are clustered before LLM synthesis. |
| recurrence: false → **true** | ❌ CORRECTION | Failure Pattern Detection (consolidation stage 5): `consolidateFailurePatterns` in consolidate_failure.go detects repeated mistakes. `failure_repeats_detected`, `failure_patterns_found` in results. |
| persona: false → ⚠️ PARTIAL | ⚠️ CORRECTION | `init` tool creates `/self` namespace hierarchy with capabilities, limits, preferences. Agent self-model infrastructure exists. However, it's scaffold-based (manual init), not auto-extracted persona from behavior. |

---

## Platform Support

| Claim | Verdict | Evidence |
|-------|---------|----------|
| p_claude: true | ✅ CONFIRMED | README lists Claude Desktop MCP config. docs/index.html: "Claude Desktop" section with `claude_desktop_config.json`. |
| p_codex: false | ✅ CONFIRMED (absent) | Codex not listed in supported clients. |
| p_opencode: true | ✅ CONFIRMED | README lists OpenCode MCP config: `~/.config/opencode/config.json` with `type: "remote"`. |
| p_gemini: false | ✅ CONFIRMED (absent) | Not listed in supported clients. |
| p_cursor: true | ✅ CONFIRMED | README lists Cursor MCP config: `~/.cursor/mcp.json`. |
| p_windsurf: true | ✅ CONFIRMED | README lists Windsurf MCP config: `~/.codeium/windsurf/mcp_config.json`. |
| p_copilot: false | ✅ CONFIRMED (absent) | Not listed in supported clients. |

---

## MCP Tools (28 confirmed)

mcp.go registers these tools:

1. `init` — create /self namespace scaffold
2. `remember` — store episode by content + namespace
3. `recall` — semantic search (pgvector) across episodes + facts
4. `forget` — soft-delete episodes by content match
5. `consolidate` — run 8-stage pipeline manually
6. `set_context` — write active working context per namespace
7. `get_context` — read active working context
8. `clear_context` — clear working context
9. `list_namespaces` — list namespaces with pagination
10. `create_namespace` — create a namespace (slug + name + description)
11. `query_facts` — list facts by namespace
12. `query_relationships` — list relationships by namespace
13. `list_contradictions` — list detected contradictions
14. `resolve_contradiction` — manual contradiction resolution
15. `list_causal_links` — list cause-effect links
16. `create_causal_link` — manually create causal link
17. `trace_causal_chain` — follow causal chain forward/backward
18. `list_hypotheses` — list hypotheses by status
19. `create_hypothesis` — create hypothesis with verification plan
20. `confirm_hypothesis` — confirm hypothesis (creates supporting fact)
21. `reject_hypothesis` — reject hypothesis with reason
22. `list_goals` — list goals by status
23. `create_goal` — create goal with optional parent/priority
24. `complete_goal` — mark goal complete
25. `abandon_goal` — abandon goal with notes
26. `list_failures` — list recorded failures
27. `create_failure` — record failure with reason + lesson
28. `delete_failure` — remove a failure record

---

## Summary

**9 confirmed claims, 1 partial, 2 corrections (value changes), 11 absent→present corrections.**

### Confirmed present:
- singleBinary (with Postgres dependency caveat), semantic, context, p_claude, p_opencode, p_cursor, p_windsurf, offline (with local setup caveat)

### Confirmed absent:
- webUi, multiAgent, actions, keywords, anticipatedQueries, triggerRules, domainTag, source, originTrust, emotional, timeTravel, fulltext, hybrid, deep, codeGraph, docsSearch, timeline, quarantine, trustModel, contentPreproc, narrative, p_codex, p_gemini, p_copilot

### Corrections (absent→present):
1. **entities** → true (entity/property/value on facts)
2. **conflict** → true (contradictions table + detection)
3. **layeredMemory** → true (Episodes → Facts → Patterns)
4. **factQuery** → true (query_facts tool)
5. **decay** → true (DecayConfidence with configurable factor)
6. **autoResolve** → true (contradiction auto-resolve + decay auto-expiry)
7. **explicitForget** → true (forget tool, soft-delete)
8. **autoExtract** → true (8-stage background consolidation)
9. **dedup** → true (vector-based duplicate detection)
10. **qualityRefine** → true (LLM fact synthesis from episode clusters)
11. **clustering** → true (cosine similarity episode clustering)
12. **recurrence** → true (failure pattern detection)
13. **persona** → ⚠️ partial (/self scaffold, manual init)
14. **supersede** → ⚠️ partial (contradictions old/new fact tracking)

### Value corrections:
1. **fulltext** should be ❌ (no FTS, vector-only search)
2. **schemaFields** should be 7 (not 6: content, confidence, entity, property, value, valid_from, valid_until)

### Highlight: What stash does uniquely well
- **8-stage consolidation pipeline** — most comprehensive auto-extraction among compared systems (episodes→facts→relationships→causal_links→goals→failures→patterns→hypotheses→decay)
- **Agent self-model** — `/self` namespace with capabilities/limits/preferences scaffold
- **Hypothesis engine** — open hypotheses with verification plans, auto-confirm/reject during consolidation
- **Goal + Failure tracking** — persistent goal hierarchy with failure pattern recurrence detection
- **Causal reasoning** — cause-effect links between facts with chain tracing

---

## Evidence URL

```
evidence: "https://github.com/carsteneu/ai-memory-comparison/blob/main/evidence/stash.md"
```
