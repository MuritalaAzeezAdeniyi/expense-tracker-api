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
| 2026-09-25 | Implement user login bounded to AT-006 and AT-007 | Added a login request schema, login endpoint, and password-verification logic using the existing PBKDF2-based hash approach while keeping registration behavior and storage unchanged. | Reviewed the scope to stay within the login acceptance criteria only and kept the fix limited to the auth route, schema, service, and focused tests. | Implemented; human-approved and committed |
| 2026-09-25 | Implement JWT-based authentication bounded to AT-008 and AT-009 | Added JWT generation on successful login and a protected endpoint dependency that validates bearer tokens, rejects missing/invalid/expired tokens, and uses the configured signing secret instead of a hardcoded production secret. | Reviewed the scope to keep it limited to authentication enforcement and token validation without adding expense or persistence features. | Implemented; human-approved and committed |
| 2026-09-28 | Implement expense creation bounded to AT-010 through AT-014 | Added an in-memory expense model, request/response validation for amount, description, category, and date, and a protected POST /expenses endpoint that stores each expense tied to the authenticated JWT user without exposing sensitive information. | Reviewed the scope to keep it limited to expense creation only and confirmed the implementation does not add retrieval, update, deletion, or persistence features beyond the in-memory store required for this task. | Implemented; human-approved and committed |
| 2026-09-28 | Implement expense retrieval bounded to AT-015 through AT-020 | Added authenticated GET /expenses and GET /expenses/{expense_id} endpoints that filter by the validated JWT user ID, return 404 for nonexistent or cross-user expenses, and preserve the existing in-memory storage and Decimal-based amount handling. | Reviewed the scope to keep it limited to expense retrieval and ownership enforcement without adding update, delete, filtering, or persistence features. | Implemented; human-approved and committed |
| 2026-09-28 | Implement expense update bounded to AT-021 and AT-022 | Added authenticated PUT /expenses/{expense_id} support for valid expense updates, enforced the same validation rules as creation, and prevented cross-user updates by checking the validated JWT user ID against the expense owner before changing data. | Reviewed the scope to keep it limited to expense update and ownership protection without adding deletion, filtering, summaries, or persistence features. | Implemented; pending human review |
| 2026-09-28 | Implement expense deletion bounded to AT-023 and AT-024 | Added authenticated DELETE /expenses/{expense_id} support for owner-only deletion, removed the expense from the in-memory store, and preserved the existing 404 behavior for nonexistent or cross-user deletion attempts so deleted expenses are not retrievable afterward. | Reviewed the scope to keep it limited to deletion and ownership enforcement without adding filtering, summaries, or persistence features. | Implemented; pending human review |
| 2026-09-28 | Implement expense category validation bounded to AT-025 and AT-026 | Added shared category validation to both ExpenseCreate and ExpenseUpdate so only the allowed categories are accepted, while invalid values continue to flow through the existing Pydantic 422 validation path without altering auth, ownership, deletion, or persistence behavior. | Reviewed the scope to keep it limited to category validation and the relevant tests without adding filtering, summaries, or new dependencies. | Implemented; pending human review |
| 2026-09-29 | Implement category filtering bounded to AT-027 | Added an optional category query parameter to GET /expenses, filtered the authenticated user's in-memory expenses by the requested category when provided, preserved the default unfiltered list otherwise, and kept ownership enforcement intact so another user's records remain hidden. | Reviewed the scope to keep it limited to AT-027 and reject any date-range, summary, or persistence changes. | Implemented; pending human review |
| 2026-09-29 | Verify filter ownership/isolation bounded to AT-029 | Added tests confirming category, date-range, and combined filters cannot expose another user's expenses because filtering is scoped to the authenticated user's ID. | Reviewed the scope to keep it limited to ownership/isolation verification without adding summary, persistence, or unrelated behavior changes. | Implemented; pending human review |
| 2026-09-29 | Implement expense summary bounded to AT-030 | Added an authenticated GET /expenses/summary endpoint that calculates the current user's total amount, expense count, and category totals while preserving ownership isolation. | Reviewed the scope to keep it limited to AT-030 without adding date/category summary filters, persistence changes, or unrelated behavior. | Implemented; pending human review |
| 2026-09-29 | Verify empty expense summary bounded to AT-032 | Added a focused test confirming that an authenticated user with no expenses receives a successful empty summary with zero total, zero count, and no category totals. | Reviewed the scope to keep it limited to AT-032 without changing existing summary behavior or adding unrelated functionality. | Implemented; pending human review |
| 2026-09-29 | Verify invalid request handling bounded to AT-033 | Added focused tests confirming invalid expense requests are rejected through the existing validation behavior without creating invalid expense records. | Reviewed the scope to keep it limited to AT-033 without introducing new requirements or unrelated validation changes. | Implemented; pending human review |
| 2026-09-29 | Verify missing authentication handling bounded to AT-034 | Added focused tests confirming protected expense and summary endpoints reject requests without authentication. | Reviewed the scope to keep it limited to AT-034 without changing authentication behavior or unrelated functionality. | Implemented; pending human review |
| 2026-09-29 | Verify not-found handling bounded to AT-035 | Added focused tests confirming nonexistent expense resources return 404 for retrieval, update, and deletion without exposing resource information or changing application state. | Reviewed the scope to keep it limited to AT-035 without changing existing resource behavior. | Implemented; pending human review |
| 2026-09-29 | Verify duplicate email handling bounded to AT-036 | Added a focused test confirming that registration rejects an email already associated with an existing user without modifying the original account. | Reviewed the scope to keep it limited to duplicate email handling without changing existing registration behavior. | Implemented; pending human review |
| 2026-09-30 | Verify unexpected error handling bounded to AT-037 | Added a focused test confirming unexpected server-side failures return an appropriate 500 response without exposing traceback, secrets, file paths, or other sensitive implementation details. | Reviewed the scope to keep it limited to AT-037 without changing normal API behavior or adding unrelated error handling. | Implemented; pending human review |
| 2026-09-30 | Verify password protection bounded to AT-038 | Added focused tests confirming plaintext passwords are not returned or stored while authenticated login continues to work with the original password. | Reviewed the scope to keep it limited to password protection without changing the existing authentication design. | Implemented; pending human review |
| 2026-09-30 | Verify no hardcoded secrets bounded to AT-039 | Added a focused security check confirming production application code does not contain hardcoded credentials or secrets and that the JWT secret remains environment-based. | Reviewed the scope to keep it limited to AT-039 without introducing a new secret-management system or unrelated security changes. | Implemented; pending human review |
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
