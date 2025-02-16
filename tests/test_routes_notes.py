from fastapi.testclient import TestClient
from datetime import datetime
from .conftest import client
import pytest

def test_create_note(client: TestClient):
    """Test creating a new note"""
    note_data = {
        "pieces": [
            {"text": "Piece 1"},
            {"text": "Piece 2"}
        ]
    }
    response = client.post('/notes', json=note_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Note created successfully!", "note_id": 0}

def test_get_notes(client: TestClient):
    """Test getting all notes"""
    # Create a note
    note_data = {
        "pieces": [
            {"text": "Piece 1"},
            {"text": "Piece 2"}
        ]
    }
    client.post('/notes', json=note_data)

    response = client.get('/notes')
    assert response.status_code == 200

def test_get_note_success(client: TestClient):
    # Create a note
    note_data = {
        "pieces": [
            {"text": "Piece 1"},
            {"text": "Piece 2"}
        ]
    }
    response = client.post("/notes", json=note_data)
    note_id = response.json()["note_id"]

    # Get the note
    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["id"] == note_id
    assert len(response.json()["pieces"]) == 2

def test_get_note_not_found(client: TestClient):
    # Try to get a non-existent note
    response = client.get("/notes/22")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

def test_get_note_invalid_id(client: TestClient):
    # Try to get a note with an invalid ID
    response = client.get("/notes/xyz")
    assert response.status_code == 422

def test_get_note_empty_pieces(client: TestClient):
    # Create a note with no pieces
    note_data = {
        "pieces": []
    }
    response = client.post("/notes", json=note_data)
    note_id = response.json()["note_id"]

    # Get the note
    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["id"] == note_id
    assert len(response.json()["pieces"]) == 0

def test_get_note_multiple_notes(client: TestClient):
    # Create multiple notes
    note_data1 = {
        "pieces": [
            {"text": "Piece 1"},
            {"text": "Piece 2"}
        ]
    }
    response = client.post("/notes", json=note_data1)
    note_id1 = response.json()["note_id"]

    note_data2 = {
        "pieces": [
            {"text": "Piece 3"},
            {"text": "Piece 4"}
        ]
    }
    response = client.post("/notes", json=note_data2)
    note_id2 = response.json()["note_id"]

    # Get the notes
    response = client.get(f"/notes/{note_id1}")
    assert response.status_code == 200
    assert response.json()["id"] == note_id1
    assert len(response.json()["pieces"]) == 2

    response = client.get(f"/notes/{note_id2}")
    assert response.status_code == 200
    assert response.json()["id"] == note_id2
    assert len(response.json()["pieces"]) == 2

def test_update_note(client: TestClient):
    """Test updating a note"""
    # Create a note
    note_data = {
        "pieces": [
            {"text": "Piece 1"},
            {"text": "Piece 2"}
        ]
    }
    client.post('/notes/1', json=note_data)

    update_data = {
        "pieces": [
            {"text": "Updated Piece 1"},
            {"text": "Updated Piece 2"}
        ]
    }
    response = client.put('/notes/1', json=update_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Note updated successfully!"}

def test_update_note_invalid_note(client: TestClient):
    """Test updating a note with invalid note"""
    update_data = {
        "pieces": [
            {},
            {}
        ]
    }
    response = client.put('/notes/abc', json=update_data)
    assert response.status_code == 422

def test_update_note_note_not_found(client: TestClient):
    """Test updating a note that does not exist"""
    update_data = {
        "pieces": [
            {"text": "Updated Piece 1"},
            {"text": "Updated Piece 2"}
        ]
    }
    response = client.put('/notes/12', json=update_data)
    assert response.status_code == 404

def test_delete_note(client: TestClient):
    """Test deleting a note"""
    # Create a note
    note_data = {
        "pieces": [
            {"text": "Piece 1"},
            {"text": "Piece 2"}
        ]
    }
    client.post('/notes', json=note_data)

    response = client.delete('/notes/1')
    assert response.status_code == 200
    assert response.json() == {"message": "Note deleted successfully!"}

def test_delete_note_invalid_note_id(client: TestClient):
    """Test deleting a note with invalid note id"""
    response = client.delete('/notes/abc')
    assert response.status_code == 422

def test_delete_note_note_not_found(client: TestClient):
    """Test deleting a note that does not exist"""
    response = client.delete('/notes/15')
    assert response.status_code == 404
