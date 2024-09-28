import unittest

from unittest.mock import patch
from datetime import datetime

from notes import Piece, Note


class TestNotePiece(unittest.TestCase):

    @patch('notes.datetime')
    def test_piece_initialization(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 9, 28, 15, 30, 0)
        mock_datetime.strftime = datetime.strftime

        piece = Piece("This is a test piece.")

        self.assertEqual(piece.text, "This is a test piece.")

        self.assertEqual(piece.timestamp, "2024-09-28 15:30:00")

    @patch('notes.datetime')
    def test_note_initialization(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 9, 28, 15, 30, 0)
        mock_datetime.strftime = datetime.strftime

        note = Note()

        self.assertEqual(note.pieces, [])

        self.assertEqual(note.timestamp, "2024-09-28 15:30:00")

        self.assertEqual(note.last_update_timestamp, "2024-09-28 15:30:00")

    @patch('notes.datetime')
    def test_add_piece_to_note(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 9, 28, 15, 30, 0)
        mock_datetime.strftime = datetime.strftime
        note = Note()
        piece = Piece("This is another test piece.")
        note.pieces.append(piece)
        self.assertIn(piece, note.pieces)
        self.assertEqual(len(note.pieces), 1)
        self.assertEqual(note.pieces[0].text, "This is another test piece.")
        self.assertEqual(note.pieces[0].timestamp, "2024-09-28 15:30:00")


if __name__ == '__main__':
    unittest.main()
