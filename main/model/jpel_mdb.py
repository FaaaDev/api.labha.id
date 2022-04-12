from enum import unique
from main.shared.shared import db

class JpelMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'CUSTYPEMDB'

    id = db.Column(db.Integer, primary_key=True)
    jpel_code = db.Column(db.String(255), unique=True)
    jpel_name = db.Column(db.String(255))
    jpel_ket = db.Column(db.Text)
    

    def __init__(self, jpel_code, jpel_name, jpel_ket):
        self.jpel_code = jpel_code
        self.jpel_name = jpel_name
        self.jpel_ket = jpel_ket