import datetime
from main.shared.shared import db

class PlanHdb(db.Model):
    __table_args__ = {'schema': 'PROD'}
    __tablename__ = 'PLANHDB'

    id = db.Column(db.Integer, primary_key=True)
    pcode = db.Column(db.String(255), unique=True)
    pname = db.Column(db.String(255))
    form_id = db.Column(db.Integer)
    desc = db.Column(db.Text)
    date_created = db.Column(db.TIMESTAMP(timezone=False), default=datetime.datetime.utcnow())
    date_planing = db.Column(db.TIMESTAMP(timezone=False))
    total = db.Column(db.Integer)
    unit = db.Column(db.Integer)
    

    def __init__(self, pcode, pname, form_id, desc, date_planing, total, unit):
        self.pcode = pcode
        self.pname = pname
        self.form_id = form_id
        self.desc = desc
        self.date_planing = date_planing
        self.total = total
        self.unit = unit