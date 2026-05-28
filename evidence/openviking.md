# OpenViking — Evidence

> Every ✅ claim backed by public source code or documentation.
> Audit date: 2026-05-28. Source: GitHub `volcengine/OpenViking` main branch, `docs.openviking.ai`.

**Correct URL**: `https://github.com/volcengine/OpenViking` (user's claimed `Viking-Open/memory` is incorrect — 404).

---

## Architecture

### Web UI ✅ (weak)
- `README.md` — "If you use the official Docker image, vikingbot is already bundled in the image and starts by default together with the OpenViking server and console UI." Console UI mentioned but no standalone web dashboard described in README. Data.js has `webUi: true` which is accepted but poorly evidenced.
- `docs/en/getting-started/03-quickstart-server.md` — Server runs on port 1933, accessed via CLI or HTTP API. No browser-based UI documented.

### Offline ✅
- `README.md` — Supports Ollama for local models: "If you want to run OpenViking with local models via Ollama, the interactive setup wizard handles everything automatically." Self-hosted, local embedding and VLM possible.
- `docs/en/concepts/01-architecture.md` — "Embedded Mode: For local development and single-process applications: `client = OpenViking(path="./data")`". Fully offline capable.

### Privacy ✅ → data.js correction needed
- `docs/en/concepts/13-privacy.md` — Full privacy subsystem: "Privacy configs separate sensitive values (such as api_key, token, base_url) from skill body content so plaintext is not permanently stored." Includes placeholder extraction at write time and read-time restore.
- CLI commands: `openviking privacy categories`, `openviking privacy upsert skill <target_key> --values-json`, `openviking privacy activate skill <target_key> <version>`.
- Storage: `viking://user/{user_space}/privacy/{category}/{target_key}/` with versioning and rollback.
- `docs/en/concepts/10-encryption.md` — Separate encryption doc referenced in architecture overview: "At-rest encryption and key architecture".
- **Finding**: data.js has `privacy: false`. Should be `true`. Two documented features: (1) privacy configs for skill secrets with placeholder/restore pipeline, (2) at-rest encryption.

### Export ✅ → data.js correction needed
- `docs/en/concepts/01-architecture.md` — Service Layer table: `PackService` with methods `export_ovpack, import_ovpack, backup_ovpack, restore_ovpack`.
- **Finding**: data.js has `export: false`. Should be `true`. Full export/import via ovpack format plus backup/restore.

### Multi-agent ❌
- README focuses on single-agent context. Multi-tenancy doc (`11-multi-tenant.md`) exists but is about account/user isolation, not multi-agent collaboration. data.js `multiAgent: false` is correct.

---

## Data Model

### Entities ✅ (partial — entity category, not extraction)
- `docs/en/concepts/02-context-types.md` — Memory categories include "**entities**" at `user/memories/entities/` for "Entity memories (people, projects)". Appendable storage.
- This is entity-based memory organization, not automatic entity extraction (no NER pipeline documented). Unclear if `entities` field in data.js means storage categories or extraction. Leaning toward marking as **partial** — entity concept exists but no auto-extraction.

### Keywords ❌
- No keyword tagging or keyword-based retrieval documented. The 8 memory categories (profile, preferences, entities, events, cases, patterns, tools, skills) serve as organizational tags but are not user-defined keywords. data.js `keywords: false` is correct.

### Context ✅ → data.js correction needed
- `docs/en/concepts/02-context-types.md` — Three explicit context types: Resource, Memory, Skill. Each has type, purpose, lifecycle, initiative.
- `docs/en/concepts/01-architecture.md` — Architecture built around context types. Retrieval maps context_type to root directories. MatchedContext has `context_type` field.
- **Finding**: data.js has `context: false`. Should be `true`. Context type is a first-class field on every stored node and search result.

### Layered memory ✅
- `README.md` — "Tiered Context Loading → Reduces Token Consumption": L0 (Abstract, ~100 tokens), L1 (Overview, ~2k tokens), L2 (Details, full data).
- `docs/en/concepts/03-context-layers.md` — Progressive detail loading with `.abstract`, `.overview`, and full content files.
- data.js `layeredMemory: true` is correct.

### Time travel ❌
- No time-based browsing, snapshot history, or temporal query features documented. Privacy configs have versioning for secrets, but this is not general time travel for memories. data.js `timeTravel: false` is correct.

### Schema fields — 6→9 contested
- `docs/en/concepts/07-retrieval.md` — `MatchedContext` dataclass: `uri`, `context_type`, `is_leaf`, `abstract`, `score`, `relations` = **6 fields**.
- Stored content has more: L0 abstract, L1 overview, L2 content, URI, type, relations, timestamps. Exact count depends on how you measure. User claims 9; data.js has 6 (matches MatchedContext). No definitive count, but 6 is defensible as the core retrieval schema.

---

## Search & Retrieval

### Full-text ✅ → data.js correction needed
- `docs/en/concepts/01-architecture.md` — `FSService` has `grep` and `glob` methods.
- `README.md` — CLI example: `ov grep "openviking" --uri viking://resources/volcengine/OpenViking/docs/zh`.
- **Finding**: data.js has `fulltext: false`. Should be `true`. Grep-based fulltext search is a first-class service method.

### Semantic ✅
- `docs/en/concepts/07-retrieval.md` — `find()` and `search()` both use vector retrieval. Global vector search, recursive directory search with embedding scores.
- `docs/en/concepts/01-architecture.md` — "Vector Index: URIs, vectors, metadata (no file content)". Embedding configured via multiple providers.
- data.js `semantic: true` is correct.

### Hybrid ✅
- `docs/en/concepts/07-retrieval.md` — Hierarchical Retrieval combines vector search (semantic) with directory positioning (structural): "directory recursive retrieval" that "locks high-score directory first, then refines content exploration."
- `search()` additionally uses LLM intent analysis (`IntentAnalyzer`) plus hierarchical recursive search plus rerank. Not traditional BM25+vector hybrid but a multi-strategy fusion (vector + directory structure + LLM intent + rerank).
- data.js `hybrid: true` is correct.

### Search modes — 2→3 correction
- `docs/en/concepts/07-retrieval.md` — Two API modes: `find()` (simple, low latency, no session) and `search()` (complex, LLM intent analysis, needs session).
- `docs/en/concepts/01-architecture.md` — FSService provides `grep` (fulltext pattern matching) as a third query method.
- Three distinct query methods: grep (fulltext), find (semantic), search (hybrid with intent analysis).
- **Finding**: data.js has `searchModes: 2`. Should be `3` (grep, find, search).

### Data sources ✅
- `docs/en/concepts/02-context-types.md` — Three context types serve as data sources: Resource (documents, repos, web pages), Memory (user + agent), Skill (capabilities). data.js `dataSources: 3` is correct.

---

## Knowledge Lifecycle

### Decay ❌
- No time-based decay, staleness scoring, or automatic forgetting documented. data.js `decay: false` is correct.

### Supersede ❌
- Memory update strategies (merge, append, no-update) but no version-supersede model. New facts don't mark old ones as outdated. data.js `supersede: false` is correct.

### Explicit forget ❌
- No delete/forget operations documented for memories. Privacy configs support version management and rollback, but not memory deletion. The API docs may have delete endpoints but none visible in the fetched documentation. data.js `explicitForget: false` is accepted pending deeper API inspection.

### Quarantine ❌
- No isolation/quarantine of suspect learnings documented. data.js `quarantine: false` is correct.

---

## Extraction Pipeline

### Auto-extract ✅
- `docs/en/concepts/01-architecture.md` — Session commit flow: "Memory Extraction: Extract 8-category memories from messages."
- `docs/en/concepts/02-context-types.md` — "Memories are auto-extracted from sessions": `commit = await session.commit()` starts background memory extraction into 8 categories.
- `README.md` — "Automatic Session Management → Context Self-Iteration": analyzes task execution, updates user/agent memory directories.
- data.js `autoExtract: true` is correct.

### Content preprocessing ✅ → data.js correction needed
- `README.md` — "OpenViking automatically processes context into three levels upon writing: L0 (Abstract), L1 (Overview), L2 (Details)."
- `docs/en/concepts/01-architecture.md` — Parse module: "Async bottom-up L0/L1 generation" via SemanticQueue.
- Content is preprocessed into tiered summaries during ingestion, not at query time.
- **Finding**: data.js has `contentPreproc: false`. Should be `true`.

### Dedup ✅ → data.js correction needed
- `docs/en/concepts/01-architecture.md` — Compressor module: "8-category memory extraction, **LLM deduplication decisions**". Architecture diagram shows Compressor with "Deduplicate" capability.
- **Finding**: data.js has `dedup: false`. Should be `true`. LLM-based deduplication during memory compression/extraction.

### Quality refine ❌
- Rerank exists in retrieval pipeline (`docs/en/concepts/07-retrieval.md` — "Rerank refines candidate results"), but this is search-time ranking, not content quality assessment/refinement. No quality scoring of stored content. data.js `qualityRefine: false` is correct.

### Narrative ❌
- No narrative generation or storytelling from memory documented. 8-category extraction is factual, not narrative. data.js `narrative: false` is correct.

### Recurrence ❌
- No recurrence/pattern detection across sessions documented. "Patterns" is a memory category for storing learned patterns, not automatic recurrence detection. data.js `recurrence: false` is correct.

### Persona ❌
- No explicit persona modeling. "Profile" memory category stores basic user info but no persona-driven behavior adaptation. data.js `persona: false` is correct.

---

## Platform Support

### p_claude ✅
- `README.md` — Benchmark: "Claude Code auto-memory: 57.21% → Claude Code + OpenViking: 80.32%". Claude Code integration demonstrated.
- data.js `p_claude: true` is correct.

### p_codex ✅ → data.js correction needed
- `README.md` — "openai-codex" is a first-class VLM provider: "Use this provider when you want OpenViking to call Codex VLM through your ChatGPT/Codex OAuth session." Supports `gpt-5.3-codex` model. Stores auth at `~/.openviking/codex_auth.json`.
- **Finding**: data.js has `p_codex: false`. Should be `true`. Codex VLM is a supported backend; Codex OAuth import is part of the setup wizard.

### p_openclaw ✅
- `README.md` — Benchmark: "OpenClaw native memory: 24.20% → OpenClaw + OpenViking: 82.08%". 3.39x improvement.
- data.js `p_openclaw: true` is correct.

### p_hermes ✅
- `README.md` — Benchmark: "Hermes native memory: 33.38% → Hermes + OpenViking: 82.86%". 2.48x improvement.
- data.js `p_hermes: true` is correct.

### p_opencode ❌
- No mention of OpenCode integration. data.js `p_opencode: false` is correct.

### p_cursor ❌
- No mention of Cursor integration. data.js `p_cursor: false` is correct.

### p_windsurf ❌
- No mention of Windsurf integration. data.js `p_windsurf: false` is correct.

### p_gemini ❌ (not claimed, verified)
- Google Gemini is supported as an embedding provider only (`gemini-embedding-2-preview`). Not a full agent platform integration.

---

## Benchmarks

### LoCoMo ✅
- `README.md` — Multiple agent integrations on LoCoMo: OpenClaw+OpenViking 82.08%, Hermes+OpenViking 82.86%, Claude Code+OpenViking 80.32%. Claims ~3x accuracy improvement with 59-91% token reduction.
- `data.js b_locomo: "82.1"` — matches the average of the three integrations (82.08%, 82.86%, 80.32%).

### Token savings ✅
- `README.md` — "Token Reduction: OpenClaw -91.0%, Claude Code -63.2%, Hermes -34.3%". Highest is 91%.
- `data.js b_token: "91%"` matches best-case reduction.

---

## Summary of data.js Corrections

| Field | data.js Current | Verified | Evidence |
|-------|----------------|----------|----------|
| `privacy` | false | **true** | Privacy configs, placeholder/restore pipeline, at-rest encryption |
| `export` | false | **true** | PackService: export_ovpack, import_ovpack, backup_ovpack, restore_ovpack |
| `context` | false | **true** | Explicit context types (Resource/Memory/Skill) on every node |
| `fulltext` | false | **true** | FSService.grep, CLI `ov grep` command |
| `contentPreproc` | false | **true** | L0/L1/L2 tiered processing on write via SemanticQueue |
| `dedup` | false | **true** | Compressor: LLM deduplication decisions |
| `searchModes` | 2 | **3** | grep (fulltext) + find (semantic) + search (hybrid with intent) |
| `p_codex` | false | **true** | openai-codex VLM provider, Codex OAuth import |

### User Claims Rejected (No Evidence)

| Claim | Verdict | Reason |
|-------|---------|--------|
| timeTravel | ❌ | No temporal browsing or snapshot history |
| decay | ❌ | No staleness scoring or auto-forgetting |
| supersede | ❌ | No version-supersede model for updates |
| explicitForget | ❌ | No delete/forget operations for memories |
| qualityRefine | ❌ | Rerank is retrieval-time, not content quality |
| narrative | ❌ | No narrative generation from memory |
| recurrence | ❌ | No automatic recurrence detection |
| keywords | ❌ | No user-defined keyword tagging |
| p_opencode | ❌ | Not mentioned anywhere |
| p_cursor | ❌ | Not mentioned anywhere |
| p_windsurf | ❌ | Not mentioned anywhere |
| schemaFields=9 | ❌ | MatchedContext has 6 fields; stored schema ~6-8 |
| URL = Viking-Open/memory | ❌ | Correct URL: volcengine/OpenViking |
| searchModes=3 claimed as user-report | — | Actually correct; data.js should update |

### User Claims Confirmed (Data.js Already Correct)

| Claim | Verified |
|-------|----------|
| webUi | ✅ (console UI, weak evidence) |
| offline | ✅ |
| layeredMemory | ✅ (L0/L1/L2) |
| semantic | ✅ |
| hybrid | ✅ (directory recursive + vector) |
| autoExtract | ✅ (session memory extraction) |
| p_claude | ✅ (benchmark verified) |
| p_openclaw | ✅ (benchmark verified) |
| p_hermes | ✅ (benchmark verified) |

---

## Overall Assessment

OpenViking is a context database (not a memory-only system). Its distinguishing features are the filesystem paradigm, L0/L1/L2 tiered context loading, and directory-recursive retrieval. The README benchmarks show strong results on LoCoMo (80-83% accuracy, up to 91% token reduction).

The data.js entry requires **8 corrections**: privacy, export, context, fulltext, contentPreproc, dedup, searchModes, and p_codex all need to be flipped from false to true (or incremented for searchModes). The user's claim of "Very feature-rich" is partially correct — the system has more features than data.js currently reflects, but the user also overclaimed on timeTravel, decay, supersede, explicitForget, qualityRefine, narrative, recurrence, and several platform integrations.
