from email.policy import default
from enum import unique
from main.shared.shared import db


class TransBank(db.Model):
    __table_args__ = {"schema": "BNK"}
    __tablename__ = "TRANSBANK"

    id = db.Column(db.Integer, primary_key=True)
    trx_code = db.Column(db.String(255))
    trx_date = db.Column(db.TIMESTAMP)
    bank_id = db.Column(db.Integer)
    trx_amnt = db.Column(db.Float)
    trx_dbcr = db.Column(db.String(2))
    trx_desc = db.Column(db.Text)
    user_id = db.Column(db.Integer)

    def __init__(
        self, trx_code, trx_date, bank_id, trx_amnt, trx_dbcr, trx_desc, user_id
    ):
        self.trx_code = trx_code
        self.trx_date = trx_date
        self.bank_id = bank_id
        self.trx_amnt = trx_amnt
        self.trx_dbcr = trx_dbcr
        self.trx_desc = trx_desc
        self.user_id = user_id
