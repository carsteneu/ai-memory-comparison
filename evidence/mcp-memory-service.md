# mcp-memory-service — Audit Evidence

**Audit date:** 2026-05-28  
**Repo:** https://github.com/doobidoo/mcp-memory-service  
**Version:** v10.68.0 (May 28, 2026)  
**Author:** Heinrich Krupp (doobidoo)  
**Stars:** 1,901 (GitHub API, ~1.9k)  
**Language:** Python 3.10+  
**License:** Apache 2.0  
**Created:** 2024-12-26 (GitHub API)  
**Forks:** 296  
**Commits:** 2,780  
**Docs:** README.md, docs/ directory, GitHub Wiki, YouTube demos  

---

## Architecture

### Deployment
Local-first server with four storage backend options:
- **sqlite-vec**: Default, local-only, WAL mode for concurrent access
- **cloudflare**: Cloudflare Workers (Vectorize + D1 + R2), multi-device sync
- **hybrid**: SQLite-vec primary + Cloudflare background sync
- **milvus**: Milvus Lite (file), self-hosted Milvus, or Zilliz Cloud

Docker support: `doobidoo/mcp-memory-service:quality-cpu` image with pre-exported ONNX models.

**Evidence:** `server_impl.py` lines showing conditional backend initialization for all four backends; `pyproject.toml` `[project.optional-dependencies]` listing `milvus` extras.

### Storage
- SQLite-vec with vec0 virtual table (cosine distance), FTS5 trigram for BM25
- Cloudflare D1 (metadata), Vectorize (embeddings), R2 (large content)
- Milvus (Lite file / self-hosted server / Zilliz Cloud)
- WAL mode for concurrent access, indexes on content_hash, created_at, memory_type, deleted_at

**Evidence:** `sqlite_vec.py` `_create_virtual_table_and_indexes()` function with CREATE TABLE memories (11 columns + FTS5 + vec0).

### Integration
Three transport layers:
1. **MCP protocol** (stdio/SSE/Streamable HTTP) — native `mcp>=1.8.0` dependency
2. **REST API** — 76 FastAPI endpoints on port 8000
3. **OAuth 2.0 + DCR** — enterprise-ready with PEM key support, IDE redirect URIs

**Evidence:** `server_impl.py` imports `mcp.types`, `NotificationOptions`, `Server`; `pyproject.toml` deps include `fastapi`, `mcp>=1.8.0,<2.0.0`, `authlib`, `PyJWT[crypto]`; README "Remote MCP" section.

### Web Dashboard
8-tab web UI (Dashboard, Search, Browse, Documents, Manage, Analytics, Quality, API Docs). Interactive D3.js knowledge graph visualization. GIF tour linked in README.

**Evidence:** README screenshot and linked wiki GIF at `images/dashboard/mcp-memory-dashboard-v9.3.0-tour.gif`.

### Multi-Agent
- `X-Agent-ID` header auto-tags memories (`agent:<id>`)
- Tag namespaces: `agent:`, `crew:`, `proj:`, `sys:`, `q:`, `topic:`, `t:`, `user:`
- Real-world 5-agent cluster use case (issue #591): tags as inter-agent messaging bus
- `conversation_id` for incremental conversation storage, bypassing dedup

**Evidence:** README "Real-World: Multi-Agent Cluster with Shared Memory" section with code example.

### LLM Providers
- ONNX local embeddings (`all-MiniLM-L6-v2`, `ms-marco-MiniLM-L-6-v2`)
- SentenceTransformer fallback
- External embedding API (vLLM, Ollama, OpenAI-compatible) via `MCP_EXTERNAL_EMBEDDING_URL`
- Quality scoring: ONNX, any OpenAI-compatible endpoint (`MCP_QUALITY_AI_PROVIDER=openai-compatible`)
- Pure-Python hash fallback for environments without native DLLs (WinError 1114)

**Evidence:** `sqlite_vec.py` `_initialize_embedding_model()` showing ONNX → SentenceTransformer → hash fallback chain; `pyproject.toml` deps include `sentence-transformers`, `torch`, `onnxruntime`.

### Cache Optimization
- Module-level `_MODEL_CACHE`, `_DIMENSION_CACHE`, `_EMBEDDING_CACHE` for embedding models
- Storage instance cache (`_STORAGE_CACHE`) with cache key by backend+path
- MemoryService cache (`_MEMORY_SERVICE_CACHE`) keyed by storage ID

**Evidence:** `sqlite_vec.py` module-level caches; `server_impl.py` global `_STORAGE_CACHE`/`_MEMORY_SERVICE_CACHE` with `_get_cache_lock()`.

### Privacy / Encryption
- Local-first: embeddings computed via ONNX, memory never leaves infrastructure
- `MCP_ALLOW_ANONYMOUS_ACCESS` for trusted networks
- OAuth 2.0 authentication for remote access
- No external API calls required for core functionality

**Evidence:** README "Why Agents Need This" comparison table: "100% local", "Embeddings run locally via ONNX — memory never leaves your infrastructure".

### Data Export
SHODH Unified Memory API Specification v1.0.0 compatibility enables export/import across implementations (shodh-memory, shodh-cloudflare). Full fidelity preservation of emotional_valence, episode_id, and all spec fields.

**Evidence:** README "SHODH Ecosystem Compatibility" section.

### Setup
`pip install mcp-memory-service` (PyPI), or `git clone` + `python scripts/installation/install.py` for backend selection.

### Pricing
Free, open source (Apache 2.0). No paid tiers. Docker images on Docker Hub.

---

## Data Model

### Core Schema (memories table)
```sql
CREATE TABLE memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_hash TEXT UNIQUE NOT NULL,
    content TEXT NOT NULL,
    tags TEXT,                   -- comma-separated
    memory_type TEXT,
    metadata TEXT,               -- JSON blob
    created_at REAL,
    updated_at REAL,
    created_at_iso TEXT,
    updated_at_iso TEXT,
    deleted_at REAL DEFAULT NULL
);
```

### Vector Table
```sql
CREATE VIRTUAL TABLE memory_embeddings USING vec0(
    content_embedding FLOAT[384] distance_metric=cosine
);
```

### FTS5 Table (BM25)
```sql
CREATE VIRTUAL TABLE memory_content_fts USING fts5(
    content, content='memories', content_rowid='id', tokenize='trigram'
);
```

### Knowledge Graph Table
`memory_graph` table (migration 008) with: source_id, target_id, relationship_type, weight, valid_from, valid_until.

### SHODH Metadata Fields (in metadata JSON)
- `quality_score` (float 0.0-1.0)
- `quality_provider` (string)
- `access_count` (int)
- `last_accessed_at` (float Unix timestamp)
- `source_type` (user/system/api/file/web/ai_generated/inferred)
- `credibility` (float 0.0-1.0)
- `emotion` (string: joy/frustration/surprise/relief)
- `emotional_valence` (float -1.0 to 1.0)
- `emotional_arousal` (float 0.0 to 1.0)
- `episode_id` (string)
- `sequence_number` (int)
- `preceding_memory_id` (string)
- `conversation_id` (string)

### Memory Type Ontology
12 base types (observation, decision, learning, error, pattern, planning, ceremony, milestone, stakeholder, meeting, research, communication) with 63+ subtypes, plus custom types via `MCP_CUSTOM_MEMORY_TYPES` env var.

### Relationship Types
7 typed edges: causes, fixes, contradicts, supports, follows, related, shares_entity. Symmetric: related, contradicts, shares_entity. Asymmetric: causes, fixes, supports, follows.

**Schema fields count:** ~28-30 distinct persisted fields across memories (11), embeddings (1), graph (6), and metadata sub-fields (12+).

### Data Model Features

| Feature | Present | Evidence |
|---------|---------|----------|
| entities | ✅ | `EntityExtractor` in `reasoning/entities.py`, `EntityLinker` for shares_entity edges, auto-linked @mentions, #tags, URLs, file paths |
| actions | ❌ | No action/operation tracking in schema |
| keywords/tags | ✅ | Comma-separated tags with namespaced taxonomies (agent:, crew:, proj:, sys:, q:, topic:, t:, user:), tag match AND/OR |
| anticipated queries | ❌ | Not in schema |
| trigger rules | ❌ | No trigger/condition system |
| domain tag | ✅ | Tag namespaces provide domain segmentation |
| task type | ✅ | `memory_type` field with 12 base types + 63+ subtypes (formal ontology) |
| context (why) | ✅ | `conversation_id`, episode metadata, `context_signature` in mistake notes |
| source attribution | ✅ | `source_type` SHODH field, `X-Agent-ID` header, `client_hostname` auto-tagging |
| origin + trust | ⚠️ partial | `credibility` field (0.0-1.0) but no formal trust model with provenance chains |
| emotional | ✅ | SHODH fields: `emotion`, `emotional_valence`, `emotional_arousal` |
| conflict surfacing | ✅ | NLI contradiction detection (v10.67.0), `contradiction_action()` for fact mutability (v10.68.0) |
| layered memory | ❌ | Memory types form a taxonomy but no L0/L1/L2 structural layering |
| time-travel | ✅ | Temporal edges with `valid_from`/`valid_until` (v10.68.0), `created_at`/`updated_at` timestamps, time-filtered queries |
| schema fields | **~28** | 11 table columns + 12+ metadata sub-fields + 6 graph columns |

---

## Search & Retrieval

### Search Modes
| Mode | Evidence |
|------|----------|
| 1. Semantic/vector | `storage.retrieve()` — sqlite-vec KNN over embeddings |
| 2. Full-text (BM25) | FTS5 trigram via `memory_content_fts` virtual table |
| 3. Hybrid (BM25+Vec) | Combined search mentioned in comparison table + RRF fusion (v10.68.0) |
| 4. Tag search | `search_by_tag()` with AND/OR matching |
| 5. Temporal-filtered | Time-based queries via `created_at`/`updated_at`/`valid_from`/`valid_until` |
| 6. RRF multi-strategy | `asyncio.gather` concurrent semantic+tag with Reciprocal Rank Fusion (v10.68.0) |
| 7. Mistake note search | Semantic search scoped to `memory_type=mistake` |

**Total search modes:** **7**

### Data Sources
1. REST API (POST/GET /api/memories)
2. MCP tools (stdio/SSE/Streamable HTTP)
3. Web dashboard document upload (8-tab UI)
4. CLI transcript harvest (Claude Code, OpenCode, Codex CLI, Kiro CLI session parsing)
5. File ingestion (PDF, text, JSON, CSV) via `ingestion/` module
6. Agent auto-capture (hooks, plugins)

**Total data sources:** **6**

### Search Features

| Feature | Present | Evidence |
|---------|---------|----------|
| full-text | ✅ | FTS5 trigram table with synced triggers |
| semantic/vector | ✅ | sqlite-vec cosine distance, ONNX embeddings |
| hybrid | ✅ | BM25 + vector combined; RRF fusion (v10.68.0) |
| deep (thinking) | ❌ | No search over agent planning/thinking traces |
| code graph | ❌ | No code symbol graph or AST integration |
| docs search | ❌ | No indexed documentation search |
| fact metadata query | ✅ | Tag-based, type-based, metadata queries, timestamp filtering |
| timeline view | ✅ | Temporal edges, time-filtered queries, SSE Last-Event-ID replay |

---

## Knowledge Lifecycle

| Feature | Present | Evidence |
|---------|---------|----------|
| decay/forgetting | ✅ | Consolidation with `time_horizon`, DreamInspiredConsolidator, consolidation scheduler |
| supersede/replace | ✅ | `evolve_memory` with lineage tracking (memory evolution P1, v10.30.0+), `superseded_by` field |
| contradiction detection | ✅ | NLI contradiction detection (v10.67.0, RFC #732 Phase 3), `contradiction_action()` (v10.68.0) |
| quarantine | ❌ | No quarantine feature; only soft-delete via `deleted_at` |
| auto-resolution | ✅ | Auto consolidation compresses old memories; `contradiction_action()` handles conflicts automatically |
| trust model | ⚠️ partial | `credibility` field (0.0-1.0), `source_type`, `quality_score`; but no formal trust propagation or provenance chains |
| explicit forget | ✅ | DELETE /api/memories, soft-delete with `deleted_at` column, `purge_deleted()` in Milvus backend |

---

## Extraction Pipeline

| Feature | Present | Evidence |
|---------|---------|----------|
| auto-extraction | ✅ | Entity extraction (@mentions, #tags, URLs, file paths → entity graph), auto-tagging via `X-Agent-ID`, memory_type validation |
| content-aware preproc | ✅ | Content chunking/splitting (auto-split when exceeding max_length), boundary preservation, overlap |
| deduplication | ✅ | Semantic dedup via `semantic_dedup_threshold` (default 0.85), exact hash dedup always active, `conversation_id` bypass |
| quality refinement | ✅ | Multi-backend quality scoring: ONNX (ms-marco-MiniLM-L-6-v2 + nvidia-quality-classifier-deberta), OpenAI-compatible (Ollama, LiteLLM, vLLM), implicit signal fallback |
| narrative generation | ✅ | Insight cards: consolidation detects patterns, trends, knowledge gaps → structured insights |
| clustering | ✅ | Entity grouping, insight type auto-classification, association confidence threshold |
| recurrence detection | ✅ | Consolidation pattern detection, mistake note failure_count tracking, temporal proximity (7-day window) |
| persona extraction | ❌ | Not documented as a feature; SHODH emotional metadata exists but no persona profiling engine |

---

## Platform Support

| Platform | Present | Evidence |
|----------|---------|----------|
| Claude Code | ✅ | `claude mcp add memory -- memory server`, `.claude-plugin/` directory |
| Claude Desktop | ✅ | Config JSON example in README |
| claude.ai (Browser) | ✅ | Remote MCP via Streamable HTTP + OAuth 2.0 + Cloudflare Tunnel |
| Codex CLI | ✅ | Listed in README "CLI & Terminal AI" section, `codex_commands/` directory |
| OpenCode | ✅ | `opencode/memory-plugin.js`, `/memory` slash command, TUI toasts, Solid TUI sidebar widget |
| Gemini CLI | ✅ | Listed in README; Gemini Code Assist also listed |
| Copilot CLI | ✅ | Listed in README "CLI & Terminal AI" section |
| Cursor | ✅ | Listed in README; OAuth IDE redirect URIs (cursor://) supported (v10.59.1) |
| Windsurf | ✅ | Listed in README "Desktop & IDE" section |
| VS Code | ✅ | Listed in README "Desktop & IDE" section |
| OpenClaw | ✅ | Multi-agent cluster use case (issue #591), listed under Agent Frameworks |
| JetBrains | ✅ | Listed in README "Desktop & IDE" section |
| Goose | ✅ | Listed in README "CLI & Terminal AI" section |
| Aider | ✅ | Listed in README "CLI & Terminal AI" section |
| Continue | ✅ | Listed in README "CLI & Terminal AI" section |
| Zed | ✅ | Listed in README "Desktop & IDE" section |
| Cody | ✅ | Listed in README "Desktop & IDE" section |
| Raycast | ✅ | Listed in README "Desktop & IDE" section |
| Replit | ✅ | Listed in README "Desktop & IDE" section |
| Sourcegraph | ✅ | Listed in README "Desktop & IDE" section |
| Qodo | ✅ | Listed in README "Desktop & IDE" section |
| ChatGPT | ✅ | Developer Mode MCP support (README discussion #377) |
| LangGraph | ✅ | REST API integration guide at `docs/agents/langgraph.md` |
| CrewAI | ✅ | REST API integration guide at `docs/agents/crewai.md` |
| AutoGen | ✅ | REST API integration guide at `docs/agents/autogen.md` |
| Amp | ✅ | Listed in README "CLI & Terminal AI" section |
| Kilo Code | ✅ | Listed in README "Desktop & IDE" section |
| Hermes | ❌ | Not listed |
| pi/omp | ❌ | Not listed |
| Antigravity | ❌ | Not listed |

**Confirmed platforms for data.js:**
- p_claude: true
- p_codex: true
- p_opencode: true
- p_gemini: true
- p_copilot: true
- p_cursor: true
- p_windsurf: true
- p_openclaw: true
- p_hermes: false
- p_pi: false
- p_antigravity: false

---

## Benchmarks

| Benchmark | Value | Evidence |
|-----------|-------|----------|
| LoCoMo | — | No published LoCoMo score |
| LongMemEval | 86.0% (session) / 80.4% (turn) R@5 | Self-reported in README comparison with MemPalace; session-level via `memory_store_session` (v10.35.0), turn-level default |
| PersonaMem | — | No published score |
| Token reduction | — | No published score |
| Methodology open | ✅ | Methodology described transparently in README comparison section, including breakdown by session vs. turn-level storage |

---

## Additional Features (Not in Comparison Matrix)

- **SSE Events**: Real-time notifications when agents store/delete memories; `Last-Event-ID` replay on reconnect
- **Knowledge Graph**: D3.js interactive visualization, 7 typed relationship edges, symmetry handling, entity linking
- **Fact Mutability**: Classification into stable/volatile/ephemeral categories with `contradiction_action()` (v10.68.0)
- **Temporal Edges**: `valid_from`/`valid_until` for point-in-time graph queries (v10.68.0)
- **RRF Fusion**: Multi-strategy retrieval with Reciprocal Rank Fusion, concurrent `asyncio.gather` execution (v10.68.0)
- **NLI Contradiction Detection**: RFC #732 Phase 3, optional ONNX-based NLI model (v10.67.0)
- **Transitive Closure + Abductive Inference**: Knowledge graph reasoning (v10.66.0)
- **Integrity Monitoring**: Database health checks at startup + periodic monitoring for SQLite backends
- **Mistake Notes**: Error pattern recording with failure_count tracking, semantic dedup
- **Plugin System**: `PluginRegistry` with `on_store`, `on_retrieve`, `on_delete` hooks; smart-tagger plugin example
- **CLI Lifecycle Commands**: `memory launch`, `memory info`, `memory health`, `memory logs`, `memory stop`
- **Content Chunking**: Auto-split with boundary preservation and overlap for large content
- **Harvest System**: Multi-CLI session directory parsing (Claude Code, OpenCode, Codex CLI, Kiro CLI)
- **SHODH Interop**: Full SHODH Unified Memory API v1.0.0 compatibility for cross-implementation portability
- **Docker Quality-CPU Image**: Pre-exported ONNX models, no PyTorch at deploy time
- **OAuth 2.0 + DCR**: Dynamic Client Registration, PEM key files, IDE redirect URI schemes, offline_access support

---

## Summary for data.js

```javascript
{
  id: "mcp-memory-service",
  name: "mcp-memory-service",
  url: "https://github.com/doobidoo/mcp-memory-service",
  evidence: "evidence/mcp-memory-service.md",
  description: "Persistent memory for AI agent pipelines, REST API + MCP + knowledge graph + auto-consolidation",
  stars: 1901, language: "Python", license: "Apache 2.0", singleBinary: false, created: "2024-12-26",
  docs: "https://github.com/doobidoo/mcp-memory-service#readme",

  // Architecture
  deployment: "Local/Docker/Cloudflare/Milvus",
  storage: "SQLite-vec+Cloudflare(D1+R2+Vec)+Milvus",
  integration: "REST(76ep)+MCP+OAuth2+CLI",
  proxy: false, webUi: true, offline: true, multiAgent: true,
  llmFlex: 5, cacheOpt: true, privacy: true, export: true,
  setup: "pip install", pricing: "free",

  // Data Model
  unit: "Memory (text+metadata)",
  entities: true, actions: false, keywords: true,
  anticipatedQueries: false, triggerRules: false, domainTag: true,
  taskType: true, context: true, source: true,
  originTrust: false, emotional: true, conflict: true,
  layeredMemory: false, timeTravel: true, schemaFields: 28,

  // Search: modes=7, sources=6
  fulltext: true, semantic: true, hybrid: true, deep: false,
  codeGraph: false, docsSearch: false, factQuery: true, timeline: true,
  searchModes: 7, dataSources: 6,

  // Lifecycle
  decay: true, supersede: true, contradiction: true,
  quarantine: false, autoResolve: true, trustModel: false, explicitForget: true,

  // Extraction
  autoExtract: true, contentPreproc: true, dedup: true,
  qualityRefine: true, narrative: true, clustering: true,
  recurrence: true, persona: false,

  // Platform
  p_claude: true, p_codex: true, p_opencode: true, p_gemini: true,
  p_copilot: true, p_cursor: true, p_windsurf: true, p_openclaw: true,
  p_hermes: false, p_pi: false, p_antigravity: false,

  // Benchmarks
  b_locomo: "—", b_longmemeval: "86.0% (sess) / 80.4% (turn)",
  b_personamem: "—", b_token: "—", b_methodology: true,
}
```

## Verification Notes

- **All ✅ claims verified** against source code (server_impl.py, sqlite_vec.py, models/memory.py, models/ontology.py, services/memory_service.py, pyproject.toml) and GitHub README.
- **❌ claims confirmed absent**: No code graph, no docs search, no deep search of thinking traces, no quarantine, no formal trust model (credibility field exists but no propagation), no persona extraction engine, no LoCoMo/PersonaMem/token reduction benchmarks.
- **Schema fields count**: Derived from SQLite DDL (11 columns + vec0 embedding + 6 graph columns + 12+ metadata sub-fields). Count: ~28. The metadata JSON blob is extensible, so more fields can be added without schema changes.
- **Search modes**: Counted 7 distinct retrieval paths from code: semantic (retrieve), fulltext (FTS5), hybrid (combined), tag search (search_by_tag), temporal-filtered, RRF multi-strategy fusion, mistake note search.
- **Data sources**: Counted 6: REST API, MCP tools, web dashboard, CLI harvest, file ingestion (PDF/text/JSON/CSV), agent auto-capture.
- **Platform support**: Verified via README tool listings and source code (opencode/ dir, .claude-plugin/ dir, claude_commands/ dir, codex_commands/ dir). 27+ explicitly named tools.
- **Benchmarks**: LongMemEval scores self-reported and transparently described in comparison table with methodology explanation. Not independently verified.
- **Created date**: Verified via GitHub API: `created_at: "2024-12-26T10:15:44Z"`.
- **Star count**: Verified via GitHub API: `stargazers_count: 1901`.
