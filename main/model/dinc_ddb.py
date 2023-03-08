from main.shared.shared import db


class IncDdb(db.Model):
    __table_args__ = {"schema": "BNK"}
    __tablename__ = "INCDDB"

    id = db.Column(db.Integer, primary_key=True)
    inc_id = db.Column(db.Integer)
    acc_code = db.Column(db.Integer)
    acc_bnk = db.Column(db.Integer)
    bnk_code = db.Column(db.Integer)
    value = db.Column(db.Float)
    fc = db.Column(db.Float)
    desc = db.Column(db.Text)

    def __init__(self, inc_id, acc_code, acc_bnk, bnk_code, value, fc, desc):
        self.inc_id = inc_id
        self.acc_code = acc_code
        self.acc_bnk = acc_bnk
        self.bnk_code = bnk_code
        self.value = value
        self.fc = fc
        self.desc = desc
