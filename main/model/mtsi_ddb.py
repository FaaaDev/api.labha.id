import datetime
from main.shared.shared import db


class MtsiDdb(db.Model):
    __table_args__ = {"schema": "INV"}
    __tablename__ = "MTSIDDB"

    id = db.Column(db.Integer, primary_key=True)
    mtsi_id = db.Column(db.Integer)
    prod_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    qty = db.Column(db.Integer)

    def __init__(self, mtsi_id, prod_id, unit_id, qty):
        self.mtsi_id = mtsi_id
        self.prod_id = prod_id
        self.unit_id = unit_id
        self.qty = qty