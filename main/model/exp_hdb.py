from main.shared.shared import db


class ExpHdb(db.Model):
    __table_args__ = {'schema': 'BNK'}
    __tablename__ = 'EXPHDB'

    id = db.Column(db.Integer, primary_key=True)
    exp_code = db.Column(db.String(255), unique=True)
    exp_date = db.Column(db.TIMESTAMP)
    exp_type = db.Column(db.Integer)
    exp_acc = db.Column(db.Integer)
    exp_dep = db.Column(db.Integer)
    exp_prj = db.Column(db.Integer)
    acq_sup = db.Column(db.Integer)
    acq_pay = db.Column(db.Integer)
    kas_acc = db.Column(db.Integer)
    bank_acc = db.Column(db.Integer)
    bank_id = db.Column(db.Integer)
    bank_ref = db.Column(db.String(255))
    giro_num = db.Column(db.String(255))
    giro_date = db.Column(db.TIMESTAMP)
    approve = db.Column(db.Boolean)

    def __init__(self, exp_code, exp_date, exp_type, exp_acc, exp_dep, exp_prj, acq_sup, acq_pay, kas_acc, bank_acc, bank_id, bank_ref, giro_num, giro_date, approve):
        self.exp_code = exp_code
        self.exp_date = exp_date
        self.exp_type = exp_type
        self.exp_acc = exp_acc
        self.exp_dep = exp_dep
        self.exp_prj = exp_prj
        self.acq_sup = acq_sup
        self.acq_pay = acq_pay
        self.kas_acc = kas_acc
        self.bank_acc = bank_acc
        self.bank_id = bank_id
        self.bank_ref = bank_ref
        self.giro_num = giro_num
        self.giro_date = giro_date
        self.approve = approve
