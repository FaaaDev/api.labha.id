from flask_sqlalchemy import SQLAlchemy
from main.shared.shared import db

class MsnMdb(db.Model):
    __table_args__ = {'schema': 'PROD'}
    __tablename__ = 'MSNMDB'

    id = db.Column(db.Integer, primary_key=True)
    msn_code = db.Column(db.String(100))
    msn_name = db.Column(db.String(100))
    desc = db.Column(db.Text)

    def __init__(self, msn_code, msn_name, desc):
        self.msn_code = msn_code
        self.msn_name = msn_name
        self.desc = desc