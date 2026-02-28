from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"

def test_create_and_list_tasks():
    r = client.post("/tasks", json={"title": "test task"})
    assert r.status_code == 201
    created = r.json()
    assert "id" in created
    assert created["title"] == "test task"

    r = client.get("/tasks")
    assert r.status_code == 200
    tasks = r.json()
    assert any(t["title"] == "test task" for t in tasks)

def test_delete_missing_task_404():
    r = client.delete("/tasks/999999")
    assert r.status_code == 404