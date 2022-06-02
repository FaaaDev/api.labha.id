from email.policy import default
from enum import unique
from main.shared.shared import db


class OrdpbHdb(db.Model):
    __table_args__ = {'schema': 'AP'}
    __tablename__ = 'ORDPBHDB'

    id = db.Column(db.Integer, primary_key=True)
    ord_code = db.Column(db.String(255), unique=True)
    ord_date = db.Column(db.TIMESTAMP)
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
    status = db.Column(db.Integer, default=0)
    print = db.Column(db.Integer, default=0)

    def __init__(self, ord_code, ord_date, faktur, po_id, dep_id, sup_id, top, due_date, split_inv, prod_disc, jasa_disc, total_disc, status, print):
        self.ord_code = ord_code
        self.ord_date = ord_date
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
        self.status = status
        self.print = print
