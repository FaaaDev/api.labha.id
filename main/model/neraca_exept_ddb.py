from enum import unique
from ..shared.shared import db

class NeracaEceptionDdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'NRCEXEPTHDB'

    id = db.Column(db.Integer, primary_key=True)
    tittle_id = db.Column(db.Integer)
    accounts = db.Column(db.String(255))
    user_id = db.Column(db.Integer)
    company = db.Column(db.Integer)
    

    def __init__(self, tittle_id, accounts, user_id, company):
        self.tittle_id = tittle_id
        self.accounts = accounts
        self.user_id = user_id
        self.company = company