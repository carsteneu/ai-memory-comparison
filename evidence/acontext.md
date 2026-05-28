# Acontext — Evidence

> Every ✅ claim backed by public README, docs (docs.acontext.io), or source references.
> Repo: [memodb-io/Acontext](https://github.com/memodb-io/Acontext) (3,500 stars, JS/TS/Go/Python, Apache-2.0)
> Version: sdk-ts v0.1.21 (Apr 2026); 279 releases total.

---

## Repository Metadata

- **description**: "Agent Skills as a Memory Layer"
- **deployment**: Cloud API (acontext.io) + self-hosted Docker via `acontext server up` CLI
- **storage**: PostgreSQL, pgvector, Redis, RabbitMQ, S3 (MinIO-compatible)
- **integration**: REST API + Python SDK (pypi: `acontext`) + TypeScript SDK (npm: `@acontext/acontext`) + Claude Code Plugin + OpenClaw Plugin + CLI (`acontext-cli`)
- **setup**: `curl -fsSL https://install.acontext.io | sh` for CLI; Docker-compose for self-hosted backend; pip/npm for SDKs
- **license**: Apache-2.0 (memodb-io, 2026)
- **created**: n/a (not stated in README; repo has 1,080 commits, 279 releases across components)
- **docs**: https://docs.acontext.io

---

## Architecture

### deployment ✅
- `README.md` — Cloud: "Go to Acontext.io, claim your free credits. Go through a one-click onboarding to get your API Key"
- `README.md` — Self-hosted: "curl -fsSL https://install.acontext.io | sh", "mkdir acontext_server && cd acontext_server", "acontext server up"
- Docker compose orchestration with PostgreSQL, Redis, RabbitMQ, S3
- API: Go + Gin + GORM, Dashboard: web at localhost:3000

### storage ✅
- `README.md` architecture diagram: PostgreSQL, S3, Redis, RabbitMQ
- `AGENTS.md` — "API: Go + Gin + GORM/PostgreSQL + Redis + RabbitMQ + S3 + OpenTelemetry + Swagger"
- `AGENTS.md` — "CORE: Python + FastAPI + SQLAlchemy/PostgreSQL + pgvector + Redis + RabbitMQ + S3 + OpenAI/Anthropic + OpenTelemetry"
- `settings/core` — Configurable embedding dimensions, providers (OpenAI, Jina), pgvector for vectors

### proxy ❌
- No proxy/interceptor. Acontext is an API-based SDK service. Agents send messages via `store_message()`, skills are retrieved via tool calls. No evidence of intercepting or modifying the LLM conversation stream in-flight.

### webUi ✅
- `README.md` — "Dashboard: Web Dashboard localhost:3000" architecture diagram
- `README.md` — Screenshot of dashboard onboarding UI
- `docs/observe/dashboard` — Full dashboard page with Metrics (BI analytics), Traces (distributed traces viewer), Messages viewer, Artifacts (tree view), Tasks (status tracking), Skills viewer
- `AGENTS.md` — "Dashboard: dashboard/" (commercial) and "Dashboard (OSS): src/server/ui/" (open-source)

### offline ✅
- `settings/core` — Documents Ollama local setup: "LLM_BASE_URL=http://localhost:11434/v1", "LLM_SIMPLE_MODEL=qwen3:8b", local embedding with "qwen3-embedding:0.6b"
- Self-hosted mode via `acontext server up` with Docker — runs entirely on local infrastructure
- Caveat: requires Docker daemon running locally; not a single binary but fully local after image pull

---

## Data Model

### entities ❌
- No structured entity extraction (files, people, systems as separate DB fields or tables). Skill files are Markdown — SKILL.md schemas can define "one file per person" but entity extraction is user-defined file organization, not automated structured extraction with separate entity fields/tables. Task tracking extracts task_description and user_preferences as strings, not as named entity records.

### actions ❌
- No structured action/operation extraction as separate fields. Task tracking extracts "progresses" (step-by-step descriptions like "Built Docker image") but these are free-text progress strings, not first-class structured action records with typed verbs or queryable action tables.

### keywords ❌
- Skill SKILL.md files can include a `keywords` frontmatter field (e.g., "memory, context, skills"). This is manual metadata on skills themselves, not an extracted keyword/tag system for individual memory entries or learned facts.

### anticipatedQueries ❌
- No evidence of generating predicted search queries for memory entries to improve retrieval recall.

### triggerRules ❌
- No condition-based activation. Skills are retrieved purely via agent-initiated tool calls (`get_skill`, `get_skill_file`) — no "show when file X opened" or deadline-based trigger rules. The roadmap mentions integrations but no trigger mechanism.

### domainTag ❌
- Learning spaces support `filter_by_meta={"domain": "deployments"}` but this is user-applied metadata on spaces, not an automated domain classification system (code, marketing, legal, etc.) for individual memories.

### taskType ✅
- `docs/observe/whatis` — Tasks are classified by status: "pending, running, success, or failed"
- `docs/observe/agent_tasks` — "Each distinct request the user makes becomes a separate, trackable task"
- `docs/observe/task_eval_criteria` — Custom evaluation criteria for success/failure classification
- This qualifies as task type classification (pending/running/success/failed), matching the CRITERIA.md definition

### context ❌
- Skill files capture "what happened" (steps, resolution) but do not store an explicit "why this is relevant" field alongside memory content. The SKILL.md guidelines instruct "Only record information explicitly mentioned" — no separate context/relevance field.

### source ❌
- Messages stored via `store_message()` carry `role` (user/assistant/tool) and `format` (openai/anthropic/gemini) but there is no 3+ level source attribution system (e.g., user_stated > agreed_upon > claude_suggested). Role is a conversation participant marker, not a memory source taxonomy.

### originTrust ❌
- No trust weighting based on capture origin. No evidence of different trust scores for user-stated vs. agent-suggested vs. extracted knowledge.

### emotional ❌
- No sentiment or emotional intensity tracking per memory or session.

### conflict ❌
- No contradiction detection between stored memories.

### layeredMemory ❌
- No fixed hierarchical memory structure (L0 raw → L1 summary → L2 persona). Learning spaces organize skills by name but this is flat file organization, not a layered abstraction hierarchy. Default skills (daily-logs, user-general-facts) are two independent skills, not layers.

### timeTravel ❌
- No historical state browsing, temporal search (since/before), or versioned memory entries. `acontext_session_history` returns recent task summaries but has no temporal filter parameters.

### schemaFields (count: ~12) ✅
- **Task fields** (6): `task_description`, `status` (pending/running/success/failed), `progresses` (array), `user_preferences` (array), `order` (integer), `linked_messages` (message IDs)
- **Message fields** (3): `role` (user/assistant/tool), `content` (blob), `format` (openai/anthropic/gemini)
- **Skill fields** (4): `name`, `description`, `keywords`, `version`
- **Session fields** (2): `user` identifier, `created_at`
- Total distinct structured fields: ~12-15 across the three domains (tasks, skills, sessions)

---

## Search & Retrieval

### fulltext ✅
- SKILL.md (acontext-installer) documents `acontext_search_skills` MCP tool: "Search through skill files by keyword"
- OpenClaw plugin also includes `acontext_search_skills`: "Search through skill files by keyword"
- This is keyword-based full-text search over learned skill files — qualifies as full-text search

### semantic ❌
- No embedding-based semantic search of stored memories. pgvector exists in the stack but is used by the learning pipeline internally, not exposed as a search mode. Roadmap item: "Session search: support session search by embedding similarity" — still a TODO.
- Core settings configure embedding models (`text-embedding-3-small`, `jina`) but no semantic search tool is documented.

### hybrid ❌
- No hybrid search combining full-text and vector search with result fusion.

### deep ❌
- No search of model thinking/reasoning traces. Messages store tool calls and results but not model chain-of-thought.

### codeGraph ❌
- No code structure indexing (no Tree-sitter, AST, or code graph). Acontext is agent memory, not a code analysis tool.

### docsSearch ❌
- No dedicated documentation search across ingested framework/API docs.

### factMetadataQuery ❌
- No structured queries on memory metadata. You can `list_skills()`, `get_tasks()` but not query by entity, action, category, or domain. No WHERE-clause-style filtering beyond `filter_by_meta` on learning spaces.

### timeline ❌
- `acontext_session_history` returns recent task summaries but no `since`/`before` parameters or timeline browsing.

### searchModes (count: ~4) ✅
1. `acontext_search_skills` — keyword search of skill files (MCP tool)
2. `acontext_session_history` — task summary retrieval from recent sessions
3. `get_tasks` / `list_skills` — structured listing with pagination (`limit` parameter)
4. `get_skill` / `get_skill_file` — direct file access by name/path

### dataSources (count: ~4)
1. **Skills** — learned Markdown skill files (default + custom)
2. **Sessions** — stored messages with role/content/format + extracted tasks with status
3. **Disk** — S3-backed persistent file storage for agents (read/write/list)
4. **Sandbox** — isolated execution environments (bash, Python, code execution)

---

## Knowledge Lifecycle

### decay ❌
- No automatic relevance decay or forgetting based on time, disuse, or engagement signals.

### supersede ❌
- Skills can be re-uploaded (overwritten) but no explicit "mark A as replacing B" mechanism with a traceable version chain. `get_learnings(history=true)` style functionality not present.

### contradictionDetect ❌
- No automatic contradiction detection between stored memories.

### quarantine ❌
- No mechanism to exclude a session's memories from retrieval without deleting them.

### autoResolution ❌
- No automatic resolution/archival of stale items after TTL. Tasks remain in their extracted state indefinitely.

### trustModel ❌
- No multi-tier trust hierarchy where some sources override others.

### explicitForget ✅
- `docs/store/skill` — `client.skills.delete(skill.id)` — delete a skill
- `docs/learn/learning-spaces` — `client.learning_spaces.delete(space.id)` — delete a learning space (skills and sessions preserved)
- `docs/learn/learning-spaces` — `client.learning_spaces.exclude_skill(space.id, skill_id=...)` — remove skill from space
- Multiple explicit deletion mechanisms available

---

## Extraction Pipeline

### autoExtraction ✅
- `docs/observe/whatis` — "Automatic task extraction, progress recording, and status detection from agent conversations — zero instrumentation"
- `README.md` — "Task complete or failed — When a task is marked done or failed... that outcome is the trigger for learning"
- `README.md` — "Distillation — An LLM pass infers from the conversation and execution trace what worked, what failed, and user preferences"
- Task extraction runs automatically from buffered messages (buffer_max_turns or 8s idle timeout)
- Skill learning runs automatically after task completion (background, async)

### contentAwarePreproc ❌
- No content-type-aware preprocessing at extraction time. Message buffer flushes by turn count or timeout. Context editing strategies (token_limit, remove_tool_result, middle_out) are retrieval-side, not preprocessing for extraction.

### deduplication ✅
- `docs/security/encryption` — "Deduplication is disabled for encrypted projects. Each object is encrypted with a unique DEK, so identical content produces different ciphertext. This may increase storage usage."
- This statement confirms deduplication EXISTS for non-encrypted projects. The caveat that encryption disables it implies dedup is the default behavior.

### qualityRefinement ❌
- No LLM-based or rule-based quality pass described. The distillation step creates skill files but there's no confidence scoring, contradiction checking, or quality validation pass.

### narrative ✅
- `docs/engineering/session_summary` — "Session Summary: Compact task summary for prompts" — generates XML-format summaries with task descriptions, progress steps, and user preferences
- `docs/learn/e2e-demo` — Distillation pipeline: "report_success_analysis (SOP)", "report_factual_content", "report_failure_analysis (anti-pattern)" — generates narrative SOPs from completed tasks
- `docs/learn/learning-spaces` — Default skills: "daily-logs: Daily activity summaries — one file per day", "user-general-facts: User preferences and facts — one file per topic"
- `docs/learn/custom-memory` — Learner creates structured Markdown files (e.g., alice-chen.md with relationship, role, notes)

### clustering ❌
- No clustering of related memories by topic, embedding similarity, or semantic relationship.

### recurrence ❌
- No automated detection of recurring patterns across sessions. The E2E demo demonstrates agent-initiated recall of learned patterns (tool-based), not automated recurrence detection surfacing "this has happened before."

### persona ✅
- `docs/learn/learning-spaces` — Default skill: "user-general-facts: User preferences and facts — one file per topic"
- `docs/observe/agent_tasks` — Task data includes `user_preferences`: "User requirements mentioned" extracted automatically
- `docs/learn/custom-memory` — social-contacts skill captures relationship, role, company, preferences per person
- Combined: automatic extraction of user preferences + persistent user profile skill = persona extraction

---

## Platform Support

### p_claudeCode ✅
- `SKILL.md` (acontext-installer) — Full Claude Code installation guide: "/plugin marketplace add memodb-io/Acontext", "/plugin install acontext"
- `SKILL.md` — Claude Code MCP tools: `acontext_search_skills`, `acontext_get_skill`, `acontext_session_history`, `acontext_stats`, `acontext_learn_now`
- `SKILL.md` — Claude Code configuration: `ACONTEXT_USER_IDENTIFIER`, `ACONTEXT_BASE_URL`, `ACONTEXT_SKILLS_DIR`, `ACONTEXT_AUTO_CAPTURE`, etc.
- `AGENTS.md` — "Claude Code Plugin: run `npm run release -- X.Y.Z` in `src/packages/claude-code/`", CI workflow `package-release-claude-code.yaml`
- `README.md` — "Claude Code: Read https://acontext.io/SKILL.md and follow the instructions"

### p_codex ❌
- Not mentioned in README, docs, or source tree.

### p_openCode ❌
- `ROADMAP.md` — Listed under "Integration" as unchecked TODO: `[ ] OpenCode`

### p_gemini ❌
- Not mentioned. Messages support Gemini format storage (`format: "gemini"`) but no platform-specific integration.

### p_copilot ❌
- Not mentioned.

### p_cursor ❌
- `docs/llm_quick` — Mentions "Cursor" as "any coding agent" for llms.txt consumption, but no dedicated integration (plugin, MCP, hook). Does not qualify as documented platform integration.

### p_windsurf ❌
- Same as Cursor — mentioned generically in llm_quick, no dedicated integration.

### p_openClaw ✅
- `README.md` — "OpenClaw: Read https://acontext.io/SKILL.md and follow the instructions to install and configure"
- `SKILL.md` — Full OpenClaw installation: "openclaw plugins install @acontext/openclaw", config in `openclaw.json`
- `SKILL.md` — OpenClaw MCP tools: `acontext_search_skills`, `acontext_session_history`, `acontext_learn_now`
- `SKILL.md` — OpenClaw CLI: `openclaw acontext skills`, `openclaw acontext stats`
- `AGENTS.md` — "OpenClaw Plugin: src/packages/openclaw/ (npm: @acontext/openclaw)"

### p_hermes ❌
- Not mentioned.

### p_piOmp ❌
- Not mentioned.

### p_antigravity ❌
- Not mentioned.

---

## Benchmarks

### locomo ❌
- No published LoCoMo benchmark score or methodology.

### longMemEval ❌
- No published LongMemEval(-S) benchmark score or methodology.

### personaMem ❌
- No published PersonaMem benchmark score or methodology.

### tokenReduction ✅
- `docs/learn/e2e-demo` — Demonstrated improvement: "Act 1 (no prior knowledge): 9-12 DevOps tool calls; Act 2 (with learned skills): 4-6 DevOps tool calls; Improvement: ~40-55% fewer tool calls"
- `docs/engineering/editing` — Context editing with token_limit strategy: explicit token management for context window reduction
- `docs/engineering/session_summary` — Session summaries as token-efficient prompt compression
- Multiple documented token/call reduction mechanisms with measured results

### methodologyOpen ❌
- The E2E demo is documented with full runnable Python/TypeScript code, but it uses a mock environment (not a standard benchmark) and the 40-55% reduction is an illustrative demo result, not a published benchmark with standard methodology. No benchmark methodology that is reproducible with standard datasets.

---

## Summary

| Category | ✅ | ❌ | Coverage |
|----------|----|----|----------|
| Architecture | 4/5 | 1/5 | 80% |
| Data Model | 2/15 | 13/15 | 13% |
| Search & Retrieval | 2/10 | 8/10 | 20% |
| Knowledge Lifecycle | 1/7 | 6/7 | 14% |
| Extraction Pipeline | 5/8 | 3/8 | 63% |
| Platform Support | 2/11 | 9/11 | 18% |
| Benchmarks | 1/5 | 4/5 | 20% |

**Total: 17/61 features present (28%)**

Acontext's core strength is its **extraction pipeline** (auto-extraction, deduplication, narrative generation, persona extraction) and **platform integration** for Claude Code and OpenClaw. Its memory model is intentionally minimal — storage is flat Markdown files, retrieval is tool-based (no embedding search, no hybrid, no temporal queries), and data model is thin. The philosophy is "Skill is All You Need" — structured files over structured databases.
