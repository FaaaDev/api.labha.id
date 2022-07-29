import datetime
from main.shared.shared import db

class FprdcHdb(db.Model):
    __table_args__ = {'schema': 'PROD'}
    __tablename__ = 'FPRDCHDB'

    id = db.Column(db.Integer, primary_key=True)
    fcode = db.Column(db.String(255), unique=True)
    fname = db.Column(db.String(255))
    version = db.Column(db.Float)
    rev = db.Column(db.Float)
    desc = db.Column(db.Text)
    date_created = db.Column(db.TIMESTAMP(timezone=False), default=datetime.datetime.utcnow())
    date_updated = db.Column(db.TIMESTAMP(timezone=False), default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())
    active = db.Column(db.Boolean)
    

    def __init__(self, fcode, fname, version, rev, desc, active):
        self.fcode = fcode
        self.fname = fname
        self.version = version
        self.rev = rev
        self.desc = desc
        self.active = active