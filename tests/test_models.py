from app.models import Note, Piece
from app import db


def test_create_note_with_pieces(init_database):
    # Create a new Note object
    note = Note()
    piece1 = Piece(content="This is the first piece")
    piece2 = Piece(content="This is the second piece")

    # Add pieces to the note
    note._pieces.append(piece1)
    note._pieces.append(piece2)

    # Save the note (which saves the pieces as well)
    db.session.add(note)
    db.session.commit()

    # Fetch the note and check if it's saved correctly
    saved_note = Note.query.first()
    assert saved_note is not None
    assert len(saved_note._pieces) == 2
    assert saved_note._pieces[0].text == "This is the first piece"
    assert saved_note._pieces[1].text == "This is the second piece"


def test_note_update(init_database):
    # Create a new note with some pieces
    note = Note()
    piece1 = Piece(content="Old piece")
    note._pieces.append(piece1)

    # Save the note
    db.session.add(note)
    db.session.commit()

    # Verify that the note has 1 piece
    saved_note = Note.query.first()
    assert len(saved_note._pieces) == 1
    assert saved_note._pieces[0].text == "Old piece"

    # Update the note with new pieces
    piece2 = Piece(content="New piece 1")
    piece3 = Piece(content="New piece 2")
    saved_note.update([piece2, piece3])

    db.session.commit()

    # Fetch the updated note and verify changes
    updated_note = Note.query.first()
    assert len(updated_note._pieces) == 2
    assert updated_note._pieces[0].text == "New piece 1"
    assert updated_note._pieces[1].text == "New piece 2"
    assert updated_note.last_update_timestamp > updated_note.timestamp  # Ensure last_update_timestamp is updated


def test_delete_note_with_pieces(init_database):
    # Create a new note and pieces
    note = Note()
    piece1 = Piece(content="Piece 1")
    piece2 = Piece(content="Piece 2")
    note._pieces.append(piece1)
    note._pieces.append(piece2)

    # Save the note
    db.session.add(note)
    db.session.commit()

    # Verify the note and pieces are saved
    saved_note = Note.query.first()
    assert saved_note is not None
    assert len(saved_note._pieces) == 2

    # Delete the note
    db.session.delete(saved_note)
    db.session.commit()

    # Verify that the note and its pieces are deleted
    assert Note.query.count() == 0
    assert Piece.query.count() == 0
