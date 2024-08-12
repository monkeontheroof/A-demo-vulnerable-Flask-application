import urllib.error
from website.models import Note
from website import mysql as db
from website.errors import InvalidInput
from sqlalchemy import text
import os
import io
from xhtml2pdf import pisa
from urllib import request as requests
from urllib.parse import urlparse
from flask import send_file
import urllib

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
            
    @staticmethod
    def export_note(note_id):
        note = Note.query.get_or_404(note_id)

        file_name = os.urandom(16).hex() + '.txt'
        file_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads' , file_name)
    
        # Save the note content to the file
        try:
            with open(file_path, 'w') as file:
                file.write(note.__repr__())

            return file_name
        except Exception:
            return None
        
    @staticmethod
    def to_pdf(url):
        if not url:
            raise InvalidInput('URL is required.', 400)
        try:
            parsed_url = urlparse(url)
            response = requests.urlopen(parsed_url.geturl())
        except Exception as e:
            raise InvalidInput('Failed to fetch note.', 500)
        
        content = response.read()

        pdf_buffer = io.BytesIO()
        pisa_status = pisa.CreatePDF(content, dest=pdf_buffer) # generate PDF 
        if pisa_status.err:
            return "Error in PDF generation", 500
        
        pdf_buffer.seek(0)
        return send_file(pdf_buffer, as_attachment=False, download_name='note.pdf', mimetype='application/pdf')