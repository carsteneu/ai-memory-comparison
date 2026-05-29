# Membase — Evidence

> Every ✅ claim backed by website, docs, or changelog references.
> **Closed-source SaaS.** No public GitHub repository. All evidence from [membase.so](https://membase.so) and [docs.membase.so](https://docs.membase.so).
> Company: Aristo Technologies, Inc. (Delaware, US)

---

## Repository Metadata

- **description**: "Make your agents truly understand you" — universal memory layer for AI agents
- **deployment**: SaaS (Cloud) at app.membase.so; remote MCP server at mcp.membase.so/mcp; npm package `membase`
- **storage**: Neo4j (knowledge graph) + Supabase (RLS, JWT auth) + vector embeddings
- **integration**: MCP (remote, Streamable HTTP + OAuth), Claude Code plugin, OpenClaw plugin, Hermes plugin, generic MCP URL
- **setup**: SaaS signup at app.membase.so, then `npx -y membase@latest --client <agent>` or plugin install
- **license**: Proprietary (Aristo Technologies, Inc. — Terms of Service at membase.so/terms, last updated Dec 28, 2025)
- **created**: ~late 2025 (Terms: Dec 28, 2025; earliest changelog: v0.2.0 on Feb 20, 2026; open beta: v0.5.0 on May 19, 2026)
- **docs**: https://docs.membase.so

---

## Architecture

### webUi ✅
- Landing page + pricing page: dashboard screenshots showing graph view, table view, wiki editor, chat interface
- Docs /features/memory: "The Memories tab in the dashboard offers two views for browsing your knowledge: Graph View and Table View"
- Docs /features/wiki: "Wiki documents are markdown files", with editor, graph view, table view
- Docs /features/chat: Chat in Dashboard with citations, graph panel, session history
- Docs /use-context: Dashboard tabs — Agents, Sources, Recipes, Settings (Profile + Billing)

### offline ❌
- Docs /features/membase-mcp: MCP server at `https://mcp.membase.so/mcp` — remote, not local
- Architecture diagram shows cloud service between agent and storage
- No local/offline mode mentioned anywhere in docs or landing page
- All data flows through Membase Cloud API

### privacy ✅
- Privacy page (membase.so/privacy): "Encrypted at rest and in transit", "No model training on your data", "Delete anytime"
- TLS 1.3 in transit, AES-256 at rest, AES-256-GCM application-level for OAuth credentials
- "Zero Data Retention API tiers with LLM providers" — ZDR-tier agreements
- Row-Level Security (RLS) on all user tables, per-user graph isolation, JWT auth
- Privacy page "What we are building": SOC 2 Type II, BYOK encryption (Enterprise), audit logging

### export ✅
- Privacy page: "Export or delete your data at any time. You control what stays in Membase"
- Docs /features/chat: "Export chat: Download a conversation as Markdown for sharing or archiving" (changelog v0.5.0)
- No explicit full-data-export mechanism documented beyond chat export, but privacy page claims data export rights

### multiAgent ✅
- Docs index: "Cross-agent sharing: Context stored by one agent is available to other connected agents on your account"
- Landing page: "Give your agents context beyond sessions" — shows ChatGPT, Claude, Gemini, Codex, Cursor, VS Code, OpenCode, OpenClaw, Poke
- Docs /core-concepts/attached-vs-universal: dedicated page explaining universal (shared) vs attached memory
- Docs /quickstart: "The same agent can also write and search factual knowledge via add_wiki and search_wiki"

### llmFlex ❌
- No provider flexibility documented. Chat has "model picker" (Standard vs Advanced models) but no user-controlled provider selection
- LLM digesting is internal to Membase, not user-configurable
- No mention of BYOK or custom API keys for processing

### cacheOptimization ❌
- No mention of token optimization, context window management, or cache strategies

### proceduralMemory ❌
- No tool/workflow recording or execution memory. Memory stores preferences/decisions, not action sequences

### sandboxed ❌
- No sandboxed execution mentioned. SaaS-only with no local execution mode.

### scheduled ❌
- App integrations (Gmail, Calendar, Slack) sync automatically in background
- Docs /how-membase-works: "Connected sources... sync new data automatically in the background. Each message, event, or email becomes an episode"
- But this is background sync, not scheduled/autonomous agent triggering. No cron-like job system for agents.

### export_data ✅
- Privacy page: "Export or delete your data at any time"
- Chat export to Markdown documented (changelog v0.5.0)
- Full data export claim exists but mechanism not publicly documented

### setup_simple ✅
- Docs /quickstart: 3-step guide — create account, connect agent (one-click or single command), start using
- `npx -y membase@latest --client <agent>` for CLI setup
- One-click install for Cursor and VS Code from dashboard

### pricing ✅
- Pricing page: Free ($0) + Pro ($20/month)
- Free: limited memory searches, limited episodes, limited wiki docs (200), limited AI chats (40/month), MCP, imports, integrations
- Pro: unlimited memory searches, 5x more episodes, 10x more wiki docs (2,000), 5x more AI chats (200/month), advanced AI models, priority support

---

## Data Model

### entities ✅
- Docs /how-membase-works: "Membase identifies key entities from the episode: people, projects, tools, preferences, decisions, dates, and other meaningful concepts"
- Docs /features/memory: "Entity-centric visualization: Each node represents an entity extracted from your memories"
- Docs /quickstart: `add_memory` example: "Extracts entities: TypeScript, Bun, Next.js, Supabase"
- Entities auto-extracted and displayed in knowledge graph

### actions ❌
- Entities are extracted as concepts, but no explicit action/verb schema (e.g., "uses", "works_on", "decided")
- Relationship edges exist between entities but no typed action system documented

### keywords ✅
- Docs /features/membase-mcp: `add_memory` has `project` parameter — "lightweight category/tag slugs (up to 60 characters)"
- Docs /features/memory: "Projects are lightweight category tags for memories"
- Wiki: Collections serve as organizational folders for wiki documents
- Source attribution acts as additional tagging (Cursor, Claude, Gmail, Slack, etc.)

### anticipated_queries ❌
- No explicit anticipated-queries field in any documented schema
- No mention of pre-registering search queries

### trigger_rules ❌
- No explicit trigger rule system. Profile instructions can guide agent behavior but no declarative trigger system
- Docs /features/memory: "If you want certain projects to be applied automatically, add a rule in your profile instructions" — but this is agent-prompt guidance, not a trigger engine

### domain ✅
- `project` field serves as domain/topic categorization
- `sources` field categorizes by origin (Gmail, Slack, Cursor, Claude, etc.)
- Wiki collections for document organization

### taskType ✅
- `project` field doubles as task/project-type classification
- Memories can be moved between projects from dashboard

### context ❌
- No explicit "why was this stored" or context field
- Episodes capture content + entities but no rationale/context field

### sourceAttribution ✅
- Docs /features/memory: Table view includes source tags
- Docs /features/membase-mcp: `search_memory` `sources` parameter supports filtering by Slack, Gmail, Google Calendar, Cursor, Claude, Claude Code, VS Code, ChatGPT, Codex, Gemini CLI, OpenCode, Poke, OpenClaw, Hermes, and imports
- Docs /changelog v0.2.0: "Memory source tracking (Cursor, ChatGPT, Calendar, and more)"

### origin_trust ❌
- No trust scoring per source. Conflict resolution is time-based: "latest data takes priority"
- No provenance trust model documented

### emotional ❌
- No emotional/sentiment tracking mentioned anywhere

### conflict ✅
- Docs /features/memory: "When new information contradicts an existing memory, the latest data takes priority"
- Docs /how-membase-works: "Conflict resolution: When new information contradicts an existing memory, the latest data takes priority"
- Old memories flagged as outdated when superseded

### layeredMemory ✅
- Two distinct stores: Memory (personal context, knowledge graph) + Wiki (factual knowledge, markdown documents)
- Docs /features/membase-mcp: "Memory vs Wiki" comparison table
- Docs index: "Two knowledge stores: Memory and Wiki"
- Memory: episodes + entities in knowledge graph. Wiki: markdown documents with wikilinks, organized in collections.

### timeTravel ❌
- No version history, snapshot, or time-travel feature documented
- No git-like branching or rollback
- Wiki documents have no edit history mentioned

### schemaFields
- Memory: content (text, max 50K), project (slug, max 60), metadata (reserved), source, timestamp, entities
- Wiki: title, content (markdown, max 100K), collection, doc_id (UUID)
- Profile: display_name, role, interests, instructions, timezone
- Approximate schema fields: ~8-10 distinct fields across memory and wiki
- Not as rich as systems with dedicated learning abstractions

---

## Search & Retrieval

### fulltext ✅
- Docs /features/wiki: "hybrid search that combines full-text keyword matching (BM25-style) with semantic similarity"
- Wiki search explicitly uses BM25 for keyword queries

### semantic ✅
- Docs /features/membase-mcp: `search_memory` — "Searches stored memories by semantic similarity"
- Docs /features/membase-mcp: Results include "relevance score (0–1)"
- Wiki search also includes semantic embedding component

### hybrid ✅
- Docs /features/wiki: "hybrid search that combines full-text keyword matching (BM25-style) with semantic similarity and fuses the results with Reciprocal Rank Fusion (RRF)"
- Docs /features/membase-mcp: `search_wiki` — "hybrid search: a full-text keyword index (BM25-style) and semantic similarity, fused with Reciprocal Rank Fusion (RRF)"
- Memory search is semantic-only; Wiki search is hybrid

### deepSearch ❌
- No mention of searching over agent thinking/reasoning traces
- No "deep search" beyond content — no chain-of-thought or reasoning capture

### codeGraph ❌
- No code graph or AST-based search
- No software engineering-specific features

### docsSearch ✅
- Full documentation site at docs.membase.so with llms.txt for AI-readable indexing
- Docs are indexed and searchable

### factMetadataQuery ✅
- Docs /features/membase-mcp: `search_memory` supports filtering by `sources`, `project`, `date_from`, `date_to`, `timezone`, `limit`, `offset`
- Dashboard: filter by source, project, time range
- Wiki: filter by collection, sort by title/date
- Entity search in graph view

### timeline ✅
- Docs /features/membase-mcp: `membase://recent` resource — "Top 10 recent memories, ordered by event time"
- Table view: sort by date, filter by time range (Today, This Week, This Month, etc.)
- Chat "Session history: Past conversations are saved in the sidebar"

### searchModes
- `search_memory` (semantic): for personal context
- `search_wiki` (hybrid BM25+semantic RRF): for factual knowledge
- `membase://recent` (timeline): recent memories resource
- `membase://profile` (static): user profile resource
- Chat with Memory: combines both stores
- **Count: 3** distinct search entry points (memory, wiki, recent) via MCP tools/resources

### dataSources
- Agent conversations (live via MCP)
- Chat history import (ChatGPT, Claude, Gemini)
- App integrations: Gmail, Google Calendar, Slack
- Obsidian vault import (wiki)
- Chat in Dashboard
- **Count: 5** distinct external data source types

---

## Knowledge Lifecycle

### decay ❌
- No time-based decay/forgetting function
- Old memories are flagged as outdated when superseded by newer contradictory info, but this is replacement, not decay
- No Ebbinghaus or spaced-repetition model

### supersede ✅
- Docs /features/memory: "When existing context becomes outdated, your agent calls `add_memory` to register the updated information and flags the old memory as outdated"
- Docs /how-membase-works: "When new information contradicts an existing memory, the latest data takes priority"
- Explicit supersede mechanism via add_memory + outdated flag

### contradiction ✅
- Docs /features/memory: "Conflict resolution: When new information contradicts an existing memory, the latest data takes priority"
- Deduplication and merging also mentioned
- Docs /how-membase-works: "Deduplication: Similar memories from different sources are merged to avoid redundancy"

### quarantine ❌
- No quarantine or isolation of suspect memories
- Delete is the only removal mechanism

### autoResolution ✅
- Docs /features/memory: "Deduplication: Similar memories from different sources are merged"
- Docs /features/memory: "Conflict resolution: When new information contradicts an existing memory, the latest data takes priority"
- Docs /features/memory: "Relationship updates: New connections between entities are added to the knowledge graph as they are discovered"
- Automated merging, conflict resolution, and graph updating

### trustModel ❌
- No explicit trust scoring model
- Time is the primary signal (latest wins)
- No source-level trust weighting documented

### explicitForget ✅
- Docs /features/memory: "Delete a single memory" from table view
- Docs /features/memory: "Delete multiple memories" via bulk selection
- Docs /features/memory: "Delete all memories from a source" on Sources page
- Docs /features/wiki: Delete wiki documents (single, bulk, agent via `delete_wiki`)
- "Deleted memories cannot be recovered"

---

## Extraction Pipeline

### autoExtract ✅
- Docs /how-membase-works: "Membase identifies key entities from the episode: people, projects, tools, preferences, decisions, dates, and other meaningful concepts"
- Docs /quickstart: `add_memory` automatically "Extracts entities: TypeScript, Bun, Next.js, Supabase"
- Docs /how-membase-works: Full pipeline: episode creation → entity extraction → graph construction → dedup/merge
- Docs index: "Smart digesting: Raw conversations are automatically processed into structured, retrievable memories"
- Chat history import goes through same pipeline as live conversations

### contentPreproc ✅
- Docs /bring-context: "Your conversations are processed through the same pipeline as live interactions. Preferences, decisions, project context, and relationships are extracted"
- Docs /how-membase-works: Multiple preprocessing stages — episode creation, entity extraction, graph construction
- App integration digesting: "process, structure, and integrate external data into your memory graph"
- Slack: "generates readable summaries from thread and channel content"

### dedup ✅
- Docs /features/memory: "Deduplication: Similar memories from different sources are merged to avoid redundancy"
- Docs /how-membase-works: "Deduplication and merging" step explicitly documented in pipeline

### qualityRefinement ❌
- No explicit quality scoring, fact verification, or refinement pass beyond dedup/merge
- LLM summarization available for wiki documents on import (`summarize: true`) but this is summarization, not quality refinement

### narrative ❌
- No narrative generation or story construction
- No "weekly recap" auto-generation (Recipes exist as pre-built prompts but are user-initiated, not automatic)

### clustering ❌
- No clustering or topic grouping documented
- Entities and collections provide manual organization, not algorithmic clustering

### recurrence ❌
- No recurrence/pattern detection documented
- Calendar integration syncs recurring meetings but treats each occurrence individually

### personaExtract ✅
- Docs /how-membase-works: entity extraction extracts "preferences, decisions, habits" from conversations
- `membase://profile` resource: "User settings payload (display_name, role, interests, instructions, timezone)"
- Quickstart example: saving "I prefer TypeScript over JavaScript" as a memory
- Preferences and habits extracted as entities in knowledge graph

---

## Platform Support

| Platform | Evidence |
|---|---|
| Claude Code ✅ | Docs /connectors/agents/claude-code: dedicated plugin + slash commands + hooks + auto-recall; MCP fallback |
| Codex ✅ | Docs /connectors/agents/codex: CLI setup with `npx -y membase@latest --client codex`; changelog v0.5.0 |
| OpenCode ✅ | Docs /connectors/agents/opencode: CLI setup with `npx -y membase@latest --client opencode` + `opencode mcp auth membase` |
| Gemini CLI ✅ | Docs /connectors/agents/gemini-cli: CLI setup with `npx -y membase@latest --client gemini-cli` |
| Copilot ❌ | Not listed as supported client on landing page or docs |
| Cursor ✅ | Docs /connectors/agents/cursor: one-click MCP setup; Membase Cursor plugin with packaged rules and skills |
| Windsurf ❌ | Not listed as supported client on landing page or docs |
| OpenClaw ✅ | Docs /connectors/openclaw: plugin `openclaw plugins install @membase/openclaw-membase`; changelog v0.2.3 |
| Hermes ✅ | Docs /connectors/hermes: native provider; changelog v0.4.0 "Hermes Agent Plugin" |
| pi/omp ❌ | Not listed |
| Antigravity ❌ | Not listed |

**Additional platforms:** ChatGPT (custom MCP app), Claude Desktop (custom connector), VS Code (one-click install), Poke (MCP URL), generic MCP URL for any compatible client

---

## Benchmarks

**No published benchmarks found.** No LoCoMo, LongMemEval, PersonaMem, or token reduction scores on landing page, docs, or changelog.
