from ..shared.shared import db

class KategMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'KATEGMDB'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    kode_klasi = db.Column(db.Integer)
    kode_saldo = db.Column(db.String(10))
    imp = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)
    comp_id = db.Column(db.Integer)
    

    def __init__(self,id,  name, kode_klasi, kode_saldo, imp, user_id, comp_id):
        self.id = id
        self.name = name
        self.kode_klasi = kode_klasi
        self.kode_saldo = kode_saldo
        self.imp = imp
        self.user_id = user_id
        self.comp_id = comp_id
