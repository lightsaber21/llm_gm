# Scion Second Edition GM Prompt Design

## Goal

Create a Scion Second Edition GM prompt under `backend/prompts` for use by a RAG app or agent. The prompt should help run or assist a Storyguide using the supplied Scion jumpstart and any later retrieved source material.

## Scope

Add one prompt file: `backend/prompts/scion_second_edition_gm.md`.

Do not add app wiring, tests, prompt loaders, or eval infrastructure in this change. The prompt should be easy to augment later with more Scion books, campaign notes, pantheon material, character sheets, and session logs.

## Design

The prompt will follow the existing GM prompt pattern in `backend/prompts`:

- Start with instruction hierarchy so user/system/developer instructions remain authoritative and retrieved game text is treated only as source material.
- Define the assistant role as Scion Storyguide / GM.
- Give tone and setting anchors for modern mythic fantasy, divine community politics, Fate, Titans, heroic action, and player agency.
- Provide a compact Storypath rules capsule covering d10 pools, 8+ successes, 10-again, Difficulty, Enhancements, Complications, threshold successes, failure, Consolations, Momentum, Tension, botches, time units, Conditions, and Fields.
- Include focused procedures for the three core areas of action: procedural investigation, intrigue, and action-adventure.
- Include character and power guidance for Scions, Bands, Legend, Callings, Knacks, Boons, Relics, Guides, Followers, and Fatebindings without pretending to replace full source text.
- Keep RAG behavior explicit: prefer retrieved excerpts over the summary, cite or mention conflicts only when useful at the table, and make fair temporary rulings when source material is missing.

## Error Handling

When rules are missing or retrieved text conflicts with the prompt summary, the prompt will tell the agent to make a fair table ruling, label it as a ruling, and keep play moving. When player intent is unclear, it will ask one short clarifying question.

## Verification

Verify that the new file exists, uses the same structure as existing GM prompts, includes RAG/source-material safety language, and covers Scion-specific Storypath play loops.
