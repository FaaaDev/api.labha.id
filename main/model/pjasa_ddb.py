from enum import unique
from ..shared.shared import db


class PjasaDdb(db.Model):
    __table_args__ = {'schema': 'AP'}
    __tablename__ = 'PJASADDB'

    id = db.Column(db.Integer, primary_key=True)
    po_id = db.Column(db.Integer)
    preq_id = db.Column(db.Integer)
    rjasa_id = db.Column(db.Integer)
    sup_id = db.Column(db.Integer)
    jasa_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    order = db.Column(db.Integer)
    price = db.Column(db.Float)
    disc = db.Column(db.Float)
    total = db.Column(db.Float)

    def __init__(self, po_id, preq_id, rjasa_id, sup_id, jasa_id, unit_id, order, price, disc, total):
        self.po_id = po_id
        self.preq_id = preq_id
        self.rjasa_id = rjasa_id
        self.sup_id = sup_id
        self.jasa_id = jasa_id
        self.unit_id = unit_id
        self.order = order
        self.price = price
        self.disc = disc
        self.total = total
