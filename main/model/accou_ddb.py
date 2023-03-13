from ..shared.shared import db


class AccouDdb(db.Model):
    __table_args__ = {"schema": "GL"}
    __tablename__ = "ACCOUDDB"

    id = db.Column(db.Integer, primary_key=True)
    acc_year = db.Column(db.Integer)
    acc_month = db.Column(db.Integer)
    acc_code = db.Column(db.String(255))
    acc_awal = db.Column(db.Float)
    acc_debit = db.Column(db.Float)
    acc_kredit = db.Column(db.Float)
    acc_akhir = db.Column(db.Float)
    sa = db.Column(db.Boolean)
    from_closing = db.Column(db.Boolean)
    transfer = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

    def __init__(
        self,
        acc_year,
        acc_month,
        acc_code,
        acc_awal,
        acc_debit,
        acc_kredit,
        acc_akhir,
        sa,
        from_closing,
        transfer,
        user_id,
    ):
        self.acc_year = acc_year
        self.acc_month = acc_month
        self.acc_code = acc_code
        self.acc_awal = acc_awal
        self.acc_debit = acc_debit
        self.acc_kredit = acc_kredit
        self.acc_akhir = acc_akhir
        self.sa = sa
        self.from_closing = from_closing
        self.transfer = transfer
        self.user_id = user_id
