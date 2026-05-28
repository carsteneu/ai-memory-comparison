# AI Memory Systems — Feature Comparison

> An open-source, source-backed comparison of memory systems for AI coding agents.
> No affiliation, no marketing — just facts from public documentation.

## What this is

When choosing a memory system for your AI coding agent, feature lists and star counts tell different stories. This repo provides a **feature-level comparison** across 9 memory systems, with every claim linked to public READMEs, docs, or source code.

## What this is not

- ❌ A ranking or "best of" list
- ❌ Affiliated with any listed project
- ❌ Based on opinions, vibes, or marketing claims

## Systems compared

| System | Stars | Language | Approach |
|---|---|---|---|
| [claude-mem](https://github.com/thedotmack/claude-mem) | ~79k | TypeScript | Hooks-based observation capture |
| [Mem0](https://github.com/mem0ai/mem0) | ~57k | Python | Memory-as-a-Service platform |
| [Graphiti](https://github.com/getzep/graphiti) | ~26.7k | Python | Temporal knowledge graph |
| [Cognee](https://github.com/topoteretes/cognee) | ~17.5k | Python | Memory control plane (graph+vector) |
| [Memvid](https://github.com/memvid/memvid) | ~15.6k | Rust | Single-file memory (.mv2) |
| [EverOS](https://github.com/EverMind-AI/EverOS) | ~5.7k | Python | Self-evolving agent memory |
| [TencentDB-AM](https://github.com/Tencent/TencentDB-Agent-Memory) | ~4.3k | TypeScript | Symbolic memory (Mermaid) |
| [YesMem](https://github.com/carsteneu/yesmem) | ~9 | Go | Project continuity layer |
| [ai-memory](https://github.com/akitaonrails/ai-memory) | ~324 | Rust | Git-versioned markdown wiki |

See the full comparison in **[comparison.md](comparison.md)**.

## Curation criteria

Systems included in this comparison must be:

1. **Specifically designed for AI agent memory** — not general vector DBs, not RAG frameworks
2. **Intended for coding agents** — or adaptable to them (Claude Code, Codex, OpenCode, etc.)
3. **Actively maintained** — commits within the last 3 months
4. **Open source** — public repo with a recognized license

Not included (by design):
- Agent frameworks with built-in memory (Letta, CrewAI, LangChain) — different category
- Personal data memory (BotMem) — different use case
- Consumer bookmarking tools (Supermemory) — different use case
- Pure vector databases (Chroma, Qdrant, Pinecone) — infrastructure, not memory systems

## Methodology

Every ✅ or ❌ in the comparison is backed by a public source:

- Project README
- Official documentation
- Source code (for architecture claims)
- Published benchmarks where available

If a feature isn't documented, it's marked ❌. No assumptions, no inferences.

## Contributing

**[CONTRIBUTING.md](CONTRIBUTING.md)** has the full process. Quick version:

1. **Corrections:** Open a PR with a link to the public source proving the correction
2. **New systems:** Open an issue first — must meet curation criteria
3. **New comparison rows:** PR with sources for ALL systems in that row

Project maintainers: corrections to your project's row get priority review.

## License

CC0 — Public Domain. Fork it, republish it, use it anywhere. No attribution required.

Star counts and data are snapshots from 2026-05-27. See [comparison.md](comparison.md) for last-updated date.

## Disclosure

This comparison is maintained by the author of [YesMem](https://github.com/carsteneu/yesmem). YesMem is listed alongside every other system and follows the same evidence rules — every ✅ has a public source link, every ❌ is "not documented", not a judgment. Corrections to YesMem's row (or any other row) via PR with public evidence are welcome.
