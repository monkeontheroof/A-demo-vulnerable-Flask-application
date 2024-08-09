import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

mysql = SQLAlchemy()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password123@localhost/test_db?charest=utf8mb4'
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    mysql.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    return app

def create_database(app):
    if not os.path.exists('website/test_db'):
        mysql.create_all(app)
        print('Created Database!')