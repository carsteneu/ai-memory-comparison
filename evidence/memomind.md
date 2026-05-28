# MemoMind — Evidence

> Every ✅ claim backed by public README.
> Audit date: 2026-05-28. Source: GitHub `24kchengYe/MemoMind` master branch README.
> **URL Correction:** User-provided `https://github.com/progga004/memomind` returns 404. Correct repository: `https://github.com/24kchengYe/MemoMind` (716 stars, MIT, Python).

---

## Architecture

### Deployment ✅
- `README.md` — Two options: Windows Native (Python venv + PostgreSQL 17 portable + pgvector) and WSL2/Linux (bash install.sh + systemd). MCP stdio transport. Auto-start via Windows Task Scheduler or systemd.

### Storage ✅
- `README.md` — "PostgreSQL + pgvector." Persistent relational + vector storage.

### Offline ✅
- `README.md` — "100% local — PostgreSQL + embedding models on your machine, nothing leaves it." "Privacy: 100% local" in comparison table. GPU-accelerated embeddings run locally via CUDA. LLM API calls for retain only (configurable), not required for operation.
- `README.md` — Comparison table: "Privacy: 100% local" vs Mem0 "Cloud default."

### Web UI / TUI ✅ (user claims absent — **CORRECTION**)
- `README.md` — "Web Dashboard — browse and search all memories visually at `http://127.0.0.1:9999`." Screenshots show: Dashboard overview, Knowledge Graph, Timeline View, Type Filters, Add Memory modal. "Dual search mode — toggle between fast keyword search and semantic recall in the dashboard."
- **Finding**: Web dashboard with full CRUD, search, graph visualization, timeline. This is a full web UI.

---

## Data Model

### Data model claims

**Unit:** Memory node (text + metadata). Four types: World, Experience, Observation, Mental Model.

### Context/why ⚠️ PARTIAL (user claims present)
- `README.md` — Export JSON shows `source_memory_ids` for provenance tracing. Fact types (World/Experience/Observation/Mental Model) describe memory KIND, not WHY it was saved. No dedicated "why this memory matters" or "context this applies to" field.
- **Finding**: Source tracing exists but no structured "context/why" field. Mark as **PARTIAL** — source provenance ≠ context rationale.

### Layered memory ⚠️ PARTIAL (user claims present)
- `README.md` — Four memory types: World, Experience, Observation, Mental Model. These are **type categories**, not hierarchical layers (no L0→L1→L2→L3 structure). No explicit hierarchy or nesting.
- `README.md` — "Memory Evolution" and "Consolidation engine" describe merging/flattening observations, not preserving layers.
- **Finding**: Category types exist but no hierarchical layering. Mark as **PARTIAL**.

### Time-travel ✅
- `README.md` — Dashboard "Timeline View" shows memories organized by date. "4-way hybrid retrieval — ... + temporal search." Export includes history array. "Memory export (JSON backup)."
- `README.md` — Production stats: "Time span: 2017 – present (9 years)."

### Entities ✅ (user claims absent — **CORRECTION**)
- `README.md` — Production stats: "Named entities: 4,600+." Comparison table: Knowledge Graph is "Built-in." Export JSON includes `"entities"` array field.
- **Finding**: Entities are extracted and stored as a structured field.

### Keywords/tags ✅ (user claims absent — **CORRECTION**)
- `README.md` — v1.8 changelog: "Unified card template v2 — Language, Category, **Keywords**, Summary fields."
- `README.md` — Export JSON includes `"tags"` array field. Dashboard filter by tag/type.

### Source attribution ⚠️ PARTIAL (user claims absent)
- `README.md` — "Original Conversation Tracing — click 💬 on any memory card to view the full original conversation." Export includes `source_memory_ids`. But CRITERIA.md requires "at least 3 distinct source levels" (user, agent, pipeline). MemoMind traces back to imported conversations but doesn't classify by author/source type.
- **Finding**: Has source tracing but not multi-tier source attribution (3+ levels). Mark as **PARTIAL**.

### Schema fields — 6 ✅
- `README.md` — Export JSON format: `text`, `entities`, `tags`, `date`, `fact_type`, `source_memory_ids` = 6 distinct structured fields. Additional v1.8 fields (Language, Category, Keywords, Summary) on card template not yet in base export.

### Actions, anticipatedQueries, triggerRules, domainTag, taskType, originTrust, emotional, conflict — all absent ✅
- No evidence for any of these in README, export format, or feature list.

---

## Search & Retrieval

### Full-text (BM25) ✅
- `README.md` — "BM25 keyword" as part of 4-way hybrid retrieval. "Keyword search 20–33ms." "Dual search mode — toggle between fast keyword search and semantic recall."

### Semantic/vector ✅
- `README.md` — "bge-m3 (1024-dim), 50ms/item on consumer GPU." "Semantic recall 235–430ms." "4-way hybrid retrieval — semantic similarity + ..."

### Hybrid (BM25+Vec) ✅ (user claims absent — **CORRECTION**)
- `README.md` — "4-way hybrid retrieval — semantic similarity + BM25 keyword + knowledge graph + temporal search." Comparison table: "Retrieval: 4-way hybrid."
- **Finding**: This is explicitly hybrid search combining BM25 + vector + graph + temporal signals.

### Timeline view ✅
- `README.md` — Dashboard "Timeline View" screenshot. "Infinite scroll — lazy-loads memory cards and timeline." "Temporal search."

### Search modes — 2 ✅
- `README.md` — "Dual search mode — toggle between fast keyword search and semantic recall in the dashboard." Two distinct user-facing modes. The "4-way hybrid" is the combined retrieval architecture, not a separate user mode.

### Data sources — 3+ (user claims 2 — **UNDERCOUNT** ✅→🔺)
- `README.md` — Three distinct data sources: (1) AI conversations imported (ChatGPT + Gemini, 541 chats), (2) DayLife activities (5,500+ events), (3) NoteDiscovery Knowledge Vault documents (13,400+). Full-disk scanning for additional documents.
- **Finding**: At least 3 data sources, not 2.

### Deep, codeGraph, docsSearch, factQuery — all absent ✅
- No code graph, no docs search (document ingestion ≠ framework/API docs search), no deep/thinking search, no metadata query tool.

---

## Knowledge Lifecycle

### Supersede/replace ✅
- `README.md` — "Memory Evolution Through Consolidation — The consolidation engine automatically merges, updates, and refines observations as new facts arrive." Evolution diagram shows observation → refinement → consolidation pipeline.
- `README.md` — "Split LLM — fast cheap model for fact extraction, stronger model for consolidation (better observation merging)."

### Decay/forgetting ⚠️ PARTIAL (user claims present)
- `README.md` — v1.4 changelog: "Observation pruning (auto-cleanup stale observations weekly)" — automatic but observation-only.
- `README.md` — Roadmap: "Memory decay and archival (time-weighted relevance)" — NOT implemented (unchecked).
- **Finding**: Observation-level auto-pruning exists, but full time-weighted decay across all memory types is still in roadmap.

### Explicit forget ✅
- `README.md` — Dashboard demos show "Delete" on memory cards. REST API allows memory deletion.

### Contradiction detect, quarantine, autoResolve, trustModel — all absent ✅
- "Memory conflict detection and resolution" is in roadmap (unchecked). No quarantine, no auto-resolve, no trust model.

---

## Extraction Pipeline

### Auto-extraction ✅
- `README.md` — "Zero manual effort — AI autonomously decides what to remember and recall." `retain` operation: "Extract facts from conversation, store in vector DB." "After learning something new about you" → auto-triggered.

### Deduplication ✅
- `README.md` — Consolidation engine merges observations: "Observations don't just accumulate — they evolve. The consolidation engine automatically merges, updates, and refines observations as new facts arrive." This effectively deduplicates by merging related observations.

### Quality refinement ✅ (user claims absent — **CORRECTION**)
- `README.md` — "Split LLM — fast cheap model for fact extraction, stronger model for consolidation (better observation merging)." This is LLM-based quality refinement: a second, stronger model processes observations after initial extraction to improve merging quality.
- **Finding**: Two-pass LLM pipeline (extraction → consolidation/refinement). Meets CRITERIA.md definition of LLM-based quality pass after initial extraction.

### Clustering ❌ (user claims present — **CORRECTION**)
- `README.md` — Knowledge graph with entity linking and relationships. But CRITERIA.md defines clustering as "Groups related memories by topic, embedding similarity, or semantic relationship." Graph edge creation ≠ clustering. No evidence of topic-based clustering or embedding-based grouping of memories.
- **Finding**: Graph relationships exist but no explicit clustering of memories by topic/similarity.

### ContentPreproc, narrative, recurrence, persona — all absent ✅
- No content-type-aware truncation. "Reflect" synthesizes insights but doesn't generate session handover narratives. No recurrence detection. No persona extraction engine.

---

## Platform Support

### Claude Code ✅
- `README.md` — "MCP (stdio)" integration. `claude mcp add --scope user --transport stdio memomind ...` command documented. Core integration path.

### OpenCode ❌ (user claims present — **CORRECTION**)
- `README.md` — Roadmap: "Support for more MCP clients (Cursor, Windsurf, etc.)" — unchecked. No OpenCode mention in README, no OpenCode-specific integration docs.

### Cursor ❌ (user claims present — **CORRECTION**)
- `README.md` — Roadmap only. Not implemented.

### Windsurf ❌ (user claims present — **CORRECTION**)
- `README.md` — Roadmap only. Not implemented.

### Codex, Gemini CLI, Copilot, OpenClaw, Hermes, pi/omp, Antigravity — all absent ✅
- No evidence for any of these platforms.

---

## Benchmarks

### LoCoMo, LongMemEval, PersonaMem, Token reduction — all absent ✅
- Comparison table shows LongMemEval as "—" (not tested). No other benchmark scores published.

---

## Corrections Summary

### URL Correction
- **Provided**: `https://github.com/progga004/memomind` → **404 Not Found**
- **Correct**: `https://github.com/24kchengYe/MemoMind` (716 stars, MIT, Python)

### User claims PRESENT but verified DIFFERENTLY:

| Feature | User Claim | Verified |
|---------|-----------|----------|
| `webUi` | absent | **PRESENT** — Web Dashboard at localhost:9999 |
| `hybrid` | absent | **PRESENT** — "4-way hybrid retrieval" |
| `entities` | absent | **PRESENT** — 4,600+ named entities in production |
| `keywords` | absent | **PRESENT** — v1.8 Keywords field on card template |
| `qualityRefine` | absent | **PRESENT** — Two-pass LLM (extract + consolidate) |
| `clustering` | present | **ABSENT** — Graph linking ≠ topic clustering |
| `layeredMemory` | present | **PARTIAL** — Memory types exist but no L0→L3 hierarchy |
| `decay` | present | **PARTIAL** — Observation pruning only, full decay in roadmap |
| `context` | present | **PARTIAL** — Source tracing exists, no "why this matters" field |
| `p_opencode` | present | **ABSENT** — Roadmap only |
| `p_cursor` | present | **ABSENT** — Roadmap only |
| `p_windsurf` | present | **ABSENT** — Roadmap only |
| `dataSources` | 2 | **UNDERCOUNT** — At least 3 (AI chats, DayLife, Vault) |
| `supersede` | present | ✅ — Consolidation engine merges observations |
| `dedup` | present | ✅ — Merging observations = dedup in practice |

### Legend
- **PRESENT** / **ABSENT**: Clear binary determination from README
- **PARTIAL**: Feature partially exists but doesn't fully meet CRITERIA.md definition
- **UNDERCOUNT**: Count is higher than claimed

---

## Audit Notes

1. **Repo location**: User-provided URL is incorrect. The project is at `github.com/24kchengYe/MemoMind`, not `github.com/progga004/memomind`. Both the owner and the repo name differ.

2. **Web UI is a significant omission from "absent" claims**: The README shows extensive dashboard screenshots (memory stream, knowledge graph, timeline, filters, add-memory modal). This is a full-featured web UI. Should be marked ✅.

3. **Hybrid search is explicitly advertised**: "4-way hybrid retrieval" is a core feature. Should be marked ✅.

4. **Entities and keywords are production features**: 4,600+ named entities in the author's production instance. v1.8 added explicit Keywords field. Should be marked ✅ for both.

5. **Quality refinement via two-pass LLM**: The split-LLM architecture (cheap model for extraction, stronger model for consolidation) is a clear quality refinement pass. Should be marked ✅.

6. **Memory types vs layered memory**: The four memory types are a classification system, not a hierarchical L0→L3 layered architecture. The user's claim of `layeredMemory=true` overstates the feature. Recommend marking as partial or absent.

7. **Platform support overclaimed**: Only Claude Code is implemented. OpenCode, Cursor, and Windsurf are roadmap items ("Support for more MCP clients"). Should all be marked ❌.

8. **Decay is observation-level only**: Auto-pruning of stale observations exists (v1.4), but full time-weighted memory decay is in the roadmap. The user's claim is only partially correct.

9. **Data sources undercount**: At minimum 3 sources (AI chats, DayLife, NoteDiscovery Vault), not 2. Full-disk scanning adds more.

10. **Clustering overclaimed**: Knowledge graph entity linking is not topic/embedding-based clustering. No clustering feature exists. Should be marked ❌.
