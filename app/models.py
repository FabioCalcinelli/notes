from datetime import datetime
from typing import List

from . import db

class Piece(db.Model):
    __tablename__ = 'pieces'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.id', ondelete='CASCADE'))

    def __init__(self, text: str):
        self.text = text


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    last_update_timestamp = db.Column(db.DateTime, default=datetime.now)

    _pieces = db.relationship("Piece", backref="note", cascade="all, delete-orphan", passive_deletes=True)

    def __init__(self):
        self.timestamp = datetime.now()
        self.last_update_timestamp = self.timestamp

    def update(self, pieces: List[Piece]):
        self._pieces = pieces
        self.last_update_timestamp = datetime.now()

    __mapper_args__ = {
        "confirm_deleted_rows": False  # Disable confirmation of the number of rows deleted
    }

class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    completion_timestamp = db.Column(db.DateTime, default=None)
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, text: str):
        self.timestamp = datetime.now()
        self.text = text
        self.completed = False

    def complete(self):
        self.completed = True
        self.completion_timestamp = datetime.now()
