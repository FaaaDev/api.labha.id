from enum import unique
from main.shared.shared import db


class RjasaMdb(db.Model):
    __table_args__ = {'schema': 'AP'}
    __tablename__ = 'RJASADDB'

    id = db.Column(db.Integer, primary_key=True)
    preq_id = db.Column(db.Integer)
    sup_id = db.Column(db.Integer)
    jasa_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    qty = db.Column(db.Integer)
    price = db.Column(db.Integer)
    disc = db.Column(db.Integer)
    total = db.Column(db.Integer)

    def __init__(self, preq_id, sup_id, jasa_id, unit_id, qty, price, disc, total):
        self.preq_id = preq_id
        self.sup_id = sup_id
        self.jasa_id = jasa_id
        self.unit_id = unit_id
        self.qty = qty
        self.price = price
        self.disc = disc
        self.total = total
