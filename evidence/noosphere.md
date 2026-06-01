# Noosphere — Evidence

> `evidence: "evidence/noosphere.md"`
> Created: 2026-06-01 (v1.7.0)
> Source README audit based on `SweetSophia/noosphere` @ master (336 commits)

## Repo Identity

- **URL:** https://github.com/SweetSophia/noosphere
- **Homepage:** https://noosphere-memory.com
- **License:** MIT
- **Language:** TypeScript (Next.js 16)
- **Stars:** 53, Forks: 0, Commits: 336
- **Version:** v1.7.0
- **Created:** 2026-04-11
- **Topics:** agentic-memory, agentic-rag, agentic-workflow, ai, ai-agent, ai-skill, document-management, memory-system, wiki

---

## Vital Signs

| Claim | Status | Evidence |
|-------|--------|----------|
| stars = 53 | ✅ | GitHub API: `stargazers_count: 53` |
| language = TypeScript | ✅ | GitHub API: `language: "TypeScript"` |
| license = MIT | ✅ | GitHub API: `license: { key: "mit" }` |
| singleBinary = false | ✅ | Requires Docker + Node.js 22 |
| created = 2026-04-11 | ✅ | GitHub API: `created_at: "2026-04-11T06:53:39Z"` |

---

## Architecture

### Deployment ✅
- README: Docker Compose — `docker compose up -d` on port 6578
- README: Production Docker image: `ghcr.io/sweetsophia/noosphere:latest`
- README: `docker-compose.noosphere.yml` production template with `init` service (waits for PG, runs migrations, bootstraps admin)

### Storage ✅
- README: PostgreSQL 16 (primary), Redis 7 (optional recall cache)
- README: Prisma 7 ORM, filesystem image uploads, Markdown vault export

### Integration ✅
- README: **4 platform plugins**: OpenClaw, Hermes Agent, Opencode, Kilo Code
- README: Universal REST API for all other systems
- README: Obsidian vault sync (export/import + reverse scan)

### Proxy ❌
- Not a proxy — standalone Docker server

### Web UI ✅
- README: Next.js 16 wiki dashboard with topic hierarchy, article editing, search, revision history, admin panel
- README: Routes: `/wiki` (topics), `/wiki/{topic}/{article}` (view), edit, history, search, admin (keys, scopes, log, trash)
- README: Markdown editor with preview, GFM rendering, code highlighting

### Offline ✅
- README: Self-hosted Docker — all data local, no cloud dependency

### Multi-agent ❌
- No explicit multi-agent coordination, though OpenClaw plugin has "Multiagent support"

### LLM providers = 0 ✅
- README: Noosphere does not embed or require any LLM. It is a knowledge storage/retrieval system. Agents bring their own LLM.

### Cache optimization ✅
- README: Redis recall cache — "short-circuits repeat Noosphere article searches before the PostgreSQL full-text path"
- README: "Redis cache-aside layer for repeated Noosphere article recall and search queries"

### Procedural memory ❌
- Not mentioned

### Sandboxed exec ❌
- Not mentioned

### Scheduled/autonomous ✅
- README: "Local memory scheduler: run memory maintenance jobs with the built-in scheduler" via `npm run memory:scheduler`
- README: Promotion scanning + backfill/synthesis job lifecycle with retry

### Privacy ✅
- README: API key authentication with SHA-256 hashed keys (raw keys never stored)
- README: Scoped API keys (`READ`/`WRITE`/`ADMIN` permissions + `allowedScopes`)
- README: Restricted articles — tagged with scopes, invisible to users/keys without matching scope
- README: Docker internal network — PostgreSQL not exposed to host by default
- README: Secrets stored in `~/.noosphere/.env`, outside repo

### Export ✅
- README: `POST /api/export` — download all articles as Markdown vault zip
- README: `POST /api/import` — import from Markdown vault zip
- README: `POST /api/sync/import-scan` — read-only scan of Obsidian vault for reverse-import candidates
- README: Versioned frontmatter codec with `noosphere.schemaVersion`, `noosphere.contentHash`

### Setup ✅
- README: `docker compose up -d` (production) or `git clone + npm run dev` (development)
- README: Admin creation via `docker compose exec app node scripts/create-admin.js`

---

## Data Model

### Storage unit ✅
- README: **Article** (wiki page) — structured Markdown with title, slug, content, topic, tags, excerpt, confidence, status
- README: **Topic** hierarchy — unlimited depth with parent/slug
- README: **Tag** cross-cutting labels (many-to-many)
- README: **ApiKey** with hashed secrets, permissions, scopes

### Entities ❌
- No entity extraction pipeline — articles are structured knowledge, not extracted entities

### Context (why) ✅
- README: Articles have source metadata, topic context, tags, author attribution
- README: "Capture guidance + ingest API + backfill" auto-capture pipeline

### Keywords ✅
- README: PostgreSQL full-text search with query parameter, filters by topic/tag/status/confidence
- README: Tags as cross-cutting labels with auto-creation

### Data sources = 2 ✅
- README: (1) Noosphere article provider, (2) Hindsight HTTP recall provider (extensible)

### Schema fields = 15 ✅
- AGENTS.md + README: Article (id, title, slug, content, topicId, tags, excerpt, confidence, status, lastReviewed, restrictedTags, deletedAt, authorName, revisedAt, source metadata) ≈ 15

### Layered memory ✅
- README: Three curation levels: **ephemeral → managed → curated**
- README: Promotion pipeline: "identify repeatedly useful ephemeral memories and promote them toward managed/curated knowledge"

### Time-travel ✅
- README: "Revision history for changed articles" — per-article history tracking
- AGENTS.md: Articles have `createdAt` and `updatedAt` timestamps

### Conflict surfacing ✅
- README: "Conflict detection and configurable resolution strategies" — one of few systems with this
- README: Strategies can suppress, prefer recent, prefer curated, or surface conflicts

### Confidence scoring ✅ (bonus)
- README: Three levels: `low | medium | high`
- README: Used in composite ranking and recall scoring

### Status lifecycle ✅ (bonus)
- README: Three states: `draft | reviewed | published`
- README: Agents always save as draft; humans promote through review

### Soft delete ✅
- README: `deletedAt` field on articles, trash UI in admin panel
- README: Restore from trash

### Domain tag ❌
- Not as formal domain classification, though `restrictedTags` (scopes like `financial`, `health`) serve a similar purpose

---

## Search & Retrieval

### Full-text ✅
- README: "PostgreSQL full-text search" — live FTS with filters
- README: Redis recall cache accelerates repeat searches

### Semantic/vector ❌
- README: "vector (planned)" — not yet implemented

### Hybrid (BM25+Vec) ❌
- Not yet — vector component still planned

### Deep (incl. thinking) ❌
- Not mentioned

### Code graph ❌
- Not mentioned

### Docs search ❌
- Not mentioned

### Fact metadata query ❌
- Not mentioned (search is article-centric, not fact-level)

### Timeline view ❌
- Activity log exists (`GET /api/log`) but no timeline visualization

### Search modes = 2 ✅
- README: (1) PostgreSQL full-text search, (2) Redis recall cache lookup — confirmed

---

## Knowledge Lifecycle

### Decay/forgetting ❌
- Not mentioned — no time-based decay or forgetting mechanism

### Supersede/replace ✅
- README: `PATCH /api/articles/:id` — update articles with revision tracking
- README: Soft delete + trash (can restore)

### Contradiction detection ✅
- README: "Conflict detection and configurable resolution strategies" in recall orchestration
- README: Cross-provider conflict resolution (not just surface, but resolve)

### Quarantine ❌
- Not mentioned

### Auto-resolution ✅
- README: Conflict resolution with configurable strategies (prefer recent/curated/highest-scoring)
- README: Auto-resolution is optional and configurable

### Trust model ✅
- README: Confidence scoring (low/medium/high)
- README: Curation levels (ephemeral/managed/curated)
- README: Status lifecycle (draft/reviewed/published)

### Explicit forget ✅
- README: Soft delete via `deletedAt` — articles moved to trash
- README: Trash UI for permanent deletion or restore

---

## Extraction Pipeline

### Auto-extraction ✅
- README: "Bundled capture guidance + ingest API + backfill" — agents auto-informed when/how to save
- README: OpenClaw plugin injects `<noosphere_memory_capture>` guidance block on every prompt
- README: Opencode/Kilo plugins have idle auto-save via `session.idle` hook
- README: Backfill/synthesis jobs create articles from historical material

### Content-aware preprocessing ❌
- No mention of PII scrubbing, injection defence, or content sanitization beyond Markdown rendering

### Deduplication ✅
- README: "Cross-provider deduplication" — collapses exact, canonical, or semantic overlap while preserving provenance
- README: Part of the recall orchestration pipeline

### Quality refinement ✅
- README: Two-pass system: agents save drafts → human (or scheduled review) promotes to reviewed/published
- README: Confidence scoring, curation levels, status lifecycle all act as refinement pipeline

### Narrative generation ✅
- README: Backfill/synthesis: "Synthesize older memory material into wiki articles with retryable jobs"
- README: Ingest pipeline can synthesize multiple articles from a single external source

### Clustering ✅
- README: Topic hierarchy (unlimited depth) groups articles
- README: Tags for cross-cutting subjects
- README: Promotion identifies related memories for grouping

### Recurrence detection ❌
- Not mentioned

### Persona extraction ❌
- Not mentioned

---

## Platform Support

### OpenClaw ✅
- README: Full plugin at `openclaw-noosphere-memory/` — 6 tools (status, recall, get, save, topics, topic_create, article_create)
- README: Auto-recall via `before_prompt_build` hook + dual-block injection (capture guidance + recall results)
- README: Multi-agent support, CLI helpers (`openclaw noosphere doctor/status/upgrade`)
- README: Memory corpus supplement for OpenClaw shared memory

### Hermes Agent ✅
- README: First-class Hermes `MemoryProvider` at `hermes-noosphere-memory/`
- README: Auto-recall via `prefetch()`, explicit memory mirroring, bundled setup skill
- README: 6 tools: status, recall, get, topics, save (matching OpenClaw capabilities)

### Opencode ✅
- README: npm plugin `@sweetsophia/opencode-noosphere-memory`
- README: Auto-recall via `chat.message` hook, idle auto-save via `session.idle`
- README: Compatible with `oh-my-opencode-slim`

### Kilo Code ✅
- README: npm plugin `@sweetsophia/kilocode-noosphere-memory`
- README: Auto-recall via `chat.message` hook, idle auto-save via `session.idle`
- README: Mirror of Opencode plugin capabilities

### Claude Code ❌
- Not mentioned — universal REST API available but no dedicated plugin

### Codex ❌
- Not mentioned

### Gemini CLI ❌
- Not mentioned

### Copilot ❌
- Not mentioned

### Cursor ❌
- Not mentioned

### Windsurf ❌
- Not mentioned

### pi/omp ❌
- Not mentioned

### Antigravity ❌
- Not mentioned

---

## Benchmarks

- No published benchmarks — neither LoCoMo, LongMemEval, PersonaMem, nor custom benchmarks in README

---

## Notable Features Not in Comparison Schema

| Feature | Detail |
|---------|--------|
| **Multi-Provider Recall Orchestration** | Concurrent fan-out to Noosphere + Hindsight + future providers with ranking, dedup, conflict, and token budgeting |
| **Composite Ranking** | Relevance + confidence + recency + curation combined into single score |
| **Token Budget Manager** | Prompt-safe recall blocks with configurable result and token caps |
| **Promotion Pipeline** | Identifies repeatedly recalled ephemeral memories for promotion to curated |
| **Backfill/Synthesis Jobs** | Generates curated articles from historical material with retry support |
| **Local Scheduler** | Built-in `npm run memory:scheduler` for maintenance jobs |
| **Redis Recall Cache** | Cache-aside layer accelerates repeat searches |
| **Obsidian Sync** | Full export/import + reverse scan of Markdown vaults |
| **Revision History** | Per-article version tracking |
| **Topic Hierarchy** | Unlimited-depth tree organization |
| **Restricted Article Scopes** | Tag-based access control for sensitive content |
| **Image Support** | Upload and embed images in wiki articles |
| **Bundled Capture Guidance** | Auto-injected instructions telling agents when/how to save |
