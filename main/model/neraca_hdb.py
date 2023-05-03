from enum import unique
from ..shared.shared import db

class NeracaHdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'NERACAHDB'

    id = db.Column(db.Integer, primary_key=True)
    cp_id = db.Column(db.Integer)
    tittle = db.Column(db.String(255))
    type = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    company = db.Column(db.Integer, default=None)
    

    def __init__(self, cp_id, tittle, type, user_id, company):
        self.cp_id = cp_id
        self.tittle = tittle
        self.type = type
        self.user_id = user_id
        self.company = company