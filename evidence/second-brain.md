# Second Brain — Audit Evidence

**Repository:** https://github.com/rahilp/second-brain-cloudflare
**Audit date:** 2026-05-29
**Auditor:** DeepSeek V4 Pro (OpenCode)
**Stars at audit:** 91
**Latest release:** v1.5.1 (2026-05-28)

---

## Summary

Second Brain is a lightweight, personal-knowledge memory layer built on Cloudflare's serverless stack (Workers + D1 + Vectorize + Workers AI). It focuses on simplicity: one-click deploy, 6 MCP tools, semantic search with time-decay reranking, and a web dashboard. Users self-host in their own Cloudflare account. The philosophy is "one shared memory, available in every AI tool you use."

---

## Architecture

### Deployment
- Cloudflare Workers (serverless edge functions)
- Single-click deploy via Cloudflare Deploy button
- Runs in user's own Cloudflare account — no external service
- Free tier at personal scale

**Evidence (README):**
> "All free tier at personal scale. Your data stays in your own Cloudflare account."

### Storage
- **D1** (Cloudflare's serverless SQLite): stores entry text, tags (JSON array), source, timestamps, recall_count, importance_score, vector_ids
- **Vectorize** (Cloudflare's vector DB): 384-dimensional embeddings using `bge-small-en-v1.5` via Workers AI, cosine similarity metric
- No external databases required — fully within Cloudflare ecosystem

**Evidence (schema.sql):**
```sql
CREATE TABLE IF NOT EXISTS entries (
  id          TEXT PRIMARY KEY,
  content     TEXT NOT NULL,
  tags        TEXT NOT NULL DEFAULT '[]',
  source      TEXT NOT NULL DEFAULT 'api',
  created_at  INTEGER NOT NULL
);
```

Additional columns added via migrations: `recall_count`, `importance_score`, `vector_ids`.

### Stack
- TypeScript 68.2%, HTML 30.5%, JavaScript 1.3%
- Dependencies: `@modelcontextprotocol/sdk`, `agents`, `zod`
- Dev: `wrangler`, `vitest`, `typescript`

### Integration
- **MCP (Model Context Protocol)**: Streamable HTTP transport at `/mcp` endpoint
- **REST API**: `/capture`, `/append`, `/list`, `/update`, `/chat`, `/count`, `/tags`
- **Web UI**: Built-in dashboard at `GET /`
- No hooks/proxy — agent integration is via MCP tools + AI instructions files

### Web UI
- **YES.** Built-in single-page dashboard at Worker URL
- Three views: Recall (semantic search + LLM synthesis), Recent (chronological), Remember (manual input)
- Mobile-responsive, auth via localStorage token
- LLM-synthesized answers using Llama 3.3 70B via Workers AI
- Append/Forget inline controls, tag filtering, export panel

**Evidence (Web UI wiki):**
> "Every deployment includes a built-in dashboard — no extra setup, no separate service."

### Multi-agent
- **NO.** Single-user personal memory system. No multi-agent coordination.

### LLM Providers
- **2**: Workers AI (bge-small-en-v1.5 for embeddings, Llama 3.3 70B for recall synthesis)
- Both run on user's own Cloudflare account, no external API keys required

### Privacy/Encryption
- **PARTIAL.** Data stays in user's own Cloudflare account. No external logging. Auth token required for REST endpoints (not for MCP — Worker URL acts as access control). No end-to-end encryption.

### Export
- **YES.** Export full memory store as JSON or Markdown from Web UI Settings panel (added in v1.5)
- No import functionality documented

### Pricing
- **Free.** All on Cloudflare free tier at personal scale.

### Setup
- One-click deploy via Cloudflare Deploy button
- Set AUTH_TOKEN during deploy
- Connect AI clients using provided config snippets

---

## Data Model

### Storage Unit
- **Entry** (flat text note with metadata). No structured entity extraction.

### Schema Fields
Counting all columns in the entries table (schema.sql + release migrations):
1. `id` (TEXT PRIMARY KEY)
2. `content` (TEXT)
3. `tags` (TEXT, JSON array)
4. `source` (TEXT)
5. `created_at` (INTEGER, unix ms)
6. `recall_count` (added v1.3.0)
7. `importance_score` (added v1.3.0)
8. `vector_ids` (added v1.1.2)

**Total: 8 schema fields**

### Data Model Features
| Feature | Present | Evidence |
|---------|---------|----------|
| Entities | NO | Flat text model, no entity extraction |
| Actions | NO | No action metadata |
| Keywords/tags | YES | `tags` field as JSON array, hashtag parsing in content |
| Anticipated queries | NO | Not designed for proactive query matching |
| Trigger rules | NO | No conditional surfacing |
| Domain tag | NO | No domain classification |
| Task type | NO | No task differentiation |
| Context (why) | YES | CHATGPT_INSTRUCTIONS defines tags: personal, work, task, idea, context, claude-response + topic tag |
| Source attribution | YES | `source` field (api, phone, browser, voice, claude, chatgpt) |
| Origin + trust | NO | No trust scoring model |
| Emotional | NO | No emotional analysis |
| Conflict surfacing | YES | Contradiction detection (v1.4.0), smart merge (v1.5) |
| Layered memory | NO | Flat model, no L0-L3 tiers |
| Time-travel | NO | No historical state reconstruction |

---

## Search & Retrieval

### Search Capabilities
| Feature | Present | Evidence |
|---------|---------|----------|
| Full-text | NO | No FTS/BM25. Semantic-only retrieval. |
| Semantic/vector | YES | bge-small-en-v1.5 (384-dim), cosine similarity via Vectorize |
| Hybrid (BM25+Vec) | NO | Vector only. No keyword/semantic fusion. |
| Deep (incl. thinking) | NO | No deep search with contextual expansion |
| Code graph | NO | No codebase indexing |
| Docs search | NO | No documentation indexing |
| Fact metadata query | NO | No structured metadata query language |
| Timeline view | YES | `list_recent` tool, Recent view in Web UI, temporal navigation (v1.2.0) |

### Search Modes
1. **Semantic recall** (`recall` tool — vector similarity + time-decay reranking)
2. **Chronological list** (`list_recent` tool — reverse chronological)
3. **Tag-filtered** (tag parameter on both recall and list_recent)
4. **Temporal** (time-based recall queries, v1.2.0)

**Total: 4 search modes**

### Search Scoring
The recall scoring formula (v1.3.0):
```
score = similarity × time_decay × (1 + log1p(recall_count))
```
- `similarity`: cosine similarity from Vectorize
- `time_decay`: e^(-age / half_life), half-life is tag-configurable (default 7 days)
- `recall_count`: tracks usage frequency, fire-and-forget increment

### Web UI Search
- Recall tab: semantic search with LLM-synthesized answer (Llama 3.3 70B)
- Sources toggle shows individual memories used
- Tag filtering in both Recall and Recent views

### Data Sources
- **1** primary: User-created entries via /capture, remember MCP tool, Web UI, Obsidian, iOS Shortcuts, browser bookmarklet

### Duplicate Detection
Three-tier system verified in v1.5 release notes:
- **≥ 95% similarity**: Blocked — near-exact duplicate, nothing stored
- **85-95% similarity**: Smart merge prompt → keep_both / replace / merge / contradiction
- **45-85% similarity**: Contradiction check only
- **< 45% similarity**: Stored as-is (with optional importance scoring)
- Uses multi-point sampling (v1.1.2)

---

## Knowledge Lifecycle

| Feature | Present | Evidence |
|---------|---------|----------|
| Decay/forgetting | YES | Time-decay reranking: e^(-age/half-life). Tag-based configurable half-life (v1.1.2). Cap at 1.0 multiplier (v1.5.1). |
| Supersede/replace | YES | `update` MCP tool replaces full content (v1.5). Smart merge's `replace` action. |
| Contradiction detect | YES | LLM-powered contradiction detection (v1.4.0). Auto-resolution. Smart merge `contradiction` action (v1.5). |
| Quarantine | NO | No quarantine mechanism |
| Auto-resolution | YES | Contradiction auto-resolution (v1.4.0), smart merge with auto-decisions (v1.5) |
| Trust model | NO | No provenance/trust scoring |
| Explicit forget | YES | `forget` MCP tool + Web UI Forget button. Deletes from D1 + all Vectorize chunks including update chunks. No undo. |

### Content Lifecycle Tools
1. `remember` — store new entry
2. `append` — add timestamped update to existing entry
3. `update` — replace full content in place (v1.5)
4. `forget` — delete entry + all vectors
5. Smart merge — LLM decides between keep_both/replace/merge/contradiction for near-duplicates (v1.5)

### Time-Decay Reranking
Verified in How It Works wiki:
- `recall` retrieves 3x semantic matches (e.g., top 15 for topK=5)
- Each match multiplied by e^(-age / half-life)
- Re-sorted by adjusted score
- Dedup by parent ID, final topK selection

---

## Extraction Pipeline

| Feature | Present | Evidence |
|---------|---------|----------|
| Auto-extraction | INSTRUCTION-BASED | CHATGPT_INSTRUCTIONS.md: "Store everything important automatically... Never ask permission." No code-level extraction — relies on AI client instructions. |
| Content-aware preproc | NO | No preprocessing pipeline |
| Deduplication | YES | Three-tier duplicate detection at capture time (see above) |
| Quality refinement | YES | AI importance scoring (1-5, v1.3.0), recall_count tracking, LLM-synthesized insights in Web UI |
| Narrative generation | YES | LLM-synthesized recall answers in Web UI (Llama 3.3 70B via Workers AI) |
| Clustering | NO | No topic/entity clustering |
| Recurrence detection | NO | No pattern recurrence detection beyond recall_count |
| Persona extraction | NO | No user persona/profile building |

### Quality Scoring
- `importance_score`: Scored 1-5 by AI at capture time (non-blocking, `ctx.waitUntil`)
- `recall_count`: Incremented on every recall hit, fire-and-forget
- Scoring formula incorporates both

### Chunking
- Notes ≤ 1,600 chars: single vector
- Notes > 1,600 chars: split at sentence/newline boundaries, 200-char overlap
- Each chunk gets independent Vectorize vector pointing to parent entry ID
- Recall deduplicates by parent ID — best-matching chunk per entry

---

## Platform Support

| Platform | Status | Evidence |
|----------|--------|----------|
| Claude Desktop | YES | Documented config in Connect-to-AI-Clients wiki |
| Claude Code | YES | `claude mcp add` command documented. CLAUDE_INSTRUCTIONS.md |
| claude.ai / iOS | YES | Custom connector setup documented |
| ChatGPT | YES | CHATGPT_INSTRUCTIONS.md exists, generic MCP connection |
| Cursor | CLAIMED | README mentions Cursor. No dedicated instructions file (CURSOR_INSTRUCTIONS.md → 404). Works via generic MCP. |
| Windsurf | NOT MENTIONED | Not in README, wiki, or instructions files |
| Codex | NO | Not documented |
| OpenCode | NO | Not documented |
| Gemini CLI | NO | Not documented |
| Copilot | NO | Not documented |
| OpenClaw | NO | Not documented |
| Hermes | NO | Not documented |
| pi/omp | NO | Not documented |
| Antigravity | NO | Not documented |

**Verified platforms: 5** (Claude Desktop, Claude Code, claude.ai, ChatGPT, Cursor — though Cursor lacks dedicated instructions)

### AI Instruction Files
- `AI_Instructions/CLAUDE_INSTRUCTIONS.md` — rules for Claude-based clients
- `AI_Instructions/CHATGPT_INSTRUCTIONS.md` — rules for ChatGPT (source: "chatgpt", tags include "chatgpt-response")
- No Cursor, Windsurf, or Codex instructions

### Integrations (Non-AI)
- **Obsidian**: Community plugin (`second-brain-obsidian-plugin`)
- **iOS**: Brain Dump, Text Brain Dump, Save to Brain shortcuts
- **Browser**: Bookmarklet in `integrations/bookmarklet.js`

---

## Benchmarks

| Benchmark | Result | Evidence |
|-----------|--------|----------|
| LoCoMo | — | No published scores |
| LongMemEval | — | No published scores |
| PersonaMem | — | No published scores |
| Token reduction | — | No published measurements |
| Methodology open | — | No methodology published |

No benchmarks published. The system has 155 tests (v1.5) but no standardized memory benchmarks.

---

## Vital Signs

| Field | Value | Evidence |
|-------|-------|----------|
| Stars | 91 | GitHub (2026-05-29) |
| Language | TypeScript | 68.2% TS, 30.5% HTML, 1.3% JS |
| License | MIT | LICENSE file, package.json badge |
| Single binary | NO | Cloudflare Workers deployment, not a binary |
| Created | ~2026-05-17 | First release v1.1.0 on May 17, 2026. Likely created earlier in May. |
| Coverage | 155 tests (v1.5) | Release notes |
| docs URL | https://github.com/rahilp/second-brain-cloudflare/wiki | Repository wiki |
| Website | https://www.thesecondbrain.dev | Repository metadata |

---

## MCP Tools (6 total)

| Tool | Parameters | Description |
|------|-----------|-------------|
| `remember` | content, tags?, source? | Store a note with duplicate detection |
| `append` | id, addition | Append update to existing entry |
| `recall` | query, topK? (default 5), tag? | Semantic search with time-decay + chunk dedup |
| `list_recent` | n? (default 10), tag? | Chronological listing |
| `forget` | id | Delete entry and all chunks |
| `update` | id, content | Replace full content (v1.5) |

---

## REST Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/capture` | POST | Store entry (auth required) |
| `/append` | POST | Append to existing entry (auth required) |
| `/update` | POST | Full content replacement (v1.5, auth required) |
| `/list` | GET | Recent entries (auth required) |
| `/count` | GET | Total memory count (v1.5, auth required) |
| `/tags` | GET | List all tags (v1.1.3, auth required) |
| `/chat` | POST | LLM-synthesized recall answer (v1.1.0) |
| `/mcp` | GET+POST | MCP server, Streamable HTTP (no auth) |
| `/` | GET | Web dashboard (no auth, client-side token) |

---

## Feature Inclusions Summary

### ✅ VERIFIED PRESENT
- Semantic search (bge-small-en-v1.5, 384-dim, cosine similarity)
- Time-decay reranking (tag-configurable half-life)
- Duplicate detection (3-tier: block/merge/contradict)
- Contradiction detection (LLM-powered, v1.4.0)
- Smart merge (keep_both/replace/merge/contradiction, v1.5)
- Explicit forget (delete from D1 + Vectorize)
- Supersede via update tool
- Web UI (Recall/Recent/Remember views + LLM synthesis)
- Data export (JSON/Markdown, v1.5)
- MCP integration (6 tools, Streamable HTTP)
- REST API (9 endpoints)
- Tags/keywords (JSON array, hashtag parsing)
- Source attribution (source field)
- Quality refinement (importance scoring 1-5, recall_count tracking)
- Narrative generation (LLM-synthesized recall answers)
- Chunking (1600-char threshold, 200-char overlap)
- Append (timestamped updates)
- Obsidian plugin
- iOS Shortcuts
- Browser bookmarklet
- Tag filtering (exact match, lowercase)

### ❌ VERIFIED ABSENT
- Full-text/BM25 search
- Hybrid (BM25 + vector) search
- Code graph search
- Deep search (context expansion)
- Docs search
- Fact metadata query
- Entities extraction
- Actions tracking
- Anticipated queries
- Trigger rules
- Domain tagging
- Task type classification
- Origin + trust model
- Emotional analysis
- Layered memory (L0-L3 tiers)
- Time-travel (historical state reconstruction)
- Auto-extraction from conversation (code-level; instruction-based only)
- Content-aware preprocessing
- Clustering
- Recurrence detection
- Persona extraction
- Proxy architecture
- Multi-agent support
- Offline support
- Sandboxed exec
- Scheduled exec
- Procedural memory
- Cache optimization
- Published benchmarks
- Dedicated platform plugins (uses generic MCP)
- Import functionality (export only)

---

## Comparison Table Data (for data.js)

```javascript
{
  id: "second-brain",
  name: "Second Brain",
  url: "https://github.com/rahilp/second-brain-cloudflare",
  evidence: "evidence/second-brain.md",
  description: "Serverless personal memory layer — one deploy, all MCP clients",
  stars: 91, language: "TypeScript", license: "MIT", singleBinary: false, created: "2026-05-17", docs: "https://github.com/rahilp/second-brain-cloudflare/wiki",
  deployment: "Cloudflare Workers (serverless)", storage: "D1 (SQLite) + Vectorize", integration: "MCP + REST", proxy: false, webUi: true, offline: false, multiAgent: false, llmFlex: 2, cacheOpt: false, proceduralMemory: false, sandboxedExec: false, scheduledExec: false, privacy: true, export: true, setup: "1-click deploy", pricing: "free",
  unit: "Entry (text note)",
  entities: false, actions: false, keywords: true, anticipatedQueries: false, triggerRules: false, domainTag: false, taskType: false, context: true, source: true, originTrust: false, emotional: false, conflict: true, layeredMemory: false, timeTravel: false, schemaFields: 8,
  fulltext: false, semantic: true, hybrid: false, deep: false, codeGraph: false, docsSearch: false, factQuery: false, timeline: true, searchModes: 4, dataSources: 1,
  decay: true, supersede: true, contradiction: true, quarantine: false, autoResolve: true, trustModel: false, explicitForget: true,
  autoExtract: false, contentPreproc: false, dedup: true, qualityRefine: true, narrative: true, clustering: false, recurrence: false, persona: false,
  p_claude: true, p_codex: false, p_opencode: false, p_gemini: false, p_copilot: false, p_cursor: true, p_windsurf: false, p_openclaw: false, p_hermes: false, p_pi: false, p_antigravity: false,
  b_locomo: "—", b_longmemeval: "—", b_personamem: "—", b_token: "—", b_methodology: false,
}
```

Note on `context`: true — the tag convention includes "context" as a tag type, and the scoring system uses recall_count to track relevance. However, there is no dedicated "why this was stored" field.

Note on `qualityRefine`: true — AI importance scoring (1-5) at capture time + recall_count usage tracking + LLM-synthesized recall answers.

Note on `autoExtract`: false — the auto-storage behavior is instruction-driven (CLAUDE_INSTRUCTIONS.md, CHATGPT_INSTRUCTIONS.md tell the AI to remember things). There is no code-level automatic extraction from conversation streams. The system requires explicit tool calls.

Note on `decay`: true — time-decay reranking with tag-configurable half-life. Note this is retrieval-time decay, not permanent memory expiration. Entries are never permanently deleted by the system.

Note on `p_cursor`: true — README explicitly lists Cursor. No dedicated instructions file, but works via generic MCP client connection.
