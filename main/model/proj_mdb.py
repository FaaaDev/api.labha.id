from main.shared.shared import db

class ProjMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'PROJMDB'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    keterangan = db.Column(db.Text)
    

    def __init__(self, name, keterangan):
        self.name = name
        self.keterangan = keterangan