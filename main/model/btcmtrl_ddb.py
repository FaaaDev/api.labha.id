import datetime
from main.shared.shared import db

class BtcmtrlDdb(db.Model):
    __table_args__ = {'schema': 'PROD'}
    __tablename__ = 'BMTRLDDB'

    id = db.Column(db.Integer, primary_key=True)
    btc_id = db.Column(db.Integer)
    prod_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    qty = db.Column(db.Float)
    qty_f = db.Column(db.Float)
    price = db.Column(db.Float)
    t_price = db.Column(db.Float)
    

    def __init__(self, btc_id, prod_id, unit_id, qty, qty_f, price, t_price):
        self.btc_id = btc_id
        self.prod_id = prod_id
        self.unit_id = unit_id
        self.qty = qty
        self.qty_f = qty_f
        self.price = price
        self.t_price = t_price