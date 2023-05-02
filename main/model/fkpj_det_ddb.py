from ..shared.shared import db


class FkpjDetDdb(db.Model):
    __table_args__ = {"schema": "AR"}
    __tablename__ = "FKPJDETDDB"

    id = db.Column(db.Integer, primary_key=True)
    fk_id = db.Column(db.Integer)
    inv_id = db.Column(db.Integer)
    sale_id = db.Column(db.Integer)
    inv_date = db.Column(db.TIMESTAMP)
    total = db.Column(db.Float)
    total_pay = db.Column(db.Float)
    post = db.Column(db.Boolean, default=False)
    closing = db.Column(db.Boolean, default=False)

    def __init__(self, fk_id, inv_id, sale_id, inv_date, total, total_pay):
        self.fk_id = fk_id
        self.inv_id = inv_id
        self.sale_id = sale_id
        self.inv_date = inv_date
        self.total = total
        self.total_pay = total_pay
