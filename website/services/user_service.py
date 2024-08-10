from website.models import User
from website import mysql as db
from website import bcrypt
from sqlalchemy import text

class UserService:
    
    @staticmethod
    def get_all_users():
        return User.query.all()
    
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def add_user(email, password, first_name):
        existed_user = UserService.get_user_by_email(email)
        if existed_user:
            raise ValueError('Email already exists.') 
        
        new_user = User(email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'), first_name=first_name)
        db.session.add(new_user)
        db.session.commit()
        # db.session.execute(text()) 
        return new_user
        
    @staticmethod
    def authenticate(email, password):
        user = UserService.get_user_by_email(email)
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        return None