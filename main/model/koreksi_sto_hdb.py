import datetime
from main.shared.shared import db


class KorStoHdb(db.Model):
    __table_args__ = {"schema": "INV"}
    __tablename__ = "KORSTOHDB"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), unique=True)
    date = db.Column(
        db.TIMESTAMP(timezone=False), default=datetime.datetime.utcnow()
    )
    dep_id = db.Column(db.Integer)
    proj_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    def __init__(self, code, date, dep_id, proj_id, user_id):
        self.code = code
        self.date = date
        self.dep_id = dep_id
        self.proj_id = proj_id
        self.user_id = user_id
