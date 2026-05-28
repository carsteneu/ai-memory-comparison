# MSA (Memory Sparse Attention) — Evidence & Classification

> Audit date: 2026-05-28. Source: GitHub `EverMind-AI/MSA` main branch, arXiv 2603.23516.
> **Stars:** ~3,456 | **Language:** Python (98.4%), Shell (1.6%) | **License:** MIT

---

## VERDICT: NOT AN AGENT-MEMORY SYSTEM — DO NOT ADD TO COMPARISON

**MSA is a neural architecture / attention mechanism**, not an agent-memory system. It modifies transformer attention internals to handle ultra-long contexts (up to 100M tokens). It is end-to-end trainable (158.95B tokens of continuous pretraining + SFT), meaning it is baked into model weights — it is not an external tool, API, or integration that agents plug into.

### What MSA actually is:

1. **A sparse attention mechanism** — modifies how transformer layers attend to tokens, using top-k document selection + document-wise RoPE for O(L) complexity scaling from 16K→100M tokens.
2. **A model architecture** — replaces standard attention in a Qwen3-4B backbone. The result is a model you download and run (MSA-4B on HuggingFace), not a memory system you integrate.
3. **Latent-state memory** — the "memory" in MSA refers to compressed KV caches (chunk-mean pooled K/V/Kr), stored as latent vectors within a single forward pass. There is no persistent memory across sessions.
4. **A research project** — published as an arXiv paper with benchmark results on QA/NIAH tasks. The repo is model code + evaluation scripts, not a deployable memory service.

### Key differentiators from agent-memory:

| Aspect | Agent-Memory (e.g., Mem0, YesMem) | MSA |
|--------|-----------------------------------|-----|
| **Memory persistence** | Across sessions, days, months | Within a single forward pass |
| **Integration** | MCP, SDK, API, hooks | Model weights (download + run) |
| **Storage** | SQLite, Vector DB, etc. | GPU VRAM (KV cache) |
| **Retrieval** | Search APIs (semantic, full-text) | Attention-based routing (cosine sim) |
| **User-visible data model** | Entities, actions, keywords, etc. | Latent vectors (no structured fields) |
| **Deployment** | Service or library alongside agent | Model file loaded into GPU |
| **Benchmarks** | LoCoMo, LongMemEval (retrieval) | MS MARCO, NQ, NIAH (QA/comprehension) |
| **Lifecycle** | Decay, forget, supersede, etc. | N/A — stateless per forward pass |

### Why it's confusing:

- **Same org as EverOS**: EverMind-AI builds both MSA (the attention mechanism) and EverOS (the agent-memory system). MSA could theoretically power the retrieval in EverOS, but MSA itself is not the memory system.
- **The word "Memory" in the name**: "Memory Sparse Attention" refers to latent memory states in the attention mechanism, not agent-accessible memory storage.
- **3,456 stars**: The repo gained significant attention as a long-context research breakthrough, not as a developer tool.

---

## Feature Matrix (all default to ❌ — not applicable)

### Architecture

| Feature | Present? | Evidence |
|---------|----------|----------|
| webUi | ❌ | No web UI. Repo contains model code + benchmark scripts only. |
| offline | ❌ | N/A — runs locally as a model, but not an agent tool. Requires 2×A800 GPUs for 100M-token inference. |
| privacy | ❌ | N/A — model architecture, not a deployment concern. |
| export | ❌ | No export feature. |
| multiAgent | ❌ | No multi-agent support. |
| llmFlex | ❌ | Tied to Qwen3-4B backbone. Architecture is backbone-agnostic in theory but only Qwen3-4B weights are published. |

### Data Model

| Feature | Present? | Evidence |
|---------|----------|----------|
| entities | ❌ | No entity extraction. |
| actions | ❌ | No action storage. |
| keywords | ❌ | No keyword/tag system. |
| context | ❌ | No context/why field. |
| source | ❌ | No source attribution. |
| emotional | ❌ | No emotional tracking. |
| conflict | ❌ | No contradiction detection. |
| layeredMemory | ❌ | Has latent-state memory (document-wise KV compression) but this is a model-internal representation, not user-visible layered memory. |
| timeTravel | ❌ | No temporal replay. |
| schemaFields | 0 | No structured memory fields — everything is latent vectors. |

### Search & Retrieval

| Feature | Present? | Evidence |
|---------|----------|----------|
| fulltext | ❌ | No text search API. Retrieval is attention-based (cosine similarity between query projection Qr and document key Kr). |
| semantic | ❌ | Uses cosine similarity for routing within attention, but this is not a semantic search API accessible to users/agents. |
| hybrid | ❌ | No hybrid search. |
| deep | ❌ | No deep search. |
| codeGraph | ❌ | No code graph indexing. |
| docsSearch | ❌ | No documentation search. |
| factQuery | ❌ | No fact querying. |
| timeline | ❌ | No timeline view. |
| searchModes | 0 | No search modes. Retrieval is a single pathway: compute Qr, match with Kr, select top-k documents. |

### Knowledge Lifecycle

| Feature | Present? | Evidence |
|---------|----------|----------|
| decay | ❌ | No decay mechanism. Latent states are computed fresh on each forward pass. |
| supersede | ❌ | No supersede mechanism. |
| contradiction | ❌ | No contradiction detection. |
| quarantine | ❌ | No quarantine. |
| autoResolve | ❌ | No auto-resolution. |
| trustModel | ❌ | No trust model. |
| explicitForget | ❌ | No forget mechanism. Memory is ephemeral per forward pass. |

### Extraction Pipeline

| Feature | Present? | Evidence |
|---------|----------|----------|
| autoExtract | ❌ | No extraction pipeline. The "memory" is latent KV states computed during forward pass, not extracted from conversation. |
| contentPreproc | ❌ | No content-aware preprocessing. |
| dedup | ❌ | No deduplication. |
| qualityRefine | ❌ | No quality refinement. |
| narrative | ❌ | No narrative generation. |
| clustering | ❌ | No clustering of memories. |
| recurrence | ❌ | No recurrence detection. |
| persona | ❌ | No persona extraction. |

### Platform Support

All ❌ — MSA is a model (weights + inference code), not a tool that integrates with coding agents. It has no MCP server, no hooks, no SDK, no API.

### Benchmarks

| Feature | Present? | Evidence |
|---------|----------|----------|
| b_locomo | ❌ | Not evaluated on LoCoMo. Benchmarks are QA datasets: MS MARCO, Natural Questions, DuReader, TriviaQA, NarrativeQA, PopQA, 2WikiMultiHopQA, HotpotQA, MuSiQue. |
| b_longmemeval | ❌ | Not evaluated on LongMemEval. |
| b_personamem | ❌ | Not evaluated on PersonaMem. |
| b_token | ⚠️ | Claims 100M-token context on 2×A800 GPUs, but this is about model context length — not token reduction for agent memory. Not comparable to TencentDB-AM's 61% or Memori's 95% fewer tokens. |
| b_methodology | ✅ | Full arXiv paper (2603.23516) with methodology, ablations, and open-source code. Training: 158.95B-token continuous pretraining + two-stage SFT (8k→64k curriculum). Ablations (paper Table 4) document contribution of each component. |

---

## Recommendation

**Do NOT add MSA to the ai-memory-comparison table.** Including it would be misleading — it would imply it's a competing agent-memory system when it is fundamentally a different category of technology (neural architecture vs. memory middleware).

If desired, MSA could be mentioned in a separate section or footnote about "Related Technologies" or "Underlying Architectures," noting that some agent-memory systems (potentially EverOS) may use MSA-like attention internally. But placing MSA alongside Mem0, YesMem, ByteRover, etc. would misrepresent what it is and confuse readers comparing agent-memory systems.

### If referenced at all:

> **MSA (Memory Sparse Attention)** by EverMind-AI is a neural attention architecture for extending LLM context windows to 100M tokens. It is not an agent-memory system — it modifies transformer internals, not external memory storage. It could potentially power the retrieval backend of an agent-memory system (e.g., EverOS from the same organization), but MSA itself is model infrastructure, not a memory product.

---

## Source References

- [GitHub: EverMind-AI/MSA](https://github.com/EverMind-AI/MSA) — README, QUICK_START.md, source tree
- [arXiv: 2603.23516](https://arxiv.org/abs/2603.23516) — MSA paper
- [HuggingFace: MSA-4B](https://huggingface.co/EverMind-AI/MSA-4B) — Model weights
- [HuggingFace: MSA-RAG-BENCHMARKS](https://huggingface.co/datasets/EverMind-AI/MSA-RAG-BENCHMARKS) — Benchmark data
- [evermind.ai](https://evermind.ai/) — Organization homepage
