import datetime
from main.shared.shared import db

class PlmchDdb(db.Model):
    __table_args__ = {'schema': 'PROD'}
    __tablename__ = 'PLMCHDDB'

    id = db.Column(db.Integer, primary_key=True)
    pl_id = db.Column(db.Integer)
    mch_id = db.Column(db.Integer)

    def __init__(self, pl_id, mch_id):
        self.pl_id = pl_id
        self.mch_id = mch_id
        