from ..shared.shared import db


class CompMdb(db.Model):
    __table_args__ = {"schema": "master"}
    __tablename__ = "COMPMDB"

    id = db.Column(db.Integer, primary_key=True)
    cp_name = db.Column(db.String(255))
    cp_addr = db.Column(db.Text)
    cp_ship_addr = db.Column(db.Text)
    cp_telp = db.Column(db.String(20))
    cp_email = db.Column(db.String(225))
    cp_webs = db.Column(db.String(100))
    cp_npwp = db.Column(db.String(20))
    cp_coper = db.Column(db.String(20))
    cp_logo = db.Column(db.Text)
    multi_currency = db.Column(db.Boolean)
    appr_po = db.Column(db.Boolean)
    appr_payment = db.Column(db.Boolean)
    over_stock = db.Column(db.Boolean)
    discount = db.Column(db.Boolean)
    tiered = db.Column(db.Boolean)
    rp = db.Column(db.Boolean)
    over_po = db.Column(db.Boolean)
    cutoff = db.Column(db.Integer)
    year_co = db.Column(db.Integer)
    gl_detail = db.Column(db.Boolean)

    def __init__(
        self,
        cp_name,
        cp_addr,
        cp_ship_addr,
        cp_telp,
        cp_email,
        cp_webs,
        cp_npwp,
        cp_coper,
        cp_logo,
        multi_currency,
        appr_po,
        appr_payment,
        over_stock,
        discount,
        tiered,
        rp,
        over_po,
        cutoff,
        year_co,
        gl_detail,
    ):
        self.cp_name = cp_name
        self.cp_addr = cp_addr
        self.cp_ship_addr = cp_ship_addr
        self.cp_telp = cp_telp
        self.cp_email = cp_email
        self.cp_webs = cp_webs
        self.cp_npwp = cp_npwp
        self.cp_coper = cp_coper
        self.cp_logo = cp_logo
        self.multi_currency = multi_currency
        self.appr_po = appr_po
        self.appr_payment = appr_payment
        self.over_stock = over_stock
        self.discount = discount
        self.tiered = tiered
        self.rp = rp
        self.over_po = over_po
        self.cutoff = cutoff
        self.year_co = year_co
        self.gl_detail = gl_detail
