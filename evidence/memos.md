# MemOS — Evidence

> Every ✅ claim backed by public source code or documentation.
> Audit date: 2026-05-28. Source: GitHub `MemTensor/MemOS` main branch, `memos-docs.openmem.net`, arXiv `2507.03724v4`.

## Architecture

### webUi ✅
- `README.md` — "MemOS Dashboard" linked: `https://memos-dashboard.openmem.net/login/`. Cloud-hosted dashboard with API key management, usage monitoring.
- `README.md` (memos-local-plugin 2.0 section) — "full Memory Viewer dashboard" for local plugin.
- `docs: openclaw/guide` — "Visual Configuration UI (Config UI)" from v0.1.12: "built-in local visual configuration service" at `http://127.0.0.1:38463`. Form-based editing, real-time sync, heartbeat monitoring.
- `README.md` (v1.0.0) — "Expanded Playground features" — interactive playground for algorithm performance.

### offline ✅
- `README.md` (Hermes plugin section) — "100% local, zero cloud dependency."
- `README.md` (Local Plugin v1.0.0) — "100% on-device memory with persistent SQLite."
- `README.md` (Self-Hosted) — "Self-Hosted (Local/Private)" deployment via Docker Compose or uvicorn CLI.

### privacy ✅
- `README.md` — "local-first storage" for memos-local-plugin 2.0.
- `README.md` — "100% on-device memory" — all data stays on device with local plugin.
- `README.md` — Self-hosted option (Neo4j + Qdrant) gives full data sovereignty.

### export ❌
- Not found in public documentation or source code. MemDumper component exists in paper (section 5.5.3) but its export functionality is not described as user-facing.

### multiAgent ✅
- `README.md` (OpenClaw Cloud Plugin) — "Multi-agent memory sharing by `user_id`."
- `docs: openclaw/guide` — "Multi-Agent Support & Isolation" section: `agent_id` parameter, `multiAgentMode`, `allowedAgents` whitelist, `agentOverrides` for per-agent configuration (memoryLimitNumber, relativity, knowledgebaseIds). "Ensures complete data isolation between different Agents."
- `README.md` (Hermes plugin) — "multi-agent collaboration."

### llmFlex ✅
- `README.md` — "Supported LLM providers: **OpenAI**, **Azure OpenAI**, **Qwen (DashScope)**, **DeepSeek**, **MiniMax**, **Ollama**, **HuggingFace**, **vLLM**. Set `MOS_CHAT_MODEL_PROVIDER` to select the backend."
- `docs: installation` — `.env` config shows separate provider selection: `MOS_CHAT_MODEL`, `MEMRADER_MODEL`, `MOS_EMBEDDER_BACKEND` (ollama | universal_api), `MOS_RERANKER_BACKEND`. Embedder backend supports Ollama for local models.
- Count: 8 distinct LLM providers documented.

---

## Data Model

### entities ❌
- Not found. No entity extraction or entity-specific data model field in public documentation. The system uses MemCubes as organizational units, not entity-based schemas.

### actions ❌
- Not found. No "action" field or action-tracking metadata in documented schema.

### keywords ❌
- Not found as a named field. `tags` array exists (documented in API search response), but "keywords" as a distinct concept is absent.

### context ✅
- `docs: installation` (search response) — `metadata.background` field: "User expressed a preference for strawberries, indicating a tendency in dietary preferences." Contextual background stored per memory.
- `arXiv 2507.03724v4 §5.4.1` — "Multi-perspective Memory Structuring" for organizing memories with contextual relationships.
- `README.md` (v1.0.0) — "contextual understanding for the tree-structured plaintext memory search interface."

### source ✅
- `docs: installation` (search response) — `metadata.source` field (null in example, but present in schema).
- `docs: installation` (search response) — `metadata.sources` array field (empty `[]` in example, but present).
- `arXiv 2507.03724v4 §4.2` — MemCube includes "provenance" as metadata. "As the basic unit, a MemCube encapsulates both memory content and metadata such as provenance and versioning."

### emotional ❌
- Not found. No emotional tagging, sentiment analysis, or affective dimension in documented schema or features.

### conflict ❌
- Not found. No contradiction detection or conflict resolution mechanism documented.

### layeredMemory ✅
- `README.md` (memos-local-plugin 2.0) — "Self-evolving memory: L1 trace, L2 policy, L3 world model, and crystallized Skills driven by feedback."
- `arXiv 2507.03724v4 §4.1` — Three memory types: **Plaintext Memory** (structured knowledge fragments), **Activation Memory** (contextual inference state / KV-cache), **Parameter Memory** (knowledge in model weights). Unified scheduling across all three.
- `arXiv 2507.03724v4 §5.1` — Three-layer architecture: Memory Interface Layer, Memory Operation Layer, Memory Infrastructure Layer.
- `README.md` (Hermes plugin) — "tiered skill evolution."

### timeTravel ✅
- `arXiv 2507.03724v4 §5.4.3.2` — "Time Machine and Freezing Mechanism" in MemLifecycle component. Enables versioning and temporal snapshots of memory state.
- `arXiv 2507.03724v4 §4.2` — MemCube includes versioning: "metadata such as provenance and versioning."
- `arXiv 2507.03724v4 §5.4.3.1` — "State Modeling and Evolution Logic" in MemLifecycle with lifecycle state tracking.

### schemaFields ✅ (count: ~19)
- `docs: installation` (search response metadata) — Full memory metadata schema: `id`, `memory`, `user_id`, `session_id`, `status` (e.g. "activated"), `type` (e.g. "fact"), `key`, `confidence` (0.99), `source`, `tags`, `visibility`, `updated_at`, `memory_type` (e.g. "UserMemory"), `sources`, `embedding`, `created_at`, `usage` (array of access records), `background`, `relativity` (similarity score), `vector_sync`, `ref_id`.
- Fields explicitly documented: `id`, `memory`, `user_id`, `session_id`, `status`, `type`, `key`, `confidence`, `source`, `tags`, `visibility`, `updated_at`, `memory_type`, `created_at`, `usage`, `background`, `relativity`, `embedding`, `sources`. Total distinct: **19**.

---

## Search & Retrieval

### fulltext ✅
- `README.md` (Hermes plugin) — "Hybrid retrieval (FTS5 + vector)" — SQLite FTS5 for full-text search.
- `docs: openclaw/guide` — "BM25 Search (Lexical Matching): FTS5-based lexical matching. Handles 'exact tokens', such as error codes, function names, or specific IDs."
- `arXiv 2507.03724v4 §5.4.1` — Hybrid retrieval with BM25 component for lexical matching.

### semantic ✅
- `README.md` (Hermes plugin) — "Hybrid retrieval (FTS5 + vector)" — vector component for semantic search.
- `docs: openclaw/guide` — "Vector Search: Cosine Similarity. Captures semantic associations, excels at 'concept matching'."
- `docs: installation` — Embedder configuration: `MOS_EMBEDDER_BACKEND` supports `ollama` and `universal_api`. Vector dimension configurable via `EMBEDDING_DIMENSION`.
- `docs: installation` (search response) — `relativity` field shows cosine similarity score (0.634976...).

### hybrid ✅
- `docs: openclaw/guide` — "Weighted Score Fusion: `Score = (0.7 * VectorScore) + (0.3 * BM25Score)`." Confirmed weighted hybrid retrieval.
- `README.md` — "hybrid-retrieval" in repo description tagline.
- `arXiv 2507.03724v4 §5.4.1` — "Hybrid Retrieval and Dynamic Dispatch" section in MemOperator.

### deep ❌
- Not found. No "deep search" with ±context window expansion documented.

### codeGraph ❌
- Not found. No code graph traversal or call-path analysis. Neo4j is used for memory graph, not source code graphs.

### docsSearch ❌
- Not found. No indexed documentation search feature.

### factQuery ❌
- Not found. No metadata query API (query by entity/action/keyword) documented. Search is content/vector-based.

### timeline ❌
- Not found. No chronological browsing or time-based retrieval mode documented.

### searchModes ✅ (count: 3)
- `docs: openclaw/guide` — Three retrieval engines documented: **Vector Search** (cosine similarity), **BM25 Search** (FTS5 lexical), **Weighted Fusion** (0.7 vector + 0.3 BM25).
- API has single `/product/search` endpoint (REST API) that uses hybrid retrieval. The three modes represent the internal retrieval pipeline stages, all accessible through the unified search endpoint.
- Count: 3 search modes (fulltext/BFTS, semantic/vector, hybrid/fused).

---

## Knowledge Lifecycle

### decay ❌
- Not found. No time-based decay or staleness scoring documented. `status: "activated"` suggests a binary active/inactive model rather than gradual decay.

### supersede ✅
- `README.md` — "Memory Feedback & Correction: Refine memory with natural-language feedback—correcting, supplementing, or replacing existing memories over time."
- `README.md` (v2.0 release) — "Added natural language feedback and correction for memories" — includes replacing existing memories.
- `arxiv 2507.03724v4 §4.2` — MemCube versioning: memories can be composed, migrated, and fused. Versioning enables superseding older memory versions.
- `docs` — MemFeedback module documented in navigation: `/open_source/modules/mem_feedback`.

### contradiction ❌
- Not found. No contradiction detection between memories documented.

### quarantine ❌
- Not found. No quarantine or isolation mechanism for suspect memories.

### autoResolve ❌
- Not found. No automatic task resolution or completion detection.

### trustModel ✅ (partial — confidence scoring)
- `docs: installation` (search response) — `metadata.confidence` field with numeric value (e.g. `0.99`). Per-memory confidence scoring.
- `docs: installation` (search response) — `metadata.status` field (e.g. `"activated"`) suggesting lifecycle state that could influence trust.

### explicitForget ✅
- `README.md` — "Added memory deletion API by memory ID."
- `README.md` — "Added MCP support for memory deletion and feedback."
- `arxiv 2507.03724v4 §5.4.3` — MemLifecycle component: "State Modeling and Evolution Logic" including memory disposal, archiving, and expiration.
- Single memory deletion via `/product/delete` by memory ID; bulk deletion not explicitly documented.

---

## Extraction Pipeline

### autoExtract ✅
- `docs: openclaw/guide` — "Automatically remember all conversations without relying on models to actively log, ensuring no critical information is missed." Plugin intercepts agent conversations.
- `docs: openclaw/guide` — Plugin automatically recalls context before agent starts and saves conversation back to MemOS after agent finishes.
- `arxiv 2507.03724v4 §5.3.1` — MemReader component: "reads and parses input, extracting and normalizing memory cues."
- `arxiv 2507.03724v4 §5.3.3` — Memory Pipeline: automated end-to-end pipeline from ingestion to storage.

### contentPreproc ✅
- `docs: openclaw/guide` — "MemOS can summarize/compress, deduplicate, and archive" — summarization and compression of long tool outputs.
- `arxiv 2507.03724v4 §5.4.1` — "Pipeline Coupling and Caching Strategy" for preprocessing and optimizing memory flow.
- `arxiv 2507.03724v4 §5.5.3` — MemLoader & MemDumper for format transformation and loading.

### dedup ✅
- `README.md` (Hermes plugin) — "smart dedup."
- `docs: openclaw/guide` — "Structured + Deduplicated + High Compression, avoiding 'Long Output Pollution'" — deduplication explicitly listed as core processing step.
- `arxiv 2507.03724v4 §5.4.1` — "Task-Aligned Memory Routing" for avoiding redundant storage.

### qualityRefine ✅
- `README.md` — "Memory Feedback & Correction: Refine memory with natural-language feedback—correcting, supplementing, or replacing existing memories."
- `docs: installation` (search response) — `confidence` scoring (0.99) provides quality metric for retrieval ranking.
- `arxiv 2507.03724v4 §5.4.1` — "Multi-perspective Memory Structuring" for quality organization.

### narrative ❌
- Not found. No narrative generation or storytelling from memory chains documented.

### clustering ❌
- Not found. No automatic memory clustering or topic grouping documented.

### recurrence ❌
- Not found. No recurrence pattern detection documented.

### persona ✅
- `README.md` — "Multi-Modal Memory: Natively supports text, images, tool traces, and **personas**, retrieved and reasoned together in one memory system."
- `arxiv 2507.03724v4 §7.2.3` — "Enabling Personalization and Multi-Role Modeling" — supports persona-based memory selection and role adaptation.
- `arxiv 2507.03724v4 §4.1` — Multi-modal memory explicitly includes personas as a supported modality.

---

## Platform Support

### p_claude ✅
- `GitHub topics` — "claude" tag on repository.
- `arxiv 2507.03724v4 §1` — Claude referenced as existing memory system for comparison: "Although tools like ChatGPT and Claude now offer memory."

### p_codex ❌
- Not found. No Codex CLI integration documented.

### p_opencode ❌
- Not found. No OpenCode integration documented.

### p_gemini ❌
- Not found. No Gemini CLI integration documented.

### p_copilot ❌
- Not found. No GitHub Copilot integration documented.

### p_cursor ❌
- Not found. Cursor IDE integration not documented.

### p_windsurf ❌
- Not found. No Windsurf IDE integration documented.

### p_openclaw ✅
- `README.md` (header) — "Your lobsters and Hermes Agents now have the best memory system." + dedicated OpenClaw sections.
- `docs: openclaw/guide` — Full OpenClaw Cloud Plugin installation guide: `openclaw plugins install @memtensor/memos-cloud-openclaw-plugin@latest`.
- `docs: openclaw/local_plugin` — Local plugin for OpenClaw with "local-first long-term memory, three-tier retrieval, skill crystallization, and an observable management panel."
- NPM packages: `@memtensor/memos-cloud-openclaw-plugin`, `@memtensor/memos-local-plugin`.

### p_hermes ✅
- `README.md` (header) — "Your lobsters and Hermes Agents now have the best memory system."
- `README.md` (memos-local-plugin 2.0) — "One local-first memory core for **Hermes Agent** and **OpenClaw**."
- `README.md` (Hermes plugin launch) — "MemOS Hermes Agent Local Plugin Official Hermes Agent memory plugins launched."
- NPM package: `@memtensor/memos-local-plugin`.

### p_pi ❌
- Not found. No Pi AI integration documented.

### p_antigravity ❌
- Not found. No Antigravity IDE integration documented.

### Additional platform integrations (not in checklist):
- **Coze**: `docs` — "Configuring Memos MCP in Coze Space" — MCP integration for Coze agent framework.
- **Dify**: `docs` — "One-click integration with Coze, Dify, and other Agent frameworks via MCP or SDK."
- **MCP**: Universal MCP support for any MCP-compatible agent framework.

---

## Benchmarks

### b_locomo ✅
- `README.md` (hero banner) — "LoCoMo 75.80."
- `arxiv 2507.03724v4 §6.1` — "End-to-End Evaluation on Long Context Memory" — Table 3 with LoCoMo benchmark results. MemOS-1031 achieves highest overall mean LLM judge score.
- `arxiv 2507.03724v4 Figure 1` — "MemOS (MemOS-1031) consistently ranks first" on LoCoMo, significantly outperforming MIRIX, Mem0, Zep, Memobase, MemU, Supermemory.

### b_longmemeval ✅
- `README.md` (hero banner) — "LongMemEval +40.43%."
- `arxiv 2507.03724v4 §6.1` — Table 4 with LongMemEval results. LongMemEval evaluates long-context memory retention.
- `README.md` (v1.0.0 release) — "Added LongMemEval evaluation results and scripts."

### b_personamem ✅
- `README.md` (hero banner) — "PersonaMem +40.75%."
- `arxiv 2507.03724v4 §6.2` — "End-to-End Evaluation on Personalization and Preference Understanding" — Table 5/6 with PersonaMem precision scores.
- `arxiv 2507.03724v4 Figure 1` — PersonaMem results shown in comparison bar chart.

### b_token ✅
- `README.md` (hero banner) — "Saves 35.24% Memory Tokens."
- `README.md` (repo description) — "35.24% token savings."
- `docs: openclaw/guide` — "Reduces token usage by 72%." (plugin-specific, not the 35.24% system-level figure).

### b_methodology ✅
- `arxiv 2507.03724v4 §6` — Full evaluation section (sections 6.1–6.5) covering: end-to-end long context memory, personalization/preference, chunk sizes and Top-K selection, memory retrieval robustness, KV-based memory acceleration.
- `arxiv 2507.03724v4 §6.3` — Ablation studies: chunk size and Top-K selection evaluation.
- `arxiv 2507.03724v4 §6.4` — Robustness evaluation of memory retrieval.
- Benchmarks compared against: MIRIX, Mem0, Zep, Memobase, MemU, Supermemory, OpenAI Memory.
- Evaluation scripts available in `/evaluation` directory of repository.

### Additional benchmarks (not in checklist):
- **PrefEval-10**: `README.md` (hero banner) — "PrefEval-10 +2568%." Preference evaluation benchmark results.
- **Memory Retrieval Robustness**: `arxiv 2507.03724v4 §6.4` — Dedicated robustness evaluation.
- **KV-Based Memory Acceleration**: `arxiv 2507.03724v4 §6.5` — KV-cache memory acceleration evaluation.

---

## Metadata

- **Description**: "Self-evolving memory OS for LLM & AI Agents: ultra-persistent memory, hybrid-retrieval, and cross-task skill reuse, with 35.24% token savings"
- **Deployment**: Docker Compose (Neo4j + Qdrant + Redis), uvicorn CLI, pip install (`MemoryOS[all]`), Cloud API (hosted SaaS with dashboard)
- **Storage**: Neo4j (graph DB — primary memory store), Qdrant (vector DB), SQLite (local plugin), Redis Streams (task scheduling/queue)
- **Integration**: REST API (`/product/add`, `/product/search`, `/product/delete`), MCP protocol, OpenClaw plugin (NPM), Hermes Agent plugin (NPM), Coze, Dify, SDK (Python `memos` package)
- **Setup**: `git clone && docker compose up` or `pip install MemoryOS[all] && uvicorn memos.api.server_api:app` or cloud dashboard signup
- **License**: Apache 2.0
- **Created**: 2025-07-04 (arXiv paper); 2025-07-07 (v1.0 "Stellar" Preview Release)
- **Docs URL**: https://memos-docs.openmem.net/
- **Repository**: https://github.com/MemTensor/MemOS
- **Stars**: ~9,442 (at audit time)
- **Language**: TypeScript 57.6%, Python 35.2%, HTML 4.3%, JavaScript 1.5%
- **ArXiv**: https://arxiv.org/abs/2507.03724 (long version, 36 pages), https://arxiv.org/abs/2505.22101 (short version)
- **Website**: https://memos.openmem.net/
