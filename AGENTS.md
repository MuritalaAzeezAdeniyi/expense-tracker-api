# Agent Instructions

## 1. Project Overview

This project is an Expense Tracker API built with Python and FastAPI.

The API allows authenticated users to create, view, update, delete, categorize, filter, and summarize their personal expenses.

The implementation must follow the requirements defined in:

* `docs/SPECIFICATION.md`
* `docs/ACCEPTANCE_TEST_PLAN.md`
* `docs/AI_WORKFLOW_POLICY.md`

---

## 2. Technology Stack

Use the technologies already defined in `requirements.txt`.

Primary technologies:

* Python
* FastAPI
* Pydantic
* Pytest
* Relational Database

Do not introduce new dependencies unless they are necessary for the task. Any new dependency must be justified and documented.

---

## 3. General Development Rules

* Read the relevant specification before making changes.
* Follow the requirements in `docs/SPECIFICATION.md`.
* Follow the acceptance criteria in `docs/ACCEPTANCE_TEST_PLAN.md`.
* Follow the AI development rules in `docs/AI_WORKFLOW_POLICY.md`.
* Do not invent new requirements.
* Do not change existing requirements without human approval.
* Keep changes focused on the assigned task.
* Do not modify unrelated files.
* Prefer simple, maintainable solutions over unnecessary complexity.

---

## 4. Repository Structure

Application code belongs under:

```text
app/
```

Automated tests belong under:

```text
tests/
```

Project documentation belongs under:

```text
docs/
```

Do not place application logic directly in the repository root unless specifically required.

---

## 5. API Development

* Follow RESTful API principles.
* Use appropriate HTTP methods and status codes.
* Use Pydantic models for request and response validation.
* Keep route handlers focused.
* Move business logic into appropriate service components when necessary.
* Return clear and meaningful API responses.
* Do not expose internal implementation details in API responses.

---

## 6. Authentication and Authorization

Security is a core requirement of this project.

* Protected endpoints must require valid authentication.
* Identify users through the authenticated identity.
* Do not trust a client-supplied `user_id` for authorization.
* Verify ownership before allowing users to view, update, or delete expenses.
* Users must never access another user's expenses.
* Passwords must never be stored in plaintext.
* Password hashes must never be returned in API responses.
* Never hardcode passwords, API keys, tokens, or other secrets.
* Use environment variables for sensitive configuration.
* Never commit `.env` files or secrets to Git.

---

## 7. Validation and Error Handling

Validate user input at the API boundary.

Examples include:

* Invalid email addresses
* Missing required fields
* Invalid passwords
* Duplicate email addresses
* Expense amounts less than or equal to zero
* Invalid categories
* Invalid dates
* Invalid authentication tokens

Use appropriate HTTP status codes and meaningful error messages.

Do not expose stack traces, passwords, tokens, database credentials, or other sensitive implementation details to API clients.

---

## 8. Testing Requirements

Every significant feature should have automated tests.

Tests should cover, where applicable:

* Successful operations
* Input validation
* Authentication
* Authorization
* Error handling
* Resource ownership
* Security-related behavior

Before considering a task complete:

1. Run the relevant tests.
2. Run the complete test suite when appropriate.
3. Investigate and fix failures.
4. Report the test results.

Do not claim that tests pass without actually running them.

---

## 9. AI Implementation Rules

AI coding agents must work on bounded and clearly defined tasks.

Before implementing a task:

1. Read the relevant specification.
2. Identify the exact acceptance criteria involved.
3. Understand the existing project structure.
4. Determine the smallest reasonable change required.
5. Avoid modifying unrelated functionality.

During implementation:

* Follow the existing architecture.
* Do not silently change requirements.
* Do not add unnecessary features.
* Do not rewrite unrelated code.
* Do not introduce dependencies without justification.

After implementation:

1. Review the changed files.
2. Inspect the Git diff.
3. Run relevant tests.
4. Review security implications.
5. Check for unintended changes.
6. Report assumptions or limitations.
7. Wait for human review and approval before considering the change complete.

---

## 10. Human Review and Approval

AI-generated code is not automatically considered correct.

A human developer must review:

* Correctness
* Code quality
* Security
* Tests
* API behavior
* Acceptance criteria
* Git diff
* Unintended changes

The human developer has final responsibility for approving or rejecting AI-generated changes.

---

## 11. Git Practices

Keep commits focused and meaningful.

Use descriptive commit messages such as:

```text
feat: implement user registration
test: add registration acceptance tests
fix: prevent cross-user expense access
docs: update AI usage log
```

Do not commit:

* `.venv/`
* `.env`
* secrets
* generated temporary files
* unrelated changes

Review the Git diff before committing changes.

---

## 12. Documentation and Traceability

Important AI-assisted activities must be recorded in:

```text
docs/AI_USAGE_LOG.md
```

The log should record:

* Task performed
* AI assistance used
* Human review
* Decisions made
* Corrections or rejected suggestions
* Final result

Documentation should be updated when a significant implementation or design decision changes.

---

## 13. Scope Control

The AI agent must not independently:

* Redefine project requirements
* Remove acceptance criteria
* Disable security controls
* Introduce unrelated features
* Modify unrelated parts of the application
* Mark a task as complete without testing
* Claim that unverified behavior works

If a requirement is unclear or a change could significantly affect the architecture, stop and request human clarification.

---

## 14. Definition of Done

A task is considered complete only when:

* The implementation satisfies the relevant specification.
* Relevant acceptance criteria are satisfied.
* Appropriate automated tests exist.
* Tests have been executed successfully.
* The implementation has been reviewed.
* The Git diff has been inspected.
* Security implications have been reviewed.
* No unintended changes are present.
* Relevant documentation has been updated.
* A human developer has approved the change.
* The changes are committed to Git.
