from main.shared.shared import db


class FkpbHdb(db.Model):
    __table_args__ = {'schema': 'AP'}
    __tablename__ = 'FKPBHDB'

    id = db.Column(db.Integer, primary_key=True)
    fk_code = db.Column(db.String(255), unique=True)
    fk_date = db.Column(db.TIMESTAMP)
    ord_id = db.Column(db.Integer)
    fk_tax = db.Column(db.String(255))
    fk_ppn = db.Column(db.Integer)
    fk_lunas = db.Column(db.Integer, default=0)

    def __init__(self, fk_code, fk_date, ord_id, fk_tax, fk_ppn):
        self.fk_code = fk_code
        self.fk_date = fk_date
        self.ord_id = ord_id
        self.fk_tax = fk_tax
        self.fk_ppn = fk_ppn