from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.errors import InvalidInput
from website.services.user_service import UserService
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import *

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = UserService.authenticate(email, password)
        if user:
            flash('Logged in successfully!', category='success')
            login_user(user)
            return redirect(url_for('notes.home'))
        else:
            flash('Incorrect email or password.', category='error')
    
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    if request.method == 'POST':
        data = request.form

        email = data.get('email')
        firstName = data.get('firstName')
        password1 = data.get('password1')
        password2 = data.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Password do not matcch.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            try:
                user = UserService.add_user(email, password1, firstName)
                flash('Account created!', category='success')
                login_user(user)
                return redirect(url_for('notes.home'))
            except ValueError as e:
                flash(str(e), category='error')
            
    return render_template("signup.html", user=current_user)

