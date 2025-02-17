from datetime import datetime

from fastapi import HTTPException, Path, APIRouter
from typing import List
from pydantic import BaseModel
from app.models import Todo, Note, Piece


notes = []
todos = []
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

@notes_router.post('/notes')
def create_note(note_data: NoteCreate):
    note_id = len(notes)+1
    note = Note(note_id)
    for piece_content in note_data.pieces:
        piece = Piece(piece_content.text)
        note.add_piece(piece)

    notes.append(note)

    return {"message": "Note created successfully!", "note_id": note.id}


@notes_router.get('/notes')
def get_notes():
    result = []

    for note in notes:
        pieces = [{'text': piece.text, 'timestamp': piece.timestamp} for i, piece in enumerate(note.pieces)]
        result.append({
            'id': note.id,
            'creation_timestamp': note.creation_timestamp,
            'last_update_timestamp': note.last_update_timestamp,
            'pieces': pieces
        })

    return result

@notes_router.get('/notes/{note_id}')
def get_note(note_id: int):
    for note in notes:
        if note.id == note_id:
            pieces = [{'text': piece.text, 'timestamp': piece.timestamp} for i, piece in enumerate(note.pieces)]
            return {
                'id': note.id,
                'creation_timestamp': note.creation_timestamp,
                'last_update_timestamp': note.last_update_timestamp,
                'pieces': pieces
            }

    raise HTTPException(status_code=404, detail="Note not found")

@notes_router.put('/notes/{note_id}')
def update_note(note_id: int, note_data: NoteUpdate):
    for note in notes:
        if note.id == note_id:
            existing_pieces = note.pieces.copy()

            note.pieces.clear()

            for piece_content in note_data.pieces:
                existing_piece = next((p for p in existing_pieces if p.text == piece_content.text), None)
                if existing_piece:
                    note.add_piece(existing_piece)
                else:
                    piece = Piece(piece_content.text, datetime.now())
                    note.add_piece(piece)

            note.update_timestamp()
            return {"message": "Note updated successfully!"}

    raise HTTPException(status_code=404, detail="Note not found")


@notes_router.delete('/notes/{note_id}')
def delete_note(note_id: int):
    for i, note in enumerate(notes):
        if note.id == note_id:
            del notes[i]
            return {"message": "Note deleted successfully!"}

    raise HTTPException(status_code=404, detail="Note not found")


@todos_router.post('/todos/')
def create_todo(todo_data: TodoCreate):
    todo_id = len(todos)+1
    todo = Todo(todo_id, todo_data.text)
    todos.append(todo)

    return {"message": "Todo created successfully!", "todo_id": todo.id}

@todos_router.get('/todos/')
def get_todos():
    result = []

    for todo in todos:
        result.append({
            'id': todo.id,
            'text': todo.text,
            'timestamp': todo.timestamp,
            'completion_timestamp': todo.completion_timestamp,
            'completed': todo.completed
        })

    return result

@todos_router.get('/todos/{todo_id}')
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return {
                'id': todo.id,
                'text': todo.text,
                'timestamp': todo.timestamp,
                'completion_timestamp': todo.completion_timestamp,
                'completed': todo.completed
            }

    raise HTTPException(status_code=404, detail="Todo not found")


@todos_router.put('/todos/{todo_id}')
def update_todo(todo_id: int, todo_data: TodoUpdate):
    for todo in todos:
        if todo.id == todo_id:
            if todo_data.text:
                todo.text = todo_data.text
            if todo_data.switchCompletion:
                todo.switch_completion()
            return {"message": "Todo updated successfully!"}

    raise HTTPException(status_code=404, detail="Todo not found")


@todos_router.delete('/todos/{todo_id}')
def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            del todos[i]
            return {"message": "Todo deleted successfully!"}

    raise HTTPException(status_code=404, detail="Todo not found")