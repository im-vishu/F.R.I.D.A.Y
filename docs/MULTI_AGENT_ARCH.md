# F.R.I.D.A.Y Multi-Agent Orchestration

- Agents run in isolation, communicate over event bus using standard message schema.
- NLU processes transcripts, extracts intent/entities, hands off to planner.
- Planner decomposes and routes tasks to skills.
- Skills execute atomic actions, return results (to origin or orchestrator).
- Flexible: Add new skills/agents by registering a [name, handler] and announcing via event.