from datetime import datetime


class Piece:
    def __init__(self, text: str, timestamp: datetime = None):
        """
        Initialize a Piece with the given text and current timestamp.

        :param text: The text of the piece.
        """
        if timestamp is None:
            self.timestamp = datetime.now()
        else:
            self.timestamp = timestamp
        self.text = text

    def __repr__(self):
        return f"Piece(timestamp={self.timestamp}, text='{self.text}')"


class Note:
    def __init__(self, id: int):
        """
        Initialize a Note with the current timestamp and an empty list of pieces.
        """
        self.id = id
        self.creation_timestamp = datetime.now()
        self.last_update_timestamp = self.creation_timestamp
        self.pieces = []

    def add_piece(self, piece: Piece):
        """
        Add a piece to the note and update the last update timestamp.

        :param piece: The piece to add.
        """
        self.pieces.append(piece)
        self.last_update_timestamp = datetime.now()

    def update_timestamp(self):
        self.last_update_timestamp = datetime.now()

    def __repr__(self):
        return f"Note(creation_timestamp={self.creation_timestamp}, last_update_timestamp={self.last_update_timestamp}, pieces={self.pieces})"


class Todo:
    def __init__(self, id: int, text: str):
        """
        Initialize a To-do with the given text, current timestamp, and incomplete state.

        :param text: The text of the to-do.
        """
        self.id = id
        self.text = text
        self.timestamp = datetime.now()
        self.completed = False
        self.completion_timestamp = None

    def switch_completion(self):
        """

        """
        self.completed = not self.completed
        if self.completed:
            self.completion_timestamp = datetime.now()

    def __repr__(self):
        return f"Todo(text='{self.text}', timestamp={self.timestamp}, completed={self.completed}, completion_timestamp={self.completion_timestamp})"
