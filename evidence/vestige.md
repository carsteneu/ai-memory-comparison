# Vestige Audit

**Date:** 2026-05-28
**Source:** https://github.com/samvallad33/vestige
**Version:** v2.1.23 (latest as of audit)
**Language:** Rust
**Stars:** 540
**License:** AGPL-3.0

## URL Correction

The claimed URL `https://github.com/nicholasgriffintn/vestige` returns **404** — the repository does not exist at that path and never redirected. The actual repository is `https://github.com/samvallad33/vestige`.

## Summary

Vestige is a Rust-based "cognitive memory for AI agents" exposed as an MCP server. It implements neuroscience-inspired primitives (FSRS-6 spaced repetition, prediction error gating, synaptic tagging, spreading activation, memory dreaming). Runs as a single ~20MB binary with an optional SvelteKit + Three.js 3D dashboard on localhost:3927. 25 MCP tools across core memory, cognitive engine, autonomic, scoring/dedup, maintenance, deep reference, and active forgetting categories.

## Claim Audit

### Verified Claims

| Claim | Status | Evidence |
|-------|--------|----------|
| offline | ✅ Verified | "100% local. Zero cloud."; "First run downloads embedding model (~130MB), then fully offline" |
| privacy | ✅ Verified | "your data never leaves your machine" |
| keywords | ✅ Verified | `search` tool: "Concrete literal search for exact identifiers"; keyword-mode search |
| timeline | ✅ Verified | `memory_timeline`: "Browse chronologically, grouped by day"; `memory_changelog`: "Audit trail of state transitions" |
| p_claude | ✅ Verified | "Works Everywhere" table lists Claude Code integration |
| p_codex | ✅ Verified | "Works Everywhere" table lists Codex integration |
| p_windsurf | ✅ Verified | "Works Everywhere" table lists Windsurf integration |

### Partially Verified

| Claim | Issue | Evidence |
|-------|-------|----------|
| entities | Not a named feature; memories exist as graph nodes with connections via spreading activation. No dedicated "entity" metadata tagging. | Knowledge graph with node-edge structure. No entity-type annotation on memories. |
| autoExtract | Not called "autoExtract." The `smart_ingest` tool performs prediction error gating (CREATE/UPDATE/SUPERSEDE) which is a form of automatic extraction/classification, but is triggered by tool call, not automatic background extraction. | `smart_ingest`: "Intelligent storage with CREATE/UPDATE/SUPERSEDE via Prediction Error Gating" |
| searchModes=4 | Cannot confirm exactly 4. The `search` tool has concrete/literal, keyword, semantic (HyDE), reranking, temporal, competition, spreading activation — at least 7 stages. These are not presented as discrete "modes" numbered as 4. | "Concrete literal search for exact identifiers, or 7-stage cognitive search" |

### Unverified (not enough data)

| Claim | Issue |
|-------|-------|
| schemaFields=5 | README does not describe DB schema structure or field count. Mentions SQLite + FTS5 + USearch HNSW vector store, but no schema enumeration. |

### Corrections — Claimed Absent, Actually Present

| Feature | User Claim | Reality |
|---------|-----------|---------|
| **webUi** | absent | **Present.** Full SvelteKit + Three.js 3D dashboard (`vestige dashboard` on localhost:3927/Dashboard) with WebSocket real-time events, memory birth animations, retention curves. Heavily marketed. |
| **fulltext** | false | **Present.** SQLite FTS5 explicitly listed in architecture: "SQLite + FTS5 · USearch HNSW · Nomic Embed v1.5" |
| **semantic** | absent | **Present.** 7-stage cognitive search includes "semantic" + HyDE query expansion: "Template-based Hypothetical Document Embeddings" |
| **hybrid** | absent | **Present.** "7-stage cognitive search — HyDE expansion + keyword + semantic + reranking + temporal + competition + spreading activation" |
| **deep** | absent | **Present.** `deep_reference` tool: "8-stage pipeline: FSRS-6 trust scoring, intent classification, spreading activation, temporal supersession, contradiction analysis, relation assessment, dream insight integration, reasoning chain generation" |
| **decay** | absent | **Present.** FSRS-6 spaced repetition: "21 parameters governing the mathematics of forgetting." Central marketing pillar. |
| **supersede** | absent | **Present.** `smart_ingest` explicitly supports SUPERSEDE mode. "When new information arrives, Vestige compares it against existing memories. Redundant? Merged. Contradictory? Superseded." |
| **contradiction** | absent | **Present.** `contradictions` MCP tool: "Honest memory inspection. Scans a topic or recent memories for trust-weighted disagreements." v2.1.2 added "First-class contradiction inspection." |
| **trustModel** | absent | **Present.** FSRS-6 trust scoring in `deep_reference` pipeline; "trust-weighted disagreements" in contradictions tool. |
| **explicitForget** | absent | **Present.** Two distinct forgetting mechanisms: `suppress` (reversible 24h inhibition, Anderson 2025 SIF) and `purge` (irreversible, permanent deletion). Both are intentional, user-triggered. |
| **dedup** | absent | **Present.** `find_duplicates`: "Detect and merge redundant memories via cosine similarity." Also prediction error gating auto-merges during ingest. |

### Confirmed Absent

The following features are genuinely not mentioned anywhere in the README:

multiAgent, actions, anticipatedQueries, triggerRules, domainTag, taskType, context (as category), source (as metadata field), originTrust, emotional, conflict (as explicit module, though contradictions related), layeredMemory, timeTravel, codeGraph (has knowledge graph, not code graph), docsSearch, factQuery, quarantine, autoResolve, contentPreproc, qualityRefine, narrative, clustering, recurrence, persona.

### Special: fulltext=false but keywords=true

User flagged this as an unusual combination. Confirmed: **fulltext IS present** via SQLite FTS5. The `search` tool has both concrete/keyword matching and semantic search. The claim of "fulltext=false, keywords=true" is contradicted by the README.

## Feature Inventory (from README)

### MCP Tools (25)
`session_context`, `search`, `smart_ingest`, `memory`, `codebase`, `intention`, `dream`, `explore_connections`, `predict`, `memory_health`, `memory_graph`, `importance_score`, `find_duplicates`, `system_status`, `consolidate`, `memory_timeline`, `memory_changelog`, `backup`, `export`, `gc`, `restore`, `deep_reference`, `cross_reference`, `contradictions`, `suppress`

### Cognitive Modules (30)
17 neuroscience, 11 advanced, 2 search — covering prediction error gating, FSRS-6, HyDE expansion, synaptic tagging, spreading activation, dual-strength model, memory dreaming, waking SWR tagging, autonomic regulation, active forgetting (suppression-induced forgetting + Rac1 cascade).

### Platform Support
macOS ARM + Intel, Linux x86_64, Windows x86_64. MCP stdio transport. Optional HTTP MCP (`--http`).

### Optional Features
- Qwen3 0.6B embeddings (Candle backend, Metal on Apple Silicon)
- CUDA/cuDNN for NVIDIA GPU acceleration
- SANHEDRIN verifier (off by default, OpenAI-compatible endpoint required)
- SQLCipher encryption
- Cognitive Sandwich Claude Code hooks (opt-in)

### Dashboard
SvelteKit 2 + Svelte 5 + Three.js + Tailwind CSS 4 + WebSocket. 3D force-directed graph, bloom post-processing, memory birth animations, FSRS retention curves, command palette, PWA installable. 16 left-nav pages.

## Architecture Notes

- Monorepo: Rust core/MCP/e2e + SvelteKit dashboard + hook coverage
- ~80,000 lines of Rust
- Single binary deployment (~20MB compressed)
- Embedding: Nomic Embed Text v1.5 (768d -> 256d Matryoshka, 8192 context) — downloaded on first run (~130MB)
- Vector search: USearch HNSW
- Reranker: Jina Reranker v1 Turbo (38M params)
- Backend events: 20-event WebSocket bus powering real-time dashboard updates
- Autopilot: background tasks for event routing, duplicate detection, supervisor loop with panic recovery

## Notable Design Decisions

1. **Neuroscience-first branding.** Every feature is anchored to a real cognitive science paper (Bjork & Bjork 1992, Buzsaki 2015, Anderson 2025, etc.). The "active forgetting" primitive is explicitly distinguished from passive decay.

2. **Agent-neutral, MCP-native.** Default transport is stdio MCP. Any MCP client can use it. HTTP transport is opt-in.

3. **Dashboard as first-class surface.** Unlike many memory systems that are invisible, Vestige treats the 3D visualization as a core product feature, not an afterthought.

4. **AGPL-3.0 license.** Network service provision requires open-sourcing modifications.

5. **No cloud dependency.** Model download is one-time. Everything afterward runs locally.

## Evidence

`evidence: "https://github.com/carsteneu/ai-memory-comparison/blob/main/evidence/vestige.md"`
