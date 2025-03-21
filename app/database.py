from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

PATH_TO_DATABASE = '/home/fabio/PycharmProjects/notes/app.db'
# Original database configuration
SQLALCHEMY_DATABASE_URL = f"sqlite:///{PATH_TO_DATABASE}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Model definitions
class DBPiece(Base):
    __tablename__ = "pieces"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    timestamp = Column(DateTime)
    note_id = Column(Integer, ForeignKey("notes.id"))

class DBNote(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    creation_timestamp = Column(DateTime)
    last_update_timestamp = Column(DateTime)
    pieces = relationship("DBPiece", backref="note")

class DBTodo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    timestamp = Column(DateTime)
    completed = Column(Boolean)
    completion_timestamp = Column(DateTime)

# Create tables in the original database
Base.metadata.create_all(bind=engine)

# Dependency for the original database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



