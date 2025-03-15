from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
from .database import DBNote, DBPiece
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from .database import get_db, DBTodo


notes_router = APIRouter()
todos_router = APIRouter()

class PieceCreate(BaseModel):
    text: str

class NoteCreate(BaseModel):
    pieces: List[PieceCreate]

class PieceUpdate(BaseModel):
    text: str

class NoteUpdate(BaseModel):
    pieces: List[PieceUpdate]

class TodoCreate(BaseModel):
    text: str

class TodoUpdate(BaseModel):
    text: str
    switchCompletion: bool




@notes_router.post('/notes', status_code=status.HTTP_201_CREATED)
def create_note(note_data: NoteCreate, db: Session = Depends(get_db)):
    try:
        # Create new note
        db_note = DBNote(
            creation_timestamp=datetime.now(),
            last_update_timestamp=datetime.now()
        )
        db.add(db_note)
        db.commit()
        db.refresh(db_note)

        # Add pieces
        for piece in note_data.pieces:
            db_piece = DBPiece(
                text=piece.text,
                timestamp=datetime.now(),
                note_id=db_note.id
            )
            db.add(db_piece)

        db.commit()
        return {"message": "Note created successfully!", "note_id": db_note.id}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )


@notes_router.get('/notes')
def get_all_notes(db: Session = Depends(get_db)):
    notes = db.query(DBNote).all()
    return [
        {
            "id": note.id,
            "creation_timestamp": note.creation_timestamp,
            "last_update_timestamp": note.last_update_timestamp,
            "pieces": [
                {
                    "text": piece.text,
                    "timestamp": piece.timestamp
                } for piece in note.pieces
            ]
        } for note in notes
    ]


@notes_router.get('/notes/{note_id}')
def get_single_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(DBNote).filter(DBNote.id == note_id).first()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    return {
        "id": note.id,
        "creation_timestamp": note.creation_timestamp,
        "last_update_timestamp": note.last_update_timestamp,
        "pieces": [
            {
                "text": piece.text,
                "timestamp": piece.timestamp
            } for piece in note.pieces
        ]
    }

@notes_router.put('/notes/{note_id}')
def update_note(note_id: int, note_data: NoteUpdate, db: Session = Depends(get_db)):
    try:
        # Get existing note
        note = db.query(DBNote).filter(DBNote.id == note_id).first()

        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )

        # Get existing pieces
        existing_pieces = db.query(DBPiece).filter(DBPiece.note_id == note_id).all()

        # Update existing pieces
        for i, piece in enumerate(note_data.pieces):
            if i < len(existing_pieces):
                # Update existing piece if text has changed
                if piece.text != existing_pieces[i].text:
                    existing_pieces[i].text = piece.text
                    existing_pieces[i].timestamp = datetime.now()
            else:
                # Add new piece
                db_piece = DBPiece(
                    text=piece.text,
                    timestamp=datetime.now(),
                    note_id=note_id
                )
                db.add(db_piece)

        # Delete extra existing pieces
        for i in range(len(note_data.pieces), len(existing_pieces)):
            db.delete(existing_pieces[i])

        # Update timestamps
        note.last_update_timestamp = datetime.now()

        db.commit()
        return {"message": "Note updated successfully!"}

    except HTTPException as e:
        # Re-raise HTTPExceptions to ensure they are not caught by the generic exception handler
        raise e

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )


@notes_router.delete('/notes/{note_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(DBNote).filter(DBNote.id == note_id).first()

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    try:
        # Delete associated pieces first
        db.query(DBPiece).filter(DBPiece.note_id == note_id).delete()
        # Delete the note
        db.delete(note)
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@todos_router.post('/todos/', status_code=status.HTTP_201_CREATED)
def create_todo(todo_data: TodoCreate, db: Session = Depends(get_db)):
    try:
        db_todo = DBTodo(
            text=todo_data.text,
            timestamp=datetime.now(),
            completed=False,
            completion_timestamp=None
        )
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return {"message": "Todo created successfully!", "todo_id": db_todo.id}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )


@todos_router.get('/todos/')
def get_all_todos(db: Session = Depends(get_db)):
    todos = db.query(DBTodo).all()
    return [
        {
            "id": todo.id,
            "text": todo.text,
            "timestamp": todo.timestamp,
            "completed": todo.completed,
            "completion_timestamp": todo.completion_timestamp
        } for todo in todos
    ]


@todos_router.get('/todos/{todo_id}')
def get_single_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(DBTodo).filter(DBTodo.id == todo_id).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return {
        "id": todo.id,
        "text": todo.text,
        "timestamp": todo.timestamp,
        "completed": todo.completed,
        "completion_timestamp": todo.completion_timestamp
    }


@todos_router.put('/todos/{todo_id}')
def update_todo(todo_id: int, todo_data: TodoUpdate, db: Session = Depends(get_db)):
    try:
        todo = db.query(DBTodo).filter(DBTodo.id == todo_id).first()

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )

        if todo_data.text is not None:
            todo.text = todo_data.text

        if todo_data.switchCompletion:
            todo.completed = not todo.completed
            todo.completion_timestamp = datetime.now() if todo.completed else todo.completion_timestamp

        db.commit()
        return {"message": "Todo updated successfully!"}

    except HTTPException:
        # Re-raise HTTPExceptions to ensure they are not caught by the generic exception handler
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )



@todos_router.delete('/todos/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(DBTodo).filter(DBTodo.id == todo_id).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    try:
        db.delete(todo)
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
