# AI Workflow Policy

## 1. Purpose

This policy defines how AI tools and coding agents are used during the development of the Expense Tracker API.

AI is treated as an engineering collaborator that can assist with planning, implementation, testing, documentation, and code review.

Human developers retain final responsibility for requirements, architecture, security, testing, and approval of all changes.

---

## 2. Core Principles

The project follows these principles:

1. Human-defined requirements
2. AI-assisted development
3. Bounded AI tasks
4. Human review and approval
5. Automated testing
6. Security review
7. Git-based traceability
8. Documented AI usage
9. No unapproved requirement changes

---

## 3. Requirements and Specification

Project requirements must be defined and approved by a human before implementation.

The primary requirements are documented in:

```text
docs/SPECIFICATION.md
```

Acceptance criteria are documented in:

```text
docs/ACCEPTANCE_TEST_PLAN.md
```

AI may help clarify, organize, or improve requirements, but it must not independently redefine the project's requirements.

Any significant requirement change must receive human approval before implementation.

---

## 4. AI Planning

AI may be used to:

* Analyze requirements
* Break features into smaller tasks
* Suggest implementation approaches
* Identify potential edge cases
* Suggest testing strategies
* Identify potential security concerns

For significant changes, the proposed approach should be reviewed by the human developer before implementation begins.

---

## 5. Bounded AI Implementation

AI coding agents should receive clearly defined and limited tasks.

Examples include:

* Implement user registration
* Add login authentication
* Create an expense endpoint
* Add validation for expense amounts
* Write tests for a specific acceptance criterion
* Fix a specific failing test

AI should not be instructed to independently build the entire application without review checkpoints.

Each task should have:

* Clear scope
* Relevant acceptance criteria
* Expected files or components
* Testing requirements
* A defined completion condition

---

## 6. Human Code Review

All AI-generated code must be reviewed by a human before being considered complete.

The review should check:

* Correctness
* Compliance with the specification
* Code quality
* Maintainability
* Security
* Error handling
* Test coverage
* API behavior
* Unintended changes

The human developer must inspect the Git diff to understand exactly what changed.

---

## 7. Testing

AI may assist with generating automated tests.

However, generated tests must be reviewed to ensure that they correctly test the intended behavior.

For significant changes:

1. Relevant tests must be written.
2. Tests must be executed.
3. Failures must be investigated.
4. The complete test suite should be run when appropriate.
5. Results must be reviewed by the human developer.

AI must not claim that tests pass without actually running them.

---

## 8. Security Review

Security must be considered for every feature that handles authentication, authorization, user data, or sensitive information.

The review should consider:

* Authentication
* Authorization
* User ownership
* Password protection
* Input validation
* Secrets management
* Environment variables
* Sensitive information in responses
* Error messages
* Dependency risks
* Cross-user data access

AI suggestions involving security must be reviewed by the human developer before acceptance.

---

## 9. Git and Change Traceability

Development should use Git to maintain a clear history of changes.

Changes should be:

* Small
* Focused
* Related to a specific task
* Described with meaningful commit messages

The Git diff should be reviewed before committing AI-assisted changes.

Example commit messages:

```text
feat: implement user registration
test: add registration acceptance tests
fix: validate expense ownership
docs: update AI usage log
```

---

## 10. AI Usage Logging

Significant AI-assisted activities must be recorded in:

```text
docs/AI_USAGE_LOG.md
```

The log should capture:

* Date
* Task
* AI assistance used
* Human review
* Decisions made
* Changes requested or rejected
* Final result

The purpose of the log is to provide traceability between AI assistance, human decisions, and the resulting implementation.

---

## 11. Human Approval Gate

An AI-generated change must pass the following approval process:

```text
Requirement
     ↓
Acceptance Criteria
     ↓
AI Planning
     ↓
Human Review
     ↓
Bounded AI Implementation
     ↓
Git Diff Inspection
     ↓
Automated Tests
     ↓
Security Review
     ↓
Human Approval
     ↓
Git Commit
```

A change must not be considered complete until it passes the human approval gate.

---

## 12. Handling AI Errors

AI-generated code may contain incorrect assumptions, bugs, security weaknesses, or unnecessary complexity.

When an AI-generated change is incorrect:

1. Identify the problem.
2. Reject or modify the proposed solution.
3. Record significant decisions in the AI usage log when appropriate.
4. Request a corrected implementation if needed.
5. Re-run tests.
6. Review the updated diff.
7. Approve only after the change satisfies the requirements.

AI output must be treated as a proposal rather than unquestioned authority.

---

## 13. Scope and Change Control

AI must not:

* Change project requirements without approval
* Remove acceptance criteria
* Disable security controls to make tests pass
* Introduce unrelated features
* Modify unrelated files
* Add unnecessary dependencies
* Hardcode secrets
* Commit sensitive information
* Skip required tests
* Mark unverified work as complete

If an implementation requires a significant architectural or requirement change, human approval is required first.

---

## 14. Final Responsibility

AI assists with engineering work, but the human developer remains responsible for the final result.

The human developer is responsible for approving:

* Requirements
* Architecture
* Implementation
* Tests
* Security
* Documentation
* Git changes
* Final release

The use of AI does not transfer engineering responsibility from the human developer to the AI system.
