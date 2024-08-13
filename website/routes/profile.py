from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for
from website.services.user_service import UserService
from flask_login import current_user, login_required


profile = Blueprint('profile', __name__)

@profile.route('/profile', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        data = request.form

        UserService.update_password(current_user.id, data)
        return redirect(url_for('profile.home'))

    return render_template("profile.html", user=current_user)