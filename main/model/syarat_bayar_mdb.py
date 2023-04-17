from enum import unique
from unicodedata import name
from ..shared.shared import db

class RulesPayMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'RPAYMENTMDB'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    day = db.Column(db.Integer)
    ket = db.Column(db.Text)
    

    def __init__(self, name, day, ket):
        self.name = name
        self.day = day
        self.ket = ket