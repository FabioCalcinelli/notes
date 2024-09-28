from datetime import datetime
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Create the base class for SQLAlchemy models
Base = declarative_base()


class Piece(Base):
    __tablename__ = 'pieces'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    note_id = Column(Integer, ForeignKey('notes.id'))  # ForeignKey to link Piece to Note

    def __init__(self, content: str):
        self.text = content
        self.timestamp = datetime.now()


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now)
    last_update_timestamp = Column(DateTime, default=datetime.now)
    _pieces = relationship("Piece", backref="note", cascade="all, delete-orphan")

    def __init__(self):
        self.timestamp = datetime.now()
        self.last_update_timestamp = self.timestamp

    def update(self, pieces: List[Piece]):
        self._pieces = pieces
        self.last_update_timestamp = datetime.now()


# Set up the SQLite database (or any other database engine you prefer)
engine = create_engine('sqlite:///notes.db', echo=True)

# Create all tables
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()


# Example: Adding and saving notes and pieces
def create_sample_data():
    note1 = Note()
    piece1 = Piece("First piece of note 1")
    piece2 = Piece("Second piece of note 1")

    note1.update([piece1, piece2])

    session.add(note1)
    session.commit()


create_sample_data()

# Querying the database
all_notes = session.query(Note).all()
for note in all_notes:
    print(f"Note created at: {note.timestamp}, Last updated at: {note.last_update_timestamp}")
    for piece in note._pieces:
        print(f"- Piece: {piece.text}, Created at: {piece.timestamp}")



