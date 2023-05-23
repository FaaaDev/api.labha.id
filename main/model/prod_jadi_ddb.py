import datetime
from main.shared.shared import db

class PJadiDdb(db.Model):
    __table_args__ = {'schema': 'PROD'}
    __tablename__ = 'PJADIDDB'

    id = db.Column(db.Integer, primary_key=True)
    pp_id = db.Column(db.Integer)
    prod_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    loc_id = db.Column(db.Integer)
    qty = db.Column(db.Integer)
    

    def __init__(self, pp_id, prod_id, unit_id, loc_id, qty):
        self.pp_id = pp_id
        self.prod_id = prod_id
        self.unit_id = unit_id
        self.loc_id = loc_id
        self.qty = qty
       