from enum import unique
from main.shared.shared import db

class PajakMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'PAJAKMDB'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    nilai = db.Column(db.String(10))
    

    def __init__(self, code, name, nilai):
        self.code = code
        self.name = name
        self.nilai = nilai