from enum import unique
from ..shared.shared import db


class RsprodDdb(db.Model):
    __table_args__ = {'schema': 'AP'}
    __tablename__ = 'RSPRODDDB'

    id = db.Column(db.Integer, primary_key=True)
    ret_id = db.Column(db.Integer)
    prod_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    retur = db.Column(db.Integer)
    price = db.Column(db.Integer)
    disc = db.Column(db.Integer)
    nett_price = db.Column(db.Integer)
    totl = db.Column(db.Integer)
    location = db.Column(db.Integer)

    def __init__(self, ret_id, prod_id, unit_id, retur, price, disc, nett_price, totl, location):
        self.ret_id = ret_id
        self.prod_id = prod_id
        self.unit_id = unit_id
        self.retur = retur
        self.price = price
        self.disc = disc
        self.nett_price = nett_price
        self.totl = totl
        self.location = location
