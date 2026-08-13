# deja-vu — Evidence

**Repo:** `github.com/vshulcz/deja-vu`
**Stars:** 493
**Language:** Go
**License:** MIT
**Created:** 2026-07-01
**Description:** Retroactive local memory for 17 coding agents — indexes the session transcripts the agents already write to disk (no capture step, history from before install), serves it back over MCP/hooks; zero daemon, no API keys, no LLM calls.

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

### Web/TUI ✅
- Source: [cmd/deja/view.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/cmd/deja/view.go#L72) — `deja view` writes the whole memory as one self-contained local HTML page and opens it in the browser. Everything is inlined; the page makes no network requests.

### Offline ✅
- Source: [docs/guide/privacy.html](https://github.com/vshulcz/deja-vu/blob/v0.16.0/docs/guide/privacy.html#L57) — "Indexing and search have no network path"; network only for self-update and optional SSH sync.

### Multi-agent ✅
- Source: [README.md](https://github.com/vshulcz/deja-vu/blob/v0.16.0/README.md#L21) — one shared index across 12 agents ("solve it in Codex, Claude remembers"); [cmd/deja/handoff.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/cmd/deja/handoff.go) — packaged context handoff between agents.

### LLM providers (count: 0) ✅
- Source: [README.md](https://github.com/vshulcz/deja-vu/blob/v0.16.0/README.md#L3) — no LLM calls at all; memory is indexed and served without any model. Optional local embedding endpoint (Ollama/LM Studio) for rerank: [internal/embed/client.go#L20](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/embed/client.go#L20).

### Cache optimization ❌

### Procedural memory ❌

### Sandboxed execution ❌

### Scheduled/autonomous ❌

### Privacy/encrypt ✅
- Source: [internal/redact/redact.go#L70](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/redact/redact.go#L70) — secrets (keys, JWTs, PEM blocks, high-entropy values) stripped at index time. Honest limit: index is plaintext under file permissions, no encryption — `doctor` states this in output: [cmd/deja/doctor.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/cmd/deja/doctor.go#L343).

### Data export ✅
- Source: [internal/index/sync.go#L33](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/index/sync.go#L33) — `deja sync export` (JSONL records); `deja share` sanitized digests; `deja promote --to` Markdown export.

---

## Data Model

### Entities ❌

### Actions ❌

### Keywords/tags ✅
- Source: [cmd/deja/promote.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/cmd/deja/promote.go#L43) and [cmd/deja/remember.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/cmd/deja/remember.go#L26) — `--tag` on both `deja promote` and `deja remember`; tags are normalised (deduplicated, `#` stripped) and stored per note.

### Anticipated queries ❌

### Trigger rules ❌

### Domain tag ❌

### Task type ❌

### Context (why) ❌

### Source attribution ✅
- Source: [cmd/deja/promote.go#L17](https://github.com/vshulcz/deja-vu/blob/v0.16.0/cmd/deja/promote.go#L17) — every curated note carries provenance (harness:session-id, date); search hits show source session, harness, project and update date.

### Origin + trust ✅
- Source: [internal/policy/policy.go#L64](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/policy/policy.go#L64) — origins classified `local` / `imported:<peer>`; policy table decides which origin may activate on which path (search / MCP / auto-inject); receipts and `deja log` name the rule.

### Emotional ❌

### Conflict surfacing ✅
- Source: [cmd/deja/promote.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/cmd/deja/promote.go#L94) — promoting a note that covers ground an existing accepted note already covers prints `conflict: another accepted note covers this ground — …` and points at `--state superseded`.

### Layered memory ✅
- Source: [cmd/deja/promote.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/cmd/deja/promote.go#L14) — curated note layer (`deja promote`, lifecycle states accepted/rejected/superseded/stale) sits above raw transcript layer and outranks it in recall.

### Time-travel ✅
- Source: [cmd/deja/promote.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/cmd/deja/promote.go#L60) — notes carry `accepted | rejected | superseded | stale`, so a superseded version stays readable rather than being overwritten.
- Source: [internal/index/reltime.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/index/reltime.go) — temporal search: `--since`, relative expressions and month names resolve against session timestamps.
- Reading this against your definition ("past sessions, superseded versions, or temporal search"): deja queries past sessions by construction, and both other clauses hold. Mark it ❌ if you scope this row to browsing a system's own memory history rather than session history — I would rather it be wrong in your favour than mine.

### Schema fields (count: 6) ✅
- Source: [internal/index/index.go#L126](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/index/index.go#L126) — Record{Key, SourcePath, Role, Text, Time} + session metadata (ID, Harness, Project, Title, Started, Updated).

---

## Search & Retrieval

### Full-text ✅
- Source: [internal/search/search.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/search/search.go#L280) — BM25 over postings index with proximity/title/reuse boosts.

### Semantic/vector ✅
- Source: [internal/embed/client.go#L20](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/embed/client.go#L20) — opt-in local embedding endpoint (auto-probes Ollama :11434 and LM Studio :1234); semantic tier when lexical returns nothing.

### Hybrid (BM25+Vec) ✅
- Source: [internal/embed/rerank.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/embed/rerank.go) — vector rerank over BM25 candidates when the local endpoint is available; `deja bench recall` reports lexical and hybrid rows.

### Deep (incl. thinking) ❌
- (thinking parts are deliberately skipped at parse time: [internal/sources/kimi.go#L23](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/sources/kimi.go#L23))

### Code graph ❌

### Docs search ❌

### Fact metadata query ✅
- Source: [cmd/deja/main.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/cmd/deja/main.go#L800) — filters `--harness`, `--project`, `--since`, `--role` on search/last/blame; `deja blame <path>` queries by file mention.

### Timeline view ✅
- Source: [cmd/deja/statshtml.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/cmd/deja/statshtml.go) — `deja stats --html` renders an activity timeline; `deja last` is a chronological session listing.

### Search modes (count: 6) ✅
- Source: [internal/index/retrieval.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/index/retrieval.go#L533) — exact → substring → stem/suffix forms → fuzzy (Damerau) → co-occurrence rescue → semantic (opt-in); each degradation step is narrated in output.

### Data sources (count: 13) ✅
- Source: [internal/sources/registry.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/sources/registry.go) — Claude Code, Codex, opencode, Cursor (CLI+IDE), aider, Gemini CLI, Antigravity, Grok Build, Qwen Code, Kimi Code, pi, Copilot CLI + deja's own notes.

---

## Knowledge Lifecycle

### Decay/forgetting ✅
- Source: [internal/search/search.go#L322](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/search/search.go#L322) — freshness decay in ranking (older sessions rank lower). Note: ranking decay only, no automatic deletion.

### Supersede/replace ✅
- Source: [internal/search/search.go#L213](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/search/search.go#L213) — earlier attempts on the same ground are marked `[earlier attempt — a newer session covers this]`; `deja promote --state superseded` supersedes curated notes append-only.

### Contradiction detection ❌

### Quarantine ❌

### Auto-resolution ❌

### Trust model ✅
- Source: [internal/policy/policy.go#L46](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/policy/policy.go#L46) — per-activation × per-origin allow table (`policy.json`); imported peers can be denied per path; every injection receipt names the policy that allowed it.

### Explicit forget ✅
- Source: [internal/index/privacy.go#L118](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/index/privacy.go#L118) — `deja forget --session/--project/--before` with persisted tombstones (survive rebuilds), `--dry-run`, `--unforget`.

---

## Extraction Pipeline

### Auto-extraction ❌
- (by design: serves verbatim transcript evidence, not LLM-extracted facts)

### Content-aware preprocessing ✅
- Source: [internal/redact/redact.go#L70](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/redact/redact.go#L70) — redaction before indexing; [internal/digest/digest.go#L134](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/digest/digest.go#L134) — tool-output/noise/artifact filtering for digests.

### Deduplication ✅
- Source: [internal/index/ingest.go#L520](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/index/ingest.go#L520) — message-level dedup at ingest; [internal/search/recall.go#L166](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/search/recall.go#L166) — near-duplicate session suppression in auto-recall.

### Quality refinement ❌

### Narrative generation ❌

### Clustering ❌

### Recurrence detection ✅
- Source: [cmd/deja/hook_prompt.go#L240](https://github.com/vshulcz/deja-vu/blob/v0.16.0/cmd/deja/hook_prompt.go#L240) — déjà vu moments: a prompt matching prior work triggers a visible "you have been here — <session> (<age>)" line; counted in `deja stats`.

### Persona extraction ❌

---

## Platform Support

### Claude Code ✅
- Source: [internal/sources/claude.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/sources/claude.go) — transcripts + SessionStart/UserPromptSubmit/PreCompact hooks + MCP.

### Codex ✅
- Source: [internal/sources/codex.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/sources/codex.go) — transcripts + session-start hook + MCP (config.toml).

### OpenCode ✅
- Source: [internal/sources/opencode.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/sources/opencode.go) — reads opencode.db directly + deja.js plugin (session-start inject) + MCP.

### Gemini CLI ✅
- Source: [internal/sources/gemini.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/sources/gemini.go) — transcripts + MCP (settings.json).

### Copilot ✅
- Source: [internal/sources/copilot.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/sources/copilot.go) — session-state transcripts + MCP + skill guidance.

### Cursor ✅
- Source: [internal/sources/cursor.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/sources/cursor.go) — CLI transcripts + IDE sqlite stores + MCP (mcp.json).

### Windsurf ❌

### OpenClaw ✅
- Source: [internal/sources/registry.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/sources/registry.go#L300) — OpenClaw sessions are parsed and `deja install` writes the MCP server into OpenClaw's config.

### Hermes ✅
- Source: [internal/sources/hermes.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/sources/hermes.go) — Hermes Agent sessions are indexed, with a plugin and MCP wiring installed by `deja install`.

### pi/omp ✅
- Source: [internal/sources/pi.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/sources/pi.go) — pi session transcripts + MCP (mcp.json).

### Antigravity ✅
- Source: [internal/sources/antigravity.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/internal/sources/antigravity.go) — transcript ingestion + MCP config (GUI app, so no hook injection).

*(also indexes aider, Grok Build, Qwen Code and Kimi Code — no columns for those)*

---

## Benchmarks

### LoCoMo ✅
- Score: session-level retrieval, 1,982 questions — hit@1 **69.8%**, hit@5 85.6%, MRR 0.766, median search ~6 ms.
- Harness: [scripts/locomo/main.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/scripts/locomo/main.go) — `go run ./scripts/locomo -data locomo10.json`.
- Not comparable to most published LoCoMo numbers, and the page says so: those are end-to-end QA accuracy with an answering LLM, deja reports retrieval only.

### LongMemEval ✅
- Score: LongMemEval-S, session-level retrieval, 470 questions on the cleaned set — hit@1 **84.9%**, hit@5 94.3%, hit@10 95.7%, MRR 0.890, median search ~40 ms. Full set including abstention (500 questions): hit@1 84.2%.
- Harness: [scripts/longmemeval/main.go](https://github.com/vshulcz/deja-vu/blob/v0.16.0/scripts/longmemeval/main.go) — `go run ./scripts/longmemeval -skip-abs -data longmemeval_s.json`.
- Methodology: [benchmarks page](https://vshulcz.github.io/deja-vu/guide/benchmarks.html). Haystack sessions are written as real transcript files and indexed through the production path; questions are used verbatim, no LLM, no embeddings, no query rewriting.
- Caveat stated on the page: hit@k credits a question when any evidence session ranks in the top k, which is looser than the official per-evidence metric.

### PersonaMem ❌

### Token reduction ✅
- Source: [docs/guide/benchmarks.html](https://github.com/vshulcz/deja-vu/blob/v0.16.0/docs/guide/benchmarks.html) — `deja bench context`: ~200× fewer tokens to working context vs grepping raw logs at equal fact coverage, seeded and reproducible; `deja stats --impact` reports the served-vs-raw ratio measured on the user's own machine.

### Methodology open ✅
- Source: [docs/guide/benchmarks.html](https://github.com/vshulcz/deja-vu/blob/v0.16.0/docs/guide/benchmarks.html) — benchmark harness ships in the binary (`deja bench recall`, `deja bench context`), seeded, runnable on any corpus.
