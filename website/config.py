import os

class Config:
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'password123'
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = '3306'
    MYSQL_DATABASE = 'test_db'

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'Admin@123' # os.getenv('APP_SECRET_KEY')
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')
    print(UPLOAD_FOLDER)

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)