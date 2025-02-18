from flask import Blueprint, jsonify, redirect, render_template, render_template_string, request, flash
from flask_login import login_required, current_user
from markupsafe import Markup
from website.errors import InvalidInput
from website.services.note_service import NoteService
from flask import url_for

note = Blueprint('notes', __name__)

@note.route('/')
@login_required
def home():
    # message = request.args.get('message', 'Welcome back!')
    # return render_template_string(f'{os.getenv('APP_SECRET_KEY')}')
    return render_template("home.html", user=current_user)

@note.route('/notes', methods=['GET', 'POST'])
@login_required
def my_note():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            try:
                NoteService.add_note(data=note, user_id=current_user.id)
                flash('Note added!', category='success')
            except Exception:
                flash('Failed.', category='error')

    message = Markup(f'{current_user.first_name}\'s Notes')

    return render_template("note.html", user=current_user, message=message)

@note.route('/note/<note_id>', methods=['GET', 'POST'])
@login_required
def notes(note_id):
    note = NoteService.get_note_by_id(note_id)
    
    if not note or note.user_id != current_user.id:
        return redirect(url_for('notes.my_note'))

    if request.method == 'POST':
        data = request.get_json()

        NoteService.edit_note(note.id, data=data)
        flash('Saved successfully.', category='success')
        return jsonify({'success':True})
    
    return render_template("edit_note.html", user=current_user, note=note)

@note.route('/delete-note/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    NoteService.delete_note(note_id, current_user.id)
    return jsonify({})

@note.route('/save-note/<int:note_id>', methods=['POST'])
@login_required
def save_note(note_id):
    file_name = NoteService.export_note(note_id)    
    
    if not file_name:
        raise InvalidInput('Failed to save note.', 500)
    
    file_url = request.host_url + 'static/uploads/' + file_name
    
    # return redirect(url_for('notes.convert_to_pdf', url=file_url))
    return jsonify({'url': file_url})

@note.route('/pdf')
@login_required
def convert_to_pdf():
    url = request.args.get('url')
    
    return NoteService.to_pdf(url)
    



