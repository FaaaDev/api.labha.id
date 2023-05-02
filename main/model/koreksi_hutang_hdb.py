from ..shared.shared import db


class KorHutangHdb(db.Model):
    __table_args__ = {"schema": "BNK"}
    __tablename__ = "DEBTHDB"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), unique=True)
    date = db.Column(db.TIMESTAMP)
    sup_id = db.Column(db.Integer)
    tipe = db.Column(db.String(5))
    acc_lwn = db.Column(db.Integer)
    value = db.Column(db.Integer)
    due_date = db.Column(db.TIMESTAMP)
    desc = db.Column(db.Text)
    user_id = db.Column(db.Integer)

    def __init__(
        self, code, date, sup_id, tipe, acc_lwn, value, due_date, desc, user_id
    ):
        self.code = code
        self.date = date
        self.sup_id = sup_id
        self.tipe = tipe
        self.acc_lwn = acc_lwn
        self.value = value
        self.due_date = due_date
        self.desc = desc
        self.user_id = user_id
