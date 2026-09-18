---
title: "ADR-0001: Orchestrated Workflow with RAG and Validators"
status: "Proposed"
date: "2026-09-17"
authors: "Project owner"
tags: ["architecture", "decision", "agentic-ai", "rag", "rules-engine", "vampire-the-masquerade-v5"]
supersedes: ""
superseded_by: ""
---

# ADR-0001: Orchestrated Workflow with RAG and Validators

## Status

**Proposed** | Accepted | Rejected | Superseded | Deprecated

## Context

This personal project will provide an AI Storyteller and, after the MVP, optional autonomous AI companion players for *Vampire: The Masquerade Fifth Edition* (V5). The MVP will target duet play: exactly one human-controlled player character using a web application with an AI Storyteller. The Storyteller may create and control NPCs, but the MVP will not generate AI companion player characters. Later releases may support multiple human players and AI companions.

The system has three separate workflows:

- **CTX-001**: MVP character creation accepts and validates one human player's full V5 character schema for mechanical legality and lore accuracy. Post-MVP character creation may generate compatible, mechanically legal, lore-accurate AI companion characters.
- **CTX-002**: Premise generation combines a player's requested story direction with character sheets. The premise remains hidden, broad, and adaptable during play without uncontrolled deviation.
- **CTX-003**: Game execution generates narration, addresses explicit participants, requests decisions or dice rolls without necessarily advancing the scene, performs NPC actions, and updates campaign state.

Users upload rule and lore sources. Documents and embeddings remain local. Users label source edition and choose source priority. Retrieved excerpts may be sent to a remote model API, creating an explicit privacy boundary. Source citations are exposed only during disputes.

Mechanics should be enforced wherever practical. All player and NPC dice are rolled by software and remain auditable, including pools, modifiers, individual dice, Hunger dice, successes, and outcomes. The application must track complete relevant state, including attributes, skills, disciplines, health, Willpower, Hunger, Humanity, stains, conditions, inventory, relationships, location, and scene time.

The architecture must support older tool-capable OpenAI models such as GPT-4o while providing model abstraction from the start. No current latency or cost target exists. Campaign data remains local.

## Decision

Use one deterministic orchestrator to run three separate workflows: character creation, premise generation, and gameplay. Each workflow may call specialized LLM generators, local retrieval, deterministic validators, and a bounded LLM critic. These components are roles within controlled workflows, not independent conversational agents.

- **DEC-001**: Use local RAG as a shared tool for generators and critics. Retrieval does not independently control workflow execution.
- **DEC-002**: Give an encoded deterministic V5 rules engine authority over mechanics. Prioritized retrieved sources govern lore and rules not yet encoded. Human decisions override generated content.
- **DEC-003**: Require typed structured outputs for character sheets, narration envelopes, dice requests, NPC actions, citations, and proposed state changes.
- **DEC-004**: Let the game master propose state changes. Validate and apply them through the rules engine. Structured canonical state overrides contradictory prose.
- **DEC-005**: Maintain an append-only event log, structured current state, and rolling narrative summaries. Do not treat dialogue history as the sole memory system.
- **DEC-006**: Use bounded generate-review-repair cycles. Permit at most three LLM repair attempts by default. After the cap, deterministically repair invalid fields and return the best valid draft.
- **DEC-007**: Use deterministic schema and mechanics validation before LLM criticism. Restrict the critic to lore consistency, narrative fit, party diversity, character compatibility, and premise adherence.
- **DEC-008**: Model MVP targets explicitly with `player:<id>`, `table`, `system`, and `none` instead of relying only on free-form prose. Reserve `companion:<id>` for post-MVP expansion.
- **DEC-009**: Exclude AI companion player characters from the MVP. In a later release, companions may act autonomously using only information available to the human player and must require human approval for major plot choices.
- **DEC-010**: Keep premise guidance flexible. Permit emergent story development while checking generated actions against premise constraints and recorded campaign facts.
- **DEC-011**: Abstract model invocation, tool calling, structured-output parsing, retries, and capability checks behind a provider-neutral interface.
- **DEC-012**: Keep uploaded documents, embeddings, campaign state, and event logs local. Send only retrieved excerpts and required interaction context to the configured model provider.

## Consequences

### Positive

- **POS-001**: Deterministic validation makes mechanical outcomes reproducible, auditable, and testable.
- **POS-002**: Shared retrieval improves lore grounding without making an opaque autonomous retrieval agent responsible for application control.
- **POS-003**: Typed state and event history prevent prose contradictions from silently corrupting campaign state.
- **POS-004**: Separate workflows isolate prompts, tools, schemas, tests, and failure handling for each phase.
- **POS-005**: Bounded repair prevents unbounded writer-editor loops and controls latency and model cost.
- **POS-006**: Provider abstraction permits model replacement as tool-calling and structured-output support evolves.
- **POS-007**: Excluding AI companions from the MVP reduces turn-routing, autonomy, party-composition, and player-agency complexity while retaining a future expansion path.

### Negative

- **NEG-001**: Building and maintaining a useful V5 rules engine requires substantial domain modeling and test coverage.
- **NEG-002**: Full V5 schemas, canonical state, event logs, summaries, and source precedence create more implementation work than a chat-only prototype.
- **NEG-003**: Rules not encoded in the engine still depend on retrieval quality and LLM interpretation.
- **NEG-004**: Sending retrieved excerpts to a remote model means uploaded content is not fully local during inference.
- **NEG-005**: Older models may fail structured outputs or tool calls, requiring strict parsing, retries, and capability-specific fallbacks.
- **NEG-006**: The MVP cannot validate AI companion generation, autonomy, party composition, or companion-specific turn routing.
- **NEG-007**: No initial latency or cost budget makes performance acceptance criteria incomplete.

## Alternatives Considered

### Independent Writer and Editor Agents

- **ALT-001**: **Description**: A writer produces each artifact, then an editor with RAG repeatedly reviews and returns revisions, with a maximum of five iterations.
- **ALT-002**: **Rejection Reason**: Two unconstrained LLM agents duplicate context, increase cost and latency, may disagree without convergence, and cannot reliably enforce deterministic mechanics.

### Agentic RAG Subagent

- **ALT-003**: **Description**: An autonomous retrieval agent plans searches, evaluates sources, and supplies or validates answers for each generation phase.
- **ALT-004**: **Rejection Reason**: Agentic retrieval adds control complexity before retrieval needs justify it. Direct orchestrated retrieval is easier to observe, test, and constrain. Agentic retrieval may be added later for multi-hop disputes.

### Single Monolithic Game-Master Prompt

- **ALT-005**: **Description**: One LLM prompt performs generation, rules interpretation, dice resolution, state tracking, and narration from conversation history.
- **ALT-006**: **Rejection Reason**: Prose-only memory and implicit state make mechanical enforcement, auditing, recovery, testing, and long-running consistency unreliable.

### Fully Deterministic Game Engine

- **ALT-007**: **Description**: Encode mechanics, narrative transitions, characters, and story behavior without LLM generation.
- **ALT-008**: **Rejection Reason**: Deterministic software suits rules resolution but cannot economically provide the open-ended narration and improvisation required from an AI game master.

## Implementation Notes

- **IMP-001**: Define versioned schemas first: V5 character sheet, campaign state, event, roll request, roll result, NPC action, narration envelope, state patch, source reference, validation report, and premise constraints.
- **IMP-002**: Build the first vertical slice around duet play: one human-created and human-controlled character, one AI Storyteller, Storyteller-controlled NPCs, premise generation, one scene, software dice rolling, validated state updates, persistence, and reload. Do not include AI companion player characters.
- **IMP-003**: Resolve every roll in deterministic application code. Record random seed or equivalent replay metadata, pool construction, modifiers, die faces, Hunger dice, successes, criticals, messy criticals, bestial failures, and final outcome.
- **IMP-004**: Establish authority order: human correction, deterministic rules engine for encoded mechanics, user-configured source priority for retrieved material, canonical structured state, then LLM output.
- **IMP-005**: Validate all state patches against schema, invariants, permissions, and rules before committing them. Never let narration mutate canonical state directly.
- **IMP-006**: Support scene responses that request a roll or decision without advancing scene time or applying premature consequences.
- **IMP-007**: Store uploaded source identity, edition, user priority, chunk provenance, and page or section metadata. Return citations on dispute requests.
- **IMP-008**: After the MVP, give companion actions an impact classification and require human confirmation when an action crosses the major-plot-choice threshold.
- **IMP-009**: Add provider capability checks for tool calling, schema-constrained output, context size, and retry behavior. Keep provider-specific payloads outside domain workflows.
- **IMP-010**: Test rules with deterministic unit cases, schemas with contract tests, retrieval with known-answer evaluations, and full workflows with replayable scenarios.
- **IMP-011**: Measure invalid-output rate, deterministic repair rate, rules disagreement rate, retrieval citation accuracy, state contradiction rate, turn latency, token use, and major-choice approval compliance.
- **IMP-012**: Defer all AI companion generation and behavior, party-diversity evaluation, companion targeting, multi-human play, automated safety controls, and autonomous multi-hop retrieval until the duet vertical slice proves state and rules correctness.

## References

- **REF-001**: User-uploaded *Vampire: The Masquerade Fifth Edition* rule and lore sources; edition and precedence are user configured.
- **REF-002**: Future ADRs should define canonical schemas, rules-engine coverage, retrieval pipeline, state persistence, and model-provider interface.
- **REF-003**: This decision records requirements established through the project-owner architecture interview on 2026-09-17.
