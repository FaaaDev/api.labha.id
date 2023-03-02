from main.shared.shared import db


class MukapDdb(db.Model):
    __table_args__ = {"schema": "BNK"}
    __tablename__ = "MUKAPDDB"

    id = db.Column(db.Integer, primary_key=True)
    exp_id = db.Column(db.Integer)
    po_id = db.Column(db.Integer)
    t_bayar = db.Column(db.Float)
    value = db.Column(db.Float)
    remain = db.Column(db.Float)
    desc = db.Column(db.Text)

    def __init__(
        self,
        exp_id,
        po_id,
        t_bayar,
        value,
        remain,
        desc,
    ):
        self.exp_id = exp_id
        self.po_id = po_id
        self.t_bayar = t_bayar
        self.value = value
        self.remain = remain
        self.desc = desc
