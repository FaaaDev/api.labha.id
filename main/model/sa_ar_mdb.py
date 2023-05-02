from enum import unique
from ..shared.shared import db

class SaldoARMdb(db.Model):
    __table_args__ = {'schema': 'AR'}
    __tablename__ = 'SLDARMDB'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), unique=True)
    date = db.Column(db.TIMESTAMP)
    due_date = db.Column(db.TIMESTAMP)
    cus_id = db.Column(db.Integer)
    type = db.Column(db.String(5))
    nilai = db.Column(db.Float)
    user_id = db.Column(db.Integer)
    

    def __init__(self, code, date, due_date, cus_id, type, nilai, user_id):
        self.code = code
        self.date = date
        self.due_date = due_date
        self.cus_id = cus_id
        self.type = type
        self.nilai = nilai
        self.user_id = user_id