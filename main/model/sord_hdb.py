from email.policy import default
from enum import unique
from main.shared.shared import db


class SordHdb(db.Model):
    __table_args__ = {'schema': 'AR'}
    __tablename__ = 'SORDHDB'

    id = db.Column(db.Integer, primary_key=True)
    so_code = db.Column(db.String(255), unique=True)
    so_date = db.Column(db.TIMESTAMP)
    pel_id = db.Column(db.Integer)
    ppn_type = db.Column(db.String(255))
    sub_addr = db.Column(db.Boolean)
    sub_id = db.Column(db.Integer)
    req_date = db.Column(db.TIMESTAMP)
    top = db.Column(db.Integer)
    due_date = db.Column(db.TIMESTAMP)
    split_inv = db.Column(db.Boolean)
    prod_disc = db.Column(db.Integer)
    jasa_disc = db.Column(db.Integer)
    total_disc = db.Column(db.Integer)
    status = db.Column(db.Integer, default=0)
    print = db.Column(db.Integer, default=0)

    def __init__(self,
                 so_code,
                 so_date,
                 pel_id,
                 ppn_type,
                 sub_addr,
                 sub_id,
                 req_date,
                 top,
                 due_date,
                 split_inv,
                 prod_disc,
                 jasa_disc,
                 total_disc,
                 status,
                 print
                 ):
        self.so_code = so_code
        self.so_date = so_date
        self.pel_id = pel_id
        self.ppn_type = ppn_type
        self.sub_addr = sub_addr
        self.sub_id = sub_id
        self.req_date = req_date
        self.top = top
        self.due_date = due_date
        self.split_inv = split_inv
        self.prod_disc = prod_disc
        self.jasa_disc = jasa_disc
        self.total_disc = total_disc
        self.status = status
        self.print = print
