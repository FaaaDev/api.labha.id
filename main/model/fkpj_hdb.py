from ..shared.shared import db


class FkpjHdb(db.Model):
    __table_args__ = {'schema': 'AR'}
    __tablename__ = 'FKPJHDB'

    id = db.Column(db.Integer, primary_key=True)
    fk_code = db.Column(db.String(255), unique=True)
    fk_date = db.Column(db.TIMESTAMP)
    pel_id = db.Column(db.Integer)
    fk_tax = db.Column(db.String(255))
    fk_ppn = db.Column(db.Integer)
    fk_lunas = db.Column(db.Integer, default=0)
    fk_desc = db.Column(db.String(255))
    post = db.Column(db.Boolean, default=False)
    closing = db.Column(db.Boolean, default=False)

    def __init__(self, fk_code, fk_date, pel_id, fk_tax, fk_ppn, fk_desc):
        self.fk_code = fk_code
        self.fk_date = fk_date
        self.pel_id = pel_id
        self.fk_tax = fk_tax
        self.fk_ppn = fk_ppn
        self.fk_desc = fk_desc