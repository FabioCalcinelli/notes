from flask import Blueprint, request, jsonify
from .models import Note, Piece
from . import db
from datetime import datetime

# Create a blueprint for notes routes
notes_bp = Blueprint('notes', __name__)


# Create a Note
@notes_bp.route('/', methods=['POST'])
def create_note():
    data = request.get_json()
    pieces_data = data.get('pieces', [])

    note = Note()
    for piece_content in pieces_data:
        piece = Piece(content=piece_content)
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
    note = Note.query.get_or_404(note_id)
    data = request.get_json()

    pieces_data = data.get('pieces', [])

    # Clear existing pieces
    note._pieces.clear()

    # Add new pieces
    for piece_content in pieces_data:
        piece = Piece(content=piece_content)
        note._pieces.append(piece)

    note.last_update_timestamp = datetime.now()

    db.session.commit()

    return jsonify({'message': 'Note updated successfully!'}), 200


# Delete a Note
@notes_bp.route('/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()

    return jsonify({'message': 'Note deleted successfully!'}), 200
