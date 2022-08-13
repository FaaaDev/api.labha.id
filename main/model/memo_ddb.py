from enum import unique
from main.shared.shared import db

class MemoDdb(db.Model):
    __table_args__ = {'schema': 'GL'}
    __tablename__ = 'MEMODDB'

    id = db.Column(db.Integer, primary_key=True)
    mcode = db.Column(db.Integer)
    acc_id = db.Column(db.Integer)
    dep_id = db.Column(db.Integer)
    currency = db.Column(db.Integer)
    dbcr = db.Column(db.String(10))
    amnt = db.Column(db.Integer)    
    amnh = db.Column(db.Integer)    
    desc = db.Column(db.Text)    

    def __init__(self, mcode, acc_id, dep_id, currency, dbcr, amnt, amnh, desc ):
        self.mcode = mcode
        self.acc_id = acc_id
        self.dep_id = dep_id
        self.currency = currency
        self.dbcr = dbcr
        self.amnt = amnt
        self.amnh = amnh
        self.desc = desc