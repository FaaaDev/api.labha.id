
from main.shared.shared import db


class AccouMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'ACCOUMDB'

    id = db.Column(db.Integer, primary_key=True)
    acc_code = db.Column(db.String(255), unique=True)
    acc_name = db.Column(db.String(255))
    umm_code = db.Column(db.String(255))
    kat_code = db.Column(db.Integer)
    dou_type = db.Column(db.String(10))
    sld_type = db.Column(db.String(10))
    connect = db.Column(db.Boolean)
    sld_awal = db.Column(db.Integer)
    level = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    comp_id = db.Column(db.Integer)

    def __init__(self, acc_code, acc_name, umm_code, kat_code, dou_type, sld_type, connect, sld_awal, level, user_id, comp_id):
        self.acc_code = acc_code
        self.acc_name = acc_name
        self.umm_code = umm_code
        self.kat_code = kat_code
        self.dou_type = dou_type
        self.sld_type = sld_type
        self.connect = connect
        self.sld_awal = sld_awal
        self.level = level
        self.user_id = user_id
        self.comp_id = comp_id
