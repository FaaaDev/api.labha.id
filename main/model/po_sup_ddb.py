from enum import unique
from main.shared.shared import db

class PoSupDdb(db.Model):
    __table_args__ = {'schema': 'AP'}
    __tablename__ = 'POSUPDDB'

    id = db.Column(db.Integer, primary_key=True)
    po_id = db.Column(db.Integer)
    sup_id = db.Column(db.Integer)
    prod_id = db.Column(db.Integer)
    price = db.Column(db.Float)
    

    def __init__(self, po_id, sup_id, prod_id, price):
        self.po_id = po_id
        self.sup_id = sup_id
        self.prod_id = prod_id
        self.price = price