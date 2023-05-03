import datetime
from ..shared.shared import db


class MtsiDdb(db.Model):
    __table_args__ = {"schema": "INV"}
    __tablename__ = "MTSIDDB"

    id = db.Column(db.Integer, primary_key=True)
    mtsi_id = db.Column(db.Integer)
    prod_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    qty = db.Column(db.Float)
    qty_terima = db.Column(db.Float)

    def __init__(self, mtsi_id, prod_id, unit_id, qty, qty_terima):
        self.mtsi_id = mtsi_id
        self.prod_id = prod_id
        self.unit_id = unit_id
        self.qty = qty
        self.qty_terima = qty_terima
