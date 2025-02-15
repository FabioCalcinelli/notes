from datetime import datetime
from app.models import Piece, Note
import pytest

def test_piece_init():
    """Test Piece initialization with default timestamp."""
    piece = Piece("Test text")
    assert isinstance(piece.timestamp, datetime)
    assert piece.text == "Test text"

def test_piece_init_with_timestamp():
    """Test Piece initialization with custom timestamp."""
    timestamp = datetime(2022, 1, 1, 12, 0, 0)
    piece = Piece("Test text", timestamp)
    assert piece.timestamp == timestamp
    assert piece.text == "Test text"

def test_piece_repr():
    """Test Piece representation."""
    piece = Piece("Test text")
    assert repr(piece).startswith("Piece(timestamp=")

def test_note_init():
    """Test Note initialization."""
    note = Note(1)
    assert isinstance(note.creation_timestamp, datetime)
    assert isinstance(note.last_update_timestamp, datetime)
    assert note.creation_timestamp == note.last_update_timestamp
    assert note.pieces == []

def test_note_add_piece():
    """Test adding a piece to a note."""
    note = Note(1)
    piece = Piece("Test text")
    note.add_piece(piece)
    assert len(note.pieces) == 1
    assert note.pieces[0] == piece
    assert note.last_update_timestamp > note.creation_timestamp

def test_note_update_timestamp():
    """Test updating the last update timestamp of a note."""
    note = Note(1)
    initial_timestamp = note.last_update_timestamp
    note.update_timestamp()
    assert note.last_update_timestamp > initial_timestamp

def test_note_repr():
    """Test Note representation."""
    note = Note(1)
    assert repr(note).startswith("Note(creation_timestamp=")

def test_piece_timestamp_accuracy():
    """Test Piece timestamp accuracy."""
    piece = Piece("Test text")
    assert (datetime.now() - piece.timestamp).total_seconds() < 1

def test_note_timestamp_accuracy():
    """Test Note timestamp accuracy."""
    note = Note(1)
    assert (datetime.now() - note.creation_timestamp).total_seconds() < 1
    assert (datetime.now() - note.last_update_timestamp).total_seconds() < 1

def test_note_add_multiple_pieces():
    """Test adding multiple pieces to a note."""
    note = Note(1)
    piece1 = Piece("Test text 1")
    piece2 = Piece("Test text 2")
    note.add_piece(piece1)
    note.add_piece(piece2)
    assert len(note.pieces) == 2
    assert note.pieces[0] == piece1
    assert note.pieces[1] == piece2

def test_note_update_timestamp_multiple_times():
    """Test updating the last update timestamp of a note multiple times."""
    note = Note(1)
    initial_timestamp = note.last_update_timestamp
    note.update_timestamp()
    first_update_timestamp = note.last_update_timestamp
    note.update_timestamp()
    second_update_timestamp = note.last_update_timestamp
    assert initial_timestamp < first_update_timestamp
    assert first_update_timestamp < second_update_timestamp
