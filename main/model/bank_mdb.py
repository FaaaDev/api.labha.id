from flask_sqlalchemy import SQLAlchemy
from main.shared.shared import db
import datetime


class BankMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'BANK_MDB'

    id = db.Column(db.Integer, primary_key=True)
    BANK_CODE = db.Column(db.String(20), unique = True)
    BANK_NAME = db.Column(db.String(100))
    BANK_DESC = db.Column(db.String(120))
    acc_id = db.Column(db.Integer)
    user_entry = db.Column(db.Integer)
    entry_date = db.Column(db.TIMESTAMP(timezone=False), default=datetime.datetime.utcnow())
    user_edit = db.Column(db.Integer)
    edit_date = db.Column(db.TIMESTAMP(timezone=False), default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())



    def __init__(self, BANK_CODE, BANK_NAME, BANK_DESC, BANK_ACC, user_entry, user_edit):
        self.BANK_CODE = BANK_CODE
        self.BANK_NAME = BANK_NAME
        self.BANK_DESC = BANK_DESC
        self.acc_id = BANK_ACC
        self.user_entry = user_entry
        self.user_edit = user_edit