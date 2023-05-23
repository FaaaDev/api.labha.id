from enum import unique
from ..shared.shared import db

class MemoHdb(db.Model):
    __table_args__ = {'schema': 'GL'}
    __tablename__ = 'MEMOHDB'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), unique=True)
    date = db.Column(db.TIMESTAMP(timezone=False))
    desc = db.Column(db.Text)
    imp = db.Column(db.Boolean, default = False)
    closing = db.Column(db.Boolean, default = False)
    user_id = db.Column(db.Integer)
    

    def __init__(self, code, date, desc, imp, closing, user_id):
        self.code = code
        self.date = date
        self.desc = desc
        self.imp = imp
        self.closing = closing
        self.user_id = user_id