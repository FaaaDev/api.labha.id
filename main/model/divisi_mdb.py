from enum import unique
from ..shared.shared import db

class DivisionMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'DVSMDB'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    desc = db.Column(db.Text)
    

    def __init__(self, code, name, desc):
        self.code = code
        self.name = name
        self.desc = desc