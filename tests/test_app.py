import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app import app, db, Todo

@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("SQLALCHEMY_DATABASE_URI", "sqlite:///:memory:")
    client = app.test_client()
    with app.app_context():
        db.create_all()
    yield client

def test_home_empty(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"No tasks" in resp.data or b"To-Do List" in resp.data

def test_add_task(client):
    resp = client.post("/add", data={"title": "Test Task"}, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Test Task" in resp.data
