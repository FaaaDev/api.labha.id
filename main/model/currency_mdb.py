from flask_sqlalchemy import SQLAlchemy
from main.shared.shared import db
import datetime


class CurrencyMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'CURRMDB'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique = True)
    name = db.Column(db.String(100))
    date = db.Column(db.DATE)
    rate = db.Column(db.Integer)
    

    def __init__(self, code, name, date, rate):
        self.code = code
        self.name = name
        self.date = date
        self.rate = rate