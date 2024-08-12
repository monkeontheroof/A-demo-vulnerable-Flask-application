from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.services.user_service import UserService
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import *

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('notes.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = UserService.authenticate(email, password)
        if user:
            return redirect(url_for('notes.home'))

        flash('Incorrect email or password.', category='error')
    
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('notes.home'))
    if request.method == 'POST':
        data = request.form

        email = data.get('email')
        first_name = data.get('firstName')
        password1 = data.get('password1')
        password2 = data.get('password2')

        UserService.add_user(email, password1, password2, first_name)
        return redirect(url_for('notes.home'))
            
    return render_template("signup.html", user=current_user)

