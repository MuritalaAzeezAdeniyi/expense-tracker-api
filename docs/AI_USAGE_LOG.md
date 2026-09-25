# AI Usage Log

## Purpose

This document records significant AI-assisted activities during the development of the Expense Tracker API.

Each entry should describe what the AI agent was asked to do, what it produced, and how the human developer reviewed and approved the result.

The log must reflect actual AI usage and must not contain fabricated activities.

---

## AI-Assisted Development Log

| Date | Task | AI Assistance | Human Review / Decision | Result |
| ---- | ---- | ------------- | ----------------------- | ------ |
| 2026-09-25 | Implement user registration bounded to AT-001–AT-005 | Designed the registration endpoint, enforced required fields, email validation, duplicate checks, and password hashing in a small FastAPI implementation. | Reviewed the requirements, kept the change scoped to registration only, and validated that password hashes are never returned in API responses. | Implemented; human-approved and committed |
| 2026-09-25 | Refactor registration into separate API, schema, and service layers | Moved request/response validation into app/schemas/auth.py, transported the HTTP endpoint into app/routes/auth.py, and moved business logic into app/services/auth_service.py while preserving the same validation and hashing logic. | Human-approved architectural reason: keep HTTP concerns isolated from business logic and improve maintainability without changing the acceptance criteria or security requirements. | Implemented; human-approved and committed |
| 2026-09-25 | Cleanup registration refactor | Removed the redundant exception wrapper in the route and deleted an unused import from the schema, keeping the endpoint, validation, and hash behavior unchanged. | Reviewed the refactor for scope control and confirmed the cleanup was limited to the registration layer without altering requirements or security behavior. | Implemented; human-approved and committed |
| 2026-09-25 | Update project README documentation | Wrote a developer-facing overview of the project, current implementation status, setup instructions, API usage, testing workflow, and documentation map without changing application behavior. | Reviewed the documentation for scope and accuracy against the current codebase. Confirmed the README describes only the implemented registration scope and did not claim login, expenses, or persistence. | Implemented; pending final human approval |
| 2026-09-25 | Correct README documentation inaccuracies | Reviewed the README against the actual project structure, corrected the tree to match app/main.py, app/routes/auth.py, app/schemas/auth.py, and app/services/auth_service.py, and replaced the placeholder repository URL with the actual GitHub URL. | Confirmed the update was documentation-only and kept the wording scoped to the implemented registration feature without claiming unimplemented functionality. | Implemented; no tests run for this documentation-only correction |

---

## AI Review Process

For each significant AI-assisted implementation, record:

1. The task given to the AI agent.
2. The relevant specification and acceptance criteria.
3. The AI-generated changes or suggestions.
4. Human review of the changes.
5. Git diff inspection.
6. Tests that were run.
7. Security review.
8. Corrections or rejected suggestions.
9. Final human decision.
10. Result of the task.

---

## Example Entry Format

The following format should be used when an AI agent completes a significant task:

| Date       | Task                                 | AI Assistance                                                     | Human Review / Decision                                                                                       | Result                        |
| ---------- | ------------------------------------ | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| YYYY-MM-DD | Example: Implement user registration | AI agent implemented the bounded task according to AT-001–AT-005. | Reviewed the diff, checked validation and password security, ran tests, and corrected issues where necessary. | Approved / Revised / Rejected |

---

## Important Decisions and Rejected Suggestions

Record significant AI suggestions that were modified or rejected.

| Date | AI Suggestion / Issue | Human Decision | Reason |
| ---- | --------------------- | -------------- | ------ |
|      |                       |                |        |

---

## Notes

* Record actual AI-assisted activities only.
* Do not claim that AI performed work it did not perform.
* Record significant implementation, testing, security, and architectural assistance.
* Update this file as the project progresses.
* The human developer has final responsibility for approving changes.
