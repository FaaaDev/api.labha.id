from enum import unique
from main.shared.shared import db

class PoMdb(db.Model):
    __table_args__ = {'schema': 'AP'}
    __tablename__ = 'PORDHDB'

    id = db.Column(db.Integer, primary_key=True)
    req_code = db.Column(db.String(255), unique=True)
    req_date = db.Column(db.DATE)
    preq_id = db.Column(db.Integer)
    sup_id = db.Column(db.Text)
    ppn_type = db.Column(db.Boolean)
    top = db.Column(db.Integer)
    due_date = db.Column(db.Text)
    split_inv = db.Column(db.Boolean)
    prod_disc = db.Column(db.Boolean)
    jasa_disc = db.Column(db.Boolean)
    total_disc = db.Column(db.Boolean)
    

    def __init__(self, req_code, req_date, req_dep, req_ket, refrence, ref_sup, ref_ket):
        self.req_code = req_code
        self.req_date = req_date
        self.req_dep = req_dep
        self.req_ket = req_ket
        self.refrence = refrence
        self.ref_sup = ref_sup
        self.ref_ket = ref_ket