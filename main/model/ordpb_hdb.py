import datetime
from email.policy import default
from enum import unique
from main.shared.shared import db


class OrdpbHdb(db.Model):
    __table_args__ = {"schema": "AP"}
    __tablename__ = "ORDPBHDB"

    id = db.Column(db.Integer, primary_key=True)
    ord_code = db.Column(db.String(255), unique=True)
    ord_date = db.Column(db.TIMESTAMP)
    no_doc = db.Column(db.String(255))
    doc_date = db.Column(
        db.TIMESTAMP(timezone=False), default=datetime.datetime.utcnow()
    )
    invoice = db.Column(db.Boolean)
    faktur = db.Column(db.Boolean)
    po_id = db.Column(db.Integer)
    dep_id = db.Column(db.Integer)
    sup_id = db.Column(db.Integer)
    top = db.Column(db.Integer)
    due_date = db.Column(db.TIMESTAMP)
    split_inv = db.Column(db.Boolean)
    prod_disc = db.Column(db.Integer)
    jasa_disc = db.Column(db.Integer)
    total_disc = db.Column(db.Integer)
    total_b = db.Column(db.Integer)
    total_bayar = db.Column(db.Integer)
    ns = db.Column(db.Boolean)
    same_sup = db.Column(db.Boolean)
    status = db.Column(db.Integer, default=0)
    print = db.Column(db.Integer, default=0)
    post = db.Column(db.Boolean, default=False)
    closing = db.Column(db.Boolean, default=False)

    def __init__(
        self,
        ord_code,
        ord_date,
        no_doc,
        doc_date,
        invoice,
        faktur,
        po_id,
        dep_id,
        sup_id,
        top,
        due_date,
        split_inv,
        prod_disc,
        jasa_disc,
        total_disc,
        total_b,
        total_bayar,
        ns,
        same_sup,
        status,
        print,
    ):
        self.ord_code = ord_code
        self.ord_date = ord_date
        self.no_doc = no_doc
        self.doc_date = doc_date
        self.invoice = invoice
        self.faktur = faktur
        self.po_id = po_id
        self.dep_id = dep_id
        self.sup_id = sup_id
        self.top = top
        self.due_date = due_date
        self.split_inv = split_inv
        self.prod_disc = prod_disc
        self.jasa_disc = jasa_disc
        self.total_disc = total_disc
        self.total_b = total_b
        self.total_bayar = total_bayar
        self.ns = ns
        self.same_sup = same_sup
        self.status = status
        self.print = print
