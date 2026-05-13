# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**RunStats2** is a Flask REST API (Python 3.8+) backed by SQLAlchemy with JWT authentication. No application code exists yet — the repository is in the specification/planning stage using [Spec Kit](https://github.com/speckit).

## Planned Stack

| Layer | Technology |
|---|---|
| Web framework | Flask |
| ORM | SQLAlchemy |
| Authentication | JWT |
| Testing | pytest |
| Containerization | Docker |

When writing code, follow the planned directory layout from `.specify/templates/plan-template.md`:

```
src/
├── models/
├── services/
└── api/
tests/
├── contract/
├── integration/
└── unit/
```

## Development Workflow (Spec Kit / SDD)

This project uses **Spec Kit** for specification-driven development. The standard cycle is:

```
specify → clarify → plan → tasks → implement → checklist
```

Spec Kit scripts live in `.specify/scripts/bash/`. Feature branches and spec directories are created together:

```bash
# Create a feature branch + spec scaffold
bash .specify/scripts/bash/create-new-feature.sh "Feature description"
```

Feature branches follow sequential numbering: `001-feature-name`, `002-feature-name`, etc. Each feature's documentation lives under `specs/<branch-name>/` (spec.md, plan.md, tasks.md, etc.).

The git extension auto-commits at each workflow stage (configurable in `.specify/extensions/git/git-config.yml`).

## Constitution (Non-Negotiable Rules)

The project constitution is at `.specify/memory/constitution.md`. Key mandates:

- **TDD is mandatory**: tests must be written and must fail *before* implementation
- **Test coverage ≥ 80%**
- **All inputs validated** via Marshmallow or Pydantic; no unvalidated data persists
- **All API endpoints** must be RESTful with appropriate HTTP methods and status codes
- **SQLAlchemy for all DB access**; schema changes require migrations
- **JWT for authentication**; HTTPS enforced; inputs sanitized against injection

## Running Tests

```bash
pytest                          # all tests
pytest tests/unit/              # unit tests only
pytest tests/integration/       # integration tests only
pytest -k "test_name"           # single test by name
pytest --cov=src --cov-report=term-missing   # with coverage
```

## Spec Kit Agent Prompts

The `.github/prompts/` directory contains the AI agent prompt files that drive each speckit command. The `.github/agents/` directory contains agent configuration files. These are inputs to the speckit toolchain — do not treat them as runnable scripts.
