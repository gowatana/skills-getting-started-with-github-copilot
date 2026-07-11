from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_unregister_participant_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "test@student.mergington.edu"
    signup_endpoint = f"/activities/{activity_name}/signup"

    activities[activity_name]["participants"].append(email)

    try:
        # Act
        response = client.delete(
            signup_endpoint,
            params={"email": email},
        )
        payload = response.json()

        # Assert
        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
        assert payload["message"] == f"Unregistered {email} from {activity_name}"
    finally:
        if email in activities[activity_name]["participants"]:
            activities[activity_name]["participants"].remove(email)
