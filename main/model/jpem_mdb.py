from enum import unique
from main.shared.shared import db

class JpemMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'JPEMMDB'

    id = db.Column(db.Integer, primary_key=True)
    jpem_code = db.Column(db.String(255), unique=True)
    jpem_name = db.Column(db.String(255))
    jpem_ket = db.Column(db.Text)
    

    def __init__(self, jpem_code, jpem_name, jpem_ket):
        self.jpem_code = jpem_code
        self.jpem_name = jpem_name
        self.jpem_ket = jpem_ket