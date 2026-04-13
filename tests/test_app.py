import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert: Test /activities endpoint

def test_get_activities():
    # Arrange: (nothing to set up for GET)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data, "Activities list should not be empty"

# Arrange-Act-Assert: Test signup endpoint

def test_signup_activity():
    # Arrange
    email = "testuser@mergington.edu"
    activity = next(iter(client.get("/activities").json().keys()))
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert "message" in response.json()

# Arrange-Act-Assert: Test duplicate signup

def test_signup_duplicate():
    # Arrange
    email = "testdupe@mergington.edu"
    activity = next(iter(client.get("/activities").json().keys()))
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "detail" in response.json()

# Arrange-Act-Assert: Test unregister endpoint

def test_unregister_activity():
    # Arrange
    email = "testremove@mergington.edu"
    activity = next(iter(client.get("/activities").json().keys()))
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert "message" in response.json()
