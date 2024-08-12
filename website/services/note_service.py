from flask import flash
from website.models import Note
from website import mysql as db
from website.errors import InvalidInput
from sqlalchemy import text

class NoteService:

    @staticmethod
    def add_note(data, user_id):
        new_note = Note(data=data, user_id=user_id)
        db.session.add(new_note)
        db.session.commit()

    @staticmethod
    def get_note_by_id(note_id):
        try:
            query = text(f'SELECT * FROM note WHERE id = {note_id}')
            note = db.session.execute(query).fetchone()
            return note
        except Exception:
            return None

    @staticmethod
    def edit_note(note_id, data):
        if not data:
            raise InvalidInput("No data provided.", 400)
        elif not data.get('data'):
            raise InvalidInput("Conent cannot be empty.", 400)
        
        note = Note.query.get_or_404(note_id)
        note.data = data['data']
        db.session.commit()
        return note

    @staticmethod
    def delete_note(note_id, user_id):
        note = Note.query.get_or_404(note_id)
        if not note and note.user_id != int(user_id):
            return False
        
        db.session.delete(note)
        db.session.commit()
        return True
            