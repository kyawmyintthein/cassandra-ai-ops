# Skill: Python

Use this skill for Python coding tasks.

## Focus

- Prefer readable, maintainable Python over clever abstractions.
- Keep modules small and responsibilities clear.
- Favor standard library solutions unless a dependency is clearly justified.
- Add only the code needed for the task.
- For backend services here, prefer a multi-module monorepo with FastAPI, YAML-driven configuration, SQLAlchemy, PostgreSQL, Alembic, and `uv`.

## Expectations

- Inspect the relevant files before editing.
- Keep naming explicit and consistent.
- Avoid premature architecture or framework-heavy patterns.
- Keep functions and classes easy to reason about.
- Ask clarifying questions before substantial implementation when key behavior or interfaces are still ambiguous.
- Explain the reasoning for framework, schema, and integration choices so the guidance stays reusable.
- Prefer OpenAPI-friendly request and response schemas with Swagger support.
- Keep business logic independent from infrastructure details such as queue backends.
- Separate modules by responsibility, such as service APIs, domain logic, persistence, queue adapters, and shared schemas or contracts.

## Working Rules

- Make the smallest useful change.
- Preserve existing style unless the user asks for a refactor.
- Do not create extra files or folders unless they are required.
- When event-driven behavior is needed, define an interface first and keep the initial PostgreSQL queue implementation replaceable by Kafka or SQS later.
- Use Alembic for schema evolution instead of ad hoc database setup notes.
- In a monorepo, prefer explicit module boundaries over cross-importing convenience helpers between domains.
