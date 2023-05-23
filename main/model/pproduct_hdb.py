import datetime
from main.shared.shared import db

class PproductHdb(db.Model):
    __table_args__ = {'schema': 'PROD'}
    __tablename__ = 'PPHDB'

    id = db.Column(db.Integer, primary_key=True)
    pp_code = db.Column(db.String(255), unique=True)
    pp_date = db.Column(db.TIMESTAMP(timezone=False), default=datetime.datetime.utcnow())
    post = db.Column(db.Boolean, default=False)
    closing = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer)
    

    def __init__(self, pp_code, pp_date, user_id):
        self.pp_code = pp_code
        self.pp_date = pp_date
        self.user_id = user_id
       