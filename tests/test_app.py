"""
FastAPI backend tests using AAA (Arrange-Act-Assert) pattern.

This test module covers all API endpoints:
- GET /activities: Retrieve all activities
- POST /activities/{activity_name}/signup: Sign up a participant
- DELETE /activities/{activity_name}/unregister: Unregister a participant
- GET /: Redirect to static index

Each test follows the AAA pattern for clarity:
- Arrange: Set up test data and fixtures
- Act: Execute the action being tested
- Assert: Verify the results
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_all_activities_returns_200(self, client):
        """
        Arrange: Create a test client
        Act: Call GET /activities
        Assert: Verify 200 OK status
        """
        # Arrange
        # (client fixture provides test client)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200

    def test_get_activities_returns_dict(self, client):
        """
        Arrange: Create a test client
        Act: Call GET /activities
        Assert: Verify response is a dictionary
        """
        # Arrange
        # (client fixture provides test client)

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert isinstance(data, dict)

    def test_get_activities_contains_expected_activities(self, client):
        """
        Arrange: Create a test client
        Act: Call GET /activities
        Assert: Verify all expected activities are present
        """
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity in expected_activities:
            assert activity in data

    def test_activity_has_correct_structure(self, client, test_activity):
        """
        Arrange: Create a test client and activity name
        Act: Call GET /activities and check structure
        Assert: Verify each activity has required fields
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        data = response.json()
        activity = data[test_activity]

        # Assert
        for field in required_fields:
            assert field in activity

    def test_participants_list_is_array(self, client, test_activity):
        """
        Arrange: Create a test client and activity name
        Act: Call GET /activities
        Assert: Verify participants is a list
        """
        # Arrange
        # (client and test_activity fixtures provided)

        # Act
        response = client.get("/activities")
        data = response.json()
        participants = data[test_activity]["participants"]

        # Assert
        assert isinstance(participants, list)

    def test_participants_contain_valid_emails(self, client, test_activity):
        """
        Arrange: Create a test client and activity name
        Act: Call GET /activities
        Assert: Verify participants are email strings
        """
        # Arrange
        # (client and test_activity fixtures provided)

        # Act
        response = client.get("/activities")
        data = response.json()
        participants = data[test_activity]["participants"]

        # Assert
        assert len(participants) > 0
        for participant in participants:
            assert isinstance(participant, str)
            assert "@" in participant


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_successful_signup_returns_200(self, client, test_activity, test_email):
        """
        Arrange: Create client with test email and activity
        Act: Call POST signup endpoint
        Assert: Verify 200 OK status
        """
        # Arrange
        # (client, test_activity, test_email fixtures provided)

        # Act
        response = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 200

    def test_signup_adds_participant_to_activity(self, client, test_activity, test_email):
        """
        Arrange: Create client, activity, and test email
        Act: Signup participant then get activities
        Assert: Verify participant is in the activity
        """
        # Arrange
        # (client, test_activity, test_email fixtures provided)

        # Act
        client.post(
            f"/activities/{test_activity}/signup",
            params={"email": test_email}
        )
        response = client.get("/activities")
        data = response.json()
        participants = data[test_activity]["participants"]

        # Assert
        assert test_email in participants

    def test_signup_returns_success_message(self, client, test_activity, test_email):
        """
        Arrange: Create client, activity, and test email
        Act: Call POST signup endpoint
        Assert: Verify response contains success message
        """
        # Arrange
        # (client, test_activity, test_email fixtures provided)

        # Act
        response = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": test_email}
        )
        data = response.json()

        # Assert
        assert "message" in data
        assert test_email in data["message"]
        assert test_activity in data["message"]

    def test_duplicate_signup_returns_400(self, client, test_activity):
        """
        Arrange: Use existing participant in test activity
        Act: Try to signup same participant twice
        Assert: Verify 400 Bad Request on duplicate
        """
        # Arrange
        existing_participant = "michael@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": existing_participant}
        )

        # Assert
        assert response.status_code == 400

    def test_duplicate_signup_returns_error_message(self, client, test_activity):
        """
        Arrange: Use existing participant in test activity
        Act: Try to signup same participant twice
        Assert: Verify error message mentions duplicate
        """
        # Arrange
        existing_participant = "michael@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{test_activity}/signup",
            params={"email": existing_participant}
        )
        data = response.json()

        # Assert
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_signup_to_nonexistent_activity_returns_404(self, client, test_email, nonexistent_activity):
        """
        Arrange: Create client with non-existent activity name
        Act: Try to signup to non-existent activity
        Assert: Verify 404 Not Found
        """
        # Arrange
        # (client, test_email, nonexistent_activity fixtures provided)

        # Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 404

    def test_nonexistent_activity_returns_error_message(self, client, test_email, nonexistent_activity):
        """
        Arrange: Create client with non-existent activity name
        Act: Try to signup to non-existent activity
        Assert: Verify error message mentions activity not found
        """
        # Arrange
        # (client, test_email, nonexistent_activity fixtures provided)

        # Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": test_email}
        )
        data = response.json()

        # Assert
        assert "detail" in data
        assert "not found" in data["detail"].lower()


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint."""

    def test_successful_unregister_returns_200(self, client, test_activity):
        """
        Arrange: Use existing participant in test activity
        Act: Call DELETE unregister endpoint
        Assert: Verify 200 OK status
        """
        # Arrange
        existing_participant = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{test_activity}/unregister",
            params={"email": existing_participant}
        )

        # Assert
        assert response.status_code == 200

    def test_unregister_removes_participant_from_activity(self, client, test_activity):
        """
        Arrange: Verify participant exists in activity
        Act: Call DELETE unregister then get activities
        Assert: Verify participant is no longer in activity
        """
        # Arrange
        existing_participant = "michael@mergington.edu"
        
        # Verify participant exists before deletion
        response = client.get("/activities")
        data = response.json()
        assert existing_participant in data[test_activity]["participants"]

        # Act
        client.delete(
            f"/activities/{test_activity}/unregister",
            params={"email": existing_participant}
        )
        response = client.get("/activities")
        data = response.json()
        participants = data[test_activity]["participants"]

        # Assert
        assert existing_participant not in participants

    def test_unregister_returns_success_message(self, client, test_activity):
        """
        Arrange: Use existing participant in test activity
        Act: Call DELETE unregister endpoint
        Assert: Verify response contains success message
        """
        # Arrange
        existing_participant = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{test_activity}/unregister",
            params={"email": existing_participant}
        )
        data = response.json()

        # Assert
        assert "message" in data
        assert existing_participant in data["message"]
        assert test_activity in data["message"]

    def test_unregister_nonexistent_participant_returns_400(self, client, test_activity, nonexistent_email):
        """
        Arrange: Use email not registered for activity
        Act: Try to unregister non-existent participant
        Assert: Verify 400 Bad Request
        """
        # Arrange
        # (client, test_activity, nonexistent_email fixtures provided)

        # Act
        response = client.delete(
            f"/activities/{test_activity}/unregister",
            params={"email": nonexistent_email}
        )

        # Assert
        assert response.status_code == 400

    def test_unregister_nonexistent_participant_returns_error_message(self, client, test_activity, nonexistent_email):
        """
        Arrange: Use email not registered for activity
        Act: Try to unregister non-existent participant
        Assert: Verify error message
        """
        # Arrange
        # (client, test_activity, nonexistent_email fixtures provided)

        # Act
        response = client.delete(
            f"/activities/{test_activity}/unregister",
            params={"email": nonexistent_email}
        )
        data = response.json()

        # Assert
        assert "detail" in data
        assert "not signed up" in data["detail"].lower()

    def test_unregister_from_nonexistent_activity_returns_404(self, client, test_email, nonexistent_activity):
        """
        Arrange: Create client with non-existent activity name
        Act: Try to unregister from non-existent activity
        Assert: Verify 404 Not Found
        """
        # Arrange
        # (client, test_email, nonexistent_activity fixtures provided)

        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity}/unregister",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 404

    def test_unregister_from_nonexistent_activity_returns_error_message(self, client, test_email, nonexistent_activity):
        """
        Arrange: Create client with non-existent activity name
        Act: Try to unregister from non-existent activity
        Assert: Verify error message mentions activity not found
        """
        # Arrange
        # (client, test_email, nonexistent_activity fixtures provided)

        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity}/unregister",
            params={"email": test_email}
        )
        data = response.json()

        # Assert
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_cannot_unregister_twice(self, client, test_activity):
        """
        Arrange: Use existing participant
        Act: Unregister twice
        Assert: Verify second unregister returns 400
        """
        # Arrange
        existing_participant = "michael@mergington.edu"

        # First unregister succeeds
        response1 = client.delete(
            f"/activities/{test_activity}/unregister",
            params={"email": existing_participant}
        )
        assert response1.status_code == 200

        # Act
        response2 = client.delete(
            f"/activities/{test_activity}/unregister",
            params={"email": existing_participant}
        )

        # Assert
        assert response2.status_code == 400


class TestRootRedirect:
    """Tests for GET / endpoint."""

    def test_root_redirects_to_static_index(self, client):
        """
        Arrange: Create a test client
        Act: Call GET / with follow_redirects=False
        Assert: Verify 307 redirect to /static/index.html
        """
        # Arrange
        # (client fixture provides test client)

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
