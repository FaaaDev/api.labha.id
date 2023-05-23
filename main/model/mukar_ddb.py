from ..shared.shared import db


class MukarDdb(db.Model):
    __table_args__ = {"schema": "BNK"}
    __tablename__ = "MUKARDDB"

    id = db.Column(db.Integer, primary_key=True)
    inc_id = db.Column(db.Integer)
    so_id = db.Column(db.Integer)
    t_bayar = db.Column(db.Float)
    value = db.Column(db.Float)
    remain = db.Column(db.Float)
    desc = db.Column(db.Text)

    def __init__(
        self,
        inc_id,
        so_id,
        t_bayar,
        value,
        remain,
        desc,
    ):
        self.inc_id = inc_id
        self.so_id = so_id
        self.t_bayar = t_bayar
        self.value = value
        self.remain = remain
        self.desc = desc
