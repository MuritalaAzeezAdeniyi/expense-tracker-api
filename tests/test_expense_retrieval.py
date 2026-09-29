import os

import pytest
from fastapi.testclient import TestClient

from app.main import app


os.environ["JWT_SECRET_KEY"] = "32-character-secret-key-for-testing-123"

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    app.state.users.clear()
    app.state.expenses.clear()
    yield
    app.state.users.clear()
    app.state.expenses.clear()


def _register_and_login(email: str, full_name: str = "Expense User") -> str:
    client.post(
        "/register",
        json={
            "full_name": full_name,
            "email": email,
            "password": "StrongPass1!",
        },
    )
    login_response = client.post(
        "/login",
        json={
            "email": email,
            "password": "StrongPass1!",
        },
    )
    return login_response.json()["token"]


def test_get_expenses_returns_only_current_users_expenses():
    user_a_token = _register_and_login("usera@example.com", "User A")
    user_b_token = _register_and_login("userb@example.com", "User B")

    expense_a = client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {user_a_token}"},
        json={
            "amount": "12.50",
            "description": "Coffee",
            "category": "Food",
            "expense_date": "2026-09-28",
        },
    )
    assert expense_a.status_code == 201

    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {user_b_token}"},
        json={
            "amount": "99.00",
            "description": "Train ticket",
            "category": "Transportation",
            "expense_date": "2026-09-28",
        },
    )

    response = client.get(
        "/expenses",
        headers={"Authorization": f"Bearer {user_a_token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["description"] == "Coffee"
    assert body[0]["user_id"]


def test_get_expense_by_id_returns_owned_expense():
    token = _register_and_login("owner@example.com", "Owner")
    create_response = client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "25.00",
            "description": "Lunch",
            "category": "Food",
            "expense_date": "2026-09-28",
        },
    )
    expense_id = create_response.json()["id"]

    response = client.get(
        f"/expenses/{expense_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == expense_id
    assert response.json()["description"] == "Lunch"


def test_get_expense_by_id_returns_404_when_expense_does_not_exist():
    token = _register_and_login("missing@example.com", "Missing")

    response = client.get(
        "/expenses/does-not-exist",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found."


def test_get_expense_by_id_returns_404_for_another_users_expense():
    user_a_token = _register_and_login("usera@example.com", "User A")
    user_b_token = _register_and_login("userb@example.com", "User B")

    create_response = client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {user_a_token}"},
        json={
            "amount": "41.50",
            "description": "Hotel",
            "category": "Housing",
            "expense_date": "2026-09-28",
        },
    )
    expense_id = create_response.json()["id"]

    response = client.get(
        f"/expenses/{expense_id}",
        headers={"Authorization": f"Bearer {user_b_token}"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found."


def test_get_expenses_filters_by_valid_category():
    token = _register_and_login("filter@example.com", "Filter User")

    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "12.50",
            "description": "Coffee",
            "category": "Food",
            "expense_date": "2026-09-28",
        },
    )
    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "22.00",
            "description": "Train ticket",
            "category": "Transportation",
            "expense_date": "2026-09-28",
        },
    )

    response = client.get(
        "/expenses?category=Food",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["category"] == "Food"
    assert response.json()[0]["description"] == "Coffee"


def test_get_expenses_excludes_other_categories_when_filtered():
    token = _register_and_login("category-filter@example.com", "Category Filter")

    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "9.00",
            "description": "Lunch",
            "category": "Food",
            "expense_date": "2026-09-28",
        },
    )
    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "30.00",
            "description": "Rent",
            "category": "Housing",
            "expense_date": "2026-09-28",
        },
    )

    response = client.get(
        "/expenses?category=Housing",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["category"] == "Housing"
    assert response.json()[0]["description"] == "Rent"


def test_get_expenses_rejects_cross_user_access_when_filtered():
    user_a_token = _register_and_login("usera@example.com", "User A")
    user_b_token = _register_and_login("userb@example.com", "User B")

    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {user_a_token}"},
        json={
            "amount": "10.00",
            "description": "Taxi",
            "category": "Transportation",
            "expense_date": "2026-09-28",
        },
    )

    response = client.get(
        "/expenses?category=Transportation",
        headers={"Authorization": f"Bearer {user_b_token}"},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_get_expenses_rejects_invalid_category_filter():
    token = _register_and_login("invalid-filter@example.com", "Invalid Filter")

    response = client.get(
        "/expenses?category=Travel",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422


def test_get_expenses_filters_by_start_date():
    token = _register_and_login("start-date@example.com", "Start Date")

    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "10.00",
            "description": "Day 1",
            "category": "Food",
            "expense_date": "2026-09-01",
        },
    )
    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "15.00",
            "description": "Day 10",
            "category": "Food",
            "expense_date": "2026-09-10",
        },
    )
    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "20.00",
            "description": "Day 20",
            "category": "Food",
            "expense_date": "2026-09-20",
        },
    )

    response = client.get(
        "/expenses?start_date=2026-09-10",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert [item["description"] for item in response.json()] == ["Day 10", "Day 20"]


def test_get_expenses_filters_by_end_date():
    token = _register_and_login("end-date@example.com", "End Date")

    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "10.00",
            "description": "Before",
            "category": "Food",
            "expense_date": "2026-09-05",
        },
    )
    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "15.00",
            "description": "Included",
            "category": "Food",
            "expense_date": "2026-09-10",
        },
    )
    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "20.00",
            "description": "After",
            "category": "Food",
            "expense_date": "2026-09-20",
        },
    )

    response = client.get(
        "/expenses?end_date=2026-09-10",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert [item["description"] for item in response.json()] == ["Before", "Included"]


def test_get_expenses_filters_by_date_range():
    token = _register_and_login("range@example.com", "Range User")

    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "10.00",
            "description": "Outside early",
            "category": "Food",
            "expense_date": "2026-09-01",
        },
    )
    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "15.00",
            "description": "Included start",
            "category": "Food",
            "expense_date": "2026-09-10",
        },
    )
    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "20.00",
            "description": "Included middle",
            "category": "Food",
            "expense_date": "2026-09-15",
        },
    )
    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "25.00",
            "description": "Included end",
            "category": "Food",
            "expense_date": "2026-09-30",
        },
    )
    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "30.00",
            "description": "Outside late",
            "category": "Food",
            "expense_date": "2026-10-05",
        },
    )

    response = client.get(
        "/expenses?start_date=2026-09-10&end_date=2026-09-30",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert [item["description"] for item in response.json()] == [
        "Included start",
        "Included middle",
        "Included end",
    ]


def test_get_expenses_includes_boundary_dates():
    token = _register_and_login("boundary@example.com", "Boundary Day")

    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "10.00",
            "description": "Boundary start",
            "category": "Food",
            "expense_date": "2026-09-10",
        },
    )
    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "15.00",
            "description": "Boundary end",
            "category": "Food",
            "expense_date": "2026-09-30",
        },
    )

    response = client.get(
        "/expenses?start_date=2026-09-10&end_date=2026-09-30",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert [item["description"] for item in response.json()] == ["Boundary start", "Boundary end"]


def test_get_expenses_date_filter_does_not_expose_another_users_expenses():
    user_a_token = _register_and_login("usera@example.com", "User A")
    user_b_token = _register_and_login("userb@example.com", "User B")

    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {user_a_token}"},
        json={
            "amount": "10.00",
            "description": "User A item",
            "category": "Food",
            "expense_date": "2026-09-15",
        },
    )

    response = client.get(
        "/expenses?start_date=2026-09-10&end_date=2026-09-20",
        headers={"Authorization": f"Bearer {user_b_token}"},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_get_expenses_rejects_invalid_date_filter():
    token = _register_and_login("invalid-date@example.com", "Invalid Date")

    response = client.get(
        "/expenses?start_date=not-a-date",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422


def test_get_expenses_filters_by_category_and_date_together():
    token = _register_and_login("combo@example.com", "Combo User")

    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "10.00",
            "description": "Food match",
            "category": "Food",
            "expense_date": "2026-09-05",
        },
    )
    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "15.00",
            "description": "Food within range",
            "category": "Food",
            "expense_date": "2026-09-15",
        },
    )
    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "20.00",
            "description": "Housing within range",
            "category": "Housing",
            "expense_date": "2026-09-15",
        },
    )

    response = client.get(
        "/expenses?category=Food&start_date=2026-09-10&end_date=2026-09-20",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert [item["description"] for item in response.json()] == ["Food within range"]


def test_get_expenses_category_filter_only_returns_authenticated_users_expenses():
    user_a_token = _register_and_login("usera@example.com", "User A")
    user_b_token = _register_and_login("userb@example.com", "User B")

    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {user_a_token}"},
        json={
            "amount": "10.00",
            "description": "User A food",
            "category": "Food",
            "expense_date": "2026-09-15",
        },
    )
    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {user_b_token}"},
        json={
            "amount": "12.50",
            "description": "User B food",
            "category": "Food",
            "expense_date": "2026-09-18",
        },
    )

    response = client.get(
        "/expenses?category=Food",
        headers={"Authorization": f"Bearer {user_b_token}"},
    )

    assert response.status_code == 200
    assert [item["description"] for item in response.json()] == ["User B food"]


def test_get_expenses_date_range_filter_only_returns_authenticated_users_expenses():
    user_a_token = _register_and_login("usera@example.com", "User A")
    user_b_token = _register_and_login("userb@example.com", "User B")

    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {user_a_token}"},
        json={
            "amount": "15.00",
            "description": "User A date in range",
            "category": "Food",
            "expense_date": "2026-09-18",
        },
    )
    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {user_b_token}"},
        json={
            "amount": "20.00",
            "description": "User B date in range",
            "category": "Food",
            "expense_date": "2026-09-19",
        },
    )

    response = client.get(
        "/expenses?start_date=2026-09-10&end_date=2026-09-20",
        headers={"Authorization": f"Bearer {user_b_token}"},
    )

    assert response.status_code == 200
    assert [item["description"] for item in response.json()] == ["User B date in range"]


def test_get_expenses_combined_filters_only_return_authenticated_users_expenses():
    user_a_token = _register_and_login("usera@example.com", "User A")
    user_b_token = _register_and_login("userb@example.com", "User B")

    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {user_a_token}"},
        json={
            "amount": "25.00",
            "description": "User A combo",
            "category": "Food",
            "expense_date": "2026-09-16",
        },
    )
    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {user_b_token}"},
        json={
            "amount": "30.00",
            "description": "User B combo",
            "category": "Food",
            "expense_date": "2026-09-17",
        },
    )

    response = client.get(
        "/expenses?category=Food&start_date=2026-09-10&end_date=2026-09-20",
        headers={"Authorization": f"Bearer {user_b_token}"},
    )

    assert response.status_code == 200
    assert [item["description"] for item in response.json()] == ["User B combo"]


def test_get_expenses_summary_returns_total_amount_and_count_for_authenticated_user():
    token = _register_and_login("summary@example.com", "Summary User")

    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "10.00",
            "description": "Lunch",
            "category": "Food",
            "expense_date": "2026-09-01",
        },
    )
    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "15.50",
            "description": "Train",
            "category": "Transportation",
            "expense_date": "2026-09-02",
        },
    )

    response = client.get(
        "/expenses/summary",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["total_amount"] == "25.50"
    assert response.json()["total_count"] == 2


def test_get_expenses_summary_groups_totals_by_category_for_authenticated_user():
    token = _register_and_login("category-summary@example.com", "Category Summary")

    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "10.00",
            "description": "Lunch",
            "category": "Food",
            "expense_date": "2026-09-01",
        },
    )
    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "12.00",
            "description": "Dinner",
            "category": "Food",
            "expense_date": "2026-09-02",
        },
    )
    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": "40.00",
            "description": "Rent",
            "category": "Housing",
            "expense_date": "2026-09-03",
        },
    )

    response = client.get(
        "/expenses/summary",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["category_totals"] == {"Food": "22.00", "Housing": "40.00"}


def test_get_expenses_summary_excludes_another_users_expenses():
    user_a_token = _register_and_login("usera@example.com", "User A")
    user_b_token = _register_and_login("userb@example.com", "User B")

    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {user_a_token}"},
        json={
            "amount": "50.00",
            "description": "User A expense",
            "category": "Food",
            "expense_date": "2026-09-10",
        },
    )
    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {user_b_token}"},
        json={
            "amount": "15.00",
            "description": "User B expense",
            "category": "Food",
            "expense_date": "2026-09-11",
        },
    )

    response = client.get(
        "/expenses/summary",
        headers={"Authorization": f"Bearer {user_b_token}"},
    )

    assert response.status_code == 200
    assert response.json()["total_amount"] == "15.00"
    assert response.json()["total_count"] == 1
    assert response.json()["category_totals"] == {"Food": "15.00"}


def test_get_expenses_summary_rejects_unauthenticated_request():
    response = client.get("/expenses/summary")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated."


def test_get_expenses_rejects_cross_user_access():
    user_a_token = _register_and_login("usera@example.com", "User A")
    user_b_token = _register_and_login("userb@example.com", "User B")

    client.post(
        "/expenses",
        headers={"Authorization": f"Bearer {user_a_token}"},
        json={
            "amount": "10.00",
            "description": "Taxi",
            "category": "Transportation",
            "expense_date": "2026-09-28",
        },
    )

    response = client.get(
        "/expenses",
        headers={"Authorization": f"Bearer {user_b_token}"},
    )

    assert response.status_code == 200
    assert response.json() == []
