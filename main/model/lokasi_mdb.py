from enum import unique
from ..shared.shared import db

class LocationMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'LOCATMDB'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    address = db.Column(db.Text)
    desc = db.Column(db.Text)
    

    def __init__(self, code, name, address, desc):
        self.code = code
        self.name = name
        self.address = address
        self.desc = desc