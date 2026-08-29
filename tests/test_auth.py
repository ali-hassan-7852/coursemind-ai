"""
Auth flow tests. These need a real (or test) Postgres database configured
via DATABASE_URL to run against - they're stubbed here to show the shape
of what to test. Fill in as your project matures.
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_signup_and_login():
    # 1. Sign up a new user
    signup_response = client.post(
        "/auth/signup",
        json={"email": "student@example.com", "password": "testpassword123"},
    )
    assert signup_response.status_code in (200, 400)  # 400 if already exists from a prior run

    # 2. Log in with the same credentials
    login_response = client.post(
        "/auth/login",
        data={"username": "student@example.com", "password": "testpassword123"},
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
