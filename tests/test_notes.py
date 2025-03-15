import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from app.database import Base, get_db, DBNote, DBPiece

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
    # Clear all data before each test
    db = TestingSessionLocal()
    try:
        # Delete all data from tables
        db.query(DBPiece).delete()
        db.query(DBNote).delete()
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()

    yield

    # Clear all data after each test
    db = TestingSessionLocal()
    try:
        db.query(DBPiece).delete()
        db.query(DBNote).delete()
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()


def test_create_note():
    response = client.post(
        "/notes",
        json={"pieces": [{"text": "Test note piece 1"}, {"text": "Test note piece 2"}]}
    )
    assert response.status_code == 201
    data = response.json()
    assert "note_id" in data
    assert data["message"] == "Note created successfully!"


def test_get_all_notes_empty():
    response = client.get("/notes")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_notes():
    # Create a note first
    create_response = client.post(
        "/notes",
        json={"pieces": [{"text": "Test note piece"}]}
    )

    response = client.get("/notes")
    assert response.status_code == 200
    notes = response.json()
    assert len(notes) == 1
    assert "id" in notes[0]
    assert "creation_timestamp" in notes[0]
    assert "last_update_timestamp" in notes[0]
    assert "pieces" in notes[0]
    assert len(notes[0]["pieces"]) == 1
    assert notes[0]["pieces"][0]["text"] == "Test note piece"


def test_get_single_note():
    # Create a note first
    create_response = client.post(
        "/notes",
        json={"pieces": [{"text": "Test note piece"}]}
    )
    note_id = create_response.json()["note_id"]

    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    note = response.json()
    assert note["id"] == note_id
    assert len(note["pieces"]) == 1
    assert note["pieces"][0]["text"] == "Test note piece"


def test_get_single_note_not_found():
    response = client.get("/notes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"


def test_update_note():
    # Create a note first
    create_response = client.post(
        "/notes",
        json={"pieces": [{"text": "Original text"}]}
    )
    note_id = create_response.json()["note_id"]

    # Update the note
    update_response = client.put(
        f"/notes/{note_id}",
        json={"pieces": [{"text": "Updated text"}]}
    )
    assert update_response.status_code == 200
    assert update_response.json()["message"] == "Note updated successfully!"

    # Verify the update
    get_response = client.get(f"/notes/{note_id}")
    note = get_response.json()
    assert note["pieces"][0]["text"] == "Updated text"


def test_update_note_remove_pieces():
    # Create a note first with multiple pieces
    create_response = client.post(
        "/notes",
        json={"pieces": [{"text": "Piece 1"}, {"text": "Piece 2"}]}
    )
    note_id = create_response.json()["note_id"]

    # Update the note with fewer pieces
    update_response = client.put(
        f"/notes/{note_id}",
        json={"pieces": [{"text": "Piece 1"}]}
    )
    assert update_response.status_code == 200

    # Verify the update
    get_response = client.get(f"/notes/{note_id}")
    note = get_response.json()
    assert len(note["pieces"]) == 1
    assert note["pieces"][0]["text"] == "Piece 1"


def test_update_note_not_found():
    response = client.put(
        "/notes/999",
        json={"pieces": [{"text": "Updated text"}]}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"


def test_delete_note():
    # Create a note first
    create_response = client.post(
        "/notes",
        json={"pieces": [{"text": "Test note piece"}]}
    )
    note_id = create_response.json()["note_id"]

    # Delete the note
    delete_response = client.delete(f"/notes/{note_id}")
    assert delete_response.status_code == 204

    # Verify the note is deleted
    get_response = client.get(f"/notes/{note_id}")
    assert get_response.status_code == 404


def test_delete_note_not_found():
    response = client.delete("/notes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"


