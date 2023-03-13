from enum import unique
from ..shared.shared import db

class SldAkhir(db.Model):
    __table_args__ = {'schema': 'GL'}
    __tablename__ = 'SLDAKHIR'

    id = db.Column(db.Integer, primary_key=True)
    trx = db.Column(db.String(255), unique=True)
    acc_code = db.Column(db.String(255))
    date = db.Column(db.TIMESTAMP)
    saldo = db.Column(db.Float)
    posting = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)
    

    def __init__(self, trx, acc_code, date, saldo, posting, user_id):
        self.trx = trx
        self.acc_code = acc_code
        self.date = date
        self.saldo = saldo
        self.posting = posting
        self.user_id = user_id