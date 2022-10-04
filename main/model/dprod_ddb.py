from enum import unique
from main.shared.shared import db


class DprodDdb(db.Model):
    __table_args__ = {'schema': 'AP'}
    __tablename__ = 'OPRODDDB'

    id = db.Column(db.Integer, primary_key=True)
    ord_id = db.Column(db.Integer)
    pprod_id = db.Column(db.Integer)
    prod_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    order = db.Column(db.Integer)
    price = db.Column(db.Integer)
    disc = db.Column(db.Integer)
    location = db.Column(db.Integer)
    nett_price = db.Column(db.Integer)
    total = db.Column(db.Integer)

    def __init__(self,
                 ord_id,
                 pprod_id,
                 prod_id,
                 unit_id,
                 order,
                 price,
                 disc,
                 location,
                 nett_price,
                 total):
        self.ord_id = ord_id
        self.pprod_id = pprod_id
        self.prod_id = prod_id
        self.unit_id = unit_id
        self.order = order
        self.price = price
        self.disc = disc
        self.location = location
        self.nett_price = nett_price
        self.total = total
