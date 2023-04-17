from ..shared.shared import db


class InvDdb(db.Model):
    __table_args__ = {"schema": "INV"}
    __tablename__ = "INVENDDB"

    id = db.Column(db.Integer, primary_key=True)
    inv_year = db.Column(db.Integer)
    inv_month = db.Column(db.Integer)
    inv_code = db.Column(db.String(255))
    loc_code = db.Column(db.String(255))
    inv_awal = db.Column(db.Float)
    inv_debit = db.Column(db.Float)
    inv_kredit = db.Column(db.Float)
    inv_akhir = db.Column(db.Float)
    qty_awal = db.Column(db.Integer)
    qty_debit = db.Column(db.Integer)
    qty_kredit = db.Column(db.Integer)
    qty_akhir = db.Column(db.Integer)
    hpp = db.Column(db.Float)
    sa = db.Column(db.Boolean)
    from_closing = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

    def __init__(
        self,
        inv_year,
        inv_month,
        inv_code,
        loc_code,
        inv_awal,
        inv_debit,
        inv_kredit,
        inv_akhir,
        qty_awal,
        qty_debit,
        qty_kredit,
        qty_akhir,
        hpp,
        sa,
        from_closing,
        user_id,
    ):
        self.inv_year = inv_year
        self.inv_month = inv_month
        self.inv_code = inv_code
        self.loc_code = loc_code
        self.inv_awal = inv_awal
        self.inv_debit = inv_debit
        self.inv_kredit = inv_kredit
        self.inv_akhir = inv_akhir
        self.qty_awal = qty_awal
        self.qty_debit = qty_debit
        self.qty_kredit = qty_kredit
        self.qty_akhir = qty_akhir
        self.hpp = hpp
        self.sa = sa
        self.from_closing = from_closing
        self.user_id = user_id
