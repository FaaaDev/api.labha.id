from enum import unique
from main.shared.shared import db

class JasaMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'JASAMDB'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    desc = db.Column(db.Text)
    acc_id = db.Column(db.Integer)
    

    def __init__(self, code, name, desc, acc_id):
        self.code = code
        self.name = name
        self.desc = desc
        self.acc_id = acc_id