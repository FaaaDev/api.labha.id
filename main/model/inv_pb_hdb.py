from main.shared.shared import db


class InvpbHdb(db.Model):
    __table_args__ = {"schema": "AP"}
    __tablename__ = "INVPBHDB"

    id = db.Column(db.Integer, primary_key=True)
    inv_code = db.Column(db.String(255), unique=True)
    inv_date = db.Column(db.TIMESTAMP)
    ord_id = db.Column(db.Integer)
    inv_tax = db.Column(db.String(255))
    inv_ppn = db.Column(db.Integer)
    inv_lunas = db.Column(db.Integer, default=0)
    inv_desc = db.Column(db.String(255))
    total_bayar = db.Column(db.Float)
    faktur = db.Column(db.Boolean, default=False)
    post = db.Column(db.Boolean, default=False)
    closing = db.Column(db.Boolean, default=False)

    def __init__(self, inv_code, inv_date, ord_id, inv_tax, inv_ppn, inv_desc, total_bayar, faktur):
        self.inv_code = inv_code
        self.inv_date = inv_date
        self.ord_id = ord_id
        self.inv_tax = inv_tax
        self.inv_ppn = inv_ppn
        self.inv_desc = inv_desc
        self.total_bayar = total_bayar
        self.faktur = faktur
