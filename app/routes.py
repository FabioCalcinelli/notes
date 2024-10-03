from flask import Blueprint, request, jsonify
from .models import Note, Piece
from . import db
from datetime import datetime

notes_bp = Blueprint('notes', __name__)

# Create a Note
@notes_bp.route('/', methods=['POST'])
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
@notes_bp.route('/', methods=['GET'])
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
@notes_bp.route('/<int:note_id>', methods=['PUT'])
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
@notes_bp.route('/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = db.session.get(Note, note_id)  # Use Session.get() instead of Query.get()
    if note is None:
        return jsonify({'message': 'Note not found'}), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({'message': 'Note deleted successfully!'}), 200

