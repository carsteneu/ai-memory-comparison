# context-infra — Evidence

> **Audit date:** 2026-05-28
> **Source:** https://github.com/grapeot/context-infrastructure
> **Evidence:** `main` branch, REAMDE.md, AGENTS.md, PRD.md, KNOWLEDGE_BASE.md, OBSERVATIONS.md, observer.py, reflector.py, semantic_search/cli.py, USER.md, SOUL.md, WORKSPACE.md, COMMUNICATION.md, setup_guide.md, SKILL_ECOSYSTEM.md

> ⚠️ **URL correction:** The repo is `grapeot/context-infrastructure`, not `f5d4s/context-infra`.
> ⚠️ **License correction:** `data.js` says `"?"` — README explicitly states MIT.

---

## Vital Signs

### Language ✅
- All `.py` files, 95% Python. `README.md` — `Python 95.0%`.

### Single binary ❌
- Not a single executable. Requires Python + dependencies (numpy, opencode_client, embedding server). `setup_guide.md` references `uv pip install`.

---

## Architecture

### Offline ✅
- All file-based, local operation. `setup_guide.md` Step 3b: "确认本地 OpenCode Server 运行". Semantic search uses local embedding server: `observer.py:--endpoint http://localhost:1234/v1`.
- Correct in `data.js` — no change.

### webUi ❌
- No web UI. All interaction through AI agent (Claude Code, OpenCode, Cursor). File-based system.
- Correct in `data.js` — no change.

### privacy ❌ (absent as design goal)
- Data stays local by nature, but privacy is not a named design goal or feature. No encryption, no privacy controls.
- Correct in `data.js` — no change.

### export ❌
- No dedicated export feature. Data is in plain Markdown files, but no structured export tool.
- Correct in `data.js` — no change.

---

## Data Model

### layeredMemory ✅ — CORRECTION
- **`periodic_jobs/ai_heartbeat/docs/PRD.md`** — "Global layered architecture: L3: global hard constraints (rules/, passive loading). L1/L2: dynamic observation logs (global memory pool, agent-initiated retrieval)."
- **`AGENTS.md`** — "三层记忆架构：L3（全局约束）：rules/ 被动加载。L1/L2（动态记忆）：contexts/memory/OBSERVATIONS.md，agent主动检索。自动积累：periodic_jobs/ai_heartbeat/ 每日 observer + 每周 reflector."
- **Three explicit tiers:** L1 (daily observer, append-only observations) → L2 (weekly reflector, GC + promotion to rules) → L3 (rules/SOUL.md, USER.md, axioms, skills — loaded every session).
- **Correction:** `data.js` says `layeredMemory: false` → **true**.

### timeTravel ❌
- No mechanism to browse historical state, query past versions, or time-travel through memory snapshots.
- Correct in `data.js` — no change.

### schemaFields: 4 ✅ (no change)
- OBSERVATIONS.md memory entry format: `Date: YYYY-MM-DD` + `🔴/🟡/🟢 Priority: [Category] Description` = 4 structured fields (Date, Priority, Category, Content).
- `OBSERVATIONS.md` — "Date: YYYY-MM-DD\n\n🔴 High: [方法论/约束] 描述\n🟡 Medium: [项目状态/决策] 描述\n🟢 Low: [任务流水] 描述"
- Rules (USER.md, SOUL.md) have their own structure but are not memory entries in the schema sense.
- Correct in `data.js` — no change.

### entities ❌
- No named-entity extraction or entity storage as distinct database fields. USER.md has a name field ("grapeot") but this is a profile file, not memory entities.
- Correct in `data.js` — no change.

### persona: — → ✅ — CORRECTION
- **`periodic_jobs/ai_heartbeat/docs/KNOWLEDGE_BASE.md` §4.2** — "根据最新观测到的有效规律、语言风格变化、以及长效约束，修改或更新 rules/ 下的核心规则文件 (SOUL.md, USER.md, COMMUNICATION.md, WORKSPACE.md)."
- The L2 reflector extracts patterns from observations and updates USER.md (user preferences, traits, working style). This IS persona extraction from accumulated observations.
- **Correction:** `data.js` says `persona: false` → **true**.

### All other Data Model fields ❌ (no change)
- actions, keywords, anticipatedQueries, triggerRules, domainTag, taskType, context (why), source, originTrust, emotional, conflict — none present.
- grep is documented for keyword search (`grep -n "关键词" OBSERVATIONS.md`), but this is shell grep, not a structured keyword/tag system.

---

## Search & Retrieval

### fulltext: — → ✅ — CORRECTION
- **`contexts/memory/OBSERVATIONS.md`** documents grep-based search: `grep -n "关键词" contexts/memory/OBSERVATIONS.md` and `grep -A 20 "Date: $(date -v-7d +%Y-%m-%d)" contexts/memory/OBSERVATIONS.md`.
- CRITERIA.md explicitly accepts "grep" as full-text search. System's own documentation treats grep as its primary text search method.
- **Correction:** `data.js` says `fulltext: false` → **true**.

### semantic: — → ✅ — CORRECTION
- **`tools/semantic_search/main.py`** and **`tools/semantic_search/search/cli.py`** — Full embedding-based semantic search with cosine similarity, chunking (MarkdownChunker), parallel embedding extraction, and ForwardIndex caching.
- **`rules/skills/semantic_search.md`** — "通用语义搜索工具，可对任意本地文本文件建索引并做自然语言查询。它超越关键词匹配，理解语义层面的关联。"
- Uses local embedding server (text-embedding-qwen3-embedding-8b via `--endpoint http://localhost:1234/v1`).
- **Correction:** `data.js` says `semantic: false` → **true**.

### hybrid ❌
- No BM25+vector result fusion. Only cosine similarity semantic search.
- Correct in `data.js` — no change.

### searchModes: 1 → 2 — CORRECTION
- **Mode 1:** Semantic search (`python tools/semantic_search/main.py --query "..." --file-list ...`).
- **Mode 2:** grep-based full-text keyword search (documented in OBSERVATIONS.md).
- Both are distinct search modes documented for use.
- **Correction:** `data.js` says `searchModes: 1` → **2**.

### dataSources: 1 ✅ (no change)
- Single data source: Markdown files on disk (observations, blog posts, daily records, survey sessions, rules, skills).
- Semantic search indexes all `.md` files in specified directories. No non-Markdown data sources are indexed.
- Correct in `data.js` — no change.

### cacheOpt: — → ✅ — CORRECTION
- **`tools/semantic_search/search/cli.py`** — ForwardIndex with `needs_update()` check using `mtime` comparison: `if not index.needs_update(file_path, mtime): return []`. Batch-based index persistence (`index.save(new_chunks, updated_files)`).
- `.knowledge_cache` directory stores precomputed feature vectors.
- **Correction:** `data.js` says `cacheOpt: false` → **true**.

### All other Search fields ❌ (no change)
- deep, codeGraph, docsSearch, factQuery, timeline — none present.

---

## Knowledge Lifecycle

### All Knowledge Lifecycle fields ❌ (no change)
- **decay:** L2 reflector has scheduled weekly garbage collection of expired 🟢 entries, but this is a binary GC pass, not gradual time-based decay. CRITERIA requires "automatically reduces relevance," not schedule-based deletion.
- **supersede:** No explicit supersede mechanism. Reflector promotes observations to rules, but this is a different mechanism — it transforms content, doesn't mark old entries as superseded.
- **contradiction, quarantine, autoResolve, trustModel, explicitForget** — none present.

---

## Extraction Pipeline

### autoExtract: — → ✅ — CORRECTION
- **`periodic_jobs/ai_heartbeat/src/v0/observer.py`** — Trigger script that auto-extracts observations from daily file changes. No manual `save` calls needed. Runs via cron.
- **`observer.py`** PROMPT_TEMPLATE — "执行观测记忆提取并直接持久化到磁盘...你的目标是生成观测记录。"
- **Correction:** `data.js` says `autoExtract: false` → **true**.

### contentPreproc: — → ✅ — CORRECTION
- **`periodic_jobs/ai_heartbeat/docs/KNOWLEDGE_BASE.md` §2.1-2.3** — Observer applies path whitelist/blacklist (includes `contexts/life_record/`, ignores `contexts/daily_records/`), blog content checks metadata Date field to distinguish new content from formatting changes.
- **`PRD.md` §1.2** — "抗噪设计: 利用 AI 的语义理解能力识别真正的'新内容'。例如，针对 300+ 篇 Blog 的格式变动，AI 应通过检查元数据（Metadata）中的创建日期来识别真正的新文章。"
- This is content-type-aware filtering before extraction.
- **Correction:** `data.js` says `contentPreproc: false` → **true**.

### qualityRefine: — → ✅ — CORRECTION
- **`periodic_jobs/ai_heartbeat/src/v0/reflector.py`** — L2 reflector performs quality refinement: "将具有普适性的内容晋升到 rules/...GC：重写 OBSERVATIONS.md，删除已晋升及过期 🟢 记录."
- **`KNOWLEDGE_BASE.md` §4.2** — "实现从'短期观测'到'长期规则'的进化." This is an LLM-based quality pass after initial extraction.
- **Correction:** `data.js` says `qualityRefine: false` → **true**.

### narrative: — → ✅ — CORRECTION
- **`observer.py`** — Generates daily observation summaries with structured format (Date, 🔴🟡🟢 priorities, descriptions). These are daily handover summaries.
- **`reflector.py`** — Generates weekly "promotion reports" ("完成后回复简短晋升汇报").
- **AGENTS.md** — Serves as a comprehensive project profile (workspace routing, model routing, skill index, memory system overview).
- **Correction:** `data.js` says `narrative: false` → **true**.

### recurrence: — → ✅ — CORRECTION
- **`periodic_jobs/ai_heartbeat/docs/KNOWLEDGE_BASE.md` §4.2** — L2 reflector detects patterns: "将具有普适性的内容晋升到 rules/，按职责边界分类." "跨项目通用 + 多次验证 + 有明确适用场景."
- The reflector explicitly looks for cross-project, repeatedly verified patterns to promote to axioms/skills.
- **Correction:** `data.js` says `recurrence: false` → **true**.

### dedup ❌
- No deduplication mechanism. The observer has an idempotency check (`if f"Date: {target_date}" in content: skip`) but this prevents re-extraction of the same date, not content deduplication.
- Correct in `data.js` — no change.

### clustering ❌
- No clustering of memories by topic or similarity.
- Correct in `data.js` — no change.

---

## Platform Support

### p_claude ✅ (no change)
- **`README.md`** — "用 Claude Code / OpenCode / Cursor 打开这个目录."
- **`AGENTS.md`** — Extensive Claude Code-specific routing table ("Sub-agent 模型路由").
- Correct in `data.js` — no change.

### p_opencode: — → ✅ — CORRECTION
- **`README.md`** — "用 Claude Code / OpenCode / Cursor 打开这个目录."
- **`PRD.md` §5** — "执行引擎: 本地 OpenCode Server (localhost:<your-port>)." §1.3 — "OpenCode-Builder: 作为记忆的生产者和核心消费者."
- **`observer.py`** — Uses `opencode_client` OpenCodeClient API: `client.create_session()`, `client.send_message()`, `client.wait_for_session_complete()`, `client.delete_session()`.
- **`AGENTS.md`** — "配置文件：~/.config/opencode/oh-my-opencode.json"
- **Correction:** `data.js` says `p_opencode: false` → **true**.

### p_cursor ❌ → ✅ — CORRECTION
- **`README.md`** — "用 Claude Code / OpenCode / Cursor 打开这个目录."
- Cursor is explicitly listed as a supported agent in the quickstart.
- **Correction:** `data.js` says `p_cursor: false` → **true**.

### p_codex, p_gemini, p_copilot, p_windsurf, p_openclaw, p_hermes, p_pi, p_antigravity ❌ (no change)
- None documented.

---

## Benchmarks

### All benchmarks ❌ (no change)
- No published scores on LoCoMo, LongMemEval, PersonaMem, or token reduction. No benchmark methodology.
- Correct in `data.js` — no change.

---

## Summary of corrections

| Field | data.js (current) | Verified | Evidence |
|---|---|---|---|
| `license` | `"?"` | `"MIT"` | README footer |
| `storage` | `"?"` | `"Markdown files"` | README directory structure, OBSERVATIONS.md |
| `setup` | `"?"` | `"setup_guide.md"` | setup_guide.md with step-by-step instructions |
| `layeredMemory` | `false` | **`true`** | PRD.md §1.2, AGENTS.md — L3/L2/L1 three-tier hierarchy |
| `fulltext` | `false` | **`true`** | OBSERVATIONS.md grep commands |
| `semantic` | `false` | **`true`** | semantic_search/cli.py embedding search |
| `searchModes` | `1` | **`2`** | semantic + grep (both documented) |
| `autoExtract` | `false` | **`true`** | observer.py auto-extracts from file changes |
| `contentPreproc` | `false` | **`true`** | KNOWLEDGE_BASE.md §2 — blog metadata filtering, whitelist/blacklist |
| `qualityRefine` | `false` | **`true`** | reflector.py — promotes observations, GC expired entries |
| `narrative` | `false` | **`true`** | Daily observation summaries, weekly promotion reports |
| `recurrence` | `false` | **`true`** | KNOWLEDGE_BASE.md §4.2 — cross-project pattern detection |
| `persona` | `false` | **`true`** | KNOWLEDGE_BASE.md §4.2 — updates USER.md from observations |
| `p_opencode` | `false` | **`true`** | README, PRD.md, observer.py using OpenCodeClient |
| `p_cursor` | `false` | **`true`** | README — "用 Claude Code / OpenCode / Cursor" |
| `cacheOpt` | `false` | **`true`** | semantic_search ForwardIndex with mtime caching |

**Corrections:** 16 fields changed (12 Boolean + 3 metadata + 1 numeric).
