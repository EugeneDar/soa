from flask_sqlalchemy import SQLAlchemy
from datetime import date

MAX_FIELD_SIZE = 100

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(MAX_FIELD_SIZE), unique=True, nullable=False)
    password = db.Column(db.String(MAX_FIELD_SIZE), nullable=False)
    name = db.Column(db.String(MAX_FIELD_SIZE))
    surname = db.Column(db.String(MAX_FIELD_SIZE))
    birthdate = db.Column(db.Date)
    email = db.Column(db.String(MAX_FIELD_SIZE), unique=True)
    phone = db.Column(db.String(MAX_FIELD_SIZE), unique=True)

    def init(self, username, password, name=None, surname=None, birthdate=None, email=None, phone=None):
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        self.email = email
        self.phone = phone
