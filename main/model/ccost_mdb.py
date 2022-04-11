from main.shared.shared import db

class CcostMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'CCOSTMDB'

    id = db.Column(db.Integer, primary_key=True)
    ccost_code = db.Column(db.String(255), unique=True)
    ccost_name = db.Column(db.String(255))
    ccost_ket = db.Column(db.Text)
    

    def __init__(self, code, name, keterangan):
        self.ccost_code = code
        self.ccost_name = name
        self.ccost_ket = keterangan