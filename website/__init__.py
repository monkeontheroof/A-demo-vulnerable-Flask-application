from datetime import datetime
import os
from flask import Flask, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from website.config import Config
import pymysql
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .errors import InvalidInput

mysql = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    
    app.config.from_object(Config) # from config.py

    app.config['SQLALCHEMY_DATABASE_URI'] += Config.MYSQL_DATABASE + '?charset=utf8mb4'
    
    mysql.init_app(app)
    bcrypt.init_app(app)
    
    from .routes.note import note
    from .routes.auth import auth

    app.register_blueprint(note, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Flag
    
    create_database()
    
    # configure the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.session_protection = None
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.errorhandler(InvalidInput)
    def handle_invalid_input(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    # create tables and insert records
    with app.app_context():
        mysql.drop_all()
        mysql.create_all()

        admin = User(email="admin@gmail.com", password="$2a$10$YVxRbvILas.DQFjLs0A12ui0xXkQhzvg6fxXwWTAHZLkoYV.4deLq", first_name="administrator")
        flag = Flag(flag="FLAG{sQL_INj3c7!0n_m@ST3R}")
        admin_note = Note(data="How did you find my note?", date=datetime.now(), user_id=1)

        mysql.session.add(admin)
        mysql.session.add(flag)
        mysql.session.add(admin_note)
        mysql.session.commit()
    
    return app

# initialize the schema
def create_database():
    """Create the database if it does not exist."""
    connection = pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        port=int(Config.MYSQL_PORT)
    )
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DATABASE};")
    connection.close()
