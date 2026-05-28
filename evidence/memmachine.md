# MemMachine — Evidence

> **Audit Date:** 2026-05-28 | **Version:** v0.3.9 (latest) | **Stars:** 3,092
> Repository: https://github.com/MemMachine/MemMachine | Docs: https://docs.memmachine.ai
> License: Apache 2.0 | Created: 2025-08-15 | Language: Python (95.6%)

## Summary

MemMachine is an open-source "long-term memory layer for AI agents" built by MemVerge Inc. It uses a client-server architecture with Neo4j (graph) for episodic memory and PostgreSQL + pgvector for semantic/profile memory. Provides Python SDK, TypeScript SDK, REST API, and MCP server. Supports self-hosted Docker and managed cloud (console.memmachine.ai). LLM-agnostic with support for OpenAI, Anthropic, Bedrock, Ollama.

## Architecture

### webUi ✅
- `[docs.memmachine.ai/platform/introduction.md]` — "The Platform provides a central, convenient location where you can organize your data, track usage, and manage secure access." Includes Dashboard Overview for "usage metrics, API call volume, and resource consumption."

### offline ✅
- `[USAGE.md]` — "MemMachine is **not a hosted service**. Users must run their own MemMachine server instance." Docker compose runs fully locally; Ollama integration supports offline LLM/embedding.

### privacy ✅
- `[USAGE.md]` — Self-hosted deployment option keeps all data on user's own infrastructure. Docker compose script creates local Neo4j + PostgreSQL instances.

### export ❌
- No evidence of a dedicated memory export feature. ChatGPT2MemMachine exists for import only.

### multiAgent ✅
- `[README.md]` — "Persistent memory for CrewAI multi-agent systems." Memory API accepts `agent_id` for scoping. Also supports AWS Strands Agent SDK.
- `[USAGE.md]` — Memory context includes `agent_id` parameter: `project.memory(group_id="default", agent_id="travel_agent", user_id="alice", session_id="session_001")`

### llmFlex ✅
- `[README.md]` — "LLM Agnostic: Works with OpenAI, Anthropic, Bedrock, Ollama, and any LLM provider"
- `[docs.memmachine.ai/install_guide/config/ollama.md]` — Dedicated Ollama configuration guide
- `[docs.memmachine.ai/install_guide/config/aws_bedrock.md]` — Dedicated Bedrock configuration guide

## Data Model

### entities ✅
- `[docs.memmachine.ai/open_source/memory_types.md]` — Semantic memory uses a structured entity model: `set_id` (user/role grouping), `category` (e.g. "user_profile"), `tag` (e.g. "Preferences"), `feature` (e.g. "likes_pizza"), `value` (detailed content). The `prof` table stores these as a two-level key-value structure.

### actions ❌
- No evidence of action tracking in the data model. Messages have roles (user/assistant/system) but no action classification.

### keywords ❌
- No explicit keyword extraction or tagging model. Semantic categories/tags serve a similar role but are LLM-extracted, not keyword-based.

### context ✅
- `[USAGE.md]` — Memory context is scoped by `user_id`, `agent_id`, `session_id`, `group_id`. Messages include `producer`, `produced_for`, `role`, `timestamp`, and jsonb `metadata`. Metadata auto-includes context fields.

### source ✅
- `[docs.memmachine.ai/open_source/memory_types.md]` — Citations table: "This table acts as a link between a semantic feature and the episodes (messages) that support it." Links `profile_id` → `episode_id` for provenance tracking.
- `[docs.memmachine.ai/open_source/memory_types.md]` — "Citations provide traceability back to original conversations."

### emotional ❌
- No evidence of emotional state tracking or sentiment modeling.

### conflict ❌
- No evidence of conflict detection or resolution mechanisms.

### layeredMemory ✅
- `[README.md]` — Three explicit layers: "Working Memory: Short-term context for the current session", "Episodic Memory: Graph-based conversational context that persists across sessions", "Profile Memory: Long-term user facts and preferences stored in SQL"
- `[USAGE.md]` — "Episodic Memory: Stores conversational episodes... Supports both short-term (recent context) and long-term (summarized) storage. Semantic Memory: User-specific facts, preferences, and knowledge extracted from conversations."

### timeTravel ❌
- No evidence of time-based versioning or point-in-time query capability.

### schemaFields: 10
- `[docs.memmachine.ai/open_source/memory_types.md]` — The `prof` table (semantic memory) has 10 columns: `id`, `set_id`, `category`, `tag`, `feature`, `value`, `create_at`, `update_at`, `embedding`, `metadata`. The message/episode model adds: `content`, `producer`, `produced_for`, `role`, `timestamp`.

## Search

### fulltext ❌
- No evidence of full-text search. Search is vector-based (pgvector) plus graph traversal.

### semantic ✅
- `[docs.memmachine.ai/open_source/memory_types.md]` — "We use vector embeddings in this table to give us a powerful way to perform semantic searches." Uses pgvector extension in PostgreSQL for vector similarity search.

### hybrid ✅
- `[USAGE.md]` — `memory.search()` returns both `episodic_memory` (graph-based) and `semantic_memory` (vector-based) results in a single call. The retrieval agent further orchestrates across both stores.

### deep ❌
- No evidence of deep/expanded-context search beyond `expand_context` parameter (default 0).

### codeGraph ❌
- Not a code-focused tool. No code graph or AST analysis.

### docsSearch ❌
- No indexed documentation search feature.

### factQuery ❌
- No dedicated fact query endpoint. Facts are queried via general semantic search.

### timeline ❌
- Messages have timestamps but no timeline-based search/view mode.

### searchModes: 2
- `[USAGE.md]` — Standard mode (`agent_mode=false`, default): direct vector + graph search.
- `[docs.memmachine.ai/open_source/retrieval_agent_architecture.md]` — Agentic mode (`agent_mode=true`): intelligent orchestration with `ToolSelectAgent` routing to `MemMachineAgent` (direct), `SplitQueryAgent` (parallel), or `ChainOfQueryAgent` (multi-hop). Supports multi-hop reasoning chains.

## Lifecycle

### decay ❌
- No evidence of memory decay or TTL mechanisms.

### supersede ❌
- No evidence of versioning/superseding. Updates require delete + re-add.

### contradiction ❌
- No contradiction detection between memories.

### quarantine ❌
- No quarantine or sandbox functionality for suspect memories.

### autoResolve ❌
- No automatic conflict resolution.

### trustModel ❌
- No trust scoring or confidence-weighted memory model.

### explicitForget ✅
- `[docs.memmachine.ai/api_reference/mcp.md]` — `delete_memory` MCP tool: "Use this to remove outdated, incorrect, or sensitive information that should no longer be retained."
- `[USAGE.md]` — `memory.delete_episodic(episodic_id)` and `memory.delete_semantic(semantic_id)`. REST endpoints: `POST /api/v2/memories/episodic/delete`, `POST /api/v2/memories/semantic/delete`.

## Extraction

### autoExtract ✅
- `[docs.memmachine.ai/open_source/memory_types.md]` — "An LLM analyzes conversations to extract meaningful knowledge" → "Structured knowledge gets stored into the prof table with vector embeddings." Extraction from raw messages to structured semantic memory is automatic.

### contentPreproc ✅
- `[docs.memmachine.ai/open_source/memory_types.md]` — Embedder processes raw text into vector embeddings. Reranker sorts and filters. "The Episode batch is then ranked using a Reranker and deduplicated for the most frequent hits."

### dedup ✅
- `[docs.memmachine.ai/open_source/memory_types.md]` — Explicit deduplication in long-term memory pipeline: "The Episode batch is then ranked using a Reranker and deduplicated for the most frequent hits."

### qualityRefine ❌
- No evidence of quality scoring beyond reranking. The reranker sorts relevance but doesn't score quality.

### narrative ❌
- No evidence of narrative compression or story generation from memory.

### clustering ❌
- No explicit clustering of memories by topic or similarity.

### recurrence ❌
- No recurrence pattern detection or periodic memory extraction.

### persona ✅
- `[README.md]` — "Profile Memory: Long-term user facts and preferences stored in SQL"
- `[docs.memmachine.ai/open_source/memory_types.md]` — "Semantic, or profile memory specifically focuses on information and data specific to a user and their experience." Stores preferences, traits, background information with structured categories/tags.

## Platform

### p_claude ✅
- `[README.md]` — "native Model Context Protocol (MCP) server for seamless integration with Claude Desktop"
- `[docs.memmachine.ai/install_guide/integrate/claude_code_mcp.md]` — Dedicated Claude Code integration page.

### p_codex ❌
- No dedicated Codex integration. USAGE.md mentions Codex as an example of AI assistants but no integration exists.

### p_opencode ❌
- No OpenCode integration.

### p_gemini ❌
- No Google Gemini-specific integration.

### p_copilot ❌
- No GitHub Copilot integration.

### p_cursor ✅
- `[README.md]` — MCP server "for seamless integration with Claude Desktop, Cursor, and other MCP-compatible clients"

### p_windsurf ❌
- No Windsurf integration.

### p_openclaw ✅
- `[docs.memmachine.ai/install_guide/integrate/openclaw.md]` — Dedicated OpenClaw integration: "Enable persistent, long-term memory for your OpenClaw agents"

### p_hermes ❌
- No Hermes integration.

### p_pi ❌
- No Pi integration.

### p_antigravity ❌
- No Antigravity integration.

## Benchmarks

### b_locomo ✅
- `[evaluation/README.md]` — Full LoCoMo benchmark pipeline: `./run_test.sh locomo exp1 ingest retrieval_agent` and `./run_test.sh locomo exp1 search retrieval_agent`. Also has legacy `episodic_memory/locomo` workflow.

### b_longmemeval ❌
- No LongMemEval benchmark in evaluation suite.

### b_personamem ❌
- No PersonaMem benchmark.

### b_token ✅
- `[evaluation/README.md]` — Benchmarks report "Avg Input Tokens per Question" and "Avg Output Tokens per Question" per agent/tool.

### b_methodology ✅
- `[evaluation/README.md]` — Three test targets: `memmachine` (retrieval only), `retrieval_agent` (orchestrated), `llm` (baseline without MemMachine). Metrics include recall, precision, llm_score per category/level, per-tool accuracy, and per-tool token usage. Additional datasets: WikiMultiHop, HotpotQA.
- `[evaluation/retrieval_agent/README.md]` — Configuration file controls "the language model, embedder, reranker, and database for every run — enabling non-OpenAI and local models."

## Metadata

- **description:** "Universal memory layer for AI Agents. It provides scalable, extensible, and interoperable memory storage and retrieval to streamline AI agent state management for next-generation autonomous systems."
- **deployment:** Docker, Docker Compose (one-command: `./memmachine-compose.sh`), pip install (`pip install memmachine`), Kubernetes (Helm chart), AWS CloudFormation, managed cloud (console.memmachine.ai)
- **storage:** Neo4j (graph database for episodic memory), PostgreSQL + pgvector (relational + vector for semantic/profile memory)
- **integration:** Python SDK, TypeScript SDK, REST API v2, MCP Server (stdio + HTTP), LangChain, LangGraph, CrewAI, LlamaIndex, AWS Strands Agent SDK, n8n, Dify, FastGPT, OpenClaw, NebulaGraph Enterprise, GPT Store
- **setup:** 5-minute quickstart via Docker Compose. `pip install memmachine-client` for client-side. `memmachine-mcp-stdio` / `memmachine-mcp-http` for MCP. Requires OpenAI API key (or Bedrock/Ollama alternative).
- **license:** Apache 2.0 (Copyright 2025 MemVerge Inc.)
- **created date:** 2025-08-15 (GitHub repo creation)
- **docs URL:** https://docs.memmachine.ai
- **latest release:** v0.3.9 (May 18, 2026), 30 total releases
