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
            {"text": "Updated Piece 1", "timestamp": datetime.now().isoformat()},
            {"text": "Updated Piece 2", "timestamp": datetime.now().isoformat()}
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
            {"text": "Updated Piece 1", "timestamp": datetime.now().isoformat()},
            {"text": "Updated Piece 2", "timestamp": datetime.now().isoformat()}
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
