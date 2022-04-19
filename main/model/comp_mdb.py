from main.shared.shared import db

class CompMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'COMPMDB'

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
    

    def __init__(self, cp_name, cp_addr, cp_ship_addr, cp_telp, cp_email, cp_webs, cp_npwp, cp_coper, cp_logo, multi_currency, appr_po, appr_payment):
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