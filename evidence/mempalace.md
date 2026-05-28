# MemPalace — Audit Evidence

> **Audited:** 2026-05-28
> **Source:** https://github.com/MemPalace/mempalace (develop branch, v3.3.5)
> **Docs:** https://mempalaceofficial.com

## Methodology

Every claim verified against README, official docs, source tree structure, benchmarks, and the project's own corrections log (docs/HISTORY.md). No inferences from secondary sources.

---

## Verified Claims (all match data.js)

### Vital Signs
| Field | Claim | Evidence |
|-------|-------|----------|
| **stars** | ~53k | GitHub: 53k stars |
| **language** | Python | pyproject.toml, README badges, 93.9% Python |
| **license** | MIT | LICENSE file, README badge |
| **singleBinary** | false | Python package, uv/pip install, no binary distribution |
| **created** | 2026-04-05 | GitHub repo creation date |

### Architecture
| Field | Claim | Evidence |
|-------|-------|----------|
| **offline** | ✅ | README: "Nothing leaves your machine unless you opt in." Local ChromaDB, no cloud dependency. |
| **privacy** | ✅ | README: local-first, zero API calls in raw mode. No data exfiltration. |
| **webUi** | false | No TUI, no web dashboard. Website (mempalaceofficial.com) is docs only. |
| **multiAgent** | false | Agents doc explicitly states: "MemPalace does **not** currently ship an agent registry, `~/.mempalace/agents/*.json`, or a `mempalace_list_agents` tool." Agent diaries exist (`mempalace_diary_write`/`read`) but no multi-agent orchestration, spawning, messaging, or crash recovery. |

### Data Model
| Field | Claim | Evidence |
|-------|-------|----------|
| **entities** | ✅ | Knowledge graph stores typed entities (person, project, tool, concept). `mempalace_kg_add` / `mempalace_kg_query`. README: "temporal entity-relationship graph." |
| **actions** | false | No action tracking. KG has predicates but no action metadata on learnings. |
| **keywords** | false | No keyword/tag field on drawers. Rooms categorize but are not user-defined tags. |
| **anticipatedQueries** | false | Not documented. |
| **triggerRules** | false | Not documented. |
| **domainTag** | false | Not documented. Rooms are topics, not domains. |
| **taskType** | false | Not documented. |
| **context** | false | No "why" or context field. Verbatim text is the content itself. |
| **source** | false | `source_file` is a file path, not a formal source attribution system. No trust tiers. |
| **originTrust** | false | No trust model documented. |
| **emotional** | false | Not documented. |
| **conflict** | false | Contradiction detection docs: "Experimental. Contradiction detection is a **planned capability, not a shipped end-to-end feature** in the current MCP workflow." HISTORY.md (Apr 7): "`fact_checker.py` exists as a separate utility but is not currently wired into the knowledge graph operations." |
| **layeredMemory** | false | Wings/rooms/drawers is hierarchical categorization, not temporal layering (cf. L0→L3 pyramid, working/session/wiki layers). |
| **timeTravel** | false | KG has `mempalace_kg_query(as_of=...)` and `mempalace_kg_timeline` for fact history, but main memory retrieval has no time-travel (no session replay, no deep_search with date ranges, no frame rewind). |
| **schemaFields** | ~5 | Drawer: `wing`, `room`, `content`, `source_file`, `added_by`. Verbatim text unit, no structured extraction. |

### Search & Retrieval
| Field | Claim | Evidence |
|-------|-------|----------|
| **fulltext** | **false** | Unusual but verified. README: "retrieves it with semantic search." MCP `mempalace_search`: "Semantic search. Returns verbatim drawer content with similarity scores." No FTS5, no BM25 index, no dedicated full-text engine. Hybrid mode uses keyword overlap scoring in Python post-processing (not a search index). BM25 appears in benchmarks only as an external baseline comparison. |
| **semantic** | ✅ | ChromaDB-backed embeddings (all-MiniLM-L6-v2 or embeddinggemma-300m). README: "semantic search." |
| **hybrid** | ✅ | Benchmarks: "keyword overlap scoring on top of embedding similarity" + temporal proximity boost. Multiple hybrid versions (v1–v5). |
| **deep** | false | No deep search into thinking/planning content. |
| **codeGraph** | false | No Tree-sitter or code graph integration. |
| **docsSearch** | false | No indexed documentation search. |
| **factQuery** | false | `mempalace_kg_query` exists for entity-relationship queries, but no structured metadata query over learnings (no query by entity+action+keyword over a learning metadata table). |
| **timeline** | false | `mempalace_kg_timeline` exists for KG facts only. No timeline view of memories/conversations. |
| **searchModes** | 1 | Single search tool: `mempalace_search` (semantic). Hybrid/palace/diary are internal pipeline configs, not user-facing search modes. |
| **dataSources** | 2 | 1) Project files: `mempalace mine ~/projects/myapp`. 2) Conversations: `mempalace mine ~/.claude/projects/ --mode convos`. |

### Knowledge Lifecycle
| Field | Claim | Evidence |
|-------|-------|----------|
| **decay** | false | No Ebbinghaus forgetting curve or decay mechanism. |
| **supersede** | false | `mempalace_update_drawer` overwrites, no version chains. KG has `invalidate()` but no supersede/replace cascade. |
| **contradiction** | false | "Planned, not shipped." `fact_checker.py` exists but not wired into KG ops (per HISTORY.md Apr 7 correction). |
| **quarantine** | false | Not documented. |
| **autoResolve** | false | Not documented. |
| **trustModel** | false | No trust scoring, no source-tier multipliers. |
| **explicitForget** | false | `mempalace_delete_drawer` is irreversible delete, not a formal forget/quarantine mechanism. No skip-indexing, no quarantine. |

### Extraction Pipeline
| Field | Claim | Evidence |
|-------|-------|----------|
| **autoExtract** | ✅ | Auto-save hooks (Claude Code), `mempalace mine` for files, `mempalace sweep` for per-message verbatim storage. Agent diary auto-write. |
| **contentPreproc** | false | Stores verbatim text. No content-aware preprocessing or reduction. |
| **dedup** | false | `mempalace_check_duplicate` is a manual check tool, not automatic pipeline deduplication. |
| **qualityRefine** | false | No LLM-based quality refinement. |
| **narrative** | false | No narrative generation from memories. |
| **clustering** | false | Not documented. |
| **recurrence** | false | Not documented. |
| **persona** | false | No persona extraction engine. |

### Platform Support
| Field | Claim | Evidence |
|-------|-------|----------|
| **p_claude** | ✅ | README: "Two Claude Code hooks save periodically and before context compression." `.claude-plugin/` directory. Claude Code retention checklist. |
| **p_gemini** | ✅ | README: "For Claude Code, Gemini CLI, MCP-compatible tools, and local models." AGENTS.md in repo root. |
| **p_opencode** | false | Not documented. No OpenCode plugin. |
| **p_codex** | false | `.codex-plugin/` directory exists in repo but integration not referenced in README or docs as supported platform. |

### Benchmarks
| Field | Claim | Evidence |
|-------|-------|----------|
| **b_locomo** | "88.9" | Honest top-10 hybrid v5 score (no rerank). Beats Memori 81.95% by 7pp. From benchmarks/BENCHMARKS.md: "Hybrid v5 (top-10): 88.9%". The 100% result used top-k=50 which structurally includes all sessions (19-32 per conversation), making retrieval trivial — the project's own docs flag this: "The honest LoCoMo score is the top-10 result." |
| **b_longmemeval** | "96.6" | Raw mode (no LLM, no API key). 500 questions, R@5. Indepently reproducible. From README: "96.6% R@5 on LongMemEval in raw mode — zero API calls." Hybrid v4 held-out 450q: 98.4% (clean generalization). |
| **b_methodology** | ✅ | Full reproduction instructions in benchmarks/BENCHMARKS.md. Scripts committed. Result JSONLs committed. Deterministic runs. Split methodology (50 dev / 450 held-out) documented. Self-audited benchmark integrity section. HISTORY.md corrections log. |

---

## Notable Nuances & Context

### Corrections History (from docs/HISTORY.md)

MemPalace has a transparent corrections log. Notable retractions:
- **Apr 7, 2026:** "+34% palace boost" removed (standard metadata filtering, not novel). AAAK "30x lossless" withdrawn (lossy, 84.2% R@5 vs raw 96.6%). Contradiction detection claim softened (`fact_checker.py` not wired into KG). "100% with Haiku rerank" removed from headlines (teaching-to-the-test on final 0.6%).
- **Apr 14, 2026:** Competitor comparison tables mixing retrieval recall with QA accuracy removed per community audit (issue #875). The 100% LoCoMo top-50 result flagged as structurally guaranteed. Honest held-out number (98.4%) published.

### Full-text Search Nuance

The hybrid mode performs keyword overlap scoring in Python as a post-retrieval boost. This is not a full-text search engine (no FTS5, no BM25 index, no inverted index). The terms "keyword" in the benchmark context refer to regex-based term extraction from queries, matched against stored text in memory — not a search index. This is why `fulltext=false` is correct.

### Knowledge Graph vs. Memory System

The knowledge graph (`mempalace_kg_*` tools) has temporal query capabilities and entity tracking that blur some feature boundaries:
- KG has timeline (`mempalace_kg_timeline`) — but this is for entity facts, not memory/conversation timeline.
- KG has invalidation — but this is for fact expiry, not memory lifecycle management.
- These KG features exist alongside but separate from the main verbatim memory store.

### Agent Diaries vs. Multi-Agent

Agent diaries (`mempalace_diary_write`/`read`) let named agents maintain separate diary streams. This is single-agent journaling, not multi-agent orchestration. No spawning, messaging, heartbeat, crash recovery, or scratchpad. The docs explicitly disclaim agent registry and `mempalace_list_agents`.

### Duplicate Detection

`mempalace_check_duplicate` performs similarity-based duplicate detection (cosine similarity threshold). This is a manual pre-flight check, not an automatic pipeline deduplication step.

---

## Source References

- README: https://github.com/MemPalace/mempalace#readme
- Benchmarks: https://github.com/MemPalace/mempalace/blob/develop/benchmarks/BENCHMARKS.md
- Corrections: https://github.com/MemPalace/mempalace/blob/develop/docs/HISTORY.md
- MCP Tools: https://mempalaceofficial.com/reference/mcp-tools.html (30 tools)
- Knowledge Graph: https://mempalaceofficial.com/concepts/knowledge-graph.html
- Agents: https://mempalaceofficial.com/concepts/agents.html
- Contradiction Detection: https://mempalaceofficial.com/concepts/contradiction-detection.html

---

## Verdict

**All claims in data.js verified.** No corrections needed. The `fulltext=false` claim, while unusual for a memory system, is accurate: MemPalace uses semantic search (ChromaDB) with Python-level keyword boosting, not a dedicated full-text search engine (FTS5/BM25 index).

One refinement noted: the Knowledge Graph provides partial temporal query capabilities (`as_of`, `timeline`) that exist adjacent to but separate from the main memory retrieval system. These do not change any boolean flags but are worth documenting in the system description.
