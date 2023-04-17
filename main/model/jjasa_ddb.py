from enum import unique
from ..shared.shared import db


class JjasaDdb(db.Model):
    __table_args__ = {"schema": "AR"}
    __tablename__ = "JJASADDB"

    id = db.Column(db.Integer, primary_key=True)
    pj_id = db.Column(db.Integer)
    sup_id = db.Column(db.Integer)
    jasa_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    order = db.Column(db.Integer)
    price = db.Column(db.Float)
    disc = db.Column(db.Integer)
    total_fc = db.Column(db.Float)
    total = db.Column(db.Float)

    def __init__(
        self, pj_id, sup_id, jasa_id, unit_id, order, price, disc, total_fc, total
    ):
        self.pj_id = pj_id
        self.sup_id = sup_id
        self.jasa_id = jasa_id
        self.unit_id = unit_id
        self.order = order
        self.price = price
        self.disc = disc
        self.total_fc = total_fc
        self.total = total
