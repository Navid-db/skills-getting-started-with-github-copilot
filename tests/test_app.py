from fastapi.testclient import TestClient
import copy

from src import app as app_module

client = TestClient(app_module.app)


def setup_function():
    # make a deep copy of activities to restore after tests
    global _activities_backup
    _activities_backup = copy.deepcopy(app_module.activities)


def teardown_function():
    # restore original activities state
    app_module.activities.clear()
    app_module.activities.update(_activities_backup)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    email = "pytest-student@mergington.edu"

    # sign up
    resp = client.post("/activities/Chess%20Club/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in client.get("/activities").json()["Chess Club"]["participants"]

    # signing up same email again should fail
    resp2 = client.post("/activities/Chess%20Club/signup", params={"email": email})
    assert resp2.status_code == 400

    # unregister
    resp3 = client.delete("/activities/Chess%20Club/participants", params={"email": email})
    assert resp3.status_code == 200
    assert email not in client.get("/activities").json()["Chess Club"]["participants"]
