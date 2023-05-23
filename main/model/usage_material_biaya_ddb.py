from enum import unique
from main.shared.shared import db


class UsageMatBiayaDdb(db.Model):
    __table_args__ = {"schema": "PROD"}
    __tablename__ = "UMBIAYADDB"

    id = db.Column(db.Integer, primary_key=True)
    um_id = db.Column(db.Integer)
    acc_id = db.Column(db.Integer)
    value = db.Column(db.Float)
    desc = db.Column(db.Text)

    def __init__(self, um_id, acc_id, value, desc):
        self.um_id = um_id
        self.acc_id = acc_id
        self.value = value
        self.desc = desc
