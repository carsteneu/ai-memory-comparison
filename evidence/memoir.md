# memoir — Evidence

> `evidence: "https://github.com/carsteneu/ai-memory-comparison/blob/main/evidence/memoir.md"`

## Repo Identity

- **Claimed:** `https://github.com/jabberwocky-db/memoir` — **404, org does not exist**
- **Actual:** `https://github.com/zhangfengcdt/memoir` — verified 2026-05-28
- **Website:** https://www.memoir-ai.dev
- **PyPI:** `memoir-ai`
- **License:** Apache 2.0
- **Language:** Python (66.6%), Shell (14.3%), TypeScript (13.5%)
- **Stars:** 555, Forks: 35, Commits: 158

**Note:** A second project named "memoir" exists at `https://github.com/camgitt/memoir` (memoir.sh, 11 stars, Node.js/MCP-based). That is a different tool (workspace sync + session backup, not a structured knowledge base). All citations below refer to `zhangfengcdt/memoir` unless noted otherwise.

---

## Corrections

| Claim | Status | Detail |
|-------|--------|--------|
| `jabberwocky-db/memoir` | **❌ URL correction** | 404. Correct org is `zhangfengcdt`. |

---

## Architecture

### Offline ✅
- `README.md` — Quick look section: `memoir remember "..." -p path` described as "offline, no LLM call"
- `README.md` — `memoir get preferences.coding.style` described as "Read back by path (offline)"

### Web/TUI ✅
- `README.md` — Ships visual explorer (`memoir ui`), auto-opens in browser
- Docs reference: Tree, Graph, Timeline, Places views + `/stats`

---

## Data Model

### Entities ✅
- Semantic path system (e.g., `preferences.coding.style`, `profile.professional.skills.python`) serves as hierarchical structured entity organization — each path segment is a distinct category

### Time-travel ✅
- `README.md` — "Git-like Versioning — Branch, commit, merge, and rollback memories with cryptographic integrity"
- `README.md` — "memoir checkout" to revert, "memoir blame" to audit

---

## Search & Retrieval

### Full-text ✅
- `README.md` — "Multiple Search Engines — Choose between fast keyword-based or intelligent LLM-powered search"

### Search modes = 2 ✅
- `README.md` — Two engines documented: (1) keyword-based, (2) LLM-powered (`memoir recall "..."`)

---

## Knowledge Lifecycle

### Supersede/replace ✅
- `README.md` — Git-like versioning (branch, commit, merge, rollback) implies supersede semantics
- `README.md` — Rollback described: "One bad session poisons every future retrieval. Without memoir blame or memoir checkout, there's no way to audit who taught the agent a rule or revert a hallucination"

---

## Extraction Pipeline

### Auto-extraction ✅
- `README.md` — Claude Code plugin: "your project gets automatic context injection and auto-captured memories"
- Plugin registers hooks for session start, user-prompt-submit, and stop

---

## Platform Support

### Claude Code ✅
- `README.md` — Full Claude Code plugin: `/plugin marketplace add zhangfengcdt/memoir`, slash commands, hooks (session start, user-prompt-submit, stop)

### OpenAI Codex ✅
- `README.md` — Full Codex plugin: marketplace, `codex plugin marketplace add zhangfengcdt/memoir`, lifecycle hooks, skills (memory-recall, memoir-onboard, memoir-remember, memoir-status, memoir-ui), transcript parsing

### OpenCode ❌
- Not mentioned in README or docs index

### GitHub Copilot ❌
- Not mentioned in README or docs index

### Cursor ❌
- Not mentioned in README or docs index

---

## Claims NOT verified from public README

These are claimed by the submitter but have **no citation in the public README**:

| Claim | Status | Note |
|-------|--------|------|
| keywords/tags | ❌ no citation | Semantic paths serve as taxonomy, but explicit keyword/tag system not documented |
| context (why) | ❌ no citation | Not documented in README |
| source attribution | ❌ no citation | Not documented in README |
| explicit forget | ❌ no citation | Not documented in README |
| deduplication | ❌ no citation | "Memory Aggregation" mentioned but not deduplication specifically |
| schemaFields=5 | ❌ no citation | Cannot verify from README alone |
| OpenCode support | ❌ claim false | Not in README |
| Copilot support | ❌ claim false | Not in README |
| Cursor support | ❌ claim false | Not in README |

---

## Alternative: camgitt/memoir

A separate project at `https://github.com/camgitt/memoir` (memoir.sh, MIT, JavaScript, 59 commits). This is a workspace-sync + MCP memory server, not a structured knowledge base. It supports Claude Code, Cursor, Windsurf, Gemini CLI, Copilot, Codex, ChatGPT, Aider, Zed, Cline, Continue, Augment, Trae (13 tools). It does **not** implement entities, time-travel, search modes, supersede, or auto-extraction — it provides MCP tools (`memoir_recall`, `memoir_remember`, `memoir_list`, `memoir_read`) over flat memory files.
