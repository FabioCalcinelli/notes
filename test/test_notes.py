import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from notes import Base, Note, Piece  # Assuming your main code is in a file named 'my_code.py'


class TestNotePieceModel(unittest.TestCase):

    def setUp(self):
        """ Set up an in-memory SQLite database and a session for each test """
        self.engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(self.engine)  # Create tables in the in-memory database
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        """ Close the session and dispose of the engine after each test """
        self.session.close()
        self.engine.dispose()

    def test_create_note_with_pieces(self):
        """ Test creating a note with multiple pieces and saving it to the database """
        note = Note()
        piece1 = Piece("First piece")
        piece2 = Piece("Second piece")
        note.update([piece1, piece2])

        self.session.add(note)
        self.session.commit()

        # Check if the note and pieces were added
        saved_note = self.session.query(Note).first()
        self.assertIsNotNone(saved_note)
        self.assertEqual(len(saved_note._pieces), 2)
        self.assertEqual(saved_note._pieces[0].text, "First piece")
        self.assertEqual(saved_note._pieces[1].text, "Second piece")

    def test_update_note(self):
        """ Test updating a note and checking if the timestamp changes """
        note = Note()
        piece1 = Piece("Original piece")
        note.update([piece1])

        self.session.add(note)
        self.session.commit()

        original_timestamp = note.last_update_timestamp

        # Update the note with new pieces
        piece2 = Piece("Updated piece")
        note.update([piece2])
        self.session.commit()

        updated_note = self.session.query(Note).first()
        self.assertEqual(len(updated_note._pieces), 1)
        self.assertEqual(updated_note._pieces[0].text, "Updated piece")
        self.assertNotEqual(updated_note.last_update_timestamp, original_timestamp)

    def test_delete_note_cascades_to_pieces(self):
        """ Test that deleting a note also deletes its associated pieces (cascade behavior) """
        note = Note()
        piece1 = Piece("First piece to delete")
        piece2 = Piece("Second piece to delete")
        note.update([piece1, piece2])

        self.session.add(note)
        self.session.commit()

        # Delete the note
        self.session.delete(note)
        self.session.commit()

        # Ensure that both the note and pieces are deleted
        deleted_note = self.session.query(Note).first()
        remaining_pieces = self.session.query(Piece).all()

        self.assertIsNone(deleted_note)
        self.assertEqual(len(remaining_pieces), 0)

    def test_timestamp_on_creation(self):
        """ Test that timestamps are properly set on note creation """
        note = Note()
        self.session.add(note)
        self.session.commit()

        saved_note = self.session.query(Note).first()
        self.assertIsNotNone(saved_note.timestamp)
        self.assertIsNotNone(saved_note.last_update_timestamp)

        # Check that the timestamps are close to the current time
        now = datetime.now()
        timestamp_diff = now - saved_note.timestamp
        self.assertLess(timestamp_diff.total_seconds(), 2)  # Should be very recent

    def test_multiple_notes(self):
        """ Test creating multiple notes with different pieces """
        note1 = Note()
        note2 = Note()

        piece1 = Piece("Piece for note 1")
        piece2 = Piece("Piece for note 2")

        note1.update([piece1])
        note2.update([piece2])

        self.session.add(note1)
        self.session.add(note2)
        self.session.commit()

        all_notes = self.session.query(Note).all()
        self.assertEqual(len(all_notes), 2)
        self.assertEqual(len(all_notes[0]._pieces), 1)
        self.assertEqual(len(all_notes[1]._pieces), 1)

        self.assertEqual(all_notes[0]._pieces[0].text, "Piece for note 1")
        self.assertEqual(all_notes[1]._pieces[0].text, "Piece for note 2")


if __name__ == '__main__':
    unittest.main()