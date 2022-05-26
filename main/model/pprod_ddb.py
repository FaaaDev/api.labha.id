from enum import unique
from main.shared.shared import db


class PprodDdb(db.Model):
    __table_args__ = {'schema': 'AP'}
    __tablename__ = 'PPRODDDB'

    id = db.Column(db.Integer, primary_key=True)
    po_id = db.Column(db.Integer)
    preq_id = db.Column(db.Integer)
    preq_id = db.Column(db.Integer)
    rprod_id = db.Column(db.Integer)
    prod_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    order = db.Column(db.Integer)
    price = db.Column(db.Float)
    disc = db.Column(db.Float)
    nett_price = db.Column(db.Float)
    total = db.Column(db.Float)

    def __init__(self, po_id, preq_id, rprod_id, prod_id, unit_id, order, price, disc, nett_price, total):
        self.po_id = po_id
        self.preq_id = preq_id
        self.rprod_id = rprod_id
        self.prod_id = prod_id
        self.unit_id = unit_id
        self.order = order
        self.price = price
        self.disc = disc
        self.nett_price = nett_price
        self.total = total
