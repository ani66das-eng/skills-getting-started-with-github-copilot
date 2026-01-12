from pathlib import Path
import sys
from urllib.parse import quote

from fastapi.testclient import TestClient

# Ensure `src` is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from app import app  # noqa: E402

client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "Programming Class" in data


def test_signup_and_unregister_flow():
    activity = "Programming Class"
    email = "teststudent@example.com"

    # Ensure email not already present
    res = client.get("/activities")
    assert res.status_code == 200
    assert email not in res.json()[activity]["participants"]

    # Sign up
    res = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
    assert res.status_code == 200
    assert "Signed up" in res.json().get("message", "")

    # Verify added
    res = client.get("/activities")
    assert res.status_code == 200
    assert email in res.json()[activity]["participants"]

    # Unregister
    res = client.delete(f"/activities/{quote(activity)}/unregister?email={quote(email)}")
    assert res.status_code == 200
    assert "Unregistered" in res.json().get("message", "")

    # Verify removed
    res = client.get("/activities")
    assert res.status_code == 200
    assert email not in res.json()[activity]["participants"]
