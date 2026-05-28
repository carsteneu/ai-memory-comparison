# MemLayer — Evidence

> Every ✅ claim backed by public README, documentation, or source code.
> Lines may shift; citations reference `main` for readability.
> Audited: 2026-05-28 | Stars: 275 | Created: 2025-11-16

---

## Vital Signs

### stars: 275 ✅
- GitHub: 275 stars at audit time

### language: Python ✅
- 100% Python per GitHub language stats
- `pyproject.toml` at repo root

### license: MIT ✅
- `LICENSE` file at repo root (MIT)
- `pyproject.toml`: `license = {text = "MIT"}`

### singleBinary: false
- Ships via `pip install memlayer` (PyPI package)
- Python runtime required

### created: 2025-11-16 ✅
- GitHub API: `created_at: 2025-11-16T10:57:16Z`

---

## Architecture

### deployment: "Python library" ✅
- README: `pip install memlayer`
- Library that wraps LLM providers to add memory

### storage: "ChromaDB+NetworkX" ✅
- README: "Hybrid Storage: Vector Store (ChromaDB) + Knowledge Graph (NetworkX)"
- `docs/storage/chroma.md`: ChromaDB notes, metadata types, connection handling
- `docs/storage/networkx.md`: Knowledge graph persistence, node schemas
- Lightweight mode: NetworkX only (graph-only)

### integration: "Library/SDK" ✅
- Wraps LLM providers (OpenAI, Claude, Gemini, Ollama, LMStudio)
- All share the same `chat()` API
- `update_from_text()` for direct text ingestion
- No MCP server, no hooks system, no proxy

### proxy: false
- No conversation-stream interception/proxy layer
- Library wraps providers at the API level, not stream manipulation
- CRITERIA.md: "Intercepts and modifies the LLM conversation stream in-flight" — MemLayer adds memory via tool calls, not stream interception

### webUi: false
- No web dashboard, no TUI mentioned in README, docs, or repo structure

### offline: true ✅
- LOCAL mode: "Run 100% offline!" (Ollama + local sentence-transformers)
- `docs/tuning/operation_mode.md`: Local mode — "No internet required", "Fully local"
- Core functionality (graph storage, local embeddings) works without internet

### multiAgent: false
- No inter-agent communication, coordination, or swarm features
- `user_id` isolates memory per user, not per agent
- No mention of multi-agent in README or docs

### llmFlex: 5 ✅
- OpenAI (via `from memlayer import OpenAI`)
- Claude/Anthropic (via `from memlayer import Claude`)
- Google Gemini (via `from memlayer import Gemini`)
- Ollama (via `from memlayer import Ollama`)
- LMStudio (via `from memlayer import LMStudio`)
- README: "Works with all major LLM providers"

### privacy: true ✅
- LOCAL mode: "All computation on-premises", "No external API calls"
- `docs/tuning/operation_mode.md`: "Privacy: Fully local" for local mode
- No encryption mentioned, but local mode ensures data never leaves the machine
- ONLINE mode sends embeddings to OpenAI API — privacy only in LOCAL mode

### export: false
- Graph stored as `.pkl` file (internal format), not a user-facing export
- No export/backup command or documented export format
- No import from other memory systems

### setup: "pip install" ✅
- README: `pip install memlayer`
- Available on PyPI

---

## Data Model

### unit: "Fact + Entity (graph+vec)" ✅

### entities: true ✅
- `analyze_and_extract_knowledge()` returns `entities: [{"name": "Alice", "type": "Person"}, ...]`
- `Knowledge Graph: Automatically extracts entities, relationships, and facts from conversations`
- Entity deduplication: "Entity deduplication (e.g., 'John' = 'John Smith')"
- `get_entity_subgraph()` method for entity traversal
- Entities stored as separate structured nodes in NetworkX graph

### actions: false
- No extraction or storage of commands, operations, or tool calls as structured fields
- API reference has no action-related methods or schemas

### keywords: false
- No explicit keyword/tag system for categorizing stored items
- Lightweight mode uses "keyword-based" search (text scanning), not a keyword metadata system
- Salience gate is ML-based classification, not keyword tagging

### anticipatedQueries: false
- No generation of predicted search queries for memory entries

### triggerRules: false
- Task reminders are time-based (deadline triggers), not condition-based rules
- No file-open triggers, context-based activation rules
- CRITERIA.md requires: "condition-based activation (e.g., 'show this memory when file X is opened', deadline-based triggers)" — deadline-only reminders too narrow to qualify

### domainTag: false
- No domain categorization (code, marketing, legal, finance, general)

### taskType: false
- Tasks are simple reminders with description + due_timestamp
- No classification by type (task/idea/blocked/stale)

### context: false
- No dedicated "why" field for relevance rationale alongside memory content
- Facts have importance_score but no context/rationale field

### source: false
- No structured source attribution
- Facts extracted from conversation but no tracking of who/what authored them
- CRITERIA.md requires "at least 3 distinct source levels"

### originTrust: false
- No trust weight hierarchy based on capture method
- Salience threshold controls what gets stored, but no per-source trust weights

### emotional: false
- No sentiment or emotional intensity tracking per memory or session

### conflict: false
- No contradiction detection between memories
- Entity dedup merges similar entities, but doesn't detect conflicting facts

### layeredMemory: false
- No hierarchical memory organization (L0 raw → L1 summary → L2 persona)
- Facts are stored flat in ChromaDB, entities/relationships flat in NetworkX
- No summarization or abstraction layers

### timeTravel: false
- No historical state querying or browsing
- Curation service archives/deletes items but no ability to browse past versions
- No temporal search parameters

### schemaFields: 3 ✅
Per fact (primary memory unit in ChromaDB):
1. `fact` — text content
2. `importance_score` — float, salience-based importance
3. `expiration_date` — auto-extracted from text, used by curation

Additional fields exist on separate objects (entities: name+type, relationships: subject+predicate+object, tasks: description+due_timestamp) but these are different storage types, not fields on the primary memory entry. Auto-generated IDs and timestamps excluded per CRITERIA.md.

---

## Search & Retrieval

### fulltext: true ✅
- Lightweight mode: "Keyword-based (medium accuracy)" — O(n) text scan
- `docs/tuning/operation_mode.md`: "Graph Keyword Search → NetworkX Traversal → Results"
- Qualifies as "grep or equivalent" per CRITERIA.md definition
- NOTE: Full-text search only available in lightweight mode. Online/local modes are vector-only.

### semantic: true ✅
- Online/Local modes: ChromaDB vector search with embeddings
- `docs/API_REFERENCE.md`: `search_facts()` → "Search for similar facts using vector similarity"
- Two embedding backends: OpenAI API (online) or sentence-transformers (local)
- 3 tiers: 2, 5, or 10 vector results depending on tier

### hybrid: true ✅
- Deep tier combines vector similarity + knowledge graph traversal
- README: "Hybrid Search: Combines vector similarity + knowledge graph traversal for accurate retrieval"
- Deep tier: "Graph traversal enabled (entity extraction + 1-hop relationships)"
- `docs/basics/overview.md`: "Hybrid search combines vector similarity + graph traversal"
- NOTE: This is vector+graph hybrid, not BM25+vector. CRITERIA.md says "(e.g., Reciprocal Rank Fusion)" — the definition is broader than just BM25+Vec. Two retrieval methods are combined: ChromaDB vector search + NetworkX graph traversal with result fusion. Qualifies.

### deep: false
- "Deep Tier" in MemLayer refers to graph traversal depth, NOT search of model thinking/reasoning traces
- CRITERIA.md: "Search includes model thinking/reasoning traces, not just final outputs" — not present

### codeGraph: false
- No Tree-sitter, AST, or code structure indexing

### docsSearch: false
- No dedicated documentation search across ingested framework/API docs

### factQuery: false
- No structured metadata query tool
- `search_facts()` is vector similarity search, not structured field queries
- No equivalent of `query_facts()` for "all unfinished tasks" or "all decisions about Y"

### timeline: false
- No chronological browsing, no `since`/`before` parameters
- No timeline view of memories

### searchModes: 3 ✅
Three search tiers (all via `search_service.search()` with tier parameter):
1. **Fast** (<100ms): 2 vector results, no graph traversal
2. **Balanced** (<500ms, default): 5 vector results, no graph traversal
3. **Deep** (<2s): 10 vector results + graph traversal + entity extraction

Additional retrieval methods:
- `synthesize_answer()` — memory-grounded Q&A with confidence score and sources
- Lightweight keyword search (different engine but same `search()` interface, counted as configuration variant)

Count: 3 distinct search tiers as the primary search modes.

### dataSources: 1
- Only one data type indexed: conversation memories (facts + entities + relationships)
- `update_from_text()` ingests arbitrary text into the same memory store
- No separate code, docs, or message source indices

---

## Knowledge Lifecycle

### decay: true ✅
- CurationService: "Archive low-relevance memories" using hybrid relevance scoring
- Scoring includes: vector similarity, access recency, importance score
- Archives when relevance < `archive_threshold` (~0.3)
- Deletes when current time > `expiration_date`
- `docs/services/curation.md`: "Hybrid relevance scoring (vector similarity, access recency, importance score)"
- CRITERIA.md: "Automatically reduces relevance or removes memories based on time, disuse, or engagement signals" — access recency as engagement signal + automatic archival meets this
- Runs automatically, no manual trigger needed

### supersede: false
- No explicit mechanism to mark one memory as replacing another with traceable chain
- Facts can be archived/deleted by curation but no supersede/replacement chain
- No version history for individual facts

### contradiction: false
- No automatic contradiction detection between memories
- Entity dedup merges similar entities but doesn't detect conflicting facts

### quarantine: false
- No session-level quarantine from retrieval
- Memories can be archived/deleted individually by curation, but no bulk session exclusion

### autoResolve: false
- Curation auto-deletes expired facts (expiration_date check) and auto-archives low-relevance items
- However, no TTL-based resolution of stale tasks or unfinished items
- CRITERIA.md specifically references "unfinished tasks after a TTL" — task system lacks auto-resolution
- The expiration_date cleanup is a basic lifecycle, not the task-resolution pattern described in criteria

### trustModel: false
- No multi-tier trust hierarchy
- Salience threshold applies uniformly regardless of source

### explicitForget: false
- No documented delete/forget/remove method in the API reference
- Curation service handles archiving/deletion automatically, but no user-facing forget command
- No mention of explicit memory deletion in README or Quick Start

---

## Extraction Pipeline

### autoExtract: true ✅
- "After each conversation, background threads: Extract facts, entities, and relationships using LLM"
- Consolidation service runs asynchronously after each chat turn
- `docs/basics/overview.md`: "Knowledge Extraction: After each conversation turn... facts, entities, and relationships are extracted"
- `update_from_text()` for programmatic ingestion
- No manual `save` calls required

### contentPreproc: false
- No content-type-aware truncation or filtering
- Salience gate filters by importance, not by content type

### dedup: true ✅
- `docs/basics/overview.md`: "Entity deduplication (e.g., 'John' = 'John Smith')"
- Knowledge graph with entity deduplication during extraction
- Entities with same name are merged

### qualityRefine: false
- No explicit second-pass quality refinement
- Salience gate is single-pass filtering by importance
- No confidence scoring or contradiction checking pass

### narrative: false
- No session summaries, handover narratives, or project profiles
- Facts are stored individually, no aggregate narrative generation

### clustering: false
- No topic or embedding-based clustering of related memories

### recurrence: false
- No recurrence/pattern detection across sessions

### persona: false
- No persistent persona trait extraction
- Memory is per-user (user_id) but no persona model derived from conversations

---

## Platform Support

MemLayer is a Python library that wraps LLM providers to add memory. It does NOT integrate with coding agent platforms (Claude Code, Codex, Cursor, etc.). Per CRITERIA.md, platform support requires "Documented integration with [platform] (MCP, hooks, plugin, or skill)." MemLayer has none of these.

### p_claude: false
- MemLayer wraps Claude models as an LLM provider, not Claude Code integration
- No MCP server, no hooks, no skill for Claude Code

### p_codex: false
### p_opencode: false
### p_gemini: false — wraps Gemini models, not Gemini CLI
### p_copilot: false
### p_cursor: false
### p_windsurf: false
### p_openclaw: false
### p_hermes: false
### p_pi: false
### p_antigravity: false

---

## Benchmarks

All benchmarks: `—` — no published benchmark scores.

### b_locomo: "—"
### b_longmemeval: "—"
### b_personamem: "—"
### b_token: "—"
### b_methodology: false

No benchmark methodology, no published scores, no comparison to baselines.

---

## Absent Features (Verified)

The following features from the data model are confirmed as genuinely absent:

| Feature | Evidence of Absence |
|---|---|
| singleBinary | Ships as pip package, requires Python runtime |
| proxy | Library wraps providers; no stream interception |
| webUi | No dashboard/TUI in repo or docs |
| multiAgent | No agent communication; user_id-based isolation only |
| actions | No structured commands/operations field |
| keywords | No tag/keyword metadata system |
| anticipatedQueries | No predicted query generation |
| triggerRules | Time-based tasks only, no condition rules |
| domainTag | No domain categorization |
| taskType | No task/idea/blocked/stale classification |
| context | No "why" field for relevance rationale |
| source | No structured source attribution |
| originTrust | No trust weight hierarchy |
| emotional | No sentiment tracking |
| conflict | No contradiction detection |
| layeredMemory | Flat storage, no hierarchical layers |
| timeTravel | No historical state browsing |
| deep (search) | No model thinking trace search |
| codeGraph | No AST/code structure indexing |
| docsSearch | No docs search |
| factQuery | No structured metadata queries |
| timeline | No chronological browsing |
| supersede | No memory replacement chain |
| contradiction | No automatic conflict detection |
| quarantine | No session exclusion |
| autoResolve | No TTL task resolution |
| trustModel | No trust hierarchy |
| explicitForget | No user-facing delete command |
| qualityRefine | Single-pass extraction only |
| narrative | No session summaries or profiles |
| clustering | No topic clustering |
| recurrence | No pattern detection |
| persona | No trait extraction |
| contentPreproc | No content-type-aware filtering |
| export | No data export functionality |
| cacheOpt | No result caching optimization |

All platform support (p_claude through p_antigravity): MemLayer wraps LLM providers, not coding agent platforms.

All benchmarks: No published scores.

---

## Summary

MemLayer is a well-designed LLM memory library focused on ease of integration (3 lines of code). Its strengths are:

- **Provider flexibility**: 5 LLM providers with identical API
- **Architecture flexibility**: 3 operation modes (online/local/lightweight) for different deployment needs
- **Hybrid storage**: Vector (ChromaDB) + Graph (NetworkX) with automatic consolidation
- **Offline capable**: LOCAL mode runs 100% locally with no API calls
- **Auto-extraction**: Fully automatic knowledge extraction with entity dedup
- **Decay**: Curation service with relevance scoring and automatic archival

Its primary limitation is scope: it's a Python library for adding memory to LLM conversations, not an agent memory platform. No MCP server, no coding-agent integrations, no code graph, no benchmarks.

**Coverage calculation**: 14 of 70 Boolean features present = **20%**
