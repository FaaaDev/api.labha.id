from enum import unique
from ..shared.shared import db


class StCard(db.Model):
    __table_args__ = {'schema': 'public'}
    __tablename__ = 'STCARDMDB'

    id = db.Column(db.Integer, primary_key=True)
    trx_code = db.Column(db.String(255))
    trx_date = db.Column(db.TIMESTAMP)
    trx_dbcr = db.Column(db.String(2))
    trx_type = db.Column(db.String(255))
    trx_seku = db.Column(db.String(3))
    trx_qty = db.Column(db.Integer)
    trx_amnt = db.Column(db.Integer)
    trx_total = db.Column(db.Integer)
    trx_hpok = db.Column(db.Integer)
    trx_sprice = db.Column(db.Integer)
    trx_disc = db.Column(db.Integer)
    prod_id = db.Column(db.Integer)
    loc_id = db.Column(db.Integer)
    scu_code = db.Column(db.Integer)
    flag = db.Column(db.Integer)
    kode_kasir = db.Column(db.Integer)
    

    def __init__(self,
                 trx_code,
                 trx_date,
                 trx_dbcr,
                 trx_type,
                 trx_seku,
                 trx_qty,
                 trx_amnt,
                 trx_total,
                 trx_hpok,
                 trx_sprice,
                 trx_disc,
                 prod_id,
                 loc_id,
                 scu_code,
                 flag,
                 kode_kasir):
        self.trx_code = trx_code
        self.trx_date = trx_date
        self.trx_dbcr = trx_dbcr
        self.trx_type = trx_type
        self.trx_seku = trx_seku
        self.trx_qty = trx_qty
        self.trx_amnt = trx_amnt
        self.trx_total = trx_total
        self.trx_hpok = trx_hpok
        self.trx_sprice = trx_sprice
        self.trx_disc = trx_disc
        self.prod_id = prod_id
        self.loc_id = loc_id
        self.scu_code = scu_code
        self.flag = flag
        self.kode_kasir = kode_kasir
