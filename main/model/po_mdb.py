from email.policy import default
from enum import unique
from main.shared.shared import db


class PoMdb(db.Model):
    __table_args__ = {'schema': 'AP'}
    __tablename__ = 'PORDHDB'

    id = db.Column(db.Integer, primary_key=True)
    po_code = db.Column(db.String(255), unique=True)
    po_date = db.Column(db.TIMESTAMP)
    preq_id = db.Column(db.Integer)
    sup_id = db.Column(db.Integer)
    ppn_type = db.Column(db.String(255))
    top = db.Column(db.Integer)
    due_date = db.Column(db.TIMESTAMP)
    split_inv = db.Column(db.Boolean)
    prod_disc = db.Column(db.Float)
    jasa_disc = db.Column(db.Float)
    total_disc = db.Column(db.Float)
    status = db.Column(db.Integer, default=0)
    print = db.Column(db.Integer, default=0)

    def __init__(self, po_code, po_date, preq_id, sup_id, ppn_type, top, due_date, split_inv, prod_disc, jasa_disc, total_disc, status, print):
        self.po_code = po_code
        self.po_date = po_date
        self.preq_id = preq_id
        self.sup_id = sup_id
        self.ppn_type = ppn_type
        self.top = top
        self.due_date = due_date
        self.split_inv = split_inv
        self.prod_disc = prod_disc
        self.jasa_disc = jasa_disc
        self.total_disc = total_disc
        self.status = status
        self.print = print