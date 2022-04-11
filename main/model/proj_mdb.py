from enum import unique
from main.shared.shared import db

class ProjMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'PROJMDB'

    id = db.Column(db.Integer, primary_key=True)
    proj_code = db.Column(db.String(255), unique=True)
    proj_name = db.Column(db.String(255))
    proj_ket = db.Column(db.Text)
    

    def __init__(self, proj_code, proj_name, proj_ket):
        self.proj_code = proj_code
        self.proj_name = proj_name
        self.proj_ket = proj_ket