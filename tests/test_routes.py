import pytest
from datetime import datetime
from app.models import Note, Piece, db

@pytest.fixture
def create_sample_note(init_database):
    """
    Fixture to create a sample note with two pieces for testing.
    """
    note = Note()
    piece1 = Piece(text="Piece 1 content")
    piece2 = Piece(text="Piece 2 content")
    note._pieces.append(piece1)
    note._pieces.append(piece2)
    db.session.add(note)
    db.session.commit()

    yield note

    # Cleanup after the test
    db.session.delete(note)
    db.session.commit()

# Test creating a note
def test_create_note_success(client, init_database):
    data = {
        'pieces': ['Piece 1', 'Piece 2']
    }
    response = client.post('/notes/', json=data)
    assert response.status_code == 201
    assert b'Note created successfully!' in response.data

    # Verify the note was created with pieces
    note = db.session.get(Note, 1)  # Use Session.get() instead of Query.get()
    assert note is not None
    assert len(note._pieces) == 2
    assert note._pieces[0].text == 'Piece 1'
    assert note._pieces[1].text == 'Piece 2'

def test_create_note_empty_pieces(client, init_database):
    data = {}
    response = client.post('/notes/', json=data)
    assert response.status_code == 201  # Expect success with empty pieces
    assert b'Note created successfully!' in response.data

    # Verify that the note was created with no pieces
    note = db.session.get(Note, 1)  # Use Session.get() instead of Query.get()
    assert note is not None
    assert len(note._pieces) == 0

# Test retrieving all notes
def test_get_notes_empty(client, init_database):
    response = client.get('/notes/')
    assert response.status_code == 200
    assert response.json == []

def test_get_notes_with_data(client, init_database, create_sample_note):
    response = client.get('/notes/')
    assert response.status_code == 200
    assert len(response.json) == 1

    # Verify the note data
    note_data = response.json[0]
    assert note_data['id'] == create_sample_note.id
    assert len(note_data['pieces']) == 2
    assert note_data['pieces'][0]['text'] == 'Piece 1 content'
    assert note_data['pieces'][1]['text'] == 'Piece 2 content'

# Test updating a note
def test_update_note_success(client, init_database, create_sample_note):
    note_id = create_sample_note.id
    data = {
        'pieces': ['Updated Piece 1', 'Updated Piece 2']
    }
    response = client.put(f'/notes/{note_id}', json=data)
    assert response.status_code == 200
    assert b'Note updated successfully!' in response.data

    # Verify the note was updated with new pieces
    updated_note = db.session.get(Note, note_id)  # Use Session.get() instead of Query.get()
    assert len(updated_note._pieces) == 2
    assert updated_note._pieces[0].text == 'Updated Piece 1'
    assert updated_note._pieces[1].text == 'Updated Piece 2'

def test_update_note_not_found(client, init_database):
    note_id = 999  # Non-existent note
    data = {
        'pieces': ['Updated Piece 1', 'Updated Piece 2']
    }
    response = client.put(f'/notes/{note_id}', json=data)
    assert response.status_code == 404

# Test deleting a note
def test_delete_note_success(client, init_database, create_sample_note):
    note_id = create_sample_note.id
    response = client.delete(f'/notes/{note_id}')
    assert response.status_code == 200
    assert b'Note deleted successfully!' in response.data

    # Verify the note was deleted
    deleted_note = db.session.get(Note, note_id)  # Use Session.get() instead of Query.get()
    assert deleted_note is None

def test_delete_note_not_found(client, init_database):
    note_id = 999  # Non-existent note
    response = client.delete(f'/notes/{note_id}')
    assert response.status_code == 404

