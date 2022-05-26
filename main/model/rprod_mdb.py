from enum import unique
from main.shared.shared import db


class RprodMdb(db.Model):
    __table_args__ = {'schema': 'AP'}
    __tablename__ = 'RPRODDDB'

    id = db.Column(db.Integer, primary_key=True)
    preq_id = db.Column(db.Integer)
    prod_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    request = db.Column(db.Integer)
    remain = db.Column(db.Integer)

    def __init__(self, preq_id, prod_id, unit_id, request, remain):
        self.preq_id = preq_id
        self.prod_id = prod_id
        self.unit_id = unit_id
        self.request = request
        self.remain = remain
