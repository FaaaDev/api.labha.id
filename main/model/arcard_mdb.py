from enum import unique
from main.shared.shared import db


class ArCard(db.Model):
    __table_args__ = {'schema': 'AR'}
    __tablename__ = 'ARCARDMDB'

    id = db.Column(db.Integer, primary_key=True)
    cus_id = db.Column(db.Integer)
    trx_code = db.Column(db.String(255))
    trx_date = db.Column(db.TIMESTAMP)
    trx_due = db.Column(db.TIMESTAMP)
    acq_id = db.Column(db.Integer)
    acq_date = db.Column(db.TIMESTAMP)
    bkt_id = db.Column(db.Integer)
    bkt_date = db.Column(db.TIMESTAMP)
    cur_conv = db.Column(db.Integer)
    trx_dbcr = db.Column(db.String(2))
    trx_type = db.Column(db.String(255))
    pay_type = db.Column(db.String(255))
    trx_amnh = db.Column(db.Integer)
    trx_amnv = db.Column(db.Integer)
    acq_amnh = db.Column(db.Integer)
    acq_amnv = db.Column(db.Integer)
    bkt_amnv = db.Column(db.Integer)
    bkt_amnh = db.Column(db.Integer)
    trx_desc = db.Column(db.Text)
    giro_id = db.Column(db.Integer)
    giro_date = db.Column(db.TIMESTAMP)
    pos_flag = db.Column(db.TIMESTAMP)
    loc_id = db.Column(db.Integer)
    trx_pymnt = db.Column(db.Integer)

    def __init__(self,
                 cus_id,
                 trx_code,
                 trx_date,
                 trx_due,
                 acq_id,
                 acq_date,
                 bkt_id,
                 bkt_date,
                 cur_conv,
                 trx_dbcr,
                 trx_type,
                 pay_type,
                 trx_amnh,
                 trx_amnv,
                 acq_amnh,
                 acq_amnv,
                 bkt_amnv,
                 bkt_amnh,
                 trx_desc,
                 giro_id,
                 giro_date,
                 pos_flag,
                 loc_id,
                 trx_pymnt):
        self.cus_id = cus_id
        self.trx_code = trx_code
        self.trx_date = trx_date
        self.trx_due = trx_due
        self.acq_id = acq_id
        self.acq_date = acq_date
        self.bkt_id = bkt_id
        self.bkt_date = bkt_date
        self.cur_conv = cur_conv
        self.trx_dbcr = trx_dbcr
        self.trx_type = trx_type
        self.pay_type = pay_type
        self.trx_amnh = trx_amnh
        self.trx_amnv = trx_amnv
        self.acq_amnh = acq_amnh
        self.acq_amnv = acq_amnv
        self.bkt_amnv = bkt_amnv
        self.bkt_amnh = bkt_amnh
        self.trx_desc = trx_desc
        self.giro_id = giro_id
        self.giro_date = giro_date
        self.pos_flag = pos_flag
        self.loc_id = loc_id
        self.trx_pymnt = trx_pymnt
