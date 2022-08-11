import datetime
from main.shared.shared import db

class RpbbMdb(db.Model):
    __table_args__ = {'schema': 'PROD'}
    __tablename__ = 'RPBBMDB'

    id = db.Column(db.Integer, primary_key=True)
    pl_id = db.Column(db.Integer)
    prod_id = db.Column(db.Integer)
    saldo = db.Column(db.Integer)
    plan = db.Column(db.Integer)
    sisa = db.Column(db.Integer)
    sugestion = db.Column(db.Integer)
    loc_id = db.Column(db.Integer)
    date_created = db.Column(db.TIMESTAMP(timezone=False), default=datetime.datetime.utcnow())
    date_updated = db.Column(db.TIMESTAMP(timezone=False), default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())
    

    def __init__(self, pl_id, prod_id, saldo, plan, sisa, sugestion, loc_id):
        self.pl_id = pl_id
        self.prod_id = prod_id
        self.saldo = saldo
        self.plan = plan
        self.sisa = sisa
        self.sugestion = sugestion
        self.loc_id = loc_id