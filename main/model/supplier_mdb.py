from flask_sqlalchemy import SQLAlchemy
from main.shared.shared import db


class SupplierMdb(db.Model):
    __table_args__ = {"schema": "master"}
    __tablename__ = "SUPPLMDB"

    id = db.Column(db.Integer, primary_key=True)
    sup_code = db.Column(db.String(20), unique=True)
    sup_name = db.Column(db.String(100))
    sup_jpem = db.Column(db.Integer)
    sup_ppn = db.Column(db.Integer)
    sup_npwp = db.Column(db.String(100))
    sup_pkp = db.Column(db.Boolean)
    sup_country = db.Column(db.Integer)
    sup_address = db.Column(db.Text)
    sup_kota = db.Column(db.String(100))
    sup_kpos = db.Column(db.Integer)
    sup_telp1 = db.Column(db.String(20))
    sup_telp2 = db.Column(db.String(20))
    sup_fax = db.Column(db.String(20))
    sup_cp = db.Column(db.String(20))
    sup_curren = db.Column(db.Integer)
    sup_ket = db.Column(db.Text)
    sup_hutang = db.Column(db.Integer)
    sup_uang_muka = db.Column(db.Integer)
    sup_limit = db.Column(db.Integer)

    def __init__(
        self,
        sup_code,
        sup_name,
        sup_jpem,
        sup_ppn,
        sup_npwp,
        sup_pkp,
        sup_country,
        sup_address,
        sup_kota,
        sup_kpos,
        sup_telp1,
        sup_telp2,
        sup_fax,
        sup_cp,
        sup_curren,
        sup_ket,
        sup_hutang,
        sup_uang_muka,
        sup_limit,
    ):
        self.sup_code = sup_code
        self.sup_name = sup_name
        self.sup_jpem = sup_jpem
        self.sup_ppn = sup_ppn
        self.sup_npwp = sup_npwp
        self.sup_pkp = sup_pkp
        self.sup_country = sup_country
        self.sup_address = sup_address
        self.sup_kota = sup_kota
        self.sup_kpos = sup_kpos
        self.sup_telp1 = sup_telp1
        self.sup_telp2 = sup_telp2
        self.sup_fax = sup_fax
        self.sup_cp = sup_cp
        self.sup_curren = sup_curren
        self.sup_ket = sup_ket
        self.sup_hutang = sup_hutang
        self.sup_uang_muka = sup_uang_muka
        self.sup_limit = sup_limit
