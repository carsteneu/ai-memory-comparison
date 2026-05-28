# memsearch — Audit Evidence

**URL**: https://github.com/zilliztech/memsearch
**Audit date**: 2026-05-28
**Audit method**: GitHub README + source code inspection (core.py, store.py, chunker.py, config.py, cli.py, CLAUDE.md, CONTRIBUTING.md, evaluation/README.md, design-philosophy docs, GitHub API metadata)
**Version**: 0.4.5 (latest release)
**Stars at audit**: 1,861 (GitHub API); README badge shows 1.9k

---

## Vital Signs

| Feature | Value | Evidence |
|---------|-------|----------|
| **stars** | 1861 | GitHub API `stargazers_count`: 1861 |
| **language** | Python | GitHub API `language`: Python; pyproject.toml, core.py, cli.py |
| **license** | MIT | GitHub API `license.key`: mit; LICENSE file |
| **singleBinary** | false | Python package, requires `uv tool install` or `pip install`, no compiled binary |
| **created** | 2026-02-09 | GitHub API `created_at`: "2026-02-09T02:29:16Z" |
| **coverage** | N/A | Tests exist (`tests/` directory, pytest), but no published coverage metric found |
| **docs** | https://zilliztech.github.io/memsearch/ | README badge, mkdocs.yml, design-philosophy page |

---

## Architecture

| Feature | Value | Evidence |
|---------|-------|----------|
| **deployment** | Local CLI / Python library, with optional Zilliz Cloud | `uv tool install memsearch` (CLI tool), `MemSearch` class (library). Milvus Lite (local .db), Milvus Server (Docker), Zilliz Cloud (managed). README: "Pick your platform, install the plugin" |
| **storage** | Milvus (vector) + Markdown files (source of truth) | store.py: MilvusStore wrapping pymilvus.MilvusClient. README: "Markdown is the source of truth... Milvus is a shadow index: a derived, rebuildable cache" |
| **integration** | Plugins (4) + CLI + Python API | CLAUDE.md: plugins/claude-code/, plugins/codex/, plugins/opencode/, plugins/openclaw/. core.py: MemSearch class. cli.py: Click CLI |
| **proxy** | false | No proxy architecture. MemSearch is a direct library/CLI, plugins shell out to `memsearch` CLI |
| **webUi** | false | No web UI found in source or docs. No TUI either |
| **offline** | true | ONNX bge-m3 runs locally on CPU (no API key needed). Milvus Lite is a local .db file. evaluation/README.md: "No API key required — zero-config experience" |
| **multiAgent** | true | Cross-platform memory sharing across 4 agents. design-philosophy: "memories written by one agent are searchable from any other." Shared markdown files + Milvus index |
| **llmFlex** | 9 | config.py: 8 embedding providers (openai, google, voyage, jina, mistral, ollama, local, onnx) + anthropic for compact/summarization. pyproject.toml extras: google, voyage, jina, mistral, ollama, local, anthropic, onnx |
| **cacheOpt** | true | core.py index_file: SHA-256 content hash dedup — only re-embeds changed chunks. chunker.py compute_chunk_id: composite hash ID prevents redundant work |
| **privacy** | false | No encryption. Data in plain markdown files + local Milvus Lite db. No privacy/encryption features documented |
| **export** | true | Markdown is the source of truth — portable plain-text files. No export step needed. README: "If you stop using memsearch tomorrow, your knowledge base is still right there on disk, fully intact" |
| **setup** | `uv tool install memsearch` | README Installation section; also `pipx install memsearch` or `pip install memsearch` |
| **pricing** | free (self-hosted), Zilliz Cloud has free tier | README: "Milvus Lite (default) — zero config, single file." Zilliz Cloud: "free tier available" with signup |

---

## Data Model

| Feature | Value | Evidence |
|---------|-------|----------|
| **unit** | Markdown chunk | chunker.py: Chunk dataclass — `content, source, heading, heading_level, start_line, end_line, content_hash`. Chunks are markdown sections split by heading boundaries |
| **entities** | false | No entity extraction. Chunk model has no entity fields |
| **actions** | false | No action/tool tracking in data model |
| **keywords** | false | No keyword/tag system |
| **anticipatedQueries** | false | No anticipated query field |
| **triggerRules** | false | No trigger rule / disclosure condition system |
| **domainTag** | false | No domain tagging |
| **taskType** | false | No task type classification |
| **context** | false | No "why" context field. Chunks store raw content only |
| **source** | true | store.py schema: `source` (VARCHAR, 1024) — file path of origin. Every chunk tracks its source markdown file |
| **originTrust** | false | No trust scoring per source. All sources treated equally |
| **emotional** | false | No emotional metadata |
| **conflict** | false | No conflict detection/surfacing between memories |
| **layeredMemory** | false | No explicit memory layers (working/episodic/semantic). Progressive disclosure (L1→L2→L3) is a retrieval pattern, not storage layers |
| **timeTravel** | false | No temporal versioning of individual memories. Daily .md files provide coarse time buckets (YYYY-MM-DD.md) but no per-memory time-travel |
| **schemaFields** | 9 | store.py _ensure_collection(): `chunk_hash` (PK), `embedding`, `content`, `sparse_vector`, `source`, `heading`, `heading_level`, `start_line`, `end_line`. Plus dynamic fields enabled |

---

## Search & Retrieval

| Feature | Value | Evidence |
|---------|-------|----------|
| **fulltext** | true | store.py: BM25 via `sparse_vector` auto-generated by Milvus BM25 Function on `content` field. Hybrid search uses `AnnSearchRequest` on `sparse_vector` with `metric_type: "BM25"` |
| **semantic** | true | store.py: dense vector search on `embedding` field (FLOAT_VECTOR, COSINE metric). core.py search(): embed query → store.search() |
| **hybrid** | true | store.py search(): `AnnSearchRequest` for both `embedding` (COSINE) and `sparse_vector` (BM25) → `RRFRanker(k=60)` for fusion. Design doc confirms "Dense vector + BM25 sparse + RRF reranking" |
| **deep** | false | No search across raw conversation transcripts or thinking traces in core. Transcript parsing (L3) is plugin-level (Claude Code JSONL parser in transcript.py), not a search mode. No search across agent reasoning/thinking |
| **codeGraph** | false | No code graph analysis. No tree-sitter, no AST parsing, no symbol graph traversal |
| **docsSearch** | false | No documentation search/indexing capability |
| **factQuery** | false | No structured fact/metadata querying. store.py query() does scalar filter on chunk fields but no fact-level queries |
| **timeline** | false | Daily markdown files (YYYY-MM-DD.md) provide temporal organization but no interactive timeline view or query-by-date-range feature |
| **searchModes** | 3 | Progressive disclosure: L1 (`memsearch search` — ranked chunks from Milvus), L2 (`memsearch expand <chunk_hash>` — full markdown section from source file), L3 (`transcript.py <jsonl>` — raw conversation turns). Design-philosophy: "Three-layer progressive disclosure" |
| **dataSources** | 1 | Markdown files only. store.py scanner: finds `.md`/`.markdown`. No additional data source types. Transcripts are parsed on-the-fly (L3) but not separately indexed |

---

## Knowledge Lifecycle

| Feature | Value | Evidence |
|---------|-------|----------|
| **decay** | false | No time-based decay or forgetting curve. No staleness scoring. No FSRS or spaced repetition |
| **supersede** | false | No semantic supersede mechanism. Stale chunks are deleted on re-index (idempotent indexing) but no explicit "this replaces that" relationship. Daily files accumulate additively |
| **contradiction** | false | No contradiction detection between stored facts |
| **quarantine** | false | No quarantined/excluded sessions or learnings |
| **autoResolve** | false | No auto-resolution of tasks or stale knowledge. Compact generates summaries (append-only), not resolution |
| **trustModel** | false | No trust/confidence scoring. All sources equal weight |
| **explicitForget** | true | CLI: `memsearch reset --yes` drops entire collection. API: `store.delete_by_source()` removes chunks when source file deleted. `store.delete_by_hashes()` for specific chunk removal. File deletion → auto-cleanup on next `index()`. However, no per-memory "forget this" tool exposed in plugin UX — only CLI-level deletion |

---

## Extraction Pipeline

| Feature | Value | Evidence |
|---------|-------|----------|
| **autoExtract** | true | Plugin hooks auto-capture conversations. README: "Stop hook fires → Parse last turn → LLM summarizes (haiku) → Append to memory/YYYY-MM-DD.md → memsearch index → Milvus." All 4 platform plugins implement capture |
| **contentPreproc** | false | chunker.py clean_content_for_embedding() strips HTML comments and collapses blank lines, but this is embedding-quality preprocessing only. No content-aware enrichment, entity extraction, or structural preprocessing |
| **dedup** | true | SHA-256 content hash on chunks (chunker.py). Composite chunk_id = hash(source:startLine:endLine:contentHash:model). Only re-embeds changed chunks. core.py: "hash unchanged? → skip (no API call)" |
| **qualityRefine** | false | No quality scoring, fact verification, or confidence calibration |
| **narrative** | false | `memsearch compact` generates LLM-powered summaries ("Memory Compact" appended to daily log), but this is chunk summarization, not narrative generation with timelines or story arcs |
| **clustering** | false | No chunk clustering, topic modeling, or community detection |
| **recurrence** | false | No pattern/recurrence detection across sessions |
| **persona** | false | user_profile maintenance task exists in config (`plugins.<platform>.user_profile`) but is disabled by default. It's a scheduled background task, not part of the core extraction pipeline. Not a built-in automatic feature |

---

## Platform Support

| Platform | Supported | Evidence |
|----------|-----------|----------|
| **p_claude** | true | plugins/claude-code/: 4 shell hooks + 1 skill (memory-recall). README: `/plugin marketplace add zilliztech/memsearch` |
| **p_codex** | true | plugins/codex/: shell hooks (SessionStart, Stop, UserPromptSubmit) + memory-recall skill. README: `bash memsearch/plugins/codex/scripts/install.sh` |
| **p_opencode** | true | plugins/opencode/: TypeScript npm plugin. README: `{ "plugin": ["@zilliz/memsearch-opencode"] }` |
| **p_openclaw** | true | plugins/openclaw/: TypeScript plugin (index.ts). README: `openclaw plugins install --force clawhub:memsearch` |
| **p_gemini** | false | No Gemini CLI plugin found |
| **p_copilot** | false | No Copilot integration found |
| **p_cursor** | false | No Cursor integration found |
| **p_windsurf** | false | No Windsurf integration found |
| **p_hermes** | false | No Hermes integration found |
| **p_pi** | false | No pi/omp integration found |
| **p_antigravity** | false | No Antigravity integration found |

---

## Benchmarks (Published)

| Benchmark | Value | Evidence |
|-----------|-------|----------|
| **b_locomo** | — | No LoCoMo benchmark results published |
| **b_longmemeval** | — | No LongMemEval benchmark results published |
| **b_personamem** | — | No PersonaMem benchmark results published |
| **b_token** | — | No token reduction claims published |
| **b_methodology** | true | evaluation/README.md: Comprehensive embedding provider benchmark methodology — 955 chunks × 2172 queries, 12 embedding models evaluated across Recall@K, MRR, NDCG@10 in both Chinese and English. However this benchmarks embedding quality, not memory system performance |

---

## Additional Findings

### Markdown as Source of Truth

This is memsearch's foundational design principle. Confirmed in source: `core.py` reads `.md` files and indexes them. Design-philosophy: "The vector database is a derived index — it can be dropped and rebuilt at any time from the markdown files on disk." The chunk_id includes `content_hash` and `model` name, meaning changing embedding providers requires re-indexing.

### 3-Layer Progressive Recall

Unique among audited systems. L1 (`search`) returns ranked chunk snippets. L2 (`expand`) shows the full heading section from the source .md file. L3 (`transcript`) parses raw Claude Code JSONL conversation files. In the Claude Code plugin, the entire recall runs in a forked subagent (`context: fork`) to avoid polluting main context. CLAUDE.md confirms this architecture.

### Embedding Provider Evaluation

The evaluation/ directory contains a thorough benchmark of 12 embedding models (plus ONNX variants) across Chinese and English. This is methodology-only (not a memory system benchmark like LoCoMo/LongMemEval). The ONNX bge-m3 int8 model was chosen as the Claude Code plugin default based on: zh R@5=0.776, en R@5=0.814, 558MB download, zero API key.

### Cross-Platform Design

memsearch is the only system in the comparison explicitly designed for cross-agent memory sharing. The 4 plugins (Claude Code, Codex, OpenClaw, OpenCode) all write to the same `.memsearch/memory/` directory in identical format, using the same Milvus index. design-philosophy: "memories written by one agent are searchable from any other."

### SHA-256 Dedup

Every chunk is hashed with SHA-256 (first 16 hex chars used). The composite chunk_id = `hash(markdown:source:startLine:endLine:contentHash:model)`. When re-indexing, only chunks whose composite ID has changed are re-embedded. Unchanged chunks are skipped — a natural dedup mechanism without a separate cache layer.

### Tailored for Milvus

Unlike competitors that wrap multiple vector stores, memsearch is tightly integrated with Milvus. The BM25 sparse vector is auto-generated by Milvus's built-in BM25 Function (no app-side sparse encoding). The 3-tier deployment model (Milvus Lite → Milvus Server → Zilliz Cloud) uses the same API — just change one URI.

### No "Learning" Abstraction

memsearch has no concept of a "learning" or "fact" — it operates at the raw text chunk level. There is no entity extraction, no structured metadata (entities, actions, keywords, domain tags, trigger rules, trust scores), no contradiction detection, no decay model. The system is purely a search engine over markdown content. This is a deliberate design choice (markdown as source of truth), but it means memsearch scores low on data model richness compared to systems like YesMem or agentmemory.

### Compact (LLM Summarization)

The `compact` command uses an LLM to summarize indexed chunks and appends the result to a daily markdown log. This creates a "Memory Compact" section in `memory/YYYY-MM-DD.md`. The next `index()` run picks this up as normal markdown. This provides a form of hierarchical summarization but is append-only and not part of an automatic extraction pipeline.

### Config System

Layered TOML configuration: dataclass defaults → `~/.memsearch/config.toml` → `.memsearch.toml` → CLI flags. Supports per-project configuration, plugin summarization routing (route each plugin's summarizer through a different LLM provider), and `env:VAR_NAME` syntax for secrets. The config system is well-structured with typed dataclasses (config.py).

---

## Summary Verification vs. README Claims

| README Claim | Verified | Notes |
|---|---|---|
| "Cross-platform semantic memory" | ✅ | 4 platform plugins confirmed |
| "3-layer progressive recall" | ✅ | L1 search → L2 expand → L3 transcript, confirmed in CLI and plugin source |
| "Markdown is the source of truth" | ✅ | core.py reads .md files; Milvus is shadow index, rebuildable |
| "Hybrid search: dense + BM25 + RRF" | ✅ | store.py: ANN on embedding + ANN on sparse_vector + RRFRanker(k=60) |
| "Smart dedup: SHA-256 content hashing" | ✅ | chunker.py: content_hash via SHA-256; core.py: skip unchanged chunks |
| "Live sync: file watcher auto-indexes" | ✅ | watcher.py + cli.py watch command |
| "ONNX bge-m3, runs locally on CPU" | ✅ | evaluation confirms zh R@5=0.776; 558MB model; onnxruntime provider |
| "1.9k stars" | ⚠️ | README badge shows 1.9k; GitHub API shows 1861 |
| "Milvus-backed" | ✅ | pymilvus >= 2.5.0; milvus-lite for local |
