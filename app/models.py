from datetime import datetime
from . import db

class Piece(db.Model):
    __tablename__ = 'pieces'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'))  # ForeignKey to link Piece to Note

    def __init__(self, content: str):
        self.text = content
        self.timestamp = datetime.now()


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    last_update_timestamp = db.Column(db.DateTime, default=datetime.now)
    _pieces = db.relationship("Piece", backref="note", cascade="all, delete-orphan")

    def __init__(self):
        self.timestamp = datetime.now()
        self.last_update_timestamp = self.timestamp

    def update(self, pieces):
        self._pieces = pieces
        self.last_update_timestamp = datetime.now()
