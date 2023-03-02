from enum import unique
from main.shared.shared import db


class JprodDdb(db.Model):
    __table_args__ = {"schema": "AR"}
    __tablename__ = "JPRODDDB"

    id = db.Column(db.Integer, primary_key=True)
    pj_id = db.Column(db.Integer)
    sprod_id = db.Column(db.Integer)
    prod_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    location = db.Column(db.Integer)
    order = db.Column(db.Integer)
    price = db.Column(db.Float)
    disc = db.Column(db.Integer)
    nett_price = db.Column(db.Float)
    total_fc = db.Column(db.Float)
    total = db.Column(db.Float)

    def __init__(
        self,
        pj_id,
        sprod_id,
        prod_id,
        unit_id,
        location,
        order,
        price,
        disc,
        nett_price,
        total_fc,
        total,
    ):
        self.pj_id = pj_id
        self.sprod_id = sprod_id
        self.prod_id = prod_id
        self.unit_id = unit_id
        self.location = location
        self.order = order
        self.price = price
        self.disc = disc
        self.nett_price = nett_price
        self.total_fc = total_fc
        self.total = total
