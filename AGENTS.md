# AGENTS.md

This repository contains AI assistant coding guidance only.

## Scope

- Keep changes limited to AI guide files unless the user explicitly asks for more.
- Do not generate unnecessary code, folders, or project scaffolding.
- Prefer small documentation updates over broad rewrites.

## Git Workflow

- Use a dedicated branch for each feature, fix, or task.
- Prefer a separate git worktree for each active task.
- Default branch names to `codex/<task>` unless the user asks for a different scheme.
- Do not mix unrelated work on the same branch.

Typical flow:

```bash
git worktree add ../cassandra-ai-ops-<task> -b codex/<task>
cd ../cassandra-ai-ops-<task>
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

## Working Style

- Prefer clear, direct guidance.
- Keep instructions practical and reusable.
- Align changes with Codex and ChatGPT usage.
