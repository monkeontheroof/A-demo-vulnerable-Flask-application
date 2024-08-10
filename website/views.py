from flask import Blueprint, json, render_template, request, render_template_string, flash
from flask_login import login_required, current_user
from markupsafe import Markup
from website.services.note_service import NoteService
from flask import jsonify

views = Blueprint('views', __name__)

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            try:
                NoteService.add_note(data=note, user_id=current_user.id)
                flash('Note added!', category='success')
            except ValueError as e:
                flash(f'{e}', category='error')

    greeting = 'Welcome back anonymous!'
    if (current_user.is_authenticated):
        greeting = render_template_string(f'Welcome back {current_user.first_name}')
    return render_template("home.html", user=current_user, greeting=greeting)

@views.route('/note/<int:note_id>', methods=['GET', 'POST'])
def note(note_id):
    note = NoteService.get_note_by_id(note_id)

    if request.method == 'POST':
        data = request.get_json()
        if data:
            NoteService.edit_note(note.id, data=data)
            flash('Note saved!', category='success')
            return jsonify({'success':True})
        elif not data:
            return jsonify({"success": False, "error": "No data found"}), 404
        
        required_fields = ['date', 'data']
            for field in required_fields:
                if not data.get(field):
                    raise ValueError(f"{field.capitalize()} field is required")
    
    return render_template("note.html", user=current_user, note=note)

@views.route('/delete-note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    NoteService.delete_note(note_id, current_user.id)
    return jsonify({})

@views.route('/')
def index():
    message = request.args.get('greeting', 'Welcome back!')
    return render_template_string("""
        {% extends "base.html" %} {% block title %}Index{% endblock %}
        {% block content %}""" 
        + f'<p>{message}</p>' + 
        '{% endblock %}'
        , user=current_user)