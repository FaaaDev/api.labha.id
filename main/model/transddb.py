from enum import unique
from main.shared.shared import db


class TransDdb(db.Model):
    __table_args__ = {'schema': 'GL'}
    __tablename__ = 'TRANSDDB'

    id = db.Column(db.Integer, primary_key=True)
    trx_code = db.Column(db.String(255))
    trx_date = db.Column(db.TIMESTAMP)
    acc_id = db.Column(db.Integer)
    ccost_id = db.Column(db.Integer)
    proj_id = db.Column(db.Integer)
    acq_date = db.Column(db.TIMESTAMP)
    cur_id = db.Column(db.Integer)
    cur_rate = db.Column(db.Integer)
    trx_vala = db.Column(db.Integer)
    trx_amnt = db.Column(db.Integer)
    trx_dbcr = db.Column(db.String(2))
    trx_desc = db.Column(db.Text)
    gen_post = db.Column(db.Integer)
    post_date = db.Column(db.TIMESTAMP)

    def __init__(self,
                 trx_code,
                 trx_date,
                 acc_id,
                 ccost_id,
                 proj_id,
                 acq_date,
                 cur_id,
                 cur_rate,
                 trx_vala,
                 trx_amnt,
                 trx_dbcr,
                 trx_desc,
                 gen_post,
                 post_date):
        self.trx_code = trx_code
        self.trx_date = trx_date
        self.acc_id = acc_id
        self.ccost_id = ccost_id
        self.proj_id = proj_id
        self.acq_date = acq_date
        self.cur_id = cur_id
        self.cur_rate = cur_rate
        self.trx_vala = trx_vala
        self.trx_amnt = trx_amnt
        self.trx_dbcr = trx_dbcr
        self.trx_desc = trx_desc
        self.gen_post = gen_post
        self.post_date = post_date
