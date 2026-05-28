# token-savior — Evidence & Audit Report

> **Repository:** https://github.com/Mibayy/token-savior
> **Audit date:** 2026-05-28
> **Auditor:** OpenCode (DeepSeek V4 Pro)
> **Sources:** README.md, CLAUDE.md, server.json, memory_schema.sql, memory_db.py, memory/search.py, memory/observations.py, memory/auto_extract.py, memory/embeddings.py, memory/lattice.py, memory/consistency.py, memory/dedup.py, memory/decay.py, memory/links.py, memory/roi.py, memory/reasoning.py, memory/bus.py, memory/viewer.py, tool_schemas.py

---

## Vital Signs

| Claim | Verdict | Evidence |
|-------|---------|----------|
| Stars: ~913 | ✅ CONFIRMED | GitHub page shows 913 stars. |
| Language: Python | ✅ CONFIRMED | 97.7% Python per GitHub language stats. |
| License: MIT | ✅ CONFIRMED | README and LICENSE file confirm MIT. |
| Single binary: false | ✅ CONFIRMED | Python package on PyPI (`pip install token-savior-recall`). Requires Python runtime. |

---

## Architecture

| Claim | Verdict | Evidence |
|-------|---------|----------|
| p_claude: true | ✅ CONFIRMED | Named for Claude Code, CLAUDE.md with full tool routing rules, `ts init --agent claude`, `TOKEN_SAVIOR_CLIENT=claude-code`. MCP server. |
| offline: true | ✅ CONFIRMED | Runs locally as MCP server. SQLite WAL storage. Code index is local. Optional: `memory-vector` pip extra for embeddings, `TS_AUTO_EXTRACT=1` for LLM auto-extract (both disabled by default). Core is fully offline. |
| b_token: -77% to -80% | ✅ CONFIRMED | README claims -80% active tokens on tsbench (3395 vs 17221). CLAUDE.md: 192/192 score at -80% tokens. Headline "100% on tsbench at -77% active tokens, -76% wall time." |
| schemaFields: ~14 | ⚠️ CORRECTION | The user claims 4 but the observations table alone has: `type`, `title`, `content`, `why`, `how_to_apply`, `symbol`, `file_path`, `context`, `tags`, `private`, `importance`, `is_global`, `narrative`, `facts`, `concepts`, `agent_id`, `expires_at_epoch`, `decay_immune` — **18+ structured fields** (excluding auto-generated IDs and timestamps). Plus linked tables: sessions, session_summaries, events, user_prompts, reasoning_chains, observation_links, corpora, consistency_scores. Estimated total: ~14 for observation-level fields (conservative, counting only the core structured ones per CRITERIA methodology). |
| searchModes: ~6 | ⚠️ CORRECTION | The user claims 1 but the actual search modes are: **(1)** `memory_search` — hybrid FTS5+vector (RRF) search across observations; **(2)** `memory_index` — recency-ranked index; **(3)** `memory_get` — direct ID fetch (layer 3 progressive disclosure); **(4)** `reasoning_search` — FTS5+Jaccard over reasoning chains; **(5)** `capture_search` — FTS5 over sandboxed tool outputs; **(6)** `memory_admin` op=`top`/`timeline`/`session_history` — structured lookups. Additional: `corpus_query`, `search_codebase` (semantic mode), `search_in_symbols`, `get_call_chain`. Minimum 6 distinct search tools. |

---

## Data Model — Features PRESENT (corrections to user's absent claims)

| Feature | User Claimed | Actual | Evidence |
|---------|-------------|--------|----------|
| **entities** | absent | ✅ PRESENT | Observations link to `symbol` (code symbol name) and `file_path` (relative path). `observation_get_by_symbol()` and `observation_get_by_file()` query by these entities. Schema has `observation_links` table linking observations via entity relations. |
| **actions** | absent | ✅ PRESENT | Observation types encode action semantics: `decision`, `error_pattern`, `bugfix`, `command`, `convention`, `guardrail`. `reasoning_chains` stores sequences of `{tool, args, observation}` steps. |
| **keywords/tags** | absent | ✅ PRESENT | `tags` JSON array field on observations. FTS5-indexed. Used for filtering, corpuses, and auto-tagging (`auto-extract`, `near-duplicate`, `bus`, `volatile`, `ruled-out`). |
| **context (why)** | absent | ✅ PRESENT | `why` field on observations. README: "Schema: why, how_to_apply". FTS5-indexed. Separate `context` field also exists. |
| **domainTag** | absent | ✅ PRESENT | 18 observation types function as domain taxonomy: `user`, `feedback`, `project`, `reference`, `guardrail`, `error_pattern`, `decision`, `convention`, `bugfix`, `warning`, `note`, `command`, `research`, `infra`, `config`, `idea`, `ruled_out`. |
| **taskType** | absent | ✅ PRESENT | `idea`, `ruled_out`, `bugfix`, `command` types encode task classification. `events` table has `severity` field (info/warning/critical). |
| **source** | absent | ✅ PRESENT | 18 distinct observation types encode source semantics (user-stated, feedback, project-derived, reference material, guardrail, error_pattern, decision, convention). Clear multi-tier source classification. |
| **originTrust** | absent | ✅ PRESENT | `consistency.py`: Bayesian validity scoring with `CONSISTENCY_QUARANTINE_THRESHOLD`, confidence updates via `update_consistency_score()`. `TYPE_SCORES` in index.py weights observation types differently (guardrail=1.0, user=1.0, convention=1.0, feedback=0.999, decision=0.998, error_pattern=0.997). Separate `roi.py` with Bayesian ROI tracking across observations. |
| **conflict** | absent | ✅ PRESENT | `observation_links` table with `contradicts` relation type. `consistency.py` exports `detect_contradictions()`, `check_symbol_staleness()`, `run_consistency_check()`. `CONTRADICTION_OPPOSITES` list of phrase pairs. Quarantine threshold at 40% validity. |
| **layeredMemory** | absent | ✅ PRESENT | Progressive disclosure (3 layers): Layer 1 = `memory_index` (compact recency index), Layer 2 = `memory_search` (snippets), Layer 3 = `memory_get` (full content). `summaries` table with `observation_ids` (JSON array, "covers_until_epoch" progressive). `mdl_distiller.py` for MDL-based hierarchical distillation. `lattice.py` with `LATTICE_LEVELS` and `LATTICE_CONTEXTS` (navigation/edit/review/unknown). `session_summaries` structured rollups. |
| **timeTravel** | absent | ✅ PRESENT | `get_timeline_around()` in index.py. `memory_admin` op=`timeline`. `sessions` table tracks `created_at_epoch`/`completed_at_epoch`. `observation_links` with `supersedes` chains. `session_summaries_fts` for session-level time travel. Temporal search via `since`/`before` epoch parameters. |
| **emotional** | absent | ❌ ABSENT | No sentiment or emotional intensity tracking found. Observation `importance` (1-10) is the closest but encodes practical relevance, not emotion. |
| **webUi** | absent | ✅ PRESENT | `memory/viewer.py` with SSE-based real-time web viewer. `TS_VIEWER_PORT` env var for dashboard. `dashboard.py` exists in source tree. README: "Optional web viewer" in env vars table. `notify_observation_saved()` pushes to SSE subscribers. |

---

## Search & Retrieval — Features PRESENT (corrections)

| Feature | User Claimed | Actual | Evidence |
|---------|-------------|--------|----------|
| **fulltext** | absent | ✅ PRESENT | FTS5 on FIVE separate tables: `observations_fts` (title, content, why, how_to_apply, tags, narrative, facts, concepts), `session_summaries_fts` (request, investigated, learned, completed, next_steps, notes), `user_prompts_fts` (prompt_text), `reasoning_chains_fts` (goal, conclusion), `tool_captures_fts` (output_full, args_summary, tool_name). Every INSERT/UPDATE/DELETE triggers sync FTS. |
| **semantic** | absent | ✅ PRESENT | `memory/embeddings.py`: FastEmbed + Nomic `nomic-ai/nomic-embed-text-v1.5-Q` (768-dim L2-normalized). `obs_vectors` vec0 table. Optional pip install: `token-savior-recall[memory-vector]`. `search_codebase(semantic=true)` for code symbol embeddings via `symbol_embeddings.py`. Task-prefix tuned (`search_document:` / `search_query:`). |
| **hybrid** | absent | ✅ PRESENT | `memory/search.py` `hybrid_search()`: FTS5 results + vector k-NN fused via **Reciprocal Rank Fusion (RRF, k=60)**. Graceful degradation when vector stack is unavailable — falls back to FTS-only. Clean, explicit implementation. |
| **deep** | absent | ✅ PRESENT | `reasoning_chains` table stores thinking traces: `steps` (JSON array of `{tool, args, observation}`), `conclusion`, `confidence`, `evidence_hash`. `reasoning_search()` with FTS5+Jaccard. `reasoning_list()` and `reasoning_inject()` for surfacing prior reasoning. |
| **codeGraph** | absent | ✅ PRESENT | Core feature of the system. Full code graph indexed by Tree-sitter with annotators for 15+ languages (Python, TypeScript, Go, Rust, Java, C, C#, Ruby, HCL, Dockerfile, Prisma, YAML, TOML, INI, XML, JSON). Tools: `find_symbol`, `get_function_source`, `get_class_source`, `get_dependencies`, `get_dependents`, `get_call_chain`, `get_change_impact`, `get_full_context`, `get_edit_context`, `get_file_dependencies`, `get_file_dependents`, `find_import_cycles`, `find_hotspots`. |
| **docsSearch** | absent | ✅ PRESENT | `get_db_schema` tool: parses SQL migrations (PostgreSQL-flavored, Supabase RLS-aware) into condensed schema snapshots. `analyze_config` tool: audits config files (.env/.yaml/.toml/.json) for duplicates, secrets, orphans. `analyze_docker` tool: audits Dockerfiles. |
| **factQuery** | absent | ✅ PRESENT | `memory_index` with `type_filter` parameter, `observation_get_by_file()`, `observation_get_by_symbol()`, `observation_get_by_session()`. `memory_admin` op=`top` (ranked by score), op=`prompts` (prompt history), op=`bus_list` (agent messages), op=`quarantine_list`. `corpus_get()` for named observation sets. |
| **timeline** | absent | ✅ PRESENT | `get_timeline_around()` in index.py. `memory_admin` op=`timeline`. Sessions have `created_at_epoch`/`completed_at_epoch`. `session_history` op returns chronological context. `created_at_epoch` indexes on all major tables. |
| **dataSources** | N/A | 5 | (1) observations_fts, (2) session_summaries_fts, (3) user_prompts_fts, (4) reasoning_chains_fts, (5) tool_captures_fts — five independently searchable data sources. Plus structured lookups (sessions, events, observation_links, corpora). |

---

## Knowledge Lifecycle — Features PRESENT (corrections)

| Feature | User Claimed | Actual | Evidence |
|---------|-------------|--------|----------|
| **decay** | absent | ✅ PRESENT | `decay_config` table with per-observation-type decay rates, min_scores, and `boost_on_access`. `memory/decay.py`: `run_decay()` applies exponential decay, `_bump_access()` resets on read. Default rates: guardrail=1.0 (no decay), user=1.0, feedback=0.999, decision=0.998, error_pattern=0.997, reference=0.995, project=0.99. Separate `expires_at_epoch` and `ttl_days` per observation. |
| **supersede** | absent | ✅ PRESENT | `observation_links` table with `supersedes` relation type. `memory/links.py`: `auto_link_observation()`, `relink_all()`, `run_promotions()` with `_PROMOTION_RULES`. Links index via `idx_links_unique` (source, target, type). |
| **contradiction** | absent | ✅ PRESENT | `observation_links` with `contradicts` relation. `consistency.py`: `detect_contradictions()` with `_CONTRADICTION_OPPOSITES` pair list, `_RULE_TYPES_FOR_CONTRADICTION`. `compute_continuity_score()`. `run_consistency_check()` automated sweep. |
| **quarantine** | absent | ✅ PRESENT | `CONSISTENCY_QUARANTINE_THRESHOLD` = 0.40 (Bayesian validity < 40%). `list_quarantined_observations()`. Quarantined obs excluded from `memory_search()` by default (`include_quarantine=False`). `observation_search` LEFT JOINs `consistency_scores` with quarantine filter. |
| **autoResolve** | absent | ✅ PRESENT | `roi_gc` (ROI-based garbage collection) in `memory/roi.py` with `run_roi_gc()`, `_ROI_HORIZON_DAYS`, `_ROI_THRESHOLD`. Auto-archival via `expires_at_epoch` on observations. `_decay_candidates_sql()` for automated decay candidate selection. |
| **trustModel** | absent | ✅ PRESENT | Multi-tier trust via `consistency.py`: Bayesian validity scores, quarantine thresholds (40%), stale suspicion thresholds. `TYPE_SCORES` in index.py assigns per-type weights. `compute_observation_roi()` in roi.py with `_ROI_TYPE_MULTIPLIER` per type. Trust hierarchy: guardrail (1.0) > user (1.0) > convention (1.0) > feedback (0.999) > decision (0.998) > error_pattern (0.997) > reference (0.995) > project (0.99). |
| **explicitForget** | absent | ✅ PRESENT | `memory_delete` MCP tool (soft-delete → `archived=1`). `observation_delete()` and `observation_restore()` functions. `observation_list_archived()` to review deleted items. `memory_admin` op=`archive` for batch operations. |

---

## Extraction Pipeline — Features PRESENT (corrections)

| Feature | User Claimed | Actual | Evidence |
|---------|-------------|--------|----------|
| **autoExtract** | absent | ✅ PRESENT | `memory/auto_extract.py`: opt-in LLM auto-extraction via PostToolUse hooks. Activates with `TS_AUTO_EXTRACT=1` + `TS_API_KEY`. Non-blocking daemon thread. Calls Anthropic API to extract 0-3 observations per tool use. Tags observations with `auto-extract`. Valid types: bugfix, convention, warning, guardrail, infra, command. |
| **contentPreproc** | absent | ✅ PRESENT | Auto-extract: `_truncate()` limits tool output to `MAX_OUTPUT_CHARS=2000`. Embeddings: `_MAX_INPUT_CHARS=2000` truncation before Nomic embed. Observation save: `_is_corrupted_content()` detects tool response artifacts and rejects. `strip_private()` removes `<private>` tags. Session budget tracking via `budget.py`. |
| **dedup** | absent | ✅ PRESENT | Three-tier dedup: **(1)** `content_hash` SHA-256 (first 16 chars) — exact match skip on save; **(2)** `global_dedup_check()` — Jaccard similarity across all projects (threshold 0.85); **(3)** `semantic_dedup_check()` — per-project near-duplicate detection. `dedup_sweep()` for batch dedup. Dedup scores ≥0.95 skip insert entirely; 0.85-0.95 tag as `near-duplicate`. |
| **qualityRefine** | absent | ⚠️ PARTIAL | No standalone LLM quality refinement pass, but: `mdl_distiller.py` (MDL-based quality distillation), consistency scoring with Bayesian updates, ROI-based quality tracking. The `narrative`, `facts`, `concepts` fields enable structured enrichment. |
| **narrative** | absent | ✅ PRESENT | `narrative` field on observations (free-form explanatory prose). `session_summaries` table with structured rollup fields: `request`, `investigated`, `learned`, `completed`, `next_steps`, `notes`. `session_end()` generates per-session context. `reasoning_chains` `conclusion` field. `project_summary` and `stats` tools. |
| **clustering** | absent | ✅ PRESENT | `leiden_communities.py` (Leiden community detection on code graph). `find_semantic_duplicates` MCP tool with `method='embedding'` for cosine-based conceptual clone detection. `corpora` table for building named observation clusters by type/tag/symbol. `corpus_build`/`corpus_query` MCP tools. |
| **recurrence** | absent | ⚠️ PARTIAL | `prompt_search()` in prompts.py. `user_prompts` table with FTS5 tracks repeated prompts. `roi.py` access-count tracking could detect recurring patterns. `_recalculate_relevance_scores()` tracks usage frequency. No explicit "recurrence detection" module, but the dedup system (global + semantic) and prompt tracking provide some recurrence awareness. |
| **persona** | absent | ✅ PRESENT | `memory/lattice.py`: Personality lattice with `LATTICE_LEVELS` and `LATTICE_CONTEXTS` (navigation, edit, review, unknown). `thompson_sample_level()` for contextual bandit-based profile adaptation. `record_lattice_feedback()` for learning from interaction patterns. `get_lattice_stats()` for profile reporting. `mdl_distiller.py` for MDL-based persona compression. |

---

## Multi-Agent Features

| Feature | Claim | Evidence |
|---------|-------|----------|
| multiAgent | ⚠️ PARTIAL | `agent_id` field on observations with `idx_obs_agent` index. `memory/bus.py` with `memory_bus_list()` — inter-agent memory bus. `observation_save_volatile()` for agent-to-agent messages with `bus`+`volatile` tags and short TTL. `DEFAULT_VOLATILE_TTL_DAYS` auto-cleanup. No agent spawning/orchestration (that's the host system's job). No multi-agent crash recovery. |

---

## Summary of Corrections

The user's initial premise ("all search features are false — this is unusual") is **substantially incorrect**. token-savior has one of the most comprehensive memory architectures among all systems in the comparison table:

| User Claim | Corrected |
|------------|-----------|
| searchModes=1 | **~6** (memory_search hybrid, memory_index, memory_get, reasoning_search, capture_search, memory_admin) |
| schemaFields=4 | **~14** (18+ fields in observation table alone, plus linked tables) |
| No fulltext | **FTS5 across 5 independent tables** |
| No semantic | **768-dim Nomic vector embeddings with RRF hybrid fusion** |
| No hybrid | **Hybrid FTS5+vector with Reciprocal Rank Fusion (k=60)** |
| No codeGraph | **15+ language Tree-sitter code graph with full navigation tools** |
| No decay/supersede/contradiction/quarantine | **All four present with full implementations** |
| No autoExtract | **Opt-in LLM auto-extraction via PostToolUse hooks** |
| No persona | **Thompson-sampled personality lattice with contextual bandits** |
| No webUi | **SSE-based web viewer dashboard** |

### Features genuinely ABSENT

| Feature | Evidence |
|---------|----------|
| **emotional** | No sentiment or emotional intensity tracking. Importance (1-10) is practical, not emotional. |
| **triggerRules** | No condition-based activation (e.g., "show when file X opens"). Context-specific injection happens but via hardcoded logic, not configurable rules. |
| **anticipatedQueries** | No generated predicted-search-queries field for recall improvement. |
| **proxy** | MCP server, not a conversation proxy. No stream interception. |

### token-savior Relative Position

token-savior sits at the intersection of **code navigation** (strongest in the field, with 15+ language annotators, call graphs, import cycles, semantic duplicate detection) and **memory engineering** (decay, contradiction, quarantine, Bayesian trust, hybrid search). Its strength is the **integration** of these two worlds: code structure informs memory (observations linked to symbols and files), and memory informs code operations (observations injected at tool boundaries).

Compared to YesMem, token-savior has:
- Stronger code graph (15 languages vs Go-only Tree-sitter in current YesMem scope)
- More compact memory representation (designed for token efficiency)
- Weaker extraction pipeline (auto-extract is opt-in and simple, vs YesMem's 6-phase pipeline)
- Weaker search breadth (6 modes vs 9)
- Fewer unique data model fields (14 vs 22)
- No multi-agent orchestration (just a message bus, no spawn/coordinate)

It belongs in the comparison table and ranks among the top systems for data model depth and search features.

---

## Evidence URL

```
evidence: "https://github.com/carsteneu/ai-memory-comparison/blob/main/evidence/token-savior.md"
```
