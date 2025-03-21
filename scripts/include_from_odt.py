import re
from datetime import datetime

import odf.text
import odf.opendocument
from odf.text import P
from sqlalchemy.orm import Session

def parse_timestamp(para):
    # Remove the '#<integer> ' prefix
    line = re.sub(r'^#\d+ ', '', para)
    # Parse the timestamp
    try:
        timestamp = datetime.strptime(line, '%A, %d %B %Y %H:%M:%S')
    except:
        pass
    return timestamp

def process_odt(file_path: str, db: Session):
    # Open the .odt file
    textdoc = odf.opendocument.load(file_path)

    # Extract text content
    paragraphs = []
    for element in textdoc.getElementsByType(P):
        paragraph = str(element)
        if paragraph != '' and paragraph is not None:
            paragraphs.append(paragraph)

    first=True
    for para in paragraphs:
        if para[0] == "#":
            current_timestamp = parse_timestamp(para)
            if not first:
                db.commit()
            if first:
                first = False
            new_note = DBNote(
                creation_timestamp=current_timestamp,
                last_update_timestamp=current_timestamp,
            )
            db.add(new_note)
            continue
        elif para[:5] == "TODO:" or para[:5] == "DONE:":
            new_todo = DBTodo(
                text=para[5:],
                timestamp=current_timestamp,
                completed = para[:5] == "DONE:"
            )
            if para[:5] == "DONE:":
                new_todo.completion_timestamp=current_timestamp
            db.add(new_todo)
            db.commit()
            continue
        db.commit()
        new_piece = DBPiece(
            text=para,
            timestamp=current_timestamp,
            note_id=new_note.id,
        )
        db.add(new_piece)
    db.commit()

# Usage example:
if __name__ == "__main__":
    from app.database import SessionLocal, Base, DBPiece, DBNote, DBTodo

    db = SessionLocal()
    process_odt("/home/fabio/Documents/notes/Notes.odt", db)
    db.close()
