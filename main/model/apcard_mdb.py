from enum import unique
from main.shared.shared import db


class ApCard(db.Model):
    __table_args__ = {"schema": "AP"}
    __tablename__ = "APCARDMDB"

    id = db.Column(db.Integer, primary_key=True)
    trx_code = db.Column(db.String(255))
    sup_id = db.Column(db.Integer)
    ord_id = db.Column(db.Integer)
    ord_date = db.Column(db.TIMESTAMP)
    ord_due = db.Column(db.TIMESTAMP)
    po_id = db.Column(db.Integer)
    acq_id = db.Column(db.Integer)
    acq_date = db.Column(db.TIMESTAMP)
    cur_conv = db.Column(db.Integer)
    trx_dbcr = db.Column(db.String(2))
    trx_type = db.Column(db.String(255))
    pay_type = db.Column(db.String(255))
    trx_amnh = db.Column(db.Integer)
    trx_amnv = db.Column(db.Integer)
    acq_amnh = db.Column(db.Integer)
    acq_amnv = db.Column(db.Integer)
    giro_id = db.Column(db.Integer)
    giro_date = db.Column(db.TIMESTAMP)
    sa_id = db.Column(db.Integer)
    sa = db.Column(db.Boolean, default=False)
    lunas = db.Column(db.Boolean, default=False)

    def __init__(
        self,
        trx_code,
        sup_id,
        ord_id,
        ord_date,
        ord_due,
        po_id,
        acq_id,
        acq_date,
        cur_conv,
        trx_dbcr,
        trx_type,
        pay_type,
        trx_amnh,
        trx_amnv,
        acq_amnh,
        acq_amnv,
        giro_id,
        giro_date,
        sa_id,
        sa,
    ):

        self.trx_code = trx_code
        self.sup_id = sup_id
        self.ord_id = ord_id
        self.ord_date = ord_date
        self.ord_due = ord_due
        self.po_id = po_id
        self.acq_id = acq_id
        self.acq_date = acq_date
        self.cur_conv = cur_conv
        self.trx_dbcr = trx_dbcr
        self.trx_type = trx_type
        self.pay_type = pay_type
        self.trx_amnh = trx_amnh
        self.trx_amnv = trx_amnv
        self.acq_amnh = acq_amnh
        self.acq_amnv = acq_amnv
        self.giro_id = giro_id
        self.giro_date = giro_date
        self.sa_id = sa_id
        self.sa = sa
