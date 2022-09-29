from flask_sqlalchemy import SQLAlchemy
from main.shared.shared import db

class DepaMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'DEPAMDB'

    id = db.Column(db.Integer, primary_key=True)
    depaname = db.Column(db.String(100))
    

    def __init__(self, name):
        self.depaname = name