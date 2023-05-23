from flask_sqlalchemy import SQLAlchemy
from ..shared.shared import db
import datetime


class CurrencyDdb(db.Model):
    __table_args__ = {'schema': 'master'}
    __tablename__ = 'CURRDDB'

    id = db.Column(db.Integer, primary_key=True)
    cur_id = db.Column(db.Integer)
    date = db.Column(db.TIMESTAMP)
    rate = db.Column(db.Float)
    comp_id = db.Column(db.Integer)
    

    def __init__(self, cur_id, date, rate, comp_id):
        self.cur_id = cur_id
        self.date = date
        self.rate = rate
        self.comp_id = comp_id