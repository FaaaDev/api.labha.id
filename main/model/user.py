from flask_sqlalchemy import SQLAlchemy
from main.shared.shared import db

class User(db.Model):
    __tablename__ = 'HR_USER'

    uid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(200), unique = True)
    image = db.Column(db.String(200))
    dob = db.Column(db.String(100))

    def __init__(self, username, phone, email, image, dob):
        self.username = username
        self.email = email
        self.phone = phone
        self.image = image
        self.dob = dob