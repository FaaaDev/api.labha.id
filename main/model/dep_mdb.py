from enum import unique
from main.shared.shared import db

class DepMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'DEPMDB'

    id = db.Column(db.Integer, primary_key=True)
    cp_id = db.Column(db.Integer)
    name = db.Column(db.String(255))
    user_id = db.Column(db.Integer)
    

    def __init__(self, cp_id, name, user_id):
        self.cp_id = cp_id
        self.name = name
        self.user_id = user_id