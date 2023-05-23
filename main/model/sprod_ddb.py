from enum import unique
from ..shared.shared import db


class SprodDdb(db.Model):
    __table_args__ = {'schema': 'AR'}
    __tablename__ = 'SPRODDDB'

    id = db.Column(db.Integer, primary_key=True)
    so_id = db.Column(db.Integer)
    prod_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    location = db.Column(db.Integer)
    request = db.Column(db.Integer)
    order = db.Column(db.Integer)
    remain = db.Column(db.Integer)
    price = db.Column(db.Integer)
    disc = db.Column(db.Integer)
    nett_price = db.Column(db.Integer)
    total = db.Column(db.Integer)

    def __init__(self, so_id, prod_id, unit_id, location, request, order, remain, price, disc, nett_price, total):
        self.so_id = so_id
        self.prod_id = prod_id
        self.unit_id = unit_id
        self.location = location
        self.request = request
        self.order = order
        self.remain = remain
        self.price = price
        self.disc = disc
        self.nett_price = nett_price
        self.total = total
