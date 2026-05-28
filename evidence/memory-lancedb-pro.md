# memory-lancedb-pro — Evidence

> **Source:** [GitHub: CortexReach/memory-lancedb-pro](https://github.com/CortexReach/memory-lancedb-pro)
> **Audit date:** 2026-05-28
> **Version reviewed:** v1.1.0-beta.11 (beta channel), v1.0.26 (stable)
> **Evidence base:** README.md, package.json, openclaw.plugin.json, CHANGELOG.md, docs/memory_architecture_analysis.md, src/*.ts

---

## Vital Signs

| Property | Value | Evidence |
|----------|-------|----------|
| **Description** | Enhanced LanceDB memory plugin for OpenClaw — Hybrid Retrieval (Vector + BM25), Cross-Encoder Rerank, Multi-Scope Isolation, Management CLI | `README.md:title` |
| **Stars** | ~4,400 | `README.md:Star 4.4k` (line 1897) |
| **Language** | TypeScript (49%) + JavaScript (50.1%) | `README.md:Languages` (line 1937) |
| **License** | MIT | `README.md:License` (line 1863), `package.json:license` |
| **Deployment** | npm package, OpenClaw plugin | `README.md:npm i memory-lancedb-pro@beta` |
| **Storage** | LanceDB (vector store) | `README.md:dbPath: ~/.openclaw/memory/lancedb-pro` |
| **Integration** | OpenClaw Plugin API (hooks + MCP-like tools), Claude Code skill | `openclaw.plugin.json:hooks.allowConversationAccess`, skill install |
| **Setup** | `openclaw plugins install memory-lancedb-pro@beta` or `npm i memory-lancedb-pro@beta` | `README.md:Quick Start` |
| **Created** | ~2025 Q4 (37 releases, 461 commits by May 2026; v1.0.0 initial npm release in CHANGELOG) | `CHANGELOG.md:v1.0.0 Initial npm release`, 37 releases |
| **Docs URL** | https://github.com/CortexReach/memory-lancedb-pro/tree/master/docs | `README.md:Documentation` (line 1771) |

---

## Architecture

| Feature | Present | Evidence |
|---------|---------|----------|
| **webUi** | ❌ | No web UI. OpenClaw plugin only. No dashboard or viewer mentioned. |
| **offline** | ⚠️ | LanceDB is local. With Ollama embedding (local), fully offline. With cloud embedding (Jina/OpenAI), requires API access. README mentions "Fully Local (Ollama, zero API cost)" deployment plan. |
| **privacy** | ⚠️ | Local LanceDB storage. But embedding/LLM calls go to external APIs by default. Fully local only with Ollama. No explicit privacy guarantees in docs. |
| **export** | ✅ | `memory-pro export --scope global --output memories.json` and `memory-pro import`. Auto JSONL backup every 24h. `mdMirror` dual-writes to Markdown files. |
| **multiAgent** | ✅ | Multi-scope isolation: `global`, `agent:<id>`, `project:<id>`, `user:<id>`, `custom:<name>`. Agent-level access control via `scopes.agentAccess`. `autoRecallExcludeAgents` per-agent exclusion. |
| **llmFlex** | ✅ | Any OpenAI-compatible embedding (Jina, OpenAI, Voyage, Gemini, Ollama, Azure). Configurable LLM for smart extraction with OAuth support. 4 deployment plans: Jina+OpenAI, SiliconFlow, OpenAI-only, Ollama. |

### Architecture Citations

- **offline (Ollama):** `README.md:Deployment plans: Fully Local (Ollama, zero API cost)`
- **export:** `README.md:openclaw memory-pro export [--scope global] [--output memories.json]` (line 1461)
- **multiAgent:** `openclaw.plugin.json:scopes.agentAccess`, `README.md:Multi-Scope Isolation: agent:<id>, project:<id>, user:<id>` (line 973)
- **llmFlex:** `README.md:Embedding Providers` (line 1170), `README.md:Rerank Providers` (line 1222)

---

## Data Model

| Feature | Present | Evidence |
|---------|---------|----------|
| **entities** | ✅ | Smart extraction has `entities` category. `metadata.memory_category = "entities"`. Also `profile`, `preferences`, `events`, `cases`, `patterns`. |
| **actions** | ❌ | No explicit action/junction table. Actions are captured as memory text content. |
| **keywords** | ❌ | No keyword/tag system. Five storage categories (`preference`/`fact`/`decision`/`entity`/`other`) but no freeform tags. |
| **context** | ✅ | L0/L1/L2 layered context: `l0_abstract` (one-sentence index), `l1_overview` (structured summary), `l2_content` (full narrative). `source_session` tracks origin. |
| **source** | ✅ | `metadata.source_session` links to source session. Noise classification: noise prototypes track signal quality. `mdMirror` writes human-readable source. |
| **emotional** | ❌ | No emotional valence or sentiment scoring. |
| **conflict** | ❌ | No contradiction detection. The dedup logic handles merge/skip but not explicit conflict surfacing. |
| **layeredMemory** | ✅ | L0/L1/L2 semantic pyramid (like TencentDB). Three-tier promotion: `Peripheral ↔ Working ↔ Core`. Canonical Corpus layer (file-based). |
| **timeTravel** | ❌ | Has `timestamp` and `last_accessed_at` but no explicit time-travel replay or point-in-time query. `valid_until`/`valid_at` semantics absent. |
| **schemaFields** | ~17 | 8 LanceDB columns (`id`, `text`, `vector`, `category`, `scope`, `importance`, `timestamp`, `metadata`) + ~9 semantic metadata keys (`memory_category`, `tier`, `l0_abstract`, `l1_overview`, `l2_content`, `access_count`, `confidence`, `last_accessed_at`, `source_session`). Additional keys: `type`, `tier_updated_at`, `migratedFrom`, `originalId`. |

### Data Model Citations

- **entities:** `docs/memory_architecture_analysis.md: 6-category extraction: profile, preferences, entities, events, cases, patterns`
- **context (layered):** `README.md:L0/L1/L2 Layered Storage: L0 (one-sentence index) → L1 (structured summary) → L2 (full narrative)` (line 956)
- **source:** `docs/memory_architecture_analysis.md:metadata JSON: memory_category tier l0/l1/l2 access_count confidence ... source_session`
- **layeredMemory (tiers):** `README.md:Three-Tier Promotion: Peripheral ↔ Working ↔ Core with configurable thresholds` (line 965)
- **schemaFields:** `README.md:Database Schema` (line 1564), `docs/memory_architecture_analysis.md:current metadata fields` (line ~180)

---

## Search & Retrieval

| Feature | Present | Evidence |
|---------|---------|----------|
| **fulltext** | ✅ | BM25 FTS via LanceDB FTS index. Configurable `bm25Weight`. Falls back to lexical search when FTS unavailable. |
| **semantic** | ✅ | Vector search via LanceDB ANN (cosine distance). Provider-agnostic embedding with task-aware embeddings (`taskQuery`/`taskPassage`). |
| **hybrid** | ✅ | Vector + BM25 fusion: vector score as base, BM25 hits receive weighted boost. Configurable `vectorWeight`/`bm25Weight`. Not standard RRF — tuned for real-world recall. |
| **deep** | ❌ | No deep search over raw conversation/thinking content. Session transcripts are indexed via canonicalCorpus but not searchable as thinking. |
| **codeGraph** | ❌ | No code graph or Tree-sitter integration. Purely text-based memory. |
| **docsSearch** | ❌ | No documentation search. `canonicalCorpus` indexes MEMORY.md and memory/*.md files but this is file indexing, not API docs. |
| **factQuery** | ✅ | `memory_list --category <type> --scope <scope> --limit N`. `memory_stats` for aggregations. Metadata filtering by scope/category. |
| **timeline** | ❌ | Timestamps exist but no explicit timeline search mode. No `before`/`since` temporal query filter in search. |
| **searchModes** | 3 | (1) hybrid (vector+BM25 fusion), (2) vector-only, (3) lexical fallback (no FTS). Plus adaptive retrieval mode that decides whether to search at all. |

### Search Citations

- **fulltext (BM25):** `README.md:BM25 Full-Text Search — exact keyword matching via LanceDB FTS index` (line 906)
- **semantic (vector):** `README.md:Vector Search — semantic similarity via LanceDB ANN (cosine distance)` (line 905)
- **hybrid:** `README.md:Hybrid Fusion — vector score as base, BM25 hits receive a weighted boost` (line 907)
- **factQuery:** `README.md:openclaw memory-pro list [--scope global] [--category fact] [--limit 20]` (line 1453)
- **searchModes:** `openclaw.plugin.json:retrieval.mode: enum [hybrid, vector]` (line ~73), `README.md:lexicalFallbackSearch()` in architecture docs

---

## Knowledge Lifecycle

| Feature | Present | Evidence |
|---------|---------|----------|
| **decay** | ✅ | Weibull stretched-exponential decay engine. Composite score = recency + frequency + intrinsic (importance × confidence). Tier-specific beta values (core=0.8, working=1.0, peripheral=1.3). Configurable half-life (default 30 days). |
| **supersede** | ✅ | `memory_update` — updates text and re-embeds while preserving `id` and `timestamp`. `memory_promote` tool. Tier promotion/demotion (`Peripheral ↔ Working ↔ Core`). Memory compaction merges similar old entries. |
| **contradiction** | ❌ | No contradiction detection. Two-stage dedup handles CREATE/MERGE/SKIP but doesn't surface contradictions. |
| **quarantine** | ✅ | `autoRecallSuppressionDurationMs` (default 30min): suppresses memories with high `bad_recall_count`. `bad_recall_count` auto-decays after 24h. Session summaries excluded from tier evaluation. |
| **autoResolve** | ❌ | No auto-resolution or TTL-based cleanup. Tier promotion/demotion is automatic but doesn't delete. Compaction merges but doesn't auto-delete. |
| **trustModel** | ✅ | `importance` (0–1) × `confidence` (0–1) scoring. Admission control (`admissionControl`) with type priors, utility, confidence, novelty, recency weights. Source trust via `metadata.source_session`. |
| **explicitForget** | ✅ | `memory_forget` tool. `memory-pro delete <id>`, `memory-pro delete-bulk --scope global --before DATE`. Noise filtering auto-filters low-quality content. |

### Lifecycle Citations

- **decay:** `README.md:Weibull Decay Engine: composite score = recency + frequency + intrinsic value` (line 964); `src/decay-engine.ts` in architecture
- **supersede:** `README.md:memory_update supports updating entries (re-embeds, preserves timestamp)` (docs); `CHANGELOG.md:1.1.0-beta.2 Tier transitions (best-effort)`
- **quarantine:** `openclaw.plugin.json:autoRecallSuppressionDurationMs: default 1800000 (30 minutes)` (line 169)
- **trustModel:** `openclaw.plugin.json:admissionControl with typePriors (profile:0.95, preferences:0.9, patterns:0.85, cases:0.8, entities:0.75, events:0.45)` (line ~260)
- **explicitForget:** `README.md:openclaw memory-pro delete <id>` (line 1459), `openclaw.plugin.json:contracts.tools: memory_forget` (line 7)

---

## Extraction Pipeline

| Feature | Present | Evidence |
|---------|---------|----------|
| **autoExtract** | ✅ | `autoCapture` on `agent_end` hook. Smart Extraction: LLM-powered 6-category extraction (profile, preferences, entities, events, cases, patterns). Regex fallback when smart extraction disabled. Up to 3 memories per turn. |
| **contentPreproc** | ✅ | Embedding-based noise pre-filtering (NoisePrototypeBank: language-agnostic, 15+ multilingual prototypes, threshold 0.82). Regex noise filter (agent refusals, meta-questions, greetings). Session compression (`sessionCompression.enabled`) with scoring. |
| **dedup** | ✅ | Two-stage dedup: (1) vector similarity pre-filter (cosine ≥ 0.7), (2) LLM semantic dedup decision: CREATE/MERGE/SKIP. Category-aware merge: profile always merges, events/cases append-only. |
| **qualityRefine** | ❌ | No separate quality refinement LLM pass. Smart extraction does inline dedup but no explicit "improve quality" reprocessing stage. Admission control filters low-value candidates before persistence. |
| **narrative** | ❌ | No narrative generation. L0/L1/L2 are structured summarization layers but not prose narrative generation from memories. Dreaming engine (light/deep/REM) does reflection but generates reports, not narratives. |
| **clustering** | ✅ | `memoryCompaction`: progressive summarization consolidating semantically similar old memories (cosine similarity threshold 0.88, minClusterSize 2). Periodic (configurable cooldown, default 24h). |
| **recurrence** | ❌ | No recurrence detection. Clustering merges similar memories but doesn't track pattern recurrence over time. No "this happened again" signals. |
| **persona** | ✅ | Smart extraction `profile` category captures user traits. `preferences` category captures preferences. Admission control typePriors favor profile (0.95) and preferences (0.9) heavily. |

### Extraction Citations

- **autoExtract:** `README.md:Auto-Capture (agent_end): extracts preference/fact/decision/entity from conversations` (line 981); `README.md:LLM-Powered 6-Category Extraction` (line 955)
- **contentPreproc:** `docs/memory_architecture_analysis.md:NoisePrototypeBank — language-agnostic noise detection, 15+ multilingual prototypes, threshold 0.82` (line ~110)
- **dedup:** `README.md:Two-Stage Dedup: vector similarity pre-filter (≥0.7) → LLM semantic decision (CREATE/MERGE/SKIP)` (line 957)
- **clustering:** `openclaw.plugin.json:memoryCompaction: similarityThreshold 0.88, minClusterSize 2, minAgeDays 7` (line ~360)
- **persona:** `openclaw.plugin.json:admissionControl.typePriors.profile: 0.95, preferences: 0.9` (line ~274)

---

## Platform Support

| Feature | Present | Evidence |
|---------|---------|----------|
| **p_claude** | ✅ | Claude Code skill available: `git clone ... ~/.claude/skills/memory-lancedb-pro`. README shows Claude Code install instructions. |
| **p_codex** | ❌ | Not mentioned. OpenClaw plugin — depends on OpenClaw runtime, not Codex. |
| **p_opencode** | ❌ | Not mentioned. |
| **p_gemini** | ❌ | Not mentioned. |
| **p_copilot** | ❌ | Not mentioned. |
| **p_cursor** | ❌ | Not mentioned. May work if Cursor uses OpenClaw, but no direct Cursor support. |
| **p_windsurf** | ❌ | Not mentioned. |
| **p_openclaw** | ✅ | **Primary platform.** Native OpenClaw plugin with full hook integration (`before_prompt_build`, `agent_end`, `message_received`, `command:new`), tool contracts, CLI commands, and memory slot binding. |
| **p_hermes** | ❌ | Not mentioned. |
| **p_pi** | ❌ | Not mentioned. |
| **p_antigravity** | ❌ | Not mentioned. |

### Platform Citations

- **p_claude:** `README.md:Install for Claude Code: git clone ... ~/.claude/skills/memory-lancedb-pro` (line 779)
- **p_openclaw:** `README.md:OpenClaw Plugin badge`, `openclaw.plugin.json:id: memory-lancedb-pro, kind: memory` (line 20, 24)

---

## Benchmarks

| Feature | Present | Evidence |
|---------|---------|----------|
| **b_locomo** | ❌ | `package.json` has `bench:locomo` script (`jiti benchmark/run.ts --benchmark locomo`) but benchmark directory returns 404 — no published results. |
| **b_longmemeval** | ❌ | `package.json` has `bench:longmemeval` script. Same as above — no published results found. |
| **b_personamem** | ❌ | Not mentioned anywhere. |
| **b_token** | ❌ | No token reduction claims or measurements. |
| **b_methodology** | ❌ | No published benchmark methodology. Architecture analysis is thorough but no evaluation methodology. |

### Benchmark Citations

- **bench scripts:** `package.json:scripts: bench:locomo, bench:longmemeval` — infrastructure exists but no published scores
- **No LoCoMo score found** in README, CHANGELOG, or docs

---

## Unique Differentiators

1. **OpenClaw-native memory slot** — Only system that binds directly into OpenClaw's `plugins.slots.memory`, replacing the built-in memory-lancedb. Tightest OpenClaw integration in the comparison.

2. **Canonical Corpus + LanceDB dual-plane** — Memory files (MEMORY.md, memory/**/*.md) remain source of truth, LanceDB is the semantic index. Search returns grounded paths, line spans, snippets, and citations.

3. **Dreaming sidecar engine** — Three-phase reflection (light/deep/REM) that processes memories offline, generates dream reports, and has a memory recovery subsystem. Unique among compared systems.

4. **A-MAC-style admission control** — Configurable admission governance on the write path: utility, confidence, novelty, recency, and type-prior scoring before persistence. Category-aware thresholds (profile: 0.95, events: 0.45).

5. **NoisePrototypeBank with LLM feedback loop** — Language-agnostic embedding-based noise detection that learns from LLM extraction failures (texts producing zero candidates are added to the noise bank).

6. **Self-improvement toolset** — `self_improvement_log`, `self_improvement_extract_skill`, `self_improvement_review` tools for skill extraction from mistakes and pattern learning.

7. **12-language README** — README available in English, Chinese (Simplified/Traditional), Japanese, Korean, French, Spanish, German, Italian, Russian, Portuguese (Brazil).

---

## Features NOT present (notable gaps vs comparison)

- **No contradiction detection** — Dedup handles merge/skip but doesn't flag conflicting facts
- **No time-travel** — Has timestamps but no point-in-time query or replay
- **No code graph** — Text-only memory, no Tree-sitter or code-aware indexing
- **No deep search** — Can't search over raw thinking/agent reasoning traces
- **No published benchmarks** — Benchmark infrastructure exists but no scores published
- **No emotional signals** — No sentiment or emotional valence tracking
- **No narrative generation** — L0/L1/L2 summarization but no prose narrative
- **No recurrence detection** — Can't detect repeating patterns across sessions
- **Platform-locked** — OpenClaw-only (plus Claude Code skill); no Codex, Cursor, Windsurf, Gemini CLI, OpenCode support
- **No web UI** — CLI and agent tools only, no dashboard
- **No auto-resolution** — No TTL-based or threshold-based auto-cleanup
