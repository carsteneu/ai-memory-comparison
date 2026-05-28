# LightMem Audit Evidence

**Repository**: https://github.com/zjunlp/LightMem
**Stars**: 872 | **Forks**: 79 | **Language**: Python | **Created**: 2025-06-11
**Last push**: 2026-05-04 | **Commits**: 274
**License**: MIT (LICENSE file; pyproject.toml incorrectly states Apache-2.0)
**Docs URL**: https://github.com/zjunlp/LightMem/blob/main/README.md

---

## Description

LightMem is a **dual-purpose academic project** from Zhejiang University NLP (ZJUNLP) — published at **ICLR 2026**. It serves two roles:

1. **Research framework**: A baseline evaluation pipeline for benchmarking memory-augmented LLM systems on LongMemEval and LoCoMo datasets. Compares LightMem against Mem0, A-MEM, LangMem, MemoryOS, FullContext, and NaiveRAG.
2. **Practical library**: A deployable Python package (`pip install lightmem` — "Coming soon" per README) with an **MCP server** that allows Claude Code and other MCP-compatible agents to use it as an external memory backend.

The secondary paper **StructMem** (ACL 2026) adds hierarchical event-level memory with cross-event consolidation.

**Is it a research artifact or a practical tool?** It's both, but the **weight is on the research side**. The README opens with ICLR 2026 acceptance, and most content is benchmark results. Practical tooling exists (MCP server, Jupyter notebooks for travel/code assistants) but is secondary. The infrastructure is built for evaluation rigor, not production deployment. No pip release exists yet ("Coming soon").

**Deployment**: Local Python library. Runs as an imported module in Python scripts or as an MCP HTTP server via FastMCP.
**Storage**: Qdrant (local vector DB), FAISS, BM25 (JSON files). No remote/cloud storage dependency.
**Integration**: MCP protocol (Claude Code, any MCP client). Python API (`LightMemory.from_config()`).
**Setup**: `git clone`, conda env, `pip install -e .`, download HuggingFace models (LLMLingua-2, all-MiniLM-L6-v2), configure API keys.

---

## Feature Audit

Legend: true = evidence found, false = no evidence, — = feature referenced but not yet implemented/placeholder.

### Architecture

| Feature | Present | Evidence |
|---------|---------|----------|
| webUi | false | No web UI mentioned. MCP server is HTTP API only. |
| offline | true | Local deployment via Ollama, vLLM, Transformers. Qdrant local storage. No cloud dependency. |
| privacy | true | All processing local. Embeddings via HuggingFace models locally. Vector DB on disk. |
| export | true | `save_memory_entries()` exports to JSON. Memory entries persist to Qdrant on disk. |
| multiAgent | false | No multi-agent support. Single-threaded MCP server. No inter-agent communication. |
| llmFlex | true | Supports OpenAI, DeepSeek (v4-flash, v4-pro), Ollama (local), vLLM (local), Transformers (local). Configurable per backend. |

### Data Model

| Feature | Present | Evidence |
|---------|---------|----------|
| entities | true | StructMem event extraction captures "factual components: who, what, when, where". `category`/`subcategory`/`memory_class` fields imply entity typing. |
| actions | false | No explicit action/verb tracking. Memory entries store factual statements and relations, not action primitives. |
| keywords | true | `metadata_generate=True` extracts keywords and entities from messages. Stored as metadata in vector DB payload. |
| context | true | Topic segmentation preserves conversation context. `topic_id` links memories to topic segments. `session_time`/`weekday` provide temporal context. |
| source | true | `speaker_id` and `speaker_name` fields track who said what. `source_id` links extracted facts back to source messages. |
| emotional | false | No emotion detection, sentiment analysis, or affect tracking. |
| conflict | false | No contradiction detection between memories. Offline update merges, doesn't detect conflicts. |
| layeredMemory | true | Three-tier: sensory memory buffer (SenMemBufferManager) → short-term memory buffer (ShortMemBufferManager) → long-term memory (Qdrant). StructMem adds hierarchical summarization (detail → cross-event summary). |
| timeTravel | true | `float_time_stamp` on every entry. Temporal filters via Qdrant range queries. `retrieve()` supports time-range filtering. `retrieval_scope="historical"` limits to past-only. |
| schemaFields (count) | 17 | MemoryEntry dataclass fields: `id`, `time_stamp`, `float_time_stamp`, `weekday`, `category`, `subcategory`, `memory_class`, `memory`, `original_memory`, `compressed_memory`, `topic_id`, `topic_summary`, `speaker_id`, `speaker_name`, `hit_time`, `update_queue`, `consolidated` |

### Search

| Feature | Present | Evidence |
|---------|---------|----------|
| fulltext | true | BM25 retriever (`rank-bm25` dependency). Config via `context_retriever` with `model_name='BM25'`. |
| semantic | true | Vector search via Qdrant and FAISS (`retrieve_strategy='embedding'`). Embeddings from HuggingFace models (default: all-MiniLM-L6-v2, 384d). |
| hybrid | true | `retrieve_strategy='hybrid'` combines context (BM25) filtering with vector reranking. Two-stage retrieval. |
| deep | false | No deep search with surrounding context. Retrieval returns formatted strings: `"{timestamp} {weekday} {memory}"`. |
| codeGraph | false | No code graph indexing. The `graph.py` module exists but is a stub (20 bytes, empty placeholder for `graph_mem` config). |
| docsSearch | false | No documentation indexing or search. |
| factQuery | true | Vector search supports `filters` parameter for metadata filtering (timestamp ranges, speakers, etc.). Qdrant payload filters. |
| timeline | true | Temporal range queries via `float_time_stamp` filters (`gte`, `lte`, `lt`). Time-window based summarization iterates chronologically. |
| searchModes (count) | 3 | `embedding` (vector only), `context` (BM25/keyword only), `hybrid` (BM25 filter + vector rerank) |

### Lifecycle

| Feature | Present | Evidence |
|---------|---------|----------|
| decay | false | No time-based decay or expiration. `consolidated` flag prevents re-processing but doesn't remove entries. |
| supersede | true | `offline_update_all_entries()` uses LLM to decide `action: "update"` (replace `memory` field with `new_memory`) or `action: "delete"`. Update queue constructed from temporal neighbors. |
| contradiction | false | No contradiction detection. Update LLM receives candidate sources but no explicit conflict resolution logic. |
| quarantine | false | No session quarantine. No mechanism to isolate or suppress specific sessions from search results. |
| autoResolve | false | Offline update requires explicit `construct_update_queue_all_entries()` + `offline_update_all_entries()` calls. Not automatic. |
| trustModel | false | No trust scoring. No source-weighted retrieval. All entries treated equally. |
| explicitForget | true | Offline update supports `action: "delete"` — LLM can decide an entry should be removed. No direct "forget this" API though. |

### Extraction

| Feature | Present | Evidence |
|---------|---------|----------|
| autoExtract | true | `metadata_generate=True` automatically extracts facts/metadata from messages using LLM calls. Prompts are configurable. Two extraction modes: `flat` (facts) and `event` (facts + relations + temporal binding). |
| contentPreproc | true | `pre_compress=True` with LLMLingua-2 or entropy-based compression before storage. Reduces token counts before extraction. |
| dedup | true | `construct_update_queue_all_entries()` finds temporal neighbors for similarity-based merging. `extract_threshold` controls extraction selectivity. QA during update uses LLM to decide merge/update/delete. |
| qualityRefine | false | No explicit quality scoring or refinement pass. Extraction is single-pass from LLM output. Offline update is the only refinement mechanism. |
| narrative | true | StructMem event extraction mode preserves event bindings and causal relationships. Hierarchical summarization with cross-event consolidation (`summarize()` with `enable_cross_event=True`). `retrieval_scope="global"` vs `"historical"`. |
| clustering | true | Topic segmentation via LLMLingua-2 splits long conversations into topical clusters. Each segment gets a unique `topic_id`. |
| recurrence | false | No recurring pattern or periodic event detection across sessions. |
| persona | false | No user persona/profile extraction. No trait modeling. Speaker tracking exists but doesn't build personality models. |

### Platform

| Feature | Present | Evidence |
|---------|---------|----------|
| p_claude | true | MCP server (`mcp/server.py`) built with FastMCP. README shows Claude Desktop config. MCP tools: `add_memory`, `retrieve_memory`, `offline_update`, `get_timestamp`, `show_lightmem_instance`. |
| p_codex | false | No Codex-specific integration. |
| p_opencode | false | No OpenCode-specific integration. (MCP server is generic and could work, but not tested/targeted.) |
| p_gemini | false | No Gemini-specific integration. |
| p_copilot | false | No GitHub Copilot extension. |
| p_cursor | false | No Cursor integration. |
| p_windsurf | false | No Windsurf integration. |
| p_openclaw | false | No OpenClaw integration. |
| p_hermes | false | No Hermes integration. |
| p_pi | false | No Pi integration. |
| p_antigravity | false | No Antigravity integration. |

### Benchmarks

| Feature | Present | Evidence |
|---------|---------|----------|
| b_locomo | true | Extensive LoCoMo results with multiple backbone/judge model combinations. Full detail tables with token costs, runtime, per-question-type breakdowns (Multi, Open, Single, Temp). |
| b_longmemeval | true | LongMemEval reproduction scripts. Baseline evaluation framework runs LightMem, A-MEM, LangMem, MemZero, FullContext, NaiveRAG on LongMemEval. |
| b_personamem | false | No PersonaMem benchmark mentioned. |
| b_token | true | Built-in `token_stats` tracking: prompt/completion/total tokens per operation (add_memory, update, summarize, embedding). `get_token_statistics()` method. Baseline framework has `token_monitor.py` for cross-tool cost tracking. |
| b_methodology | true | Three-stage pipeline: memory construction (incremental message-by-message) → memory retrieval (top-k for each query) → QA + judge evaluation. Checkpoint/resume support. Parallel processing (multi-thread + multi-process). Non-invasive monkey-patching for token monitoring. |

---

## Summary

LightMem is a **strong research artifact** with practical aspirations. It is genuinely a tool (you can `pip install` and run it), but its primary identity is academic — the ICLR 2026 paper dominates the README, and the infrastructure is built for reproducible benchmarking, not product polish.

**Strengths for comparison**: Well-defined data model (17 fields), clean search stack (BM25 + vector + hybrid), MCP integration for Claude, temporal awareness, event extraction mode, comprehensive benchmarks.

**Gaps vs. production memory tools**: No web UI, no decay, no conflict resolution, no trust model, graph memory is a stub, no persona extraction, limited platform support (Claude only via MCP), `online_update` is a placeholder (no-op).

**Classification**: Paper-first, tool-second. For the ai-memory-comparison matrix, treat as a research framework with usable MCP integration.
