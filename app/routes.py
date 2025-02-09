from flask import Blueprint, request, jsonify
from .models import Note, Piece, Todo
from . import db
from datetime import datetime

notes_bp = Blueprint('notes', __name__)

# Create a Note
@notes_bp.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    pieces_data = data.get('pieces', [])

    note = Note()
    for piece_content in pieces_data:
        piece = Piece(text=piece_content)
        note._pieces.append(piece)

    db.session.add(note)
    db.session.commit()

    return jsonify({'message': 'Note created successfully!', 'note_id': note.id}), 201

# Get All Notes
@notes_bp.route('/notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    result = []

    for note in notes:
        pieces = [{'id': piece.id, 'text': piece.text, 'timestamp': piece.timestamp} for piece in note._pieces]
        result.append({
            'id': note.id,
            'timestamp': note.timestamp,
            'last_update_timestamp': note.last_update_timestamp,
            'pieces': pieces
        })

    return jsonify(result), 200

# Update a Note
@notes_bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = db.session.get(Note, note_id)  # Use Session.get() instead of Query.get()
    if note is None:
        return jsonify({'message': 'Note not found'}), 404

    data = request.get_json()
    pieces_data = data.get('pieces', [])

    # Clear existing pieces
    note._pieces.clear()

    # Add new pieces
    for piece_content in pieces_data:
        piece = Piece(text=piece_content)
        note._pieces.append(piece)

    note.last_update_timestamp = datetime.now()
    db.session.commit()

    return jsonify({'message': 'Note updated successfully!'}), 200

# Delete a Note
@notes_bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = db.session.get(Note, note_id)  # Use Session.get() instead of Query.get()
    if note is None:
        return jsonify({'message': 'Note not found'}), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({'message': 'Note deleted successfully!'}), 200

# Create a To-do
@notes_bp.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    text_data = data.get('text', '')

    todo = Todo(text_data)

    db.session.add(todo)
    db.session.commit()

    return jsonify({'message': 'Todo created successfully!', 'todo_id': todo.id}), 201

# Get a To_do
@notes_bp.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = db.session.get(Todo, todo_id)  # Use Session.get() instead of Query.get()
    if todo is None:
        return jsonify({'message': 'Todo not found'}), 404

    return jsonify({
        'id': todo.id,
        'text': todo.text,
        'timestamp': todo.timestamp,
        'completion_timestamp': todo.completion_timestamp,
        'completed': todo.completed
    }), 200

# Update a To_do
@notes_bp.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = db.session.get(Todo, todo_id)  # Use Session.get() instead of Query.get()
    if todo is None:
        return jsonify({'message': 'Todo not found'}), 404

    data = request.get_json()
    text = data.get('text')

    if text:
        todo.text = text

    db.session.commit()

    return jsonify({'message': 'Todo updated successfully!'}), 200

# Complete a To_do
@notes_bp.route('/todos/<int:todo_id>/complete', methods=['PUT'])
def complete_todo(todo_id):
    todo = db.session.get(Todo, todo_id)  # Use Session.get() instead of Query.get()
    if todo is None:
        return jsonify({'message': 'Todo not found'}), 404

    todo.complete()
    db.session.commit()

    return jsonify({'message': 'Todo completed successfully!'}), 200

# Delete a To_do
@notes_bp.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = db.session.get(Todo, todo_id)  # Use Session.get() instead of Query.get()
    if todo is None:
        return jsonify({'message': 'Todo not found'}), 404

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'message': 'Todo deleted successfully!'}), 200
