from email.policy import default
from enum import unique
from main.shared.shared import db


class DordHdb(db.Model):
    __table_args__ = {'schema': 'AP'}
    __tablename__ = 'DORDHDB'

    id = db.Column(db.Integer, primary_key=True)
    do_code = db.Column(db.String(255), unique=True)
    do_date = db.Column(db.TIMESTAMP)
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

    def __init__(self, do_code, do_date, dep_id, sup_id, top, due_date, split_inv, prod_disc, jasa_disc, total_disc, status, print):
        self.do_code = do_code
        self.do_date = do_date
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
