import datetime
from ..shared.shared import db

class PbbHdb(db.Model):
    __table_args__ = {'schema': 'PROD'}
    __tablename__ = 'PBBHDB'

    id = db.Column(db.Integer, primary_key=True)
    pbb_code = db.Column(db.String(255), unique=True)
    pbb_name = db.Column(db.String(255))
    pbb_date = db.Column(db.TIMESTAMP(timezone=False), default=datetime.datetime.utcnow())
    batch_id = db.Column(db.Integer)
    acc_cred = db.Column(db.Integer)
    

    def __init__(self, pbb_code, pbb_name, pbb_date, batch_id, acc_cred):
        self.pbb_code = pbb_code
        self.pbb_name = pbb_name
        self.pbb_date = pbb_date
        self.acc_cred = acc_cred
        self.batch_id = batch_id
       