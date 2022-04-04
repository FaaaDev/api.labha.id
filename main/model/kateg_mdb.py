from main.shared.shared import db

class KategMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'KATEGMDB'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    kode_klasi = db.Column(db.Integer)
    kode_saldo = db.Column(db.String(10))
    

    def __init__(self, name, kode_klasi, kode_saldo):
        self.name = name
        self.kode_klasi = kode_klasi
        self.kode_saldo = kode_saldo