import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from app.database import Base, get_db, DBTodo

# Create a separate in-memory SQLite database for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Ensures same connection is used
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables
Base.metadata.create_all(bind=engine)


# Override the dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    # Create tables before each test
    Base.metadata.create_all(bind=engine)
    yield
    # Clean up after each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_todo():
    response = client.post(
        "/todos/",
        json={"text": "Test todo item"}
    )
    assert response.status_code == 201
    data = response.json()
    assert "todo_id" in data
    assert data["message"] == "Todo created successfully!"


def test_get_all_todos_empty():
    response = client.get("/todos/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_todos():
    # Create a todo first
    client.post(
        "/todos/",
        json={"text": "Test todo item"}
    )

    response = client.get("/todos/")
    assert response.status_code == 200
    todos = response.json()
    assert len(todos) == 1
    assert "id" in todos[0]
    assert "text" in todos[0]
    assert "timestamp" in todos[0]
    assert "completed" in todos[0]
    assert "completion_timestamp" in todos[0]
    assert todos[0]["text"] == "Test todo item"
    assert todos[0]["completed"] == False
    assert todos[0]["completion_timestamp"] is None


def test_get_single_todo():
    # Create a todo first
    create_response = client.post(
        "/todos/",
        json={"text": "Test todo item"}
    )
    todo_id = create_response.json()["todo_id"]

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    todo = response.json()
    assert todo["id"] == todo_id
    assert todo["text"] == "Test todo item"
    assert todo["completed"] == False
    assert todo["completion_timestamp"] is None


def test_get_single_todo_not_found():
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


def test_update_todo_text():
    # Create a todo first
    create_response = client.post(
        "/todos/",
        json={"text": "Original todo text"}
    )
    todo_id = create_response.json()["todo_id"]

    # Update the todo text
    update_response = client.put(
        f"/todos/{todo_id}",
        json={"text": "Updated todo text", "switchCompletion": False}
    )
    assert update_response.status_code == 200
    assert update_response.json()["message"] == "Todo updated successfully!"

    # Verify the update
    get_response = client.get(f"/todos/{todo_id}")
    todo = get_response.json()
    assert todo["text"] == "Updated todo text"
    assert todo["completed"] == False


def test_update_todo_completion():
    # Create a todo first
    create_response = client.post(
        "/todos/",
        json={"text": "Todo item"}
    )
    todo_id = create_response.json()["todo_id"]

    # Mark as completed
    update_response = client.put(
        f"/todos/{todo_id}",
        json={"text": "Todo item", "switchCompletion": True}
    )
    assert update_response.status_code == 200

    # Verify the update
    get_response = client.get(f"/todos/{todo_id}")
    todo = get_response.json()
    assert todo["completed"] == True
    assert todo["completion_timestamp"] is not None

    # Mark as incomplete again
    update_response = client.put(
        f"/todos/{todo_id}",
        json={"text": "Todo item", "switchCompletion": True}
    )
    assert update_response.status_code == 200

    # Verify the update
    get_response = client.get(f"/todos/{todo_id}")
    todo = get_response.json()
    assert todo["completed"] == False


def test_update_todo_not_found():
    response = client.put(
        "/todos/999",
        json={"text": "Updated text", "switchCompletion": False}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


def test_delete_todo():
    # Create a todo first
    create_response = client.post(
        "/todos/",
        json={"text": "Test todo item"}
    )
    todo_id = create_response.json()["todo_id"]

    # Delete the todo
    delete_response = client.delete(f"/todos/{todo_id}")
    assert delete_response.status_code == 204

    # Verify the todo is deleted
    get_response = client.get(f"/todos/{todo_id}")
    assert get_response.status_code == 404


def test_delete_todo_not_found():
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"
