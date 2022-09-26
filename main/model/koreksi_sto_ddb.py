import datetime
from main.shared.shared import db


class KorStoDdb(db.Model):
    __table_args__ = {"schema": "INV"}
    __tablename__ = "KORSTODDB"

    id = db.Column(db.Integer, primary_key=True)
    kor_id = db.Column(db.Integer)
    prod_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    location = db.Column(db.Integer)
    dbcr = db.Column(db.String(10))
    qty = db.Column(db.Integer)

    def __init__(self, kor_id, prod_id, unit_id, location, dbcr, qty):
        self.kor_id = kor_id
        self.prod_id = prod_id
        self.unit_id = unit_id
        self.location = location
        self.dbcr = dbcr
        self.qty = qty
