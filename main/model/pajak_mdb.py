from enum import unique
from ..shared.shared import db

class PajakMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'PAJAKMDB'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255))
    name = db.Column(db.String(255))
    nilai = db.Column(db.Integer)
    cutting = db.Column(db.Boolean)
    acc_sls_tax = db.Column(db.Integer)
    acc_pur_tax = db.Column(db.Integer)
    combined = db.Column(db.String(255))
    

    def __init__(self, type, name, nilai, cutting, acc_sls_tax, acc_pur_tax, combined):
        self.type = type
        self.name = name
        self.nilai = nilai
        self.cutting = cutting
        self.acc_sls_tax = acc_sls_tax
        self.acc_pur_tax = acc_pur_tax
        self.combined = combined