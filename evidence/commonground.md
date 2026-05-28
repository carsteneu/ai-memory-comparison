# CommonGround Audit Evidence

**Date audited**: 2026-05-28
**GitHub**: https://github.com/Intelligent-Internet/CommonGround
**Stars**: 137
**Auditor**: DeepSeek V4 Pro (OpenCode)

---

## Description

CommonGround Kernel v3r1 is an open-source "constitutional ledger kernel" for human-agent and multi-agent collaboration. It is **not** a full memory product — it describes itself as "memory-ready, not memory-complete." It provides durable work records (Agent identity, Turn lifecycle, claim fencing, causal lineage, semantic records) on top of PostgreSQL as the ground layer. Higher-level memory abstraction, search, and knowledge distillation are explicitly deferred to upper layers. Think of it as a coordination/audit ledger, not an agent memory system.

---

## Deployment

- Python package via PyPI: `uv tool install 'commonground-kernel[server]'`
- CLI tool: `cg`
- Local development: `cg local run` (single-port: service + admin on one uvicorn process)

## Storage

PostgreSQL (required). Uses a CardBox submodule for content storage schema. `PG_DSN` environment variable.

## Integration

- HTTP API at `/v3r1/projects/{project_id}/...`
- Python clients: `HttpAgentClient`, `ProjectionHttpClient`
- CLI: `cg` (dispatch, turn inspection, work-memory reporting, worker lifecycle, project observation)
- BYOA (Bring Your Own Agent): agents can run in any runtime (Codex, NanoBot, OpenCode, script, service)
- NanoBot: reference integration fixtures under `Integrations/nanobot/`
- Claude Code skills: `.agents/skills/` directory with `cg-worker/SKILL.md`

## Setup

1. `uv tool install 'commonground-kernel[server]'`
2. PostgreSQL database + `PG_DSN`
3. `cg setup project seed --default-local`
4. `cg local run --project-id cg-demo`

## License

Apache 2.0

## Created Date

v3r1 initial open-source preview released ~May 20, 2026 (v3.1.0 tag). Earlier v1 preview existed on `legacy/v1` branch. Repository has 20 commits.

## Docs URL

https://github.com/Intelligent-Internet/CommonGround/tree/main/docs/en

---

## Feature Audit

### Architecture

| Feature | Present | Evidence |
|---------|---------|----------|
| webUi | **false** | No web UI. Dashboard/projections mentioned as future upper-layer concerns: "Push notifications, dashboards, summaries, and projections can make work easier to see. They do not replace the correctness baseline." — README |
| offline | **false** | PostgreSQL required. Local-first developer path exists (`cg local run`) but requires running PostgreSQL. Not truly offline. |
| privacy | **true** | Local-first architecture. Pull-first design. Agent credential tokens with 0600 permissions. No hosted service required. "The kernel does not reason for Agents, make strategy judgments... or grant authorization merely because a record was persisted." — Constitution §1.1 |
| export | **false** | No export mechanism. Feed/ledger API exists for inspection but no formal export feature. |
| multiAgent | **true** | Core design goal: "CommonGround Kernel turns real multi-Agent work into durable public facts." "Independent agents at the edges. Durable public work records at the kernel." — README. Multi-agent dispatch, child derivation, parent observation, claim fencing all built in. |
| llmFlex | **true** | Uses `litellm` and `instructor` as dependencies. Agents can be "backed by an LLM, human, service, script, external runtime, or hybrid system." — README. The kernel itself is LLM-agnostic. |

### Data Model

| Feature | Present | Evidence |
|---------|---------|----------|
| entities | **true** | Agent is a first-class entity with stable logical identity. Turn is a first-class work boundary entity. — Constitution §2.1, §2.2 |
| actions | **false** | No action/tool tracking. Semantic records have roles (observation, progress, deliverable) but these describe content roles, not agent actions. |
| keywords | **false** | No keyword tagging system. Metadata fields exist (`public_metadata`, `annotations`) but no keyword entity type. |
| context | **true** | Turn context API: `GET /turns/{turn_id}/context` with `after_turn_seq` + `limit` pagination. Agents can read context to recover judgment. — HTTP Reference, Three-Plane Model §3.5 |
| source | **true** | Provenance tracked per Agent: `registration_provenance_kind`, `registration_provenance_ref`, `registration_provenance_payload_hash`. CauseRef on Turns. Source refs in work-memory manifest records. |
| emotional | **false** | No emotional state tracking. |
| conflict | **false** | No conflict resolution mechanism. Claim fencing prevents concurrent writes but doesn't resolve content conflicts. |
| layeredMemory | **false** | Explicitly deferred: "memory-ready, not memory-complete." "Higher-level memory abstraction, search, dossier surfaces... can be built on top of durable facts, but they are not kernel truth by default." — What Is CommonGround |
| timeTravel | **false** | No time-travel query capability. Ledger has sequence numbers for ordering but no point-in-time reconstruction. Feed is append-only forward iteration. |
| schemaFields | **62** | Counted across 4 DB row types. AgentRow: 19 fields (project_id, agent_id, enabled, accepts_work, capacity, capabilities, grants, public_metadata, created_at, updated_at, last_seen_at, role, description, registered_by_agent_id, registration_provenance_kind, registration_provenance_ref, registration_provenance_payload_hash, admitted_spec_hash). AgentCredentialRow: 14 fields. TurnRow: 21 fields. SpawnEnvelopeRow: 8 fields. Source: `contracts/rows.py`. |

### Search

| Feature | Present | Evidence |
|---------|---------|----------|
| fulltext | **false** | No full-text search. Search is explicitly deferred: "Higher-level memory abstraction, search, dossier surfaces... can be built on top" — What Is CommonGround |
| semantic | **false** | No vector/semantic search. |
| hybrid | **false** | No hybrid search. |
| deep | **false** | No deep search. |
| codeGraph | **false** | No code graph traversal. |
| docsSearch | **false** | No documentation search. |
| factQuery | **false** | Projection API provides filtered queries (agents by role/capability, turns by state/outcome) but no structured fact query system. Feed/ledger is sequential iteration, not queryable facts. |
| timeline | **false** | Ledger has `ledger_seq` ordering and `created_at` timestamps, but no explicit timeline view or reconstruction feature. Feed is paginated forward iteration. |
| searchModes | **0** | Search is entirely out of scope for v3r1 kernel. Explicitly deferred to upper layers. |
| codeGraph | **false** | No code graph. |

### Lifecycle

| Feature | Present | Evidence |
|---------|---------|----------|
| decay | **false** | No content decay. Claim tokens have TTL (`CG_CLAIM_TIMEOUT_SECONDS`, default 30s) but this is authorization fencing, not content decay. |
| supersede | **false** | No learning superseding. Agent metadata can be replaced (`PUT public-metadata`) but no content-level versioning. |
| contradiction | **false** | No contradiction detection or handling. |
| quarantine | **false** | No quarantine mechanism. Sessions/learnings cannot be quarantined. |
| autoResolve | **false** | No auto-resolution. Claim reaper reconciles expired claims but this is authorization cleanup, not content resolution. |
| trustModel | **partial** | Formal trust model through Agent credentials (bearer tokens), claim tokens, and authorization boundaries. The kernel enforces identity verification, claim fencing, and write guards. But no content trust scoring or reputation: "The kernel does not decide on behalf of upper-layer subjects whether a result satisfies business conditions." — Constitution §3.5 |
| explicitForget | **false** | No forget/delete mechanism. Credential revocation exists (`POST .../credentials/{id}:revoke`) but this is authorization removal, not content deletion. |

### Extraction

| Feature | Present | Evidence |
|---------|---------|----------|
| autoExtract | **false** | "The kernel does not reason for Agents... or grant authorization... merely because a record was persisted." — Constitution §3.7. "The kernel must not interpret business fields outside that envelope." — Constitution §3.7 |
| contentPreproc | **false** | No content preprocessing. Payloads are opaque CardBox references to the kernel. |
| dedup | **false** | No deduplication. Idempotency via `dispatch_key` / `request_id` for Turn dispatch, but not for content dedup. |
| qualityRefine | **false** | No quality refinement. |
| narrative | **false** | No narrative generation. |
| clustering | **false** | No clustering. |
| recurrence | **false** | No recurrence detection. |
| persona | **false** | No persona extraction. Agent has `role` and `description` fields set at registration but no dynamic persona modeling. |

### Platform

| Feature | Present | Evidence |
|---------|---------|----------|
| p_claude | **true** | `.agents/skills/` directory follows Claude Code skill convention. AGENTS.md present. |
| p_codex | **true** | Mentioned in BYOA integration scenarios: "It can run in Codex, NanoBot, OpenCode, a script, a service, or another runtime." — Agent Integration Scenarios |
| p_opencode | **true** | Mentioned in BYOA integration scenarios (same source as above). |
| p_gemini | **true** | Skills structure at `.agents/skills/` suggests multi-platform support. BYOA path is runtime-agnostic: any agent that can run `cg` CLI. |
| p_copilot | **false** | No specific Copilot integration or mention. |
| p_cursor | **false** | No Cursor integration. |
| p_windsurf | **false** | No Windsurf integration. |
| p_openclaw | **false** | No OpenClaw integration. |
| p_hermes | **false** | No Hermes integration. |
| p_pi | **false** | No Pi integration. |
| p_antigravity | **false** | No Antigravity integration. |
| p_nanobot | **true** | Explicit reference integration: `Integrations/nanobot/` directory with adapter, runtime, provision lifecycle, and supervisor/leaf worker handlers. |

### Benchmarks

| Feature | Present | Evidence |
|---------|---------|----------|
| b_locomo | **false** | No mention of LoCoMo benchmark anywhere in repository. |
| b_longmemeval | **false** | No mention of LongMemEval. |
| b_personamem | **false** | No mention of PersonaMem. |
| b_token | **false** | No token efficiency benchmarks. |
| b_methodology | **false** | No evaluation methodology documented. Tests are functional/integration (`pytest`), not benchmark-based. |

---

## Key Design Notes

1. **Not a memory system**: CommonGround is explicitly a "Ledger Kernel" — a coordination substrate. Memory is deferred to upper layers. This is by design, not a gap.

2. **Constitutional approach**: The project has a formal constitution (`01-constitution.md`), three-plane model, and design review principles. Design decisions are governed by the axiom "Assume nothing beyond what constraints demand."

3. **Three core entities**: Agent (stable logical executor), Turn (minimum durable work boundary), Complete Semantics (Turn-owned public facts). These three planes form the minimal ontology.

4. **Pull-first design**: "Even if notifications are lost, runtimes restart, or processes move, the system can return from durable facts to correct work judgment." — What Is CommonGround

5. **Claim fencing**: Execution authority is temporary, verifiable, and invalidatable through claim tokens with TTLs. Claims prevent concurrent modification of the same Turn.

6. **Breaking v1→v3r1**: v3r1 is not backward-compatible with v1. Package layout, runtime assumptions, and API surface changed completely.

7. **No automatic effect**: "Readable does not mean automatically legally effective." Historical records provide inspect/audit/reference effects but do not automatically grant continuity, identity proof, or authorization.
