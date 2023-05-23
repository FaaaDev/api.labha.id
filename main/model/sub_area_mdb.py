from enum import unique
from ..shared.shared import db

class SubAreaMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'SUBAREAMDB'

    id = db.Column(db.Integer, primary_key=True)
    sub_code = db.Column(db.String(255), unique=True)
    sub_area_code = db.Column(db.Integer)
    sub_name = db.Column(db.String(255))
    sub_ket = db.Column(db.Text)
    

    def __init__(self, sub_code, sub_area_code, sub_name, sub_ket):
        self.sub_code = sub_code
        self.sub_area_code = sub_area_code
        self.sub_name = sub_name
        self.sub_ket = sub_ket