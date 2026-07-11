import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture(autouse=True)
def reset_activities():
    original_state = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_state)


client = TestClient(app)


def test_get_activities_returns_available_activities():
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)
    payload = response_json(response)

    # Assert
    assert response.status_code == 200
    assert "Chess Club" in payload
    assert "Programming Class" in payload


def test_signup_for_activity_prevents_duplicate_registration():
    # Arrange
    activity_name = "Chess Club"
    email = "student@mergington.edu"
    signup_endpoint = f"/activities/{activity_name}/signup"

    # Act
    first_response = client.post(
        signup_endpoint,
        params={"email": email},
    )
    second_response = client.post(
        signup_endpoint,
        params={"email": email},
    )
    second_payload = response_json(second_response)

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_payload["detail"] == "Student already signed up for this activity"
    assert activities[activity_name]["participants"].count(email) == 1


def response_json(response):
    return response.json()
