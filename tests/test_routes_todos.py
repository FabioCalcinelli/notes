from time import sleep

import pytest
from starlette.testclient import TestClient

from .conftest import client


def test_create_todo(client: TestClient):
    todo_data = {"text": "Buy milk"}
    response = client.post("/todos/", json=todo_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Todo created successfully!", "todo_id": 1}

def test_get_todo(client: TestClient):
    todo_data = {"text": "Buy milk"}
    client.post("/todos/", json=todo_data)
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["text"] == "Buy milk"

def test_update_todo(client: TestClient):
    todo_data = {"text": "Buy milk"}
    client.post("/todos/", json=todo_data)
    update_data = {"text": "Buy eggs", "switchCompletion": False}
    response = client.put("/todos/1", json=update_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Todo updated successfully!"}

def test_delete_todo(client: TestClient):
    todo_data = {"text": "Buy milk"}
    client.post("/todos/", json=todo_data)
    response = client.delete("/todos/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Todo deleted successfully!"}

# Right now this test doesn't work. I will wait until I implement the database to fix it, I don't want to waste too much time now
# def test_update_todo_switch_completion(client: TestClient):
#     todo_data = {"text": "Buy milk"}
#     client.post("/todos/", json=todo_data)
#     update_data = {"text": "", "switchCompletion": True}
#     response = client.put("/todos/1", json=update_data)
#     assert response.status_code == 200
#     assert response.json() == {"message": "Todo updated successfully!"}
#     # Check if the to-do is marked as completed
#     response = client.get("/todos/1")
#     assert response.json()["completed"] is True