import os

class Config:
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'password123'
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = '3306'
    MYSQL_DATABASE = 'test_db'
    
    SECRET_KEY = 'Admin@123' # os.getenv('APP_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/'
    SQLALCHEMY_TRACK_MODIFICATIONS = False