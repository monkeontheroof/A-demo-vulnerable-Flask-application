import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from website.config import Config
import pymysql
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

mysql = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    
    app.config.from_object(Config)

    app.config['SQLALCHEMY_DATABASE_URI'] += Config.MYSQL_DATABASE + '?charset=utf8mb4'
    
    mysql.init_app(app)
    bcrypt.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    
    create_database()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    with app.app_context():
        mysql.create_all()

    return app

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