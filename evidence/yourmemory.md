# YourMemory — Audit Evidence

**Repo**: [sachitrafa/YourMemory](https://github.com/sachitrafa/YourMemory)
**Audit date**: 2026-05-29
**Version**: 1.4.29 (PyPI)
**Stars**: 231 | **Forks**: 17 | **Language**: Python 99%+ | **License**: CC BY-NC 4.0
**Created**: 2026-03-02
**Homepage**: https://yourmemoryai.xyz/
**Docs**: https://github.com/sachitrafa/YourMemory#readme
**PyPI**: https://pypi.org/project/yourmemory/

---

## Description

Persistent memory for AI agents built on the Ebbinghaus forgetting curve. Self-hosted MCP server that plugs into Claude Code, Cursor, Cline, Windsurf, OpenCode, and any MCP client. Local-first (SQLite/DuckDB default), Postgres+pgvector for teams. Models memory on human cognition: importance-modulated decay, subject-aware deduplication, entity-graph linking, and hybrid BM25+vector+graph retrieval. Claims 2x better recall than Zep Cloud on LoCoMo (59% vs 28%), 89.4% Recall@5 on LongMemEval.

---

## Architecture

- **Pattern**: MCP stdio server (FastAPI + uvicorn for HTTP API + SSE transport)
- **Deployment**: `pip install yourmemory`, one-command setup (`yourmemory-setup`), Docker image available
- **Backends**: DuckDB (default, zero-setup), SQLite, PostgreSQL+pgvector
- **Graph backends**: NetworkX (default, pickle persistence at `~/.yourmemory/graph.pkl`), Neo4j (optional)
- **Embeddings**: sentence-transformers `multi-qa-mpnet-base-dot-v1` (768 dims), local
- **NLP**: spaCy `en_core_web_sm` for NER, categorization, contradiction detection
- **Scheduler**: APScheduler for 24h decay/pruning job
- **Self-hosted**: TRUE — everything runs locally, no cloud dependency
- **Offline-capable**: TRUE — local embeddings, local DB, no API calls required for core operation

---

## Data Model

### Tables

| Table | Purpose |
|---|---|
| `memories` | Primary memory store with embeddings |
| `user_activity` | Tracks active days for activity-aware decay |
| `memory_history` | Audit trail for superseded/updated memories |
| `agent_registrations` | Multi-agent API key auth |

### Memories Table — Schema Fields (12–14 depending on backend)

| # | Field | Type | Backend | Notes |
|---|-------|------|---------|-------|
| 1 | `id` | SERIAL/BIGINT/INTEGER | All | Primary key |
| 2 | `user_id` | TEXT/VARCHAR | All | Multi-tenant key |
| 3 | `content` | TEXT | All | The memory text |
| 4 | `category` | TEXT/VARCHAR | All | `fact`/`strategy`/`assumption`/`failure` |
| 5 | `importance` | FLOAT/REAL | All | 0.0–1.0, modulates decay rate |
| 6 | `embedding` | FLOAT[768]/vector(768)/TEXT JSON | All | 768-dim sentence embedding |
| 7 | `recall_count` | INTEGER | All | Number of times recalled |
| 8 | `created_at` | TIMESTAMP/TEXT | All | Creation timestamp |
| 9 | `last_accessed_at` | TIMESTAMP/TEXT | All | Last recall timestamp |
| 10 | `agent_id` | VARCHAR/TEXT | All | Multi-agent ownership |
| 11 | `visibility` | VARCHAR/TEXT | All | `shared` or `private` |
| 12 | `context_paths` | VARCHAR/TEXT | All (via migration) | JSON array of file/dir paths for spatial boost |
| 13 | `memory_type` | TEXT | Postgres+SQLite only | `trivial` default (not in DuckDB) |
| 14 | `content_tsv` | tsvector (GENERATED) | Postgres only | Generated column for FTS |

- **UNIQUE constraint**: `(user_id, content)` — prevents exact duplicate storage, triggers recall_count bump on conflict

### Memory Categories (controls decay rate)

| Category | Base λ | Half-life (importance=0.5) | Purpose |
|----------|--------|---------------------------|---------|
| `strategy` | 0.10 | ~38 days | Successful patterns, decisions |
| `fact` | 0.16 | ~24 days | Preferences, identity, stable knowledge |
| `assumption` | 0.20 | ~19 days | Inferred context, uncertain beliefs |
| `failure` | 0.35 | ~11 days | Errors, wrong approaches, env issues |

---

## Search / Retrieval

### Pipeline (2 rounds)

**Round 1 — Hybrid search:**
```
hybrid_score = 0.4 × bm25_norm + 0.6 × cosine_similarity
```
- Vector cosine similarity (primary, threshold 0.50 with 0.20 fallback)
- BM25 full-text keyword scoring (all three backends: DuckDB FTS, Postgres tsvector, SQLite FTS5)
- Results sorted by hybrid score (decay intentionally excluded from ranking)

**Round 2 — Graph BFS expansion:**
- Multi-hop BFS from Round 1 seeds (depth 2)
- Entity edges (spaCy NER): shared named entities (PERSON, ORG, GPE, LOC, FAC, PRODUCT, EVENT, WORK_OF_ART, NORP, LAW) → weight 0.55
- Similarity edges: cosine similarity × verb weight (from SVO extraction) → weight varies
- Expanded nodes capped at similarity = reinforce_threshold - 0.01 (0.74) to prevent accidental recall propagation

### Search Modes (4 mechanisms in unified pipeline)

1. **Vector-only** — cosine similarity on 768-dim embeddings
2. **BM25/keyword** — full-text search across all backends
3. **Hybrid fusion** — weighted BM25 + cosine combinatio
4. **Graph BFS expansion** — multi-hop entity + similarity edge traversal

### Boost Mechanisms

- **Spatial boost** (+0.08): When `current_path` matches stored `context_paths`
- **Temporal boost** (+0.25): When query contains time window expressions ("last week", "recently")
- **Session wrap-up**: Recalled memory IDs tracked per session; recall_count bumped on session idle (default 30 min)
- **Recall throttling**: `YOURMEMORY_RECALL_COOLDOWN` caches identical (user, query) pairs
- **Chain-aware recall propagation**: High-similarity memories (≥0.75) propagate recall boost to depth-1 graph neighbours

---

## Lifecycle

### Ebbinghaus Forgetting Curve

```
effective_λ = base_λ × (1 − importance × 0.8)
strength    = clamp(importance × e^(−effective_λ × active_days) × (1 + recall_count × 0.2), 0, 1)
```

- **Activity-aware**: `active_days` counts only days user was active (from `user_activity` table), not wall-clock days
- **Fallback**: wall-clock days if `user_activity` table is empty
- **Prune threshold**: memories with strength < 0.05 auto-pruned every 24 hours
- **Chain-aware pruning**: A decayed memory with a strong graph neighbour is kept alive (preserves multi-hop chains)
- **Recall boost**: `recall_count + 0.2` multiplier slows decay each time retrieved
- **Session wrap-up**: Idle session flush (30 min timeout) bumps recall_count for all recalled memories

### Supersession & Audit

- `update_memory(id, new_content, importance)` — re-embeds, replaces content, logs old content to `memory_history`
- PUT `/memories/{id}` — same supersession audit trail
- DELETE `/memories/{id}` — REST endpoint, **NOT an MCP tool** (not exposed to AI agents)

### Deduplication Pipeline (`resolve.py`)

4-tier resolution based on cosine similarity with existing memories:

| Similarity | Action | Description |
|-----------|--------|-------------|
| ≥ 0.92 | **reinforce** | Near-identical paraphrase, bump recall_count only |
| 0.85–0.92 + contradiction | **replace** | Same entity, conflicting info → overwrite |
| 0.85–0.92 + no contradiction | **merge** | Same entity, complementary info → entity-append |
| < 0.85 | **new** | Distinct memory, plain INSERT |

**Subject-aware gate**: Embeddings of leading 2 words compared — different subjects ("Sachit" vs "YourMemory") never merge even at high similarity.

---

## Extraction

### Categorization (`extract.py`)

- **spaCy dependency parse**: Subject → `fact`, no subject → `assumption`
- **Regex fallback**: Imperative patterns → `assumption`
- Additional categories (`strategy`, `failure`) set manually by the AI at store time

### Question Detection (`is_question`)

- Ends with `?` OR first word in `{what, who, where, when, why, how, which, whose, whom}` → rejected (422)
- Prevents accidental storage of questions

### Contradiction Detection (`detect_contradiction`)

3 detection strategies:
1. **Polarity flip**: Positive verb (love/use/prefer) ↔ negative verb (hate/avoid/refuse)
2. **Negation flip**: Same ROOT verb with opposite negation ("appeared" vs "did not appear")
3. **Number conflict**: Different 3-4 digit numbers within shared context (≥4 common words)

### Entity Extraction (Graph — `svo_extract.py` + `_entity_linked_nodes`)

- spaCy NER with curated labels (PERSON, ORG, GPE, LOC, FAC, PRODUCT, EVENT, WORK_OF_ART, NORP, LAW)
- Multi-word prefix decomposition: "Shirley Temple Black" → also matches "Shirley Temple"
- SVO triples for verb-weighted similarity edges

### Merge (`merge_entities`)

- Named entities + noun chunks + capitalized tokens appended when absent from existing memory
- e.g., "With MongoDB" → "uses DuckDB with MongoDB"

---

## Platforms

| Platform | Evidence | Method |
|----------|----------|--------|
| **Claude Code** | ✅ | `~/.claude/settings.json` auto-configured by `yourmemory-setup` |
| **Claude Desktop** | ✅ | `claude_desktop_config.json` on macOS/Windows/Linux |
| **Cursor** | ✅ | `~/.cursor/mcp.json` + macOS/Windows settings.json paths |
| **Cline (VS Code)** | ✅ | `cline_mcp_settings.json` in VS Code globalStorage |
| **Windsurf** | ✅ | `~/.codeium/windsurf/mcp_settings.json` + platform paths |
| **OpenCode** | ✅ | `~/.config/opencode/opencode.json` with different schema (array commands, not string) |
| **Any MCP client** | ✅ | Standard stdio MCP server; SSE transport available |
| **CLAUDE.md injection** | ✅ | `_inject_memory_rules()` writes memory workflow rules to CLAUDE.md, Cursor rules, Windsurf memories, OpenCode instructions |

---

## Benchmarks

| Benchmark | Metric | Score | Date | Script |
|-----------|--------|:-----:|------|--------|
| **LongMemEval-S** | Recall-any@5 | **89.4%** | 2026-04-28 | `benchmarks/longmemeval_fullstack.py` |
| **LongMemEval-S** | Recall-all@5 | 84.8% | 2026-04-28 | Same |
| **LoCoMo-10** | Recall@5 | **59%** | 2026-04-20 | `benchmarks/locomo_4way.py` |
| **HotpotQA** | BOTH_FOUND@5 | **71.5%** | 2026-05-06 | `benchmarks/hotpotqa_reasoning.py` |
| **Token savings** | 3-session reduction | −19.7% | N/A | `benchmarks/two_session_comparison.py` |

**Methodology notes**:
- All benchmark scripts are open-source in the repo
- LoCoMo: compared against Zep Cloud (28%), Supermemory (31%*), Mem0 (18%*); * = free-tier quota exhausted mid-benchmark
- LongMemEval: temporal boost ablation published (0pp gain on this benchmark — temporal questions are event-anchored, not window-anchored)
- HotpotQA: entity graph adds +12pp over similarity-only graph
- Token savings: measured with `claude-sonnet-4-6` pricing; 30-session projection shows −84.1%

---

## Additional Features

### Web UI (Built-in)
- **Memory Browser**: `http://localhost:3033/ui` — stats bar, memory cards with strength bars, filters by category, sort by strength/recency/recall, agent tabs
- **Graph Visualizer**: `http://localhost:3033/graph?memoryId=42&userId=sachit&depth=2` — interactive force-directed graph, color-coded nodes, click for full content

### Ask Without LLM (`yourmemory ask`)
- CLI: `yourmemory ask "what database does this project use"` → answers from memory without API call
- `/ask` POST endpoint with optional Ollama integration for natural language answers
- Falls back to `"Not enough memory context to answer without Claude."` when confidence below threshold (0.55)

### Multi-Agent Memory
- API key authentication (`ym_xxxx` format, SHA-256 hashed)
- Read/write permission scopes per agent
- `visibility`: shared (all agents) or private (agent-only)
- `register_agent()` via `src/services/api_keys.py`

### MCP Tools (3)

| Tool | Purpose |
|------|---------|
| `recall_memory(query, user_id?, api_key?, top_k?, current_path?)` | Hybrid search + graph expansion + spatial/temporal boosts |
| `store_memory(content, importance, category?, user_id?, api_key?, visibility?, context_paths?, created_at?)` | Dedup → store → graph index → activity record |
| `update_memory(memory_id, new_content, importance)` | Supersession with audit trail → re-embed → graph refresh |

---

## Feature Checklist Summary

| Feature | Present | Notes |
|---------|:-------:|-------|
| Self-hosted | ✅ | DuckDB/SQLite default, Postgres optional |
| MCP server | ✅ | 3 tools + SSE transport |
| Hybrid search | ✅ | BM25 + vector (0.4/0.6 weight) + graph BFS |
| Vector search | ✅ | Cosine similarity, 768-dim |
| BM25/keyword search | ✅ | DuckDB FTS, Postgres tsvector, SQLite FTS5 |
| Graph expansion | ✅ | Entity edges (spaCy NER) + similarity edges (SVO) |
| Ebbinghaus decay | ✅ | Category-specific λ, importance-modulated, activity-aware |
| Deduplication | ✅ | 4-tier: new/reinforce/merge/replace |
| Contradiction detection | ✅ | 3 strategies: polarity/negation/number conflict |
| Audit trail | ✅ | memory_history table |
| Spatial boost | ✅ | context_paths matching current directory |
| Temporal boost | ✅ | Time window expression detection |
| Session tracking | ✅ | Wrap-up recall_count boost on idle |
| Recall throttling | ✅ | Configurable cooldown cache |
| Chain-aware pruning | ✅ | Neighbours keep decayed memories alive |
| Web UI | ✅ | Memory browser + graph visualizer |
| Ask without LLM | ✅ | CLI + /ask endpoint |
| Multi-agent | ✅ | API keys, visibility, read/write scopes |
| NP extraction | ✅ | spaCy NER, SVO triples, entity merging |
| Question rejection | ✅ | is_question() filter on store |
| On-disk persistence | ✅ | DuckDB/SQLite file; NetworkX pickle; Postgres optional |
| DELETE endpoint | ✅ | REST API only, not MCP |
| Claude Code plugin | ✅ | MCP + CLAUDE.md injection |
| Cursor plugin | ✅ | MCP + rules injection |
| OpenCode plugin | ✅ | MCP with unique schema |
| Windsurf plugin | ✅ | MCP + memories injection |
| Cline plugin | ✅ | MCP integration |
| Benchmarks published | ✅ | 3 external datasets, reproducible scripts |
| Offline-capable | ✅ | Local embeddings, local DB, no cloud dependency |
| Docker | ✅ | Docker build CI workflow |
| Export/Import | ❌ | Not present |
| Time-travel query | ❌ | No query-by-date capability |
| Trust model | ❌ | No source-weighted trust scoring |
| Layered memory | ❌ | Single-tier memory (no L0/L1/L2/L3) |
| Prompt-based extraction | ❌ | No LLM-based auto-extract from conversations |
| Forget MCP tool | ❌ | Delete is REST-only, not exposed to AI agents |
| Code-graph search | ❌ | No codebase-aware graph traversal |
| Multi-modal | ❌ | Text-only (no image/audio/video) |

---

## Source Evidence

- **Schema**: `src/db/duckdb_schema.sql` (12 fields + context_paths migration), `src/db/schema.sql` (Postgres, 14 fields incl. generated tsvector), `src/db/sqlite_schema.sql` (13 fields incl. memory_type)
- **Search**: `src/services/retrieve.py` (lines ~1050) — hybrid fusion, BM25, vector, graph BFS expansion
- **Decay**: `src/services/decay.py` — Ebbinghaus formula, activity-aware, category-specific rates
- **Dedup**: `src/services/resolve.py` — 4-tier resolution, contradiction detection (3 types), subject-aware gate
- **Extraction**: `src/services/extract.py` — spaCy dependency parse, regex fallback, question detection
- **Graph**: `src/graph/graph_store.py` — SVO extraction, entity edges, chain-aware pruning, recall propagation
- **Session**: `src/services/session.py` — Thread-safe session tracking, idle flush, recall throttling
- **MCP**: `memory_mcp.py` — 3 tools (recall/store/update), SSE transport, lazy imports
- **API**: `src/routes/memories.py` — CRUD (POST/GET/PUT/DELETE), `src/routes/retrieve.py` — retrieval endpoint
- **UI**: `src/routes/ui.py`, `src/routes/graph_viz.py` — Embedded HTML dashboard and graph visualizer
- **Setup**: `yourmemory-setup` auto-detects 6 client types, injects rules into agent instructions
- **Benchmarks**: `benchmarks/` directory — longmemeval, locomo, hotpotqa, token-efficiency scripts
- **Dependencies**: `pyproject.toml` — duckdb, sentence-transformers, spacy, networkx, fastapi, uvicorn, apscheduler, mcp
- **Docker**: `docker-publish.yml` GitHub Actions workflow
