# agentmemory — Evidence Audit

> **Source:** https://github.com/rohitg00/agentmemory
> **Audit date:** 2026-05-28
> **Auditor:** automated (Claude/OpenCode)
> **Documents reviewed:** README.md, DESIGN.md, AGENTS.md, ROADMAP.md, benchmark/LONGMEMEVAL.md, benchmark/COMPARISON.md

---

## Vital Signs

| Field | Claim | Verified | Evidence |
|-------|-------|----------|----------|
| stars | ~19.2k | ✅ | README shows "Star 19.2k" (19,238 at audit time). data.js has 19053 (previous snapshot). |
| language | TypeScript | ✅ | `package.json`, `tsconfig.json`, AGENTS.md confirms "TypeScript → ESM via tsdown" |
| license | Apache 2.0 | ✅ | LICENSE file + badge in README |
| singleBinary | false | ✅ | npm package, requires Node.js + iii-engine binary. Not a single binary. |
| created | 2026-02-25 | ✅ | Star history chart begins ~Feb 2026; 421 commits. Specific date from repo metadata. |
| pricing | free | ✅ | README: "Self-hosted: Yes (default)", no paid tiers |

---

## Architecture

| Field | Claim | Verified | Evidence |
|-------|-------|----------|----------|
| deployment | Local server (npm) | ✅ | `npm install -g @agentmemory/agentmemory`, runs on :3111 |
| storage | SQLite (0 external DBs) | ✅ | README badge: "0 external DBs". AGENTS.md: "File-based SQLite via iii-engine's StateModule". COMPARISON.md: "External deps: None (SQLite + iii-engine)" |
| integration | MCP + Hooks (12) | ✅ | README: "12 hooks". AGENTS.md: "12 hooks, 4 skills, 53 MCP tools, 125 REST endpoints" |
| proxy | false | ✅ | No proxy layer. Direct MCP server connection. |
| webUi | true | ✅ | README: "Real-time viewer: Yes (port 3113)". Session replay UI. |
| offline | true | ✅ | README: "Self-hosted: Yes (default)". Local SQLite, local embeddings (`all-MiniLM-L6-v2`). |
| multiAgent | true | ✅ | README: "AGENT_ID multi-agent isolation". COMPARISON.md: "Multi-agent coordination: Leases + signals + mesh". |
| llmFlex | 3 (min) | ✅ | Claude Code, Codex, Copilot native plugins. Any MCP client. More than 3 LLM providers supported via MCP. |
| privacy | true | ✅ | COMPARISON.md: "Privacy filtering: Strips secrets pre-store". |
| export | true | ⚠️ CORRECTION | data.js has `export: false`. COMPARISON.md: "Obsidian export: Built-in". Should be `true`. |
| cacheOpt | false | ✅ | No explicit cache optimization strategy documented. iii-engine has internal caching but not exposed as a feature. |

---

## Data Model

| Field | Claim | Verified | Evidence |
|-------|-------|----------|----------|
| unit | Memory entry (structured, confidence-scored) | ✅ | README gist description: "confidence scoring, lifecycle, knowledge graphs, and hybrid search" |
| entities | false | ⚠️ DEBATABLE | COMPARISON.md: "Knowledge graph: Entity extraction + BFS". Entities ARE extracted for graph edges. However, they are not stored as structured data model fields (junction table). Per comparison taxonomy definition, Mem0 has `entities: true` because of entity extraction — by that standard, agentmemory should also be `true`. |
| actions | false | ✅ | Not documented |
| keywords | false | ✅ | Not documented. Search uses BM25 stemming, not explicit keyword/tag fields. |
| anticipatedQueries | false | ✅ | Not documented |
| triggerRules | false | ✅ | Not documented |
| domainTag | false | ✅ | Not documented |
| taskType | false | ✅ | Not documented (no task/idea/blocked classification) |
| context | false | ✅ | No explicit "why was this stored" field in the data model. Source session tracked but not reason context. |
| source | false | ✅ | No multi-tier source attribution. Session-based but not YesMem-style 5-tier source (user_stated, agreed_upon, claude_suggested, etc.). |
| originTrust | false | ✅ | No trust multiplier or origin-based weighting. Confidence scoring exists but is not origin-derived. |
| emotional | false | ✅ | Not documented |
| conflict | false | ✅ | No contradiction detection. Jaccard-based supersession detects similarity, not explicit conflicts (compare/contrast with engram's mem_judge/mem_compare). |
| layeredMemory | true | ✅ | COMPARISON.md: "4-tier consolidation: Working → episodic → semantic → procedural". Memory lifecycle table in README: "4-tier consolidation + decay + auto-forget". |
| timeTravel | false | ✅ | Session replay exists (scrub timeline, play/pause) but this is timeline viewing, not YesMem-style reconstructing knowledge state at a past point in time. |
| schemaFields | ~8 | ✅ | Confidence score, lifecycle stage, decay weight, embedding (384d), BM25 token index, graph edges, version chain ID, source session ID, timestamp. Estimate ~8. |

---

## Search & Retrieval

| Field | Claim | Verified | Evidence |
|-------|-------|----------|----------|
| fulltext | true | ✅ | BM25 with Porter stemming (LONGMEMEVAL.md). AGENTS.md mentions FTS. |
| semantic | true | ✅ | Vector search with `all-MiniLM-L6-v2` (384 dimensions, local). Benchmarked at 95.2% R@5 on LongMemEval-S. |
| hybrid | true | ✅ | README: "BM25 + Vector + Graph (RRF fusion)". LONGMEMEVAL.md confirms hybrid mode. |
| deep | false | ✅ | No deep search of thinking/planning blocks or raw conversation. Search is over crystallized memory entries. |
| codeGraph | false | ✅ | No codebase-level graph (tree-sitter, call graphs). Knowledge graph is entity-based, not code-structure based. |
| docsSearch | false | ✅ | No indexed documentation search |
| factQuery | false | ✅ | No structured metadata query tool (equivalent to query_facts). |
| timeline | false | ✅ | Session replay exists but not YesMem-style temporal search with since/before date ranges, session chains, or temporal state reconstruction. |
| searchModes | 1 | ⚠️ CORRECTION | data.js says `searchModes: 1`. But system has: BM25-only (fallback), vector-only, and hybrid (BM25+Vector). That's effectively 3 modes. LONGMEMEVAL.md tests both "bm25" and "hybrid" modes. |
| dataSources | 1 | ✅ | Memory entries from session observations. No separate code graph, docs, or fact query data sources. |

---

## Knowledge Lifecycle

| Field | Claim | Verified | Evidence |
|-------|-------|----------|----------|
| decay | true | ✅ | COMPARISON.md: "Memory decay: Ebbinghaus + tiered". README vs-competitors table: "4-tier consolidation + decay + auto-forget". |
| supersede | true | ✅ | COMPARISON.md: "Version / supersession: Jaccard-based". |
| contradiction | false | ✅ | Jaccard similarity for supersession, not explicit contradiction detection with compare/judge. |
| quarantine | false | ✅ | Not documented. Governance features planned for Q4 2026 (RBAC, audit export) but no quarantine today. |
| autoResolve | false | ✅ | Not documented. Auto-forget via decay exists, but not auto-resolution of stale/conflicting facts. |
| trustModel | false | ✅ | Confidence scoring exists but not a multi-tier trust model with origin multipliers. |
| explicitForget | true | ✅ | Skills include `/forget`. AGENTS.md: "Governance baseline". COMPARISON.md mentions governance_delete. |

---

## Extraction Pipeline

| Field | Claim | Verified | Evidence |
|-------|-------|----------|----------|
| autoExtract | true | ✅ | README: "12 hooks (zero manual effort)". Auto-capture via lifecycle hooks (SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, etc.). |
| contentPreproc | false | ✅ | Not documented. Privacy filtering strips secrets but no content-aware preprocessing pipeline. |
| dedup | false | ⚠️ POSSIBLE CORRECTION | AGENTS.md mentions "FingerprintId() for content-addressable dedup". This is a deduplication mechanism using content hashing. Should likely be `true` — content-addressable dedup at the storage level is a real feature. |
| qualityRefine | false | ✅ | Not documented. No LLM-based quality refinement of extracted memories. |
| narrative | false | ✅ | Not documented. No narrative generation from clustered memories. |
| clustering | false | ✅ | Not documented. Knowledge graph exists but not thematic clustering of memories. |
| recurrence | false | ✅ | Not documented |
| persona | false | ✅ | Not documented. Confidence and lifecycle exist, but no persona trait extraction. |

---

## Platform Support

All verified from README agent integration sections:

| Field | Claim | Verified | Evidence |
|-------|-------|----------|----------|
| p_claude | true | ✅ | Native plugin + 12 hooks + MCP. Plugin marketplace entry. |
| p_codex | true | ✅ | Native plugin + 6 hooks + MCP. Codex plugin marketplace. |
| p_opencode | true | ✅ | "22 hooks + MCP + plugin". ROADMAP mentions OpenCode hook bus with 22 hooks. |
| p_gemini | true | ✅ | MCP server. `gemini mcp add` command documented. |
| p_copilot | true | ✅ | MCP-only (`connect copilot-cli`) + full plugin (`copilot plugin install`). |
| p_cursor | true | ✅ | MCP server (standard mcpServers block for Cursor). |
| p_windsurf | false | ✅ | Not listed in supported agents. Not in the Windsurf config table. |
| p_openclaw | true | ✅ | Native plugin + MCP. Dedicated `integrations/openclaw/` directory. |
| p_hermes | true | ✅ | Native plugin + MCP. Dedicated `integrations/hermes/` directory. |
| p_pi | true | ✅ | Native plugin + MCP. Dedicated `integrations/pi/` directory. |
| p_antigravity | true | ✅ | v0.9.22 release notes: "New connect adapters (Qwen Code, Antigravity, Kiro)". `agentmemory connect antigravity`. |

---

## Benchmarks

| Field | Claim | Verified | Evidence |
|-------|-------|----------|----------|
| b_locomo | — | ✅ | Not benchmarked on LoCoMo. COMPARISON.md only cites Mem0 (68.5%) and Letta (83.2%) LoCoMo scores. |
| b_longmemeval | "95.2" | ✅ | LONGMEMEVAL.md: "agentmemory BM25+Vector: R@5 95.2%". Retrieval-only eval on LongMemEval-S (not end-to-end QA). Methodological caveats clearly stated. |
| b_token | "92% fewer" | ✅ | README badge: "92% fewer tokens". Token table: 170K tokens/year vs full context (19.5M+) ≈ 99.1% reduction. But 92% figure may compare to LLM-summarized baseline (650K → 170K = 73.8%) or a different scenario. Badge claim accepted as stated. |
| b_methodology | true | ✅ | Full benchmark docs at `benchmark/LONGMEMEVAL.md` with dataset source (HuggingFace), methodology, per-category breakdown, reproducibility instructions. `eval/README.md` for adapter-pluggable harness. |

---

## Notable Features NOT in Current Comparison Taxonomy

These features are documented in agentmemory but have no corresponding column in the comparison matrix:

| Feature | Evidence |
|---------|----------|
| **Session Replay** | Full timeline scrub with play/pause/speed control (0.5×-4×), keyboard shortcuts |
| **Knowledge Graph** | Entity extraction + BFS graph traversal (`/agentmemory/graph` endpoint) |
| **Audit Trail** | COMPARISON.md: "All mutations logged". AGENTS.md: `recordAudit()` function. |
| **Obsidian Export** | COMPARISON.md: "Obsidian export: Built-in" |
| **Privacy Filtering** | COMPARISON.md: "Strips secrets pre-store" |
| **Confidence Scoring** | README gist description: "confidence scoring, lifecycle, knowledge graphs" |
| **Content-Addressable Dedup** | AGENTS.md: "FingerprintId() for content-addressable dedup" |
| **JSONL Import** | `agentmemory import-jsonl` for importing Claude Code transcripts |
| **Multi-Agent Isolation** | `AGENT_ID` with opt-in `AGENTMEMORY_AGENT_SCOPE=isolated` |

---

## DESIGN.md Note

The DESIGN.md file at this repo is a **visual design system** (Lamborghini brand colors, typography rules, component stylings, responsive breakpoints, etc.) — not the technical system architecture. The actual architecture documentation is in:

- **AGENTS.md** — function registration patterns, MCP tool wiring, testing standards
- **benchmark/*.md** — search methodology, metrics, reproducibility
- **README.md** — feature table, agent integrations, lifecycle overview

---

## Corrections Summary

| Field | data.js current | Should be | Reason |
|-------|----------------|-----------|--------|
| `export` | `false` | `true` | COMPARISON.md: "Obsidian export: Built-in" |
| `entities` | `false` | `true` (debatable) | COMPARISON.md: "Knowledge graph: Entity extraction + BFS". Entity extraction is a documented feature. Taxonomy alignment depends on whether "entities in data model" means structured junction table or any entity extraction. |
| `searchModes` | `1` | `3` | System supports BM25-only (fallback), vector-only, and hybrid (BM25+Vector). LONGMEMEVAL.md benchmarks both "bm25" and "hybrid" modes separately. |
| `dedup` | `false` | `true` (likely) | AGENTS.md: "FingerprintId() for content-addressable dedup" |
| `stars` | `19053` | `~19200` | Current count from README. Snapshot update only. |

---

## Unusual/Distinctive Patterns

1. **DESIGN.md is a UI design system, not architecture docs.** All other audited systems put system architecture in their DESIGN.md. agentmemory ships a Lamborghini-themed brand/UI design system instead, with architecture fragmented across AGENTS.md, README, and benchmark docs.

2. **Marketed but not the core product.** The README heavily promotes agent integrations (17+ agents with dedicated setup sections) and the real-time viewer. The memory engine itself is a thin layer over iii-engine primitives (Worker/Function/Trigger), with most complexity in the iii-engine runtime.

3. **95.2% R@5 is retrieval-only, not QA accuracy.** LONGMEMEVAL.md is explicit: "These are retrieval recall scores, not end-to-end QA accuracy". The official LongMemEval metric is QA accuracy with GPT-4o judge. This disclaimer exists but the 95.2% number is prominently displayed without the QA-vs-retrieval distinction in the README badge.

4. **92% token reduction figure doesn't match the detailed table.** The token table shows 170K vs 19.5M (99.1% reduction) or 170K vs 650K (73.8%). Neither equals 92%. This may be a stale badge or based on a different baseline.

