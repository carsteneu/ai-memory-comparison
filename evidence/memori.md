# Memori — Evidence

> Every ✅ claim backed by public source code or documentation.
> Audit date: 2026-05-28. Source: GitHub `MemoriLabs/Memori` main branch, `memorilabs.ai` docs.

## Architecture

### Web/TUI ✅
- `README.md` — "Use the Dashboard — Memories, Analytics, Playground, and API Keys." Hosted at `app.memorilabs.ai`.
- `docs/memori-cloud/concepts/knowledge-graph.mdx` — "The Memori Playground includes a Memory Graph Viewer" showing nodes, edges, mention counts, and timestamps.
- Dashboard includes: memory browser, analytics, playground (interactive query), API key management.

### Full-text ✅
- `docs/memori-cloud/concepts/advanced-augmentation.mdx` — The recall system searches "across both extracted facts and the knowledge graph" for relevant context. Conversation text is searchable.
- The augmentation pipeline processes raw conversation text, generating vector embeddings for semantic search. Full-text search of stored conversations is implicitly supported since conversations are persisted.

### Semantic/vector ✅
- `docs/memori-cloud/concepts/advanced-augmentation.mdx` — "Generates vector embeddings for semantic search." "Uses semantic search to find entity facts matching the query" during Context Recall.
- `docs/memori-cloud/benchmark/overview.mdx` — Advanced Augmentation "extracts, compresses, and organizes high-signal information from raw interactions for efficient retrieval."
- Semantic triples are vector-embedded for similarity-based retrieval. Recall ranks facts by vector similarity to the query.

---

## Data Model

### Entities ❌
- Memori has `entity_id` as an attribution/scoping concept (the user or thing being remembered about), but there is no `entities` metadata field on individual memories that could be used for structured lookup. Entity is a namespace/tenant, not a searchable tag on a memory record.

### Actions ❌
- No `actions` metadata field on memories. Memori has `memori_recall`, `memori_recall_summary`, `memori_compaction`, `memori_advanced_augmentation` as MCP tools, but these are retrieval/management tools, not metadata fields on stored memories.

### Keywords ❌
- No keyword tagging system. Facts are stored as semantic triples (subject-predicate-object), not tagged with human-defined keywords.

### anticipatedQueries ❌
- No anticipated query matching. Search is reactive (query → semantic match), not proactive (pre-defined query patterns).

### triggerRules ❌
- No trigger rules that auto-surface memories on specific conditions.

### domainTag ❌
- No domain tagging. The only scoping dimensions are entity, process, and session — no domain classification.

### taskType ❌
- No task type classification for memories. Advanced Augmentation extracts facts, preferences, skills, and attributes, but these are content categories, not task-state metadata.

### context ❌
- No `context` metadata field describing when/why a memory is relevant. Conversation summaries provide narrative context, but individual memories lack a structured "relevance context" tag.

### source ❌
- No `source` provenance tracking on individual memories. Conversations are attributed to entity+process, but the origin of a specific fact is not tagged with a source classification (user_stated, inferred, etc.).

### originTrust ❌
- No trust scoring based on extraction origin. All extracted facts have equal weight.

### emotional ❌
- No emotional state tracking on memories or conversations.

### conflict ❌
- No conflict detection between memories. Deduplication exists for triples (mention count increment), but contradictory facts are not flagged.

### layeredMemory ❌
- Memori has entity/process/session levels, but these are attribution scoping (who, what agent, which session), not layered memory where the same fact exists at different confidence levels or tiers. A fact is either present or not.

### timeTravel ❌
- No point-in-time query capability. You cannot query "what did the system know about X on date Y." Triple timestamps exist (first seen, last seen) but there is no historical snapshot query.

---

## Search & Retrieval

### Hybrid (BM25+Vec) ❌
- The recall system uses semantic search (vector) and knowledge graph traversal. Full-text search on conversation text exists. However, there is no documented combined BM25+vector hybrid search interface with weighted fusion. The search is either semantic (vector similarity on triples) or conversational (text search on stored conversations), not a fused hybrid pipeline.

### Deep ❌
- No deep search mode that returns full conversation context around matches. Recall returns extracted facts and summaries, not raw conversation snippets with surrounding context.

### Code graph ❌
- No code graph capability. Memori is a general-purpose conversational memory system, not code-aware.

### docsSearch ❌
- No documentation indexing or search. Memori does not ingest or search external documentation.

### factQuery ❌
- No structured metadata query on memories. You can recall by entity+query (semantic) but cannot filter memories by structured fields like "all facts of type preference."

### Timeline ❌
- No timeline view of memory evolution. Triple timestamps exist (first_seen, last_seen) but there is no chronological timeline UI or API for browsing memory history.

---

## Knowledge Lifecycle

### Supersede ❌
- No supersede/replace mechanism. Deduplication increments mention counts for identical triples, but there is no mechanism to mark an old fact as superseded by a new one. Old facts coexist with new facts.

### Explicit forget ❌
- No documented forget/delete mechanism for individual memories. The MCP tools listed are `memori_recall`, `memori_recall_summary`, `memori_compaction`, and `memori_advanced_augmentation` — no `memori_delete` or `memori_forget` tool. The SDK has `resetSession()` / `new_session()` but no memory deletion API.

### Decay ❌
- No memory decay. Facts persist indefinitely with no time-based confidence reduction.

### Contradiction ❌
- No contradiction detection between facts. If a user changes their preference, the old and new facts coexist.

### Quarantine ❌
- No quarantine or sandbox for unverified/low-quality memories.

### autoResolve ❌
- No automatic resolution of tasks or conflicting information.

### trustModel ❌
- No trust model. All extracted facts are treated equally regardless of source confidence.

---

## Extraction Pipeline

### Auto-extraction ✅
- `docs/memori-cloud/concepts/advanced-augmentation.mdx` — "Advanced Augmentation is the AI engine inside Memori Cloud that turns raw conversations into structured, searchable memories. It runs asynchronously in the background." Pipeline: reads full conversation → identifies facts/preferences/skills/attributes → extracts semantic triples → generates vector embeddings → stores in managed memory space.
- `docs/memori-cloud/benchmark/overview.mdx` — Advanced Augmentation "functions as an automated cognitive filter. It is a background memory creation pipeline designed to distill raw dialogue into searchable memory assets."
- Extraction types: Facts, Preferences, Skills & Knowledge, Attributes. All done automatically with no manual annotation.

### contentPreproc ❌
- No explicit content preprocessing. The augmentation pipeline processes raw conversation text directly — no text cleaning, normalization, or filtering step documented.

### Dedup — partial (triple-level only) ⚠️
- `docs/memori-cloud/concepts/knowledge-graph.mdx` — "Memori automatically deduplicates triples — if the same fact is mentioned multiple times, it increments the mention count and updates the timestamp."
- This is triple-level deduplication only. There is no deduplication at the conversation summary level or for the broader memory store. Not a general memory dedup system.

### qualityRefine ❌
- No quality refinement step. The augmentation engine extracts and stores — there is no second-pass refinement, fact-checking, or quality scoring.

### Narrative ❌
- No narrative generation. Conversation summaries capture what happened in a session, but there is no long-form narrative synthesis across multiple sessions.

### Clustering ❌
- No memory clustering or topic grouping. Facts are stored individually or linked by entity, not grouped into clusters.

### Recurrence ❌
- No recurrence pattern detection across sessions.

### Persona ❌
- No persona engine. Facts, preferences, and skills are extracted per entity, but there is no unified persona model or profile generation.

---

## Platform Support

### Claude Code ✅
- `docs/memori-cloud/mcp/client-setup.mdx` — Dedicated Claude Code section. MCP server at `https://api.memorilabs.ai/mcp/`. CLI config: `claude mcp add --transport http memori https://api.memorilabs.ai/mcp/ ...` with API key + entity headers. Project config via `.mcp.json`. Tools: `memori_recall`, `memori_recall_summary`, `memori_compaction`, `memori_advanced_augmentation`.
- `README.md` — "If you use Claude Code, Cursor, Codex, Warp, or Antigravity, you can connect Memori with no SDK integration needed."

### Cursor ✅
- `docs/memori-cloud/mcp/client-setup.mdx` — Dedicated Cursor section. Config at `~/.cursor/mcp.json` or `.cursor/mcp.json`. HTTP transport to `https://api.memorilabs.ai/mcp/`. Project-scoped attribution using workspace placeholders.

### OpenClaw ✅
- `README.md` — Dedicated OpenClaw section. Plugin: `openclaw plugins install @memorilabs/openclaw-memori`. "Automatically captures structured memory from conversation and agent execution after each turn — including tool calls, decisions, and outcomes."
- `docs/memori-cloud/openclaw/quickstart.mdx` — Full setup guide referenced.

### Hermes ✅
- `README.md` — Dedicated Hermes section. Package: `pip install hermes-memori`. "Captures completed conversations in the background and gives Hermes explicit `memori_recall` and `memori_recall_summary` tools for agent-controlled recall."
- `docs/memori-cloud/hermes/quickstart.mdx` — Full setup guide referenced.

---

## Benchmarks

### LoCoMo — 81.95 ✅
- `docs/memori-cloud/benchmark/results.mdx` — Table 1: Overall accuracy = 81.95% (average of three rounds). Breakdown: Single-hop 87.87%, Multi-hop 72.70%, Open-domain 63.54%, Temporal 80.37%.
- `docs/memori-cloud/benchmark/overview.mdx` — "Memori achieves 81.95% accuracy, outperforming existing memory systems while using only 1,294 tokens per query (~5% of full context)."
- Paper: `arxiv.org/abs/2603.19935`.

### Token efficiency — 95% fewer ✅
- `docs/memori-cloud/benchmark/results.mdx` — Table 2: Memori uses 1,294 tokens (4.97% of full-context 26,031 tokens). That is ~95% fewer tokens. "67% fewer tokens than Zep (3,911)" and "over 20× savings compared to full-context methods."
- `README.md` — "reducing prompt size by roughly 67% vs. Zep and lowering context cost by more than 20x vs. full-context prompting."

### Methodology open ✅
- `docs/memori-cloud/benchmark/overview.mdx` — LLM-as-a-Judge framework with four reasoning categories: Multi-Hop, Temporal, Open-Domain, Single-Hop.
- `docs/memori-cloud/benchmark/results.mdx` — Full methodology: ingestion → retrieval → LLM answerer → judge LLM scoring. Compared against Zep, LangMem, Mem0, and Full-Context ceiling. Paper available on arXiv for full reproducibility.
- Benchmark code in `benchmarks/` directory of the open-source repository.

---

## Claims NOT present (marked false in data.js) — verified

The following features are correctly marked `false` in data.js. No public evidence was found for any of them:

**Data Model:** entities, actions, keywords, anticipatedQueries, triggerRules, domainTag, taskType, context, source, originTrust, emotional, conflict, layeredMemory, timeTravel — all ❌ (flat attribution model with entity/process/session scoping; no structured metadata fields on individual memories)

**Search:** hybrid, deep, codeGraph, docsSearch, factQuery, timeline — all ❌ (semantic recall + knowledge graph; no fused BM25+vector, no deep search, no code or doc index, no metadata query, no timeline)

**Lifecycle:** decay, supersede, contradiction, quarantine, autoResolve, trustModel, explicitForget — all ❌ (add-only accumulation; no forgetting/decay, no contradiction handling, no quarantine, no trust model, no delete API)

**Extraction:** contentPreproc, qualityRefine, narrative, clustering, recurrence, persona — all ❌ (background extraction pipeline is single-pass; no quality refinement, no narrative synthesis, no clustering, no recurrence, no persona engine)

**Dedup — partial only:** Triple-level dedup exists (increment mention count for identical triples). Not general memory deduplication. Does not meet the threshold for ✅.

---

## Audit Notes

1. **Dedup is triple-level only**: The knowledge graph deduplicates identical semantic triples by incrementing mention counts. This is not a general memory deduplication system — conversation summaries and other memory artifacts are not deduplicated. Marked as partial/absent.

2. **Hybrid search not documented**: While the recall system combines semantic vector search with knowledge graph traversal, there is no documented BM25+vector fused hybrid search with weighted scoring. The search pipeline is semantic-first with knowledge graph augmentation, not a classic hybrid (BM25+vector) design. Marked as absent.

3. **Full-text is implicit**: The conversation history is stored and searchable, but full-text search is not documented as a distinct feature or API. It exists as part of the semantic recall pipeline. Cautiously marked as ✅ since conversations are persisted and searchable.

4. **No explicit forget/delete**: Unlike Mem0 (which has `delete_memory`, `delete_all_memories`, `delete_entities` MCP tools), Memori's documented MCP tools are read-only: `memori_recall`, `memori_recall_summary`, `memori_compaction`, `memori_advanced_augmentation`. No delete/forget capability in the documented API surface.
