# cassandra-ai-ops

AI-based casualty and root cause investigation agent for Cassandra and application environments.

## About

This repository describes an AI-based casualty and root cause investigation agent for Cassandra and application environments. It stays intentionally lightweight and focuses on AI assistant guidance, operating conventions, and reusable skill documents for working with Codex or ChatGPT on Cassandra-related tasks.

## Project Files

- `AGENTS.md` defines repository-level rules, git workflow, and working style.
- `skills/python.md` covers Python implementation and backend structure guidance.
- `skills/langgraph.md` covers LangGraph workflows, agents, and orchestration.
- `skills/openai-llm.md` covers OpenAI model integration, prompting, and model usage.

## Recommended Workflow

1. Read `AGENTS.md`.
2. Read the relevant file in `skills/`.
3. Use a dedicated branch for each task, preferably in a separate git worktree.
4. Keep changes minimal, practical, and task-focused.

## GitHub

- Pull requests use the template at `.github/PULL_REQUEST_TEMPLATE.md`.
- The repository is licensed under the MIT License in `LICENSE`.

## Example Prompt

```text
Read AGENTS.md and the relevant skill file, then help with my next Cassandra AI ops task using a new branch or worktree.
```
