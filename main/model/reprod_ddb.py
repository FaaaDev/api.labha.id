from enum import unique
from ..shared.shared import db


class ReprodDdb(db.Model):
    __table_args__ = {'schema': 'AP'}
    __tablename__ = 'REPRODDDB'

    id = db.Column(db.Integer, primary_key=True)
    ret_id = db.Column(db.Integer)
    prod_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    retur = db.Column(db.Integer)
    price = db.Column(db.Float)
    disc = db.Column(db.Float)
    nett_price = db.Column(db.Float)
    totl = db.Column(db.Float)
    location = db.Column(db.Integer)
    totl_fc = db.Column(db.Float)

    def __init__(self, ret_id, prod_id, unit_id, retur, price, disc, nett_price, totl, location, totl_fc):
        self.ret_id = ret_id
        self.prod_id = prod_id
        self.unit_id = unit_id
        self.retur = retur
        self.price = price
        self.disc = disc
        self.nett_price = nett_price
        self.totl = totl
        self.location = location
        self.totl_fc = totl_fc
