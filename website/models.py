from . import mysql as db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(150), default=func.now())
    user_id = db.Column(db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Note('id': '{self.id}', 'user_id': '{self.user_id}' , 'date': '{self.date}, 'data': '{self.data}')"

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    
class Flag(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    flag = db.Column(db.String(256), unique=True)

    