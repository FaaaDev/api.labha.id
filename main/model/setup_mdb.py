from main.shared.shared import db


class SetupMdb(db.Model):
    __table_args__ = {"schema": "master"}
    __tablename__ = "SETUPMDB"

    id = db.Column(db.Integer, primary_key=True)
    cp_id = db.Column(db.Integer)
    ar = db.Column(db.Integer)
    ap = db.Column(db.Integer)
    pnl = db.Column(db.Integer)
    pnl_year = db.Column(db.Integer)
    rtn_income = db.Column(db.Integer)
    sls_rev = db.Column(db.Integer)
    sls_disc = db.Column(db.Integer)
    sls_retur = db.Column(db.Integer)
    sls_shipping = db.Column(db.Integer)
    sls_prepaid = db.Column(db.Integer)
    sls_unbill = db.Column(db.Integer)
    sls_unbill_recv = db.Column(db.Integer)
    sls_tax = db.Column(db.Integer)
    pur_cogs = db.Column(db.Integer)
    pur_discount = db.Column(db.Integer)
    pur_shipping = db.Column(db.Integer)
    pur_retur = db.Column(db.Integer)
    pur_advance = db.Column(db.Integer)
    pur_unbill = db.Column(db.Integer)
    pur_tax = db.Column(db.Integer)
    sto = db.Column(db.Integer)
    sto_broken = db.Column(db.Integer)
    sto_general = db.Column(db.Integer)
    sto_production = db.Column(db.Integer)
    sto_hpp_diff = db.Column(db.Integer)
    sto_wip = db.Column(db.Integer)
    sto_bb = db.Column(db.Integer)
    sto_bbp = db.Column(db.Integer)
    fixed_assets = db.Column(db.Integer)

    def __init__(
        self,
        cp_id,
        ar,
        ap,
        pnl,
        pnl_year,
        rtn_income,
        sls_rev,
        sls_disc,
        sls_retur,
        sls_shipping,
        sls_prepaid,
        sls_unbill,
        sls_unbill_recv,
        sls_tax,
        pur_cogs,
        pur_discount,
        pur_shipping,
        pur_retur,
        pur_advance,
        pur_unbill,
        pur_tax,
        sto,
        sto_broken,
        sto_general,
        sto_production,
        sto_hpp_diff,
        sto_wip,
        sto_bb,
        sto_bbp,
        fixed_assets,
    ):
        self.cp_id = cp_id
        self.ar = ar
        self.ap = ap
        self.pnl = pnl
        self.pnl_year = pnl_year
        self.rtn_income = rtn_income
        self.sls_rev = sls_rev
        self.sls_disc = sls_disc
        self.sls_retur = sls_retur
        self.sls_shipping = sls_shipping
        self.sls_prepaid = sls_prepaid
        self.sls_unbill = sls_unbill
        self.sls_unbill_recv = sls_unbill_recv
        self.sls_tax = sls_tax
        self.pur_cogs = pur_cogs
        self.pur_discount = pur_discount
        self.pur_shipping = pur_shipping
        self.pur_retur = pur_retur
        self.pur_advance = pur_advance
        self.pur_unbill = pur_unbill
        self.pur_tax = pur_tax
        self.sto = sto
        self.sto_broken = sto_broken
        self.sto_general = sto_general
        self.sto_production = sto_production
        self.sto_hpp_diff = sto_hpp_diff
        self.sto_wip = sto_wip
        self.sto_bb = sto_bb
        self.sto_bbp = sto_bbp
        self.fixed_assets = fixed_assets
