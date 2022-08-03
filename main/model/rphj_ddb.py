import datetime
from main.shared.shared import db

class RphjDdb(db.Model):
    __table_args__ = {'schema': 'PROD'}
    __tablename__ = 'RPHJDDB'

    id = db.Column(db.Integer, primary_key=True)
    phj_id = db.Column(db.Integer)
    prod_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    qty = db.Column(db.Float)
    

    def __init__(self, phj_id, prod_id, unit_id, qty):
        self.phj_id = phj_id
        self.prod_id = prod_id
        self.unit_id = unit_id
        self.qty = qty