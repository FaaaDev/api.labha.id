from enum import unique
from main.shared.shared import db

class UnitMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'UNITMDB'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255))
    name = db.Column(db.String(255))
    type = db.Column(db.String(10))
    desc = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    qty = db.Column(db.Integer)
    u_from = db.Column(db.Integer)
    u_to= db.Column(db.Integer)
    

    def __init__(self, code, name, type, desc, active, qty, u_from, u_to):
        self.code = code
        self.name = name
        self.type = type
        self.desc = desc
        self.active = active
        self.qty = qty
        self.u_from = u_from
        self.u_to = u_to