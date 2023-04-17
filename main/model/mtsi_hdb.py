import datetime
from ..shared.shared import db


class MtsiHdb(db.Model):
    __table_args__ = {"schema": "INV"}
    __tablename__ = "MTSIHDB"

    id = db.Column(db.Integer, primary_key=True)
    mtsi_code = db.Column(db.String(255), unique=True)
    mtsi_date = db.Column(
        db.TIMESTAMP(timezone=False), default=datetime.datetime.utcnow()
    )
    loc_from = db.Column(db.Integer)
    loc_to = db.Column(db.Integer)
    dep_id = db.Column(db.Integer)
    prj_id = db.Column(db.Integer)
    doc = db.Column(db.String(255))
    doc_date = db.Column(
        db.TIMESTAMP(timezone=False), default=datetime.datetime.utcnow()
    )

    def __init__(self, mtsi_code, mtsi_date, loc_from, loc_to, dep_id, prj_id, doc, doc_date):
        self.mtsi_code = mtsi_code
        self.mtsi_date = mtsi_date
        self.loc_from = loc_from
        self.loc_to = loc_to
        self.dep_id = dep_id
        self.prj_id = prj_id
        self.doc = doc
        self.doc_date = doc_date
