from enum import unique
from main.shared.shared import db

class MemoHdb(db.Model):
    __table_args__ = {'schema': 'GL'}
    __tablename__ = 'MEMOHDB'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), unique=True)
    date = db.Column(db.TIMESTAMP(timezone=False))
    desc = db.Column(db.Text)
    

    def __init__(self, code, date, desc):
        self.code = code
        self.date = date
        self.desc = desc