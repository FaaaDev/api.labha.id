from enum import unique
from main.shared.shared import db

class PreqMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'PREQMDB'

    id = db.Column(db.Integer, primary_key=True)
    req_code = db.Column(db.String(255), unique=True)
    req_date = db.Column(db.String(255))
    req_dep = db.Column(db.Integer)
    req_ket = db.Column(db.Text)
    refrence = db.Column(db.Boolean)
    ref_sup = db.Column(db.Integer)
    ref_ket = db.Column(db.Text)
    

    def __init__(self, req_code, req_date, req_dep, req_ket, refrence, ref_sup, ref_ket):
        self.req_code = req_code
        self.req_date = req_date
        self.req_dep = req_dep
        self.req_ket = req_ket
        self.refrence = refrence
        self.ref_sup = ref_sup
        self.ref_ket = ref_ket