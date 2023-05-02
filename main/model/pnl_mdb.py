from enum import unique
from ..shared.shared import db

class PnlMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'PNLMDB'

    id = db.Column(db.Integer, primary_key=True)
    cp_id = db.Column(db.Integer)
    klasi = db.Column(db.String(255))
    user_id = db.Column(db.Integer)
    

    def __init__(self, cp_id, klasi, user_id):
        self.cp_id = cp_id
        self.klasi = klasi
        self.user_id = user_id