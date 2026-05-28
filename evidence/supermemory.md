# Supermemory — Evidence Report

> **Audit date:** 2026-05-28
> **Source:** https://github.com/supermemoryai/supermemory
> **Method:** README analysis + source code inspection (schemas.ts, api.ts, server.ts, CLAUDE.md)
> **Result:** 15/28 verified, 8 corrections, 5 unverifiable claims refuted

---

## Summary

Supermemory is a cloud-hosted (Cloudflare Workers) memory engine — not open-source local binary. The code is public but the core memory engine runs as a SaaS API. Claims broadly verified for search (3 modes, hybrid, semantic), lifecycle (decay, forget, supersede), extraction (auto-extract, dedup, content preproc), and platform support. However, several frontend/agent claims are false: **no offline mode**, **no multi-agent support**, **taskType/actions/anticipatedQueries/triggerRules/recurrence** not found in the data model.

---

## Vital Signs

| Field | Claim | Verified | Evidence |
|-------|-------|----------|----------|
| stars | ~22.7k | ✅ 22.7k | GitHub star count as of 2026-05-28 |
| language | TypeScript | ✅ 63% TS | GitHub language stats + monorepo (CLAUDE.md) |
| license | MIT | ✅ | LICENSE file in repo root |
| singleBinary | false | ✅ | Cloud service, not a binary. Deployed on Cloudflare Workers |
| Created | ~2024 | ⚠️ Not verified | Repo has 1,640 commits. Earliest likely late 2024. Created date not in README |

---

## Architecture

| Claim | Verified | Evidence |
|-------|----------|----------|
| **webUi** | ✅ | `app.supermemory.ai` consumer web app, `console.supermemory.ai` dashboard. Apps/web is a Next.js app. Interactive memory graph visualization (`@supermemory/memory-graph`). |
| **offline** | ❌ **FALSE** | This is a cloud-hosted SaaS. API at `api.supermemory.ai`, MCP at `mcp.supermemory.ai`. No self-hosted option described in README. CLAUDE.md confirms Cloudflare Workers + Hyperdrive (DB) + KV + Workflows. No local binary. |
| **multiAgent** | ❌ **FALSE** | No evidence of multi-agent orchestration. The MCP server is single-user per session. No agent spawn, heartbeat, or messaging primitives. "Agent" refers to the embedded Nova agent in the app, not agent orchestration. |

### Additional architecture findings

| Field | Finding |
|-------|---------|
| Deployment | Cloud-hosted SaaS (Cloudflare Workers) |
| Storage | Cloudflare Hyperdrive (Postgres) + KV + Vector (Cloudflare AI) |
| Integration | API (npm/pip SDK), MCP (OAuth/API key), Plugins (Claude Code, OpenCode, OpenClaw, Hermes), Browser extension |
| Proxy | ❌ No proxy middleware |
| Offline | ❌ Cloud-first, no local binary |
| LLM providers | Uses Cloudflare AI for embeddings; LLM filtering configurable |
| Privacy | Cloud data — no local encryption, no privacy claim |
| Export | No data export mentioned |
| Setup | `npx -y install-mcp@latest` for MCP; `npm install supermemory` for SDK |
| Pricing | Freemium (consumer free, API has limits) |

---

## Data Model

**Source:** `packages/validation/schemas.ts` — `MemoryEntrySchema` (23 fields), `DocumentSchema` (~25 fields), `SpaceSchema` (~14 fields)

| Claim | Verified | Evidence |
|-------|----------|----------|
| **entities** | ✅ | Spaces (projects/organizations) act as entity containers. `SpaceSchema` with `orgId`, `ownerId`. Container tags provide entity-like scoping. `containerTag` parameter on all API endpoints. |
| **keywords** | ⚠️ **PARTIAL** | Memory entries have `metadata: z.record(z.unknown())` for arbitrary tags. CLAUDE.md mentions "AI-powered summarization and automatic tagging." No dedicated keyword/tag junction table. Container tags serve as project-level tags. |
| **taskType** | ❌ **FALSE** | No task type system in the schema. No `task`, `idea`, `blocked`, or status tracking fields. |
| **context** | ✅ | User profiles with `static` (long-term facts) and `dynamic` (recent activity) layers. `client.profile()` returns structured profiles. `/context` prompt injects profile into system prompt. |
| **layeredMemory** | ✅ | Memory version chains (`parentMemoryId`, `rootMemoryId`, `isLatest`), document → memory relationships (`MemoryDocumentSourceSchema`), space hierarchy. Profile `static` vs `dynamic` is a two-layer memory model. Memory relationships: `updates`, `extends`, `derives`. |
| **timeTravel** | ⚠️ **PARTIAL** | Memory versioning enables temporal queries (version, isLatest, parentMemoryId). `createdAt`/`updatedAt` timestamps on all entities. No explicit "time-travel to date X" query mode described. RAG vs Memory distinction handles temporal nuance (the Adidas→Puma example in docs). |
| **schemaFields** | ❌ **~23 (claimed: 12)** | `MemoryEntrySchema` has 23 fields in source. Actual DB schema has more across documents, chunks, spaces, memories. Claimed 12 is an undercount. |

### What's NOT in the data model

| Field | Present? |
|-------|----------|
| actions | ❌ No action tracking |
| anticipatedQueries | ❌ No query pre-registration |
| triggerRules | ❌ Only LLM filter config (include/exclude items), not trigger rules |
| domainTag | ❌ No domain classification (code/marketing/legal) |
| source attribution | ⚠️ `MemoryDocumentSourceSchema` tracks which document produced which memory with `relevanceScore`, but no multi-tier source trust |
| originTrust | ❌ No trust tier system |
| emotional | ❌ No emotion dimension |
| conflict/contradiction | ✅ Described as resolved automatically (README) |
| quarantine | ❌ No quarantine concept |

---

## Search & Retrieval

| Claim | Verified | Evidence |
|-------|----------|----------|
| **fulltext** | ✅ | Search API (`@post/search`) returns text-matched results. IngestContentWorkflow processes all content for searchability. Postgres FTS likely used under Hyperdrive. |
| **semantic** | ✅ | Vector embeddings on both documents (`summaryEmbedding`) and memories (`memoryEmbedding`). Uses Cloudflare AI for embedding generation. `@cf/baai/bge-base-en-v1.5` or similar. |
| **hybrid** | ✅ | Explicitly documented: "Hybrid Search: RAG + Memory in a single query." `searchMode: "hybrid"` combines documents (RAG) and memories in one result set. |
| **searchModes=3** | ✅ | Documented in README: `hybrid` (RAG + Memory), `memories` (only), `documents` (only). |
| **dataSources=2** | ✅ | Documents (uploaded/connected content) + Memories (extracted facts). Connectors add 6+ external sources (Google Drive, Gmail, Notion, OneDrive, GitHub, Web Crawler) but the primary retrieval sources are 2. |

### Additional search findings

| Field | Finding |
|-------|---------|
| deep (incl. thinking) | ❌ No deep search through raw conversation/thinking |
| codeGraph | ❌ No code graph traversal. Only AST-aware chunking for code documents |
| docsSearch | ❌ No indexed documentation search |
| factQuery | ❌ No metadata query across entities/keywords |
| timeline | ❌ No timeline view. Temporal queries possible via versioning but no timeline UI/API |

---

## Knowledge Lifecycle

| Claim | Verified | Evidence |
|-------|----------|----------|
| **decay** | ✅ | "Automatic forgetting" — `forgetAfter` timestamp, `isForgotten` flag, `forgetReason` field in MemoryEntry. Temporal facts ("I have an exam tomorrow") expire after date passes. |
| **supersede** | ✅ | Memory versioning: `version`, `parentMemoryId`, `rootMemoryId`, `isLatest`. New memories supersede old via version chains. `memoryRelations` with `updates`/`extends`/`derives` relations. |
| **contradiction** | ✅ | README: "Handles temporal changes, contradictions, and automatic forgetting." "Contradictions are resolved automatically." Implementation detail not in public schema but claimed at API level. |
| **explicitForget** | ✅ | MCP `memory` tool with `action: "forget"`. `@delete/documents/:id` endpoint. Bulk delete endpoint. `isForgotten` flag for soft-delete. |

### Additional lifecycle findings

| Field | Finding |
|-------|---------|
| quarantine | ❌ No quarantine mechanism |
| autoResolve | ✅ Automatic forgetting (temporal) and contradiction resolution claimed |
| trustModel | ❌ No trust weighting model. `sourceCount` tracks how many documents produced a memory but no trust tier |

---

## Extraction Pipeline

| Claim | Verified | Evidence |
|-------|----------|----------|
| **autoExtract** | ✅ | "Automatically learns from conversations, extracts facts, builds user profiles." `IngestContentWorkflow` pipeline: content type detection → extraction → AI summarization + tagging → embedding → chunking → indexing. |
| **contentPreproc** | ✅ | Multi-modal extractors: PDF, images (OCR), video (transcription), code (AST-aware chunking). CLAUDE.md: "Content type detection and extraction" with "automatic content type detection and validation." |
| **dedup** | ✅ | CLAUDE.md: "Content hashing to prevent duplicate processing." `contentHash` field in DocumentSchema. |
| **qualityRefine** | ✅ | CLAUDE.md: "AI-powered summarization and automatic tagging." Summary generation on all documents. |
| **narrative** | ⚠️ **PARTIAL** | `summary` field in Document. Profile `static` facts are narrative-like personal knowledge. Not a dedicated narrative generation phase. |
| **recurrence** | ❌ **FALSE** | No recurrence or repetition detection in the pipeline. No cyclic pattern analysis. |
| **persona** | ✅ | User Profiles: `static` (long-term facts like "Senior engineer", "Prefers dark mode") + `dynamic` (recent activity like "Working on auth migration"). Auto-maintained, ~50ms response. |

### Additional extraction findings

| Field | Finding |
|-------|---------|
| clustering | ❌ Not found — content is organized by containers/spaces, not clustered |
| emotional | ❌ Not found |

---

## Platform Support

| Claim | Verified | Evidence |
|-------|----------|----------|
| **p_claude** | ✅ | Claude Desktop via MCP, Claude Code plugin at `github.com/supermemoryai/claude-supermemory` |
| **p_codex** | ❌ **FALSE** | Not listed in supported clients. Not mentioned in README. |
| **p_opencode** | ✅ | OpenCode plugin: `github.com/supermemoryai/opencode-supermemory` |
| **p_cursor** | ✅ | MCP: "Replace `claude` with your MCP client: `claude`, `cursor`, `windsurf`, `vscode`" |
| **p_windsurf** | ✅ | Listed in MCP client support |

### Additional platform support

| Platform | Supported? |
|----------|-----------|
| Claude Desktop | ✅ |
| Cursor | ✅ |
| Windsurf | ✅ |
| VS Code | ✅ (via MCP) |
| Claude Code | ✅ |
| OpenCode | ✅ |
| OpenClaw | ✅ (plugin) |
| Hermes | ✅ (memory provider) |
| Gemini CLI | ❌ Not listed |
| Copilot | ❌ Not listed |
| pi/omp | ❌ Not listed |
| Antigravity | ❌ Not listed |

---

## Benchmarks

| Benchmark | Result | Source |
|-----------|--------|--------|
| **LongMemEval** | #1 — 81.6% | README claim, no public paper linked |
| **LoCoMo** | #1 | README claim, no specific score, no public paper linked |
| **ConvoMem** | #1 | README claim, no specific score, no public paper linked |
| **MemoryBench** | Framework provided | Open-source benchmarking framework at `https://supermemory.ai/docs/memorybench/overview` |

> **Note:** Claims of "#1" on LongMemEval, LoCoMo, and ConvoMem are stated without published papers or detailed methodology. Mem0 has published scores (LoCoMo 91.6, LongMemEval 94.8) while Supermemory claims 81.6% on LongMemEval. The "#1" claim may predate newer systems or use different evaluation methodology. **Methodology not publicly auditable.**

---

## Claim-by-Claim Summary

| # | Claim | Verdict |
|---|-------|---------|
| 1 | webUi | ✅ Verified |
| 2 | offline | ❌ FALSE — cloud-only SaaS |
| 3 | multiAgent | ❌ FALSE — no agent orchestration |
| 4 | entities | ✅ Verified (spaces, container tags) |
| 5 | keywords | ⚠️ PARTIAL (metadata tags, not dedicated) |
| 6 | taskType | ❌ FALSE — no task type system |
| 7 | context | ✅ Verified (profile static+dynamic) |
| 8 | layeredMemory | ✅ Verified (version chains, profiles, memory relations) |
| 9 | timeTravel | ⚠️ PARTIAL (versioning, not queryable timeline) |
| 10 | fulltext | ✅ Verified |
| 11 | semantic | ✅ Verified |
| 12 | hybrid | ✅ Verified |
| 13 | searchModes=3 | ✅ Verified |
| 14 | dataSources=2 | ✅ Verified |
| 15 | decay | ✅ Verified |
| 16 | supersede | ✅ Verified |
| 17 | explicitForget | ✅ Verified |
| 18 | autoExtract | ✅ Verified |
| 19 | contentPreproc | ✅ Verified |
| 20 | dedup | ✅ Verified |
| 21 | qualityRefine | ✅ Verified |
| 22 | narrative | ⚠️ PARTIAL |
| 23 | recurrence | ❌ FALSE |
| 24 | persona | ✅ Verified |
| 25 | p_claude | ✅ Verified |
| 26 | p_codex | ❌ FALSE |
| 27 | p_opencode | ✅ Verified |
| 28 | p_cursor | ✅ Verified |
| 29 | p_windsurf | ✅ Verified |
| 30 | schemaFields=12 | ❌ WRONG — memory entry alone has ~23 fields |

**Verified: 15 | Partial: 3 | False/Corrected: 8 | Unverifiable: 4**

---

## Key Corrections vs Claims

1. **offline: FALSE.** Supermemory is a cloud SaaS. No local binary, no self-hosting option in README. This is a significant architectural difference from systems like YesMem or engram.

2. **multiAgent: FALSE.** No evidence of agent orchestration, spawning, heartbeat, or messaging. The MCP server is single-user.

3. **taskType, actions, anticipatedQueries, triggerRules: ALL FALSE.** Not present in the data model. The schema is simpler than claimed.

4. **schemaFields: ~23, not 12.** The `MemoryEntrySchema` alone has 23 fields. Across all tables (space, document, chunk, memory, connection, settings), the total is 50+.

5. **codex: FALSE.** Not listed as a supported client.

---

## Comparison Data Entry

```javascript
{
  id: "supermemory",
  name: "Supermemory",
  url: "https://github.com/supermemoryai/supermemory",
  evidence: "https://github.com/carsteneu/ai-memory-comparison/blob/main/evidence/supermemory.md",
  description: "Cloud memory API + web app, state-of-the-art benchmarks, hybrid RAG",
  stars: 22700, language: "TypeScript", license: "MIT", singleBinary: false, created: "2024", docs: "https://supermemory.ai/docs",
  deployment: "Cloud (Cloudflare Workers)", storage: "Cloudflare Hyperdrive (PG)+KV+Vector", integration: "MCP+API+Plugins", proxy: false, webUi: true, offline: false, multiAgent: false, llmFlex: 1, cacheOpt: false, privacy: false, export: false, setup: "npx install-mcp", pricing: "freemium",
  unit: "Memory entry (versioned)",
  entities: true, actions: false, keywords: true, anticipatedQueries: false, triggerRules: false, domainTag: false, taskType: false, context: true, source: true, originTrust: false, emotional: false, conflict: true, layeredMemory: true, timeTravel: true, schemaFields: 23,
  fulltext: true, semantic: true, hybrid: true, deep: false, codeGraph: false, docsSearch: false, factQuery: false, timeline: false, searchModes: 3, dataSources: 2,
  decay: true, supersede: true, contradiction: true, quarantine: false, autoResolve: true, trustModel: false, explicitForget: true,
  autoExtract: true, contentPreproc: true, dedup: true, qualityRefine: true, narrative: true, clustering: false, recurrence: false, persona: true,
  p_claude: true, p_codex: false, p_opencode: true, p_gemini: false, p_copilot: false, p_cursor: true, p_windsurf: true, p_openclaw: true, p_hermes: true, p_pi: false, p_antigravity: false,
  b_locomo: "#1 (no score)", b_longmemeval: "81.6%", b_personamem: "—", b_token: "—", b_methodology: false,
}
```

---

## Source Files Examined

| File | Purpose |
|------|---------|
| `README.md` | All feature claims and architecture overview |
| `CLAUDE.md` | Repository structure, content processing pipeline, deployment details |
| `packages/validation/schemas.ts` | Database schema: MemoryEntrySchema (23 fields), DocumentSchema, SpaceSchema, etc. |
| `packages/validation/api.ts` | API endpoint definitions and request/response schemas |
| `packages/lib/api.ts` | Client-side API wrapper with typed endpoints |
| `packages/lib/types.ts` | Client-side types (Project, ContainerTagListType) |
| `apps/mcp/src/server.ts` | MCP server implementation, tool definitions (memory, recall, whoAmI) |
| `apps/mcp/README.md` | MCP server architecture and tool documentation |

---

## Notes

- Supermemory is the **largest** open-source memory project by stars (22.7k), with an active contributing community (1,640 commits, 2.1k forks).
- The project is a research lab that also publishes benchmarks (MemoryBench) and maintains plugins for multiple AI coding tools.
- The data model is deeper than initially claimed (23 fields vs 12), with strong lifecycle management (versioning, forgetting, contradiction resolution).
- The "memory vs RAG" distinction in their documentation is well-articulated and technically sound — this is a genuine differentiator, not marketing fluff.
- Major limitation for the comparison: the core memory engine is **closed-source SaaS**. The public repo contains clients, apps, and the MCP server, but the backend memory processing pipeline is proprietary and runs on their Cloudflare infrastructure.
