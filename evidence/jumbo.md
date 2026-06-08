# Jumbo — Evidence

> Every ✅ claim backed by public source code or documentation.
> Source: [https://github.com/jumbocontext/jumbo.cli](https://github.com/jumbocontext/jumbo.cli)

**Repo:** `jumbocontext/jumbo.cli`
**Stars:** 102
**Language:** TypeScript
**License:** AGPL-3.0
**Created:** 2025-12-05
**Description:** Goal-driven memory system that serves the right context at the right time

---

## System Metadata

| Field | Value |
|-------|-------|
| **Deployment** | Local CLI |
| **Storage** | Event store + SQLite |
| **Integration** | CLI + hooks + AGENTS.md |
| **Single binary?** | no |
| **Setup** | npm install |
| **Pricing** | free |
| **Storage unit** | Memory entity node (11 types) + relation graph edge |

---

## Architecture

### Proxy ❌

### Web/TUI ✅
- Source: [README.md:160](https://github.com/jumbocontext/jumbo.cli/blob/main/README.md#L160) — Terminal UI is built with Ink and React.
- Source: [docs/flows/cmd-jumbo-flow.md:16](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/flows/cmd-jumbo-flow.md#L16) — Bare `jumbo` launches the TUI.

### Offline ✅
- Source: [README.md:46](https://github.com/jumbocontext/jumbo.cli/blob/main/README.md#L46) — Data stays local.
- Source: [README.md:48](https://github.com/jumbocontext/jumbo.cli/blob/main/README.md#L48) — Jumbo documents no network calls for local operation.
- Source: [docs/getting-started/what-jumbo-creates.md:12](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/getting-started/what-jumbo-creates.md#L12) — `.jumbo/` is the local project memory directory.

### Multi-agent ✅
- Source: [README.md:36](https://github.com/jumbocontext/jumbo.cli/blob/main/README.md#L36) — Jumbo supports running different agents in parallel.
- Source: [README.md:126](https://github.com/jumbocontext/jumbo.cli/blob/main/README.md#L126) — Sessions include pause, resume, compact, and multi-agent support.
- Source: [docs/reference/commands/worker.md:28](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/reference/commands/worker.md#L28) — Worker identity tracks each LLM agent session for ownership and work tracking.

### LLM providers (count: 6+) ✅
- Source: [src/infrastructure/agents/AgentCliGateway.ts:6](https://github.com/jumbocontext/jumbo.cli/blob/main/src/infrastructure/agents/AgentCliGateway.ts#L6) — Supported agent CLI IDs are `claude`, `gemini`, `copilot`, `codex`, `cursor`, and `vibe`.
- Source: [src/infrastructure/agents/AgentCliGateway.ts:18](https://github.com/jumbocontext/jumbo.cli/blob/main/src/infrastructure/agents/AgentCliGateway.ts#L18) — Command mappings define those six backends.
- Source: [README.md:89](https://github.com/jumbocontext/jumbo.cli/blob/main/README.md#L89) — Jumbo also works with any agent that supports AGENTS.md.

### Cache optimization ✅
- Source: [README.md:141](https://github.com/jumbocontext/jumbo.cli/blob/main/README.md#L141) — Writes are append-only events and reads come from optimized SQLite views.
- Source: [src/infrastructure/context/search/migrations/001-create-search-index-entries.sql:1](https://github.com/jumbocontext/jumbo.cli/blob/main/src/infrastructure/context/search/migrations/001-create-search-index-entries.sql#L1) — Global search index is projected from memory entity events.

### Procedural memory ✅
- Source: [README.md:89](https://github.com/jumbocontext/jumbo.cli/blob/main/README.md#L89) — Jumbo explicitly targets harnesses that support open agent skills.
- Source: [assets/skills/refine-jumbo-goals/SKILL.md:3](https://github.com/jumbocontext/jumbo.cli/blob/main/assets/skills/refine-jumbo-goals/SKILL.md#L3) — Shipped refinement skill curates relations before implementation so the agent receives optimal architectural context.
- Source: [assets/skills/codify-jumbo-goal/SKILL.md:3](https://github.com/jumbocontext/jumbo.cli/blob/main/assets/skills/codify-jumbo-goal/SKILL.md#L3) — Shipped codification skill captures new learnings, updates stale entities, and reconciles documentation before closing a goal.
- Source: [JUMBO.md:35](https://github.com/jumbocontext/jumbo.cli/blob/main/JUMBO.md#L35) — Generated agent instructions make real-time memory maintenance part of the agent's job.

### Sandboxed execution ❌

### Scheduled/autonomous ✅
- Source: [docs/reference/commands/work.md:14](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/reference/commands/work.md#L14) — `work refine` is a long-running daemon.
- Source: [docs/reference/commands/work.md:32](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/reference/commands/work.md#L32) — It polls for goals, spawns an agent subprocess, retries, and repeats until stopped.
- Source: [docs/reference/commands/work.md:60](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/reference/commands/work.md#L60) — `work review` is also a long-running review daemon.

### Privacy/encrypt ✅
- Source: [README.md:46](https://github.com/jumbocontext/jumbo.cli/blob/main/README.md#L46) — Jumbo states all data stays local.
- Source: [README.md:220](https://github.com/jumbocontext/jumbo.cli/blob/main/README.md#L220) — Data is stored locally in `.jumbo/`.
- Source: [docs/reference/commands/telemetry.md:54](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/reference/commands/telemetry.md#L54) — Telemetry can be disabled.

### Data export ✅
- Source: [src/presentation/cli/rendering/Renderer.ts:5](https://github.com/jumbocontext/jumbo.cli/blob/main/src/presentation/cli/rendering/Renderer.ts#L5) — CLI output supports text, JSON, YAML, and NDJSON formats.
- Source: [src/presentation/cli/commands/search/search.ts:45](https://github.com/jumbocontext/jumbo.cli/blob/main/src/presentation/cli/commands/search/search.ts#L45) — Search can emit structured JSON.

## Data Model

### Entities ✅
- Source: [README.md:107](https://github.com/jumbocontext/jumbo.cli/blob/main/README.md#L107) — Jumbo remembers project, audience, pain, value proposition, architecture, component, dependency, decision, guideline, invariant, and goal memory entities.
- Source: [README.md:122](https://github.com/jumbocontext/jumbo.cli/blob/main/README.md#L122) — Relations are the graph that ties memory entities together.
- Source: [src/domain/relations/Constants.ts:2](https://github.com/jumbocontext/jumbo.cli/blob/main/src/domain/relations/Constants.ts#L2) — Relation entity-type constants enumerate the graph node types and relation edge type.
- Source: [src/application/context/components/ComponentView.ts:3](https://github.com/jumbocontext/jumbo.cli/blob/main/src/application/context/components/ComponentView.ts#L3) — Components are structured entities with name, type, description, responsibility, path, and status.
- Source: [docs/reference/commands/relations.md:8](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/reference/commands/relations.md#L8) — Relations link goals, components, decisions, and other entities.

### Actions ✅
- Source: [src/domain/BaseEvent.ts:9](https://github.com/jumbocontext/jumbo.cli/blob/main/src/domain/BaseEvent.ts#L9) — Every stored domain event has structured `type`, `aggregateId`, `version`, `timestamp`, and payload fields.
- Source: [README.md:141](https://github.com/jumbocontext/jumbo.cli/blob/main/README.md#L141) — Every state change is stored as a domain event.

### Keywords/tags ✅
- Source: [src/application/context/search/SearchCategory.ts:1](https://github.com/jumbocontext/jumbo.cli/blob/main/src/application/context/search/SearchCategory.ts#L1) — Search documents are categorized as component, dependency, decision, guideline, or invariant.
- Source: [src/application/context/guidelines/GuidelineView.ts:10](https://github.com/jumbocontext/jumbo.cli/blob/main/src/application/context/guidelines/GuidelineView.ts#L10) — Guidelines have a structured category field.

### Anticipated queries ❌

### Trigger rules ✅
- Source: [src/presentation/cli/commands/sessions/start/SessionStartOutputBuilder.ts:12](https://github.com/jumbocontext/jumbo.cli/blob/main/src/presentation/cli/commands/sessions/start/SessionStartOutputBuilder.ts#L12) — Session start routes the agent to the appropriate workflow command before work begins.
- Source: [src/presentation/cli/commands/sessions/start/SessionStartOutputBuilder.ts:22](https://github.com/jumbocontext/jumbo.cli/blob/main/src/presentation/cli/commands/sessions/start/SessionStartOutputBuilder.ts#L22) — The execute-goal route triggers `jumbo goal start --id <goalId>`.
- Source: [README.md:151](https://github.com/jumbocontext/jumbo.cli/blob/main/README.md#L151) — Goal start conditionally assembles the context packet from memories linked to that goal through relations.
- Source: [docs/getting-started/concepts.md:125](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/getting-started/concepts.md#L125) — Project knowledge is delivered when relevant to the current goal.

### Domain tag ✅
- Source: [src/domain/guidelines/Constants.ts:17](https://github.com/jumbocontext/jumbo.cli/blob/main/src/domain/guidelines/Constants.ts#L17) — Guidelines have explicit categories: testing, coding style, process, communication, documentation, security, performance, and other.
- Source: [src/application/context/guidelines/GuidelineView.ts:10](https://github.com/jumbocontext/jumbo.cli/blob/main/src/application/context/guidelines/GuidelineView.ts#L10) — Guideline read models persist the category field.
- Source: [src/infrastructure/context/guidelines/get/SqliteGuidelineViewReader.ts:24](https://github.com/jumbocontext/jumbo.cli/blob/main/src/infrastructure/context/guidelines/get/SqliteGuidelineViewReader.ts#L24) — Guideline retrieval can filter by category.

### Task type ✅
- Source: [src/domain/goals/Constants.ts:35](https://github.com/jumbocontext/jumbo.cli/blob/main/src/domain/goals/Constants.ts#L35) — Goal status classifies work as defined, refined, doing, blocked, paused, submitted, in-review, approved, codifying, done, and related states.
- Source: [src/application/context/goals/GoalView.ts:14](https://github.com/jumbocontext/jumbo.cli/blob/main/src/application/context/goals/GoalView.ts#L14) — Goal read models persist the structured status field.
- Source: [src/application/host/workers/WorkerMode.ts:5](https://github.com/jumbocontext/jumbo.cli/blob/main/src/application/host/workers/WorkerMode.ts#L5) — Worker modes classify active agent work as plan, implement, review, or codify.

### Context (why) ✅
- Source: [src/application/context/decisions/DecisionView.ts:8](https://github.com/jumbocontext/jumbo.cli/blob/main/src/application/context/decisions/DecisionView.ts#L8) — Decisions store context, rationale, alternatives, and consequences.
- Source: [src/application/context/guidelines/GuidelineView.ts:15](https://github.com/jumbocontext/jumbo.cli/blob/main/src/application/context/guidelines/GuidelineView.ts#L15) — Guidelines store rationale and examples.

### Source attribution ❌

### Origin + trust ❌

### Emotional ❌

### Conflict surfacing ❌

### Layered memory ✅
- Source: [docs/getting-started/concepts.md:81](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/getting-started/concepts.md#L81) — Jumbo defines distinct context packet layers for session start, project north-star, and goal start.
- Source: [src/application/context/project/query/north-star/ProjectNorthStarView.ts:7](https://github.com/jumbocontext/jumbo.cli/blob/main/src/application/context/project/query/north-star/ProjectNorthStarView.ts#L7) — Project north-star is a project alignment packet combining project, audiences, audience pains, and value propositions.
- Source: [src/application/context/sessions/get/SessionContext.ts:6](https://github.com/jumbocontext/jumbo.cli/blob/main/src/application/context/sessions/get/SessionContext.ts#L6) — Session context is a separate orientation container with project context, categorized goals, and recent decisions.
- Source: [README.md:151](https://github.com/jumbocontext/jumbo.cli/blob/main/README.md#L151) — Goal-start context packets assemble relation-bound components, decisions, guidelines, invariants, and architecture.
- Source: [docs/getting-started/what-jumbo-creates.md:79](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/getting-started/what-jumbo-creates.md#L79) — Persistence is layered as append-only event source of truth plus SQLite CQRS read projection.

### Time-travel ✅
- Source: [README.md:141](https://github.com/jumbocontext/jumbo.cli/blob/main/README.md#L141) — Event sourcing stores every state change with full history and replay.
- Source: [docs/reference/commands/session.md:93](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/reference/commands/session.md#L93) — Session history can be listed and filtered by status.
- Source: [docs/reference/commands/decisions.md:134](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/reference/commands/decisions.md#L134) — Decisions can be marked superseded by newer decisions.

### Schema fields (count: 16) ✅
- Source: [src/application/context/goals/GoalView.ts:7](https://github.com/jumbocontext/jumbo.cli/blob/main/src/application/context/goals/GoalView.ts#L7) — Goal read model has objective, criteria, scope, status, note, review issues, progress, claim ownership, chained goals, branch, and worktree fields; excluding IDs, timestamps, and version gives about 16 meaningful fields.

---

## Search & Retrieval

### Full-text ✅
- Source: [docs/reference/commands/search.md:14](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/reference/commands/search.md#L14) — `jumbo search` searches indexed memory categories.
- Source: [src/infrastructure/context/search/SqliteSearchIndexStore.ts:97](https://github.com/jumbocontext/jumbo.cli/blob/main/src/infrastructure/context/search/SqliteSearchIndexStore.ts#L97) — Search uses case-normalized `LIKE` matching across title, summary, and content.

### Semantic/vector ❌

### Hybrid (BM25+Vec) ❌

### Deep (incl. thinking) ❌

### Code graph ❌

### Docs search ❌

### Fact metadata query ✅
- Source: [docs/reference/commands/search.md:27](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/reference/commands/search.md#L27) — Global search supports category filters.
- Source: [docs/reference/commands/components.md:130](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/reference/commands/components.md#L130) — Component search filters by name, type, status, and free text.
- Source: [docs/reference/commands/decisions.md:77](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/reference/commands/decisions.md#L77) — Decision search filters by status, title, and free text.

### Timeline view ❌

### Search modes (count: 6) ✅
- Source: [src/presentation/cli/commands/search/search.ts:49](https://github.com/jumbocontext/jumbo.cli/blob/main/src/presentation/cli/commands/search/search.ts#L49) — Global search links to component, decision, dependency, guideline, and invariant search commands; total modes: global search plus five typed searches.

### Data sources (count: 5) ✅
- Source: [src/application/context/search/SearchCategory.ts:1](https://github.com/jumbocontext/jumbo.cli/blob/main/src/application/context/search/SearchCategory.ts#L1) — Search data sources are components, dependencies, decisions, guidelines, and invariants.

---

## Knowledge Lifecycle

### Decay/forgetting ❌

### Supersede/replace ✅
- Source: [docs/reference/commands/decisions.md:134](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/reference/commands/decisions.md#L134) — `jumbo decision supersede` marks a decision as superseded by a newer decision.
- Source: [src/application/context/decisions/DecisionView.ts:12](https://github.com/jumbocontext/jumbo.cli/blob/main/src/application/context/decisions/DecisionView.ts#L12) — Decision read model stores `status` and `supersededBy`.

### Contradiction detection ✅
- Source: [src/presentation/cli/commands/goals/review/GoalReviewOutputBuilder.ts:115](https://github.com/jumbocontext/jumbo.cli/blob/main/src/presentation/cli/commands/goals/review/GoalReviewOutputBuilder.ts#L115) — QA review checks whether implementation conflicts with bound design decisions and records issues for rejection.
- Source: [src/presentation/cli/commands/goals/review/GoalReviewOutputBuilder.ts:127](https://github.com/jumbocontext/jumbo.cli/blob/main/src/presentation/cli/commands/goals/review/GoalReviewOutputBuilder.ts#L127) — QA review checks implementation against invariants and records non-adherence for rejection.
- Source: [src/presentation/cli/commands/goals/codify/GoalCodifyOutputBuilder.ts:73](https://github.com/jumbocontext/jumbo.cli/blob/main/src/presentation/cli/commands/goals/codify/GoalCodifyOutputBuilder.ts#L73) — Codification asks whether decisions were superseded or invalidated by the completed work.
- Source: [src/presentation/cli/commands/goals/reject/GoalRejectOutputBuilder.ts:45](https://github.com/jumbocontext/jumbo.cli/blob/main/src/presentation/cli/commands/goals/reject/GoalRejectOutputBuilder.ts#L45) — Rejection persists review issues back into the workflow for rework.

### Quarantine ✅
- Source: [src/application/context/search/SearchIndexEventHandler.ts:31](https://github.com/jumbocontext/jumbo.cli/blob/main/src/application/context/search/SearchIndexEventHandler.ts#L31) — Search-index event handling removes documents from retrieval when a projector emits a remove operation.
- Source: [src/application/context/search/projectors/DependencySearchDocumentProjector.ts:24](https://github.com/jumbocontext/jumbo.cli/blob/main/src/application/context/search/projectors/DependencySearchDocumentProjector.ts#L24) — Removed dependency events remove dependency documents from the search index.
- Source: [src/infrastructure/context/guidelines/get/SqliteGuidelineViewReader.ts:21](https://github.com/jumbocontext/jumbo.cli/blob/main/src/infrastructure/context/guidelines/get/SqliteGuidelineViewReader.ts#L21) — Guideline reads exclude removed guidelines by default.
- Source: [src/infrastructure/context/goals/remove/SqliteGoalRemovedProjector.ts:25](https://github.com/jumbocontext/jumbo.cli/blob/main/src/infrastructure/context/goals/remove/SqliteGoalRemovedProjector.ts#L25) — Removing a goal deletes it from the active goal read model.
- Source: [docs/reference/commands/goal.md:540](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/reference/commands/goal.md#L540) — Goal removal removes active tracking while preserving event history.

### Auto-resolution ✅
- Source: [src/application/context/goals/codify/CodifierProcessManager.ts:67](https://github.com/jumbocontext/jumbo.cli/blob/main/src/application/context/goals/codify/CodifierProcessManager.ts#L67) — Codifier daemon selects eligible goals for codification.
- Source: [src/application/context/goals/codify/CodifierProcessManager.ts:100](https://github.com/jumbocontext/jumbo.cli/blob/main/src/application/context/goals/codify/CodifierProcessManager.ts#L100) — The daemon invokes an agent subprocess to run codification.
- Source: [src/application/context/goals/codify/CodifierProcessManager.ts:114](https://github.com/jumbocontext/jumbo.cli/blob/main/src/application/context/goals/codify/CodifierProcessManager.ts#L114) — The daemon treats the work as complete when the goal reaches `done`.
- Source: [src/application/context/goals/codify/CodifierProcessManager.ts:166](https://github.com/jumbocontext/jumbo.cli/blob/main/src/application/context/goals/codify/CodifierProcessManager.ts#L166) — The daemon prompt instructs the agent to reconcile context and close the goal.
- Source: [src/domain/goals/Goal.ts:887](https://github.com/jumbocontext/jumbo.cli/blob/main/src/domain/goals/Goal.ts#L887) — Goal close transitions from codifying to done after codification.
- Source: [assets/skills/codify-jumbo-goal/SKILL.md:106](https://github.com/jumbocontext/jumbo.cli/blob/main/assets/skills/codify-jumbo-goal/SKILL.md#L106) — Codification rules require every entity category to be evaluated for staleness before closure.

### Trust model ❌

### Explicit forget ✅
- Source: [docs/reference/commands/goal.md:15](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/reference/commands/goal.md#L15) — Goal commands include `remove`.
- Source: [docs/reference/commands/components.md:243](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/reference/commands/components.md#L243) — Components can be marked removed.
- Source: [docs/reference/commands/guidelines.md:138](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/reference/commands/guidelines.md#L138) — Guidelines have a remove command.

---

## Extraction Pipeline

### Auto-extraction ❌

### Content-aware preprocessing ✅
- Source: [src/presentation/cli/commands/goals/codify/GoalCodifyOutputBuilder.ts:62](https://github.com/jumbocontext/jumbo.cli/blob/main/src/presentation/cli/commands/goals/codify/GoalCodifyOutputBuilder.ts#L62) — Codify output separates entity review by component, decision, invariant, guideline, dependency, and relation type.
- Source: [assets/skills/refine-jumbo-goals/SKILL.md:65](https://github.com/jumbocontext/jumbo.cli/blob/main/assets/skills/refine-jumbo-goals/SKILL.md#L65) — Refinement uses category-specific evaluation: invariants and guidelines are handled by exclusion, while components, decisions, and dependencies are handled by inclusion.
- Source: [docs/getting-started/first-run.md:72](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/getting-started/first-run.md#L72) — Brownfield capture scans documentation, code structure, and patterns as distinct input classes.

### Deduplication ✅
- Source: [src/application/context/components/add/AddComponentCommandHandler.ts:17](https://github.com/jumbocontext/jumbo.cli/blob/main/src/application/context/components/add/AddComponentCommandHandler.ts#L17) — Component add checks for an existing component with the same name.
- Source: [src/application/context/components/add/AddComponentCommandHandler.ts:24](https://github.com/jumbocontext/jumbo.cli/blob/main/src/application/context/components/add/AddComponentCommandHandler.ts#L24) — Existing components are updated instead of duplicated.
- Source: [src/application/context/relations/add/AddRelationCommandHandler.ts:11](https://github.com/jumbocontext/jumbo.cli/blob/main/src/application/context/relations/add/AddRelationCommandHandler.ts#L11) — Relation add is idempotent when an identical relation already exists.
- Source: [assets/skills/jumbo-add-decision/SKILL.md:11](https://github.com/jumbocontext/jumbo.cli/blob/main/assets/skills/jumbo-add-decision/SKILL.md#L11) — The decision-registration skill instructs agents to search for existing decisions and update/supersede rather than duplicate.

### Quality refinement ✅
- Source: [src/presentation/cli/commands/goals/review/GoalReviewOutputBuilder.ts:35](https://github.com/jumbocontext/jumbo.cli/blob/main/src/presentation/cli/commands/goals/review/GoalReviewOutputBuilder.ts#L35) — Review output assigns a QA specialist role and requires verification against implementation instructions.
- Source: [src/presentation/cli/commands/goals/review/GoalReviewOutputBuilder.ts:52](https://github.com/jumbocontext/jumbo.cli/blob/main/src/presentation/cli/commands/goals/review/GoalReviewOutputBuilder.ts#L52) — Review output instructs the agent to record issues for rejection when criteria are unmet.
- Source: [src/presentation/cli/commands/goals/codify/GoalCodifyOutputBuilder.ts:52](https://github.com/jumbocontext/jumbo.cli/blob/main/src/presentation/cli/commands/goals/codify/GoalCodifyOutputBuilder.ts#L52) — Codification filters proposed memory additions to universal, dense, actionable learnings.
- Source: [src/presentation/cli/commands/goals/codify/GoalCodifyOutputBuilder.ts:64](https://github.com/jumbocontext/jumbo.cli/blob/main/src/presentation/cli/commands/goals/codify/GoalCodifyOutputBuilder.ts#L64) — Codification reviews existing registrations for needed updates based on the work performed.

### Narrative generation ✅
- Source: [src/presentation/cli/commands/sessions/end/session.end.ts:19](https://github.com/jumbocontext/jumbo.cli/blob/main/src/presentation/cli/commands/sessions/end/session.end.ts#L19) — Session end requires a focus summary of what was accomplished.
- Source: [src/presentation/cli/commands/sessions/end/session.end.ts:25](https://github.com/jumbocontext/jumbo.cli/blob/main/src/presentation/cli/commands/sessions/end/session.end.ts#L25) — Session end accepts a detailed session summary.
- Source: [src/domain/sessions/end/SessionEndedEvent.ts:6](https://github.com/jumbocontext/jumbo.cli/blob/main/src/domain/sessions/end/SessionEndedEvent.ts#L6) — Session-ended events capture final focus and summary of work accomplished.
- Source: [docs/getting-started/concepts.md:22](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/getting-started/concepts.md#L22) — Ending a session captures what was accomplished as the project history book of record.

### Clustering ✅
- Source: [src/presentation/cli/commands/relations/add/relation.add.ts:17](https://github.com/jumbocontext/jumbo.cli/blob/main/src/presentation/cli/commands/relations/add/relation.add.ts#L17) — Relations add semantic relationships between knowledge graph entities.
- Source: [src/presentation/cli/commands/relations/add/relation.add.ts:38](https://github.com/jumbocontext/jumbo.cli/blob/main/src/presentation/cli/commands/relations/add/relation.add.ts#L38) — Relation type records the semantic relationship, such as involves, uses, or depends-on.
- Source: [src/infrastructure/context/SqliteGoalContextAssembler.ts:53](https://github.com/jumbocontext/jumbo.cli/blob/main/src/infrastructure/context/SqliteGoalContextAssembler.ts#L53) — Goal context assembly groups related entity IDs by type before fetching context.
- Source: [src/infrastructure/context/SqliteGoalContextAssembler.ts:118](https://github.com/jumbocontext/jumbo.cli/blob/main/src/infrastructure/context/SqliteGoalContextAssembler.ts#L118) — Assembled context groups related memories into components, dependencies, decisions, invariants, and guidelines.

### Recurrence detection ❌

### Persona extraction ❌

---

## Platform Support

### Claude Code ✅
- Source: [docs/reference/project-initialization.md:87](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/reference/project-initialization.md#L87) — Claude Code integration creates `.claude/settings.json` with a SessionStart hook.
- Source: [src/infrastructure/context/project/init/ClaudeConfigurer.ts:21](https://github.com/jumbocontext/jumbo.cli/blob/main/src/infrastructure/context/project/init/ClaudeConfigurer.ts#L21) — Claude configurer writes `CLAUDE.md` and Claude hooks.

### Codex ✅
- Source: [docs/reference/project-initialization.md:88](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/reference/project-initialization.md#L88) — Codex integration creates `.codex/hooks.json`.
- Source: [src/infrastructure/context/project/init/CodexConfigurer.ts:20](https://github.com/jumbocontext/jumbo.cli/blob/main/src/infrastructure/context/project/init/CodexConfigurer.ts#L20) — Codex configurer manages lifecycle hooks and skill platform.

### OpenCode ✅
- Source: [README.md:89](https://github.com/jumbocontext/jumbo.cli/blob/main/README.md#L89) — Jumbo works with any agent that supports AGENTS.md.
- Source: [OpenCode docs](https://open-code.ai/docs/en/rules) — OpenCode documents AGENTS.md project guidelines.

### Gemini CLI ✅
- Source: [docs/reference/project-initialization.md:90](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/reference/project-initialization.md#L90) — Gemini CLI integration creates `GEMINI.md` and `.gemini/settings.json`.
- Source: [src/infrastructure/context/project/init/GeminiConfigurer.ts:18](https://github.com/jumbocontext/jumbo.cli/blob/main/src/infrastructure/context/project/init/GeminiConfigurer.ts#L18) — Gemini configurer manages Gemini CLI requirements.

### Copilot ✅
- Source: [docs/reference/project-initialization.md:89](https://github.com/jumbocontext/jumbo.cli/blob/main/docs/reference/project-initialization.md#L89) — GitHub Copilot integration writes Copilot instructions.
- Source: [src/infrastructure/context/project/init/CopilotConfigurer.ts:17](https://github.com/jumbocontext/jumbo.cli/blob/main/src/infrastructure/context/project/init/CopilotConfigurer.ts#L17) — Copilot configurer manages Copilot instructions and GitHub hooks.

### Cursor ✅
- Source: [src/infrastructure/context/project/init/CursorConfigurer.ts:17](https://github.com/jumbocontext/jumbo.cli/blob/main/src/infrastructure/context/project/init/CursorConfigurer.ts#L17) — Cursor configurer is implemented.
- Source: [src/infrastructure/context/project/init/CursorConfigurer.ts:65](https://github.com/jumbocontext/jumbo.cli/blob/main/src/infrastructure/context/project/init/CursorConfigurer.ts#L65) — Cursor integration writes `.cursor/hooks.json` with a session-start hook.

### Windsurf ❌

### OpenClaw ❌

### Hermes ❌

### pi/omp ❌

### Antigravity ❌

---

## Benchmarks

### LoCoMo ❌
- Score: —

### LongMemEval ❌
- Score: —

### PersonaMem ❌
- Score: —

### Token reduction ❌
- Score: —

### Methodology open ❌
