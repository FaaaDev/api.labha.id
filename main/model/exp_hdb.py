from main.shared.shared import db


class ExpHdb(db.Model):
    __table_args__ = {"schema": "BNK"}
    __tablename__ = "EXPHDB"

    id = db.Column(db.Integer, primary_key=True)
    exp_code = db.Column(db.String(255), unique=True)
    exp_date = db.Column(db.TIMESTAMP)
    type_trx = db.Column(db.Integer)
    acq_sup = db.Column(db.Integer)
    acq_pay = db.Column(db.Integer)
    acq_kas = db.Column(db.Integer)
    bank_ref = db.Column(db.String(255))
    bank_acc = db.Column(db.Integer)
    giro_num = db.Column(db.String(255))
    giro_date = db.Column(db.TIMESTAMP)
    bank_id = db.Column(db.Integer)
    exp_type = db.Column(db.Integer)
    kas_acc = db.Column(db.Integer)
    exp_bnk = db.Column(db.Integer)
    type_acc = db.Column(db.Integer)
    exp_dep = db.Column(db.Integer)
    exp_prj = db.Column(db.Integer)
    dp_type = db.Column(db.Integer)
    dp_sup = db.Column(db.Integer)
    dp_kas = db.Column(db.Integer)
    dp_bnk = db.Column(db.Integer)
    approve = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

    def __init__(
        self,
        exp_code,
        exp_date,
        type_trx,
        acq_sup,
        acq_pay,
        acq_kas,
        bank_ref,
        bank_acc,
        giro_num,
        giro_date,
        bank_id,
        exp_type,
        kas_acc,
        exp_bnk,
        type_acc,
        exp_dep,
        exp_prj,
        dp_type,
        dp_sup,
        dp_kas,
        dp_bnk,
        approve,
        user_id,
    ):
        self.exp_code = exp_code
        self.exp_date = exp_date
        self.type_trx = type_trx
        self.acq_sup = acq_sup
        self.acq_pay = acq_pay
        self.acq_kas = acq_kas
        self.bank_ref = bank_ref
        self.bank_acc = bank_acc
        self.giro_num = giro_num
        self.giro_date = giro_date
        self.bank_id = bank_id
        self.exp_type = exp_type
        self.kas_acc = kas_acc
        self.exp_bnk = exp_bnk
        self.type_acc = type_acc
        self.exp_dep = exp_dep
        self.exp_prj = exp_prj
        self.dp_type = dp_type
        self.dp_sup = dp_sup
        self.dp_kas = dp_kas
        self.dp_bnk = dp_bnk
        self.approve = approve
        self.user_id = user_id
