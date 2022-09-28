from main.shared.shared import db


class IncHdb(db.Model):
    __table_args__ = {'schema': 'BNK'}
    __tablename__ = 'INCHDB'

    id = db.Column(db.Integer, primary_key=True)
    inc_code = db.Column(db.String(255), unique=True)
    inc_date = db.Column(db.TIMESTAMP)
    inc_type = db.Column(db.Integer)
    inc_acc = db.Column(db.Integer)
    inc_dep = db.Column(db.Integer)
    inc_prj = db.Column(db.Integer)
    acq_cus = db.Column(db.Integer)
    acq_pay = db.Column(db.Integer)
    acc_kas = db.Column(db.Integer)
    bank_ref = db.Column(db.String(255))
    bank_id = db.Column(db.Integer)
    giro_num = db.Column(db.String(255))
    giro_date = db.Column(db.TIMESTAMP)
    giro_bnk = db.Column(db.Integer)
    approve = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

    def __init__(self, inc_code, inc_date, inc_type, inc_acc, inc_dep, inc_prj, acq_cus, acq_pay, acc_kas, bank_ref, bank_id, giro_num, giro_date, giro_bnk, approve, user_id):
        self.inc_code = inc_code
        self.inc_date = inc_date
        self.inc_type = inc_type
        self.inc_acc = inc_acc
        self.inc_dep = inc_dep
        self.inc_prj = inc_prj
        self.acq_cus = acq_cus
        self.acq_pay = acq_pay
        self.acc_kas = acc_kas
        self.bank_ref = bank_ref
        self.bank_id = bank_id
        self.giro_num = giro_num
        self.giro_date = giro_date
        self.giro_bnk = giro_bnk
        self.approve = approve
        self.user_id = user_id
