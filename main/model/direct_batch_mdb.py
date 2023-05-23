import datetime
from main.shared.shared import db


class DirectBatchMdb(db.Model):
    __table_args__ = {"schema": "PROD"}
    __tablename__ = "DRBTCHMDB"

    id = db.Column(db.Integer, primary_key=True)
    bcode = db.Column(db.String(255), unique=True)
    batch_date = db.Column(
        db.TIMESTAMP(timezone=False), default=datetime.datetime.utcnow()
    )
    forml_id = db.Column(db.Integer)
    mat_id = db.Column(db.Integer)
    dep_id = db.Column(db.Integer)
    loc_id = db.Column(db.Integer)
    msn_id = db.Column(db.Integer)
    total = db.Column(db.Integer)
    pb = db.Column(db.Boolean)
    post = db.Column(db.Boolean)
    closing = db.Column(db.Boolean)
    prdc_rm = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

    def __init__(
        self,
        bcode,
        batch_date,
        forml_id,
        mat_id,
        dep_id,
        loc_id,
        msn_id,
        total,
        pb,
        post,
        closing,
        prdc_rm,
        user_id,
    ):
        self.bcode = bcode
        self.batch_date = batch_date
        self.forml_id = forml_id
        self.mat_id = mat_id
        self.dep_id = dep_id
        self.loc_id = loc_id
        self.msn_id = msn_id
        self.total = total
        self.pb = pb
        self.post = post
        self.closing = closing
        self.prdc_rm = prdc_rm
        self.user_id = user_id
