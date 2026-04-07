# AI Assistant Coding Guide

This repository is intentionally trimmed down to guidance for AI-assisted coding workflows.

## Included Files

- `AGENTS.md` for project-level rules and workflow expectations
- `skills/` for task-specific guidance files that Codex or ChatGPT can read before starting work

## Recommended Usage

Ask the assistant to:

1. Read `AGENTS.md`
2. Read the relevant file in `skills/`
3. Use a new branch and prefer a git worktree for each task
4. Keep changes minimal and focused

Current skills:

- `skills/python.md`
- `skills/langgraph.md`
- `skills/openai-llm.md`

Example prompt:

```text
Read AGENTS.md and skills/python.md, then help with my next task using a new git worktree and branch.
```
