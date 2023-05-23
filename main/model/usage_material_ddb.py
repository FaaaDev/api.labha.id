import datetime
from main.shared.shared import db

class UsageMatDdb(db.Model):
    __table_args__ = {'schema': 'PROD'}
    __tablename__ = 'MATERIALDDB'

    id = db.Column(db.Integer, primary_key=True)
    um_id = db.Column(db.Integer)
    prod_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    qty = db.Column(db.Float)
    

    def __init__(self, um_id, prod_id, unit_id, qty):
        self.um_id = um_id
        self.prod_id = prod_id
        self.unit_id = unit_id
        self.qty = qty