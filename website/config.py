import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MYSQL_USER = os.getenv('DB_USER', 'root')
    MYSQL_PASSWORD = os.getenv('DB_PASSWORD', 'password123')
    MYSQL_HOST = os.getenv('DB_HOST', 'db')
    MYSQL_PORT = os.getenv('DB_PORT', '3306')
    MYSQL_DATABASE = os.getenv('DB_NAME', 'test_db')

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv('APP_SECRET_KEY')
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False')
    SESSION_COOKIE_HTTPONLY = os.getenv('SESSION_COOKIE_HTTPONLY', 'False')

    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')
    print(UPLOAD_FOLDER)

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)