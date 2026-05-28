# Letta (formerly MemGPT) — Evidence

> **Repository:** https://github.com/letta-ai/letta (23k stars, Python, Apache 2.0)
> **Letta Code:** https://github.com/letta-ai/letta-code (2.6k stars, TypeScript)
> **Docs:** https://docs.letta.com
> **Last verified:** 2026-05-28

---

## Audit Summary

| Claim | Status | Evidence |
|-------|--------|----------|
| multiAgent | ✅ Verified | `send_message_to_agent_and_wait_for_reply`, `send_message_to_agents_matching_tags`, subagents in letta-code |
| entities | ❌ Not found | No structured entity extraction; memory is block-based (label:value) |
| actions | ❌ Not found | No action tracking in schema |
| context | ❌ Not found | No "why" or context metadata field on memories; ContextWindowOverview tracks token counts, not semantic context |
| conflict | ❌ Not found | No conflict detection/surfacing between memories |
| layeredMemory | ✅ Verified | Core blocks (in-context) + recall (conversation) + archival (long-term semantic) + MemFS (git-backed md) |
| timeTravel | ✅ Verified | Git-backed MemFS version history; date-range filtering in `conversation_search` and `archival_memory_search` |
| fulltext | ✅ Verified | `conversation_search` uses hybrid text+semantic; MemFS is plain markdown |
| semantic | ✅ Verified | `archival_memory_search` uses semantic similarity; embedding_config present |
| searchModes=2 | ✅ Verified | `conversation_search` (hybrid) + `archival_memory_search` (semantic) — 2 core memory search modes |
| supersede | ⚠️ Partial | `memory_replace`/`core_memory_replace`/`memory_rethink` allow overwrite; no formal supersede with version chains |
| explicitForget | ✅ Verified | `core_memory_replace` with empty string; `memory` tool has `delete` subcommand; `/doctor` for audit |
| autoExtract | ✅ Verified | Sleep-time dreaming/reflection subagents (`/sleeptime`); "proactive memory creation and consolidation" |
| contentPreproc | ❌ Not found | Blocks stored as-is; no content-aware preprocessing or reduction pipeline |
| narrative | ❌ Not found | No narrative generation; dreaming consolidates but doesn't produce narrative summaries |
| recurrence | ❌ Not found | No recurrence detection pattern |
| persona | ✅ Verified | `persona` block in ChatMemory default; `system/persona.md` in MemFS; personality customization docs |
| p_claude | ✅ Verified | Model-agnostic: Claude, GPT, Gemini, GLM, Kimi; `anthropic/claude-sonnet-4-6` in examples |
| schemaFields=10 | ⚠️ Approximate | Block has ~16 fields total (8-10 meaningful non-template); ArchivalMemory has 3-4; ~10 is reasonable |

---

## Data Model

### multiAgent ✅
- `letta/constants.py` — `LETTA_MULTI_AGENT_TOOL_MODULE_NAME = "letta.functions.function_sets.multi_agent"`, `MULTI_AGENT_TOOLS = ["send_message_to_agent_and_wait_for_reply", "send_message_to_agents_matching_tags", "send_message_to_agent_async"]`
- `letta/schemas/agent.py` — `AgentState` has `multi_agent_group`/`managed_group` fields; `CreateAgent` has `include_multi_agent_tools` param
- `letta/functions/function_sets/multi_agent.py` — Full implementation of `send_message_to_agent_and_wait_for_reply`, `send_message_to_agents_matching_tags`, `send_message_to_agent_async`
- letta-code README: "Subagents & Multi-agent: Agents can call any other agent (including themselves) as subagents"

### entities ❌
- No entity extraction model found in schemas. Memory is block-based (`Block` model: label, value, description, tags) — no structured entity extraction with junction tables.
- Archival memory uses simple text + tags model.

### actions ❌
- No action tracking found. Tools exist (`core_memory_append`, `core_memory_replace`, `send_message`) but these are agent tools, not a stored action metadata model.

### context ❌
- `letta/schemas/memory.py` — `ContextWindowOverview` tracks token counts (`num_tokens_core_memory`, `num_tokens_system`, etc.) and window metrics, not semantic "why" context metadata on stored memories.
- No "context" or "why" field on Block, ArchivalMemory, or any memory schema.

### conflict ❌
- No `mem_judge`, `mem_compare`, or conflict detection tools found. Memory editing is direct (replace, append, rethink) with no contradiction detection between entries.

### layeredMemory ✅
- `letta/schemas/memory.py` — `ContextWindowOverview` reveals three-tier architecture: `num_archival_memory`, `num_recall_memory`, `core_memory` (blocks)
- `letta/constants.py` — `BASE_TOOLS = [..., "archival_memory_insert", "archival_memory_search"]`, `BASE_MEMORY_TOOLS = ["core_memory_append", "core_memory_replace", ...]`
- Memory docs: "MemFS (memory filesystem)... organized as a directory of markdown files... system/ directory loaded into system prompt... files outside system/ visible via tree but not auto-loaded"
- Three layers: (1) Core memory blocks (in-context), (2) Recall memory (conversation history, searchable via `conversation_search`), (3) Archival memory (long-term, semantic search)

### timeTravel ✅
- Memory docs: "git-backed filesystem... gives you a full version history of everything your agent has learned"
- `letta/functions/function_sets/base.py` — `conversation_search` accepts `start_date`/`end_date` with ISO 8601 format; `archival_memory_search` accepts `start_datetime`/`end_datetime`
- MemFS is a git repo at `~/.letta/agents/<agent-id>/memory`

---

## Search & Retrieval

### fulltext ✅
- `letta/functions/function_sets/base.py:conversation_search` — "Search prior conversation history using hybrid search (text + semantic similarity)"
- MemFS stores all memory as plain markdown files — inherently full-text searchable via git grep

### semantic ✅
- `letta/functions/function_sets/base.py:archival_memory_search` — "Search archival memory using semantic similarity to find relevant information... search by meaning, not exact keyword matching"
- `letta/schemas/agent.py` — `embedding_config` field on AgentState and CreateAgent
- `letta/constants.py` — `DEFAULT_EMBEDDING_DIM = 1024`, `MAX_EMBEDDING_DIM = 4096`, `EMBEDDING_BATCH_SIZE = 200`

### searchModes=2 ✅
- Two core memory search tools: `conversation_search` (hybrid text+semantic on recall/conversation memory) and `archival_memory_search` (semantic on long-term archival memory)
- File-specific: `grep_files` and `semantic_search_files` (but these are for external file sources, not memory per se)

---

## Knowledge Lifecycle

### supersede ⚠️
- `letta/functions/function_sets/base.py:memory_replace` — String-level replacement in blocks
- `letta/functions/function_sets/base.py:memory_rethink` — "completely rewrite the contents of a memory block"
- `letta/functions/function_sets/base.py` — `memory` tool with `str_replace`, `insert`, `delete`, `rename` subcommands
- **However:** No formal supersede mechanism with version chains, old→new linking, or decay-based replacement. Overwrite is manual and immediate.

### explicitForget ✅
- `letta/functions/function_sets/base.py:core_memory_replace` — "To delete memories, use an empty string for new_content"
- `letta/functions/function_sets/base.py:memory` — Has `delete` subcommand for removing memory blocks
- Memory docs: `/doctor` command to "audit the current memory layout and refine it for proper memory placement"
- Git-backed: can revert any change

---

## Extraction Pipeline

### autoExtract ✅
- Memory docs: "Letta Code launches periodic sleep-time (dream) subagents to reflect on your recent conversations and interactions... proactive memory creation and consolidation"
- Configurable via `/sleeptime` command: trigger by step count or compaction event
- letta-code README: "Self-improvement & Learning: Agents programmatically rewrite their context to improve and adapt over time"
- `letta/schemas/agent.py` — `enable_sleeptime` field on agent config

### contentPreproc ❌
- Blocks are stored as-is with no content-aware preprocessing or reduction pipeline
- No deduplication, content summarization, or compression before storage found

### narrative ❌
- No narrative generation feature. Dreaming subagents consolidate memories but don't produce narrative storytelling summaries

### recurrence ❌
- No recurrence detection pattern found. No tracking of how often concepts appear or pattern emergence

### persona ✅
- `letta/schemas/block.py` — `Persona(Block)` with `label: str = "persona"`
- `letta/schemas/memory.py` — `ChatMemory.__init__(persona, human, limit)` creates default persona + human blocks
- Memory docs: "customize your agent's personality... deeply personalize your agents to be unique to you"
- MemFS: `system/persona.md` as dedicated self-identity block

---

## Platform Support

### p_claude ✅
- letta-code README: "memory-first agent harness... across models (Claude, GPT, Gemini, GLM, Kimi, and more)"
- `letta --backend local connect anthropic` explicit Anthropic support
- Example: `letta --backend local --new-agent --model anthropic/claude-sonnet-4-6`
- `letta/constants.py` — `PROVIDER_ORDER` includes `"anthropic": 2`
- letta-code repo has `CLAUDE.md` file

---

## Schema Fields

### schemaFields=10 ⚠️
- `letta/schemas/block.py:BaseBlock` — 15 fields total: `value`, `limit`, `project_id`, `template_name`, `is_template`, `template_id`, `base_template_id`, `deployment_id`, `entity_id`, `preserve_on_migration`, `label`, `read_only`, `description`, `metadata`, `hidden`
- Stripping template/cloud-specific fields leaves ~8 meaningful fields: `value`, `limit`, `label`, `read_only`, `description`, `metadata`, `tags` (+ `hidden`)
- `letta/schemas/memory.py:CreateArchivalMemory` — 3 fields: `text`, `tags`, `created_at`
- `letta/schemas/memory.py:ArchivalMemorySearchResult` — 4 fields: `id`, `timestamp`, `content`, `tags`
- **Verdict:** ~10 is approximately correct for the core Block model's meaningful fields, but depends heavily on what's counted.

---

## Corrections Summary

Claims that need correction in comparison table if Letta is added:

| Claim | Correct Value | Reason |
|-------|---------------|--------|
| entities | ❌ (not ✅) | No structured entity extraction |
| actions | ❌ (not ✅) | No action tracking |
| context | ❌ (not ✅) | No "why" metadata on memories |
| conflict | ❌ (not ✅) | No conflict detection |
| contentPreproc | ❌ (not ✅) | No preprocessing pipeline |
| narrative | ❌ (not ✅) | No narrative generation |
| recurrence | ❌ (not ✅) | No recurrence detection |
| supersede | ⚠️ partial | Replace exists but no formal supersede chains |

**Verified claims (8):** multiAgent, layeredMemory, timeTravel, fulltext, semantic, explicitForget, autoExtract, persona, p_claude
**Partially verified (2):** schemaFields=10 (~approx), supersede (partial)
**Not found (7):** entities, actions, context, conflict, contentPreproc, narrative, recurrence

---

## Vital Signs

| | Value |
|---|---|
| **Stars** | 23k (letta) + 2.6k (letta-code) |
| **Language** | Python (letta API) + TypeScript (letta-code CLI) |
| **License** | Apache 2.0 |
| **Single binary** | ❌ (npm package + Python server) |
| **Deployment** | Local CLI / Desktop App / Cloud (Constellation) |
| **Storage** | PostgreSQL (API) + git-backed MemFS (markdown) + vector DB (embeddings) |
| **Integration** | CLI, Desktop App, Telegram, Slack, Discord, MCP |
| **Formerly** | MemGPT (rebranded to Letta) |

---

## Sources

- `letta/schemas/memory.py` — Memory, BasicBlockMemory, ChatMemory, ContextWindowOverview, ArchivalMemory models
- `letta/schemas/block.py` — Block, BaseBlock, CreateBlock, Human, Persona
- `letta/schemas/agent.py` — AgentState, CreateAgent, multi-agent fields
- `letta/constants.py` — Tool definitions, provider list, memory tool constants
- `letta/functions/function_sets/base.py` — conversation_search, archival_memory_insert, archival_memory_search, memory tool, core_memory_append/replace, memory_replace/insert/rethink
- `letta/functions/function_sets/multi_agent.py` — send_message_to_agent* implementations
- https://docs.letta.com/letta-code/memory — Memory system documentation (MemFS, dreaming, layers)
- https://github.com/letta-ai/letta-code — Letta Code README (features, platform support)
- https://github.com/letta-ai/letta — Letta API README (architecture overview)

`evidence: "https://github.com/carsteneu/ai-memory-comparison/blob/main/evidence/letta.md"`
