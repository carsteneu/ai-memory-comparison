# Memanto Audit

> **Source**: https://github.com/moorcheh-ai/memanto (organization: moorcheh-ai, not moorcheh)
> **Audit date**: 2026-05-28
> **Stars at audit**: 232
> **Evidence**: README, docs.memanto.ai, memanto.ai homepage, arXiv paper 2604.22085, Hermes integration docs, temporal memory docs, memory types reference, daily workflows, CLI connect docs

---

## Description
MEMANTO is a memory agent — three primitives (remember, recall, answer) that give AI agents persistent semantic recall across sessions. Built on Moorcheh.ai's no-indexing information-theoretic search engine. TypeScript-like typed memory schema with 13 categories, sub-90ms retrieval, zero ingestion latency. Open source (MIT), self-hostable.

## Deployment
- Docker (`docker-compose up -d`)
- Python pip (`pip install memanto`)
- Cloud: AWS ECS, Google Cloud Run, Azure Container Instances
- Local: single machine

## Storage
Moorcheh.ai — serverless no-indexing semantic database. Data stored in Moorcheh cloud namespaces. Local server proxies to Moorcheh API. No local vector DB option documented.

## Integration
- CLI (`memanto` commands)
- REST API (local server on port 8000, session-based auth via JWT)
- MCP server (`integrations/mcp`) for any MCP-compatible client
- IDE/CLI connect targets: Claude Code, Codex, Cursor, Windsurf, Antigravity, Gemini CLI, Cline, Continue, OpenCode, Goose, Roo, GitHub Copilot, Augment Code
- Framework integrations: CrewAI, LangChain, LlamaIndex, n8n
- Agent plugins: Hermes (`hermes-memanto`), MemantoClaw (OpenClaw/NemoClaw)

## Setup
```bash
pip install memanto
memanto                        # prompts for Moorcheh API key
memanto agent create <name>    # create agent namespace
memanto remember "..."         # store memory
memanto recall "..."           # semantic search
memanto answer "..."           # RAG-grounded answer
```

## License
MIT

## Created
2026-03-23 (first GitHub commit)

## Docs URL
https://docs.memanto.ai

---

## Feature Matrix

### Architecture
| Feature | Present | Evidence |
|---------|---------|----------|
| webUi | **TRUE** | `memanto ui` — interactive browser dashboard; also web dashboard screenshots on memanto.ai |
| offline | **TRUE** | Self-hosted via Docker or pip; local REST API server; runs fully locally (only API key to Moorcheh cloud) |
| privacy | **TRUE** | Self-hosted, data stays local; credentials never persisted to config files (API key only in env); sandbox isolation in MemantoClaw |
| export | **TRUE** | `memanto memory export` — exports structured memory markdown; `memanto memory sync` — syncs MEMORY.md into projects |
| multiAgent | **TRUE** | Multi-agent namespaces via `memanto agent create/list/delete`; isolated memory per agent (separate Moorcheh namespaces); "Up to 5 agents" on free tier |
| llmFlex | **TRUE** | Built-in LLM proxy via Moorcheh API key (no separate LLM key needed); tested with Claude Sonnet 4 and Gemini 3; inference routing in MemantoClaw supports hot-swapping |

### Data Model
| Feature | Present | Evidence |
|---------|---------|----------|
| entities | **FALSE** | No entity extraction or entity tracking. No knowledge graph. Architecture is explicitly "not graph-based" |
| actions | **FALSE** | No action/event tracking as a first-class concept beyond the `event` memory type (which is just a category label) |
| keywords | **TRUE** | `tags` field on memory objects — arbitrary tag strings for filtering (see Remember API body: `tags` array) |
| context | **TRUE** | `context` is one of the 13 memory types ("Situational info"); contextual information stored as typed memories |
| source | **TRUE** | `source` field (e.g. `agent`, `user`) + `provenance` metadata with 6 values: `explicit_statement`, `inferred`, `corrected`, `validated`, `observed`, `imported` |
| emotional | **FALSE** | No emotional valence, sentiment, or mood tracking found anywhere in docs or API |
| conflict | **TRUE** | `memanto conflicts` CLI; `POST .../recall/conflicts` for listing; `POST .../resolve-conflict` for resolution; "Catches and flags conflicting information immediately" |
| layeredMemory | **TRUE** | 13 typed memory categories separating episodic (event, observation), semantic (fact, preference, decision, goal), procedural (instruction, error); explicitly designed for typed/hierarchical memory |
| timeTravel | **TRUE** | Three temporal query modes: `recall/as-of` (point-in-time), `recall/changed-since` (differential), `recall/recent` (newest-first); ISO 8601 timestamps |
| schemaFields | **7** | Content, type (13 values), title, confidence (0.0-1.0), tags (array), source (string), provenance (6 values). Plus system fields: memory_id, agent_id, session_id, namespace, status, created_at |

### Search
| Feature | Present | Evidence |
|---------|---------|----------|
| fulltext | **TRUE** | Moorcheh's "exact search" engine — deterministic, not approximate; information-theoretic retrieval with exact matching semantics |
| semantic | **TRUE** | Core feature: semantic search via Moorcheh engine; "Query for 'How should we contact the user?' matches 'User prefers email communication' without keyword overlap" |
| hybrid | **FALSE** | No hybrid (BM25+vector) search mentioned. Moorcheh uses information-theoretic search, not traditional hybrid approach |
| deep | **FALSE** | No multi-depth or iterative search; single-query retrieval with dynamic k (up to 100 chunks at adjustable threshold) |
| codeGraph | **FALSE** | Explicitly NOT graph-based. Paper: "challenging the prevailing assumption that knowledge graph complexity is necessary" |
| docsSearch | **TRUE** | `memanto upload` supports .pdf, .docx, .xlsx, .json, .txt, .csv, .md — content chunked and made instantly searchable via recall |
| factQuery | **TRUE** | Query by type filter, temporal queries, provenance filter, confidence filter; CLI: `--type preference`, `--as-of`, `--changed-since` |
| timeline | **TRUE** | Three temporal query endpoints: point-in-time (`as-of`), change-range (`changed-since` with `change_type` field), recency (`recent`); memory versioning with `status` field tracking supersession |
| searchModes | **5** | standard recall (semantic), recall/as-of (temporal point-in-time), recall/changed-since (differential temporal), recall/recent (recency), answer (RAG-grounded synthesis) |

### Lifecycle
| Feature | Present | Evidence |
|---------|---------|----------|
| decay | **TRUE** | "Prioritizes new info — new information always outranks older, stale notes"; recency signals; temporal queries for freshness filtering |
| supersede | **TRUE** | Conflict resolution marks older memories as `superseded`; versioning with `status` field (`active`/`superseded`); `updated_at` tracking with `change_type` |
| contradiction | **TRUE** | `memanto conflicts` — automated conflict detection; `POST .../resolve-conflict` — interactive resolution; "Catches and flags conflicting information immediately" |
| quarantine | **FALSE** | No quarantine or sandbox mechanism for suspicious/isolated memories found |
| autoResolve | **FALSE** | Conflicts are resolved interactively (`memanto conflicts` with manual resolution). No automatic conflict resolution documented |
| trustModel | **TRUE** | Confidence scores (0.0–1.0) on every memory; provenance tracking (6 values); "distinguish between explicitly stated facts, inferred patterns, and potentially outdated information" |
| explicitForget | **FALSE** | No individual memory deletion endpoint. Docs explicitly state: "DON'T delete old memories — let conflict resolution mark them superseded." Only agent-level deletion via `DELETE /api/v2/agents/{agent_id}` |

### Extraction
| Feature | Present | Evidence |
|---------|---------|----------|
| autoExtract | **TRUE** | Hermes integration: auto-recall (injects relevant memories before each turn), turn capture (stores meaningful turns as `event` memories), memory mirroring (echoes built-in memory writes). Not in core Memanto, but in ecosystem |
| contentPreproc | **TRUE** | File upload chunking (.pdf/.docx/.xlsx → searchable text); Hermes plugin sanitizes `<memanto-memory>` delimiters from stored content; turn capture skips trivial acknowledgements |
| dedup | **FALSE** | No deduplication mechanism documented. Conflict detection catches contradictions but not duplicates |
| qualityRefine | **FALSE** | No quality scoring, refinement, or ranking of memory quality beyond confidence scores |
| narrative | **TRUE** | `memanto daily-summary` — compiles all day's memories into a summary; `memanto agent bootstrap` — generates intelligence snapshot. Hermes: RAG answers synthesize memories into narratives |
| clustering | **FALSE** | No memory clustering or grouping beyond the 13 type categories |
| recurrence | **TRUE** | `memanto schedule enable` — scheduled daily summaries; cron job examples for backups; Hermes: background thread warmup with cooldown-and-retry pattern |
| persona | **TRUE** | Hermes: profile isolation via `agent_id: hermes-{identity}` per profile; `preference` memory type; personality/identity scoping. Not a standalone persona extraction feature |

### Platform Support
| Feature | Present | Evidence |
|---------|---------|----------|
| p_claude | **TRUE** | `memanto connect claude-code` — installs CLAUDE.md + memanto-memory skill |
| p_codex | **TRUE** | `memanto connect codex` — OpenAI Codex CLI target |
| p_opencode | **TRUE** | `memanto connect opencode` — OpenCode CLI target |
| p_gemini | **TRUE** | `memanto connect gemini-cli` — Google Gemini CLI target |
| p_copilot | **TRUE** | `memanto connect github-copilot` — GitHub Copilot target |
| p_cursor | **TRUE** | `memanto connect cursor` — Cursor IDE target |
| p_windsurf | **TRUE** | `memanto connect windsurf` — Windsurf IDE target |
| p_openclaw | **TRUE** | MemantoClaw — dedicated reference stack for OpenClaw/NemoClaw. `memantoclaw onboard` provisions OpenClaw + OpenShell sandbox with Memanto memory bridge |
| p_hermes | **TRUE** | `hermes-memanto` PyPI package; dedicated Hermes agent memory provider with auto-recall, turn capture, and explicit tools |
| p_pi | **FALSE** | No Pi (Inflection) integration found anywhere in docs, integrations directory, or connect targets |
| p_antigravity | **TRUE** | `memanto connect antigravity` — Google Antigravity target |
| Additional | — | Also supports: Cline, Continue, Goose, Roo, Augment Code, MCP (universal), CrewAI, LangChain, LlamaIndex, n8n |

### Benchmarks
| Feature | Present | Evidence |
|---------|---------|----------|
| b_locomo | **TRUE** | 87.1% overall (SOTA). Breakdown: Open Domain 92.4%, Temporal 85.4%, Single-Hop 78.7%, Multi-Hop 70.8% |
| b_longmemeval | **TRUE** | 89.8% overall (SOTA). Breakdown: Single-session User 95.7%, SS Assistant 100%, SS Preference 93.3%, Knowledge Update 93.6%, Temporal Reasoning 88.0%, Multi-session 81.2% |
| b_personamem | **FALSE** | No PersonaMem benchmark results mentioned in paper, research page, or documentation |
| b_token | **FALSE** | No token efficiency benchmark or cost-per-operation metrics published |
| b_methodology | **TRUE** | 5-stage progressive ablation study detailed in paper (arXiv 2604.22085): Naive RAG (56.6%/76.2%) → Relaxed Retrieval k=40 (77.0%/82.8%) → Optimized Prompts (79.2%/82.9%) → Dynamic Retrieval k=100 (85.0%/86.3%) → Gemini 3 Inference (89.8%/87.1%). "13 Pages, 10 Tables, 8 Figures" |

### Comparative Notes
- **Rivals compared**: Mem0 (66.9% LoCoMo), Mem0 G (68.4% LoCoMo), Zep (75.1% LoCoMo, 71.2% LongMemEval), Letta (74.0% LoCoMo), LangMem (58.1% LoCoMo), EmergenceMem (86.0% LongMemEval), Supermemory (85.2% LongMemEval), Memobase (75.8% LoCoMo)
- Memanto outperforms all evaluated systems on both LoCoMo and LongMemEval with a vector-only architecture (no graph databases)
- All competing systems use either Graph+Vector or full-context architectures, many requiring multi-query retrieval pipelines
- Memanto achieves SOTA with single-query retrieval and zero ingestion cost
