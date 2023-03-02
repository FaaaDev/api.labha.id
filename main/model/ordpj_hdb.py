from email.policy import default
from enum import unique

from main.shared.shared import db


class OrdpjHdb(db.Model):
    __table_args__ = {"schema": "AR"}
    __tablename__ = "ORDPJHDB"

    id = db.Column(db.Integer, primary_key=True)
    ord_code = db.Column(db.String(255), unique=True)
    ord_date = db.Column(db.TIMESTAMP)
    no_doc = db.Column(db.String(255))
    doc_date = db.Column(db.TIMESTAMP(timezone=False))
    so_id = db.Column(db.Integer)
    invoice = db.Column(db.Boolean)
    pel_id = db.Column(db.Integer)
    ppn_type = db.Column(db.Integer)
    sub_addr = db.Column(db.Boolean)
    sub_id = db.Column(db.Integer)
    slsm_id = db.Column(db.Integer)
    surat_jalan = db.Column(db.Integer)
    req_date = db.Column(db.TIMESTAMP)
    top = db.Column(db.Integer)
    due_date = db.Column(db.TIMESTAMP)
    split_inv = db.Column(db.Boolean)
    prod_disc = db.Column(db.Integer)
    jasa_disc = db.Column(db.Integer)
    total_disc = db.Column(db.Integer)
    total_b = db.Column(db.Float)
    total_bayar = db.Column(db.Float)
    status = db.Column(db.Integer, default=0)
    print = db.Column(db.Integer, default=0)

    def __init__(
        self,
        ord_code,
        ord_date,
        no_doc,
        doc_date,
        so_id,
        invoice,
        pel_id,
        ppn_type,
        sub_addr,
        sub_id,
        slsm_id,
        surat_jalan,
        req_date,
        top,
        due_date,
        split_inv,
        prod_disc,
        jasa_disc,
        total_disc,
        total_b,
        total_bayar,
        status,
        print,
    ):
        self.ord_code = ord_code
        self.ord_date = ord_date
        self.no_doc = no_doc
        self.doc_date = doc_date
        self.so_id = so_id
        self.invoice = invoice
        self.pel_id = pel_id
        self.ppn_type = ppn_type
        self.sub_addr = sub_addr
        self.sub_id = sub_id
        self.slsm_id = slsm_id
        self.surat_jalan = surat_jalan
        self.req_date = req_date
        self.top = top
        self.due_date = due_date
        self.split_inv = split_inv
        self.prod_disc = prod_disc
        self.jasa_disc = jasa_disc
        self.total_disc = total_disc
        self.total_b = total_b
        self.total_bayar = total_bayar
        self.status = status
        self.print = print
