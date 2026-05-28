# aipass — Evidence & Audit Report

> **Repository:** https://github.com/AIOSAI/AIPass
> **Audit date:** 2026-05-28
> **Auditor:** OpenCode (DeepSeek V4 Pro)
> **Sources:** GitHub README, AGENTS.md, memory agent README, pyproject.toml, template JSON, source code (manager.py, orchestrator.py)

---

## Verdict: REPOSITORY FOUND — PREVIOUSLY MISDIRECTED

**https://github.com/AIOSAI/AIPass exists and is active.** The previous audit (evidence/aipass.md) targeted `https://github.com/arkohut/aipass` (404). The correct owner is `AIOSAI`, not `arkohut`.

| Metric | Value |
|--------|-------|
| Stars | 150 |
| Language | Python 3.10+ |
| License | MIT |
| Version | 2.4.0 (beta) |
| Commits | 970 |
| Agents | 13 core |
| Tests | 8,400+ |
| PyPI | `pip install aipass` |

---

## Claim Audit

### Vital Signs

| Claim | Verdict | Evidence |
|-------|---------|----------|
| stars: 150 | ✅ CORRECTED | README badge, GitHub sidebar |
| language: Python | ✅ Python | pyproject.toml requires-python >=3.10 |
| license: MIT | ✅ CORRECTED | pyproject.toml + LICENSE file |

### Architecture

| Claim | Verdict | Evidence |
|-------|---------|----------|
| webUi: true | ❌ **REFUTED** | README: "No UI, no dashboard. You work in your terminal." CLI-native only. |
| offline: true | ✅ VERIFIED | README: "Everything is local. Memory is JSON files. Communication is local mailbox files. No cloud, no external APIs." AI LLM calls need internet; memory system is fully local. |
| privacy: true | ✅ VERIFIED | README: "Everything is plain files. No daemon, no hidden state. Delete the directory and it's gone." Local-first, no cloud storage. |
| export: true | ⚠️ QUALIFIED | No explicit export command, but all memory is plain JSON files in `.trinity/` — inherently portable. ChromaDB archives are queryable. Export is trivial (copy files). |

### Data Model (claimed schemaFields=10)

| Claim | Verdict | Evidence |
|-------|---------|----------|
| schemaFields=10 | ✅ VERIFIED (qualified) | LOCAL.template.json `document_metadata` has exactly 10 sub-fields: document_type, document_name, version, schema_version, created, last_updated, managed_by, tags, limits, status |
| keywords: true | ❌ **REFUTED** | The "key_learnings" dict uses string keys (e.g. `"deploy_flow": "use make deploy..."`). These are learning topic labels, NOT a keyword search mechanism. No keyword-based search is documented. Search is semantic (vector) only. |
| layeredMemory: true | ✅ VERIFIED (corrected meaning) | 2-layer architecture: hot layer = JSON files in `.trinity/` (passport, local, observations); cold layer = ChromaDB vector store (auto-archived via rollover when JSON limits exceeded). |
| timeTravel: true | ✅ VERIFIED | All entries have timestamps (`[YYYY-MM-DD]`). Sessions are date-ordered. `get_entry_age()` computes age in days. Chronological ordering enforced ("Newest entries at TOP, oldest at BOTTOM"). Rollover prioritizes oldest entries. |
| narrative: true | ✅ VERIFIED | `.trinity/` files create persistent narrative: passport = identity, local.json = session history + key learnings, observations = collaboration patterns. README: "They remember across sessions. Expertise develops over time." |
| persona: true | ✅ VERIFIED | `.trinity/passport.json` defines agent identity. Spawn creates agents with `--role`, `--purpose`, `--traits`. AGENTS.md startup protocol: "Read: .trinity/passport.json" first. |
| supersede: true | ⚠️ QUALIFIED | Overwrite by key: `add_learning()` replaces existing entries with same key (new timestamp). ChromaDB upsert uses content-hash IDs (sha256[:16]) → same content = replace. But NO explicit "learning X supersedes learning Y" relationship. Simple overwrite, not versioned supersede. |
| explicitForget: true | ❌ **REFUTED** | LOCAL.template.json explicitly states: "DO NOT trim, prune, or delete entries. Rollover to @memory handles overflow automatically." System prohibits manual deletion. No forget/delete API exists. |

### Search & Retrieval (claimed: fulltext, semantic, searchModes=3)

| Claim | Verdict | Evidence |
|-------|---------|----------|
| fulltext: true | ❌ **REFUTED** | Search is vector/semantic via ChromaDB (embedding model: `all-MiniLM-L6-v2`). No fulltext/BM25 search is documented. The `drone @memory search "query"` command performs semantic search. |
| semantic: true | ✅ VERIFIED | README: "ChromaDB vectors, semantic search". Memory README: "Semantic query routing". Uses fastembed (ONNX) with `all-MiniLM-L6-v2` model. |
| timeline: true | ⚠️ QUALIFIED | Data supports timeline queries (all entries timestamped, chronological ordering) but no dedicated "timeline view" or time-travel browsing feature is documented. |
| searchModes: 3 | ⚠️ **EXAGGERATED** | There are 2 documented search paths: (1) semantic search (`drone @memory search`), (2) symbolic fragment search (`drone @memory symbolic fragments`). Plus plan verification (`drone @memory verify`). Only 2 actual search modes, not 3 distinct search modes. |

### Knowledge Lifecycle

| Claim | Verdict | Evidence |
|-------|---------|----------|
| decay: true | ✅ VERIFIED (corrected mechanism) | Age-based pruning, not explicit decay. `get_entry_age()` computes days. Oldest entries removed first in rollover. Untimestamped entries treated as age=999999 (removed first). Limits: max 20 sessions, max 25 key_learnings, max 600 lines per file. |
| supersede: true | ⚠️ QUALIFIED | (see above under Data Model) Overwrite via key match, not explicit supersede chain. |
| explicitForget: true | ❌ REFUTED | (see above under Data Model) Prohibited by design. |

### Extraction Pipeline

| Claim | Verdict | Evidence |
|-------|---------|----------|
| autoExtract: true | ✅ VERIFIED | Rollover pipeline auto-extracts oldest entries when limits exceeded (`extractor.extract_with_metadata()`). Trigger agent fires events. Memory pool processor auto-intake. `process_file()` auto-processes `.local.json`. |
| contentPreproc: true | ⚠️ QUALIFIED | `extract_text_from_memories()` handles multiple entry formats (activities arrays, summary fields, key-value pairs). Schema normalize handler exists. But not a major documented pipeline feature. |
| dedup: true | ✅ VERIFIED | ChromaDB upsert with content-hash IDs (sha256[:16]). Memory README: "content-hash IDs, no duplicates". Symbolic memory has dedicated deduplicator. |
| qualityRefine: true | ⚠️ **MISCHARACTERIZED** | seedgo agent runs 36 automated quality standards — these are code quality checks across all agents, NOT memory quality refinement (no content scoring, no relevance ranking, no fact verification). |

### Platform Support (claimed: p_claude, p_codex, p_opencode, p_cursor)

| Claim | Verdict | Evidence |
|-------|---------|----------|
| p_claude: true | ✅ VERIFIED | README CLI support table: "Claude Code — Fully tested". AGENTS.md and CLAUDE.md present. |
| p_codex: true | ⚠️ QUALIFIED (experimental) | README: "Codex — Experimental". Wired but needs end-to-end testing. Not production-ready. |
| p_opencode: true | ❌ **REFUTED** | No mention of OpenCode anywhere in README, AGENTS.md, or any documentation. Only Claude Code and Codex CLI are listed. |
| p_cursor: true | ❌ **REFUTED** | No IDE integration at all. AIPass is CLI-native: "No UI, no dashboard. You work in your terminal." No Cursor support exists. |

---

## Summary

| Metric | Count |
|--------|-------|
| Claims verified ✅ | 10 |
| Claims partially verified / qualified ⚠️ | 7 |
| Claims refuted ❌ | 6 |
| Claims corrected (different from claim) ⚠️ | 3 |

### Key Corrections from Original Claims

1. **webUi** claimed true → actually false (CLI-only)
2. **fulltext** claimed true → actually false (semantic/vector only)
3. **explicitForget** claimed true → actually false (prohibited by design)
4. **p_opencode** claimed true → actually false (no OpenCode support)
5. **p_cursor** claimed true → actually false (no IDE support)
6. **keywords** claimed true → actually false (key_learnings are labels, not keyword search)
7. **url** was `arkohut/aipass` → corrected to `AIOSAI/AIPass`

### Notable Design Decisions

- AIPass is a **multi-agent framework with memory**, not a standalone memory tool. Memory is one of 13 agents.
- Memory is **file-based first** (JSON), with ChromaDB as an archival layer — not a database-first approach.
- The system explicitly **prohibits manual memory deletion** — rollover/archival is the only management mechanism.
- No web UI — entirely CLI-native, targeting Claude Code and Codex CLI users.
- Memory model: hot (`.trinity/` JSON) + cold (ChromaDB vectors) with automatic rollover at file size limits.

---

## Evidence URL

```
evidence: "https://github.com/carsteneu/ai-memory-comparison/blob/main/evidence/aipass.md"
```
