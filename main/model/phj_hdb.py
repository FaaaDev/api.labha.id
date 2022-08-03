import datetime
from main.shared.shared import db

class PhjHdb(db.Model):
    __table_args__ = {'schema': 'PROD'}
    __tablename__ = 'PHJHDB'

    id = db.Column(db.Integer, primary_key=True)
    phj_code = db.Column(db.String(255), unique=True)
    phj_date = db.Column(db.TIMESTAMP(timezone=False), default=datetime.datetime.utcnow())
    batch_id = db.Column(db.Integer)
    

    def __init__(self, phj_code, phj_date, batch_id):
        self.phj_code = phj_code
        self.phj_date = phj_date
        self.batch_id = batch_id
       