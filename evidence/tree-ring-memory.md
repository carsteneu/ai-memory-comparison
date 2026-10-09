# Tree Ring Memory — Evidence

> Every checked claim below is backed by public source code or documentation.
> Sources are pinned to Tree Ring Memory commit `6e734451f150704197fa872a3bb213a7e4cc3c33` for review stability.
> Disclosure: submitted by the Tree Ring Memory project maintainer.

**Repo:** `github.com/TerminallyLazy/Tree-Ring-Memory`
**Stars:** 3
**Language:** Rust
**License:** MIT
**Created:** 2026-07-04
**Description:** Framework-agnostic, local-first memory lifecycle layer for AI agents with a Rust CLI, SQLite/FTS recall, forgetting, audit, consolidation, and portable agent guidance.

---

## System Metadata

| Field | Value |
|-------|-------|
| **Deployment** | `Local CLI` |
| **Storage** | `SQLite + FTS5` |
| **Integration** | `CLI / local skill / DOX-Revolve adapters` |
| **Single binary?** | `yes (Rust CLI release artifact)` |
| **Setup** | `curl installer / brew install / cargo install` |
| **Pricing** | `free (MIT)` |
| **Storage unit** | `MemoryEvent` |

- Metadata source: [`README.md` lines 47-56](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L47-L56) — documents Rust crates for core, SQLite/FTS storage, and native CLI ownership.
- Metadata source: [`README.md` lines 60-70](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L60-L70) — documents curl installer and Homebrew setup.
- Metadata source: [`README.md` lines 373-375](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L373-L375) — documents release-mode CLI packaging into platform tarballs.

---

## Architecture

### Proxy ❌

### Web/TUI ✅
- Source: [`README.md` lines 297-305](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L297-L305) — documents the Ratatui terminal console and `tree-ring tui`.

### Offline ✅
- Source: [`README.md` lines 34-45](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L34-L45) — initial implementation is SQLite with no required cloud services, and current runtime is Rust-native.
- Source: [`README.md` lines 282-295](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L282-L295) — audit, consolidation, and maintenance are deterministic local operations.

### Multi-agent ❌

### LLM providers (count: 0) ✅
- Source: [`README.md` lines 286-290](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L286-L290) — consolidation is deterministic and does not require an LLM.

### Cache optimization ❌

### Procedural memory ❌

### Sandboxed execution ❌

### Scheduled/autonomous ❌

### Privacy/encrypt ✅
- Source: [`README.md` lines 85-89](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L85-L89) — persistent memory lives in the configured local memory root.
- Source: [`README.md` lines 337-339](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L337-L339) — sensitive details are hidden by default and secret-like memory is blocked before storage.

### Data export ✅
- Source: [`README.md` lines 275-280](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L275-L280) — `tree-ring export` writes newline-delimited JSON with schema metadata and import validation.

---

## Data Model

### Entities ❌

### Actions ❌

### Keywords/tags ✅
- Source: [`crates/tree-ring-memory-cli/src/main.rs` lines 51-64](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/crates/tree-ring-memory-cli/src/main.rs#L51-L64) — `remember` accepts repeated `--tag` values.
- Source: [`crates/tree-ring-memory-sqlite/src/lib.rs` lines 104-134](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/crates/tree-ring-memory-sqlite/src/lib.rs#L104-L134) — SQLite stores `tags_json` and indexes `tags` in the FTS table.

### Anticipated queries ❌

### Trigger rules ❌

### Domain tag ❌

### Task type ❌

### Context (why) ✅
- Source: [`README.md` lines 198-223](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L198-L223) — `tree-ring evidence` records outcomes with evidence references from evaluations, checkpoints, PRs, issues, logs, or run artifacts.
- Source: [`crates/tree-ring-memory-core/src/models.rs` lines 109-148](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/crates/tree-ring-memory-core/src/models.rs#L109-L148) — each memory has `details`, `source`, `links`, review metadata, confidence, salience, and lifecycle fields.

### Source attribution ✅
- Source: [`crates/tree-ring-memory-core/src/models.rs` lines 57-67](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/crates/tree-ring-memory-core/src/models.rs#L57-L67) — `MemorySource` stores `source_type`, source reference, and quote.
- Source: [`crates/tree-ring-memory-core/src/recall.rs` lines 147-156](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/crates/tree-ring-memory-core/src/recall.rs#L147-L156) — recall scoring distinguishes user, contract, eval, file, tool, summary, manual, and unknown sources.

### Origin + trust ✅
- Source: [`crates/tree-ring-memory-core/src/recall.rs` lines 147-156](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/crates/tree-ring-memory-core/src/recall.rs#L147-L156) — source types are assigned different authority weights during recall.

### Emotional ❌

### Conflict surfacing ✅
- Source: [`README.md` lines 282-284](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L282-L284) — audit reports conservative contradiction candidates.
- Source: [`crates/tree-ring-memory-core/src/audit.rs` lines 312-351](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/crates/tree-ring-memory-core/src/audit.rs#L312-L351) — contradiction audit groups use/avoid guidance by project, scope, event type, tag, and subject, then emits findings.

### Layered memory ✅
- Source: [`README.md` lines 5-7](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L5-L7) — memory is organized into tree rings where fresh memory, older compressed memory, scars, and heartwood have distinct roles.
- Source: [`crates/tree-ring-memory-core/src/models.rs` lines 6-9](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/crates/tree-ring-memory-core/src/models.rs#L6-L9) — allowed ring and scope values include cambium, outer, inner, heartwood, scar, and seed.

### Time-travel ✅
- Source: [`README.md` lines 275-280](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L275-L280) — export excludes superseded memories by default but can include them with `--include-superseded`.
- Source: [`crates/tree-ring-memory-sqlite/src/lib.rs` lines 215-220](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/crates/tree-ring-memory-sqlite/src/lib.rs#L215-L220) — storage can list all memories or filter out superseded ones.

### Schema fields (count: 18) ✅
- Source: [`crates/tree-ring-memory-core/src/models.rs` lines 109-148](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/crates/tree-ring-memory-core/src/models.rs#L109-L148) — excluding ID and timestamps, `MemoryEvent` has 18 structured fields: project, agent_profile, scope, ring, event_type, summary, details, source, tags, salience, confidence, sensitivity, retention, expires_at, supersedes, superseded_by, links, and review.

---

## Search & Retrieval

### Full-text ✅
- Source: [`crates/tree-ring-memory-sqlite/src/lib.rs` lines 128-134](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/crates/tree-ring-memory-sqlite/src/lib.rs#L128-L134) — creates an FTS5 table over summary, details, tags, and source reference.
- Source: [`crates/tree-ring-memory-sqlite/src/lib.rs` lines 260-267](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/crates/tree-ring-memory-sqlite/src/lib.rs#L260-L267) — recall queries `memory_fts MATCH ?` and orders by FTS rank.

### Semantic/vector ❌

### Hybrid (BM25+Vec) ❌

### Deep (incl. thinking) ❌

### Code graph ❌

### Docs search ❌

### Fact metadata query ✅
- Source: [`crates/tree-ring-memory-sqlite/src/lib.rs` lines 289-367](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/crates/tree-ring-memory-sqlite/src/lib.rs#L289-L367) — text search can be filtered by project, agent profile, scope, rings, event types, sensitivity visibility, superseded visibility, and limit.

### Timeline view ❌

### Search modes (count: 1) ✅
- Source: [`README.md` lines 167-181](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L167-L181) — public search mode is `tree-ring recall`.

### Data sources (count: 3) ✅
- Source: [`README.md` lines 227-253](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L227-L253) — manual memories, DOX `AGENTS.md` summaries, and Revolve/evaluation records persist through the same SQLite store.

---

## Knowledge Lifecycle

### Decay/forgetting ✅
- Source: [`crates/tree-ring-memory-core/src/recall.rs` lines 131-135](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/crates/tree-ring-memory-core/src/recall.rs#L131-L135) — recall score includes automatic recency decay based on memory age.
- Source: [`README.md` lines 292-295](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L292-L295) — maintenance can delete eligible temporary-memory expiry or redact secret-like memories when explicit apply flags are used.

### Supersede/replace ✅
- Source: [`crates/tree-ring-memory-sqlite/src/lib.rs` lines 369-384](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/crates/tree-ring-memory-sqlite/src/lib.rs#L369-L384) — `supersede` marks the old memory with `superseded_by`.
- Source: [`crates/tree-ring-memory-sqlite/src/lib.rs` lines 709-713](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/crates/tree-ring-memory-sqlite/src/lib.rs#L709-L713) — imported or stored events with `supersedes` apply supersession chains.

### Contradiction detection ✅
- Source: [`crates/tree-ring-memory-core/src/audit.rs` lines 312-351](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/crates/tree-ring-memory-core/src/audit.rs#L312-L351) — contradiction audit detects contradictory use/avoid guidance pairs.

### Quarantine ❌

### Auto-resolution ❌

### Trust model ✅
- Source: [`crates/tree-ring-memory-core/src/recall.rs` lines 147-156](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/crates/tree-ring-memory-core/src/recall.rs#L147-L156) — source authority hierarchy gives different weights to user, contract, eval, file, tool, summary, manual, and unknown sources.

### Explicit forget ✅
- Source: [`README.md` lines 167-177](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L167-L177) — CLI exposes `tree-ring forget` plus export, import, audit, consolidate, and maintenance commands.
- Source: [`crates/tree-ring-memory-sqlite/src/lib.rs` lines 386-409](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/crates/tree-ring-memory-sqlite/src/lib.rs#L386-L409) — store implements delete and redact operations.

---

## Extraction Pipeline

### Auto-extraction ❌
- Source: [`README.md` lines 416-420](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L416-L420) — Tree Ring does not scrape transcripts or run a hidden recorder; durable writes require explicit CLI calls or explicit adapter/import/TUI/consolidation/maintenance actions.

### Content-aware preprocessing ❌

### Deduplication ❌

### Quality refinement ✅
- Source: [`README.md` lines 282-295](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L282-L295) — audit and maintenance report stale, sensitive, low-confidence, supersession, contradiction, expiry, secret redaction, and FTS repair concerns.
- Source: [`crates/tree-ring-memory-core/src/audit.rs` lines 124-149](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/crates/tree-ring-memory-core/src/audit.rs#L124-L149) — `audit_memories` runs the selected audit types and emits findings.

### Narrative generation ✅
- Source: [`README.md` lines 286-290](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L286-L290) — consolidation creates deterministic local summary memories and handles sensitive-memory summarization cautiously.

### Clustering ❌

### Recurrence detection ❌

### Persona extraction ❌

---

## Platform Support

For each platform: checked only when a documented bridge target or integration path exists.

### Claude Code ✅
- Source: [`README.md` lines 409-412](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L409-L412) — recommends `.claude/skills/tree-ring-memory/SKILL.md` plus `CLAUDE.md` references for Claude Code.

### Codex ✅
- Source: [`README.md` lines 409-412](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L409-L412) — recommends `.agents/skills/tree-ring-memory/SKILL.md` for Codex/Gemini-style skill loaders.

### OpenCode ✅
- Source: [`README.md` lines 409-412](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L409-L412) — recommends root `AGENTS.md` references for OpenCode/DOX-style agents.

### Gemini CLI ✅
- Source: [`README.md` lines 409-412](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L409-L412) — recommends `.agents/skills/tree-ring-memory/SKILL.md` for Codex/Gemini-style skill loaders.

### Copilot ❌

### Cursor ❌

### Windsurf ❌

### OpenClaw ❌

### Hermes ❌

### pi/omp ✅
- Source: [`README.md` lines 409-412](https://github.com/TerminallyLazy/Tree-Ring-Memory/blob/6e734451f150704197fa872a3bb213a7e4cc3c33/README.md#L409-L412) — recommends `.pi/settings.json` resource references for Pi.

### Antigravity ❌

---

## Benchmarks

### LoCoMo ❌
- Score: `—`

### LongMemEval ❌
- Score: `—`

### PersonaMem ❌
- Score: `—`

### Token reduction ❌
- Score: `—`

### Methodology open ❌
