from ..shared.shared import db

class KategMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'KATEGMDB'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    kode_klasi = db.Column(db.Integer)
    kode_saldo = db.Column(db.String(10))
    imp = db.Column(db.Boolean)
    

    def __init__(self,id,  name, kode_klasi, kode_saldo, imp):
        self.id = id
        self.name = name
        self.kode_klasi = kode_klasi
        self.kode_saldo = kode_saldo
        self.imp = imp