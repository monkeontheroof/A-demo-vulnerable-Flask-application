from flask import flash, redirect
from flask_login import login_user
from website.models import User
from website import mysql as db
from website import bcrypt
from sqlalchemy import text
from flask import url_for
from flask import url_for
from flask import url_for

class UserService:
    
    @staticmethod
    def get_all_users():
        return User.query.all()
    
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def add_user(email, password1, password2, first_name):
        
        if len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        if len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        if password1 != password2:
            flash('Password do not matcch.', category='error')
        if len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            try:
                existed_user = UserService.get_user_by_email(email)
                if existed_user:
                    raise ValueError('Email already exists.') 
                
                new_user = User(email=email, password=bcrypt.generate_password_hash(password1).decode('utf-8'), first_name=first_name)
                db.session.add(new_user)
                db.session.commit()
                flash('Account created!', category='success')
                login_user(new_user)
            except ValueError as e:
                flash(str(e), category='error')
        
    @staticmethod
    def authenticate(email, password):
        user = UserService.get_user_by_email(email)
        if user and bcrypt.check_password_hash(user.password, password):
            flash('Logged in successfully!', category='success')
            return login_user(user)
        return False
    
    @staticmethod
    def update_password(user_id, data):
        user = User.query.get_or_404(user_id)
        if not user or not data:
            flash('No password provided.', category='error')
            return redirect(url_for('profile.home'))
        if not bcrypt.check_password_hash(user.password, data.get('current_password')):
           flash('Incorrect current password.', category='error')
           return redirect(url_for('profile.home'))
        if data.get('new_password') != data.get('confirm_password'):
            flash('Passwords do not match.', category='error')
            return redirect(url_for('profile.home'))
        if len(data.get('new_password')) < 1:
            flash('Password cannot be empty.', category='error')
            return redirect(url_for('profile.home'))

        new_password = bcrypt.generate_password_hash(data.get('new_password')).decode('utf-8')
        query = f"UPDATE user SET password = \"{new_password}\", email=\"{user.email}\" WHERE id = {user.id}"
        db.session.execute(text(query))
        db.session.commit()
        flash('New password updated.', category='success')