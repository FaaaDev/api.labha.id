from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from ..shared.shared import db
import datetime


class CustomerMdb(db.Model):
    __table_args__ = {"schema": "master"}
    __tablename__ = "CUSTOMDB"

    id = db.Column(db.Integer, primary_key=True)
    cus_code = db.Column(db.String(20), unique=True)
    cus_name = db.Column(db.String(100))
    cus_jpel = db.Column(db.Integer)
    cus_sub_area = db.Column(db.Integer)
    sub_cus = db.Column(db.Boolean, default=False)
    cus_id = db.Column(db.Integer)
    cus_npwp = db.Column(db.Integer)
    cus_pkp = db.Column(db.Boolean)
    cus_country = db.Column(db.Integer)
    cus_address = db.Column(db.Text)
    cus_kota = db.Column(db.String(100))
    cus_kpos = db.Column(db.Integer)
    cus_telp1 = db.Column(db.String(20))
    cus_telp2 = db.Column(db.String(20))
    cus_email = db.Column(db.String(20))
    cus_fax = db.Column(db.String(20))
    cus_cp = db.Column(db.String(20))
    cus_curren = db.Column(db.Integer)
    cus_pjk = db.Column(db.Integer)
    cus_ket = db.Column(db.Text)
    cus_gl = db.Column(db.Integer)
    cus_uang_muka = db.Column(db.Integer)
    cus_limit = db.Column(db.Integer)

    def __init__(
        self,
        cus_code,
        cus_name,
        cus_jpel,
        cus_sub_area,
        cus_npwp,
        cus_pkp,
        cus_country,
        cus_address,
        cus_kota,
        cus_kpos,
        cus_telp1,
        cus_telp2,
        cus_email,
        cus_fax,
        cus_cp,
        cus_curren,
        cus_pjk,
        cus_ket,
        cus_gl,
        cus_uang_muka,
        cus_limit,
        sub_cus,
        cus_id,
    ):
        self.cus_code = cus_code
        self.cus_name = cus_name
        self.cus_jpel = cus_jpel
        self.cus_sub_area = cus_sub_area
        self.cus_npwp = cus_npwp
        self.cus_pkp = cus_pkp
        self.cus_country = cus_country
        self.cus_address = cus_address
        self.cus_kota = cus_kota
        self.cus_kpos = cus_kpos
        self.cus_telp1 = cus_telp1
        self.cus_telp2 = cus_telp2
        self.cus_email = cus_email
        self.cus_fax = cus_fax
        self.cus_cp = cus_cp
        self.cus_curren = cus_curren
        self.cus_pjk = cus_pjk
        self.cus_ket = cus_ket
        self.cus_gl = cus_gl
        self.cus_uang_muka = cus_uang_muka
        self.cus_limit = cus_limit
        self.sub_cus = sub_cus
        self.cus_id = cus_id
