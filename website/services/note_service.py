from website.models import Note
from website import mysql as db

class NoteService:

    @staticmethod
    def add_note(data, user_id):
        new_note = Note(data=data, user_id = user_id)
        db.session.add(new_note)
        db.session.commit()

    @staticmethod
    def get_note_by_id(note_id):
        return Note.query.get_or_404(note_id)

    @staticmethod
    def edit_note(note_id, data):
        if data:
            note = Note.query.get_or_404(note_id)
            note.data = data['data']
            note.date = data['date']
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
            