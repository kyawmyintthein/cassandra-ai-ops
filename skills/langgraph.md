# Skill: LangGraph

Use this skill for LangGraph-based agent or workflow design.

## Focus

- Model flows as clear graph steps with explicit state.
- Keep node responsibilities narrow and observable.
- Prefer simple orchestration over deeply nested agent behavior.
- Make control flow easy to debug.

## Expectations

- Define state shape clearly.
- Keep transitions intentional and easy to follow.
- Separate tool execution, reasoning, and output formatting when possible.
- Avoid unnecessary complexity in graph topology.

## Working Rules

- Add only the graph structure needed for the task.
- Prefer deterministic behavior where possible.
- Keep prompts, tools, and state boundaries explicit.
