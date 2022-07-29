import datetime
from main.shared.shared import db

class FmtrlDdb(db.Model):
    __table_args__ = {'schema': 'PROD'}
    __tablename__ = 'FMTRLDDB'

    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer)
    prod_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    qty = db.Column(db.Float)
    price = db.Column(db.Float)
    

    def __init__(self, form_id, prod_id, unit_id, qty, price):
        self.form_id = form_id
        self.prod_id = prod_id
        self.unit_id = unit_id
        self.qty = qty
        self.price = price