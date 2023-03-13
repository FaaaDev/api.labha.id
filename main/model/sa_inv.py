from enum import unique
from main.shared.shared import db

class SaldoInvMdb(db.Model):
    __table_args__ = {'schema': 'INV'}
    __tablename__ = 'SLDAMDB'

    id = db.Column(db.Integer, primary_key=True)
    loc_id = db.Column(db.Integer)
    prod_id = db.Column(db.Integer)
    qty = db.Column(db.Integer)
    nilai = db.Column(db.Integer)
    total = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    

    def __init__(self, loc_id, prod_id, qty, nilai, total, user_id):
        self.loc_id = loc_id
        self.prod_id = prod_id
        self.qty = qty
        self.nilai = nilai
        self.total = total
        self.user_id = user_id