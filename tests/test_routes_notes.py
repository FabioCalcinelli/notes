from fastapi.testclient import TestClient
from main import app
from datetime import datetime

client = TestClient(app)

def test_create_note():
    """Test creating a new note"""
    note_data = {
        "pieces": [
            {"text": "Piece 1"},
            {"text": "Piece 2"}
        ]
    }
    response = client.post('/notes/1', json=note_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Note created successfully!", "note_id": 1}

def test_create_note_invalid_note_id():
    """Test creating a new note with invalid note id"""
    note_data = {
        "pieces": [
            {"text": "Piece 1"},
            {"text": "Piece 2"}
        ]
    }
    response = client.post('/notes/abc', json=note_data)
    assert response.status_code == 422

def test_get_notes():
    """Test getting all notes"""
    # Create a note
    note_data = {
        "pieces": [
            {"text": "Piece 1"},
            {"text": "Piece 2"}
        ]
    }
    client.post('/notes/1', json=note_data)

    response = client.get('/notes')
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_notes_empty():
    """Test getting all notes when there are no notes"""
    response = client.get('/notes')
    assert response.status_code == 200
    assert response.json() == []

def test_update_note():
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

def test_update_note_invalid_note():
    """Test updating a note with invalid note"""
    update_data = {
        "pieces": [
            {},
            {}
        ]
    }
    response = client.put('/notes/abc', json=update_data)
    assert response.status_code == 422

def test_update_note_note_not_found():
    """Test updating a note that does not exist"""
    update_data = {
        "pieces": [
            {"text": "Updated Piece 1", "timestamp": datetime.now().isoformat()},
            {"text": "Updated Piece 2", "timestamp": datetime.now().isoformat()}
        ]
    }
    response = client.put('/notes/1', json=update_data)
    assert response.status_code == 404

def test_delete_note():
    """Test deleting a note"""
    # Create a note
    note_data = {
        "pieces": [
            {"text": "Piece 1"},
            {"text": "Piece 2"}
        ]
    }
    client.post('/notes/1', json=note_data)

    response = client.delete('/notes/1')
    assert response.status_code == 200
    assert response.json() == {"message": "Note deleted successfully!"}

def test_delete_note_invalid_note_id():
    """Test deleting a note with invalid note id"""
    response = client.delete('/notes/abc')
    assert response.status_code == 422

def test_delete_note_note_not_found():
    """Test deleting a note that does not exist"""
    response = client.delete('/notes/1')
    assert response.status_code == 404
