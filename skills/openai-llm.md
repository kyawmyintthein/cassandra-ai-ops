# Skill: OpenAI LLM

Use this skill for OpenAI model integration and LLM application design.

## Focus

- Use OpenAI models intentionally, with clear inputs and outputs.
- Prefer structured prompts and predictable response handling.
- Keep model usage scoped to the task instead of adding vague AI layers.
- Design for clarity, debuggability, and safe iteration.

## Expectations

- Choose models based on task needs such as reasoning, latency, and cost.
- Keep prompts concise and task-specific.
- Prefer structured outputs when the downstream workflow benefits from them.
- Make failure handling and retries explicit when needed.

## Working Rules

- Add only the OpenAI integration needed for the current task.
- Avoid overengineering prompt frameworks.
- Keep model assumptions visible in the code or guide text.
