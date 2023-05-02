from ..shared.shared import db


class IncHdb(db.Model):
    __table_args__ = {"schema": "BNK"}
    __tablename__ = "INCHDB"

    id = db.Column(db.Integer, primary_key=True)
    inc_code = db.Column(db.String(255), unique=True)
    inc_date = db.Column(db.TIMESTAMP)
    type_trx = db.Column(db.Integer)
    acq_cus = db.Column(db.Integer)
    acq_pay = db.Column(db.Integer)
    acq_kas = db.Column(db.Integer)
    bank_ref = db.Column(db.String(255))
    bank_acc = db.Column(db.Integer)
    giro_num = db.Column(db.String(255))
    giro_date = db.Column(db.TIMESTAMP)
    giro_bnk = db.Column(db.Integer)
    inc_type = db.Column(db.Integer)
    inc_kas = db.Column(db.Integer)
    inc_bnk = db.Column(db.Integer)
    inc_dep = db.Column(db.Integer)
    inc_prj = db.Column(db.Integer)
    acc_type = db.Column(db.Integer)
    dp_type = db.Column(db.Integer)
    dp_cus = db.Column(db.Integer)
    dp_kas = db.Column(db.Integer)
    dp_bnk = db.Column(db.Integer)
    approve = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

    def __init__(
        self,
        inc_code,
        inc_date,
        type_trx,
        acq_cus,
        acq_pay,
        acq_kas,
        bank_ref,
        bank_acc,
        giro_num,
        giro_date,
        giro_bnk,
        inc_type,
        inc_kas,
        inc_bnk,
        inc_dep,
        inc_prj,
        acc_type,
        dp_type,
        dp_cus,
        dp_kas,
        dp_bnk,
        approve,
        user_id,
    ):
        self.inc_code = inc_code
        self.inc_date = inc_date
        self.type_trx = type_trx
        self.acq_cus = acq_cus
        self.acq_pay = acq_pay
        self.acq_kas = acq_kas
        self.bank_ref = bank_ref
        self.bank_acc = bank_acc
        self.giro_num = giro_num
        self.giro_date = giro_date
        self.giro_bnk = giro_bnk
        self.inc_type = inc_type
        self.inc_kas = inc_kas
        self.inc_bnk = inc_bnk
        self.inc_dep = inc_dep
        self.inc_prj = inc_prj
        self.acc_type = acc_type
        self.dp_type = dp_type
        self.dp_cus = dp_cus
        self.dp_kas = dp_kas
        self.dp_bnk = dp_bnk
        self.approve = approve
        self.user_id = user_id
