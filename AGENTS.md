# AGENTS.md

This repository contains AI assistant coding guidance only.

## Scope

- Keep changes limited to AI guide files unless the user explicitly asks for more.
- Do not generate unnecessary code, folders, or project scaffolding.
- Prefer small documentation updates over broad rewrites.

## Collaboration Defaults

- Ask clarifying questions before taking substantial actions when requirements, scope, or architecture choices are still open.
- Explain the reasoning behind important implementation choices before or alongside the proposed change.
- Follow `AGENTS.md` first, then the relevant skill file, then the user request.

## Git Workflow

- Use a dedicated branch for each feature, fix, or task.
- Prefer a separate git worktree for each active task.
- Create a shared `.worktree` folder under the projects root and keep task worktrees there.
- Default branch names to `codex/<task>` unless the user asks for a different scheme.
- Do not mix unrelated work on the same branch.

Typical flow:

```bash
mkdir -p ../.worktree
git worktree add ../.worktree/cassandra-ai-ops-<task> -b codex/<task>
cd ../.worktree/cassandra-ai-ops-<task>
```

## Skill Usage

When starting work:

1. Read `AGENTS.md`.
2. Read the relevant file in `skills/`.
3. Keep the change minimal and task-focused.

Use these skills:

- `skills/python.md` for Python implementation and backend structure
- `skills/langgraph.md` for LangGraph workflows, agents, and orchestration
- `skills/openai-llm.md` for OpenAI LLM integration, prompting, and model usage

## Backend Defaults

For Python backend services in this repository, prefer:

- a multi-module monorepo structure with clear module boundaries
- `uv` for environment and dependency management
- `FastAPI` for HTTP APIs
- YAML-driven configuration
- `SQLAlchemy` with PostgreSQL for persistence
- `Alembic` for schema migrations
- OpenAPI and Swagger for API documentation
- event-driven integration with a PostgreSQL-backed queue for `v1`, behind an abstraction that can later support Kafka or SQS

Model backend modules so domain logic, APIs, queue adapters, and shared contracts can evolve independently without collapsing into one service package.

## Working Style

- Prefer clear, direct guidance.
- Keep instructions practical and reusable.
- Align changes with Codex and ChatGPT usage.
