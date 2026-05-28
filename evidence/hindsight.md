# Hindsight Audit

**Date:** 2026-05-28
**Source:** https://github.com/vectorize-io/hindsight
**Version:** v0.7.1 (latest as of audit)
**Language:** Python
**Stars:** 14,979
**License:** MIT

## URL Correction

The claimed URL `https://github.com/AdjectiveAllison/hindsight` returns **404** — the user `AdjectiveAllison` and repository do not exist on GitHub. The actual repository is `https://github.com/vectorize-io/hindsight`. This was already correctly registered in data.js (line 575). The repo name "hindsight" is correct; only the org is wrong.

## Summary

Hindsight is a production-grade agent memory system by Vectorize.io that structures memory into four biomimetic networks: world facts, agent experiences, synthesized entity summaries, and evolving beliefs (paper: arXiv:2512.12818). Three core operations — retain, recall, reflect — govern information flow. During retain, an LLM auto-extracts entities, relationships, temporal data, and classifies into world vs. experience pathways. Recall runs 4 parallel retrieval strategies (semantic/vector, keyword/BM25, graph/temporal-causal, temporal/range) fused via reciprocal rank fusion + cross-encoder reranking. Reflect generates new observations by reasoning over accumulated memories. Ships as Docker container with web UI + Python embedded mode. SDKs for Python, Node.js, REST, CLI. 15k stars, 1,500 commits, Fortune 500 production use. Achieves 91.4% on LongMemEval (state of the art as of January 2026).

The user's claims are **significantly understated**: of 20 claimed features, 10 are verified present, 1 is partially present. 8 are absent. But the current data.js entry (line 575-583) is wildly inaccurate — 16 features wrongly marked `false` that should be `true`. The user also undersold searchModes (3 claimed, actual = 4), entities, context, and timeTravel which are all clearly present. URL org correction needed.

## Claim Audit

### Verified Claims

| Claim | Status | Evidence |
|-------|--------|----------|
| entities | ✅ Verified | README: "retain operation uses an LLM to extract key facts, temporal data, **entities**, and relationships." Paper: "temporal, entity aware memory layer" + "synthesized entity summaries." Entities are canonicalized via normalization. |
| keywords | ✅ Verified | Recall runs "Keyword: BM25 exact matching" as one of 4 parallel retrieval strategies. |
| context | ✅ Verified | `retain()` accepts explicit `context` parameter: `client.retain(bank_id="my-bank", content="...", context="career update", timestamp="2025-06-15T10:00:00Z")`. |
| timeTravel | ✅ Verified | Temporal recall: `client.recall(bank_id="my-bank", query="What happened in June?")`. Memories stored as "time series" representations. `retain()` accepts explicit `timestamp`. Paper: "a temporal, entity aware memory layer incrementally turns conversational streams into a structured, queryable memory bank." |
| fulltext | ✅ Verified | "Keyword: BM25 exact matching" as one of 4 retrieval strategies. |
| semantic | ✅ Verified | "Semantic: Vector similarity" as one of 4 retrieval strategies. Also: "sparse/dense vector representations to aid in later recall." |
| hybrid | ✅ Verified | 4 retrieval strategies (semantic, keyword, graph, temporal) run in parallel. "Merged, then ordered by relevance using reciprocal rank fusion and a cross-encoder reranking model." This is a multi-strategy hybrid approach. |
| autoExtract | ✅ Verified | README: "retain operation uses an LLM to extract key facts, temporal data, entities, and relationships" + "normalization process to transform extracted data into canonical entities, time series, and search indexes along with metadata." This is automated LLM-driven extraction on every `retain()` call. |
| p_claude | ✅ Verified | Repo contains `.claude-plugin/` and `.claude/skills/` directories. README: `npx skills add https://github.com/vectorize-io/hindsight --skill hindsight-docs` — "Works with Claude Code, Cursor, and other AI coding assistants." Python/Node SDKs available. |
| searchModes=3 | ⚠️ Undersold: 4 | Actually **4 parallel retrieval strategies**: Semantic (vector), Keyword (BM25), Graph (entity/temporal/causal links), Temporal (time range filtering). All fused via RRF. User claimed 3. |

### Partially Verified

| Claim | Issue | Evidence |
|-------|-------|----------|
| offline | LLM-dependent but local LLM supported | Docker mode needs `OPENAI_API_KEY` and LLM. Python Embedded mode still requires `llm_provider`/`llm_api_key`. However, supported providers include `ollama` and `lmstudio` (local LLMs). With a local LLM + Python Embedded or Docker on localhost, Hindsight can run without internet. Not truly "offline" in the no-LLM sense, but can be fully on-prem. |

### Not Present (Not Found in README or Paper)

| Claim | Evidence of Absence |
|-------|---------------------|
| privacy | Not marketed as privacy-first. Cloud offering exists (Hindsight Cloud at `ui.hindsight.vectorize.io`). README doesn't emphasize privacy guarantees. Self-hosted Docker available but no privacy claims beyond standard self-hosting. |
| export | No export API, tool, or format mentioned in README. No migration/export dialog in any screenshot or description. |
| decay | No time-based decay, forgetting curve, or automatic expiration mentioned in README or paper abstract. |
| supersede | No mechanism for marking facts as outdated/superseded. The reflect operation generates new observations, but old ones are not marked superseded — they coexist. No version chain or lifecycle model described. |
| explicitForget | No delete, forget, or unlearn operation. Three core operations are retain/recall/reflect — no forget/delete. |
| dedup | No deduplication mentioned. "Canonical entities" via normalization may reduce duplicates but dedup is not an advertised or explicit feature. |
| narrative | No narrative generation. Reflect produces "observations and insights" — point-level reasoning over existing memories, not multi-session narrative synthesis. |
| recurrence | No recurrence, cycle, or pattern detection mentioned. |

### Schema Fields: Claimed 7 → Actual >> 7

The explicit `retain()` API accepts: `bank_id`, `content`, `context`, `timestamp` = 4 user-facing fields. Behind the scenes, the LLM extraction pipeline produces: entities, relationships, temporal data, memory classification (world/experience), sparse vector, dense vector, metadata. Paper describes 4 logical memory networks. Actual schema likely 10+ fields. User's claim of 7 is in the right ballpark but the current data.js has `schemaFields: 3` which is incorrect.

### Features NOT Claimed but Present

These are significant features the user didn't list:

| Feature | Evidence |
|---------|----------|
| **webUi** | Docker exposes UI at `localhost:9999`. Shown in README screenshots. Full management UI. |
| **reflect / deep reasoning** | `reflect` generates "new observations and insights from existing memories." Paper: "reflection layer reasons over this bank to produce answers and to update information in a traceable way." Equivalent to deep/chain-of-thought search. |
| **Graph search** | Recall includes "Graph: Entity/temporal/causal links" as one of 4 retrieval strategies. |
| **multi-strategy fusion** | RRF (Reciprocal Rank Fusion) + cross-encoder reranking merges results from all 4 strategies. |
| **biomimetic architecture** | 4 memory networks modeled on human memory: world facts, experiences, entity summaries, evolving beliefs. Distinct from simple vector/knowledge-graph approaches. |
| **cloud offering** | Hindsight Cloud at `ui.hindsight.vectorize.io`. Enterprise-ready. |
| **production proven** | "Used in production at Fortune 500 enterprises." |
| **benchmarks** | 91.4% LongMemEval, 89.61% LoCoMo — state of the art as of January 2026. Independently reproduced by Virginia Tech + The Washington Post. |
| **Docker + Helm** | Production deployment via Docker and Helm charts for Kubernetes. |
| **multi-language SDKs** | Python, Node.js/TypeScript, REST, CLI — full suite. |
| **per-user isolation** | Metadata filtering for per-user memory isolation with custom metadata. |
| **academic paper** | Formalized in `arXiv:2512.12818`. Architecture described in detail. |

## Feature Inventory (from source)

### Core Operations (3)
`retain(bank_id, content, context?, timestamp?)` — Store with auto-extraction
`recall(bank_id, query)` — Multi-strategy retrieval
`reflect(bank_id, query)` — Deep reasoning over memories

### Retrieval Strategies (4, not 3)
- **Semantic** — Dense vector similarity
- **Keyword** — BM25 exact matching
- **Graph** — Entity/temporal/causal link traversal
- **Temporal** — Time range filtering
- **Fusion** — RRF + cross-encoder reranking merge

### Memory Networks (4)
1. **World** — Facts about the world
2. **Experiences** — Agent's own experiences
3. **Entity summaries** — Synthesized per-entity profiles
4. **Beliefs** — Evolving, updatable mental models

### Deployment
- Docker (single container or docker-compose with PostgreSQL)
- Python Embedded (no server, `hindsight-all` package)
- Helm charts for Kubernetes
- Hindsight Cloud (managed)

### Clients
- Python: `hindsight-client` (PyPI)
- Node.js/TypeScript: `@vectorize-io/hindsight-client` (npm)
- REST API (documented)
- CLI

### Supported LLM Providers
OpenAI, Anthropic, Gemini, Groq, Ollama (local), LM Studio (local), MiniMax

### Platform Integrations
- Claude Code (`.claude-plugin/`, `.claude/skills/`, `npx skills add`)
- Cursor ("Works with Claude Code, Cursor, and other AI coding assistants")
- Any MCP-compatible agent (via REST API / client SDKs)

## Architecture Notes

- **Storage:** PostgreSQL (Docker) or embedded SQLite/PG. Oracle AI Database also supported for enterprise.
- **LLM dependency:** Required for retain (extraction) and reflect (reasoning). Multiple providers, including local models.
- **Retrieval pipeline:** 4 parallel strategies → RRF fusion → cross-encoder reranking → token-limit trimming
- **Auto-extraction:** Every `retain()` call runs LLM extraction. Not a background process — synchronous with retain.
- **Memory classification:** Memories classified as world facts or experiences on ingestion, affecting retrieval priority.
- **Reflect is incremental:** "reason over this bank to produce answers and to update information in a traceable way" — updates are traceable, not black-box.

## Data.js Corrections Needed

The current data.js entry (lines 575-583) has 16 features incorrectly marked `false`:

| Feature | Current | Should Be |
|---------|---------|------------|
| webUi | false | true |
| entities | false | true |
| keywords | false | true |
| context | false | true |
| timeTravel | false | true |
| fulltext | false | true |
| hybrid | false | true |
| autoExtract | false | true |
| p_claude | false | true |
| searchModes | 1 | 4 |
| schemaFields | 3 | 7+ |
| deployment | "SDK/Library" | "Server (Docker) + SDK + Embedded" |
| storage | "Vector store" | "PostgreSQL + Vector + Graph" |
| integration | "Python API" | "Python/Node SDK + REST + CLI" |
| offline | false | "local llm" (partial) |

Plus: `b_longmemeval` should be `"91.4%"` with `b_methodology: true`.

## Evidence

`evidence: "https://github.com/carsteneu/ai-memory-comparison/blob/main/evidence/hindsight.md"`
