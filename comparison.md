# AI Memory Systems — Feature-Level Comparison

> **Open-Source fact table.** Every claim links to public README, docs, or source.
> Corrections via PR welcome. No affiliation with any listed project.

**Last updated:** 2026-05-27
**Systems:** claude-mem, Mem0, Graphiti, Cognee, Memvid, EverOS, TencentDB-Agent-Memory, YesMem, ai-memory

---

## 1. Vital Signs

| | claude-mem | Mem0 | Graphiti | Cognee | Memvid | EverOS | TencentDB-AM | YesMem | ai-memory |
|---|---|---|---|---|---|---|---|---|---|
| **Stars** | ~79k | ~57k | ~26.7k | ~17.5k | ~15.6k | ~5.7k | ~4.3k | ~9 | ~324 |
| **Language** | TS | Python | Python | Python | Rust | Python | TS | Go | Rust |
| **License** | Apache 2.0 | Apache 2.0 | Apache 2.0 | Apache 2.0 | Apache 2.0 | Apache 2.0 | MIT | Apache 2.0 | MIT |
| **Single binary** | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ |

---

## 2. Architecture

| | claude-mem | Mem0 | Graphiti | Cognee | Memvid | EverOS | TencentDB-AM | YesMem | ai-memory |
|---|---|---|---|---|---|---|---|---|---|
| **Deployment** | Local CLI | Lib/Self-host/Cloud | Library | Lib/Cloud | Lib/Local file | Lib/MCP | Plugin (OpenClaw) | Local binary | Local binary |
| **Storage** | SQLite+Chroma | Qdrant/Vector-DB | Graph DB | Graph+Vector | Single .mv2 file | Vector DB | SQLite+sqlite-vec | SQLite+Vector | Git wiki (markdown) |
| **Integration** | Hooks (5) | API/SDK | Library | API+Hooks | SDK | MCP | Plugin hooks | Proxy+MCP+Hooks | MCP+Hooks |
| **Proxy** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Web UI** | ✅ | ✅ Cloud | ❌ | ✅ -ui | ❌ | ❌ | ❌ | ❌ | ✅ /web |
| **Offline** | ✅ | ⚠️ lib only | ✅ | ⚠️ lib only | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 3. Data Model — What Gets Stored

| | claude-mem | Mem0 | Graphiti | Cognee | Memvid | EverOS | TencentDB-AM | YesMem | ai-memory |
|---|---|---|---|---|---|---|---|---|---|
| **Unit** | Observation (text) | Memory (text) | Fact (graph node) | Fact (graph+vec) | Smart Frame | Memory entry | Atom/P scenario/Persona | **Learning V2** | Wiki page (md) |
| **Entities** | ❌ | ✅ | ✅ nodes | ✅ graph | ❌ | ❌ | ✅ | ✅ junction tbl | ❌ |
| **Actions** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ junction tbl | ❌ |
| **Keywords** | ❌ | ❌ | ❌ | ❌ | ✅ tags | ❌ | ❌ | ✅ junction tbl | ❌ |
| **Anticipated queries** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Trigger rules** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Domain tag** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ 5 domains | ❌ |
| **Task type** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ task/idea/blocked | ❌ |
| **Context (why)** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Source** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ 5-tier | ❌ |
| **Origin + trust** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ multiplier | ❌ |
| **Emotional** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ 0.0–1.0 | ❌ |
| **Layered memory** | ❌ | ❌ | ✅ temporal | ❌ | ✅ Frames timeline | ❌ | ✅ L0→L3 pyramid | ❌ | ❌ |
| **Time-travel / history** | ❌ | ❌ | ✅ valid_at | ❌ | ✅ frame rewind | ❌ | ❌ | ✅ sessions+chains+temporal search | ✅ git versioned |
| **Schema fields** | ~4 | ~6 | ~8 | ~10 | ~8 | ~8 | ~12 | **~22** | ~6 |

---

## 4. Search & Retrieval

| | claude-mem | Mem0 | Graphiti | Cognee | Memvid | EverOS | TencentDB-AM | YesMem | ai-memory |
|---|---|---|---|---|---|---|---|---|---|
| **Full-text** | ✅ FTS5 | ✅ BM25 | ✅ | ✅ | ✅ BM25 | ✅ | ✅ | ✅ FTS5 | ✅ FTS5 |
| **Semantic/vector** | ✅ Chroma | ✅ | ✅ GraphRAG | ✅ | ✅ HNSW+ONNX | ✅ | ✅ sqlite-vec | ✅ 512d | ❌ |
| **Hybrid (BM25+Vec)** | ❌ | ✅ | ✅ Graph | ✅ | ❌ | ❌ | ❌ | ✅ RRF | ❌ |
| **Deep (incl. thinking)** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Code graph** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ Tree-sitter | ❌ |
| **Docs search** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Fact metadata query** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Distinct search modes** | 3 | 1 | 1 | 1 | 1 | 1 | 1 | **9** | 2 |
| **Data sources** | 1 | 1 | 1 | 1 | 1 | 1 | 1 | **4** | 1 |

---

## 5. Knowledge Lifecycle

| | claude-mem | Mem0 | Graphiti | Cognee | Memvid | EverOS | TencentDB-AM | YesMem | ai-memory |
|---|---|---|---|---|---|---|---|---|---|
| **Decay/forgetting** | ❌ | ❌ | ✅ temporal | ❌ | ❌ | ❌ | ❌ | ✅ Ebbinghaus | ❌ |
| **Supersede/replace** | ❌ | ❌ add-only | ✅ edges | ❌ | ❌ | ❌ | ❌ | ✅ chains+cycles | ✅ pages |
| **Contradiction detect** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ Pearce&Hall | ❌ |
| **Quarantine** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Auto-resolution** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ TTL | ❌ |
| **Trust model** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ 4-tier | ❌ |
| **Explicit forget** | ❌ | ✅ | ❌ | ✅ `forget()` | ❌ | ❌ | ❌ | ✅ quarantine+skip_indexing | ❌ |

---

## 6. Extraction Pipeline

| | claude-mem | Mem0 | Graphiti | Cognee | Memvid | EverOS | TencentDB-AM | YesMem | ai-memory |
|---|---|---|---|---|---|---|---|---|---|
| **Auto-extraction** | ✅ hooks | ✅ 1-pass | ✅ auto | ✅ pipeline | ❌ manual put | ✅ | ✅ L0→L3 | ✅ **6-phase** | ✅ compile |
| **Content-aware preproc** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ ~70% reduction | ❌ |
| **Deduplication** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ 3-method | ❌ |
| **Quality refinement LLM** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ Phase 3 | ❌ |
| **Narrative generation** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ Phase 4 | ✅ LLM compile |
| **Clustering** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ Phase 4.5 | ❌ |
| **Recurrence detection** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ Phase 4.6 | ❌ |
| **Persona extraction** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ L3 Persona | ✅ Phase 6, 50+ traits | ❌ |

---

## 7. Unique Differentiators

| System | What nobody else does |
|---|---|
| **claude-mem** | Progressive Disclosure (3-layer retrieval); massive community; `<private>` tags |
| **Mem0** | Best benchmark scores (LoCoMo 91.6, LongMemEval 94.8); YC-backed; agent signup flow |
| **Graphiti** | Temporal knowledge graph (valid_at/invalid_at); open-source engine under Zep |
| **Cognee** | `remember`/`recall`/`forget`/`improve` API; graph+vector unified; explicit forget |
| **Memvid** | Single-file memory (.mv2); Smart Frames (video-codec inspired); frame rewinding; +35% SOTA on LoCoMo; sub-ms latency |
| **EverOS** | Full evaluation framework for memory; benchmark suites included; self-evolving agent focus |
| **TencentDB-AM** | Mermaid symbolic memory (max semantics, min tokens); L0→L3 semantic pyramid; 61% token reduction; 51% pass rate improvement |
| **YesMem** | Deepest data model (22 fields); 9 search modes across 4 sources; 6-phase extraction; 6-count scoring; Sawtooth proxy collapse; multi-agent orchestration; code graph; persona engine; time-travel via sessions+supersede chains+temporal search |
| **ai-memory** | Git-versioned markdown wiki (grep-able, Obsidian-compatible); zero LLM mode; cross-agent handoff pages; thin-client CLI |

---

## 8. Platform Support

| | claude-mem | Mem0 | Graphiti | Cognee | Memvid | EverOS | TencentDB-AM | YesMem | ai-memory |
|---|---|---|---|---|---|---|---|---|---|
| **Claude Code** | ✅ | ✅ skill | ❌ | ✅ plugin | ❌ | ✅ MCP | ❌ | ✅ | ✅ |
| **Codex** | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ MCP | ❌ | ✅ | ✅ |
| **OpenCode** | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ MCP | ❌ | ✅ | ✅ |
| **Gemini CLI** | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ MCP | ❌ | ❌ | ✅ |
| **Copilot** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Cursor** | ❌ | ✅ skill | ❌ | ❌ | ❌ | ✅ MCP | ❌ | ❌ | ✅ |
| **OpenClaw** | ✅ | ❌ | ❌ | ✅ plugin | ❌ | ✅ MCP | ✅ native | ❌ | ✅ |
| **Hermes** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ native | ❌ | ❌ |
| **pi/omp** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 9. Benchmarks (where published)

| | claude-mem | Mem0 | Graphiti | Cognee | Memvid | EverOS | TencentDB-AM | YesMem | ai-memory |
|---|---|---|---|---|---|---|---|---|---|
| **LoCoMo** | ❌ | **91.6** | ❌ | ❌ | claims +35% SOTA | ✅ | ❌ | 0.87 | ❌ |
| **LongMemEval** | ❌ | **94.8** | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| **BEAM 1M** | ❌ | **64.1** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **PersonaMem** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **76%** (+59%) | ❌ | ❌ |
| **Token reduction** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **61%** | ~30% proxy | ❌ |
| **Methodology open** | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |

---

## Summary

| Dimension | Best |
|---|---|
| **Data model depth** | **YesMem** (22 fields vs next-best TencentDB-AM ~12) |
| **Search breadth** | **YesMem** (9 modes, 4 sources) |
| **Knowledge lifecycle** | **YesMem** (decay, supersede, contradict, quarantine, auto-resolve, trust) |
| **Extraction pipeline** | **YesMem** (6 phases vs 1–3 elsewhere) |
| **Retrieval benchmarks** | **Mem0** (LoCoMo 91.6, LongMemEval 94.8) / **Memvid** (claims +35% SOTA) |
| **Token efficiency** | **TencentDB-AM** (61% reduction, Mermaid symbols) |
| **Time-travel / versioning** | **YesMem** (sessions + supersede chains + temporal search) / **Memvid** (frame rewinding) / **ai-memory** (git wiki) |
| **Temporal reasoning** | **Graphiti** (valid_at/invalid_at edges) |
| **Setup simplicity** | **claude-mem** (`npx claude-mem install`) |
| **Community/trust** | **claude-mem** (79k stars) |
| **Zero-infra (single file)** | **Memvid** (.mv2) / **ai-memory** (markdown in git) |
| **Multi-agent orchestration** | **YesMem** (spawn, heartbeat, crash recovery, messaging, scratchpad) |
| **Cross-agent portability** | **ai-memory** (quit Claude, resume Codex — wiki handoff) |

---

## Source References

<details>
<summary>Click to expand</summary>

### claude-mem
- [README](https://github.com/thedotmack/claude-mem#readme)
- [Architecture](https://docs.claude-mem.ai/architecture/overview)
- [MCP Search Tools](https://github.com/thedotmack/claude-mem#mcp-search-tools)

### Mem0
- [README](https://github.com/mem0ai/mem0#readme)
- [New Memory Algorithm v3](https://github.com/mem0ai/mem0#new-memory-algorithm-april-2026): Single-pass ADD-only, entity linking, multi-signal retrieval

### Graphiti
- [README](https://github.com/getzep/graphiti#readme): Temporal knowledge graph with valid_at/invalid_at

### Cognee
- [README](https://github.com/topoteretes/cognee#readme): `remember`/`recall`/`forget`/`improve` API
- [Claude Code Plugin](https://github.com/topoteretes/cognee-integrations/tree/main/integrations/claude-code)

### Memvid
- [README](https://github.com/memvid/memvid#readme): Smart Frames, single-file .mv2, +35% SOTA

### EverOS
- [README](https://github.com/EverMind-AI/EverOS#readme): Use cases, methods, benchmarks

### TencentDB-Agent-Memory
- [README](https://github.com/Tencent/TencentDB-Agent-Memory#readme): L0→L3 pyramid, Mermaid symbolic memory, 61% token reduction

### YesMem
- [README](https://github.com/carsteneu/yesmem#readme)
- [Features.md](https://github.com/carsteneu/yesmem/blob/main/Features.md): 70 tools
- [docs/features/memory.md](https://github.com/carsteneu/yesmem/blob/main/docs/features/memory.md): 6-count scoring, V2 learnings, extraction pipeline
- [docs/mcp-tools-reference.md](https://github.com/carsteneu/yesmem/blob/main/docs/mcp-tools-reference.md): Full tool catalog
- [docs/BENCHMARK.md](https://github.com/carsteneu/yesmem/blob/main/docs/BENCHMARK.md): LoCoMo methodology

### ai-memory
- [README](https://github.com/akitaonrails/ai-memory#readme): Git-versioned wiki, cross-agent handoffs
- [ARCHITECTURE.md](https://github.com/akitaonrails/ai-memory/blob/main/docs/ARCHITECTURE.md)

</details>

---

## Contributing

1. Open a PR with corrections or additions
2. Every factual claim must link to public documentation or source code
3. Project maintainers: corrections get priority
4. New rows welcome — keep it verifiable, not marketing

## License

CC0 — Public Domain. Use anywhere, no attribution required.
