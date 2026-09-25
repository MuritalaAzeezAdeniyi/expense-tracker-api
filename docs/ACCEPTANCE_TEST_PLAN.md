# Expense Tracker API Acceptance Test Plan

## 1. Purpose

This document defines the acceptance criteria that will be used to verify that the Expense Tracker API satisfies the requirements defined in `docs/SPECIFICATION.md`.

A feature will only be considered complete when its relevant acceptance criteria have been satisfied and the required automated tests have passed.

---

# 2. User Registration

## AT-001 — Successful User Registration

**Given** a new user provides a valid full name, email address, and password

**When** the user submits the registration request

**Then** the system should:

* Create the user account.
* Generate a unique user ID.
* Store the user's email address.
* Store a securely hashed password.
* Return an appropriate successful response.

---

## AT-002 — Required Registration Fields

**Given** a user submits registration information with one or more required fields missing

**When** the registration request is submitted

**Then** the API should reject the request

**And** return an appropriate validation error.

---

## AT-003 — Invalid Email Address

**Given** a user provides an invalid email address

**When** the registration request is submitted

**Then** the API should reject the request

**And** return a validation error.

---

## AT-004 — Duplicate Email Address

**Given** a user account already exists with a particular email address

**When** another user attempts to register using the same email address

**Then** the API should reject the registration

**And** return an appropriate conflict response.

---

## AT-005 — Password Is Not Stored as Plain Text

**Given** a user successfully registers

**When** the user record is stored

**Then** the password must be stored as a secure hash

**And** the plain-text password must not be stored.

---

# 3. Authentication

## AT-006 — Successful Login

**Given** a registered user provides the correct email address and password

**When** the user submits the login request

**Then** the API should authenticate the user

**And** return a valid authentication token.

---

## AT-007 — Invalid Login Credentials

**Given** a registered user provides an incorrect password

**When** the login request is submitted

**Then** the API should reject the request

**And** return an appropriate authentication error.

---

## AT-008 — Unauthenticated Access

**Given** a user has not provided a valid authentication token

**When** the user attempts to access a protected expense endpoint

**Then** the API should reject the request.

---

## AT-009 — Invalid Authentication Token

**Given** a user provides an invalid or expired authentication token

**When** the user attempts to access a protected endpoint

**Then** the API should reject the request.

---

# 4. Expense Creation

## AT-010 — Successfully Create Expense

**Given** an authenticated user provides valid expense information

**When** the user submits the expense

**Then** the system should:

* Create the expense.
* Generate a unique expense ID.
* Associate the expense with the authenticated user's ID.
* Store the amount, description, category, and expense date.
* Return an appropriate successful response.

---

## AT-011 — Expense Amount Must Be Greater Than Zero

**Given** an authenticated user submits an expense with an amount less than or equal to zero

**When** the request is submitted

**Then** the API should reject the request

**And** return a validation error.

---

## AT-012 — Expense Description Is Required

**Given** an authenticated user submits an expense without a description

**When** the request is submitted

**Then** the API should reject the request

**And** return a validation error.

---

## AT-013 — Expense Category Is Required

**Given** an authenticated user submits an expense without a category

**When** the request is submitted

**Then** the API should reject the request

**And** return a validation error.

---

## AT-014 — Expense Date Is Valid

**Given** an authenticated user submits an expense

**When** the expense date contains an invalid value

**Then** the API should reject the request

**And** return a validation error.

---

# 5. Viewing Expenses

## AT-015 — View Own Expenses

**Given** an authenticated user has created expenses

**When** the user requests their expenses

**Then** the API should return their expenses

**And** should not return expenses belonging to other users.

---

## AT-016 — View Specific Own Expense

**Given** an authenticated user owns an expense

**When** the user requests the expense using its ID

**Then** the API should return the requested expense.

---

## AT-017 — Expense Does Not Exist

**Given** an authenticated user requests an expense ID that does not exist

**When** the request is submitted

**Then** the API should return an appropriate not-found response.

---

# 6. User Authorization

## AT-018 — User Cannot View Another User's Expense

**Given** User A owns an expense

**And** User B is authenticated

**When** User B attempts to retrieve User A's expense

**Then** the API should deny access to the resource.

---

## AT-019 — User Cannot Update Another User's Expense

**Given** User A owns an expense

**And** User B is authenticated

**When** User B attempts to update User A's expense

**Then** the API should deny the operation.

---

## AT-020 — User Cannot Delete Another User's Expense

**Given** User A owns an expense

**And** User B is authenticated

**When** User B attempts to delete User A's expense

**Then** the API should deny the operation.

---

# 7. Updating Expenses

## AT-021 — Successfully Update Own Expense

**Given** an authenticated user owns an expense

**When** the user submits valid updated information

**Then** the API should update the expense

**And** return the updated expense information.

---

## AT-022 — Invalid Updated Expense

**Given** an authenticated user owns an expense

**When** the user submits invalid information such as an amount less than or equal to zero

**Then** the API should reject the update

**And** return a validation error.

---

# 8. Deleting Expenses

## AT-023 — Successfully Delete Own Expense

**Given** an authenticated user owns an expense

**When** the user requests deletion

**Then** the expense should be deleted successfully.

---

## AT-024 — Deleted Expense Cannot Be Retrieved

**Given** an authenticated user has deleted an expense

**When** the user attempts to retrieve the deleted expense

**Then** the API should return a not-found response.

---

# 9. Expense Categories

## AT-025 — Create Expense With Valid Category

**Given** an authenticated user provides a valid expense category

**When** the expense is created

**Then** the expense should be stored with the specified category.

---

## AT-026 — Invalid Expense Category

**Given** an authenticated user provides an invalid category

**When** the expense is submitted

**Then** the API should reject the request

**And** return a validation error.

---

# 10. Expense Filtering

## AT-027 — Filter Expenses by Category

**Given** an authenticated user has expenses belonging to different categories

**When** the user filters expenses by a category

**Then** the API should return only the user's expenses belonging to that category.

---

## AT-028 — Filter Expenses by Date Range

**Given** an authenticated user has expenses recorded on different dates

**When** the user provides a valid date range

**Then** the API should return only expenses belonging to that user within the specified range.

---

## AT-029 — Filtering Must Respect User Ownership

**Given** multiple users have expenses matching the same filter

**When** one user applies a filter

**Then** the API should return only that user's matching expenses.

---

# 11. Expense Summary

## AT-030 — Retrieve Expense Summary

**Given** an authenticated user has recorded expenses

**When** the user requests their expense summary

**Then** the API should return:

* Total amount spent.
* Total number of expenses.
* Total amount spent per category.
* Number of expenses per category.

---

## AT-031 — Summary Must Respect User Ownership

**Given** multiple users have recorded expenses

**When** one user requests their expense summary

**Then** the summary should contain only that user's expenses.

---

## AT-032 — Summary for User With No Expenses

**Given** an authenticated user has no recorded expenses

**When** the user requests their expense summary

**Then** the API should return a valid empty summary

**And** should not return an error simply because there are no expenses.

---

# 12. Error Handling

## AT-033 — Invalid Request Data

**Given** a user submits invalid request data

**When** the API processes the request

**Then** the API should return an appropriate `400 Bad Request` response

**And** provide a meaningful validation error.

---

## AT-034 — Missing Authentication

**Given** a protected endpoint requires authentication

**When** a request is made without authentication

**Then** the API should return `401 Unauthorized`.

---

## AT-035 — Resource Not Found

**Given** a requested resource does not exist

**When** the user requests the resource

**Then** the API should return `404 Not Found`.

---

## AT-036 — Duplicate User Email

**Given** an email address is already registered

**When** another registration request uses the same email

**Then** the API should return `409 Conflict`.

---

## AT-037 — Unexpected Server Error

**Given** an unexpected internal error occurs

**When** the API processes the request

**Then** the API should return an appropriate `500 Internal Server Error`

**And** should not expose internal stack traces, database credentials, or other sensitive implementation details.

---

# 13. Security Acceptance Criteria

## AT-038 — Passwords Are Protected

The system must never return a user's password or password hash in an API response.

---

## AT-039 — Secrets Are Not Hardcoded

Application secrets, database credentials, authentication secrets, and other sensitive configuration must not be hardcoded in the source code.

---

## AT-040 — Users Cannot Access Other Users' Data

An authenticated user must not be able to view, update, delete, or include another user's expenses in their summaries or filtered results.

---

# 14. Testing and Quality Gate

A feature shall not be considered complete until:

* The relevant acceptance criteria have been satisfied.
* Automated tests have been written where appropriate.
* All relevant tests pass.
* The implementation has been reviewed.
* The Git diff has been inspected.
* Security implications have been reviewed.
* No unintended files or changes have been introduced.
* Relevant documentation has been updated.
* The human developer has approved the change.

---

# 15. Acceptance Status

Acceptance criteria will be tracked during implementation.

| ID     | Acceptance Criteria                  | Status  |
| ------ | ------------------------------------ | ------- |
| AT-001 | Successful registration              | Pending |
| AT-002 | Required registration fields         | Pending |
| AT-003 | Invalid email                        | Pending |
| AT-004 | Duplicate email                      | Pending |
| AT-005 | Password protection                  | Pending |
| AT-006 | Successful login                     | Pending |
| AT-007 | Invalid login                        | Pending |
| AT-008 | Unauthenticated access               | Pending |
| AT-009 | Invalid authentication token         | Pending |
| AT-010 | Create expense                       | Pending |
| AT-011 | Invalid expense amount               | Pending |
| AT-012 | Required description                 | Pending |
| AT-013 | Required category                    | Pending |
| AT-014 | Valid expense date                   | Pending |
| AT-015 | View own expenses                    | Pending |
| AT-016 | View specific expense                | Pending |
| AT-017 | Non-existent expense                 | Pending |
| AT-018 | Cannot view another user's expense   | Pending |
| AT-019 | Cannot update another user's expense | Pending |
| AT-020 | Cannot delete another user's expense | Pending |
| AT-021 | Update own expense                   | Pending |
| AT-022 | Invalid expense update               | Pending |
| AT-023 | Delete own expense                   | Pending |
| AT-024 | Deleted expense cannot be retrieved  | Pending |
| AT-025 | Valid expense category               | Pending |
| AT-026 | Invalid expense category             | Pending |
| AT-027 | Category filtering                   | Pending |
| AT-028 | Date-range filtering                 | Pending |
| AT-029 | Filtering respects ownership         | Pending |
| AT-030 | Expense summary                      | Pending |
| AT-031 | Summary respects ownership           | Pending |
| AT-032 | Empty expense summary                | Pending |
| AT-033 | Invalid request data                 | Pending |
| AT-034 | Missing authentication               | Pending |
| AT-035 | Resource not found                   | Pending |
| AT-036 | Duplicate email                      | Pending |
| AT-037 | Unexpected server error              | Pending |
| AT-038 | Password protection                  | Pending |
| AT-039 | Secrets not hardcoded                | Pending |
| AT-040 | User data isolation                  | Pending |
