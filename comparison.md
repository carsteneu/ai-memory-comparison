# AI Memory Systems — Feature-Level Comparison

> **Open-Source fact table.** Every claim links to public README, docs, or source.
> Corrections via PR welcome. No affiliation with any listed project.

**Last updated:** 2026-05-27
**Systems:** claude-mem, Mem0, engram, Graphiti, Cognee, ByteRover, Memvid, Memori, EverOS, TencentDB-AM, YesMem, ai-memory

---

## 1. Vital Signs

| | claude-mem | Mem0 | engram | Graphiti | Cognee | ByteRover | Memvid | Memori | EverOS | TencentDB-AM | YesMem | ai-memory |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Stars** | ~79k | ~57k | ~3.8k | ~26.7k | ~17.5k | ~4.8k | ~15.6k | ~15k | ~5.7k | ~4.3k | ~9 | ~324 |
| **Language** | TS | Python | Go | Python | Python | TS | Rust | Python | Python | TS | Go | Rust |
| **License** | Apache 2.0 | Apache 2.0 | MIT | Apache 2.0 | Apache 2.0 | Elastic 2.0 | Apache 2.0 | Apache 2.0 | Apache 2.0 | MIT | Apache 2.0 | MIT |
| **Single binary** | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |

---

## 2. Architecture

| | claude-mem | Mem0 | engram | Graphiti | Cognee | ByteRover | Memvid | Memori | EverOS | TencentDB-AM | YesMem | ai-memory |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Deployment** | Local CLI | Lib/Self-host/Cloud | Local bin / Cloud (opt-in) | Library | Lib/Cloud | Local CLI / Cloud | Lib/Local file | Cloud / BYODB | Lib/MCP | Plugin (OpenClaw) | Local binary | Local binary |
| **Storage** | SQLite+Chroma | Qdrant | SQLite+FTS5 | Graph DB | Graph+Vector | SQLite+Context tree | Single .mv2 file | Cloud | Vector DB | SQLite+sqlite-vec | SQLite+Vector | Git wiki (md) |
| **Integration** | Hooks (5) | API/SDK | MCP+Hooks (19 tools) | Library | API+Hooks | MCP+REPL | SDK | SDK/MCP | MCP | Plugin hooks | Proxy+MCP+Hooks | MCP+Hooks |
| **Proxy** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Web UI / TUI** | ✅ Web | ✅ Cloud | ✅ TUI | ❌ | ✅ CLI -ui | ✅ Web dash | ❌ | ✅ Cloud | ❌ | ❌ | ❌ | ✅ Web |
| **Offline** | ✅ | ⚠️ lib only | ✅ | ✅ | ⚠️ lib only | ✅ | ✅ | ❌ Cloud-first | ✅ | ✅ | ✅ | ✅ |

---

## 3. Data Model — What Gets Stored

| | claude-mem | Mem0 | engram | Graphiti | Cognee | ByteRover | Memvid | Memori | EverOS | TencentDB-AM | YesMem | ai-memory |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Unit** | Observation (text) | Memory (text) | Memory (title+type+What/Why/Where/Learned) | Fact (graph node) | Fact (graph+vec) | Context node (tree) | Smart Frame | Memory entry | Memory entry | Atom/Scenario/Persona | Learning V2 (structured) | Wiki page (md) |
| **Entities** | ❌ | ✅ | ❌ | ✅ nodes | ✅ graph | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ junction tbl | ❌ |
| **Actions** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ junction tbl | ❌ |
| **Keywords/tags** | ❌ | ❌ | ✅ type tag | ❌ | ❌ | ❌ | ✅ tags | ❌ | ❌ | ❌ | ✅ junction tbl | ❌ |
| **Anticipated queries** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Trigger rules** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Domain tag** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ 5 domains | ❌ |
| **Task type** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ task/idea/blocked | ❌ |
| **Context (why)** | ❌ | ❌ | ✅ "Why" field | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Source attribution** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ 5-tier | ❌ |
| **Origin + trust** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ multiplier | ❌ |
| **Emotional** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ 0.0–1.0 | ❌ |
| **Conflict surfacing** | ❌ | ❌ | ✅ judge+compare | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ contradict+supersede | ❌ |
| **Layered memory** | ❌ | ❌ | ❌ | ✅ temporal | ❌ | ❌ | ✅ Frames timeline | ❌ | ❌ | ✅ L0→L3 pyramid | ❌ | ❌ |
| **Time-travel** | ❌ | ❌ | ✅ timeline | ✅ valid_at | ❌ | ✅ git-like vc | ✅ frame rewind | ❌ | ❌ | ❌ | ✅ sessions+chains+temporal | ✅ git versioned |
| **Schema fields** | ~4 | ~6 | ~6 | ~8 | ~10 | ~6 | ~8 | ~6 | ~8 | ~12 | **~22** | ~6 |

---

## 4. Search & Retrieval

| | claude-mem | Mem0 | engram | Graphiti | Cognee | ByteRover | Memvid | Memori | EverOS | TencentDB-AM | YesMem | ai-memory |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Full-text** | ✅ FTS5 | ✅ BM25 | ✅ FTS5 | ✅ | ✅ | ✅ | ✅ BM25 | ✅ | ✅ | ✅ | ✅ FTS5 | ✅ FTS5 |
| **Semantic/vector** | ✅ Chroma | ✅ | ❌ | ✅ GraphRAG | ✅ | ❌ | ✅ HNSW+ONNX | ✅ | ✅ | ✅ sqlite-vec | ✅ 512d | ❌ |
| **Hybrid (BM25+Vec)** | ❌ | ✅ | ❌ | ✅ Graph | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ RRF | ❌ |
| **Deep (incl. thinking)** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Code graph** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ Tree-sitter | ❌ |
| **Docs search** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Fact metadata query** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Timeline view** | ✅ timeline | ❌ | ✅ timeline | ❌ | ❌ | ❌ | ✅ frames | ❌ | ❌ | ❌ | ✅ deep_search since/before | ❌ |
| **Search modes** | 3 | 1 | 4 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | **9** | 2 |
| **Data sources** | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | **4** | 1 |

---

## 5. Knowledge Lifecycle

| | claude-mem | Mem0 | engram | Graphiti | Cognee | ByteRover | Memvid | Memori | EverOS | TencentDB-AM | YesMem | ai-memory |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Decay/forgetting** | ❌ | ❌ | ❌ | ✅ temporal | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ Ebbinghaus | ❌ |
| **Supersede/replace** | ❌ | ❌ add-only | ✅ update | ✅ edges | ❌ | ✅ vc commit | ❌ | ❌ | ❌ | ❌ | ✅ chains+cycles | ✅ pages |
| **Contradiction detect** | ❌ | ❌ | ✅ judge+compare | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ Pearce&Hall | ❌ |
| **Quarantine** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Auto-resolution** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ TTL | ❌ |
| **Trust model** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ 4-tier | ❌ |
| **Explicit forget** | ❌ | ✅ | ✅ delete | ❌ | ✅ `forget()` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ quarantine+skip | ❌ |

---

## 6. Extraction Pipeline

| | claude-mem | Mem0 | engram | Graphiti | Cognee | ByteRover | Memvid | Memori | EverOS | TencentDB-AM | YesMem | ai-memory |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Auto-extraction** | ✅ hooks | ✅ 1-pass | ❌ manual save | ✅ auto | ✅ pipeline | ❌ manual curate | ❌ manual put | ✅ SDK hooks | ✅ | ✅ L0→L3 | ✅ **6-phase** | ✅ compile |
| **Content-aware preproc** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ ~70% reduction | ❌ |
| **Deduplication** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ 3-method | ❌ |
| **Quality refinement LLM** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ Phase 3 | ❌ |
| **Narrative generation** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ Phase 4 | ✅ LLM compile |
| **Clustering** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ Phase 4.5 | ❌ |
| **Recurrence detection** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ Phase 4.6 | ❌ |
| **Persona extraction** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ L3 Persona | ✅ Phase 6, 50+ traits | ❌ |

---

## 7. Unique Differentiators

| System | What nobody else does |
|---|---|
| **claude-mem** | Progressive Disclosure (3-layer retrieval); massive community; `<private>` tags |
| **Mem0** | Best published benchmarks (LoCoMo 91.6, LongMemEval 94.8); YC-backed; agent-signup flow |
| **engram** | Conflict surfacing (mem_judge/mem_compare); git-sync without merge conflicts; TUI dashboard; `engram setup pi` native |
| **Graphiti** | Temporal knowledge graph (valid_at/invalid_at); open-source engine under Zep |
| **Cognee** | `remember`/`recall`/`forget`/`improve` API; graph+vector unified |
| **ByteRover** | Context tree with git-like version control (branch/merge); strongest benchmarks (LoCoMo 96.1%, LongMemEval-S 92.8%); 22+ agent support |
| **Memvid** | Single-file memory (.mv2); Smart Frames (video-codec inspired); frame rewinding; sub-ms latency |
| **Memori** | Agent-native (captures execution, not just conversation); LoCoMo 81.95% at 5% token footprint; BYODB option |
| **EverOS** | Full evaluation framework for memory; benchmark suites included; self-evolving agent focus |
| **TencentDB-AM** | Mermaid symbolic memory (max semantics, min tokens); L0→L3 semantic pyramid; 61% token reduction |
| **YesMem** | Deepest data model (22 fields); 9 search modes across 4 sources; 6-phase extraction; 6-count scoring; Sawtooth proxy collapse; multi-agent orchestration; code graph; persona engine |
| **ai-memory** | Git-versioned markdown wiki (grep-able, Obsidian-compatible); zero LLM mode; cross-agent handoffs |

---

## 8. Platform Support

| | claude-mem | Mem0 | engram | Graphiti | Cognee | ByteRover | Memvid | Memori | EverOS | TencentDB-AM | YesMem | ai-memory |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Claude Code** | ✅ | ✅ skill | ✅ | ❌ | ✅ plugin | ✅ | ❌ | ✅ MCP | ✅ MCP | ❌ | ✅ | ✅ |
| **Codex** | ✅ | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ MCP | ❌ | ✅ | ✅ |
| **OpenCode** | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ MCP | ❌ | ✅ | ✅ |
| **Gemini CLI** | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ MCP | ❌ | ❌ | ✅ |
| **Copilot** | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Cursor** | ❌ | ✅ skill | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ MCP | ✅ MCP | ❌ | ❌ | ✅ |
| **Windsurf** | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **OpenClaw** | ✅ | ❌ | ❌ | ❌ | ✅ plugin | ❌ | ❌ | ✅ native | ✅ MCP | ✅ native | ❌ | ✅ |
| **Hermes** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ native | ❌ | ✅ native | ❌ | ❌ |
| **pi/omp** | ❌ | ❌ | ✅ `setup pi` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Antigravity** | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 9. Benchmarks (where published)

| | claude-mem | Mem0 | engram | Graphiti | Cognee | ByteRover | Memvid | Memori | EverOS | TencentDB-AM | YesMem | ai-memory |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **LoCoMo** | ❌ | **91.6** | ❌ | ❌ | ❌ | **96.1** | claims +35% SOTA | **81.95** | ✅ | ❌ | 0.87 | ❌ |
| **LongMemEval** | ❌ | **94.8** | ❌ | ❌ | ❌ | **92.8** | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| **BEAM 1M** | ❌ | **64.1** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **PersonaMem** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **76%** | ❌ | ❌ |
| **Token reduction** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 95% fewer vs full context | ❌ | **61%** | ~30% proxy | ❌ |
| **Methodology open** | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ paper | ✅ | ✅ paper | ✅ | ✅ | ✅ | ❌ |

---

## Summary

| Dimension | Best |
|---|---|
| **Data model depth** | **YesMem** (22 fields vs next-best TencentDB-AM ~12) |
| **Search breadth** | **YesMem** (9 modes, 4 sources) |
| **Knowledge lifecycle** | **YesMem** (decay, supersede, contradict, quarantine, auto-resolve, trust) |
| **Extraction pipeline** | **YesMem** (6 phases vs 1–3 elsewhere) |
| **Retrieval benchmarks** | **ByteRover** (LoCoMo 96.1, LongMemEval-S 92.8) / **Mem0** (LoCoMo 91.6) |
| **Token efficiency** | **TencentDB-AM** (61% reduction, Mermaid symbols) / **Memori** (95% fewer vs full context) |
| **Time-travel / versioning** | **ByteRover** (git-like VC) / **YesMem** (sessions+chains+temporal search) / **Memvid** (frame rewinding) |
| **Temporal reasoning** | **Graphiti** (valid_at/invalid_at edges) |
| **Conflict detection** | **YesMem** (Pearce&Hall) / **engram** (mem_judge/mem_compare) |
| **Setup simplicity** | **claude-mem** (`npx claude-mem install`) |
| **Community/trust** | **claude-mem** (79k stars) |
| **Zero-infra** | **Memvid** (.mv2 single file) / **ai-memory** (markdown in git) |
| **Multi-agent orchestration** | **YesMem** (spawn, heartbeat, crash recovery, messaging, scratchpad) |
| **Cross-agent portability** | **ai-memory** / **engram** (quit Claude, resume Codex — same memory) |

---

## Source References

<details>
<summary>Click to expand</summary>

### claude-mem
- [README](https://github.com/thedotmack/claude-mem#readme): hooks, 3-layer search, web viewer

### Mem0
- [README](https://github.com/mem0ai/mem0#readme): v3 algorithm, LoCoMo 91.6, LongMemEval 94.8

### engram
- [README](https://github.com/Gentleman-Programming/engram#readme): Go binary, SQLite+FTS5, 19 MCP tools, TUI, git sync, conflict surfacing
- [Agent Setup](https://github.com/Gentleman-Programming/engram/blob/main/docs/AGENT-SETUP.md): platform support incl. pi

### Graphiti
- [README](https://github.com/getzep/graphiti#readme): temporal knowledge graph

### Cognee
- [README](https://github.com/topoteretes/cognee#readme): remember/recall/forget/improve API

### ByteRover CLI
- [README](https://github.com/campfirein/byterover-cli#readme): context tree VC, LoCoMo 96.1, LongMemEval-S 92.8
- [Paper](https://arxiv.org/abs/2604.01599)

### Memvid
- [README](https://github.com/memvid/memvid#readme): Smart Frames, .mv2, +35% SOTA

### Memori
- [README](https://github.com/MemoriLabs/Memori#readme): agent-native, LoCoMo 81.95, BYODB
- [Paper](https://arxiv.org/abs/2603.19935)

### EverOS
- [README](https://github.com/EverMind-AI/EverOS#readme): use cases, methods, benchmarks

### TencentDB-Agent-Memory
- [README](https://github.com/Tencent/TencentDB-Agent-Memory#readme): L0→L3 pyramid, Mermaid symbols, 61% token reduction

### YesMem
- [README](https://github.com/carsteneu/yesmem#readme)
- [Features.md](https://github.com/carsteneu/yesmem/blob/main/Features.md): 70 tools
- [docs/features/memory.md](https://github.com/carsteneu/yesmem/blob/main/docs/features/memory.md): V2 learnings, 6-count scoring, extraction pipeline
- [docs/mcp-tools-reference.md](https://github.com/carsteneu/yesmem/blob/main/docs/mcp-tools-reference.md): full tool catalog

### ai-memory
- [README](https://github.com/akitaonrails/ai-memory#readme): git wiki, cross-agent handoffs
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
