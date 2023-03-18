from email.policy import default
from enum import unique
from main.shared.shared import db


class PreqMdb(db.Model):
    __table_args__ = {"schema": "AP"}
    __tablename__ = "PREQHDB"

    id = db.Column(db.Integer, primary_key=True)
    req_code = db.Column(db.String(255), unique=True)
    req_date = db.Column(db.TIMESTAMP)
    req_dep = db.Column(db.Integer)
    req_ket = db.Column(db.Text)
    refrence = db.Column(db.Boolean)
    ref_sup = db.Column(db.Integer)
    ref_ket = db.Column(db.Text)
    ns = db.Column(db.Boolean)
    status = db.Column(db.Integer, default=0)

    def __init__(
        self,
        req_code,
        req_date,
        req_dep,
        req_ket,
        refrence,
        ref_sup,
        ref_ket,
        ns,
        status,
    ):
        self.req_code = req_code
        self.req_date = req_date
        self.req_dep = req_dep
        self.req_ket = req_ket
        self.refrence = refrence
        self.ref_sup = ref_sup
        self.ref_ket = ref_ket
        self.ns = ns
        self.status = status
