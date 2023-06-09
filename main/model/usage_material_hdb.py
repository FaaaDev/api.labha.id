import datetime
from main.shared.shared import db


class UsageMatHdb(db.Model):
    __table_args__ = {"schema": "PROD"}
    __tablename__ = "USAGEHDB"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), unique=True)
    date = db.Column(
        db.TIMESTAMP(timezone=False), default=datetime.datetime.utcnow()
    )
    dep_id = db.Column(db.Integer)
    loc_id = db.Column(db.Integer)
    post = db.Column(db.Boolean)
    closing = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

    def __init__(
        self,
        code,
        date,
        dep_id,
        loc_id,
        user_id,
    ):
        self.code = code
        self.date = date
        self.dep_id = dep_id
        self.loc_id = loc_id
        self.user_id = user_id
