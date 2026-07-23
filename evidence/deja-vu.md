# deja-vu — Evidence

**Repo:** `github.com/vshulcz/deja-vu`
**Stars:** 448
**Language:** Go
**License:** MIT
**Created:** 2026-07-01
**Description:** Retroactive local memory for 12 coding agents — indexes the session transcripts the agents already write to disk (no capture step, history from before install), serves it back over MCP/hooks; zero daemon, no API keys, no LLM calls.

---

## System Metadata

| Field | Value |
|-------|-------|
| **Deployment** | Local CLI, single binary |
| **Storage** | Custom append-only log + postings index (`~/.cache/deja/index.db`) |
| **Integration** | MCP + hooks + CLI + opencode plugin |
| **Single binary?** | yes |
| **Setup** | `curl \| sh` / brew / npm / go install |
| **Pricing** | free |
| **Storage unit** | Message record (verbatim transcript text, redacted) |

---

## Architecture

### Proxy ❌

### Web/TUI ❌

### Offline ✅
- Source: [docs/guide/privacy.html](https://github.com/vshulcz/deja-vu/blob/v0.15.1/docs/guide/privacy.html#L57) — "Indexing and search have no network path"; network only for self-update and optional SSH sync.

### Multi-agent ✅
- Source: [README.md](https://github.com/vshulcz/deja-vu/blob/v0.15.1/README.md#L21) — one shared index across 12 agents ("solve it in Codex, Claude remembers"); [cmd/deja/handoff.go](https://github.com/vshulcz/deja-vu/blob/v0.15.1/cmd/deja/handoff.go) — packaged context handoff between agents.

### LLM providers (count: 0) ✅
- Source: [README.md](https://github.com/vshulcz/deja-vu/blob/v0.15.1/README.md#L3) — no LLM calls at all; memory is indexed and served without any model. Optional local embedding endpoint (Ollama/LM Studio) for rerank: [internal/embed/client.go#L20](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/embed/client.go#L20).

### Cache optimization ❌

### Procedural memory ❌

### Sandboxed execution ❌

### Scheduled/autonomous ❌

### Privacy/encrypt ✅
- Source: [internal/redact/redact.go#L70](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/redact/redact.go#L70) — secrets (keys, JWTs, PEM blocks, high-entropy values) stripped at index time. Honest limit: index is plaintext under file permissions, no encryption — `doctor` states this in output: [cmd/deja/doctor.go](https://github.com/vshulcz/deja-vu/blob/v0.15.1/cmd/deja/doctor.go#L343).

### Data export ✅
- Source: [internal/index/sync.go#L33](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/index/sync.go#L33) — `deja sync export` (JSONL records); `deja share` sanitized digests; `deja promote --to` Markdown export.

---

## Data Model

### Entities ❌

### Actions ❌

### Keywords/tags ❌

### Anticipated queries ❌

### Trigger rules ❌

### Domain tag ❌

### Task type ❌

### Context (why) ❌

### Source attribution ✅
- Source: [cmd/deja/promote.go#L17](https://github.com/vshulcz/deja-vu/blob/v0.15.1/cmd/deja/promote.go#L17) — every curated note carries provenance (harness:session-id, date); search hits show source session, harness, project and update date.

### Origin + trust ✅
- Source: [internal/policy/policy.go#L64](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/policy/policy.go#L64) — origins classified `local` / `imported:<peer>`; policy table decides which origin may activate on which path (search / MCP / auto-inject); receipts and `deja log` name the rule.

### Emotional ❌

### Conflict surfacing ❌

### Layered memory ✅
- Source: [cmd/deja/promote.go](https://github.com/vshulcz/deja-vu/blob/v0.15.1/cmd/deja/promote.go#L14) — curated note layer (`deja promote`, lifecycle states accepted/rejected/superseded/stale) sits above raw transcript layer and outranks it in recall.

### Time-travel ❌

### Schema fields (count: 6) ✅
- Source: [internal/index/index.go#L126](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/index/index.go#L126) — Record{Key, SourcePath, Role, Text, Time} + session metadata (ID, Harness, Project, Title, Started, Updated).

---

## Search & Retrieval

### Full-text ✅
- Source: [internal/search/search.go](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/search/search.go#L280) — BM25 over postings index with proximity/title/reuse boosts.

### Semantic/vector ✅
- Source: [internal/embed/client.go#L20](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/embed/client.go#L20) — opt-in local embedding endpoint (auto-probes Ollama :11434 and LM Studio :1234); semantic tier when lexical returns nothing.

### Hybrid (BM25+Vec) ✅
- Source: [internal/embed/rerank.go](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/embed/rerank.go) — vector rerank over BM25 candidates when the local endpoint is available; `deja bench recall` reports lexical and hybrid rows.

### Deep (incl. thinking) ❌
- (thinking parts are deliberately skipped at parse time: [internal/sources/kimi.go#L23](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/sources/kimi.go#L23))

### Code graph ❌

### Docs search ❌

### Fact metadata query ✅
- Source: [cmd/deja/main.go](https://github.com/vshulcz/deja-vu/blob/v0.15.1/cmd/deja/main.go#L800) — filters `--harness`, `--project`, `--since`, `--role` on search/last/blame; `deja blame <path>` queries by file mention.

### Timeline view ✅
- Source: [cmd/deja/statshtml.go](https://github.com/vshulcz/deja-vu/blob/v0.15.1/cmd/deja/statshtml.go) — `deja stats --html` renders an activity timeline; `deja last` is a chronological session listing.

### Search modes (count: 6) ✅
- Source: [internal/index/retrieval.go](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/index/retrieval.go#L533) — exact → substring → stem/suffix forms → fuzzy (Damerau) → co-occurrence rescue → semantic (opt-in); each degradation step is narrated in output.

### Data sources (count: 13) ✅
- Source: [internal/sources/registry.go](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/sources/registry.go) — Claude Code, Codex, opencode, Cursor (CLI+IDE), aider, Gemini CLI, Antigravity, Grok Build, Qwen Code, Kimi Code, pi, Copilot CLI + deja's own notes.

---

## Knowledge Lifecycle

### Decay/forgetting ✅
- Source: [internal/search/search.go#L322](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/search/search.go#L322) — freshness decay in ranking (older sessions rank lower). Note: ranking decay only, no automatic deletion.

### Supersede/replace ✅
- Source: [internal/search/search.go#L213](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/search/search.go#L213) — earlier attempts on the same ground are marked `[earlier attempt — a newer session covers this]`; `deja promote --state superseded` supersedes curated notes append-only.

### Contradiction detection ❌

### Quarantine ❌

### Auto-resolution ❌

### Trust model ✅
- Source: [internal/policy/policy.go#L46](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/policy/policy.go#L46) — per-activation × per-origin allow table (`policy.json`); imported peers can be denied per path; every injection receipt names the policy that allowed it.

### Explicit forget ✅
- Source: [internal/index/privacy.go#L118](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/index/privacy.go#L118) — `deja forget --session/--project/--before` with persisted tombstones (survive rebuilds), `--dry-run`, `--unforget`.

---

## Extraction Pipeline

### Auto-extraction ❌
- (by design: serves verbatim transcript evidence, not LLM-extracted facts)

### Content-aware preprocessing ✅
- Source: [internal/redact/redact.go#L70](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/redact/redact.go#L70) — redaction before indexing; [internal/digest/digest.go#L134](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/digest/digest.go#L134) — tool-output/noise/artifact filtering for digests.

### Deduplication ✅
- Source: [internal/index/ingest.go#L520](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/index/ingest.go#L520) — message-level dedup at ingest; [internal/search/recall.go#L166](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/search/recall.go#L166) — near-duplicate session suppression in auto-recall.

### Quality refinement ❌

### Narrative generation ❌

### Clustering ❌

### Recurrence detection ✅
- Source: [cmd/deja/hook_prompt.go#L240](https://github.com/vshulcz/deja-vu/blob/v0.15.1/cmd/deja/hook_prompt.go#L240) — déjà vu moments: a prompt matching prior work triggers a visible "you have been here — <session> (<age>)" line; counted in `deja stats`.

### Persona extraction ❌

---

## Platform Support

### Claude Code ✅
- Source: [internal/sources/claude.go](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/sources/claude.go) — transcripts + SessionStart/UserPromptSubmit/PreCompact hooks + MCP.

### Codex ✅
- Source: [internal/sources/codex.go](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/sources/codex.go) — transcripts + session-start hook + MCP (config.toml).

### OpenCode ✅
- Source: [internal/sources/opencode.go](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/sources/opencode.go) — reads opencode.db directly + deja.js plugin (session-start inject) + MCP.

### Gemini CLI ✅
- Source: [internal/sources/gemini.go](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/sources/gemini.go) — transcripts + MCP (settings.json).

### Copilot ✅
- Source: [internal/sources/copilot.go](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/sources/copilot.go) — session-state transcripts + MCP + skill guidance.

### Cursor ✅
- Source: [internal/sources/cursor.go](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/sources/cursor.go) — CLI transcripts + IDE sqlite stores + MCP (mcp.json).

### Windsurf ❌

### OpenClaw ❌

### Hermes ❌

### pi/omp ✅
- Source: [internal/sources/pi.go](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/sources/pi.go) — pi session transcripts + MCP (mcp.json).

### Antigravity ✅
- Source: [internal/sources/antigravity.go](https://github.com/vshulcz/deja-vu/blob/v0.15.1/internal/sources/antigravity.go) — transcript ingestion + MCP config (GUI app, so no hook injection).

*(also indexes aider, Grok Build, Qwen Code and Kimi Code — no columns for those)*

---

## Benchmarks

### LoCoMo ❌

### LongMemEval ❌

### PersonaMem ❌

### Token reduction ✅
- Source: [docs/guide/benchmarks.html](https://github.com/vshulcz/deja-vu/blob/v0.15.1/docs/guide/benchmarks.html) — `deja bench context`: ~200× fewer tokens to working context vs grepping raw logs at equal fact coverage, seeded and reproducible; `deja stats --impact` reports the served-vs-raw ratio measured on the user's own machine.

### Methodology open ✅
- Source: [docs/guide/benchmarks.html](https://github.com/vshulcz/deja-vu/blob/v0.15.1/docs/guide/benchmarks.html) — benchmark harness ships in the binary (`deja bench recall`, `deja bench context`), seeded, runnable on any corpus.
