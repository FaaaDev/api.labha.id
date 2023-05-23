import datetime
from ..shared.shared import db

class OvhDdb(db.Model):
    __table_args__ = {'schema': 'PROD'}
    __tablename__ = 'OVHDDB'

    id = db.Column(db.Integer, primary_key=True)
    pbb_id = db.Column(db.Integer)
    acc_id = db.Column(db.Integer)
    

    def __init__(self, pbb_id, acc_id):
        self.pbb_id = pbb_id
        self.acc_id = acc_id