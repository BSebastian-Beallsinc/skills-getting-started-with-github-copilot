"""
Pytest configuration and shared fixtures for FastAPI tests.

This module provides fixtures for:
- Creating a fresh app instance for each test
- Creating a test client for making HTTP requests
- Providing clean test data
"""

import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
import src.app as app_module


# Store the initial activities state
INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Practice soccer skills and compete in interschool matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Train basketball skills and play in friendly tournaments",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mason@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore drawing, painting, and mixed media projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce school theater performances",
        "schedule": "Thursdays, 3:30 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["mia@mergington.edu", "ethan@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and critical argumentation skills",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["charlotte@mergington.edu", "james@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Solve challenging math problems and prepare for competitions",
        "schedule": "Fridays, 3:30 PM - 4:30 PM",
        "max_participants": 18,
        "participants": ["amelia@mergington.edu", "henry@mergington.edu"]
    }
}


@pytest.fixture
def app():
    """
    Provide a fresh FastAPI app instance with clean activities database.
    
    This fixture resets the global activities database to initial state
    for each test to ensure test isolation - changes in one test don't
    affect another.
    """
    # Reset the activities database to initial state
    app_module.activities = deepcopy(INITIAL_ACTIVITIES)
    return app_module.app


@pytest.fixture
def client(app):
    """
    Provide a TestClient for making HTTP requests to the app.
    
    This uses the app fixture to ensure each test gets a clean app instance
    with fresh activities database.
    """
    return TestClient(app)


@pytest.fixture
def test_email():
    """Provide a test email address for participant testing."""
    return "test.student@mergington.edu"


@pytest.fixture
def test_activity():
    """Provide a test activity name."""
    return "Chess Club"


@pytest.fixture
def nonexistent_activity():
    """Provide a non-existent activity name for error testing."""
    return "Pottery Club"


@pytest.fixture
def nonexistent_email():
    """Provide an email not in any participant list."""
    return "notregistered@mergington.edu"
