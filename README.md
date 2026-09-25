# Expense Tracker API

An AI-native expense tracking API built with Python and FastAPI. The project is being developed using a bounded, human-reviewed workflow that keeps scope controlled and security-focused while the core registration flow is implemented.

## Overview

This repository provides a backend API for tracking personal expenses. The current implementation is intentionally limited to the user registration flow required by the project specification and acceptance tests. The application is designed to support future authentication, expense management, category validation, filtering, and summaries, but those features are still planned work and are not yet implemented.

This project follows an AI-assisted engineering workflow with human review and approval at key checkpoints, as defined in `AGENTS.md` and `docs/AI_WORKFLOW_POLICY.md`.

## Current Status

### Implemented

- User registration endpoint (`POST /register`)
- Required field validation
- Email format validation
- Duplicate email rejection
- Password strength validation
- Password hashing before storage
- Password/hash protection in API responses
- UUID-based user identifiers
- Automated registration tests covering AT-001 through AT-005

### Planned / specified but not yet implemented

- Login and authentication
- JWT or token-based auth
- Expense creation, retrieval, updating, and deletion
- Expense categories
- Expense filtering
- Expense summaries
- Database persistence
- User authorization beyond registration scope

## Technology Stack

The repository currently uses the following technologies:

- Python
- FastAPI
- Pydantic
- Pytest
- HTTPX/TestClient
- Uvicorn
- email-validator

## Project Structure

```text
app/
├── main.py
├── routes/
│   └── auth.py
├── schemas/
│   └── auth.py
└── services/
    └── auth_service.py

tests/
docs/
AGENTS.md
README.md
requirements.txt
```

### Key files and responsibilities

- `app/main.py`: application bootstrap, FastAPI instance, router registration, and health check endpoint.
- `app/routes/auth.py`: HTTP route layer for the registration endpoint.
- `app/schemas/auth.py`: request and response validation models for registration.
- `app/services/auth_service.py`: user registration business logic, including duplicate checks and password hashing.
- `tests/test_registration.py`: automated tests for the currently implemented registration acceptance criteria.
- `docs/`: project specifications, acceptance criteria, AI workflow guidance, and activity log.
- `requirements.txt`: Python dependencies for the current project.

## Setup

Clone the repository and create a virtual environment in PowerShell:

```powershell
git clone https://github.com/MuritalaAzeezAdeniyi/expense-tracker-api.git
cd expense-tracker-api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Running the API

Start the FastAPI application with Uvicorn:

```powershell
uvicorn app.main:app --reload
```

The app exposes the health endpoint:

```http
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

The currently implemented registration endpoint is:

```http
POST /register
```

Example request body:

```json
{
  "full_name": "Alice Example",
  "email": "alice@example.com",
  "password": "StrongPass1!"
}
```

Example response:

```json
{
  "id": "<uuid>",
  "full_name": "Alice Example",
  "email": "alice@example.com",
  "created_at": "2026-09-25T12:00:00+00:00",
  "updated_at": "2026-09-25T12:00:00+00:00"
}
```

The response does not include a password or password hash.

## Running Tests

Run the current test suite with:

```powershell
.\.venv\Scripts\python -m pytest -q
```

The registration suite currently covers AT-001 through AT-005.

## Development Workflow

This repository follows a bounded, AI-assisted workflow:

```text
Specification
→ Acceptance Criteria
→ Bounded AI Task
→ AI Implementation
→ Human Review
→ Tests
→ Security Review
→ Diff Review
→ Human Approval
→ Commit
```

This workflow is reinforced by the guidance in `AGENTS.md` and `docs/AI_WORKFLOW_POLICY.md`.

## Documentation

The project documentation is organized as follows:

- `docs/SPECIFICATION.md`: product and technical requirements for the Expense Tracker API.
- `docs/ACCEPTANCE_TEST_PLAN.md`: acceptance criteria and expected behaviors used to validate the implementation.
- `docs/AI_WORKFLOW_POLICY.md`: rules and checkpoints for AI-assisted development, review, testing, and approval.
- `docs/AI_USAGE_LOG.md`: records of actual AI-assisted activities, decisions, and review outcomes.

## Known Limitation

User storage is currently in-memory and therefore not persistent across application restarts.

This repository does not yet implement database persistence or long-term storage for users or expenses.

## Notes for Contributors

- Keep changes scoped to the task being worked on.
- Validate requirements against the specification and acceptance tests before editing code.
- Review security implications for authentication, user ownership, and password handling.
- Do not claim functionality that is not present in the current codebase.
