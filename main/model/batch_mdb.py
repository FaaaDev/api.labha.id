import datetime
from main.shared.shared import db

class BatchMdb(db.Model):
    __table_args__ = {'schema': 'PROD'}
    __tablename__ = 'BATCHMDB'

    id = db.Column(db.Integer, primary_key=True)
    bcode = db.Column(db.String(255), unique=True)
    batch_date = db.Column(db.TIMESTAMP(timezone=False), default=datetime.datetime.utcnow())
    plan_id = db.Column(db.Integer)
    dep_id = db.Column(db.Integer)
    

    def __init__(self, bcode, batch_date, plan_id, dep_id):
        self.bcode = bcode
        self.batch_date = batch_date
        self.plan_id = plan_id
        self.dep_id = dep_id