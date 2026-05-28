# nanobot — Audit Report

> **Source:** `HKUDS/nanobot` (43.3k stars, Python, MIT license)
> **Note:** The URL `github.com/nanobot-memory/nanobot` is incorrect. The actual repo is `github.com/HKUDS/nanobot`.
> **Date:** 2026-05-28

## Vital Signs

| Field | Value |
|---|---|
| **Stars** | ~43.3k |
| **Language** | Python (82.6%), TypeScript (16.9%) |
| **License** | MIT |
| **Deployment** | Local CLI / PyPI / uv / Docker |
| **Integration** | Standalone agent (not a memory plugin) |
| **Storage** | Filesystem: MEMORY.md, SOUL.md, USER.md, history.jsonl + GitStore |
| **Single binary** | No — requires Python runtime + pip install |

## Claim Verification

### CONFIRMED

| Claim | Evidence |
|---|---|
| **offline** | Local-first. All memory is files on disk. No cloud dependency. |
| **privacy** | All data stays in workspace (`workspace/memory/`, `workspace/sessions/`). No telemetry to external servers. |
| **export** | Memory is plain markdown/JSONL files. Portable by copy, git, or any file sync. |
| **context** | `get_memory_context()` injects `## Long-term Memory` into the system prompt. MEMORY.md loaded as context every turn. |
| **timeTravel** | GitStore versions SOUL.md, USER.md, MEMORY.md. `/dream-restore` lists and restores previous git versions. (No temporal query axis though — see corrections.) |
| **autoExtract** | Dream 2-phase pipeline: Phase 1 analyzes history.jsonl, Phase 2 edits memory files via AgentRunner. Consolidator auto-summarizes overflowed messages. |
| **narrative** | Dream Phase 2 generates narrative summaries in MEMORY.md. The memory system is described as "interpretive, not just archival." |

### PARTIALLY CONFIRMED

| Claim | Status | Evidence |
|---|---|---|
| **decay** | ⚠️ Partial | No automatic forgetting or Ebbinghaus decay. Dream annotates stale lines with `← Nd` in Phase 1 prompts, but this is purely informational for the LLM — no programmatic decay/removal. |
| **supersede** | ⚠️ Partial | Dream surgically edits MEMORY.md, which effectively supersedes old facts. But there's no explicit supersede protocol (no old→new version linking, no contradiction tracking). |
| **fulltext** | ⚠️ Partial | No built-in FTS engine. Docs suggest `grep`/`jq`/Python on history.jsonl. This is "searchable by external tools" — not a first-class search feature. |
| **dataSources=2** | ⚠️ Approximate | Two data stores: (1) history.jsonl (conversation archive), (2) long-term files (MEMORY.md, SOUL.md, USER.md). But these aren't "searchable data sources" with indexes — they're just files. |

### NOT VERIFIED / INCORRECT

| Claim | Status | Evidence |
|---|---|---|
| **entities** | ❌ | No structured entity tracking. MEMORY.md is unstructured markdown. history.jsonl has cursor/timestamp/content — no entity extraction. |
| **keywords** | ❌ | No keyword/tag system. No structured metadata on memory entries. |
| **semantic** | ❌ | No vector embeddings. No semantic/similarity search. Purely text-based. |
| **searchModes=2** | ❌ | At most 1 (plain text grep). No vector, no hybrid, no graph, no deep search, no metadata query. The `grep`/`jq` suggestions are manual workflows, not search modes. |
| **explicitForget** | ❌ | No user-facing forget/delete mechanism for memory entries. No `/forget` command. |
| **dedup** | ❌ | No deduplication logic in source code. Dream uses git blame for line ages but no dedup. |
| **recurrence** | ❌ | No recurrence detection in code or docs. |
| **p_claude** | ❌ | nanobot is NOT a Claude Code plugin. It's a standalone agent framework with its own runtime. The `CLAUDE.md` file is developer guidance for working on nanobot code — not a declaration of Claude Code platform support. nanobot has its own CLI (`nanobot agent`). No Claude Code integration listed anywhere. |
| **schemaFields=7** | ❌ | The only structured memory entry is history.jsonl: `{cursor, timestamp, content}` = **3 fields**. Long-term memory (MEMORY.md, SOUL.md, USER.md) is unstructured markdown with zero schema. |

## Architecture Summary

nanobot's Dream memory is a **file-based, LLM-driven system** with two stages:

1. **Consolidator** — Lightweight: summarizes overflowed conversation messages into `history.jsonl` (append-only JSONL: `cursor`, `timestamp`, `content`).
2. **Dream** — Heavyweight: cron-scheduled 2-phase LLM pipeline. Phase 1 analyzes new history entries + current memory files. Phase 2 uses AgentRunner with `read_file`/`edit_file` tools to surgically update `MEMORY.md`, `SOUL.md`, and `USER.md`.

Storage:
```
workspace/
├── SOUL.md              # Bot's communication style
├── USER.md              # User preferences
└── memory/
    ├── MEMORY.md        # Project facts & decisions
    ├── history.jsonl    # Append-only conversation archive
    ├── .cursor          # Consolidator write position
    ├── .dream_cursor    # Dream read position
    └── .git/            # Git history for long-term files
```

## What nanobot IS

- A **standalone AI agent framework** with memory as one subsystem
- Excellent at auto-extracting conversational knowledge into markdown
- Git-versioned memory with restore capability (`/dream-restore`)
- User-inspectable: `/dream`, `/dream-log`, `/dream-restore` commands
- Configurable cron scheduling for Dream (`intervalH`)

## What nanobot is NOT

- Not a **dedicated memory system** — memory is a feature of an agent framework
- Not a **Claude Code plugin** — has its own agent loop and runtime
- Not a **search engine** — no FTS, no vector, no semantic search
- Not a **structured knowledge base** — all memory is freetext markdown
- Not a **lifecycle manager** — no decay, no dedup, no explicit forget

## Corrections

1. **URL is wrong.** `github.com/nanobot-memory/nanobot` → `github.com/HKUDS/nanobot`
2. **Type mismatch.** nanobot is not a dedicated "AI memory system" — it's an AI agent framework where memory is one subsystem. The comparison table in `comparison.md` should classify it differently from systems like Mem0, engram, or YesMem that are dedicated memory systems.
3. **`p_claude` claim is false.** nanobot runs its own agent loop. It does not integrate into Claude Code as a memory backend.
4. **Most feature claims are overstated.** Of the 20 claimed features, only 7 are confirmed, 4 are partial, 9 are not verified/incorrect. The claims significantly overrepresent nanobot's memory capabilities.

## Recommendation

Include nanobot in the comparison table, but with accurate feature flags. It's a strong *agent* with good *auto-extraction*, but it's not comparable to dedicated memory systems on search, data model depth, or knowledge lifecycle features.

---

`evidence: "https://github.com/carsteneu/ai-memory-comparison/blob/main/evidence/nanobot.md"`
