import datetime
from main.shared.shared import db


class AkhirMdb(db.Model):
    __table_args__ = {"schema": "GL"}
    __tablename__ = "AKHIRMDB"

    id = db.Column(db.Integer, primary_key=True)
    post_month = db.Column(db.Integer)
    post_year = db.Column(db.Integer)
    closing_date = db.Column(
        db.TIMESTAMP(timezone=False), default=datetime.datetime.utcnow()
    )
    closing_user = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    def __init__(self, post_month, post_year, closing_user, user_id):
        self.post_month = post_month
        self.post_year = post_year
        self.closing_user = closing_user
        self.user_id = user_id
