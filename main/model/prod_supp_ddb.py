from enum import unique
from main.shared.shared import db


class ProdSupDdb(db.Model):
    __table_args__ = {"schema": "master"}
    __tablename__ = "PRODSUPDDB"

    id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.Integer)
    sup_id = db.Column(db.Integer)

    def __init__(
        self,
        prod_id,
        sup_id,
    ):
        self.prod_id = prod_id
        self.sup_id = sup_id
