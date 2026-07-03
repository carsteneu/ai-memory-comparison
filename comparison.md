# AI Memory Systems — Feature-Level Comparison

> **Open-source fact table.** Every claim links to public README, docs, or source.
> Corrections via PR welcome. No affiliation with any listed project.

**Last updated:** 2026-07-03  
**Systems:** 77  
**Live:** [carsteneu.github.io/ai-memory-comparison](https://carsteneu.github.io/ai-memory-comparison/)

---

## Systems Overview

| System | Stars | Lang | License | Created | Description |
|---|---:|---|---|---|---|
| [context-keeper](https://github.com/jarmstrong158/context-keeper) | ? | Python | MIT | 2026-04-01 | MCP server for project memory — structured decisions, pipelines, constraints with schema-enforced rationale, lexical+semantic hybrid retrieval |
| [fidelis](https://github.com/hermes-labs-ai/fidelis) | 1 | Python | MIT | 2026-03 | Non-LLM agent memory, BM25 + rerank, 83.2% R@1 on LongMemEval-S, depends on mem0 |
| [slowave](https://github.com/mrsalty/slowave) | 1 | Python | AGPL-3.0 | 2026-06-08 | Zero-LLM shared local memory layer — one private memory across Claude Code, Cursor, Cline, Windsurf |
| [Somnigraph](https://github.com/AlexisOlson/somnigraph) | 2 | Python | Apache-2.0 + CC | 2026-03-07 | Research-driven persistent memory — SQLite+vec+FTS5 hybrid retrieval, LightGBM reranker, biological decay, NREM/REM sleep consolidation |
| [MarsNMe](https://github.com/marsmanleo/MarsNMe) | 5 | JavaScript | MIT | 2026-03 | MCP memory gateway, own Supabase, TTL decay, supersede chains, 5+ platforms |
| [Midas](https://github.com/vornicx/Midas) | 6 | Python + TS | MIT | 2026-06-04 | Local-first, eval-first memory — no LLM at ingest or query, $0 API, source-traceable recall |
| [Kage](https://github.com/kage-core/Kage) | 6 | TypeScript | GPL-3.0-only | 2026-05 | Verified memory for coding agents — every memory is checked against the code it cites |
| [gitmem](https://github.com/gitmem-dev/gitmem) | 8 | TypeScript | MIT | 2026-04 | MCP server, BM25+semantic, 17 schema fields, keywords, local-first |
| [VIR](https://github.com/djolex999/vir) | 15 | TypeScript | MIT | 2026-04 | Obsidian-native LLM Wiki: retroactive Claude Code session distillation, MCP+CLI daemon, confidence-scored markdown notes |
| [Fullerenes](https://github.com/codebreaker77/Fullerenes) | 19 | TypeScript | MIT | 2026-04-25 | Zero-LLM Tree-sitter code graph, blast radius analysis, 64% SWE-bench token reduction |
| [YesMem](https://github.com/carsteneu/yesmem) | 23 | Go | Apache 2.0 | 2026-04-09 | Project continuity layer with deepest data model and proxy collapse |
| [Origin](https://github.com/7xuanlu/origin) | 31 | Rust | Apache 2.0 | 2026-04-19 | Local-first Rust daemon with git-versioned memories, distilled wiki pages, and knowledge graph |
| [Continuity v2](https://github.com/Haustorium12/continuity-v2) | 32 | Python | MIT | 2026-04 | SSE proxy for Claude Code, FTS5+ANN search, compaction hooks, thread recall via BFS graph |
| [Noosphere](https://github.com/SweetSophia/noosphere) | 53 | TypeScript | MIT | 2026-04-11 | Universal wiki + memory layer, multi-provider recall orchestration, conflict resolution, promotion pipeline, Obsidian sync |
| [second-brain](https://github.com/rahilp/second-brain-cloudflare) | 91 | TypeScript | MIT | 2026-05-17 | Serverless Cloudflare memory, time-decay reranking, smart merge LLM, one-click deploy |
| [Jumbo](https://github.com/jumbocontext/jumbo.cli) | 102 | TypeScript | AGPL-3.0 | 2025-12-05 | Goal-driven memory system that serves the right context at the right time |
| [CommonGround](https://github.com/Intelligent-Internet/CommonGround) | 141 | TypeScript | MIT | 2025-11 | Shared agent workspace: collaborative memory, pub/sub events, agent directory |
| [Mengram](https://github.com/alibaizhanov/mengram) | 171 | Python | Apache 2.0 | 2026-02-10 | 3-tier memory (semantic/episodic/procedural), 30 MCP tools, experience-driven procedure evolution |
| [omega-memory](https://github.com/omega-memory/omega-memory) | 177 | Python | MIT | 2026-01 | 28-tool multi-agent memory, 5 search modes, all lifecycle features, LongMemEval 76.8% |
| [ClawMem](https://github.com/yoloshii/ClawMem) | 189 | TypeScript | MIT | 2026-02-06 | On-device, hybrid BM25+vector+RRF+cross-encoder, 5+ search modes, conflict detection |
| [shodh-memory](https://github.com/varun29ankuS/shodh-memory) | 226 | Rust | ? | 2025-12-03 | Cognitive: learns from use, forgets irrelevant, TinyBERT NER, RichContext |
| [AIPass](https://github.com/AIOSAI/AIPass) | 227 | Python | MIT | 2026-02 | CLI-native agent workspace, ChromaDB, auto-rollover, no delete |
| [YourMemory](https://github.com/sachitrafa/YourMemory) | 231 | Python | CC BY-NC 4.0 | 2026-03-02 | Self-hosted MCP server, Ebbinghaus forgetting, NER+graph, LoCoMo 59%/LongMemEval 89.4% |
| [ArcRift](https://github.com/Eshaan-Nair/ArcRift) | 242 | TypeScript | MIT | 2026-04-21 | Tauri desktop app + Chrome ext + MCP, hybrid search, KG extraction, codebase indexing |
| [MoltBrain](https://github.com/nhevers/MoltBrain) | 250 | TypeScript | ? | 2026-01-26 | Long-term memory, MoltBook multi-agent, web viewer, ChromaDB |
| [MemLayer](https://github.com/divagr18/memlayer) | 277 | Python | MIT | 2025-11-16 | 3-line LTM for any LLM: hybrid vector+graph, 3 speed tiers, salience gating, offline mode |
| [icarus](https://github.com/esaradev/icarus-memory-infra) | 292 | Python | MIT | 2026-03-24 | Provenance, rollback, 3-layer: working+session+wiki, 23 schema fields |
| [Memory Palace](https://github.com/AGI-is-going-to-arrive/Memory-Palace) | 309 | Python | MIT | 2026-02-19 | Forgetting engine, snapshot rollback, intent-aware search, 4 maintenance engines |
| [Octopoda-OS](https://github.com/RyjoxTechnologies/Octopoda-OS) | 347 | Python | MIT | 2026-04-02 | Memory OS: loop detection, agent messaging, crash recovery, 29 MCP tools |
| [Memora](https://github.com/agentic-box/memora) | 417 | Python | MIT | 2025-11-11 | MCP memory: hybrid RRF, auto-hierarchy, LLM dedup, live graph UI, event-driven multi-agent |
| [memorix](https://github.com/memorix-ai/memorix) | 433 | Python | Apache 2.0 | 2026-02-14 | Generic vector-store SDK wrapping FAISS/Qdrant — NOT agent memory |
| [TeleMem](https://github.com/Tele-AI/TeleMem) | 461 | Python | MIT | 2026-05 | Mem0 drop-in replacement: semantic dedup, multimodal video, multi-user |
| [vestige](https://github.com/samvallad33/vestige) | 575 | Rust | AGPL-3.0 | 2026-01-25 | FSRS-6 spaced repetition, 29 brain modules, 3D dashboard, Rust binary |
| [memoir](https://github.com/zhangfengcdt/memoir) | 585 | Python | Apache-2.0 | 2025-08 | Git-like branch/commit/merge memory, visual explorer, Claude+Codex plugins |
| [context-infra](https://github.com/grapeot/context-infrastructure) | 645 | Python | MIT | 2026-03-16 | Memory + rules + skills + scheduled observations |
| [MemoMind](https://github.com/24kchengYe/MemoMind) | 699 | Python | ? | 2026-03-15 | GPU-accelerated, 4-way hybrid retrieval, 4600+ entities, web dashboard |
| [stash](https://github.com/alash3al/stash) | 720 | Go | Apache 2.0 | 2026-04-24 | Go binary, 8-stage consolidation pipeline, causal link + hypothesis engine |
| [Wax](https://github.com/christopherkarani/Wax) | 767 | Swift | Apache 2.0 | 2026-01-20 | Swift/Metal, Apple Silicon, single-file, sub-ms RAG, EAV entities, hybrid FTS+HNSW |
| [ai-memory](https://github.com/akitaonrails/ai-memory) | 907 | Rust | MIT | 2026-05-21 | Git-versioned markdown wiki, zero LLM mode, cross-agent handoffs |
| [LightMem](https://github.com/zjunlp/LightMem) | 952 | Python | MIT | 2025-05 | ICLR 2026: lightweight memory-augmented generation with adaptive gating |
| [opencode-mem](https://github.com/tickernelz/opencode-mem) | 1016 | TypeScript | ? | 2026-01-10 | OpenCode plugin, local vector DB, dashboard, dedup, persona extraction |
| [token-savior](https://github.com/Mibayy/token-savior) | 1034 | Python | MIT | 2026-03-30 | FTS5+vector hybrid RRF, Tree-sitter code graph, Thompson-sampled persona lattice |
| [mem9](https://github.com/mem9-ai/mem9) | 1162 | TypeScript | Apache 2.0 | 2026-01 | TiDB Cloud backed, hybrid search, multi-agent spaces, conflict resolution, 6 platforms |
| [nocturne](https://github.com/Dataojitori/nocturne_memory) | 1251 | Python | MIT | 2025-12-25 | Rollbackable, visual LTM for MCP agents, no vector RAG, 9 MCP clients |
| [LangMem](https://github.com/langchain-ai/langmem) | 1535 | Python | MIT | 2025-02 | LangChain memory toolkit — library only, no CLI/plugin, requires API keys |
| [memanto](https://github.com/moorcheh-ai/memanto) | 1571 | Python | MIT | 2026-03 | Vector-only (no graph), 13 memory types, 5 search modes, LoCoMo 87.1% SOTA |
| [memsearch](https://github.com/zilliztech/memsearch) | 1861 | Python | Apache 2.0 | 2025-08 | Cross-platform semantic memory: hybrid RRF, SHA-256 dedup, 3-layer progressive recall, ONNX bge-m3 |
| [mcp-memory-service](https://github.com/doobidoo/mcp-memory-service) | 1901 | Python | Apache 2.0 | 2024-12-26 | Persistent memory for AI agent pipelines, REST API + MCP + knowledge graph + auto-consolidation |
| [obsidian-mind](https://github.com/breferrari/obsidian-mind) | 3204 | TypeScript | MIT | 2026-02-28 | Obsidian vault template, markdown-native memory, QMD hybrid RRF search |
| [MemMachine](https://github.com/MemMachine/MemMachine) | 3235 | Python | Apache 2.0 | 2025-08 | Agentic retrieval with ChainOfQueryAgent multi-hop, 3-layer memory, Neo4j+PG |
| [MIRIX](https://github.com/MIRIX-AI/MIRIX) | 3551 | Python | MIT | 2025-09 | 6-type memory architecture, LoCoMo 85.38% SOTA, 99.9% storage reduction, best extraction pipeline |
| [Acontext](https://github.com/memodb-io/Acontext) | 3564 | JS/TS/Go/Python | Apache-2.0 | 2025-10 | Agent Skills as a Memory Layer — auto-captures learnings as Markdown skill files, progressive disclosure retrieval |
| [MemoryBear](https://github.com/Suanmo/MemoryBear) | 4167 | Python | Apache 2.0 | 2025-06 | Bio-inspired 6-engine memory: perception, graph, hybrid search, Ebbinghaus forgetting, reflection |
| [OpenMemory](https://github.com/CaviraOSS/OpenMemory) | 4294 | Python | Apache 2.0 | 2025-10 | HMD v2 cognitive engine: 5-sector decay, temporal KG, waypoint graph, document ingestion |
| [m_flow](https://github.com/FlowElement-ai/m_flow) | 4412 | Python | Apache 2.0 | 2026-02 | Bio-inspired Graph RAG, 4-layer cone, graph-routed path-cost search, LoCoMo 81.8% #1 |
| [memory-lancedb-pro](https://github.com/CortexReach/memory-lancedb-pro) | 4444 | TypeScript | MIT | 2025-11 | LanceDB plugin: 6-stage hybrid pipeline, Weibull decay, dreaming sidecar, multi-scope |
| [TencentDB-AM](https://github.com/Tencent/TencentDB-Agent-Memory) | 4506 | TypeScript | MIT | 2026-04-07 | Mermaid symbolic memory, L0→L3 pyramid, 61% token reduction |
| [engram](https://github.com/Gentleman-Programming/engram) | 4845 | Go | MIT | 2026-02-16 | Go binary agent memory with conflict surfacing and TUI |
| [ByteRover](https://github.com/campfirein/byterover-cli) | 4899 | TypeScript | Elastic 2.0 | 2025-06-19 | Context tree with git-like VC, strongest benchmarks (LoCoMo 96.1) |
| [Honcho](https://github.com/plastic-labs/honcho) | 5713 | Python | AGPL-3.0 | 2024-04 | Memory library for stateful agents, theory-of-mind reasoning, multi-agent capable |
| [MemOS](https://github.com/MemTensor/MemOS) | 10084 | Python | Apache 2.0 | 2025-10 | Self-evolving memory OS, L1/L2/L3, MemCubes, time machine, strong benchmarks |
| [EverOS](https://github.com/EverMind-AI/EverOS) | 10104 | Python | Apache 2.0 | 2025-10-28 | Self-evolving agent memory with evaluation framework |
| [memU](https://github.com/NevaMind-AI/memU) | 13700 | Python | MIT | 2025-09 | Always-on memory for 24/7 proactive agents, 3-tier layered, LoCoMo 92.09%, 5 modality preprocessing |
| [Memori](https://github.com/MemoriLabs/Memori) | 15526 | Python | Apache 2.0 | 2025-07-24 | Agent-native memory (captures execution, not just conversation) |
| [Memvid](https://github.com/memvid/memvid) | 15706 | Rust | Apache 2.0 | 2025-05-27 | Single-file memory (.mv2) with Smart Frames and time-travel |
| [hindsight](https://github.com/vectorize-io/hindsight) | 17917 | Python | MIT | 2025-10 | Self-improving agentic memory, 91.4% LongMemEval, reflect engine, web dashboard |
| [Letta](https://github.com/letta-ai/letta) | 23632 | Python | Apache-2.0 | 2023-10 | Stateful agent platform, 3-tier memory (core/recall/archival), sleep-time dreaming |
| [agentmemory](https://github.com/rohitg00/agentmemory) | 24492 | TypeScript | Apache 2.0 | 2026-02-25 | 53 MCP tools, 12 hooks, 4-tier lifecycle, 3-way RRF, pi native |
| [gbrain](https://github.com/garrytan/gbrain) | 24883 | TypeScript | MIT | 2025-07 | Garry Tan's production agent brain: zero-LLM KG, gap-aware synthesis, PGLite, dream cycle |
| [OpenViking](https://github.com/volcengine/OpenViking) | 26281 | Python | AGPL-3.0 | 2026-01-05 | ByteDance context DB, filesystem paradigm, L0/L1/L2 tiers, LoCoMo 82% |
| [Cognee](https://github.com/topoteretes/cognee) | 26687 | Python | Apache 2.0 | 2023-08-16 | Memory control plane with remember/recall/forget/improve API |
| [Supermemory](https://github.com/supermemoryai/supermemory) | 28127 | TypeScript | MIT | 2024 | Cloud memory API, hybrid RAG+Memory, #1 benchmarks, Chrome ext+MCP+plugins |
| [Graphiti](https://github.com/getzep/graphiti) | 28310 | Python | Apache 2.0 | 2024-08-08 | Temporal knowledge graph engine (powers Zep) |
| [Nanobot](https://github.com/HKUDS/nanobot) | 44974 | Python | MIT | 2025-05 | 43.3k star AI agent framework — Dream is one subsystem, NOT dedicated memory |
| [MemPalace](https://github.com/MemPalace/mempalace) | 56903 | Python | MIT | 2026-04-05 | Verbatim storage, palace metaphor, 96.6% LongMemEval raw retrieval |
| [Mem0](https://github.com/mem0ai/mem0) | 59994 | Python | Apache 2.0 | 2023-06-20 | Memory-as-a-Service platform with best published benchmarks |
| [claude-mem](https://github.com/thedotmack/claude-mem) | 85588 | TypeScript | Apache 2.0 | 2025-08-31 | Hooks-based observation capture with progressive disclosure |

---

## Vital Signs

| System | Stars | Language | License | Single binary | Created | Coverage |
| --- | --- | --- | --- | --- | --- | --- |
| context-keeper | 0 | Python | MIT | — | 2026-04-01 | 43% |
| fidelis | 1 | Python | MIT | — | 2026-03 | 10% |
| slowave | 1 | Python | AGPL-3.0 | — | 2026-06-08 | 38% |
| Somnigraph | 2 | Python | Apache-2.0 + CC | — | 2026-03-07 | 42% |
| MarsNMe | 5 | JavaScript | MIT | — | 2026-03 | 25% |
| Midas | 6 | Python + TS | MIT | — | 2026-06-04 | 40% |
| Kage | 6 | TypeScript | GPL-3.0-only | — | 2026-05 | 67% |
| gitmem | 8 | TypeScript | MIT | — | 2026-04 | 17% |
| VIR | 15 | TypeScript | MIT | — | 2026-04 | 35% |
| Fullerenes | 19 | TypeScript | MIT | — | 2026-04-25 | 15% |
| YesMem | 23 | Go | Apache 2.0 | ✅ | 2026-04-09 | 87% |
| Origin | 31 | Rust | Apache 2.0 | — | 2026-04-19 | 63% |
| Continuity v2 | 32 | Python | MIT | — | 2026-04 | 13% |
| Noosphere | 53 | TypeScript | MIT | — | 2026-04-11 | 43% |
| second-brain | 91 | TypeScript | MIT | — | 2026-05-17 | 23% |
| Jumbo | 102 | TypeScript | AGPL-3.0 | — | 2025-12-05 | 58% |
| CommonGround | 141 | TypeScript | MIT | — | 2025-11 | 8% |
| Mengram | 171 | Python | Apache 2.0 | — | 2026-02-10 | 37% |
| omega-memory | 177 | Python | MIT | — | 2026-01 | 43% |
| ClawMem | 189 | TypeScript | MIT | — | 2026-02-06 | 38% |
| shodh-memory | 226 | Rust | ? | ✅ | 2025-12-03 | 32% |
| AIPass | 227 | Python | MIT | — | 2026-02 | 28% |
| YourMemory | 231 | Python | CC BY-NC 4.0 | — | 2026-03-02 | 28% |
| ArcRift | 242 | TypeScript | MIT | — | 2026-04-21 | 32% |
| MoltBrain | 250 | TypeScript | ? | — | 2026-01-26 | 20% |
| MemLayer | 277 | Python | MIT | — | 2025-11-16 | 15% |
| icarus | 292 | Python | MIT | — | 2026-03-24 | 18% |
| Memory Palace | 309 | Python | MIT | — | 2026-02-19 | 33% |
| Octopoda-OS | 347 | Python | MIT | — | 2026-04-02 | 15% |
| Memora | 417 | Python | MIT | — | 2025-11-11 | 27% |
| memorix | 433 | Python | Apache 2.0 | — | 2026-02-14 | 7% |
| TeleMem | 461 | Python | MIT | — | 2026-05 | 7% |
| vestige | 575 | Rust | AGPL-3.0 | ✅ | 2026-01-25 | 35% |
| memoir | 585 | Python | Apache-2.0 | — | 2025-08 | 18% |
| context-infra | 645 | Python | MIT | — | 2026-03-16 | 23% |
| MemoMind | 699 | Python | ? | — | 2026-03-15 | 23% |
| stash | 720 | Go | Apache 2.0 | ✅ | 2026-04-24 | 33% |
| Wax | 767 | Swift | Apache 2.0 | ✅ | 2026-01-20 | 17% |
| ai-memory | 907 | Rust | MIT | ✅ | 2026-05-21 | 32% |
| LightMem | 952 | Python | MIT | — | 2025-05 | 3% |
| opencode-mem | 1016 | TypeScript | ? | — | 2026-01-10 | 15% |
| token-savior | 1034 | Python | MIT | — | 2026-03-30 | 28% |
| mem9 | 1162 | TypeScript | Apache 2.0 | — | 2026-01 | 33% |
| nocturne | 1251 | Python | MIT | — | 2025-12-25 | 23% |
| LangMem | 1535 | Python | MIT | — | 2025-02 | 3% |
| memanto | 1571 | Python | MIT | — | 2026-03 | 28% |
| memsearch | 1861 | Python | Apache 2.0 | — | 2025-08 | 18% |
| mcp-memory-service | 1901 | Python | Apache 2.0 | — | 2024-12-26 | 68% |
| obsidian-mind | 3204 | TypeScript | MIT | — | 2026-02-28 | 22% |
| MemMachine | 3235 | Python | Apache 2.0 | — | 2025-08 | 32% |
| MIRIX | 3551 | Python | MIT | — | 2025-09 | 40% |
| Acontext | 3564 | JS/TS/Go/Python | Apache-2.0 | — | 2025-10 | 22% |
| MemoryBear | 4167 | Python | Apache 2.0 | — | 2025-06 | 55% |
| OpenMemory | 4294 | Python | Apache 2.0 | — | 2025-10 | 25% |
| m_flow | 4412 | Python | Apache 2.0 | — | 2026-02 | 23% |
| memory-lancedb-pro | 4444 | TypeScript | MIT | — | 2025-11 | 15% |
| TencentDB-AM | 4506 | TypeScript | MIT | — | 2026-04-07 | 17% |
| engram | 4845 | Go | MIT | ✅ | 2026-02-16 | 38% |
| ByteRover | 4899 | TypeScript | Elastic 2.0 | — | 2025-06-19 | 25% |
| Honcho | 5713 | Python | AGPL-3.0 | — | 2024-04 | 18% |
| MemOS | 10084 | Python | Apache 2.0 | — | 2025-10 | 27% |
| EverOS | 10104 | Python | Apache 2.0 | — | 2025-10-28 | 23% |
| memU | 13700 | Python | MIT | — | 2025-09 | 17% |
| Memori | 15526 | Python | Apache 2.0 | — | 2025-07-24 | 15% |
| Memvid | 15706 | Rust | Apache 2.0 | — | 2025-05-27 | 17% |
| hindsight | 17917 | Python | MIT | — | 2025-10 | 20% |
| Letta | 23632 | Python | Apache-2.0 | — | 2023-10 | 20% |
| agentmemory | 24492 | TypeScript | Apache 2.0 | — | 2026-02-25 | 43% |
| gbrain | 24883 | TypeScript | MIT | — | 2025-07 | 35% |
| OpenViking | 26281 | Python | AGPL-3.0 | — | 2026-01-05 | 28% |
| Cognee | 26687 | Python | Apache 2.0 | — | 2023-08-16 | 17% |
| Supermemory | 28127 | TypeScript | MIT | — | 2024 | 47% |
| Graphiti | 28310 | Python | Apache 2.0 | — | 2024-08-08 | 25% |
| Nanobot | 44974 | Python | MIT | — | 2025-05 | 12% |
| MemPalace | 56903 | Python | MIT | — | 2026-04-05 | 15% |
| Mem0 | 59994 | Python | Apache 2.0 | — | 2023-06-20 | 17% |
| claude-mem | 85588 | TypeScript | Apache 2.0 | — | 2025-08-31 | 27% |

---

## Architecture

| System | Deployment | Storage | Integration | Proxy | Web/TUI | Offline | Multi-agent | LLM providers | Cache optimization | Procedural memory | Sandboxed exec | Scheduled/autonomous | Privacy/encrypt | Data export | Setup | Pricing |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| context-keeper | Local / MCP | JSON files (.context/) | MCP | — | — | ✅ | — | 1 | — | — | — | — | ✅ | ✅ | git clone + pip install | free |
| fidelis | MCP server + hooks | BM25+ChromaDB | MCP + hooks | — | — | ✅ | — | 1 | — | — | — | — | ✅ | — | pip install | free |
| slowave | Local CLI / MCP | SQLite | MCP | — | — | ✅ | — | 0 | — | — | — | — | ✅ | ✅ | pipx install slowave | free |
| Somnigraph | Self-host / Local (MCP) | SQLite + sqlite-vec + FTS5 | MCP (FastMCP) | — | — | ✅ | — | 2 | ✅ | — | — | — | ✅ | — | pip install | free |
| MarsNMe | MCP server | Supabase+pgvector | MCP | — | — | — | — | 1 | — | — | — | — | ✅ | — | npm install | free |
| Midas | Library + MCP server | SQLite | MCP, SDK, LangGraph | — | — | ✅ | ✅ | 3 | ✅ | — | — | — | ✅ | — | pip install / npx | free |
| Kage | Local CLI + MCP + plugin | JSON packets in repo (.agent_memory/) | MCP, hooks, CLI | — | ✅ | ✅ | ✅ | 0 | ✅ | — | — | — | ✅ | ✅ | npx -y kage-graph-mcp install | free |
| gitmem | MCP server (npx) | .gitmem/ + Supabase | MCP | — | — | ✅ | — | 1 | — | — | — | — | ✅ | — | npx install | free |
| VIR | Local CLI (npm) | SQLite + Markdown vault | MCP + Hooks + CLI | — | — | ✅ | — | 2 | ✅ | ✅ | — | ✅ | — | ✅ | npm install -g | free |
| Fullerenes | Local CLI + MCP | SQLite (graph.db) | MCP | — | — | ✅ | — | 0 | — | — | — | — | — | — | npm install | free |
| YesMem | Local binary | SQLite+Vector | Proxy+MCP+Hooks | ✅ | — | ✅ | ✅ | 4 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | curl \| bash | free |
| Origin | Local daemon | libSQL+FTS5 | MCP+CC plugin | — | — | ✅ | — | 2 | — | ✅ | — | ✅ | ✅ | ✅ | npx setup | free |
| Continuity v2 | Local proxy+MCP | SQLite+FTS5+sqlite-vec | Proxy+MCP+Hooks | ✅ | — | ✅ | — | 1 | — | — | — | — | — | — | pip install | free |
| Noosphere | Docker Compose (self-host) | PostgreSQL+Redis | Plugin (OpenClaw/Hermes/Opencode/Kilo) + REST API | — | ✅ | ✅ | — | 0 | ✅ | — | — | ✅ | ✅ | ✅ | docker compose up | free |
| second-brain | Cloudflare Workers | D1+Vectorize | MCP | — | ✅ | — | — | 1 | — | — | — | — | ✅ | — | one-click deploy | free |
| Jumbo | Local CLI | Event store + SQLite | CLI + hooks + AGENTS.md | — | ✅ | ✅ | ✅ | 6 | ✅ | ✅ | — | ✅ | ✅ | ✅ | npm install | free |
| CommonGround | Self-hosted | SQLite+Vector | REST+WebSocket | — | ✅ | ✅ | ✅ | 1 | — | — | — | — | — | — | docker compose | free |
| Mengram | Cloud/Self-hosted | PostgreSQL+pgvector | MCP+Hooks | — | — | ✅ | — | 1 | — | ✅ | — | ✅ | — | — | pip install | free |
| omega-memory | Local server | SQLite+Vector | MCP | — | — | ✅ | ✅ | 1 | — | — | — | — | — | — | pip install | free |
| ClawMem | Local server (Bun) | SQLite+FTS5+Vector | Hooks + MCP | — | — | ✅ | — | 1 | — | — | — | — | ✅ | ✅ | bun install | free |
| shodh-memory | Local binary | Tantivy+FTS5+Vector | MCP | — | — | ✅ | ✅ | 1 | — | — | — | — | ✅ | — | cargo install | free |
| AIPass | Local CLI | ChromaDB+JSON | CLI | — | — | ✅ | — | 1 | — | — | — | — | ✅ | ✅ | pip install | free |
| YourMemory | Self-hosted MCP | DuckDB/SQLite+pgvector | MCP | — | — | ✅ | — | 1 | — | — | — | — | ✅ | — | pip install | free |
| ArcRift | Tauri desktop app + Chrome ext + MCP | sqlite-vec+FTS5 | MCP + browser ext + CLI | — | ✅ | ✅ | — | 2 | — | — | — | — | ✅ | — | npx arcrift-setup | free |
| MoltBrain | Plugin | ChromaDB+SQLite | Plugin+MCP | — | ✅ | ✅ | ✅ | 1 | — | — | — | — | ✅ | — | npm install | free |
| MemLayer | Python library | ChromaDB+NetworkX | Library (3 lines) | — | — | ✅ | — | 5 | — | — | — | — | ✅ | — | pip install memlayer | free |
| icarus | Local Python | Markdown wiki + archive | MCP | — | — | ✅ | — | 1 | — | — | — | — | ✅ | — | pip install | free |
| Memory Palace | Docker / local Python | SQLite+sqlite-vec | MCP+Skills | — | ✅ | ✅ | — | 1 | — | — | — | — | — | — | docker compose | free |
| Octopoda-OS | Local server | Key-value store | MCP | — | ✅ | ✅ | — | 1 | — | — | — | — | — | ✅ | pip install | free |
| Memora | MCP server | SQLite+FTS5 | MCP | — | ✅ | ✅ | ✅ | 2 | — | — | — | — | ✅ | — | pip install | free |
| memorix | Python library | FAISS/Qdrant | Python SDK | — | — | ✅ | — | 1 | — | — | — | — | — | — | pip install | free |
| TeleMem | Library | Vector DB | SDK | — | — | ✅ | — | 1 | — | — | — | — | — | — | pip install | free |
| vestige | Local binary (22MB) | SQLite+FTS5 | MCP | — | ✅ | ✅ | — | 1 | — | — | — | — | ✅ | — | cargo install | free |
| memoir | Plugin (Claude Code, Codex) | Hierarchical paths | Plugin+CLI | — | ✅ | ✅ | — | 1 | — | — | — | — | — | — | pip install | free |
| context-infra | Local Python | Markdown files | MCP | — | — | ✅ | — | 1 | ✅ | — | — | — | — | — | setup_guide.md | free |
| MemoMind | Local Python | Local vector DB | MCP | — | ✅ | ✅ | — | 1 | — | — | — | — | — | — | pip install | free |
| stash | Local binary | Postgres+pgvector | MCP | — | — | ✅ | — | 1 | — | — | — | — | — | — | go install | free |
| Wax | Single file (Apple Silicon) | Single file (frame container) | Library+MCP | — | — | ✅ | — | 1 | — | — | — | — | — | — | swift build | free |
| ai-memory | Local binary | Git wiki (md) | MCP+Hooks | — | ✅ | ✅ | — | 1 | — | — | — | — | — | — | ? | free |
| LightMem | Research library | Memory tokens (model) | Library | — | — | ✅ | — | 1 | — | — | — | — | — | — | pip install | free |
| opencode-mem | OpenCode plugin | Local vector DB | Plugin (OpenCode) | — | ✅ | ✅ | — | 1 | — | — | — | — | — | — | npm install | free |
| token-savior | MCP server | SQLite+FTS5+sqlite-vec | MCP | — | ✅ | ✅ | — | 1 | — | — | — | — | — | — | pip install | free |
| mem9 | Cloud/Self-host | TiDB Cloud | MCP+Hooks | — | ✅ | ✅ | ✅ | 3 | — | — | — | — | ✅ | ✅ | npx install | freemium |
| nocturne | Local MCP server | SQLite | MCP | — | ✅ | ✅ | — | 1 | — | — | — | — | — | — | pip install | free |
| LangMem | Library | Pluggable backends | LangChain/LangGraph | — | — | — | — | 1 | — | — | — | — | — | — | pip install | free |
| memanto | Local/Cloud | Vector DB | MCP+SaaS | — | — | ✅ | — | 1 | — | — | — | — | — | — | pip install | freemium |
| memsearch | Local CLI+MCP | Milvus+Markdown | MCP+CLI | — | — | ✅ | — | 9 | — | — | — | — | — | — | pip install | free |
| mcp-memory-service | Local/Docker/Cloudflare | SQLite-vec+Cloudflare+Milvus | REST(76ep)+MCP+OAuth2+CLI | — | ✅ | ✅ | ✅ | 5 | ✅ | — | — | — | ✅ | ✅ | pip install | free |
| obsidian-mind | Obsidian vault + npm | Markdown + QMD/SQLite | CLI + MCP | — | ✅ | ✅ | — | 1 | — | — | — | — | — | — | npm install | free |
| MemMachine | Server+SDK | Neo4j+PostgreSQL+pgvector | MCP+SDK | — | ✅ | ✅ | ✅ | 1 | — | — | — | — | ✅ | — | docker compose | free |
| MIRIX | Self-hosted | PostgreSQL+pgvector | REST API | — | ✅ | ✅ | ✅ | 1 | — | — | — | — | ✅ | — | docker compose | free |
| Acontext | Cloud + Docker self-host | PostgreSQL+pgvector+Redis+RabbitMQ+S3 | SDK+REST | — | ✅ | ✅ | — | 3 | — | — | — | — | ✅ | ✅ | curl \| sh | freemium |
| MemoryBear | Local server | Neo4j+Elasticsearch | REST API+MCP | — | ✅ | ✅ | ✅ | 1 | — | — | — | — | ✅ | ✅ | docker compose | free |
| OpenMemory | Self-hosted | Vector DB | REST API+MCP | — | — | ✅ | — | 1 | — | — | — | — | ✅ | — | docker compose | free |
| m_flow | Local Python | Graph DB | MCP | — | ✅ | ✅ | — | 9 | — | — | — | — | — | — | pip install | free |
| memory-lancedb-pro | OpenClaw plugin | LanceDB | OpenClaw plugin | — | — | ✅ | — | 1 | — | — | — | — | — | — | npm install | free |
| TencentDB-AM | Plugin (OpenClaw) | SQLite+sqlite-vec | Plugin hooks | — | — | ✅ | — | 1 | — | — | — | — | — | — | ? | free |
| engram | Local bin / Cloud (opt-in) | SQLite+FTS5 | MCP+Hooks (19) | — | ✅ | ✅ | — | 2 | — | — | — | — | ✅ | ✅ | brew install | free |
| ByteRover | Local CLI / Cloud | SQLite+Context tree | MCP+REPL | — | ✅ | ✅ | — | 20 | — | — | — | — | — | — | npm install -g | freemium |
| Honcho | Server + SDK | Postgres+pgvector | SDK + REST + MCP | — | ✅ | ✅ | ✅ | 3 | — | — | — | — | — | — | docker compose | free |
| MemOS | Cloud/Self-host | Neo4j+Qdrant+Redis | API+Plugin | — | ✅ | ✅ | — | 1 | — | — | — | — | — | — | docker compose | freemium |
| EverOS | Lib/MCP | Vector DB | MCP | — | — | ✅ | — | 1 | — | — | — | — | — | — | ? | free |
| memU | Library+MCP | Vector DB | MCP+SDK | — | — | ✅ | — | 3 | — | — | — | — | — | — | pip install | free |
| Memori | Cloud / BYODB | Cloud | SDK/MCP | — | ✅ | — | — | 1 | — | — | — | — | — | — | ? | free |
| Memvid | Lib/Local file | Single .mv2 file | SDK | — | — | ✅ | — | 1 | — | — | — | — | — | — | ? | free |
| hindsight | SDK/Cloud | Vector+graph+temporal | Python API+MCP | — | ✅ | ✅ | — | 1 | — | — | — | — | — | — | pip install | freemium |
| Letta | Server + SDK | Postgres + vector + git | SDK + REST | — | ✅ | ✅ | ✅ | 1 | — | — | — | — | — | — | docker compose | free |
| agentmemory | Local server (npm) | SQLite (0 external DBs) | MCP + Hooks (12) | — | ✅ | ✅ | ✅ | 3 | — | — | — | — | ✅ | ✅ | npm install -g | free |
| gbrain | Local (PGLite WASM) | PGLite+pgvector | MCP+Hooks | — | ✅ | ✅ | — | 1 | — | — | — | — | ✅ | — | npx install | free |
| OpenViking | Self-hosted | Context DB (filesystem paradigm) | API | — | ✅ | ✅ | — | 1 | — | — | — | — | ✅ | ✅ | pip install | free |
| Cognee | Lib/Cloud | Graph+Vector | API+Hooks | — | ✅ | ✅ | — | 11 | — | — | — | — | — | — | ? | free |
| Supermemory | Cloud (Cloudflare Workers) | Hyperdrive (PG)+KV+Vector | MCP+API+Plugins | — | ✅ | — | — | 1 | — | — | — | — | — | — | npx install-mcp | freemium |
| Graphiti | Library | Graph DB | Library | — | — | ✅ | — | 1 | — | — | — | — | — | — | ? | free |
| Nanobot | Agent framework | Filesystem | Agent loop | — | — | ✅ | — | 1 | — | — | — | — | ✅ | ✅ | pip install | free |
| MemPalace | Local CLI | ChromaDB (pluggable) | CLI + MCP | — | — | ✅ | — | 1 | — | — | — | — | ✅ | — | uv tool install | free |
| Mem0 | Lib/Self-host/Cloud | Qdrant | API/SDK | — | ✅ | — | — | 16 | — | — | — | — | — | — | pip install | freemium |
| claude-mem | Local CLI | SQLite+Chroma | Hooks (5) | — | ✅ | ✅ | — | 1 | — | ✅ | — | — | ✅ | ✅ | npx install | free |

---

## Data Model

| System | Storage unit | Entities | Actions | Keywords/tags | Anticipated queries | Trigger rules | Domain tag | Task type | Context (why) | Source attribution | Origin + trust | Emotional | Conflict surfacing | Layered memory | Time-travel | Schema fields |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| context-keeper | Entry (decision / pipeline / constraint) | — | ✅ | ✅ | ✅ | ✅ | — | — | ✅ | ✅ | ✅ | — | ✅ | — | ✅ | 13 |
| fidelis | Verbatim passage | — | — | — | — | — | — | — | — | — | — | — | — | — | — | 3 |
| slowave | Memory (episode / prototype / schema) | — | — | — | — | — | ✅ | ✅ | ✅ | — | — | — | ✅ | ✅ | — | 14 |
| Somnigraph | Memory (text row) | — | — | ✅ | — | — | — | — | — | ✅ | ✅ | — | ✅ | ✅ | — | 20 |
| MarsNMe | Memory entry (28 fields) | — | — | — | — | — | — | — | ✅ | ✅ | — | — | ✅ | — | — | 28 |
| Midas | Memory (text record) | — | — | — | — | — | — | — | — | ✅ | ✅ | — | — | — | — | 8 |
| Kage | Memory packet (cited, fingerprinted) | ✅ | — | ✅ | — | ✅ | — | — | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 12 |
| gitmem | Learning entry | — | — | ✅ | — | — | — | — | — | — | — | — | — | — | — | 17 |
| VIR | Typed markdown note (pattern/gotcha/decision/tool) | — | — | — | — | — | — | — | — | ✅ | ✅ | — | ✅ | — | — | 8 |
| Fullerenes | Code symbol node | ✅ | — | — | — | — | — | — | — | — | — | — | — | — | — | 8 |
| YesMem | Learning V2 (structured) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | 51 |
| Origin | Memory + Page | ✅ | — | ✅ | — | — | — | — | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | 40 |
| Continuity v2 | Session entry | — | — | — | — | — | — | — | — | — | — | — | — | — | ✅ | 6 |
| Noosphere | Article (wiki page) | — | — | ✅ | — | — | — | — | ✅ | ✅ | — | — | ✅ | ✅ | ✅ | 15 |
| second-brain | Memory entry (8 fields) | — | — | ✅ | — | — | — | — | — | ✅ | — | — | — | — | — | 8 |
| Jumbo | Memory entity node (11 types) + relation graph edge | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | ✅ | — | — | — | — | ✅ | ✅ | 16 |
| CommonGround | Shared memory entry | — | — | — | — | — | — | — | — | — | — | — | — | — | — | 4 |
| Mengram | Memory (3 tiers, 26 fields) | ✅ | — | ✅ | — | ✅ | — | — | ✅ | — | — | ✅ | — | ✅ | — | 26 |
| omega-memory | Memory entry (15 fields) | — | — | — | — | — | — | — | — | — | — | — | — | — | — | 15 |
| ClawMem | Memory entry (12+ fields) | ✅ | ✅ | ✅ | — | — | — | ✅ | ✅ | ✅ | — | — | ✅ | — | ✅ | 12 |
| shodh-memory | Cognitive entry | ✅ | — | — | — | — | — | — | ✅ | ✅ | — | ✅ | — | ✅ | — | 6 |
| AIPass | Document entry (10 metadata fields) | — | — | — | — | — | — | — | — | — | — | — | — | ✅ | ✅ | 10 |
| YourMemory | Memory entry (12-14 fields) | ✅ | — | ✅ | — | — | — | — | ✅ | — | — | — | — | — | — | 12 |
| ArcRift | Chunk + sentence + graph triple | ✅ | — | ✅ | — | — | — | — | ✅ | — | — | — | — | — | — | 7 |
| MoltBrain | Observation (17 fields) | — | — | — | — | — | — | — | — | — | — | — | — | — | ✅ | 17 |
| MemLayer | Memory fact | ✅ | — | — | — | — | — | — | — | — | — | — | — | — | — | 6 |
| icarus | Working + session + wiki layers | — | — | — | — | — | — | — | — | — | — | — | — | ✅ | ✅ | 23 |
| Memory Palace | Memory entry | — | — | — | — | ✅ | — | — | — | — | — | — | — | ✅ | ✅ | 8 |
| Octopoda-OS | Memory entry | — | — | — | — | — | — | — | — | — | — | — | — | — | — | 5 |
| Memora | Memory entry (hierarchical) | — | — | ✅ | — | — | — | — | — | — | — | — | — | — | — | 8 |
| memorix | Vector entry | — | — | — | — | — | — | — | — | — | — | — | — | — | — | 6 |
| TeleMem | Memory entry | — | — | — | — | — | — | — | — | — | — | — | — | — | — | 7 |
| vestige | Cognitive memory unit | ✅ | — | ✅ | — | — | — | — | — | — | — | — | — | — | — | 5 |
| memoir | Hierarchical memory node | ✅ | — | — | — | — | — | — | — | — | — | — | — | ✅ | ✅ | 5 |
| context-infra | Context entry | — | — | — | — | — | — | — | — | — | — | — | — | ✅ | — | 4 |
| MemoMind | Memory entry | ✅ | — | ✅ | — | — | — | — | — | — | — | — | — | — | — | 6 |
| stash | Episode + Fact + Context | ✅ | — | — | — | — | — | — | ✅ | — | — | — | ✅ | ✅ | — | 7 |
| Wax | Frame entry | ✅ | — | — | — | — | — | — | — | — | — | — | — | — | — | 6 |
| ai-memory | Wiki page (md) | — | — | — | — | — | — | — | — | — | — | — | — | ✅ | ✅ | 10 |
| LightMem | Memory token | — | — | — | — | — | — | — | — | — | — | — | — | — | — | 3 |
| opencode-mem | Vector entry | — | — | — | — | — | — | — | — | ✅ | — | — | — | — | — | 10 |
| token-savior | Observation (18+ fields) | — | — | — | — | — | — | — | — | — | — | — | — | — | — | 14 |
| mem9 | Memory entry (14 fields) | — | — | ✅ | — | — | — | — | — | ✅ | — | — | ✅ | — | — | 14 |
| nocturne | Memory entry | — | — | — | — | ✅ | — | — | — | — | — | — | — | — | ✅ | 5 |
| LangMem | Memory namespace | — | — | — | — | — | — | — | — | — | — | — | — | — | — | 3 |
| memanto | Memory (13 types) | — | — | — | — | — | — | — | — | ✅ | — | — | — | — | ✅ | 6 |
| memsearch | Text chunk (no learning abstraction) | — | — | — | — | — | — | — | — | — | — | — | — | — | — | 9 |
| mcp-memory-service | Memory (text+metadata) | ✅ | — | ✅ | — | — | ✅ | ✅ | ✅ | ✅ | — | ✅ | ✅ | — | ✅ | 28 |
| obsidian-mind | Markdown note (wiki) | — | — | — | — | — | — | — | — | — | — | — | — | — | — | 4 |
| MemMachine | Memory (3 layers) | ✅ | — | — | — | — | — | — | ✅ | ✅ | — | — | — | ✅ | — | 10 |
| MIRIX | Memory (6 types) | ✅ | ✅ | ✅ | — | — | — | — | — | ✅ | — | — | — | ✅ | — | 10 |
| Acontext | Skill file (Markdown) | — | — | — | — | — | — | ✅ | — | — | — | — | — | — | — | 12 |
| MemoryBear | Memory node (12+ fields) | ✅ | — | ✅ | — | — | — | — | ✅ | ✅ | — | ✅ | ✅ | ✅ | ✅ | 12 |
| OpenMemory | Memory (5 sectors) | — | — | — | — | — | — | — | — | — | — | ✅ | — | ✅ | ✅ | 13 |
| m_flow | Graph node (4-layer cone) | ✅ | — | — | — | — | — | — | — | — | — | — | — | ✅ | — | 8 |
| memory-lancedb-pro | Memory entry (L0-L2) | — | — | — | — | — | — | — | — | — | — | — | — | ✅ | — | 17 |
| TencentDB-AM | Atom/Scenario/Persona | — | — | — | — | — | — | — | — | — | — | — | — | ✅ | — | 12 |
| engram | Memory (What/Why/Where/Learned) | — | — | ✅ | — | — | — | — | ✅ | — | — | — | ✅ | — | ✅ | 6 |
| ByteRover | Context node (tree) | — | — | ✅ | — | — | — | — | — | — | — | — | — | — | ✅ | 6 |
| Honcho | User-scoped memory | ✅ | — | — | — | — | — | — | ✅ | — | — | — | — | — | — | 5 |
| MemOS | MemCube | — | — | — | — | — | — | — | — | — | — | — | — | ✅ | ✅ | 19 |
| EverOS | Memory entry | — | — | — | — | — | — | — | — | — | — | — | — | — | — | 8 |
| memU | MemoryItem (3 tiers) | ✅ | — | — | — | — | — | — | — | — | — | — | — | ✅ | — | 8 |
| Memori | Memory entry | — | — | — | — | — | — | — | — | — | — | — | — | — | — | 6 |
| Memvid | Smart Frame | ✅ | — | ✅ | — | — | — | — | — | — | — | — | — | ✅ | ✅ | 9 |
| hindsight | Memory entry | ✅ | — | ✅ | — | — | — | — | ✅ | — | — | — | — | — | ✅ | 7 |
| Letta | Memory block | — | — | — | — | — | — | — | — | — | — | — | — | ✅ | ✅ | 10 |
| agentmemory | Memory entry (structured, confidence-scored) | ✅ | — | — | — | — | — | — | — | — | — | — | — | ✅ | — | 8 |
| gbrain | Memory entry | ✅ | — | — | — | — | — | — | ✅ | ✅ | — | — | ✅ | ✅ | — | 12 |
| OpenViking | Context node (filesystem tree) | — | — | — | — | — | — | — | ✅ | — | — | — | — | ✅ | — | 6 |
| Cognee | Fact (graph+vec) | ✅ | — | — | — | — | — | — | — | — | — | — | — | — | — | 10 |
| Supermemory | Memory entry (versioned, ~23 fields) | ✅ | — | ✅ | — | — | — | — | ✅ | ✅ | — | — | ✅ | ✅ | ✅ | 23 |
| Graphiti | Fact (graph node) | ✅ | — | — | — | — | — | — | — | — | — | — | — | ✅ | ✅ | 8 |
| Nanobot | Dream memory entry | — | — | — | — | — | — | — | ✅ | — | — | — | — | — | ✅ | 7 |
| MemPalace | Verbatim text (no summarization) | ✅ | — | — | — | — | — | — | — | — | — | — | — | — | — | 5 |
| Mem0 | Memory (text) | ✅ | — | — | — | — | — | — | — | — | — | — | — | — | — | 7 |
| claude-mem | Observation (text) | — | — | — | — | — | — | — | — | — | — | — | — | — | — | 4 |

---

## Search & Retrieval

| System | Full-text | Semantic/vector | Hybrid (BM25+Vec) | Deep (incl. thinking) | Code graph | Docs search | Fact metadata query | Timeline view | Search modes | Data sources |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| context-keeper | ✅ | ✅ | ✅ | — | — | — | — | — | 3 | 3 |
| fidelis | ✅ | ✅ | — | — | — | — | — | — | 2 | 1 |
| slowave | ✅ | ✅ | ✅ | — | — | — | — | — | 2 | 2 |
| Somnigraph | ✅ | ✅ | ✅ | — | — | — | ✅ | ✅ | 3 | 1 |
| MarsNMe | — | ✅ | — | — | — | — | — | — | 2 | 5 |
| Midas | ✅ | ✅ | ✅ | — | — | — | ✅ | ✅ | 3 | 1 |
| Kage | ✅ | ✅ | ✅ | — | ✅ | — | ✅ | ✅ | 4 | 3 |
| gitmem | ✅ | ✅ | — | — | — | — | — | — | 2 | 1 |
| VIR | ✅ | ✅ | — | — | — | — | — | ✅ | 3 | 2 |
| Fullerenes | ✅ | — | — | — | ✅ | — | — | — | 9 | 1 |
| YesMem | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 9 | 4 |
| Origin | ✅ | ✅ | ✅ | — | — | — | ✅ | ✅ | 3 | 3 |
| Continuity v2 | ✅ | ✅ | — | — | — | — | — | — | 2 | 2 |
| Noosphere | ✅ | — | — | — | — | — | — | — | 2 | 2 |
| second-brain | — | ✅ | — | — | — | — | — | — | 4 | 1 |
| Jumbo | ✅ | — | — | — | — | — | ✅ | — | 6 | 5 |
| CommonGround | ✅ | ✅ | — | — | — | — | — | — | 2 | 1 |
| Mengram | ✅ | ✅ | ✅ | — | — | — | — | — | 4 | 1 |
| omega-memory | ✅ | ✅ | ✅ | — | — | — | — | — | 5 | 1 |
| ClawMem | ✅ | ✅ | ✅ | — | — | — | — | ✅ | 5 | 3 |
| shodh-memory | ✅ | ✅ | ✅ | — | — | — | ✅ | — | 1 | 1 |
| AIPass | — | ✅ | — | — | — | — | — | ✅ | 3 | 1 |
| YourMemory | ✅ | ✅ | ✅ | — | — | — | — | — | 4 | 1 |
| ArcRift | ✅ | ✅ | ✅ | — | — | — | — | ✅ | 3 | 3 |
| MoltBrain | ✅ | ✅ | — | — | — | — | — | ✅ | 2 | 1 |
| MemLayer | ✅ | ✅ | ✅ | — | — | — | — | — | 3 | 1 |
| icarus | ✅ | ✅ | ✅ | — | — | — | — | — | 4 | 1 |
| Memory Palace | ✅ | ✅ | ✅ | — | — | — | — | — | 3 | 1 |
| Octopoda-OS | — | ✅ | — | — | — | — | — | — | 3 | 1 |
| Memora | ✅ | ✅ | ✅ | — | — | — | — | ✅ | 4 | 1 |
| memorix | — | ✅ | — | — | — | — | — | — | 2 | 1 |
| TeleMem | — | ✅ | — | — | — | — | — | — | 1 | 1 |
| vestige | ✅ | ✅ | ✅ | ✅ | — | — | — | ✅ | 4 | 1 |
| memoir | ✅ | — | — | — | — | — | — | ✅ | 2 | 1 |
| context-infra | ✅ | ✅ | — | — | — | — | — | — | 2 | 1 |
| MemoMind | ✅ | ✅ | ✅ | — | — | — | — | ✅ | 2 | 3 |
| stash | — | ✅ | — | — | — | — | ✅ | — | 1 | 1 |
| Wax | ✅ | ✅ | ✅ | — | — | — | ✅ | — | 1 | 1 |
| ai-memory | ✅ | ✅ | — | — | — | — | — | — | 3 | 1 |
| LightMem | — | — | — | — | — | — | — | — | 1 | 1 |
| opencode-mem | — | ✅ | — | — | — | — | — | ✅ | 3 | 1 |
| token-savior | ✅ | ✅ | ✅ | — | ✅ | — | — | — | 6 | 1 |
| mem9 | ✅ | ✅ | ✅ | — | — | — | — | — | 3 | 1 |
| nocturne | ✅ | — | — | — | — | — | — | — | 1 | 1 |
| LangMem | — | ✅ | — | — | — | — | — | — | 1 | 1 |
| memanto | — | ✅ | — | — | — | — | — | ✅ | 5 | 1 |
| memsearch | ✅ | ✅ | ✅ | — | — | — | — | — | 3 | 1 |
| mcp-memory-service | ✅ | ✅ | ✅ | — | — | — | ✅ | ✅ | 7 | 6 |
| obsidian-mind | ✅ | ✅ | — | — | — | — | — | — | 2 | 1 |
| MemMachine | — | ✅ | ✅ | — | — | — | — | — | 2 | 1 |
| MIRIX | ✅ | ✅ | — | — | — | — | — | ✅ | 6 | 1 |
| Acontext | ✅ | — | — | — | — | — | — | — | 4 | 4 |
| MemoryBear | ✅ | ✅ | ✅ | ✅ | — | — | ✅ | ✅ | 3 | 1 |
| OpenMemory | — | ✅ | — | — | — | — | — | ✅ | 2 | 1 |
| m_flow | ✅ | ✅ | ✅ | ✅ | — | — | — | — | 5 | 1 |
| memory-lancedb-pro | ✅ | ✅ | ✅ | — | — | — | — | — | 3 | 1 |
| TencentDB-AM | ✅ | ✅ | ✅ | — | — | — | — | — | 1 | 1 |
| engram | ✅ | — | — | — | — | — | — | ✅ | 4 | 2 |
| ByteRover | ✅ | — | — | — | — | — | — | — | 1 | 1 |
| Honcho | ✅ | ✅ | — | — | — | — | — | — | 3 | 1 |
| MemOS | ✅ | ✅ | ✅ | — | — | — | — | — | 3 | 1 |
| EverOS | ✅ | ✅ | ✅ | — | — | — | — | — | 1 | 1 |
| memU | — | ✅ | — | — | — | — | — | — | 1 | 1 |
| Memori | ✅ | ✅ | — | — | — | — | — | — | 1 | 1 |
| Memvid | ✅ | ✅ | ✅ | — | — | — | — | ✅ | 1 | 1 |
| hindsight | ✅ | ✅ | ✅ | — | — | — | — | — | 4 | 1 |
| Letta | ✅ | ✅ | — | — | — | — | — | — | 2 | 1 |
| agentmemory | ✅ | ✅ | ✅ | — | — | — | — | — | 3 | 1 |
| gbrain | ✅ | ✅ | ✅ | — | — | — | — | — | 2 | 1 |
| OpenViking | ✅ | ✅ | ✅ | — | — | — | — | — | 3 | 3 |
| Cognee | ✅ | ✅ | — | — | ✅ | — | — | — | 5 | 1 |
| Supermemory | ✅ | ✅ | ✅ | — | — | — | — | — | 3 | 2 |
| Graphiti | ✅ | ✅ | ✅ | — | — | — | — | — | 2 | 1 |
| Nanobot | — | — | — | — | — | — | — | — | 1 | 2 |
| MemPalace | — | ✅ | ✅ | — | — | — | — | — | 1 | 2 |
| Mem0 | ✅ | ✅ | ✅ | — | — | — | — | — | 1 | 1 |
| claude-mem | ✅ | ✅ | — | — | — | — | — | ✅ | 3 | 1 |

---

## Knowledge Lifecycle

| System | Decay/forgetting | Supersede/replace | Contradiction detect | Quarantine | Auto-resolution | Trust model | Explicit forget |
| --- | --- | --- | --- | --- | --- | --- | --- |
| context-keeper | ✅ | ✅ | — | — | — | — | ✅ |
| fidelis | — | — | — | — | — | — | — |
| slowave | ✅ | ✅ | ✅ | — | ✅ | — | ✅ |
| Somnigraph | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ |
| MarsNMe | ✅ | ✅ | ✅ | ✅ | — | — | ✅ |
| Midas | ✅ | ✅ | ✅ | — | — | ✅ | ✅ |
| Kage | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| gitmem | — | — | — | — | — | — | ✅ |
| VIR | — | ✅ | ✅ | — | — | ✅ | ✅ |
| Fullerenes | — | — | — | — | — | — | — |
| YesMem | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Origin | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Continuity v2 | — | — | — | — | — | — | — |
| Noosphere | — | ✅ | ✅ | — | ✅ | ✅ | ✅ |
| second-brain | ✅ | ✅ | ✅ | — | ✅ | — | ✅ |
| Jumbo | — | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| CommonGround | — | — | — | — | — | — | — |
| Mengram | — | ✅ | ✅ | — | — | — | ✅ |
| omega-memory | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| ClawMem | ✅ | ✅ | — | — | — | — | ✅ |
| shodh-memory | ✅ | — | — | — | — | — | ✅ |
| AIPass | ✅ | ✅ | — | — | — | — | — |
| YourMemory | ✅ | ✅ | ✅ | — | — | — | — |
| ArcRift | — | ✅ | — | — | — | — | ✅ |
| MoltBrain | — | — | — | — | — | — | — |
| MemLayer | ✅ | — | — | — | — | — | — |
| icarus | — | ✅ | — | — | — | — | ✅ |
| Memory Palace | ✅ | — | — | — | — | — | ✅ |
| Octopoda-OS | — | — | — | — | — | — | ✅ |
| Memora | — | ✅ | ✅ | — | — | — | ✅ |
| memorix | — | ✅ | — | — | — | — | ✅ |
| TeleMem | — | — | — | — | — | — | — |
| vestige | ✅ | ✅ | ✅ | — | — | ✅ | ✅ |
| memoir | — | ✅ | — | — | — | — | — |
| context-infra | — | — | — | — | — | — | — |
| MemoMind | — | ✅ | — | — | — | — | ✅ |
| stash | ✅ | — | — | — | ✅ | — | ✅ |
| Wax | — | — | — | — | — | — | — |
| ai-memory | ✅ | ✅ | — | — | — | — | — |
| LightMem | — | — | — | — | — | — | — |
| opencode-mem | — | — | — | — | — | — | ✅ |
| token-savior | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| mem9 | — | ✅ | — | — | — | — | ✅ |
| nocturne | — | — | — | — | — | — | — |
| LangMem | — | — | — | — | — | — | — |
| memanto | — | ✅ | — | — | — | — | — |
| memsearch | — | — | — | — | — | — | — |
| mcp-memory-service | ✅ | ✅ | ✅ | — | ✅ | — | ✅ |
| obsidian-mind | — | — | — | — | — | — | — |
| MemMachine | — | — | — | — | — | — | ✅ |
| MIRIX | ✅ | ✅ | — | — | ✅ | — | — |
| Acontext | — | — | — | — | — | — | ✅ |
| MemoryBear | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ |
| OpenMemory | ✅ | — | — | — | — | — | ✅ |
| m_flow | — | — | — | — | — | — | — |
| memory-lancedb-pro | ✅ | — | — | — | — | — | — |
| TencentDB-AM | — | — | — | — | — | — | — |
| engram | — | ✅ | ✅ | — | — | — | ✅ |
| ByteRover | ✅ | ✅ | — | — | — | — | — |
| Honcho | — | — | — | — | — | — | — |
| MemOS | — | ✅ | — | — | — | — | ✅ |
| EverOS | — | — | — | — | — | — | ✅ |
| memU | — | — | — | — | — | — | ✅ |
| Memori | — | — | — | — | — | — | — |
| Memvid | — | — | — | — | — | — | — |
| hindsight | — | — | — | — | — | — | — |
| Letta | — | — | — | — | — | — | ✅ |
| agentmemory | ✅ | ✅ | — | — | — | — | ✅ |
| gbrain | — | ✅ | ✅ | — | — | — | ✅ |
| OpenViking | — | — | — | — | — | — | — |
| Cognee | — | — | — | — | — | — | ✅ |
| Supermemory | ✅ | ✅ | ✅ | — | ✅ | — | ✅ |
| Graphiti | — | ✅ | — | — | — | — | ✅ |
| Nanobot | — | — | — | — | — | — | — |
| MemPalace | — | — | — | — | — | — | — |
| Mem0 | — | — | — | — | — | — | ✅ |
| claude-mem | — | — | — | — | — | — | — |

---

## Extraction Pipeline

| System | Auto-extraction | Content-aware preproc | Deduplication | Quality refinement | Narrative generation | Clustering | Recurrence detection | Persona extraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| context-keeper | — | — | — | ✅ | ✅ | — | — | — |
| fidelis | — | — | — | — | — | — | — | — |
| slowave | — | — | ✅ | — | — | ✅ | ✅ | — |
| Somnigraph | — | — | ✅ | ✅ | ✅ | ✅ | — | — |
| MarsNMe | — | — | ✅ | — | — | — | — | — |
| Midas | — | — | ✅ | ✅ | — | — | ✅ | — |
| Kage | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | — |
| gitmem | — | — | — | — | — | — | — | — |
| VIR | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | — |
| Fullerenes | ✅ | — | — | — | — | — | — | — |
| YesMem | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Origin | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| Continuity v2 | ✅ | — | — | — | — | ✅ | — | — |
| Noosphere | ✅ | — | ✅ | ✅ | ✅ | ✅ | — | — |
| second-brain | — | — | ✅ | ✅ | — | — | — | — |
| Jumbo | — | ✅ | ✅ | ✅ | ✅ | ✅ | — | — |
| CommonGround | — | — | — | — | — | — | — | — |
| Mengram | ✅ | — | ✅ | — | — | — | — | — |
| omega-memory | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| ClawMem | ✅ | — | ✅ | — | — | — | — | — |
| shodh-memory | ✅ | — | ✅ | — | — | — | — | — |
| AIPass | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | ✅ |
| YourMemory | — | — | ✅ | — | — | — | — | — |
| ArcRift | ✅ | ✅ | ✅ | — | — | — | — | — |
| MoltBrain | ✅ | — | — | — | ✅ | — | — | — |
| MemLayer | ✅ | — | ✅ | — | — | — | — | — |
| icarus | — | — | — | — | — | — | — | — |
| Memory Palace | — | — | ✅ | — | — | ✅ | — | — |
| Octopoda-OS | ✅ | — | ✅ | — | — | — | — | — |
| Memora | — | ✅ | ✅ | — | — | — | — | — |
| memorix | — | — | — | — | — | — | — | — |
| TeleMem | ✅ | — | ✅ | — | — | — | — | — |
| vestige | ✅ | — | ✅ | — | — | — | — | — |
| memoir | ✅ | — | — | — | — | — | — | — |
| context-infra | ✅ | ✅ | — | ✅ | ✅ | — | ✅ | ✅ |
| MemoMind | ✅ | — | ✅ | ✅ | — | — | — | — |
| stash | ✅ | — | ✅ | ✅ | — | ✅ | ✅ | — |
| Wax | — | — | — | — | — | — | — | — |
| ai-memory | ✅ | — | — | — | ✅ | — | — | — |
| LightMem | — | — | — | — | — | — | — | — |
| opencode-mem | — | — | ✅ | — | — | — | — | ✅ |
| token-savior | ✅ | — | ✅ | — | — | — | — | ✅ |
| mem9 | ✅ | — | — | — | — | — | — | — |
| nocturne | — | — | — | — | — | — | — | — |
| LangMem | ✅ | — | — | — | — | — | — | — |
| memanto | ✅ | — | — | — | — | — | — | — |
| memsearch | ✅ | — | ✅ | — | — | — | — | — |
| mcp-memory-service | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| obsidian-mind | — | — | — | — | — | — | — | — |
| MemMachine | ✅ | ✅ | ✅ | — | — | — | — | ✅ |
| MIRIX | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Acontext | ✅ | — | ✅ | — | ✅ | — | — | ✅ |
| MemoryBear | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| OpenMemory | — | — | — | — | — | — | — | — |
| m_flow | ✅ | — | ✅ | — | — | — | — | — |
| memory-lancedb-pro | ✅ | — | — | — | — | — | — | — |
| TencentDB-AM | ✅ | — | ✅ | — | — | — | — | ✅ |
| engram | — | — | ✅ | — | — | — | — | — |
| ByteRover | ✅ | ✅ | ✅ | — | — | — | — | — |
| Honcho | ✅ | — | — | — | ✅ | — | — | ✅ |
| MemOS | ✅ | ✅ | ✅ | ✅ | — | — | — | — |
| EverOS | ✅ | — | — | — | ✅ | ✅ | — | ✅ |
| memU | ✅ | ✅ | — | — | — | — | — | — |
| Memori | ✅ | — | — | — | — | — | — | — |
| Memvid | — | — | — | — | — | — | — | — |
| hindsight | ✅ | — | — | — | — | — | — | — |
| Letta | ✅ | — | — | — | — | — | — | ✅ |
| agentmemory | ✅ | — | ✅ | — | — | — | — | — |
| gbrain | ✅ | — | ✅ | ✅ | — | — | — | — |
| OpenViking | ✅ | ✅ | ✅ | — | — | — | — | — |
| Cognee | ✅ | — | — | — | — | — | — | — |
| Supermemory | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | ✅ |
| Graphiti | ✅ | — | ✅ | — | ✅ | ✅ | — | — |
| Nanobot | ✅ | — | — | — | ✅ | — | — | — |
| MemPalace | ✅ | — | — | — | — | — | — | — |
| Mem0 | ✅ | — | — | — | — | — | — | — |
| claude-mem | ✅ | — | — | — | — | — | — | — |

---

## Platform Support

| System | Claude Code | Codex | OpenCode | Gemini CLI | Copilot | Cursor | Windsurf | OpenClaw | Hermes | pi/omp | Antigravity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| context-keeper | ✅ | ✅ | — | ✅ | — | ✅ | ✅ | — | — | — | — |
| fidelis | ✅ | — | — | — | — | — | — | — | — | — | — |
| slowave | ✅ | — | — | — | — | ✅ | ✅ | — | — | — | — |
| Somnigraph | ✅ | — | — | — | — | — | — | — | — | — | — |
| MarsNMe | ✅ | — | — | — | — | ✅ | — | ✅ | ✅ | — | — |
| Midas | ✅ | ✅ | — | — | — | ✅ | ✅ | — | — | — | — |
| Kage | ✅ | ✅ | ✅ | ✅ | — | ✅ | ✅ | — | — | — | — |
| gitmem | ✅ | ✅ | — | — | — | ✅ | ✅ | — | — | — | — |
| VIR | ✅ | — | — | — | — | — | — | — | — | — | — |
| Fullerenes | ✅ | ✅ | — | — | — | ✅ | — | — | — | — | — |
| YesMem | ✅ | ✅ | ✅ | — | — | — | — | — | — | ✅ | ✅ |
| Origin | ✅ | ✅ | — | ✅ | ✅ | ✅ | — | — | — | — | — |
| Continuity v2 | ✅ | — | — | — | — | — | — | — | — | — | — |
| Noosphere | — | — | ✅ | — | — | — | — | ✅ | ✅ | — | — |
| second-brain | ✅ | — | — | — | — | ✅ | — | — | — | — | — |
| Jumbo | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | — | — | — |
| CommonGround | — | — | — | — | — | — | — | — | — | — | — |
| Mengram | ✅ | ✅ | — | — | — | ✅ | ✅ | ✅ | — | — | — |
| omega-memory | ✅ | ✅ | — | ✅ | — | ✅ | ✅ | — | — | — | — |
| ClawMem | ✅ | — | — | — | — | — | — | ✅ | ✅ | — | — |
| shodh-memory | ✅ | — | — | — | — | ✅ | — | — | — | — | — |
| AIPass | ✅ | ✅ | — | — | — | — | — | — | — | — | — |
| YourMemory | ✅ | — | ✅ | — | — | ✅ | ✅ | — | — | — | — |
| ArcRift | ✅ | — | — | — | — | ✅ | ✅ | — | — | — | — |
| MoltBrain | ✅ | — | — | — | — | — | — | ✅ | — | — | — |
| MemLayer | — | — | — | — | — | — | — | — | — | — | — |
| icarus | ✅ | — | — | — | — | ✅ | — | — | — | — | — |
| Memory Palace | ✅ | ✅ | ✅ | ✅ | — | ✅ | ✅ | — | — | — | ✅ |
| Octopoda-OS | ✅ | — | — | — | — | — | — | ✅ | — | — | — |
| Memora | ✅ | ✅ | — | — | — | — | — | — | — | — | — |
| memorix | — | — | — | — | — | — | — | — | — | — | — |
| TeleMem | — | — | — | — | — | — | — | — | — | — | — |
| vestige | ✅ | ✅ | — | — | — | — | ✅ | — | — | — | — |
| memoir | ✅ | ✅ | — | — | — | — | — | — | — | — | — |
| context-infra | ✅ | — | ✅ | — | — | ✅ | — | — | — | — | — |
| MemoMind | ✅ | — | — | — | — | — | — | — | — | — | — |
| stash | ✅ | — | ✅ | — | — | ✅ | ✅ | — | — | — | — |
| Wax | ✅ | — | — | — | — | ✅ | ✅ | — | — | — | — |
| ai-memory | ✅ | ✅ | ✅ | ✅ | — | ✅ | — | ✅ | — | ✅ | ✅ |
| LightMem | — | — | — | — | — | — | — | — | — | — | — |
| opencode-mem | — | — | ✅ | — | — | — | — | — | — | — | — |
| token-savior | ✅ | — | — | — | — | — | — | — | — | — | — |
| mem9 | ✅ | ✅ | ✅ | — | — | — | — | ✅ | ✅ | — | — |
| nocturne | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | ✅ |
| LangMem | — | — | — | — | — | — | — | — | — | — | — |
| memanto | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | — |
| memsearch | ✅ | ✅ | ✅ | — | — | — | — | ✅ | — | — | — |
| mcp-memory-service | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | — |
| obsidian-mind | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | ✅ |
| MemMachine | ✅ | — | — | — | — | ✅ | — | ✅ | — | — | — |
| MIRIX | — | — | — | — | — | — | — | — | — | — | — |
| Acontext | ✅ | — | — | — | — | — | — | ✅ | — | — | — |
| MemoryBear | — | — | — | — | — | — | — | — | — | — | — |
| OpenMemory | ✅ | ✅ | — | — | ✅ | ✅ | ✅ | — | — | — | ✅ |
| m_flow | ✅ | — | — | — | — | ✅ | — | ✅ | — | — | — |
| memory-lancedb-pro | ✅ | — | — | — | — | — | — | ✅ | — | — | — |
| TencentDB-AM | — | — | — | — | — | — | — | ✅ | ✅ | — | — |
| engram | ✅ | ✅ | ✅ | ✅ | — | ✅ | ✅ | — | — | ✅ | ✅ |
| ByteRover | ✅ | ✅ | — | — | — | ✅ | ✅ | — | — | — | — |
| Honcho | ✅ | — | — | — | — | — | — | — | — | — | — |
| MemOS | — | — | — | — | — | — | — | ✅ | ✅ | — | — |
| EverOS | ✅ | — | — | ✅ | — | ✅ | — | ✅ | — | — | — |
| memU | ✅ | — | — | — | — | — | — | ✅ | — | — | — |
| Memori | ✅ | — | — | — | — | ✅ | — | ✅ | ✅ | — | — |
| Memvid | — | — | — | — | — | — | — | — | — | — | — |
| hindsight | ✅ | — | — | — | — | — | — | — | — | — | — |
| Letta | ✅ | — | — | — | — | — | — | — | — | — | — |
| agentmemory | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | ✅ |
| gbrain | ✅ | — | — | — | — | ✅ | — | ✅ | ✅ | — | — |
| OpenViking | ✅ | ✅ | — | — | — | — | — | ✅ | ✅ | — | — |
| Cognee | ✅ | — | — | — | — | — | — | ✅ | — | — | — |
| Supermemory | ✅ | — | ✅ | — | — | ✅ | ✅ | ✅ | ✅ | — | — |
| Graphiti | ✅ | — | — | — | — | ✅ | — | — | — | — | — |
| Nanobot | — | — | — | — | — | — | — | — | — | — | — |
| MemPalace | ✅ | — | — | ✅ | — | — | — | — | — | — | — |
| Mem0 | ✅ | — | — | — | — | ✅ | — | — | — | — | — |
| claude-mem | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | — | — | — |

---

## Benchmarks (published)

| System | LoCoMo | LongMemEval | PersonaMem | Token reduction | Methodology open |
| --- | --- | --- | --- | --- | --- |
| context-keeper | — | — | — | — | ✅ |
| fidelis | — | 83.2% R@1 | — | — | ✅ |
| slowave | 76.0 | 87.8% | — | 86% | ✅ |
| Somnigraph | 85.1 | — | — | — | ✅ |
| MarsNMe | — | — | — | — | — |
| Midas | 0.73 | 0.92 | — | 30–40% | ✅ |
| Kage | — | 96.17% R@5 | — | — | ✅ |
| gitmem | — | — | — | — | — |
| VIR | — | — | — | — | — |
| Fullerenes | — | — | — | 64% | ✅ |
| YesMem | 0.87 | — | — | ~30% proxy | ✅ |
| Origin | 70.0 | 93.6 | — | — | ✅ |
| Continuity v2 | — | — | — | — | — |
| Noosphere | — | — | — | — | — |
| second-brain | — | — | — | — | — |
| Jumbo | — | — | — | — | — |
| CommonGround | — | — | — | — | — |
| Mengram | — | — | — | — | — |
| omega-memory | — | 76.8 | — | — | ✅ |
| ClawMem | — | — | — | — | — |
| shodh-memory | — | — | — | — | — |
| AIPass | — | — | — | — | — |
| YourMemory | 59.0 | 89.4 | — | — | ✅ |
| ArcRift | — | — | — | — | ✅ |
| MoltBrain | — | — | — | — | — |
| MemLayer | — | — | — | — | — |
| icarus | — | — | — | — | — |
| Memory Palace | — | — | — | — | ✅ |
| Octopoda-OS | — | — | — | — | — |
| Memora | — | — | — | — | — |
| memorix | — | — | — | — | — |
| TeleMem | — | — | — | — | — |
| vestige | — | — | — | — | — |
| memoir | — | — | — | — | — |
| context-infra | — | — | — | — | — |
| MemoMind | — | — | — | — | — |
| stash | — | — | — | — | — |
| Wax | — | — | — | — | — |
| ai-memory | — | — | — | — | — |
| LightMem | — | — | — | — | ✅ |
| opencode-mem | — | — | — | — | — |
| token-savior | — | — | — | -77% | — |
| mem9 | 58.84 | — | — | — | ✅ |
| nocturne | — | — | — | — | — |
| LangMem | — | — | — | — | — |
| memanto | 87.1 | 89.8 | — | — | ✅ |
| memsearch | — | — | — | — | ✅ |
| mcp-memory-service | — | 86.0% (sess) / 80.4% (turn) | — | — | ✅ |
| obsidian-mind | — | — | — | — | — |
| MemMachine | — | — | — | — | ✅ |
| MIRIX | 85.38 | — | — | — | ✅ |
| Acontext | — | — | — | ~45% tool calls | — |
| MemoryBear | — | — | — | — | ✅ |
| OpenMemory | — | — | — | — | — |
| m_flow | 81.8 | 89.0 | — | — | ✅ |
| memory-lancedb-pro | — | — | — | — | — |
| TencentDB-AM | — | — | 76% | 61% | — |
| engram | — | — | — | — | — |
| ByteRover | 96.1 | 92.8 | — | — | ✅ |
| Honcho | — | — | — | — | — |
| MemOS | 75.80 | +40.43% | +40.75% | 35.24% | ✅ |
| EverOS | 93.05 | 83.00 | — | — | ✅ |
| memU | 92.09 | — | — | — | ✅ |
| Memori | 81.95 | — | — | 95% fewer | ✅ |
| Memvid | +35% SOTA | — | — | — | ✅ |
| hindsight | — | 91.4 | — | — | ✅ |
| Letta | — | — | — | — | ✅ |
| agentmemory | — | 95.2 | — | 92% fewer | ✅ |
| gbrain | — | — | — | — | — |
| OpenViking | 82.1 | — | — | 91% | ✅ |
| Cognee | — | — | — | — | — |
| Supermemory | #1 (no score) | 81.6% | — | — | — |
| Graphiti | — | — | — | — | — |
| Nanobot | — | — | — | — | — |
| MemPalace | 88.9 | 96.6 | — | — | ✅ |
| Mem0 | 91.6 | 94.8 | — | — | ✅ |
| claude-mem | — | — | — | — | — |

---

*Auto-generated from `data.js` via `build.js`. Do not edit this file directly.*
