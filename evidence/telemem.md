# TeleMem — Evidence

> Every claim backed by public source code or documentation.
> Audit date: 2026-05-28. Source: GitHub `TeleAI-UAGI/telemem` main branch, arXiv:2601.06037.

**Actual URL**: `https://github.com/TeleAI-UAGI/telemem` (not `Tele-AI/TeleMem` — org was renamed).

## Vital Signs

- **Stars**: 461 (user-reported, GitHub API confirms `stargazers_count: 461`)
- **Language**: Python (92.8%), Go (3.8%), TypeScript (3.0%)
- **License**: Apache 2.0 — `LICENSE` file, `pyproject.toml` `license = {text = "Apache-2.0"}`
- **Single binary**: false — Python package via `pip install -e .`
- **Created**: 2025-12-05 — GitHub API `created_at: "2025-12-05T02:46:21Z"`
- **Coverage**: N/A — no coverage badge or measurement found
- **Docs URL**: `https://github.com/TeleAI-UAGI/telemem#readme` (+ arXiv paper)
- **Description**: "High-performance drop-in replacement for Mem0, featuring semantic deduplication, long-term dialogue memory, and multimodal video reasoning."

---

## Architecture

### Deployment: Library (Python SDK) ✅
- `pyproject.toml` — Python package, `pip install -e .` or `pip install telemem`
- `README.md` — "import telemem as mem0" drop-in replacement with one line of code
- Inherits Mem0's `Memory` class API — `telemem/__init__.py`: `from .mem0 import TeleMemory as Memory`

### Storage: FAISS + JSON ✅
- `README.md` — "FAISS + JSON dual storage for fast recall and human-readable auditability"
- `telemem/main.py:__init__` — `self.faiss_dir = Path(self.config.vector_store.config.path)`, creates `faiss_db/` directory
- `telemem/main.py:_save_faiss_index` — Dual-write: `faiss.write_index(index, str(index_path))` + JSON metadata
- `pyproject.toml` dependencies: `faiss-cpu`, `chromadb`, `nano-vectordb` (FAISS is primary, others are mem0 dependencies)

### Integration: Python SDK (Mem0 API) ✅
- `telemem/__init__.py` — `from .mem0 import TeleMemory as Memory` — drop-in Mem0 replacement
- `README.md` — `import telemem as mem0` then `memory = mem0.Memory()`
- No MCP server, no hooks, no proxy. Pure Python SDK.

### Web/TUI: false ❌
- No evidence of dashboard, TUI, or web interface anywhere in the codebase or README.
- `telemem/main.py` — pure library code, no web server or UI components.

### Offline: true ✅
- `config/config.yaml` — localhost endpoints for LLM (`http://localhost:8081/v1`) and embeddings (`http://localhost:8082/v1`)
- `README.md` — Configuration for local Qwen3-8B + FAISS. No cloud dependency required.
- `pyproject.toml` — `faiss-cpu` is the primary vector store; no mandatory cloud services.

### Privacy/encrypt: false ❌
- No encryption at rest or in transit. JSON metadata and FAISS indices stored plaintext on disk.
- No privacy-related features documented.

### Data export: false ❌
- No export tool or format. Data is stored as FAISS binary index + JSON files — technically portable but no explicit export function.

### Multi-agent: false ❌
- Single `TeleMemory` instance. No multi-agent coordination, inter-agent messaging, or agent-specific scoping beyond `sample_id`.
- No agent spawn/stop/orchestration primitives.

### LLM providers: 3 ✅
- `pyproject.toml` — depends on `openai` (OpenAI-compatible API) and `mem0ai`
- `config/config.yaml` — Qwen3-8B via OpenAI-compatible API (localhost)
- `config/config.minimax.yaml` — MiniMax M2.7 via OpenAI-compatible API
- `README.md` — OpenAI (default), Qwen3-8B, MiniMax M2.7
- Any OpenAI-compatible endpoint works, but only 3 providers are explicitly configured/mentioned.
- Uses separate LLM and embedder configurations — `telemem/configs.py` `TeleMemoryConfig` inherits from Mem0's `MemoryConfig`.

### Cache optimization: false ❌
- No caching layer. Smart caching in multimodal pipeline only (`add_mm` skips if output exists), but no general memory caching.

### Setup: `pip install -e .` ✅
- `README.md` — `pip install -e .` for development install
- `pyproject.toml` — standard hatchling build. No npm/npx, no curl install.

### Pricing: free ✅
- Apache 2.0 license. No pricing page, no freemium tiers. Library, not a service.

---

## Data Model

### Storage unit: Memory (text + vector + JSON metadata) ✅
- `telemem/main.py:_flush_buffer` — Each memory stored as: `summary` (text), `embedding` (FAISS vector), + metadata JSON
- `telemem/main.py:_process_single_round` — Memory data dict: `summary`, `embedding`, `sample_id`, `original_messages`, `round_index`, `timestamp`

### Entities: false ❌
- No entity extraction pipeline. Characters are handled via per-person summarization, not as first-class entities.
- No NER, no entity linking, no entity graph.

### Actions: false ❌
- No action/event classification as a separate field. Summaries may contain actions implicitly, but no structured action field.

### Keywords/tags: false ❌
- No keyword extraction, tagging, or label system. No `keywords` field in metadata.

### Anticipated queries: false ❌
- No `anticipated_queries` or pre-computed query expansion.

### Trigger rules: false ❌
- No trigger-based retrieval or conditional memory injection.

### Domain tag: false ❌
- No domain classification or `domain` field.

### Task type: false ❌
- No task tracking or task type classification.

### Context (why): true ✅
- `telemem/main.py:_process_single_round` — Context-aware summarization: previous 3 rounds passed as context for event extraction, previous 3 rounds for person extraction
- `telemem/utils.py:get_recent_messages_prompt` — Context window included in prompt: "该轮对话之前的若干轮对话" (previous rounds)
- `telemem/utils.py:get_person_prompt` — Person-specific context: "该轮对话之前的若干轮上下文"
- Each memory stores `original_messages`, `round_index`, `timestamp` for provenance

### Source attribution: false ❌
- No explicit `source` field or trust grading. Memories are attributed to `sample_id` but no source type.

### Origin + trust: false ❌
- No `origin` field, no trust scoring.

### Emotional: false ❌
- No emotional/sentiment tagging.

### Conflict surfacing: false ❌
- No contradiction detection between memories. Semantic merging unifies similar memories but doesn't flag contradictions.

### Layered memory: true ✅
- `telemem/main.py:add()` — Three independent memory partitions: `events` (global narrative), `person_1` (character 1 perspective), `person_2` (character 2 perspective)
- `telemem/main.py:search()` — Searches across all three layers: `results["events"]`, `results["person_1"]`, `results["person_2"]`, `results["combined"]`
- `README.md` — "Automatically creates independent memory profiles for each character"
- `telemem/main.py:offline_build_graph_json()` — Optional graph construction layer on top of events

### Time-travel: false ❌
- Timestamps are stored in metadata (`timestamp` field) but no explicit time-travel query API. No snapshot rollback, no historical state reconstruction. Timestamps are informational only.

### Schema fields: 7 ✅
Core metadata fields in stored memories (`telemem/main.py:_flush_buffer` and `_process_single_round`):
1. `summary` — the memory text
2. `embedding` — FAISS vector
3. `sample_id` — session identifier
4. `round_index` — conversation turn number
5. `timestamp` — ISO datetime
6. `original_messages` — raw dialogue that generated this memory
7. `user` — character name (only for person_1/person_2, not events)

---

## Search & Retrieval

### Full-text: false ❌
- No BM25, FTS5, or keyword search. FAISS `IndexFlatIP` only (inner product / cosine similarity).

### Semantic/vector: true ✅
- `telemem/main.py:search()` — Query embedding via `self.emb_client.embeddings.create()`, then FAISS vector search with `index.search(query_embedding, lim)`
- `telemem/main.py:_find_similar_memories()` — Vector similarity search with `threshold=0.95`, uses `IndexFlatIP` with normalized embeddings
- `README.md` — "Semantic vector-based retrieval of relevant memories"
- Config uses `Qwen3-Embedding-8B` or `text-embedding-3-small`

### Hybrid (BM25+Vec): false ❌
- No BM25 component. Pure vector/semantic search only.

### Deep (incl. thinking): false ❌
- Search returns metadata summaries, no deep content retrieval or thinking-context expansion.

### Code graph: false ❌
- No code-level graph traversal or symbol index.

### Docs search: false ❌
- No documentation ingestion or search.

### Fact metadata query: false ❌
- No structured fact/entity query. No SQL metadata query API.

### Timeline view: false ❌
- Timestamps stored but no timeline-based query or visualization.

### Search modes: 2 ✅
1. **Standard semantic search** — `search()`: FAISS vector search across events, person_1, person_2. Returns combined results.
2. **Graph-based query** — `online_query()`: Loads pre-built memory graph JSON, finds seed nodes via `search_events_for_graph()`, backtracks dependency paths. ReAct-style for multimodal.
   - `search_events_for_graph()` — internal helper for `online_query`
- `README.md` — `search()` for text, `search_mm()` for multimodal (ReAct-style with 3 tools: global_browse, clip_search, frame_inspect)

### Data sources: 1 ✅
- Single source: conversation messages (`List[Dict[str, str]]` with role/content). Multimodal adds video files, channeled through a separate pipeline.

---

## Knowledge Lifecycle

### Decay/forgetting: false ❌
- No time-based decay, FSRS scheduling, or automatic forgetting. Memories persist indefinitely.

### Supersede/replace: true ✅
- `telemem/main.py:_cluster_memories()` — Clusters similar memories by cosine similarity
- `telemem/main.py:_process_cluster()` — LLM-based semantic merging: "新记忆包含已有记忆中没有的新信息，应保留...如果新记忆是重复或无价值的，则去除"
- `telemem/main.py:_flush_buffer()` — Buffer threshold triggers batch flush → clustering → LLM merge
- `README.md` — "LLM-based semantic clustering: merges similar memories via LLM"
- Memories are effectively superseded during merge: duplicates removed, new information preserved, merged summaries replace originals.

### Contradiction detect: false ❌
- Merging combines similar memories but LLM prompt focuses on dedup/preservation, not contradiction flagging.

### Quarantine: false ❌
- No isolation or quarantine mechanism for suspect memories.

### Auto-resolution: false ❌
- Merging is automatic but not conflict resolution.

### Trust model: false ❌
- No trust scores, confidence levels, or provenance-based weighting.

### Explicit forget: false ❌
- No `delete()`, `forget()`, or `remove()` method in the public API. `TeleMemory` only exposes `add()`, `search()`, `offline_build_graph_json()`, `online_query()`, `search_mm()`, `add_mm()`.

---

## Extraction Pipeline

### Auto-extraction: true ✅
- `telemem/main.py:add()` — `infer=True` (default): processes dialogue rounds automatically, extracting summaries via LLM
- `telemem/main.py:_process_single_round()` — Three LLM calls per round: global events, character 1 perspective, character 2 perspective
- `README.md` — "Automatic memory extraction: Extracts and structures key facts from dialogues"
- Internal workflow: message preprocessing → multi-perspective summarization → vectorization → similarity search → batch processing (LLM merge) → persistence

### Content-aware preprocessing: true ✅
- `telemem/utils.py:merge_consecutive_messages()` — Merges consecutive same-role messages
- `telemem/utils.py:parse_messages()` — Normalizes message format to `role: content\n`
- `telemem/utils.py:chunk_with_context()` — Sliding window context chunks (window_size=3)
- `telemem/main.py:add()` — Rounds detection: pairs user-assistant messages into turns, handles edge cases

### Deduplication: true ✅
- `telemem/main.py:_find_similar_memories()` — Vector similarity-based duplicate detection (cosine similarity ≥ threshold, default 0.95)
- `telemem/main.py:_cluster_memories()` — Clustering of similar memories
- `telemem/main.py:_process_cluster()` — LLM-based semantic dedup: merges similar memories, removes duplicates
- `README.md` — "Semantic clustering & deduplication: Uses LLMs to semantically merge similar memories, reducing conflicts and improving consistency"

### Quality refinement: false ❌
- No post-extraction quality scoring, refinement loop, or validation step. LLM extraction is single-pass.

### Narrative generation: false ❌
- Summaries are extracted per-round, not woven into narrative arcs. No story/episode generation.

### Clustering: true ✅
- `telemem/main.py:_cluster_memories()` — Cosine similarity threshold clustering of memory embeddings
- `telemem/main.py:_flush_buffer()` — Clusters combined new+similar memories before LLM merge

### Recurrence detection: false ❌
- No pattern/recurrence detection across sessions.

### Persona extraction: true ✅
- `telemem/main.py:add()` — Creates `person_1` and `person_2` FAISS indices with per-character summaries
- `telemem/utils.py:get_person_prompt()` — Character-focused extraction prompt: "聚焦于'{target_character}'这个角色" covering relationships, plot events, character traits, items/locations
- `README.md` — "Character-profiled memory management: Builds independent memory archives for each character, ensuring precise isolation"
- Four key information types extracted per character: 人物关系与互动 (relationships), 情节发展与事件细节 (plot), 角色特征与背景 (traits), 具体物品与地点 (items/locations)

---

## Platform Support

### All platforms: false ❌
TeleMem is a Python library with Mem0 API compatibility. It does **not** ship any platform-specific integrations:
- No MCP server or MCP tools
- No Claude Code plugin (no `.claude-plugin/` directory)
- No Codex/OpenCode/Copilot/Gemini integration
- No hooks system (no SessionStart, PreToolUse, etc.)
- No REPL/CLI tool
- No plugin marketplace listing

The only integration path is: `import telemem as mem0` in Python code. Any platform that can run Python and use Mem0's Python SDK can theoretically use TeleMem as a drop-in replacement, but no platform-specific adapter code exists.

Evidence of absence:
- `telemem/__init__.py` — only exports `Memory` class. No MCP module, no plugin config.
- No `.claude-plugin/`, `.cursor-plugin/`, `.opencode/` directories in repo tree
- `pyproject.toml` — no MCP SDK, no plugin framework dependencies
- `README.md` — no platform integration section. No mention of any coding assistant.

---

## Benchmarks

### LoCoMo: — ❌
- No LoCoMo benchmark results published.

### LongMemEval: — ❌
- No LongMemEval benchmark results published.

### PersonaMem: — ❌
- No PersonaMem benchmark results published.

### Token reduction: — ❌
- README claims "Greatly reduced token cost: Optimized token usage delivers the same performance with significantly lower LLM overhead" but no quantitative percentage or measurement methodology published.

### Methodology open: true ✅
- arXiv tech report: `https://arxiv.org/abs/2601.06037` (4th version as of 2026-01-22)
- `docs/TeleMem_Tech_Report.pdf` in repo
- Evaluation uses public ZH-4O Chinese multi-character long-dialogue benchmark (from MOOM paper: arXiv:2509.11860)
- Experimental configuration documented: Qwen3-8B (thinking disabled), Qwen3-Embedding-8B, metric = QA accuracy
- Comparison baselines: RAG (62.45%), Mem0 (70.20%), MOOM (72.60%), A-mem (73.78%), Memobase (76.78%), TeleMem (86.33%)
- QA benchmark samples shown in README with exact question/answer format

### Own benchmark (ZH-4O): 86.33% ✅
- `README.md` — Experimental Results table: TeleMem achieves **86.33%** overall QA accuracy on ZH-4O
- "19% higher than Mem0" (Mem0 scored 70.20%)
- Chinese multi-character long-dialogue benchmark, 600 turns average per conversation
- Scenarios: daily interactions, plot progression, evolving character relationships

---

## Multimodal (extra)
TeleMem has unique multimodal capabilities not covered by the standard feature matrix:

- **Video memory**: `add_mm()` — full pipeline: frame extraction → VLM caption generation → FAISS vector database
- **Video QA**: `search_mm()` — ReAct-style reasoning (THINK → ACTION → OBSERVATION) with 3 specialized tools
- **Smart caching**: Skips frame extraction / captioning if outputs already exist
- **Supported VLM**: Qwen3-Omni, GPT-4.1-mini, any OpenAI-compatible VLM
- `telemem/configs.py` — `vlm` config dict with 25+ settings (CLIP_SECS, VIDEO_FPS, GLOBAL_BROWSE_TOPK, etc.)

---

## Claims NOT present (verified absent)

**Architecture:** webUi, proxy, multiAgent, cacheOpt, privacy, export — all ❌ (Python library only; no dashboard, no proxy, no multi-agent, no encryption, no export tool)

**Data Model:** entities, actions, keywords, anticipatedQueries, triggerRules, domainTag, taskType, source, originTrust, emotional, conflict, timeTravel — all ❌ (flat memory model with summary+metadata; character layers exist but no structured entity/action/keyword fields)

**Search:** fulltext, hybrid, deep, codeGraph, docsSearch, factQuery, timeline — all ❌ (pure FAISS vector search; no BM25, no graph/code/doc search, no timeline view)

**Lifecycle:** decay, contradiction, quarantine, autoResolve, trustModel, explicitForget — all ❌ (no forgetting, no contradiction flagging, no trust scores, no delete API)

**Extraction:** qualityRefine, narrative, recurrence — all ❌ (no post-extraction refinement, no story generation, no recurrence detection)

**Platform:** p_claude, p_codex, p_opencode, p_gemini, p_copilot, p_cursor, p_windsurf, p_openclaw, p_hermes, p_pi, p_antigravity — all ❌ (Python library only; no platform-specific integrations)

**Benchmarks:** b_locomo, b_longmemeval, b_personamem, b_token — all ❌ (no standard benchmark results; own ZH-4O benchmark only)

---

## Audit Notes

1. **URL discrepancy**: The user-provided URL `https://github.com/Tele-AI/TeleMem` 404s. The correct URL is `https://github.com/TeleAI-UAGI/telemem`. The org was apparently renamed from `Tele-AI` to `TeleAI-UAGI` and the repo was renamed from `TeleMem` to `telemem`.

2. **Stars**: User stated 461; GitHub API confirms 461 at audit time.

3. **Not a full agent memory system**: TeleMem is a conversation memory library, not a general-purpose agent memory system. It has no MCP server, no hooks, no coding assistant integrations. It's designed for dialogue-based AI (chatbots, roleplay, virtual characters), not for coding agent context management.

4. **Multimodal is unique**: Among the audited systems, TeleMem is the only one with video memory capabilities (frame extraction, captioning, ReAct-style video QA). This is not covered by the standard feature matrix but is a significant differentiator.

5. **Mem0 inheritance**: TeleMem inherits Mem0's API (`from mem0 import *` in `__init__.py`) but then overrides the `Memory` class with `TeleMemory`. The `add()` and `search()` method signatures match Mem0's for drop-in compatibility, but the internal implementation is completely different (FAISS instead of Qdrant, character-aware summarization, LLM-based dedup).

6. **LLM provider count**: The user mentioned "3 documented" — confirmed. Qwen3-8B, MiniMax M2.7, and default OpenAI. Any OpenAI-compatible endpoint technically works, but only 3 are explicitly configured.
