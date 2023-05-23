from enum import unique
from ..shared.shared import db

class NeracaMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'NERACAMDB'

    id = db.Column(db.Integer, primary_key=True)
    cp_id = db.Column(db.Integer)
    cur = db.Column(db.String(255))
    fixed = db.Column(db.String(255))
    depr = db.Column(db.String(255))
    ap = db.Column(db.String(255))
    cap = db.Column(db.String(255))
    user_id = db.Column(db.Integer)
    

    def __init__(self, cp_id, cur, fixed, depr, ap, cap, user_id):
        self.cp_id = cp_id
        self.cur = cur
        self.fixed = fixed
        self.depr = depr
        self.ap = ap
        self.cap = cap
        self.user_id = user_id