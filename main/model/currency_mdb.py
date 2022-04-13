from flask_sqlalchemy import SQLAlchemy
from main.shared.shared import db
import datetime


class CurrencyMdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'CURRENCYMDB'

    id = db.Column(db.Integer, primary_key=True)
    curren_code = db.Column(db.String(20), unique = True)
    curren_name = db.Column(db.String(100))
    curren_date = db.Column(db.Date)
    curren_rate = db.Column(db.String(200))
    

    def __init__(self, curren_code, curren_name, curren_date, curren_rate):
        self.curren_code = curren_code
        self.curren_name = curren_name
        self.curren_date = curren_date
        self.curren_rate = curren_rate