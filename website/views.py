from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import flask

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    greeting = request.args.get('greeting', 'Hello')
    return render_template("home.html", user=current_user, greeting=greeting)
